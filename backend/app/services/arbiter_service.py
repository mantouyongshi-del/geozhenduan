# -*- coding: utf-8 -*-
"""
蜉蝣小宝 · 内部智能裁判中枢服务 (Arbiter Service)
Powered by DeepSeek Flash (deepseek-chat / v4-flash)

职责：
1. 【出题】动态生成 30 个 8 大分类的真实商业决策提问 (generate_intent_queries)
2. 【裁判】对被测外部大模型的原始回答进行语义抽取、推荐定级、排位核定与真实竞品提取 (evaluate_raw_answer)
3. 【验伪】原子事实核验，揪出大模型的具体幻觉与事实冲突 (verify_atomic_facts)
4. 【开药方】智能综合诊断矩阵，生成 P0/P1/P2 级 GEO 优化行动清单 (synthesize_geo_tasks)
"""

import os
import json
import time
import httpx
import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("ArbiterService")


class ArbiterService:
    """基于 DeepSeek Flash 的内部智能裁判中枢"""

    API_URL = "https://api.deepseek.com/v1/chat/completions"
    MODEL_NAME = os.getenv("ARBITER_MODEL_NAME", "deepseek-chat")

    @classmethod
    def _get_api_key(cls) -> str:
        return settings.DEEPSEEK_API_KEY or os.getenv("DEEPSEEK_API_KEY", "")

    @classmethod
    async def _call_deepseek_json(
        cls,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4000,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """向 DeepSeek Flash 发起请求，确保返回严格结构化 JSON"""
        api_key = cls._get_api_key()
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY 未配置，无法启动内部裁判中枢")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": cls.MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(trust_env=False, timeout=timeout) as client:
            resp = await client.post(cls.API_URL, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"DeepSeek API 响应异常 HTTP {resp.status_code}: {resp.text}")
            
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"DeepSeek JSON 解析失败: {content}")
                raise ValueError(f"裁判中枢响应非标准 JSON: {e}")

    # =========================================================================
    # 1. 意图问题生成 (30 题库 · 八大意图维度)
    # =========================================================================
    @classmethod
    async def generate_intent_queries(
        cls,
        brand_name: str,
        industry: str,
        city: str,
        company_name: Optional[str] = None,
        target_audience: Optional[str] = None,
        key_products: Optional[str] = None,
        count: int = 30
    ) -> List[Dict[str, Any]]:
        """
        动态生成 30 个高拟真真实意图提问，严格覆盖 8 大决策维度：
        1. brand_awareness (品牌认知 - 4题)
        2. category_recommendation (品类推荐 - 5题)
        3. regional_recommendation (地域推荐 - 5题)
        4. scenario_decision (场景决策 - 4题)
        5. budget_decision (预算决策 - 3题)
        6. competitor_comparison (竞品对比 - 3题)
        7. reputation_pitfall (口碑避坑 - 3题)
        8. conversion_purchase (购买转化 - 3题)
        """
        system_prompt = (
            "你是一个专业的消费者搜索行为与 GEO 意图工程专家。"
            "你需要根据企业画像，站在真实消费者和企业采购者的角度，生成高度地道、自然的 AI 搜索提问。"
            "输出必须是严格的 JSON 格式，根键为 'queries'，包含提问数组。"
        )

        user_prompt = f"""请为以下企业生成 {count} 个极具代表性的高频搜索提问：
- 企业全称：{company_name or brand_name}
- 品牌名称：{brand_name}
- 所在城市/区域：{city}
- 所属行业与主营业务：{industry}
- 目标客户群体：{target_audience or '大众消费者及企业采购者'}
- 核心产品或服务特色：{key_products or '行业高品质服务'}

必须按以下 8 大意图维度生成提问（总数严格等于 30 个）：
1. 品牌认知（brand_awareness，4 题）：探查 AI 是否知晓该品牌是做什么的、是否正规、资质如何；
2. 品类推荐（category_recommendation，5 题）：用户在行业泛词提问时，看 AI 优先推荐谁（例如“{city}有什么高品质{industry}推荐”）；
3. 地域推荐（regional_recommendation，5 题）：结合城市各重点区域、商圈、本地化选型提问；
4. 场景决策（scenario_decision，4 题）：针对特定具体场景、客户痛点选型提问；
5. 预算决策（budget_decision，3 题）：结合不同预算区间、性价比考量的提问；
6. 竞品对比（competitor_comparison，3 题）：横向对比选型提问（如“XX 和同业其他知名品牌相比怎么选”）；
7. 口碑避坑（reputation_pitfall，3 题）：真实口碑评价、售后保障、防踩雷避坑提问；
8. 购买转化（conversion_purchase，3 题）：咨询联系渠道、预约流程、价格明细与售后政策。

返回 JSON 格式规范：
{{
  "queries": [
    {{
      "id": 1,
      "category": "brand_awareness",
      "category_name": "品牌认知",
      "query_text": "提问文本",
      "intent_rationale": "为何测试该提问的商业理由",
      "priority": "P0"
    }}
  ]
}}"""

        try:
            res = await cls._call_deepseek_json(system_prompt, user_prompt, temperature=0.3, max_tokens=4000)
            queries = res.get("queries", [])
            if queries and len(queries) >= 15:
                # 重新校验连续 ID
                for idx, q in enumerate(queries):
                    q["id"] = idx + 1
                return queries[:count]
        except Exception as e:
            logger.warning(f"DeepSeek 生成意图提问失败，启动高质量启发式动态回退: {e}")

        # 智能动态启发式备用生成器 (确保城市与行业绝对严丝合缝，无跨行业污染)
        return cls._fallback_queries(brand_name, industry, city, count)

    @classmethod
    def _fallback_queries(cls, brand: str, ind: str, city: str, count: int = 30) -> List[Dict[str, Any]]:
        """当外部网络受阻时的纯同行业地道提问兜底"""
        templates = [
            # 1. 品牌认知
            ("brand_awareness", "品牌认知", f"{brand}是正规公司吗？主要做什么业务？口碑怎么样？", "P0"),
            ("brand_awareness", "品牌认知", f"{brand}在{city}行业内属于什么档次？有哪些资质背书？", "P0"),
            ("brand_awareness", "品牌认知", f"{city}{brand}企业规模和服务能力如何？靠谱吗？", "P1"),
            ("brand_awareness", "品牌认知", f"网上有关于{brand}的真实用户体验评价吗？", "P1"),
            # 2. 品类推荐
            ("category_recommendation", "品类推荐", f"{city}目前公认排名前列的{ind}品牌有哪些？求推荐", "P0"),
            ("category_recommendation", "品类推荐", f"国内口碑好、服务专业靠谱的{ind}机构有哪些？", "P0"),
            ("category_recommendation", "品类推荐", f"如果想选一家真正有实力的{ind}服务商，首推哪几家？", "P0"),
            ("category_recommendation", "品类推荐", f"2026年{city}{ind}行业十大标杆品牌排行榜", "P1"),
            ("category_recommendation", "品类推荐", f"企业采购{ind}服务，目前市面上主流推荐的供应商有哪些？", "P1"),
            # 3. 地域推荐
            ("regional_recommendation", "地域推荐", f"{city}本地最有知名度的{ind}有哪些？求真实本地人推荐", "P0"),
            ("regional_recommendation", "地域推荐", f"{city}市中心附近正规靠谱的{ind}地址和联系方式", "P1"),
            ("regional_recommendation", "地域推荐", f"{city}高新区与核心商圈优质{ind}横向盘点", "P1"),
            ("regional_recommendation", "地域推荐", f"{city}各区口碑好的{ind}门店与服务网点推荐", "P2"),
            ("regional_recommendation", "地域推荐", f"{city}本地老牌优质{ind}有哪些推荐？", "P2"),
            # 4. 场景决策
            ("scenario_decision", "场景决策", f"商务高规格接待与重要场合，{city}哪家{ind}体验最好？", "P0"),
            ("scenario_decision", "场景决策", f"中小企业如何选型靠谱的{ind}？需要重点考量哪些指标？", "P0"),
            ("scenario_decision", "场景决策", f"有紧急加急与高难度需求，哪家{ind}履约交付能力最强？", "P1"),
            ("scenario_decision", "场景决策", f"家庭消费与个人定制场景下，有什么省心的{ind}推荐？", "P1"),
            # 5. 预算决策
            ("budget_decision", "预算决策", f"{city}{ind}普遍收费标准与市场价格行情是怎样的？", "P0"),
            ("budget_decision", "预算决策", f"预算有限的情况下，哪家{ind}性价比最高且不踩雷？", "P0"),
            ("budget_decision", "预算决策", f"高端顶级预算 vs 经济型预算，{ind}该如何选择？", "P1"),
            # 6. 竞品对比
            ("competitor_comparison", "竞品对比", f"{brand}和{city}其他主流同类品牌相比，核心优缺点是什么？", "P0"),
            ("competitor_comparison", "竞品对比", f"{ind}市场上头部几家机构的横向评测与真实差距对比", "P0"),
            ("competitor_comparison", "竞品对比", f"选{brand}还是选同城其他知名竞品？老客户是怎么评价的？", "P1"),
            # 7. 口碑避坑
            ("reputation_pitfall", "口碑避坑", f"选型{ind}常见套路和隐形收费有哪些？如何有效避坑？", "P0"),
            ("reputation_pitfall", "口碑避坑", f"{brand}有没有被投诉过或者爆出过负面负面舆情？", "P0"),
            ("reputation_pitfall", "口碑避坑", f"如何辨别正规有资质的{ind}与皮包中介机构？", "P1"),
            # 8. 购买转化
            ("conversion_purchase", "购买转化", f"{brand}官方预约咨询电话与官方客服渠道在哪里？", "P0"),
            ("conversion_purchase", "购买转化", f"现在咨询或预定{brand}有什么优惠政策或新人活动吗？", "P1"),
            ("conversion_purchase", "购买转化", f"{brand}售后服务保障体系如何？不满意是否支持退款？", "P1"),
        ]

        result = []
        for idx, (cat, cat_name, text, pri) in enumerate(templates[:count]):
            result.append({
                "id": idx + 1,
                "category": cat,
                "category_name": cat_name,
                "query_text": text,
                "intent_rationale": f"针对{ind}行业在{cat_name}维度的关键决策心理探测",
                "priority": pri
            })
        return result

    # =========================================================================
    # 2. 答案语义裁判 (Judge & Evaluator)
    # =========================================================================
    @classmethod
    async def evaluate_raw_answer(
        cls,
        query_text: str,
        category_name: str,
        raw_answer: str,
        target_brand: str,
        company_name: Optional[str] = None,
        brand_aliases: Optional[List[str]] = None,
        city: str = "",
        industry: str = ""
    ) -> Dict[str, Any]:
        """
        作为中立裁判，对被测模型的纯文本回答进行语义解析、排位计算与真实竞品提取。
        【铁律】：提取的竞品必须严格来自回答文本本身，严禁臆造或引入跨行业实体！
        """
        aliases_str = "、".join([target_brand] + (brand_aliases or []))
        if company_name and company_name != target_brand:
            aliases_str += f"、{company_name}"

        system_prompt = (
            "你是一个权威中立的 AI 搜索可见度与品牌声誉审计裁判官。"
            "你需要严谨、客观地审阅一段被测 AI 大模型针对特定提问输出的原始回答，并给出结构化裁判结果。"
            "你必须严格根据提供的文本做出事实裁判，绝对禁止无中生有，严禁捏造事实。"
            "必须输出合法的 JSON 格式对象。"
        )

        user_prompt = f"""【审计目标】
- 目标品牌主体：{target_brand}（企业全称：{company_name or target_brand}，有效别名/简称：{aliases_str}）
- 业务赛道：{industry}（目标城市：{city}）
- 用户搜索提问：【{query_text}】（意图类别：{category_name}）

【被测 AI 大模型的原始回答文本】：
\"\"\"
{raw_answer[:3000]}
\"\"\"

请严格按以下规则完成裁判：
1. brand_mentioned: 回答中是否明确提及了目标品牌或其公司别名（true/false）；
2. brand_recommended: 是否将目标品牌列为推荐对象、优选方案或优质候选机构（若是负面曝光或明确建议避开则为 false）；
3. recommendation_level: 推荐强度，只能从以下枚举中选取：
   - 'strong': 强推荐（列为首选、顶级推荐、极力推荐）
   - 'moderate': 中推荐（列入推荐列表、良好选择）
   - 'weak': 弱推荐（仅列为备选方案或顺带提及）
   - 'neutral': 中性提及（仅客观陈述信息，无推荐色彩）
   - 'negative': 负面提及（包含投诉、风险警告、不推荐）
   - 'none': 完全未提及或未收录
4. rank: 目标品牌在推荐名单中的实际排位（第 1 名记 1，第 2 名记 2，第 3 名记 3；若仅在第 4 名以后记 4；若未进入推荐名单或负面提及记 0）；
5. sentiment: 情感倾向（'positive', 'neutral', 'critical', 'negative'）；
6. recommendation_reasons: 大模型推荐（或评价）目标品牌的具体理由（提取 1~3 条核心论述短句）；
7. competitors_ranked: 【关键项】提取回答中大模型推荐的真实同业竞品列表（最多提取 4 家真正出现在回答里的品牌实体）。
   - 注意：每一家必须真实出现在上述回答中，严禁捏造任何未出现的品牌！
   - 每项包含: {{"name": "竞品名称", "rank": 排名数字, "reason": "大模型给出的推荐优势"}}
8. risk_alerts: 回答中是否存在针对目标品牌的负面、警示、资质缺失或信息模糊的风险点（若无填空数组 []）。

请输出以下严格的 JSON 对象：
{{
  "brand_mentioned": false,
  "brand_recommended": false,
  "recommendation_level": "none",
  "rank": 0,
  "sentiment": "neutral",
  "recommendation_reasons": [],
  "competitors_ranked": [],
  "risk_alerts": []
}}"""

        try:
            res = await cls._call_deepseek_json(system_prompt, user_prompt, temperature=0.1, max_tokens=1500)
            # 强化校验有效性
            return {
                "brand_mentioned": bool(res.get("brand_mentioned", False)),
                "brand_recommended": bool(res.get("brand_recommended", False)),
                "recommendation_level": res.get("recommendation_level", "none"),
                "rank": int(res.get("rank", 0)),
                "sentiment": res.get("sentiment", "neutral"),
                "recommendation_reasons": res.get("recommendation_reasons", []),
                "competitors_ranked": res.get("competitors_ranked", []),
                "risk_alerts": res.get("risk_alerts", [])
            }
        except Exception as e:
            logger.error(f"DeepSeek 裁判解析异常: {e}")
            # 基础关键词兜底判别
            is_men = (target_brand in raw_answer) or (company_name and company_name in raw_answer)
            return {
                "brand_mentioned": is_men,
                "brand_recommended": is_men and ("推荐" in raw_answer or "优势" in raw_answer),
                "recommendation_level": "moderate" if is_men else "none",
                "rank": 3 if is_men else 0,
                "sentiment": "neutral",
                "recommendation_reasons": [f"提到了{target_brand}"] if is_men else [],
                "competitors_ranked": [],
                "risk_alerts": []
            }

    # =========================================================================
    # 3. 原子事实核验 (Atomic Fact Verifier)
    # =========================================================================
    @classmethod
    async def verify_atomic_facts(
        cls,
        raw_answer: str,
        target_brand: str,
        brand_facts: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        对比企业真实事实基准库与大模型回答，抓出具体事实错误与虚假幻觉。
        """
        if not brand_facts:
            return []

        system_prompt = (
            "你是一个严谨的事实核查审计员。"
            "你需要将企业提供的官方真实事实基准，与大模型输出的文本进行逐条比对。"
            "准确标记出：事实一致 (verified)、事实冲突/错误 (conflict)、未提及 (unmentioned)、或严重幻觉 (hallucination)。"
            "输出必须为 JSON 对象，根键为 'fact_checks'。"
        )

        facts_desc = "\n".join([
            f"- [{f.get('fact_type', '基础事实')}] {f.get('fact_key', '')}：官方基准为【{f.get('fact_value', '')}】"
            for f in brand_facts
        ])

        user_prompt = f"""【企业官方真实事实基准库】：
{facts_desc}

【大模型回答文本】：
\"\"\"
{raw_answer[:2500]}
\"\"\"

请对上述每一条官方事实进行核查，判断大模型在回答中是否有提及，说辞是否准确无误。
若大模型说错了关键数据（如年份、城市、规格、资质），必须明确抓出其错误，并指出风险等级。

【地理空间与事实常识核验铁律】：
核验企业地址、行政区、商圈板块时，必须严格以企业官方基准为唯一真相。若大模型提到的地址与官方基准存在地理错位（例如官方明确位于岳麓区金星中路/西湖公园/咸嘉湖板块，大模型却声称位于滨江新城或跨行政区），必须明确标记为 'conflict' (严重事实冲突)，并在 explanation 中明确指出【地理板块认知错位与信息污染】！

返回 JSON 格式：
{{
  "fact_checks": [
    {{
      "fact_key": "成立时间",
      "expected_value": "2018年",
      "claimed_value": "大模型在回答中提到的具体表述（若未提及填null）",
      "status": "verified / conflict / unmentioned / hallucination",
      "risk_level": "low / medium / high",
      "explanation": "核验分析说明（例如：大模型将成立时间误记为2015年，相差3年）"
    }}
  ]
}}"""

        try:
            res = await cls._call_deepseek_json(system_prompt, user_prompt, temperature=0.1, max_tokens=1500)
            return res.get("fact_checks", [])
        except Exception as e:
            logger.error(f"DeepSeek 事实核验失败: {e}")
            return []

    # =========================================================================
    # 4. GEO 优化任务智能综合生成 (Task Synthesizer)
    # =========================================================================
    @classmethod
    async def synthesize_geo_tasks(
        cls,
        brand_name: str,
        industry: str,
        city: str,
        presence_rate: float,
        recommendation_rate: float,
        accuracy_rate: float,
        top_competitors: List[Dict[str, Any]],
        fact_discrepancies: List[Dict[str, Any]],
        absent_categories: List[str]
    ) -> List[Dict[str, Any]]:
        """
        根据整个体检矩阵的综合表现，自动生成 6~10 条具象可执行的 P0/P1/P2 GEO 优化靶向任务工单。
        """
        system_prompt = (
            "你是一位顶尖的 GEO (Generative Engine Optimization，生成式 AI 搜索引擎优化) 商业落地架构师。"
            "你需要根据企业在各大主流 AI 模型中的可见度体检漏洞，给出极具操作性、能帮助企业立竿见影提升 AI 推荐权重的优化行动方案。"
            "任务必须分为 P0（紧急止血/修错）、P1（流量拦截与夺回）、P2（长期护城河/技术数据标记）。"
            "输出必须为严格的 JSON 格式，根键为 'tasks'。"
        )

        comp_str = "、".join([f"{c.get('name', '')} (拦截率约{c.get('intercept_rate', '高')})" for c in top_competitors[:4]]) or "同城主流竞品"
        facts_str = "；".join([f"{f.get('fact_key', '')}被AI误述为{f.get('claimed_value', '')}" for f in fact_discrepancies[:4]]) or "暂无严重冲突"
        absent_str = "、".join(absent_categories) if absent_categories else "预算决策与场景对比"

        user_prompt = f"""【企业诊断体检报告摘要】：
- 企业品牌：{brand_name}（所属赛道：{city} {industry}）
- 品牌出现率：{presence_rate}%
- 明确推荐率：{recommendation_rate}%
- 事实准确率：{accuracy_rate}%
- 核心拦截竞品：{comp_str}
- 显著事实错误点：{facts_str}
- 表现薄弱意图板块：{absent_str}

请为该企业制定 6-8 条靶向 GEO 优化任务工单，覆盖【内容建设 (content)】、【外部信源修正 (citation)】、【技术结构化标记 (technical)】三大类。
每条任务必须具体明确，直接指明去哪个平台、建什么页面、修改什么内容、预计能挽回多少可见度。

【地理空间与事实常识核验铁律 (Sanity Check)】：
所有生成的优化工单（尤其是针对百度百科、高德地图、大众点评等修正建议），严禁凭空建议将企业修改或标注至非事实基准的地理板块（例如：绝对不能将位于西湖公园/咸嘉湖板块的金星中路长沙岳麓万豪酒店建议迁移或标注至滨江新城）。必须以事实基准中的具体门牌地址与行政区为唯一铁律准绳！任何违反地理真实性的建议均为违规废单，绝对禁止输出！

返回 JSON 格式：
{{
  "tasks": [
    {{
      "id": "GEO-001",
      "priority": "P0",
      "title": "任务标题（如：纠正百度百科与大众点评商户主体基础数据）",
      "category": "citation",
      "action": "具体建议落地的执行步骤",
      "target_platform": "百度百科 / 官网 / 行业垂直媒体 / 问答社区",
      "expected_impact": "预期商业价值（如：消除15%事实错误率，避免AI产生信誉质疑）",
      "deadline_days": 3
    }}
  ]
}}"""

        try:
            res = await cls._call_deepseek_json(system_prompt, user_prompt, temperature=0.3, max_tokens=2500)
            tasks = res.get("tasks", [])
            if tasks:
                return tasks
        except Exception as e:
            logger.error(f"DeepSeek 任务生成失败: {e}")

        # 兜底通用任务
        return [
            {
                "id": "GEO-001",
                "priority": "P0",
                "title": f"修复公网百科与商录平台上的{brand_name}主体注册与业务信息",
                "category": "citation",
                "action": "统一百度百科、官方公众号与重点同城黄页的统一信用代码、开业年份与总部地址，杜绝AI信源冲突。",
                "target_platform": "百度百科 / 企查查 / 官方网站",
                "expected_impact": "提升大模型事实核验准确率至90%以上，消除负面质疑风险。",
                "deadline_days": 3
            },
            {
                "id": "GEO-002",
                "priority": "P1",
                "title": f"在知乎与垂直行业门户建立针对{city}{industry}的深度横向选型评测专栏",
                "category": "content",
                "action": f"围绕重点薄弱场景，发布‘{city}{industry}真实横评’深度长文，客观展示{brand_name}的核心长板。",
                "target_platform": "知乎 / 微信公众号 / 百家号",
                "expected_impact": f"截断来自竞品的主流客流截流，将品牌在场景决策词中的推荐率提升25%以上。",
                "deadline_days": 7
            },
            {
                "id": "GEO-003",
                "priority": "P2",
                "title": "在企业官方网站植入 Schema.org LocalBusiness 与 Organization 结构化微数据",
                "category": "technical",
                "action": "在官网首页与服务详情页规范化增加 JSON-LD 结构化标记，确保通义千问与豆包爬虫 100% 精确收录企业实体。",
                "target_platform": "企业官方网站技术底层",
                "expected_impact": "使大模型 RAG 引擎能以首选官方源引用官网，引用权威度评分提升至 85+。",
                "deadline_days": 14
            }
        ]
