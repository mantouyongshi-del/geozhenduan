import httpx
import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("AmapService")

def _safe_str(val: Any) -> str:
    if isinstance(val, str):
        return val.strip()
    return ""

class AmapService:
    """
    高德开放平台权威地理与商业实体服务中枢
    提供：
    1. POI 智能输入联想 (InputTips) 与官方标准门牌地址补齐；
    2. 多门店/连锁品牌泛词消歧侦测 (Disambiguation Guardrail)，防止录入“万豪酒店”等泛称；
    3. 官方权威基础事实（行政区、商圈、门牌号、联系方式）精准反填。
    """
    AMAP_TIPS_URL = "https://restapi.amap.com/v3/assistant/inputtips"
    AMAP_PLACE_TEXT_URL = "https://restapi.amap.com/v3/place/text"
    AMAP_PLACE_DETAIL_URL = "https://restapi.amap.com/v3/place/detail"

    # 常见容易产生泛指混淆的连锁/集团品牌通用词词根
    CHAIN_BRAND_KEYWORDS = [
        "万豪", "万豪酒店", "JW万豪", "希尔顿", "希尔顿酒店", "喜来登", "喜来登酒店", 
        "洲际", "洲际酒店", "凯悦", "君悦", "香格里拉", "威斯汀", "艾美", "W酒店",
        "海底捞", "西贝", "肯德基", "麦当劳", "星巴克", "瑞幸咖啡",
        "保时捷", "奔驰4S", "宝马4S", "奥迪4S", "比亚迪", "蔚来中心"
    ]

    @classmethod
    async def suggest_pois(
        cls,
        keywords: str,
        city: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        根据输入关键词和城市获取高德官方 POI 联想建议列表，并进行多门店消歧研判。
        """
        kw = keywords.strip()
        if not kw or len(kw) < 2:
            return {
                "suggestions": [],
                "is_chain_generic": False,
                "warning_message": "",
                "candidate_branches": []
            }

        api_key = settings.AMAP_KEY
        if not api_key:
            return {
                "suggestions": [],
                "is_chain_generic": False,
                "warning_message": "",
                "candidate_branches": []
            }
        params = {
            "keywords": kw,
            "key": api_key
        }
        if city and city != "全国":
            params["city"] = city

        raw_tips = []
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(cls.AMAP_TIPS_URL, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("status") == "1":
                        raw_tips = data.get("tips", [])
        except Exception as e:
            logger.warning(f"高德 InputTips 检索异常: {e}")

        # 解析与标准化候选列表
        suggestions: List[Dict[str, Any]] = []
        seen_names = set()

        for t in raw_tips:
            name = _safe_str(t.get("name"))
            if not name or name in seen_names:
                continue

            poi_id = _safe_str(t.get("id"))
            district = _safe_str(t.get("district"))
            address = _safe_str(t.get("address"))
            location = _safe_str(t.get("location"))
            typecode = _safe_str(t.get("typecode"))

            # 过滤纯省/市等非实体 POI (无 address 且无 id 通常是行政区域提示)
            if not poi_id and not address:
                continue

            full_addr = district + address if district or address else ""

            # 提取城市与行政区
            adname = ""
            cityname = ""
            if "市" in district:
                parts = district.split("市")
                if len(parts) >= 2:
                    cityname = parts[0].split("省")[-1] + "市"
                    adname = parts[1]
            elif "区" in district or "县" in district:
                adname = district

            suggestions.append({
                "id": poi_id,
                "name": name,
                "district": district,
                "adname": adname,
                "cityname": cityname,
                "address": address,
                "full_address": full_addr,
                "location": location,
                "typecode": typecode
            })
            seen_names.add(name)

        # -------------------------------------------------------------
        # 多门店/集团品牌泛词消歧检测 (Disambiguation Guardrail)
        # -------------------------------------------------------------
        is_chain = False
        warning_msg = ""
        candidate_branches: List[str] = []

        # 1. 关键词本身就是泛称 (如"万豪酒店"、"希尔顿")
        exact_generic = any(kw == generic_name for generic_name in cls.CHAIN_BRAND_KEYWORDS)
        
        # 2. 或者搜出的实体中存在多家不同分店 (例如岳麓万豪、JW万豪、梅溪湖万豪)
        distinct_branches = [
            s["name"] for s in suggestions 
            if any(token in s["name"] for token in [kw, "万豪", "希尔顿", "喜来登", "分店", "店"])
        ]

        if exact_generic or len(distinct_branches) >= 2:
            is_chain = True
            candidate_branches = distinct_branches[:5]
            city_prefix = f"{city}市" if city and city != "全国" else "本地"
            warning_msg = (
                f"⚠️ 实体消歧拦截：检测到【{kw}】在{city_prefix}为拥有多家独立物业/分店的品牌集团。"
                f"严禁直接录入泛指名称，避免大模型混淆各店事实导致评测失真！"
                f"请点击下方具体门店以精确绑定事实标尺。"
            )

        return {
            "suggestions": suggestions[:8],
            "is_chain_generic": is_chain,
            "warning_message": warning_msg,
            "candidate_branches": candidate_branches
        }

    @classmethod
    async def get_poi_fact_detail(
        cls,
        poi_id: str,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取指定 POI 的权威事实标尺详情（电话、星级/标签、详细地址、经纬度坐标）
        """
        api_key = settings.AMAP_KEY
        result = {
            "name": name or "",
            "address": "",
            "district": "",
            "city": "",
            "tel": "",
            "type_tag": "",
            "location": ""
        }
        if not api_key:
            return result

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                if poi_id:
                    resp = await client.get(cls.AMAP_PLACE_DETAIL_URL, params={"id": poi_id, "key": api_key})
                    if resp.status_code == 200:
                        pois = resp.json().get("pois", [])
                        if pois:
                            p = pois[0]
                            result["name"] = _safe_str(p.get("name"))
                            result["address"] = _safe_str(p.get("address"))
                            result["district"] = _safe_str(p.get("adname"))
                            result["city"] = _safe_str(p.get("cityname"))
                            result["tel"] = _safe_str(p.get("tel"))
                            result["type_tag"] = _safe_str(p.get("keytag")) or _safe_str(p.get("type"))
                            result["location"] = _safe_str(p.get("location"))
                            return result

                # 备选：place text 检索
                if name:
                    resp = await client.get(cls.AMAP_PLACE_TEXT_URL, params={"keywords": name, "key": api_key})
                    if resp.status_code == 200:
                        pois = resp.json().get("pois", [])
                        if pois:
                            p = pois[0]
                            result["name"] = _safe_str(p.get("name"))
                            result["address"] = _safe_str(p.get("address"))
                            result["district"] = _safe_str(p.get("adname"))
                            result["city"] = _safe_str(p.get("cityname"))
                            result["tel"] = _safe_str(p.get("tel"))
                            result["type_tag"] = _safe_str(p.get("keytag")) or _safe_str(p.get("type"))
                            result["location"] = _safe_str(p.get("location"))
        except Exception as e:
            logger.warning(f"高德 POI 事实详情检索异常: {e}")

        return result
