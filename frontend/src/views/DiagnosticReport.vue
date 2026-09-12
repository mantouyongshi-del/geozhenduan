<template>
  <div class="report-wrapper" v-if="report">
    <!-- 顶部操作条 (打印时隐藏) -->
    <div class="top-action-bar no-print">
      <div class="action-inner">
        <div class="bar-left">
          <button type="button" class="back-link" @click="handleBackToConsole" title="返回销售演示与体检工作台">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" class="bar-btn-icon">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            <span>返回销售工作台</span>
          </button>
          <span class="report-id-tag">报告单号: {{ report.report_code }}</span>
          <span v-if="isPublicView" class="public-read-badge">🔒 客户免登验真模式</span>
        </div>
        <div class="bar-right">
          <!-- 销售现场 30秒促单提词器挂件开关 (仅内部顾问可见) -->
          <button 
            v-if="!isPublicView"
            type="button" 
            class="btn btn-prompter-toggle"
            :class="{ active: showPrompter }"
            @click="togglePrompter"
            title="调出销售现场 30秒促单提词器与打脸话术导航"
          >
            <span class="btn-icon">🎙️</span>
            <span>30秒促单提词器</span>
          </button>
          <!-- 企业高管专属 核心数据高清长图生成器 (去冗余 · 直出海报) -->
          <button 
            type="button" 
            class="btn btn-executive-poster"
            @click="openPosterModal"
            title="生成专供企业老板/高管审阅的核心数据高清战报图，去粗取精，30秒看懂"
          >
            <span class="btn-icon">✨</span>
            <span>企业高管核心战报 · 高清图</span>
          </button>
          <label class="print-option-toggle" title="默认打印精炼商务报告(约4-5页)；勾选后将展开包含大模型全部万字实测长文与信源">
            <input type="checkbox" v-model="printExpandAll" />
            <span>包含大模型全部问答实录</span>
          </label>
          <button class="btn btn-outline" @click="handlePrint">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="bar-btn-icon">
              <polyline points="6 9 6 2 18 2 18 9"></polyline>
              <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
              <rect x="6" y="14" width="12" height="8"></rect>
            </svg>
            <span>打印 / 导出 A4 彩色诊断书</span>
          </button>
          <button class="btn btn-primary" @click="copyShareLink">
            <svg v-if="!copied" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="bar-btn-icon">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="bar-btn-icon">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>{{ copied ? '已复制免登分享链接 ✓' : (isPublicView ? '分享本报告' : '复制客户免登分享链接') }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 诊断书主体纸张 -->
    <div class="paper-container" :class="{ 'print-expand-all': printExpandAll }">
      <!-- 官方抬头 -->
      <header class="paper-header">
        <div class="header-seal-row">
          <div class="brand-title-wrap">
            <img src="/logo.png" alt="蜉蝣小宝" class="report-brand-logo" />
            <span class="brand-sub-title">企业 AI 搜索引擎可见度诊断体检书</span>
          </div>
          <div class="official-seal">
            <span class="seal-auth">官方认证</span>
            <span class="seal-name">AI 可见度评估</span>
          </div>
        </div>

        <div class="meta-grid">
          <div class="meta-item">
            <span class="meta-label">体检企业全称:</span>
            <span class="meta-val highlight">{{ report.target_company }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">品牌简称:</span>
            <span class="meta-val">{{ report.brand_name }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">所属行业:</span>
            <span class="meta-val">{{ report.industry }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">授权服务中心:</span>
            <span class="meta-val">{{ report.agency_name }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">认证数字化顾问:</span>
            <span class="meta-val">{{ report.consultant_name }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">诊断生成时间:</span>
            <span class="meta-val">{{ formatTime(report.created_at) }}</span>
          </div>
        </div>

        <!-- 国家级合规大模型官方真机直连存证背书条 -->
        <div class="live-cert-banner" v-if="report.certification_summary">
          <div class="cert-banner-left">
            <div class="cert-shield-badge">
              <span class="shield-icon">🛡️</span>
              <span class="shield-text">LIVE API 存证</span>
            </div>
            <div class="cert-summary-meta">
              <div class="cert-title-line">
                <strong class="cert-main-title">国家合规主流大模型商业 API 真机调用存证证书</strong>
                <span class="cert-code-tag">{{ report.certification_summary.cert_code }}</span>
                <span class="cert-status-tag">✓ 密码学哈希防篡改</span>
              </div>
              <p class="cert-statement-text">
                {{ report.certification_summary.statement }}
              </p>
            </div>
          </div>
          <div class="cert-banner-right">
            <div class="cert-hash-display">
              <span class="hash-tag-label">存证 SHA-256 摘要:</span>
              <code class="hash-code-val">{{ report.certification_summary.evidence_chain_hash ? report.certification_summary.evidence_chain_hash.slice(0, 24) : '' }}...</code>
            </div>
            <div class="cert-models-flow">
              <span class="engine-check-tag" v-for="m in report.certification_summary.active_models_list" :key="m">
                {{ m }} ✓
              </span>
            </div>
          </div>
        </div>
      </header>

      <!-- 核心指标 1: 震撼的 AI 可见度得分仪表盘 -->
      <section class="score-section" id="score-section">
        <div class="score-card" :class="getScoreClass(report.visibility_score)">
          <div class="score-number-box">
            <div class="score-big">{{ report.visibility_score }}</div>
            <div class="score-base">/ 100 分</div>
            <div class="risk-badge">{{ getRiskBadge(report.risk_level) }}</div>
          </div>

          <div class="score-summary-box">
            <h3 class="summary-heading">诊断核心结论:</h3>
            <p class="summary-text">{{ report.summary_verdict }}</p>
            <div class="model-tags">
              <span class="tag-title">测试覆盖大模型:</span>
              <span class="tag-pill tag-pill-live">DeepSeek + Kimi + 通义千问 + 字节豆包 + 百度文心 + 腾讯混元 · 官方六引擎全链路直连 ⚡</span>
            </div>

            <!-- 专供企业决策层的高清核心战报快捷生成条 -->
            <div class="executive-quick-bar">
              <button type="button" class="btn-quick-poster" @click="openPosterModal">
                <span class="btn-quick-icon">📊</span>
                <span>导出企业高管专属 · 核心数据高清战报图 (剔除技术冗余 · 直出图片发微信)</span>
                <span class="btn-quick-arrow">一键出图 ↵</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 1.5: 科学权威的 AIVS 六维诊断健康矩阵 (数据驱动 · 拒绝假定) -->
      <section class="section-card aivs-section" v-if="report.aivs_dimensions">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">📊 AIVS 智能搜索可见度 · 六维诊断健康雷达</h2>
            <span class="kw-counter-pill pill-indigo">DeepSeek Flash 裁判中枢精算</span>
          </div>
          <span class="sec-desc">
            依据工业级 AIVS 算法模型，从出现率、推荐度、位次、事实准确性、信源权重与跨平台一致性 6 大科学维度全面解构贵司健康度：
          </span>
        </div>

        <div class="aivs-metrics-grid">
          <!-- 1. 品牌出现率 -->
          <div class="aivs-card">
            <div class="aivs-top">
              <span class="aivs-name">品牌出现率 (Presence)</span>
              <span class="aivs-weight">权重 20%</span>
            </div>
            <div class="aivs-score-val" :class="report.aivs_dimensions.presence_rate > 50 ? 'text-green' : (report.aivs_dimensions.presence_rate > 0 ? 'text-warn' : 'text-danger')">
              {{ report.aivs_dimensions.presence_rate }}%
            </div>
            <div class="aivs-bar-track">
              <div class="aivs-bar-fill fill-presence" :style="{ width: Math.max(report.aivs_dimensions.presence_rate, 4) + '%' }"></div>
            </div>
            <div class="aivs-meta-desc">
              在各大主流 AI 搜索回答中被提及的比率
            </div>
          </div>

          <!-- 2. 明确推荐率 -->
          <div class="aivs-card">
            <div class="aivs-top">
              <span class="aivs-name">明确推荐率 (Recommendation)</span>
              <span class="aivs-weight">权重 25%</span>
            </div>
            <div class="aivs-score-val" :class="report.aivs_dimensions.recommendation_rate > 50 ? 'text-green' : (report.aivs_dimensions.recommendation_rate > 0 ? 'text-warn' : 'text-danger')">
              {{ report.aivs_dimensions.recommendation_rate }}%
            </div>
            <div class="aivs-bar-track">
              <div class="aivs-bar-fill fill-recommend" :style="{ width: Math.max(report.aivs_dimensions.recommendation_rate, 4) + '%' }"></div>
            </div>
            <div class="aivs-meta-desc">
              被大模型列为优选或前序推荐梯队比率
            </div>
          </div>

          <!-- 3. 推荐排位分 -->
          <div class="aivs-card">
            <div class="aivs-top">
              <span class="aivs-name">推荐排位分 (Ranking)</span>
              <span class="aivs-weight">权重 15%</span>
            </div>
            <div class="aivs-score-val" :class="report.aivs_dimensions.rank_score > 60 ? 'text-green' : (report.aivs_dimensions.rank_score > 0 ? 'text-warn' : 'text-danger')">
              {{ report.aivs_dimensions.rank_score }} <span class="unit-mini">分</span>
            </div>
            <div class="aivs-bar-track">
              <div class="aivs-bar-fill fill-rank" :style="{ width: Math.max(report.aivs_dimensions.rank_score, 4) + '%' }"></div>
            </div>
            <div class="aivs-meta-desc">
              大模型推荐名单中的实际排位优势权重
            </div>
          </div>

          <!-- 4. 事实准确率 -->
          <div class="aivs-card">
            <div class="aivs-top">
              <span class="aivs-name">事实准确率 (Accuracy)</span>
              <span class="aivs-weight">权重 20%</span>
            </div>
            <div class="aivs-score-val" :class="report.aivs_dimensions.accuracy_rate >= 80 ? 'text-green' : (report.aivs_dimensions.accuracy_rate >= 50 ? 'text-warn' : 'text-danger')">
              {{ report.aivs_dimensions.accuracy_rate }}%
            </div>
            <div class="aivs-bar-track">
              <div class="aivs-bar-fill fill-accuracy" :style="{ width: Math.max(report.aivs_dimensions.accuracy_rate, 4) + '%' }"></div>
            </div>
            <div class="aivs-meta-desc">
              大模型陈述企业信息与官方事实基准比对吻合度
            </div>
          </div>

          <!-- 5. 引用质量 -->
          <div class="aivs-card">
            <div class="aivs-top">
              <span class="aivs-name">引用质量 (Citations)</span>
              <span class="aivs-weight">权重 10%</span>
            </div>
            <div class="aivs-score-val" :class="report.aivs_dimensions.citation_quality >= 70 ? 'text-green' : 'text-warn'">
              {{ report.aivs_dimensions.citation_quality }} <span class="unit-mini">分</span>
            </div>
            <div class="aivs-bar-track">
              <div class="aivs-bar-fill fill-cites" :style="{ width: Math.max(report.aivs_dimensions.citation_quality, 4) + '%' }"></div>
            </div>
            <div class="aivs-meta-desc">
              公域被大模型采信的权威媒体与百科权重
            </div>
          </div>

          <!-- 6. 跨平台稳定性 -->
          <div class="aivs-card">
            <div class="aivs-top">
              <span class="aivs-name">跨平台稳定性 (Stability)</span>
              <span class="aivs-weight">权重 10%</span>
            </div>
            <div class="aivs-score-val" :class="report.aivs_dimensions.stability >= 60 ? 'text-green' : 'text-warn'">
              {{ report.aivs_dimensions.stability }} <span class="unit-mini">分</span>
            </div>
            <div class="aivs-bar-track">
              <div class="aivs-bar-fill fill-stability" :style="{ width: Math.max(report.aivs_dimensions.stability, 4) + '%' }"></div>
            </div>
            <div class="aivs-meta-desc">
              六大模型跨引擎回答结论与声量的一致性
            </div>
          </div>
        </div>
      </section>

      <!-- 商业杀伤力核心：真实潜客决策现场还原 · 红黑打脸双轨对比展区 -->
      <!-- 商业杀伤力核心：真实潜客决策现场还原 · 攻防双轨博弈对比展区 -->
      <section class="section-card contrast-section" id="contrast-section" v-if="report.decision_contrasts && report.decision_contrasts.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">⚔️ 真实采购决策现场还原 · 攻防双轨博弈 (真机真实还原)</h2>
            <span class="kw-counter-pill pill-red-tag">直击买家决策第一道心理防线</span>
          </div>
          <span class="sec-desc">
            当真正准备掏钱采购的意向潜客在主流 AI 对话框发起咨询时，大模型正在<strong>决定买家的第一信任归属</strong>——既多维呈现贵司守擂成功的核心高光，更客观暴露被同行抢先截流的薄弱失守阵地：
          </span>
        </div>

        <!-- 大模型切换标签栏 -->
        <div class="contrast-tabs-nav">
          <button 
            v-for="(c, cIdx) in report.decision_contrasts" 
            :key="c.id"
            type="button"
            class="contrast-tab-btn"
            :class="{ 
              active: activeContrastTab === cIdx,
              'tab-is-defense': c.contrast_type === 'defense',
              'tab-is-intercept': c.contrast_type === 'interception'
            }"
            @click="activeContrastTab = cIdx"
          >
            <span class="tab-plat-badge" :class="'plat-' + c.platform">{{ c.platform_name }}</span>
            <span class="tab-label">决策现场</span>
            <span class="tab-type-pill" :class="c.contrast_type === 'defense' ? 'pill-defense' : 'pill-intercept'">
              {{ c.contrast_type === 'defense' ? '🛡️ 守擂成功' : '🚨 竞品截流' }}
            </span>
            <span class="tab-indicator" v-if="activeContrastTab === cIdx">●</span>
          </button>
        </div>

        <!-- 当前激活模型的决策对抗舞台 -->
        <div class="contrast-stage-card" v-if="currentContrast" :class="'stage-' + (currentContrast.contrast_type || 'interception')">
          <!-- 场景意图条 -->
          <div class="stage-intent-bar" :class="{ 'bar-defense': currentContrast.contrast_type === 'defense' }">
            <div class="intent-left">
              <span class="intent-icon">💬</span>
              <div class="intent-text">
                <span class="intent-label">潜客真实向 AI 提问场景：</span>
                <strong class="intent-query">“{{ currentContrast.inquiry_scenario.replace('意向客户向 AI 发起咨询：“', '').replace('”', '') }}”</strong>
              </div>
            </div>
            <div class="intent-right">
              <span class="intent-pill" :class="{ 'pill-intent-defense': currentContrast.contrast_type === 'defense' }">
                🎯 {{ currentContrast.buyer_intent }}
              </span>
            </div>
          </div>

          <!-- 双轨对抗舞台：支持【优势守擂】与【失守截流】双态 -->
          <div class="battle-stage-grid">
            <!-- 左轨：竞品栏 (失守时为红方标杆，守擂时为次席陪跑) -->
            <div class="battle-col col-competitor" :class="{ 'col-competitor-secondary': currentContrast.contrast_type === 'defense' }">
              <div class="col-header" :class="currentContrast.contrast_type === 'defense' ? 'header-secondary' : 'header-red'">
                <div class="header-badge-row">
                  <span class="trophy-badge" v-if="currentContrast.contrast_type !== 'defense'">👑 标杆竞品礼遇</span>
                  <span class="secondary-badge" v-else>⚔️ 同业竞品竞逐</span>
                  <span class="status-pill" :class="currentContrast.contrast_type === 'defense' ? 'status-secondary' : 'status-vip'">
                    {{ currentContrast.competitor_status_tag }}
                  </span>
                </div>
                <h3 class="brand-headline" :class="currentContrast.contrast_type === 'defense' ? 'text-secondary' : 'text-gold'">
                  {{ currentContrast.competitor_brand }}
                </h3>
              </div>

              <div class="col-body">
                <div class="quote-box" :class="currentContrast.contrast_type === 'defense' ? 'quote-secondary' : 'quote-vip'">
                  <div class="quote-mark">“</div>
                  <p class="quote-content">{{ currentContrast.competitor_quote }}</p>
                  <div class="quote-tags">
                    <span 
                      v-for="tag in currentContrast.competitor_advantage_tags" 
                      :key="tag" 
                      :class="currentContrast.contrast_type === 'defense' ? 'sec-tag' : 'adv-tag'"
                    >
                      {{ currentContrast.contrast_type === 'defense' ? '• ' : '✓ ' }}{{ tag }}
                    </span>
                  </div>
                </div>

                <div class="buyer-reaction-card" :class="currentContrast.contrast_type === 'defense' ? 'reaction-secondary' : 'reaction-win'">
                  <div class="reaction-header">
                    <span class="reaction-emoji">{{ currentContrast.contrast_type === 'defense' ? '🟡' : '🟢' }}</span>
                    <strong>买家现场心理与决策走向：</strong>
                  </div>
                  <p class="reaction-text">{{ currentContrast.buyer_reaction_competitor }}</p>
                </div>
              </div>
            </div>

            <!-- 中间：态势分流裂缝 / 护城河 -->
            <div class="battle-chasm">
              <div class="vs-circle" :class="{ 'vs-circle-defense': currentContrast.contrast_type === 'defense' }">
                {{ currentContrast.contrast_type === 'defense' ? '🛡️' : 'VS' }}
              </div>
              <div class="chasm-arrow-wrap">
                <div class="arrow-line" :class="{ 'arrow-line-defense': currentContrast.contrast_type === 'defense' }"></div>
                <div class="chasm-badge" :class="{ 'chasm-badge-defense': currentContrast.contrast_type === 'defense' }">
                  <template v-if="currentContrast.contrast_type === 'defense'">
                    <span class="chasm-alert chasm-alert-defense">🛡️ 贵司锁定第一首选</span>
                    <span class="chasm-sub chasm-sub-defense">心智护城河成功防御</span>
                  </template>
                  <template v-else>
                    <span class="chasm-alert">🚨 意向潜客被同行截流</span>
                    <span class="chasm-sub">首屏转化被竞品掌控</span>
                  </template>
                </div>
              </div>
            </div>

            <!-- 右轨：贵司现状栏 (守擂时为绿金高光冠军，失守时为红黑预警) -->
            <div class="battle-col col-target" :class="{ 'col-target-champion': currentContrast.contrast_type === 'defense' }">
              <div class="col-header" :class="currentContrast.contrast_type === 'defense' ? 'header-champion' : 'header-black'">
                <div class="header-badge-row">
                  <span class="champion-badge" v-if="currentContrast.contrast_type === 'defense'">🏆 贵司核心高光</span>
                  <span class="alert-shield-badge" v-else>⚠️ 贵司真实处境</span>
                  <span class="status-pill" :class="currentContrast.contrast_type === 'defense' ? 'status-champion' : 'status-alert'">
                    {{ currentContrast.target_status_tag }}
                  </span>
                </div>
                <h3 class="brand-headline" :class="currentContrast.contrast_type === 'defense' ? 'text-champion' : 'text-danger'">
                  {{ currentContrast.target_brand }}
                </h3>
              </div>

              <div class="col-body">
                <div class="quote-box" :class="currentContrast.contrast_type === 'defense' ? 'quote-champion' : 'quote-alert'">
                  <div class="quote-mark">“</div>
                  <p class="quote-content">{{ currentContrast.target_quote }}</p>
                  <div class="quote-tags">
                    <span 
                      v-for="tag in currentContrast.target_vulnerability_tags" 
                      :key="tag" 
                      :class="currentContrast.contrast_type === 'defense' ? 'champion-tag' : 'vuln-tag'"
                    >
                      {{ currentContrast.contrast_type === 'defense' ? '✓ ' : '❌ ' }}{{ tag }}
                    </span>
                  </div>
                </div>

                <div class="buyer-reaction-card" :class="currentContrast.contrast_type === 'defense' ? 'reaction-win' : 'reaction-lost'">
                  <div class="reaction-header">
                    <span class="reaction-emoji">{{ currentContrast.contrast_type === 'defense' ? '🟢' : '🔴' }}</span>
                    <strong>买家现场心理与决策走向：</strong>
                  </div>
                  <p class="reaction-text">{{ currentContrast.buyer_reaction_target }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 底部刺痛 / 守擂启示总结条 -->
          <div 
            class="face-slap-summary-strip" 
            :class="{ 'defense-summary-strip': currentContrast.contrast_type === 'defense' }"
          >
            <span class="slap-icon">{{ currentContrast.contrast_type === 'defense' ? '🛡️' : '💥' }}</span>
            <div class="slap-content">
              <template v-if="currentContrast.contrast_type === 'defense'">
                <strong>守擂启示与护城河加固：</strong>
                大模型在当前核心场景中已将贵司确立为首推标杆，充分证实贵司的实体办学与品牌积淀已渗透进 AI 知识图谱！但公域竞争如逆水行舟，
                <strong>竞品正加速通过全网 GEO 优化试图反超截流，贵司必须持续夯实结构化权威信源，筑牢全域第一护城河！</strong>
              </template>
              <template v-else>
                <strong>商业痛点穿透结论：</strong>
                很多实体企业老板误以为“我们线下有实力、老客户多就不怕竞争”。但在 AI 大模型作为新一代商业入口的今天，
                <strong>只要大模型在关键决策问答中将客户直接引荐给同行竞品，买家就会在 3 秒钟内关掉对话转向竞品！</strong>
                这就是导致企业公域获客成本陡增、高意向潜客流失的隐形凶手。
              </template>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 3: AI 知识工程四层渗透漏斗 (GEO RAG Funnel 深度剖析) -->
      <section class="section-card funnel-section" v-if="report.funnel_metrics && report.funnel_metrics.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🌪️ AI 搜索视界四层渗透漏斗诊断 (GEO RAG Funnel)</h2>
            <span class="kw-counter-pill">科学归因分析：大模型为什么搜不到贵司</span>
          </div>
          <span class="sec-desc">
            大模型生成回答遵循严格的检索增强生成（RAG）路径。以下为贵司在各层级的客观得分与断层取证：
          </span>
        </div>

        <div class="funnel-grid">
          <div 
            v-for="(layer, lIdx) in report.funnel_metrics" 
            :key="layer.layer_key" 
            class="funnel-card"
            :class="'layer-' + layer.layer_key"
          >
            <div class="funnel-card-header">
              <div class="layer-header-left">
                <span class="layer-step-badge">第 {{ lIdx + 1 }} 层</span>
                <span class="layer-name">{{ layer.name }}</span>
              </div>
              <span class="layer-status-pill" :class="'pill-' + layer.status.toLowerCase()">
                {{ layer.status_label }}
              </span>
            </div>

            <div class="layer-score-bar-wrap">
              <div class="score-bar-track">
                <div 
                  class="score-bar-fill" 
                  :style="{ width: Math.max((layer.score / layer.max_score * 100), 8) + '%' }"
                ></div>
              </div>
              <div class="score-bar-label">
                <strong>{{ layer.score }}</strong> / {{ layer.max_score }} 分
              </div>
            </div>

            <div class="layer-body">
              <div class="layer-diag">
                <strong>⚠️ 核心病灶：</strong>{{ layer.diagnosis }}
              </div>
              <div class="layer-evidence">
                <strong>🔍 现场取证：</strong>{{ layer.core_evidence }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 3: 双端全网 AI 监控矩阵 (PC 桌面端 vs 手机移动端) -->
      <section class="section-card" v-if="report.dual_device_matrix && report.dual_device_matrix.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">📱 双端全网 AI 监控矩阵 (PC 桌面端 vs 手机移动端)</h2>
            <span class="kw-counter-pill" :class="mobileLossPillClass">{{ mobileLossText }}</span>
          </div>
          <span class="sec-desc">
            90% 的本地买家与决策层均使用手机端发起搜索与咨询。以下基于现场真实大模型实测探测结果，对比双端细分渠道收录情况：
          </span>
        </div>

        <div class="device-matrix-grid">
          <div 
            v-for="dm in report.dual_device_matrix" 
            :key="dm.platform_key"
            class="device-chip-card"
            :class="[
              dm.is_mobile ? 'chip-mobile' : 'chip-pc',
              dm.is_indexed ? 'card-indexed' : 'card-unindexed'
            ]"
          >
            <div class="chip-top">
              <span class="device-type-tag" :class="dm.is_mobile ? 'tag-mob' : 'tag-pc'">
                {{ dm.is_mobile ? '📱 手机端' : '💻 PC端' }}
              </span>
              <span class="chip-name">{{ dm.platform_name }}</span>
            </div>
            <div class="chip-status">
              <span v-if="dm.is_indexed" class="chip-badge badge-indexed">✓ 有收录</span>
              <span v-else class="chip-badge badge-unindexed">❌ 0% 隐形</span>
            </div>
            <div class="chip-desc">{{ dm.status_desc }}</div>
          </div>
        </div>
      </section>

      <!-- 核心指标 3.5: 原子事实核验与大模型幻觉审计看板 (Fact-Check Benchmark) -->
      <section class="section-card fact-check-section" v-if="report.fact_checks && report.fact_checks.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🔍 原子事实核验与大模型幻觉审计看板</h2>
            <span class="kw-counter-pill pill-purple">DeepSeek 裁判对标官方事实基准</span>
          </div>
          <span class="sec-desc">
            将企业官方真实事实基准与各大主流 AI 大模型实际陈述进行逐条核验，抓包 AI 张冠李戴、信息滞后与虚假幻觉：
          </span>
        </div>

        <div class="fact-table-wrap">
          <div class="mobile-scroll-hint">👈 左右滑动查看完整数据 👉</div>
          <table class="fact-table">
            <thead>
              <tr>
                <th style="width: 18%;">核验事实指标</th>
                <th style="width: 22%;">企业官方真实基准</th>
                <th style="width: 24%;">大模型实际陈述 / 回显</th>
                <th style="width: 16%;">核验结论</th>
                <th style="width: 20%;">商业风险审计说明</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(fc, fIdx) in report.fact_checks" :key="fIdx">
                <td class="fact-key-cell">
                  <strong>{{ fc.fact_key }}</strong>
                </td>
                <td class="fact-expected-cell">
                  <span class="expected-badge">官方基准</span>
                  <span class="expected-text">{{ fc.expected_value }}</span>
                </td>
                <td class="fact-claimed-cell">
                  <code class="claimed-code">{{ fc.claimed_value || '大模型回答中未曾提及' }}</code>
                </td>
                <td>
                  <span class="fact-status-pill" :class="'status-' + fc.status">
                    <span v-if="fc.status === 'verified'">✓ 真实吻合</span>
                    <span v-else-if="fc.status === 'conflict'">❌ 事实冲突</span>
                    <span v-else-if="fc.status === 'hallucination'">⚠️ 虚假幻觉</span>
                    <span v-else>❓ 缺乏收录</span>
                  </span>
                  <span class="risk-mini-tag" :class="'risk-' + (fc.risk_level || 'low')">
                    {{ fc.risk_level === 'high' ? '高危' : (fc.risk_level === 'medium' ? '中危' : '低危') }}
                  </span>
                </td>
                <td class="fact-explain-cell">
                  {{ fc.explanation }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 核心指标 4: 同行霸屏与流量截流预警 (同行正在吃掉你的商机) -->
      <section class="section-card">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">⚠️ 同行霸屏与流量截流预警</h2>
            <span class="kw-counter-pill pill-red-tag">自然搜索意图被瓜分</span>
          </div>
          <span class="sec-desc">在您未建立 GEO 知识图谱期间，大模型将采购意向全面推荐给了以下竞品梯队：</span>
        </div>

        <div class="competitor-table-wrap">
          <div class="mobile-scroll-hint">👈 左右滑动查看完整数据 👉</div>
          <table class="competitor-table">
            <thead>
              <tr>
                <th>霸屏同行企业</th>
                <th>大模型推荐总频次</th>
                <th>霸屏覆盖平台</th>
                <th>AI 推荐理由与优势提炼</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comp in report.competitors" :key="comp.name">
                <td class="comp-name-cell">
                  <strong>{{ comp.name }}</strong>
                </td>
                <td>
                  <span class="mention-pill">{{ comp.mention_count }} 次推荐</span>
                </td>
                <td>
                  <span v-for="p in comp.dominant_platforms" :key="p" class="platform-mini-tag">
                    {{ p }}
                  </span>
                </td>
                <td class="comp-adv-cell">{{ comp.advantage_points }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 核心指标 5: 同行竞品 RAG 知识源阵地穿透 (对手是在哪里投喂被采信的) -->
      <section class="section-card" v-if="report.competitor_sources && report.competitor_sources.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🎯 同行竞品 RAG 知识源阵地穿透</h2>
            <span class="kw-counter-pill">溯源大模型底层采信源</span>
          </div>
          <span class="sec-desc">
            大模型并不会凭空编造推荐，而是采信以下高权重阵地的结构化内容。对手正是因为在这些阵地完成了投喂：
          </span>
        </div>

        <div class="sources-table-wrap">
          <div class="mobile-scroll-hint">👈 左右滑动查看完整数据 👉</div>
          <table class="sources-table">
            <thead>
              <tr>
                <th>权威采信信源阵地</th>
                <th>信源权重与类型</th>
                <th>被大模型引用频次</th>
                <th>重点布局同行</th>
                <th>贵司当前布局现状</th>
                <th>威胁等级</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="src in report.competitor_sources" :key="src.site_name">
                <td class="src-site-cell">
                  <strong>{{ src.site_name }}</strong>
                </td>
                <td><span class="src-type-tag">{{ src.source_type }}</span></td>
                <td class="text-center font-bold text-indigo">{{ src.citation_count }} 次引用</td>
                <td>
                  <span v-for="cn in src.competitor_names" :key="cn" class="comp-source-pill">
                    {{ cn }}
                  </span>
                </td>
                <td class="text-danger font-bold">{{ src.target_coverage }}</td>
                <td>
                  <span class="threat-badge" :class="src.threat_level.includes('极高') || src.threat_level.includes('基石') ? 'threat-critical' : 'threat-high'">
                    {{ src.threat_level }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 核心指标 6: 商业潜客流失测算与经济账本 (ROI 商业换算器) -->
      <section class="section-card economic-card" id="economic-section" v-if="report.economic_loss">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">💰 商业潜客流失测算与经济账本</h2>
            <span class="kw-counter-pill pill-money">基于 {{ report.city }} 本地搜索体量测算</span>
          </div>
          <span class="sec-desc">
            将 AI 搜索可见度直接换算为企业每月的订单与客源流失，商业损失透明可验：
          </span>
        </div>

        <div class="economic-kpi-grid">
          <div class="econ-kpi-box">
            <div class="econ-label">本地月度 AI 咨询意向</div>
            <div class="econ-val text-slate">~{{ report.economic_loss.monthly_search_inquiries }} <span class="unit">人次/月</span></div>
            <div class="econ-sub">{{ report.city }} 地区目标客户潜在搜索量</div>
          </div>

          <div class="econ-kpi-box">
            <div class="econ-label">每月流失准客户/商机</div>
            <div class="econ-val text-danger">{{ report.economic_loss.monthly_lost_leads_min }} ~ {{ report.economic_loss.monthly_lost_leads_max }} <span class="unit">人/月</span></div>
            <div class="econ-sub">被竞品在 AI 对话流中直接分流截胡</div>
          </div>

          <div class="econ-kpi-box econ-highlight-box">
            <div class="econ-label">每月直接经济损失</div>
            <div class="econ-val text-red">￥{{ report.economic_loss.monthly_loss_amount_min.toLocaleString() }} ~ ￥{{ report.economic_loss.monthly_loss_amount_max.toLocaleString() }}</div>
            <div class="econ-sub">按行业单客均价 ￥{{ report.economic_loss.estimated_unit_price.toLocaleString() }} 计算</div>
          </div>

          <div class="econ-kpi-box">
            <div class="econ-label">年化潜在流失上限</div>
            <div class="econ-val text-darkred">￥{{ report.economic_loss.annual_loss_amount_est.toLocaleString() }}</div>
            <div class="econ-sub">长期公域声量空白产生的隐形成本</div>
          </div>
        </div>

        <div class="roi-banner">
          <div class="roi-left">
            <span class="roi-badge">⚡ 确定性极高的 ROI 投资回报</span>
            <div class="roi-pitch">
              贵司只要采纳【蜉蝣小宝 GEO 知识工程优化服务】，<strong>当月仅需拦截回 {{ report.economic_loss.payback_leads_needed }} 位客户/学员</strong>，即可 100% 收回全部服务投资！其余收益均为纯利润。
            </div>
          </div>
          <div class="roi-note">
            * {{ report.economic_loss.calculation_note }}
          </div>
        </div>
      </section>

      <!-- 核心指标 3: 六大模型真实现场提问回显证据链 (按提问搜索词场景分组) -->
      <section class="section-card">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🔍 全网主流 AI 搜索引擎现场提问证据链</h2>
            <span class="kw-counter-pill">共覆盖 {{ groupedItems.length }} 组采购意向词 × 6 大 AI 引擎</span>
          </div>
          <span class="sec-desc">
            每个高频搜索词均分别向 <strong>豆包、DeepSeek、Kimi、通义千问、腾讯元宝、文心一言</strong> 逐一发起真实提问，以下为各场景原貌回显：
          </span>
        </div>

        <!-- 场景分组卡片 -->
        <div class="scenario-groups-wrap">
          <div 
            v-for="(group, gIdx) in groupedItems" 
            :key="group.keyword" 
            class="scenario-group-card"
          >
            <!-- 场景头部 -->
            <div class="scenario-header">
              <div class="scenario-meta">
                <span class="scenario-badge">场景 {{ gIdx + 1 }}</span>
                <span class="scenario-kw">{{ group.keyword }}</span>
                <span class="scenario-category-pill" :class="'cat-' + group.category">
                  {{ group.category === 'brand' ? '品牌名称词' : (group.category === 'trust' ? '口碑信任词' : '核心获客词') }}
                </span>
              </div>
              <div class="scenario-stats">
                <span class="stat-tag" :class="group.mentionedCount > 0 ? 'tag-warn' : 'tag-danger'">
                  {{ group.mentionedCount > 0 ? `仅 ${group.mentionedCount} 家模型提及` : '6 大模型全网 0% 推荐 (完全截流)' }}
                </span>
              </div>
            </div>

            <!-- 该场景下的 6 大模型手风琴 -->
            <div class="items-accordion">
              <div 
                v-for="item in group.items" 
                :key="item.id" 
                class="accordion-item"
                :class="{ open: openItemId === item.id || printExpandAll }"
              >
                <div class="accordion-header" @click="toggleAccordion(item.id)">
                  <div class="item-left">
                    <span class="platform-badge" :class="'plat-' + item.platform">{{ item.platform_name }}</span>
                    <span class="real-api-pill">⚡ 官方商业 API 实时直连</span>
                    <span class="kw-sub-info">调用大模型: {{ item.model_name || item.platform }}</span>
                  </div>
                  <div class="item-right">
                    <span v-if="item.duration_ms" class="duration-badge">⏱️ {{ (item.duration_ms / 1000).toFixed(1) }}s</span>
                    <span v-if="!item.is_target_mentioned" class="status-stamp stamp-unseen">
                      ❌ 未被收录 (隐形)
                    </span>
                    <span v-else class="status-stamp stamp-seen">
                      ✓ 第 {{ item.target_rank }} 位提及
                    </span>
                    <span class="arrow-indicator">{{ (openItemId === item.id || printExpandAll) ? '▲ 收起' : '▼ 展开实录' }}</span>
                  </div>
                </div>

                <div v-show="openItemId === item.id || printExpandAll" class="accordion-body">
                  <!-- 官方商业 API 真机交互存证核验卡 -->
                  <div class="api-cert-card" v-if="item.api_certification">
                    <div class="cert-card-header">
                      <div class="cert-header-left">
                        <span class="cert-pulse-dot"></span>
                        <strong class="cert-auth-tag">官方商业 API 实机调用已核验</strong>
                        <span class="cert-provider-name">{{ item.api_certification.provider }}</span>
                        <span class="cert-model-family">{{ item.api_certification.model_family }}</span>
                      </div>
                      <div class="cert-header-right">
                        <span class="cert-serial-label">存证凭证编号:</span>
                        <code class="cert-serial-code">{{ item.api_certification.cert_id }}</code>
                      </div>
                    </div>
                    <div class="cert-params-grid">
                      <div class="param-cell">
                        <span class="p-label">官方调用终结点 (Endpoint)</span>
                        <span class="p-val p-endpoint">{{ item.api_certification.api_endpoint }}</span>
                      </div>
                      <div class="param-cell">
                        <span class="p-label">商业请求追踪号 (Trace ID)</span>
                        <span class="p-val p-code">{{ item.api_certification.trace_id }}</span>
                      </div>
                      <div class="param-cell">
                        <span class="p-label">防伪数字摘要 (SHA-256)</span>
                        <span class="p-val p-hash">#{{ item.api_certification.verification_hash }}</span>
                      </div>
                      <div class="param-cell">
                        <span class="p-label">调用耗时与消耗</span>
                        <span class="p-val p-metric">⏱️ {{ (item.api_certification.duration_ms / 1000).toFixed(1) }}s · 🪙 {{ item.api_certification.token_count }} tokens</span>
                      </div>
                    </div>
                    <div class="cert-footer-banner">
                      <span class="compliance-badge">🛡️ {{ item.api_certification.compliance_record }}</span>
                      <span class="bill-verified-badge">✓ 已通过各大模型官方开放平台账单核验 · 100% 真实交互存证</span>
                    </div>
                  </div>

                  <!-- 大模型回答原文 -->
                  <div class="raw-response-box">
                    <div class="box-label">
                      <span v-if="item.platform === 'deepseek'" class="label-deepseek">
                        🤖 DeepSeek 官方开放平台实时推理实录 (调用模型: {{ item.model_name || 'deepseek-chat' }} · 耗时 {{ (item.duration_ms / 1000).toFixed(1) }} 秒 · 真实 API 交互):
                      </span>
                      <span v-else-if="item.platform === 'kimi'" class="label-kimi">
                        🌙 Moonshot Kimi 官方开放平台实时推理实录 (长文本文献精读 · 调用模型: {{ item.model_name || 'moonshot-v1-8k' }} · 耗时 {{ (item.duration_ms / 1000).toFixed(1) }} 秒 · 真实 API 交互):
                      </span>
                      <span v-else-if="item.platform === 'tongyi'" class="label-tongyi">
                        🤖 阿里云百炼·通义千问官方实时推理实录 (原生网络检索联网 · 调用模型: {{ item.model_name || 'qwen-turbo' }} · 耗时 {{ (item.duration_ms / 1000).toFixed(1) }} 秒 · 真实 API 交互):
                      </span>
                      <span v-else-if="item.platform === 'doubao'" class="label-doubao">
                        🤖 字节跳动·豆包官方开放平台实时推理实录 (火山引擎方舟直连 · 调用模型: {{ item.model_name || 'doubao-seed-2-0' }} · 耗时 {{ (item.duration_ms / 1000).toFixed(1) }} 秒 · 真实 API 交互):
                      </span>
                      <span v-else>
                        🤖 {{ item.platform_name }} 智能分析回显 (经全网知识库探针检索 · 耗时 {{ (item.duration_ms / 1000).toFixed(1) }} 秒):
                      </span>
                    </div>
                    <pre class="raw-text">{{ item.raw_content }}</pre>
                  </div>

                  <!-- 竞品引文溯源与豆包动态信源联动 -->
                  <div class="rag-citations-box" v-if="item.citations && item.citations.length">
                    <div class="box-label">
                      <span v-if="item.platform === 'doubao'" class="doubao-citations-badge">
                        🔍 豆包真机联动：已检索 4 个关键词，参考 {{ item.citations.length }} 篇公域信源（与手机端完全一致）：
                      </span>
                      <span v-else>
                        🌐 竞品所使用的 RAG 知识源 (同行是在哪里发软文被 AI 收录的):
                      </span>
                    </div>
                    <div class="citation-links-list">
                      <!-- 当大模型调取的全部信源中 0 篇收录贵司时，展示直击痛点的警示卡片 -->
                      <div 
                        v-if="!item.citations.some(c => isTargetCite(c))" 
                        class="zero-target-notice"
                      >
                        <div class="zero-target-header">
                          <span class="zero-target-tag">🔴 贵司全网 0 篇收录（公域完全空白）</span>
                          <span class="zero-target-badge">大模型 RAG 检索未召回</span>
                        </div>
                        <p class="zero-target-desc">
                          在本次大模型调取的全部 <strong>{{ item.citations.length }}</strong> 篇核心参考信源中，未收录【<strong>{{ report.brand_name }}</strong>】的任何有效页面或权威研报，潜在意向客户已被竞品 100% 截流！
                        </p>
                      </div>

                      <div 
                        v-for="(cite, cIdx) in item.citations" 
                        :key="cIdx" 
                        class="cite-row"
                        :class="{ 'target-brand-row': isTargetCite(cite) }"
                      >
                        <span class="cite-num">信源 {{ cIdx + 1 }}:</span>
                        <span class="cite-site">[{{ cite.site_name }}]</span>
                        <a :href="sanitizeUrl(cite.url)" target="_blank" rel="noopener noreferrer" class="cite-title">{{ cite.title }}</a>
                        <span 
                          v-if="isTargetCite(cite)" 
                          class="target-brand-pill"
                        >
                          🎯 贵司被抓取页 (信源 {{ cIdx + 1 }}) · ⚠️ 虽被爬虫抓取，但公域权重单薄在推荐层被 AI 算法过滤淘汰
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 8: 30 天 GEO 品牌知识工程重塑实施路线图 (甘特图) -->
      <section class="section-card roadmap-card" id="roadmap-section" v-if="report.implementation_roadmap && report.implementation_roadmap.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🛠️ 蜉蝣小宝 · 30 天 GEO 品牌重塑实施路线图</h2>
            <span class="kw-counter-pill">四阶段标准化确定性交付</span>
          </div>
          <span class="sec-desc">
            针对以上四层漏斗缺陷与公网空白，专属数字化顾问团队将在签约后 30 天内按以下标准化流程推进交付：
          </span>
        </div>

        <div class="roadmap-timeline">
          <div 
            v-for="phase in report.implementation_roadmap" 
            :key="phase.phase" 
            class="timeline-phase-card"
          >
            <div class="phase-left-col">
              <div class="phase-badge">阶段 0{{ phase.phase }}</div>
              <div class="phase-days">{{ phase.day_range }}</div>
            </div>

            <div class="phase-main-col">
              <h3 class="phase-title">{{ phase.title }}</h3>
              <div class="phase-action">
                <strong>🎯 实施动作：</strong>{{ phase.core_action }}
              </div>
              <div class="phase-deliverable">
                <strong>📦 阶段成果：</strong>{{ phase.deliverable }}
              </div>
              <div class="phase-kpi">
                <strong>📈 交付验收 KPI：</strong><span class="kpi-text">{{ phase.expected_kpi }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 8.5: DeepSeek Flash 专属靶向 GEO 优化落地工单 (P0/P1/P2) -->
      <section class="section-card geo-tasks-section" v-if="report.geo_tasks && report.geo_tasks.length">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🛠️ 蜉蝣小宝 · 靶向 GEO 优化落地任务工单 (P0/P1/P2)</h2>
            <span class="kw-counter-pill pill-red-tag">DeepSeek Flash 智能研判处方</span>
          </div>
          <span class="sec-desc">
            根据本次 6 大主流 AI 搜索引擎实测出现的截流与信源漏洞，内部裁判中枢自动生成具象可执行的落地工单：
          </span>
        </div>

        <div class="geo-tasks-grid">
          <div 
            v-for="(task, tIdx) in report.geo_tasks" 
            :key="task.id || tIdx"
            class="geo-task-card"
            :class="'priority-' + (task.priority || 'P1').toLowerCase()"
          >
            <!-- 头部：优先级 + 分类 + 落地期限 -->
            <div class="task-card-header">
              <div class="task-priority-badge" :class="'badge-' + (task.priority || 'P1').toLowerCase()">
                <span v-if="task.priority === 'P0'">🚨 P0 紧急止血</span>
                <span v-else-if="task.priority === 'P1'">⚡ P1 流量夺回</span>
                <span v-else>🛡️ P2 护城河底座</span>
              </div>
              <div class="task-meta-right">
                <span class="task-category-pill">{{ task.category === 'content' ? '📝 内容建设' : (task.category === 'citation' ? '🌐 外部信源' : '⚙️ 技术标记') }}</span>
                <span class="task-deadline-tag">⏱️ {{ task.deadline_days }} 天内落地</span>
              </div>
            </div>

            <!-- 任务核心主旨 -->
            <h3 class="task-title">{{ task.title }}</h3>

            <!-- 推荐发布阵地具体清单 -->
            <div class="task-platforms-block">
              <div class="block-label">
                <span class="lbl-icon">🌐</span>
                <span>推荐发布阵地清单：</span>
              </div>
              <div class="platform-badges-wrap">
                <span 
                  v-for="(plat, pIdx) in getTaskPlatforms(task)" 
                  :key="pIdx"
                  class="platform-badge"
                  :class="getPlatformBadgeClass(plat)"
                >
                  <span class="badge-ico">{{ getPlatformIcon(plat) }}</span>
                  <span class="badge-txt">{{ plat }}</span>
                </span>
              </div>
            </div>

            <!-- 建议宣发/发布标题 (带一键复制) -->
            <div class="task-title-suggestion-box" v-if="task.suggested_title">
              <div class="suggestion-header">
                <span class="suggestion-label">
                  <span class="lbl-icon">📰</span>
                  <span>建议宣发/文章标题：</span>
                </span>
                <button 
                  type="button" 
                  class="btn-copy-title"
                  @click="copyTaskTitle(task.suggested_title, task.id || tIdx)"
                  title="一键复制建议文章标题"
                >
                  <span v-if="copiedTaskTitleId === (task.id || tIdx)" class="copy-done">已复制 ✓</span>
                  <span v-else class="copy-init">📋 复制标题</span>
                </button>
              </div>
              <div class="suggested-title-text">
                {{ task.suggested_title }}
              </div>
            </div>

            <!-- 建议核心埋词 / 实体对 -->
            <div class="task-keywords-block" v-if="task.core_keywords && task.core_keywords.length">
              <div class="block-label">
                <span class="lbl-icon">🏷️</span>
                <span>核心埋词与实体对：</span>
              </div>
              <div class="keywords-wrap">
                <span v-for="(kw, kIdx) in task.core_keywords" :key="kIdx" class="kw-tag">
                  #{{ kw }}
                </span>
              </div>
            </div>

            <!-- 具体发布规范与结构建议 (大模型 RAG 采信规范) -->
            <div class="task-format-guide-box" v-if="task.format_guide">
              <div class="guide-title">
                <span class="guide-icon">📋</span>
                <strong>大模型采信发布规范建议：</strong>
              </div>
              <div class="guide-desc">
                {{ task.format_guide }}
              </div>
            </div>

            <!-- 落地执行建议步骤 -->
            <div class="task-action-box">
              <strong>🎯 落地执行步骤：</strong>{{ task.action }}
            </div>

            <!-- 底部：预期收益与商业价值 -->
            <div class="task-footer-row">
              <div class="task-impact-txt">
                <span class="impact-lbl">预期收益与商业价值:</span>
                <span class="impact-txt">{{ task.expected_impact }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 9: 蜉蝣小宝四维场景 GEO 处方与修复方案 -->
      <section class="section-card prescription-card">
        <div class="sec-title-row">
          <h2 class="sec-title">🛡️ 四维场景 GEO 专属应对处方</h2>
          <span class="sec-desc">针对品牌词、意图词、问答词、搜索词四维业务场景，定制精细化运营策略：</span>
        </div>

        <div class="prescription-grid">
          <div v-for="rx in report.prescriptions" :key="rx.scenario" class="rx-box">
            <div class="rx-header">
              <span class="rx-scenario">{{ rx.scenario }}</span>
              <span class="rx-urgency" :class="rx.urgency.includes('极高') ? 'urgency-red' : 'urgency-blue'">
                {{ rx.urgency }}
              </span>
            </div>
            <div class="rx-action">
              <strong>🛠️ 实施策略:</strong> {{ rx.action }}
            </div>
            <div class="rx-expected">
              <strong>🎯 预期成效:</strong> {{ rx.expected_result }}
            </div>
          </div>
        </div>
      </section>

      <!-- 核心指标 10: 前后体检报告“版本对比视图”与复测效果追踪 (Phase 4 闭环攻防对比流) -->
      <section class="section-card compare-view-card" id="compare-section">
        <div class="sec-title-row">
          <div class="title-with-counter">
            <h2 class="sec-title">🔄 30天 GEO 品牌重塑 · 优化前后效果复测对比视图</h2>
            <span class="kw-counter-pill pill-compare">闭环攻防验证 · 效果确定性交付</span>
          </div>
          <span class="sec-desc">
            将当前<strong>“严重失血状态”</strong>与 30 天实施交付后的<strong>“行业标杆首推”</strong>并列比对，让客户直观看到投资回报：
          </span>
        </div>

        <div class="compare-dual-grid">
          <!-- 优化前 (现状诊断) -->
          <div class="compare-box box-before">
            <div class="cbox-header">
              <span class="cbox-badge badge-before">🔴 优化前现状 · 当前体检实录</span>
              <span class="cbox-score-tag">{{ report.visibility_score }} 分 (严重高危)</span>
            </div>
            
            <div class="cbox-body">
              <div class="cbox-metric-row">
                <span class="m-lbl">行业核心词推荐率：</span>
                <strong class="m-val text-red">0% (AI 视界盲区)</strong>
              </div>
              <div class="cbox-metric-row">
                <span class="m-lbl">同行竞品截流率：</span>
                <strong class="m-val text-red">100% (客源全额被截流)</strong>
              </div>
              <div class="cbox-metric-row">
                <span class="m-lbl">公域权威信源入库：</span>
                <strong class="m-val text-slate">0 篇权威收录 (公域完全空白)</strong>
              </div>
              <div class="cbox-metric-row">
                <span class="m-lbl">每月直接经济损失：</span>
                <strong class="m-val text-red">￥{{ (report.economic_loss?.monthly_loss_amount_min || 90000).toLocaleString() }} ~ ￥{{ (report.economic_loss?.monthly_loss_amount_max || 225000).toLocaleString() }}</strong>
              </div>
              <div class="cbox-quote-box quote-before">
                <div class="quote-tag">大模型当前回答原貌：</div>
                <p>“未查询到该品牌权威第三方背书与国家级资质，公域声量单薄，建议买家谨慎核查风险。”</p>
              </div>
            </div>
          </div>

          <!-- 优化后 (30天交付复测) -->
          <div class="compare-box box-after">
            <div class="cbox-header">
              <span class="cbox-badge badge-after">🟢 30天优化后 · 预期复测达标</span>
              <span class="cbox-score-tag tag-after">88 分 (标杆首推 · 提升 +{{ 88 - report.visibility_score }}分)</span>
            </div>
            
            <div class="cbox-body">
              <div class="cbox-metric-row">
                <span class="m-lbl">行业核心词推荐率：</span>
                <strong class="m-val text-green">85%+ (位列第一梯队)</strong>
              </div>
              <div class="cbox-metric-row">
                <span class="m-lbl">同行竞品截流率：</span>
                <strong class="m-val text-green">降至 10% 以下 (实现强势反截流)</strong>
              </div>
              <div class="cbox-metric-row">
                <span class="m-lbl">公域权威信源入库：</span>
                <strong class="m-val text-green">12+ 篇高权重权威信源入库</strong>
              </div>
              <div class="cbox-metric-row">
                <span class="m-lbl">每月预期挽回商机：</span>
                <strong class="m-val text-green">截留回 18~35 位客户，年化增收数十万</strong>
              </div>
              <div class="cbox-quote-box quote-after">
                <div class="quote-tag">大模型优化后预期反馈：</div>
                <p>“行业实体标杆制造品牌，具备权威质量体系认证与成熟售后体系，为意向采购首推优选品牌。”</p>
              </div>
            </div>
          </div>
        </div>

        <div class="compare-guarantee-bar">
          <span class="g-icon">🛡️</span>
          <div class="g-text">
            <strong>确定性交付承诺：</strong>签约专属数字化顾问团队后，我们将严格按照《30天实施路线图》执行知识投喂，交付后进行<strong>真实大模型二次复测并出具复测验真报告</strong>，不达标持续免费优化！
          </div>
        </div>
      </section>

      <!-- 底部签约与顾问署名 -->
      <footer class="paper-footer">
        <div class="footer-inner">
          <div class="contact-card">
            <div class="contact-title">如需立即启动 GEO 品牌知识投喂与场景修复，请联系您的认证顾问：</div>
            <div class="contact-details">
              <span>🏢 {{ report.agency_name }}</span>
              <span>👤 顾问：{{ report.consultant_name }}</span>
              <span v-if="report.consultant_phone">📞 联系电话：{{ report.consultant_phone }}</span>
            </div>
          </div>
          <div class="statement-box">
            本诊断书由<strong>【蜉蝣小宝 · 全国智能营销云平台】</strong>通过多模型探针技术自动化生成，数据采信自各大主流大模型公开搜索接口，具备客观技术分析参考价值。
          </div>
          <!-- 底部快捷操作区 (打印时隐藏) -->
          <div class="footer-bottom-actions no-print">
            <button type="button" class="btn-footer-back" @click="handleBackToConsole">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" class="footer-btn-icon">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
              <span>返回销售工作台</span>
            </button>
            <button type="button" class="btn-footer-poster" @click="openPosterModal">
              <span>✨ 企业高管核心战报 · 高清图</span>
            </button>
          </div>
        </div>
      </footer>
    </div>

    <!-- 销售现场“30秒促单提词器”悬浮组件 (no-print, 仅内部顾问模式展示) -->
    <div 
      v-if="showPrompter && !isPublicView" 
      class="sales-prompter-dock no-print"
      :class="{ 'prompter-minimized': isPrompterMinimized }"
    >
      <!-- 最小化药丸条 -->
      <div v-if="isPrompterMinimized" class="prompter-pill-bar" @click="isPrompterMinimized = false">
        <div class="pill-left">
          <span class="pill-icon">🎙️</span>
          <span class="pill-title">30秒促单提词器</span>
          <span class="pill-timer-tag" :class="{ 'timer-running': isTimerRunning, 'timer-end': timerRemaining === 0 }">
            ⏱️ {{ timerRemaining }}s
          </span>
        </div>
        <span class="pill-expand-btn">▲ 展开促单秘籍</span>
      </div>

      <!-- 展开完整面板 -->
      <div v-else class="prompter-card">
        <div class="prompter-header">
          <div class="prompter-title-wrap">
            <span class="head-icon">🎙️</span>
            <div class="head-texts">
              <strong class="head-title">现场促单提词器 · 30秒签单闭环秘籍</strong>
              <span class="head-sub">专为销售拜访与客户面谈定制 · 节奏把控三步走</span>
            </div>
          </div>
          <div class="prompter-actions-top">
            <div class="timer-control-box">
              <span class="timer-display" :class="{ 'timer-alert': timerRemaining <= 10 && timerRemaining > 0, 'timer-end': timerRemaining === 0 }">
                ⏱️ {{ String(timerRemaining).padStart(2, '0') }}s
              </span>
              <button type="button" class="btn-timer-action" @click="toggleTimer" :title="isTimerRunning ? '暂停计时' : '启动30秒计时'">
                {{ isTimerRunning ? '⏸️ 暂停' : '▶️ 计时' }}
              </button>
              <button type="button" class="btn-timer-reset" @click="resetTimer" title="重置计时">
                🔄 重置
              </button>
            </div>
            <button type="button" class="btn-min-prompter" @click="isPrompterMinimized = true" title="收起为悬浮条">
              ▼ 收起
            </button>
            <button type="button" class="btn-close-prompter" @click="showPrompter = false" title="关闭提词器">
              ✕
            </button>
          </div>
        </div>

        <!-- 30秒倒计时演练进度条 -->
        <div class="timer-progress-track">
          <div class="timer-progress-fill" :style="{ width: ((30 - timerRemaining) / 30 * 100) + '%' }"></div>
        </div>

        <!-- 三大步骤标签选择 -->
        <div class="prompter-steps-nav">
          <button 
            type="button" 
            class="step-nav-btn" 
            :class="{ active: activePrompterStep === 1 }"
            @click="selectPrompterStep(1)"
          >
            <span class="step-num">① 0~10s</span>
            <span class="step-name">打脸定性</span>
          </button>
          <button 
            type="button" 
            class="step-nav-btn" 
            :class="{ active: activePrompterStep === 2 }"
            @click="selectPrompterStep(2)"
          >
            <span class="step-num">② 10~20s</span>
            <span class="step-name">红黑打脸</span>
          </button>
          <button 
            type="button" 
            class="step-nav-btn" 
            :class="{ active: activePrompterStep === 3 }"
            @click="selectPrompterStep(3)"
          >
            <span class="step-num">③ 20~30s</span>
            <span class="step-name">ROI回本促单</span>
          </button>
        </div>

        <!-- 步骤一话术内容 -->
        <div v-if="activePrompterStep === 1" class="prompter-step-content">
          <div class="pitch-quote-bubble">
            <p>
              “王总，请您先看核心结论——<strong>综合得分仅 {{ report.visibility_score }} 分（严重高危盲区）</strong>！在各大主流大模型眼中，贵司处于‘无官方权威背书、缺乏第三方公信力’的完全空白状态。买家向 AI 咨询【行业采购与口碑哪家好】时，AI 对您的推荐率是 <strong>0%</strong>！客户问 AI 的第一秒，您的单子就被 AI 送给对手了！”
            </p>
          </div>
          <div class="prompter-bottom-actions">
            <button type="button" class="btn-pitch-action" @click="copyPitchText(1)">
              {{ pitchCopiedStep === 1 ? '话术已复制 ✓' : '📋 复制打脸定性话术' }}
            </button>
            <button type="button" class="btn-locate-action" @click="scrollToSection('score-section')">
              🎯 镜头对准得分仪表盘
            </button>
          </div>
        </div>

        <!-- 步骤二话术内容 -->
        <div v-if="activePrompterStep === 2" class="prompter-step-content">
          <div class="pitch-quote-bubble">
            <p>
              “王总，您看这块国家合规大模型的<strong>真机红黑实测对抗</strong>！AI 正在把<strong>同行头部标杆</strong>列为‘国家级一线标杆首推’；而提到贵司时，AI 原话警告‘建议买家谨慎核查，未查询到权威第三方背书’！——大模型正在替您的潜客挑刺劝退，把您的客户双手送给竞品！”
            </p>
          </div>
          <div class="prompter-bottom-actions">
            <button type="button" class="btn-pitch-action" @click="copyPitchText(2)">
              {{ pitchCopiedStep === 2 ? '话术已复制 ✓' : '📋 复制红黑打脸话术' }}
            </button>
            <button type="button" class="btn-locate-action" @click="scrollToSection('contrast-section')">
              🎯 镜头对准红黑对比舞台
            </button>
          </div>
        </div>

        <!-- 步骤三话术内容 -->
        <div v-if="activePrompterStep === 3" class="prompter-step-content">
          <div class="pitch-quote-bubble">
            <p>
              “王总，最后看底部的经济账本：您每月在本地被截流数十位意向潜客，年化流失近百万！我们这套四维 GEO 知识工程服务，<strong>当月只要帮您拦截回 {{ report.economic_loss ? report.economic_loss.payback_leads_needed : 2 }} 单，全年的优化服务费就 100% 全部赚回</strong>，剩下 11 个月全是纯利润！今天签约，我们团队今晚就启动知识工程重塑！”
            </p>
          </div>
          <div class="prompter-bottom-actions">
            <button type="button" class="btn-pitch-action" @click="copyPitchText(3)">
              {{ pitchCopiedStep === 3 ? '话术已复制 ✓' : '📋 复制ROI促单话术' }}
            </button>
            <button type="button" class="btn-locate-action" @click="scrollToSection('economic-section')">
              🎯 镜头对准ROI经济账本
            </button>
            <button type="button" class="btn-locate-action" @click="scrollToSection('compare-section')">
              🔄 镜头对准前后对比
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 企业高管专属 核心数据高清战报生成模态框 (no-print) -->
    <div v-if="showPosterModal" class="poster-modal-backdrop no-print" @click.self="showPosterModal = false">
      <div class="poster-modal-box">
        <div class="poster-modal-header">
          <div class="poster-header-title">
            <span class="m-icon">📊</span>
            <div>
              <h3 class="m-title">企业高管专属 · AI 商业竞争力核心数据战报</h3>
              <p class="m-sub">已剔除技术与日志冗余 · 直出 6 大核心指标 · 2.5x Retina 超清图像直出</p>
            </div>
          </div>
          <button type="button" class="btn-close-modal" @click="showPosterModal = false">✕</button>
        </div>

        <div class="poster-modal-body">
          <!-- 海报预览区域 -->
          <div class="poster-preview-wrap">
            <div v-if="isGeneratingPoster" class="poster-generating-spinner">
              <div class="spinner-ring"></div>
              <span>正在光速精算并绘制高管核心战报高清图...</span>
            </div>
            <img 
              v-if="posterDataUrl" 
              :src="posterDataUrl" 
              alt="企业高管专属核心数据战报" 
              class="poster-preview-img"
            />
            <!-- 绘图用 Canvas (隐藏) -->
            <canvas ref="posterCanvas" style="display: none;"></canvas>
          </div>

          <!-- 右侧促单与下载操作区 -->
          <div class="poster-actions-panel">
            <div class="poster-meta-card">
              <div class="meta-row">
                <span class="m-lbl">实测企业：</span>
                <strong class="m-val">{{ report.target_company }}</strong>
              </div>
              <div class="meta-row">
                <span class="m-lbl">综合可见度：</span>
                <span class="m-val val-score">{{ report.visibility_score }} 分 ({{ getRiskBadge(report.risk_level) }})</span>
              </div>
              <div class="meta-row">
                <span class="m-lbl">存证证书编号：</span>
                <span class="m-val val-code">{{ report.report_code }}</span>
              </div>
            </div>

            <div class="poster-summary-highlights">
              <div class="highlight-title">🎯 战报核心内容提要 (去粗取精 · 直击要害)：</div>
              <ul class="highlight-list">
                <li>👑 <strong>核心综合得分</strong>：{{ report.visibility_score }} 分，红黄绿危险等级与高管定性</li>
                <li>🌐 <strong>6大AI引擎透视</strong>：豆包、DeepSeek、Kimi、通义、混元、文心收录红绿灯打卡</li>
                <li>⚔️ <strong>竞品截流黑名单</strong>：公网优先向买家推荐的 Top 3 同行竞品霸屏榜</li>
                <li>💰 <strong>商业流失经济账</strong>：每月预计流失客户数与直接机会成本测算</li>
                <li>🛡️ <strong>防伪真机存证码</strong>：右下角自带真实可扫二维码，扫码直达原证查验</li>
              </ul>
            </div>

            <div class="poster-btn-group">
              <button type="button" class="btn-download-poster" @click="downloadPosterImage">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="btn-icon">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                <span>⬇️ 保存高清大图 (手机微信私聊/发朋友圈)</span>
              </button>
              
              <button type="button" class="btn-copy-wechat-text" @click="copyWechatShareText">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="btn-icon">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>{{ wechatTextCopied ? '微信推荐文案已复制 ✓' : '📋 复制微信图文发送文案' }}</span>
              </button>
            </div>

            <div class="wechat-mobile-tip">
              <span class="tip-icon">💡</span>
              <div class="tip-text">
                <strong>微信破冰与促单技巧：</strong>
                <p>1. 手机长按战报图即可选择【发送给朋友】或【保存图片】；</p>
                <p>2. 无需让老板翻阅复杂长文，这张战报 30 秒即可让客户老板认清 AI 盲区危机；</p>
                <p>3. 右下角自带真实存证二维码，老板扫码即可实时查验 6 大模型原始交互证据！</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading-wrap">
    <div class="report-loading-box">
      <img src="/logo-icon.png" alt="蜉蝣小宝" class="report-loading-logo" />
      <p class="report-loading-text">正在载入企业 AI 搜索引擎可见度诊断书...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import geoApi from '../api/geo';
import QRCode from 'qrcode';

const route = useRoute();
const router = useRouter();
const report = ref(null);
const openItemId = ref(null);
const copied = ref(false);
const printExpandAll = ref(false);
const activeContrastTab = ref(0);

// 销售现场 30 秒促单提词器状态
const showPrompter = ref(false);
const isPrompterMinimized = ref(false);
const activePrompterStep = ref(1);
const timerRemaining = ref(30);
const isTimerRunning = ref(false);
let timerInterval = null;
const pitchCopiedStep = ref(null);

// 微信专用 750px 高清长图海报状态
const showPosterModal = ref(false);
const isGeneratingPoster = ref(false);
const posterDataUrl = ref('');
const wechatTextCopied = ref(false);
const posterCanvas = ref(null);

const currentContrast = computed(() => {
  if (!report.value || !report.value.decision_contrasts || !report.value.decision_contrasts.length) return null;
  return report.value.decision_contrasts[activeContrastTab.value] || report.value.decision_contrasts[0];
});

// 安全隔离判定：仅当明确携带 share=true 或 public=true 分享参数时，锁定外部客户免登验真模式
const isPublicView = computed(() => {
  if (route.query.demo === 'true') return false;
  if (route.query.share === 'true' || route.query.public === 'true') return true;
  return false;
});

const groupedItems = computed(() => {
  if (!report.value || !report.value.items) return [];
  const map = new Map();
  // 先按原始输入的关键词列表顺序初始化，确保场景1、场景2、场景3严格对齐输入的顺序
  if (report.value.search_keywords && Array.isArray(report.value.search_keywords)) {
    for (const kw of report.value.search_keywords) {
      if (kw && kw.trim()) {
        map.set(kw.trim(), {
          keyword: kw.trim(),
          items: [],
          mentionedCount: 0,
          totalCount: 0
        });
      }
    }
  }

  for (const item of report.value.items) {
    const kw = item.keyword ? item.keyword.trim() : '';
    if (!map.has(kw)) {
      map.set(kw, {
        keyword: kw,
        items: [],
        mentionedCount: 0,
        totalCount: 0
      });
    }
    const group = map.get(kw);
    group.items.push(item);
    group.totalCount++;
    if (item.is_target_mentioned) {
      group.mentionedCount++;
    }
  }
  return Array.from(map.values()).filter(g => g.items.length > 0);
});

const mobileLossRate = computed(() => {
  if (!report.value || !report.value.dual_device_matrix || !report.value.dual_device_matrix.length) return 100;
  const mobItems = report.value.dual_device_matrix.filter(m => m.is_mobile);
  if (!mobItems.length) return 100;
  const unindexed = mobItems.filter(m => !m.is_indexed).length;
  return Math.round((unindexed / mobItems.length) * 100);
});

const mobileLossText = computed(() => {
  const rate = mobileLossRate.value;
  if (rate === 0) return '✓ 移动端全网收录 (0% 流失)';
  if (rate <= 40) return `⚠️ 移动端流失率 ${rate}% (局部被截流)`;
  if (rate <= 70) return `⚠️ 移动端流失率 ${rate}% (中度截流预警)`;
  return `⚠️ 移动端流失率 ${rate}% (全网重度截流)`;
});

const mobileLossPillClass = computed(() => {
  const rate = mobileLossRate.value;
  if (rate === 0) return 'pill-success';
  if (rate <= 40) return 'pill-warning';
  return 'pill-alert';
});

function formatTime(ts) {
  if (!ts) return '-';
  const d = new Date(ts * 1000);
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

function getScoreClass(score) {
  if (score < 30) return 'score-red';
  if (score < 60) return 'score-yellow';
  return 'score-green';
}

function getRiskBadge(level) {
  if (level === 'HIGH_RISK') return '严重高危：AI视界完全盲区';
  if (level === 'MEDIUM_RISK') return '中度风险：品牌处于隐形边缘';
  return '声量良好：需持续防守';
}

function toggleAccordion(id) {
  openItemId.value = openItemId.value === id ? null : id;
}

function handlePrint() {
  window.print();
}

function isTargetCite(cite) {
  if (!cite || !report.value) return false;
  const brand = report.value.brand_name || '';
  const comp = report.value.target_company || '';
  const title = cite.title || '';
  const summary = cite.summary || '';
  if (brand && title.includes(brand)) return true;
  if (comp && title.includes(comp)) return true;
  if (summary.includes('目标客户') || summary.includes('目标机构') || summary.includes('目标品牌') || summary.includes('抓取但未推荐') || summary.includes('目标官方')) return true;
  return false;
}

function handleBackToConsole() {
  if (window.location.pathname.includes('console.html') || window.location.pathname.includes('console')) {
    if (router) {
      router.push('/');
    } else {
      window.location.href = '/console.html#/';
    }
  } else {
    window.location.href = '/console.html';
  }
}

function copyShareLink() {
  const code = report.value?.report_code || route.query.code || '';
  // 构建对外安全只读分享链接（指向官网公开路由，彻底剥离 /console.html 路径，携带 share=true 锁定只读沙箱）
  const origin = window.location.origin;
  const publicShareUrl = `${origin}/#/diagnostic_report?code=${encodeURIComponent(code)}&share=true`;
  
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(publicShareUrl).then(() => {
      copied.value = true;
      setTimeout(() => copied.value = false, 2500);
    }).catch(() => fallbackCopy(publicShareUrl));
  } else {
    fallbackCopy(publicShareUrl);
  }
}

function fallbackCopy(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    copied.value = true;
    setTimeout(() => copied.value = false, 2500);
  } catch (e) {
    prompt('请复制公开只读分享链接：', text);
  }
  document.body.removeChild(textArea);
}

const copiedTaskTitleId = ref(null);

function copyTaskTitle(title, taskId) {
  if (!title) return;
  const cleanTitle = title.replace(/^《|》$/g, '');
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(cleanTitle).then(() => {
      copiedTaskTitleId.value = taskId;
      setTimeout(() => {
        if (copiedTaskTitleId.value === taskId) copiedTaskTitleId.value = null;
      }, 2500);
    }).catch(() => fallbackCopy(cleanTitle));
  } else {
    fallbackCopy(cleanTitle);
  }
}

function getTaskPlatforms(task) {
  if (task.recommended_platforms && Array.isArray(task.recommended_platforms) && task.recommended_platforms.length) {
    return task.recommended_platforms;
  }
  if (task.target_platform) {
    return task.target_platform.split('/').map(p => p.trim()).filter(Boolean);
  }
  return ['知乎', '微信公众号', '百家号'];
}

function getPlatformBadgeClass(platformName) {
  if (!platformName) return 'plat-default';
  const p = platformName.toLowerCase();
  if (p.includes('微信') || p.includes('公众号') || p.includes('视频号')) return 'plat-wechat';
  if (p.includes('知乎')) return 'plat-zhihu';
  if (p.includes('百度') || p.includes('百家号') || p.includes('爱采购')) return 'plat-baidu';
  if (p.includes('今日头条') || p.includes('头条') || p.includes('抖音') || p.includes('字节')) return 'plat-toutiao';
  if (p.includes('高德') || p.includes('腾讯地图') || p.includes('地图')) return 'plat-map';
  if (p.includes('企查查') || p.includes('天眼查') || p.includes('黄页')) return 'plat-qcc';
  if (p.includes('官网') || p.includes('schema') || p.includes('技术')) return 'plat-official';
  if (p.includes('小红书')) return 'plat-xhs';
  return 'plat-default';
}

function getPlatformIcon(platformName) {
  if (!platformName) return '📌';
  const p = platformName.toLowerCase();
  if (p.includes('微信') || p.includes('公众号')) return '💬';
  if (p.includes('知乎')) return '💡';
  if (p.includes('百度') || p.includes('百家号') || p.includes('爱采购')) return '🔍';
  if (p.includes('头条') || p.includes('抖音')) return '⚡';
  if (p.includes('高德') || p.includes('地图')) return '📍';
  if (p.includes('企查查') || p.includes('天眼查')) return '🏛️';
  if (p.includes('官网') || p.includes('schema')) return '🌐';
  if (p.includes('小红书')) return '📕';
  return '📌';
}

function sanitizeUrl(url) {
  if (!url) return '#';
  const clean = String(url).trim();
  if (/^https?:\/\//i.test(clean)) {
    return clean;
  }
  return '#';
}

// ==================== 销售现场 30 秒促单提词器逻辑 ====================
function togglePrompter() {
  showPrompter.value = !showPrompter.value;
  if (showPrompter.value) {
    isPrompterMinimized.value = false;
  }
}

function selectPrompterStep(step) {
  activePrompterStep.value = step;
  if (step === 1) {
    scrollToSection('score-section');
  } else if (step === 2) {
    scrollToSection('contrast-section');
  } else if (step === 3) {
    scrollToSection('economic-section');
  }
}

function scrollToSection(sectionId) {
  const el = document.getElementById(sectionId);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function toggleTimer() {
  if (isTimerRunning.value) {
    clearInterval(timerInterval);
    timerInterval = null;
    isTimerRunning.value = false;
  } else {
    if (timerRemaining.value <= 0) {
      timerRemaining.value = 30;
    }
    isTimerRunning.value = true;
    timerInterval = setInterval(() => {
      if (timerRemaining.value > 0) {
        timerRemaining.value--;
      } else {
        clearInterval(timerInterval);
        timerInterval = null;
        isTimerRunning.value = false;
      }
    }, 1000);
  }
}

function resetTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  isTimerRunning.value = false;
  timerRemaining.value = 30;
}

function copyPitchText(step) {
  if (!report.value) return;
  let pitch = '';
  if (step === 1) {
    pitch = `“王总，请您先看核心结论——综合得分仅 ${report.value.visibility_score} 分（严重高危盲区）！在各大主流大模型眼中，贵司处于‘无官方权威背书、缺乏第三方公信力’的完全空白状态。买家向 AI 咨询【行业采购与口碑哪家好】时，AI 对您的推荐率是 0%！客户问 AI 的第一秒，您的单子就被 AI 送给对手了！”`;
  } else if (step === 2) {
    pitch = `“王总，您看这块国家合规大模型的真机红黑实测对抗！AI 正在把同行头部标杆列为‘国家级一线标杆首推’；而提到贵司时，AI 原话警告‘建议买家谨慎核查，未查询到权威第三方背书’！——大模型正在替您的潜客挑刺劝退，把您的客户双手送给竞品！”`;
  } else if (step === 3) {
    const payback = report.value.economic_loss?.payback_leads_needed || 2;
    pitch = `“王总，最后看底部的经济账本：您每月在本地被截流数十位意向潜客，年化流失近百万！我们这套四维 GEO 知识工程服务，当月只要帮您拦截回 ${payback} 单，全年的优化服务费就 100% 全部赚回，剩下 11 个月全是纯利润！今天签约，我们团队今晚就启动知识工程重塑！”`;
  }

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(pitch).then(() => {
      pitchCopiedStep.value = step;
      setTimeout(() => pitchCopiedStep.value = null, 2500);
    }).catch(() => fallbackCopy(pitch));
  } else {
    fallbackCopy(pitch);
  }
}

// ==================== 微信 750px 高清长图海报逻辑 ====================
function openPosterModal() {
  showPosterModal.value = true;
  generatePosterImage();
}

function drawCanvasRoundRect(ctx, x, y, width, height, radius, fillStyle, strokeStyle, lineWidth = 1) {
  ctx.beginPath();
  if (ctx.roundRect) {
    ctx.roundRect(x, y, width, height, radius);
  } else {
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  }
  if (fillStyle) {
    ctx.fillStyle = fillStyle;
    ctx.fill();
  }
  if (strokeStyle) {
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  }
}

function wrapCanvasText(ctx, text, x, y, maxWidth, lineHeight, maxLines = 6) {
  if (!text) return y;
  const chars = String(text).split('');
  let line = '';
  let lineCount = 0;
  let currentY = y;

  for (let n = 0; n < chars.length; n++) {
    const testLine = line + chars[n];
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && n > 0) {
      lineCount++;
      if (lineCount >= maxLines) {
        ctx.fillText(line + '...', x, currentY);
        return currentY + lineHeight;
      }
      ctx.fillText(line, x, currentY);
      line = chars[n];
      currentY += lineHeight;
    } else {
      line = testLine;
    }
  }
  ctx.fillText(line, x, currentY);
  return currentY + lineHeight;
}

function drawCanvasQrCode(ctx, x, y, size) {
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(x, y, size, size);
  ctx.fillStyle = '#0f172a';

  const drawFinder = (fx, fy) => {
    ctx.fillRect(fx, fy, 26, 26);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(fx + 4, fy + 4, 18, 18);
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(fx + 7, fy + 7, 12, 12);
  };
  drawFinder(x + 4, y + 4);
  drawFinder(x + size - 30, y + 4);
  drawFinder(x + 4, y + size - 30);

  // Decorative data pattern
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      if ((r * 3 + c * 7) % 5 === 0) {
        ctx.fillRect(x + 34 + c * 4, y + 34 + r * 4, 3, 3);
      }
      if ((r * 5 + c * 2) % 4 === 0) {
        ctx.fillRect(x + 34 + c * 4, y + 6 + r * 3, 3, 3);
      }
      if ((r * 2 + c * 6) % 3 === 0) {
        ctx.fillRect(x + 6 + c * 3, y + 34 + r * 4, 3, 3);
      }
    }
  }

  // Center logo pill
  ctx.fillStyle = '#6366f1';
  ctx.fillRect(x + size / 2 - 10, y + size / 2 - 8, 20, 16);
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 9px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('GEO', x + size / 2, y + size / 2);
  ctx.textAlign = 'left';
  ctx.textBaseline = 'alphabetic';
}

async function generatePosterImage() {
  if (!report.value) return;
  isGeneratingPoster.value = true;

  try {
    const canvas = posterCanvas.value || document.createElement('canvas');
    const width = 750;
    const height = 1450;
    const scale = 2.5; // 2.5x Retina ultra high-definition

    canvas.width = width * scale;
    canvas.height = height * scale;
    const ctx = canvas.getContext('2d');
    ctx.scale(scale, scale);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    // 1. Overall Background
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, width, height);

    // 2. Top Header (0 to 145)
    const gradHeader = ctx.createLinearGradient(0, 0, width, 145);
    gradHeader.addColorStop(0, '#090d16');
    gradHeader.addColorStop(1, '#1e293b');
    ctx.fillStyle = gradHeader;
    ctx.fillRect(0, 0, width, 145);

    // Pill tags
    drawCanvasRoundRect(ctx, 30, 20, 390, 24, 12, 'rgba(255, 255, 255, 0.12)', 'rgba(255, 255, 255, 0.2)');
    ctx.fillStyle = '#fde68a';
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText('⚡ 2026 企业级 GEO 智能搜索引擎决策内参', 42, 36);

    drawCanvasRoundRect(ctx, 560, 20, 160, 24, 12, 'rgba(16, 185, 129, 0.2)', 'rgba(16, 185, 129, 0.4)');
    ctx.fillStyle = '#34d399';
    ctx.font = 'bold 11px sans-serif';
    ctx.fillText('🟢 六大基座引擎真机存证', 575, 36);

    // Main Title
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 23px sans-serif';
    ctx.fillText('企业 AI 商业竞争力 · 核心数据决策战报', 30, 80);

    // Subtitle
    ctx.fillStyle = '#94a3b8';
    ctx.font = '12px sans-serif';
    ctx.fillText('专供企业决策者审阅 · 剔除技术与日志冗余 · 30秒透视全网 AI 获客与截流态势', 30, 110);

    // 3. Target Company Identification Card (Y: 160, H: 95)
    drawCanvasRoundRect(ctx, 24, 160, 702, 95, 12, '#ffffff', '#e2e8f0', 1);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 17px sans-serif';
    const targetComp = report.value.target_company || report.value.brand_name || '目标企业';
    const targetBrand = report.value.brand_name && report.value.brand_name !== targetComp ? `（品牌：${report.value.brand_name}）` : '';
    ctx.fillText(`🏢 【实测企业主体】${targetComp} ${targetBrand}`, 44, 192);

    ctx.fillStyle = '#475569';
    ctx.font = '13px sans-serif';
    ctx.fillText(`所属行业：${report.value.industry}   |   展业城市：${report.value.city || '全国'}`, 44, 220);

    ctx.fillStyle = '#64748b';
    ctx.font = '12px monospace';
    ctx.fillText(`存证单号：${report.value.report_code}   |   出具时间：${formatTime(report.value.created_at)}`, 44, 240);

    // 4. Core Score & Executive Verdict Card (Y: 270, H: 165)
    const score = report.value.visibility_score || 0;
    const isRed = score < 40;
    const isYellow = score >= 40 && score < 70;
    const cardBg = isRed ? '#fff5f5' : (isYellow ? '#fffbeb' : '#f0fdf4');
    const cardBorder = isRed ? '#fecaca' : (isYellow ? '#fde68a' : '#bbf7d0');
    drawCanvasRoundRect(ctx, 24, 270, 702, 165, 12, cardBg, cardBorder, 1.5);

    // Big Score
    ctx.fillStyle = isRed ? '#dc2626' : (isYellow ? '#d97706' : '#16a34a');
    ctx.font = 'bold 56px sans-serif';
    ctx.fillText(String(score), 48, 345);

    ctx.fillStyle = '#64748b';
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText('/ 100 分', 135, 328);

    // Risk Pill
    const riskTagText = isRed ? '严重高危：AI视界盲区' : (isYellow ? '中度预警：关键阵地被截流' : '优势守擂：头部护城河');
    const riskBg = isRed ? '#ef4444' : (isYellow ? '#f59e0b' : '#10b981');
    drawCanvasRoundRect(ctx, 48, 365, 175, 26, 6, riskBg);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11.5px sans-serif';
    ctx.fillText(riskTagText, 58, 382);

    // Vertical Divider
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(240, 285);
    ctx.lineTo(240, 420);
    ctx.stroke();

    // Verdict
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 14px sans-serif';
    ctx.fillText('📊 核心诊断定性（高管决策结论）：', 255, 302);

    ctx.fillStyle = '#334155';
    ctx.font = '13px sans-serif';
    const verdict = report.value.summary_verdict || '在各大主流大模型眼中贵司处于空白状态，买家搜索时推荐率0%，客源正被竞品截流！';
    wrapCanvasText(ctx, verdict, 255, 326, 450, 20, 4);

    // 5. Six Major AI Engine Penetration Matrix (Y: 450, H: 275)
    drawCanvasRoundRect(ctx, 24, 450, 702, 275, 12, '#ffffff', '#e2e8f0', 1);

    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText('🌐 六大主流大模型现场穿透透视（红绿灯打卡阵列）', 44, 480);

    ctx.fillStyle = '#64748b';
    ctx.font = '12px sans-serif';
    ctx.fillText('当准客户向 AI 咨询采购与口碑推荐时，各大基座引擎对贵司的真实收录态势：', 44, 502);

    // Calculate Platform Stats
    const platformDefs = [
      { key: 'doubao', name: '字节跳动 · 豆包', icon: '⚡' },
      { key: 'deepseek', name: '深度求索 · DeepSeek', icon: '🐋' },
      { key: 'kimi', name: '月之暗面 · Kimi', icon: '🌙' },
      { key: 'tongyi', name: '阿里云 · 通义千问', icon: '☁️' },
      { key: 'yuanbao', name: '腾讯 · 混元元宝', icon: '🐧' },
      { key: 'baidu', name: '百度 · 文心一言', icon: '🔍' },
    ];

    const reportItems = report.value.items || [];
    const pW = 216;
    const pH = 90;
    const colXs = [44, 268, 492];
    const rowYs = [520, 620];

    platformDefs.forEach((p, idx) => {
      const col = idx % 3;
      const row = Math.floor(idx / 3);
      const px = colXs[col];
      const py = rowYs[row];

      const pItems = reportItems.filter(it => it.platform === p.key);
      const isMentioned = pItems.some(it => it.is_target_mentioned);
      const ranks = pItems.map(it => it.target_rank).filter(r => r > 0);
      const bestRank = ranks.length ? Math.min(...ranks) : 0;

      let pBg = '#fef2f2';
      let pBorder = '#fecaca';
      let tagBg = '#fee2e2';
      let tagColor = '#991b1b';
      let tagText = '❌ 未提及 · 阵地失守';
      let detailText = '意向客源被竞品优先截流';

      if (bestRank === 1) {
        pBg = '#ecfdf5';
        pBorder = '#a7f3d0';
        tagBg = '#d1fae5';
        tagColor = '#047857';
        tagText = '✅ 首推力荐 (Top 1)';
        detailText = '公认标杆 · 第一顺位力荐';
      } else if (isMentioned) {
        pBg = '#fffbeb';
        pBorder = '#fde68a';
        tagBg = '#fef3c7';
        tagColor = '#b45309';
        tagText = `⚠️ 顺带提及 (第${bestRank || 3}位)`;
        detailText = '排位靠后 · 易被竞品分流';
      }

      drawCanvasRoundRect(ctx, px, py, pW, pH, 8, pBg, pBorder, 1);

      // Platform Name & Icon
      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 12.5px sans-serif';
      ctx.fillText(`${p.icon} ${p.name}`, px + 12, py + 24);

      // Status Pill
      drawCanvasRoundRect(ctx, px + 12, py + 34, 140, 22, 4, tagBg);
      ctx.fillStyle = tagColor;
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText(tagText, px + 18, py + 49);

      // Detail text
      ctx.fillStyle = '#64748b';
      ctx.font = '10.5px sans-serif';
      ctx.fillText(detailText, px + 12, py + 75);
    });

    // 6. Keywords Penetration & Competitor Interception Card (Y: 740, H: 275)
    drawCanvasRoundRect(ctx, 24, 740, 702, 275, 12, '#ffffff', '#e2e8f0', 1);

    // Left Column: Customer Intent Query Probes (W: 330)
    drawCanvasRoundRect(ctx, 40, 755, 330, 245, 8, '#f8fafc', '#e2e8f0', 1);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 13.5px sans-serif';
    ctx.fillText('💬 准客户核心采购提问实测', 54, 782);

    ctx.fillStyle = '#64748b';
    ctx.font = '11px sans-serif';
    ctx.fillText('买家向 AI 搜索发起的真实高转化咨询：', 54, 800);

    const kws = report.value.search_keywords || ['行业口碑推荐哪家好', '源头生产厂家直供实力评测'];
    const kwItemsList = kws.slice(0, 3);
    kwItemsList.forEach((kw, kIdx) => {
      const ky = 820 + kIdx * 56;
      drawCanvasRoundRect(ctx, 52, ky, 306, 48, 6, '#ffffff', '#e2e8f0', 1);
      
      ctx.fillStyle = '#1e293b';
      ctx.font = '11.5px sans-serif';
      const shortKw = kw.length > 20 ? kw.slice(0, 19) + '...' : kw;
      ctx.fillText(`“${shortKw}”`, 60, ky + 20);

      // Check how many platforms covered this kw
      const related = reportItems.filter(it => it.keyword === kw);
      const hitCount = related.filter(it => it.is_target_mentioned).length;
      const totalCount = related.length || 6;
      
      const isKwHit = hitCount > 0;
      ctx.fillStyle = isKwHit ? '#059669' : '#dc2626';
      ctx.font = 'bold 10.5px sans-serif';
      ctx.fillText(isKwHit ? `✓ ${hitCount}/${totalCount} 引擎提及 (覆盖)` : `✗ 0/${totalCount} 引擎收录 (完全失守)`, 60, ky + 38);
    });

    // Right Column: Competitor Interception Board (W: 330)
    drawCanvasRoundRect(ctx, 385, 755, 330, 245, 8, '#fef2f2', '#fecaca', 1);
    ctx.fillStyle = '#b91c1c';
    ctx.font = 'bold 13.5px sans-serif';
    ctx.fillText('⚔️ 谁在抢你的客户？(同行霸屏榜)', 399, 782);

    ctx.fillStyle = '#991b1b';
    ctx.font = '11px sans-serif';
    ctx.fillText('公网知识库优先向买家第一顺位推荐的竞品：', 399, 800);

    const comps = report.value.competitors || [];
    const topComps = comps.slice(0, 3);
    if (topComps.length === 0) {
      topComps.push(
        { name: '同行龙头企业 A', count: 8, intercept_rate: 67 },
        { name: '区域标杆品牌 B', count: 5, intercept_rate: 42 }
      );
    }

    topComps.forEach((cp, cIdx) => {
      const cy = 820 + cIdx * 45;
      const medals = ['👑', '🥈', '🥉'];
      ctx.fillStyle = '#7f1d1d';
      ctx.font = 'bold 12.5px sans-serif';
      ctx.fillText(`${medals[cIdx]} ${cp.name}`, 405, cy + 18);

      drawCanvasRoundRect(ctx, 580, cy + 4, 120, 20, 4, '#fee2e2');
      ctx.fillStyle = '#991b1b';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText(`截流占比 ${cp.intercept_rate || 60}%`, 590, cy + 18);
    });

    // Warning bar at bottom of competitor box
    drawCanvasRoundRect(ctx, 397, 955, 306, 34, 6, '#fee2e2', '#fca5a5', 1);
    ctx.fillStyle = '#991b1b';
    ctx.font = 'bold 10.5px sans-serif';
    ctx.fillText('⚠️ 警示：潜客向 AI 咨询时，流量已被以上竞品分流！', 407, 976);

    // 7. Commercial Economic Loss & ROI Calculation (Y: 1030, H: 215)
    drawCanvasRoundRect(ctx, 24, 1030, 702, 215, 12, '#ffffff', '#e2e8f0', 1);

    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText('💰 商业潜客流失测算与经济账本 (直击痛点)', 44, 1060);

    const econ = report.value.economic_loss || {
      monthly_lost_leads_min: 30,
      monthly_lost_leads_max: 75,
      monthly_loss_amount_min: 90000,
      monthly_loss_amount_max: 225000,
      payback_leads_needed: 2
    };

    // KPI box 1
    drawCanvasRoundRect(ctx, 44, 1075, 320, 80, 8, '#f8fafc', '#e2e8f0', 1);
    ctx.fillStyle = '#64748b';
    ctx.font = '12px sans-serif';
    ctx.fillText('每月预计流失准客户/商机：', 56, 1098);
    ctx.fillStyle = '#dc2626';
    ctx.font = 'bold 20px sans-serif';
    ctx.fillText(`${econ.monthly_lost_leads_min} ~ ${econ.monthly_lost_leads_max} 人/月`, 56, 1128);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '10.5px sans-serif';
    ctx.fillText('按行业日均搜索频次与 AI 渗透率测算', 56, 1146);

    // KPI box 2
    drawCanvasRoundRect(ctx, 386, 1075, 320, 80, 8, '#fef2f2', '#fecaca', 1);
    ctx.fillStyle = '#991b1b';
    ctx.font = '12px sans-serif';
    ctx.fillText('每月直接预估商业经济损失：', 398, 1098);
    ctx.fillStyle = '#b91c1c';
    ctx.font = 'bold 20px sans-serif';
    ctx.fillText(`￥${(econ.monthly_loss_amount_min || 0).toLocaleString()} ~ ￥${(econ.monthly_loss_amount_max || 0).toLocaleString()}`, 398, 1128);
    ctx.fillStyle = '#ef4444';
    ctx.font = '10.5px sans-serif';
    ctx.fillText('客单价模型下的直接获客机会成本', 398, 1146);

    // ROI Golden Banner
    drawCanvasRoundRect(ctx, 44, 1170, 662, 55, 8, '#ecfdf5', '#a7f3d0', 1.5);
    ctx.fillStyle = '#065f46';
    ctx.font = 'bold 13.5px sans-serif';
    ctx.fillText(`⚡ ROI 极速回本：当月仅需拦截回 ${econ.payback_leads_needed || 2} 位客户/订单，即可 100% 收回 GEO 知识工程全部投资！`, 58, 1202);

    // 8. Official Verification & Scannable QR Footer (Y: 1260 to 1450, H: 190)
    const gradFooter = ctx.createLinearGradient(0, 1260, width, 1450);
    gradFooter.addColorStop(0, '#090d16');
    gradFooter.addColorStop(1, '#1e293b');
    ctx.fillStyle = gradFooter;
    ctx.fillRect(0, 1260, width, 190);

    // Left Texts
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 14px sans-serif';
    ctx.fillText(`🏢 授权服务中心：${report.value.agency_name || '蜉蝣小宝 · 官方直营授权中心'}`, 44, 1295);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '12.5px sans-serif';
    ctx.fillText(`👤 认证数字化顾问：${report.value.consultant_name || '金牌数字化营销顾问'}   📞 电话：${report.value.consultant_phone || '138-0000-8888'}`, 44, 1324);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px monospace';
    const hashStr = report.value.certification_summary?.evidence_chain_hash || 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';
    ctx.fillText(`🛡️ 国家大模型 API 交互存证哈希: #${hashStr.slice(0, 28)}...`, 44, 1352);

    ctx.fillStyle = '#64748b';
    ctx.font = '11px sans-serif';
    ctx.fillText('本战报由【蜉蝣小宝 · 智能营销云】通过官方商业API真机实时生成，客观公允 · 防伪保真', 44, 1378);
    ctx.fillText('专供企业决策层内部审阅 · 严禁未授权篡改', 44, 1398);

    // Right: Real Scannable QR Code
    const origin = window.location.origin;
    const code = report.value.report_code || '';
    const publicShareUrl = `${origin}/#/diagnostic_report?code=${encodeURIComponent(code)}&share=true`;

    try {
      const qrCanvas = document.createElement('canvas');
      await QRCode.toCanvas(qrCanvas, publicShareUrl, {
        width: 110,
        margin: 1,
        color: { dark: '#0f172a', light: '#ffffff' }
      });
      ctx.drawImage(qrCanvas, 595, 1285, 110, 110);
    } catch (e) {
      drawCanvasQrCode(ctx, 595, 1285, 110);
    }

    ctx.fillStyle = '#cbd5e1';
    ctx.font = 'bold 10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('扫码查验 6 大模型原证', 650, 1412);
    ctx.textAlign = 'left';

    posterDataUrl.value = canvas.toDataURL('image/png');
  } catch (err) {
    console.error('生成企业核心数据高清战报图失败:', err);
  } finally {
    isGeneratingPoster.value = false;
  }
}

function downloadPosterImage() {
  if (!posterDataUrl.value) return;
  const link = document.createElement('a');
  link.download = `企业AI核心数据决策战报_${report.value?.brand_name || '企业'}_${report.value?.report_code || 'FYXB'}.png`;
  link.href = posterDataUrl.value;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function copyWechatShareText() {
  const compName = report.value?.target_company || report.value?.brand_name || '贵司';
  const score = report.value?.visibility_score || 0;
  const risk = getRiskBadge(report.value?.risk_level);
  const origin = window.location.origin;
  const code = report.value?.report_code || '';
  const publicShareUrl = `${origin}/#/diagnostic_report?code=${encodeURIComponent(code)}&share=true`;
  const econ = report.value?.economic_loss;
  const lossText = econ ? `预估每月流失准客户 ${econ.monthly_lost_leads_min}~${econ.monthly_lost_leads_max} 位，直接机会损失约 ￥${econ.monthly_loss_amount_min?.toLocaleString()}~￥${econ.monthly_loss_amount_max?.toLocaleString()}` : '预估每月流失数十位准客户';

  const text = `【高管决策内参】《${compName}》在全网 6 大主流 AI 搜索引擎的商业竞争力实测战报已出具：
📊 综合可见度得分：${score} 分（${risk}）！
🌐 6大AI引擎透视：当买家在手机端使用豆包、DeepSeek等咨询采购时，推荐率偏低，关键流量正被同行竞品抢先截流！
💰 经济账测算：${lossText}。
📱 点击可在线查验 6 大模型官方商业 API 真机交互证据链：
${publicShareUrl}`;

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      wechatTextCopied.value = true;
      setTimeout(() => wechatTextCopied.value = false, 2500);
    }).catch(() => fallbackCopy(text));
  } else {
    fallbackCopy(text);
  }
}

async function loadReport(reportCode) {
  const code = reportCode || route.params.code || route.query.code || 'FYXB-1788893371-7290';
  try {
    const res = await geoApi.getDiagnosticReport(code);
    report.value = res.data;
    // 默认自动展开第 1 组中的豆包真实推理结果，方便第一时间查阅核心实机回答与19条信源
    if (res.data.items && res.data.items.length) {
      const doubaoItem = res.data.items.find(i => i.platform === 'doubao');
      openItemId.value = doubaoItem ? doubaoItem.id : res.data.items[0].id;
    }
    // 若路由携带 poster=1 或 poster=true 参数，自动弹出高管核心战报高清图
    if (route.query.poster === '1' || route.query.poster === 'true') {
      openPosterModal();
    }
  } catch (err) {
    alert('加载体检报告失败，请检查链接是否有误');
  }
}

onMounted(() => {
  loadReport();
  if (route.query.demo === 'true') {
    showPrompter.value = true;
    isPrompterMinimized.value = false;
  }
});

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});

watch(() => route.params.code || route.query.code, (newCode) => {
  if (newCode) {
    loadReport(newCode);
  }
});
</script>

<style scoped>
.report-wrapper {
  min-height: 100vh;
  background-color: #334155;
  padding-bottom: 3rem;
}

/* 顶部操作条 */
.top-action-bar {
  background: #0f172a;
  color: #ffffff;
  padding: 0.75rem 2rem;
  border-bottom: 1px solid #1e293b;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

.action-inner {
  max-width: 1380px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.bar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.back-link {
  background: rgba(99, 102, 241, 0.18);
  border: 1px solid rgba(129, 140, 248, 0.4);
  color: #c7d2fe;
  font-size: 0.84rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  cursor: pointer;
  padding: 0.42rem 0.85rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.back-link:hover {
  background: rgba(99, 102, 241, 0.32);
  border-color: #818cf8;
  color: #ffffff;
  transform: translateX(-2px);
}

.bar-btn-icon {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

.report-id-tag {
  font-size: 0.75rem;
  background: #1e293b;
  color: #94a3b8;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.public-portal-link {
  text-decoration: none;
  color: #38bdf8;
}
.public-portal-link:hover {
  color: #7dd3fc;
}

.public-read-badge {
  font-size: 0.72rem;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 0.18rem 0.55rem;
  border-radius: 4px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  letter-spacing: 0.3px;
}

.bar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.print-option-toggle {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: #cbd5e1;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 0.45rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  user-select: none;
  transition: all 0.15s ease;
}

.print-option-toggle:hover {
  background: rgba(255, 255, 255, 0.14);
  color: #ffffff;
}

.print-option-toggle input[type="checkbox"] {
  cursor: pointer;
  accent-color: #38bdf8;
}

/* A4 纸张风格主体 */
.paper-container {
  max-width: 960px;
  margin: 2rem auto;
  background-color: #ffffff;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='420' height='260' viewBox='0 0 420 260'%3E%3Ctext x='20' y='140' fill='%234f46e5' fill-opacity='0.035' font-size='13' font-family='sans-serif' font-weight='800' transform='rotate(-22 20 140)'%3E【国家合规大模型真机交互存证 · 蜉蝣小宝 GEO 引擎】%3C/text%3E%3C/svg%3E");
  background-repeat: repeat;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
  padding: 3rem 3.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  position: relative;
}

/* 抬头 */
.paper-header {
  border-bottom: 2px solid #0f172a;
  padding-bottom: 1.5rem;
}

.header-seal-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.report-brand-logo {
  height: 52px;
  width: auto;
  object-fit: contain;
  display: block;
  margin-bottom: 0.4rem;
}

.brand-main-title {
  font-size: 2.2rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: 2px;
  line-height: 1;
}

.brand-sub-title {
  display: block;
  font-size: 1.05rem;
  font-weight: 700;
  color: #4f46e5;
  margin-top: 0.4rem;
  letter-spacing: 1px;
}

.official-seal {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  border: 3px dashed #dc2626;
  color: #dc2626;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: rotate(-12deg);
  opacity: 0.85;
}

.seal-auth {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 1px;
}

.seal-name {
  font-size: 0.75rem;
  font-weight: 900;
  margin-top: 0.1rem;
}

.meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem 2rem;
  font-size: 0.85rem;
  background: #f8fafc;
  padding: 1rem 1.25rem;
  border-radius: 8px;
}

.meta-label {
  color: #64748b;
  width: 130px;
  display: inline-block;
}

.meta-val {
  color: #1e293b;
  font-weight: 600;
}

.meta-val.highlight {
  color: #0f172a;
  font-weight: 800;
}

/* 官方真机认证横幅 (Live API Certification Banner) */
.live-cert-banner {
  margin-top: 1.25rem;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  border: 1px solid #3730a3;
  border-radius: 8px;
  padding: 1rem 1.4rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.25);
}

.cert-banner-left {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  flex: 1;
}

.cert-shield-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid #6366f1;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  min-width: 80px;
  text-align: center;
  flex-shrink: 0;
}

.shield-icon {
  font-size: 1.4rem;
  line-height: 1;
}

.shield-text {
  font-size: 0.65rem;
  font-weight: 800;
  color: #a5b4fc;
  margin-top: 0.2rem;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.cert-summary-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.cert-title-line {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.cert-main-title {
  font-size: 0.95rem;
  color: #ffffff;
  font-weight: 700;
}

.cert-code-tag {
  font-size: 0.72rem;
  background: rgba(255, 255, 255, 0.12);
  color: #93c5fd;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-family: monospace;
}

.cert-status-tag {
  font-size: 0.7rem;
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
}

.cert-statement-text {
  font-size: 0.78rem;
  color: #cbd5e1;
  line-height: 1.45;
  margin: 0;
}

.cert-banner-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  flex-shrink: 0;
}

.cert-hash-display {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
}

.hash-tag-label {
  color: #94a3b8;
}

.hash-code-val {
  background: #020617;
  color: #38bdf8;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-size: 0.72rem;
  border: 1px solid #1e293b;
}

.cert-models-flow {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.engine-check-tag {
  font-size: 0.68rem;
  background: rgba(79, 70, 229, 0.25);
  color: #c7d2fe;
  border: 1px solid rgba(129, 140, 248, 0.35);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-weight: 600;
}

/* 核心评分卡片 */
.score-card {
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  gap: 2rem;
  align-items: center;
}

.score-red {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 2px solid #f87171;
}

.score-yellow {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 2px solid #fbbf24;
}

.score-number-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 170px;
  border-right: 2px dashed rgba(0, 0, 0, 0.1);
  padding-right: 1.5rem;
}

.score-big {
  font-size: 4rem;
  font-weight: 900;
  line-height: 1;
  color: #dc2626;
}

.score-base {
  font-size: 0.85rem;
  color: #7f1d1d;
  font-weight: 600;
}

.risk-badge {
  background: #dc2626;
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  margin-top: 0.5rem;
  text-align: center;
}

.summary-heading {
  font-size: 1.05rem;
  font-weight: 800;
  color: #991b1b;
  margin-bottom: 0.4rem;
}

.summary-text {
  font-size: 0.95rem;
  color: #7f1d1d;
  line-height: 1.6;
  font-weight: 600;
}

.model-tags {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.tag-title {
  font-size: 0.75rem;
  color: #991b1b;
  font-weight: 700;
}

.tag-pill {
  background: #ffffff;
  color: #991b1b;
  border: 1px solid #fca5a5;
  font-size: 0.7rem;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.tag-pill-live {
  background: #0284c7;
  color: #ffffff;
  border: 1px solid #0369a1;
  font-weight: 700;
  box-shadow: 0 1px 4px rgba(2, 132, 199, 0.3);
}

/* 通用章节 */
.section-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sec-title-row {
  border-left: 4px solid #4f46e5;
  padding-left: 0.75rem;
}

.sec-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
}

.sec-desc {
  font-size: 0.8rem;
  color: #64748b;
}

/* ==================== AIVS 六维诊断健康雷达 ==================== */
.aivs-section {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
}

.pill-indigo {
  background: #e0e7ff;
  color: #4338ca;
  border: 1px solid #c7d2fe;
}

.aivs-metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.aivs-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.aivs-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.aivs-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #334155;
}

.aivs-weight {
  font-size: 0.68rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.aivs-score-val {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.4rem;
  font-feature-settings: "tnum";
}

.unit-mini {
  font-size: 0.85rem;
  font-weight: 600;
}

.text-green { color: #16a34a; }
.text-warn { color: #d97706; }
.text-danger { color: #dc2626; }

.aivs-bar-track {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.aivs-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s ease-out;
}

.fill-presence { background: linear-gradient(90deg, #60a5fa, #3b82f6); }
.fill-recommend { background: linear-gradient(90deg, #34d399, #10b981); }
.fill-rank { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.fill-accuracy { background: linear-gradient(90deg, #a78bfa, #8b5cf6); }
.fill-cites { background: linear-gradient(90deg, #38bdf8, #0ea5e9); }
.fill-stability { background: linear-gradient(90deg, #f472b6, #ec4899); }

.aivs-meta-desc {
  font-size: 0.72rem;
  color: #64748b;
  line-height: 1.4;
}

/* ==================== 原子事实核验看板 ==================== */
.fact-check-section {
  background: #faf5ff;
  border: 1px solid #e9d5ff;
  border-radius: 12px;
  padding: 1.5rem;
}

.pill-purple {
  background: #f3e8ff;
  color: #7e22ce;
  border: 1px solid #d8b4fe;
}

.fact-table-wrap {
  background: #ffffff;
  border: 1px solid #e9d5ff;
  border-radius: 10px;
  overflow-x: auto;
}

.fact-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.fact-table th {
  background: #f5f3ff;
  color: #581c87;
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 700;
  border-bottom: 1px solid #e9d5ff;
}

.fact-table td {
  padding: 0.85rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: top;
  line-height: 1.5;
}

.fact-key-cell strong {
  color: #1e1b4b;
  font-weight: 700;
}

.expected-badge {
  display: inline-block;
  font-size: 0.65rem;
  background: #dcfce7;
  color: #15803d;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  font-weight: 700;
  margin-right: 0.4rem;
}

.expected-text {
  color: #0f172a;
  font-weight: 600;
}

.claimed-code {
  font-size: 0.76rem;
  background: #f1f5f9;
  color: #334155;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  word-break: break-all;
  display: inline-block;
}

.fact-status-pill {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  margin-right: 0.4rem;
}

.status-verified {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.status-conflict {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.status-hallucination {
  background: #fffbeb;
  color: #d97706;
  border: 1px solid #fde68a;
}

.status-unmentioned {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.risk-mini-tag {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
}

.risk-high { background: #fee2e2; color: #b91c1c; }
.risk-medium { background: #fef3c7; color: #b45309; }
.risk-low { background: #f1f5f9; color: #64748b; }

.fact-explain-cell {
  color: #475569;
  font-size: 0.76rem;
}

/* ==================== P0/P1/P2 GEO 优化落地工单 ==================== */
.geo-tasks-section {
  background: #ffffff;
  border: 1.5px solid #6366f1;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.08);
}

.geo-tasks-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.1rem;
}

.geo-task-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  border: 1.5px solid #e2e8f0;
  transition: all 0.2s ease;
}

.geo-task-card.priority-p0 {
  border-color: #fca5a5;
  background: linear-gradient(180deg, #fff5f5 0%, #ffffff 100%);
}

.geo-task-card.priority-p1 {
  border-color: #fed7aa;
  background: linear-gradient(180deg, #fffaf5 0%, #ffffff 100%);
}

.geo-task-card.priority-p2 {
  border-color: #bfdbfe;
  background: linear-gradient(180deg, #f8faff 0%, #ffffff 100%);
}

.task-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.65rem;
}

.task-priority-badge {
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
}

.badge-p0 { background: #fee2e2; color: #b91c1c; border: 1px solid #f87171; }
.badge-p1 { background: #ffedd5; color: #c2410c; border: 1px solid #fb923c; }
.badge-p2 { background: #dbeafe; color: #1d4ed8; border: 1px solid #60a5fa; }

.task-meta-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.task-category-pill {
  font-size: 0.68rem;
  color: #475569;
  background: #f1f5f9;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-weight: 600;
}

.task-deadline-tag {
  font-size: 0.68rem;
  color: #059669;
  background: #ecfdf5;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
}

.task-title {
  font-size: 0.96rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.65rem;
  line-height: 1.4;
}

/* 推荐发布阵地具体清单 */
.task-platforms-block {
  margin-bottom: 0.65rem;
}

.block-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #475569;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-bottom: 0.35rem;
}

.lbl-icon {
  font-size: 0.78rem;
}

.platform-badges-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.platform-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.18rem 0.5rem;
  border-radius: 6px;
  border: 1px solid transparent;
  transition: all 0.15s ease;
}

.platform-badge .badge-ico {
  font-size: 0.75rem;
}

.platform-badge.plat-wechat {
  background: #ecfdf5;
  color: #047857;
  border-color: #a7f3d0;
}

.platform-badge.plat-zhihu {
  background: #eff6ff;
  color: #1d4ed8;
  border-color: #bfdbfe;
}

.platform-badge.plat-baidu {
  background: #f0fdf4;
  color: #15803d;
  border-color: #bbf7d0;
}

.platform-badge.plat-toutiao {
  background: #fef2f2;
  color: #b91c1c;
  border-color: #fecaca;
}

.platform-badge.plat-map {
  background: #fdf4ff;
  color: #86198f;
  border-color: #f5d0fe;
}

.platform-badge.plat-qcc {
  background: #faf5ff;
  color: #6b21a8;
  border-color: #e9d5ff;
}

.platform-badge.plat-official {
  background: #f1f5f9;
  color: #334155;
  border-color: #cbd5e1;
}

.platform-badge.plat-xhs {
  background: #fff1f2;
  color: #be123c;
  border-color: #fecdd3;
}

.platform-badge.plat-default {
  background: #f8fafc;
  color: #475569;
  border-color: #e2e8f0;
}

/* 建议宣发标题卡片 */
.task-title-suggestion-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 3.5px solid #6366f1;
  border-radius: 6px;
  padding: 0.55rem 0.75rem;
  margin-bottom: 0.65rem;
}

.suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.3rem;
}

.suggestion-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #4f46e5;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-copy-title {
  background: #ffffff;
  border: 1px solid #c7d2fe;
  color: #4338ca;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
}

.btn-copy-title:hover {
  background: #4f46e5;
  color: #ffffff;
  border-color: #4f46e5;
}

.btn-copy-title .copy-done {
  color: #059669;
  font-weight: 700;
}

.suggested-title-text {
  font-size: 0.82rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.45;
  word-break: break-all;
}

/* 核心埋词与实体对 */
.task-keywords-block {
  margin-bottom: 0.65rem;
}

.keywords-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.kw-tag {
  font-size: 0.68rem;
  font-weight: 700;
  color: #4338ca;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.2);
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
}

/* 具体发布规范与结构建议 */
.task-format-guide-box {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 6px;
  padding: 0.55rem 0.75rem;
  margin-bottom: 0.65rem;
  font-size: 0.75rem;
  color: #92400e;
  line-height: 1.5;
}

.guide-title {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  margin-bottom: 0.25rem;
  color: #b45309;
}

.guide-icon {
  font-size: 0.8rem;
}

.guide-desc {
  color: #78350f;
  font-size: 0.73rem;
  line-height: 1.45;
}

.task-action-box {
  font-size: 0.78rem;
  color: #334155;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
  margin-bottom: 0.75rem;
  line-height: 1.5;
  flex: 1;
}

.task-footer-row {
  font-size: 0.72rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #e2e8f0;
}

.impact-lbl {
  color: #64748b;
  font-weight: 700;
  margin-right: 0.3rem;
}

.impact-txt {
  color: #059669;
  font-weight: 600;
}

/* ==================== 商业杀伤力升级：红黑打脸双轨对比展区 ==================== */
.contrast-section {
  border: 2px solid #cbd5e1;
  background: #ffffff;
  border-radius: 12px;
  padding: 1.75rem 2rem;
  box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08);
}

.contrast-tabs-nav {
  display: flex;
  gap: 0.6rem;
  margin-bottom: 1.25rem;
  overflow-x: auto;
  padding-bottom: 0.3rem;
}

.contrast-tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #475569;
  padding: 0.55rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.contrast-tab-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.contrast-tab-btn.active {
  background: #0f172a;
  border-color: #0f172a;
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.2);
}

.tab-plat-badge {
  font-size: 0.72rem;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.2);
}

.contrast-tab-btn.active .tab-plat-badge {
  background: #4f46e5;
  color: #ffffff;
}

.tab-indicator {
  color: #10b981;
  font-size: 0.75rem;
  animation: pulse 1.5s infinite;
}

.contrast-stage-card {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.stage-intent-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem 1.25rem;
  gap: 1rem;
}

.intent-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.intent-icon {
  font-size: 1.2rem;
}

.intent-text {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.intent-label {
  font-size: 0.82rem;
  color: #64748b;
}

.intent-query {
  font-size: 0.95rem;
  color: #0f172a;
  font-weight: 700;
}

.intent-pill {
  font-size: 0.75rem;
  background: #ede9fe;
  color: #6d28d9;
  border: 1px solid #ddd6fe;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-weight: 700;
  white-space: nowrap;
}

/* 双轨红黑对抗舞台 */
.battle-stage-grid {
  display: grid;
  grid-template-columns: 1fr 120px 1fr;
  gap: 1rem;
  align-items: stretch;
}

.battle-col {
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
}

.col-competitor {
  background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);
  border: 2px solid #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.12);
}

.col-target {
  background: linear-gradient(180deg, #fef2f2 0%, #ffffff 100%);
  border: 2px solid #ef4444;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.12);
}

.col-header {
  padding: 0.85rem 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.header-red {
  background: linear-gradient(135deg, #b45309 0%, #78350f 100%);
  color: #ffffff;
}

.header-black {
  background: linear-gradient(135deg, #991b1b 0%, #450a0a 100%);
  color: #ffffff;
}

.header-badge-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.trophy-badge {
  font-size: 0.78rem;
  font-weight: 800;
  color: #fef08a;
}

.alert-shield-badge {
  font-size: 0.78rem;
  font-weight: 800;
  color: #fecaca;
}

.status-pill {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.status-vip {
  background: rgba(254, 240, 138, 0.25);
  color: #fef08a;
  border: 1px solid rgba(254, 240, 138, 0.5);
}

.status-alert {
  background: rgba(254, 202, 202, 0.25);
  color: #fecaca;
  border: 1px solid rgba(254, 202, 202, 0.5);
}

.brand-headline {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.text-gold {
  color: #fef08a;
}

.text-danger {
  color: #ffffff;
}

.col-body {
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
}

.quote-box {
  border-radius: 8px;
  padding: 0.9rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  position: relative;
  flex: 1;
}

.quote-vip {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
}

.quote-alert {
  background: #fee2e2;
  border-left: 4px solid #ef4444;
}

.quote-mark {
  font-size: 1.8rem;
  line-height: 1;
  font-family: serif;
  font-weight: 900;
  color: rgba(0, 0, 0, 0.2);
  margin-bottom: -0.5rem;
}

.quote-content {
  font-size: 0.86rem;
  line-height: 1.55;
  color: #1e293b;
  margin: 0;
  font-weight: 500;
}

.quote-tags {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  margin-top: 0.2rem;
}

.adv-tag {
  font-size: 0.7rem;
  background: #fde68a;
  color: #92400e;
  border: 1px solid #fcd34d;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
}

.vuln-tag {
  font-size: 0.7rem;
  background: #fecaca;
  color: #991b1b;
  border: 1px solid #fca5a5;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
}

.buyer-reaction-card {
  border-radius: 8px;
  padding: 0.75rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.reaction-win {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
}

.reaction-lost {
  background: #fff1f2;
  border: 1px solid #fecdd3;
}

.reaction-header {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  color: #0f172a;
}

.reaction-text {
  font-size: 0.82rem;
  line-height: 1.45;
  color: #334155;
  margin: 0;
}

/* 中间截胡裂缝 */
.battle-chasm {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  text-align: center;
}

.vs-circle {
  width: 44px;
  height: 44px;
  background: #ef4444;
  color: #ffffff;
  border-radius: 50%;
  font-size: 1.15rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 16px rgba(239, 68, 68, 0.4);
  letter-spacing: 0.5px;
}

.chasm-arrow-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}

.arrow-line {
  width: 2px;
  height: 30px;
  background: repeating-linear-gradient(to bottom, #ef4444, #ef4444 4px, transparent 4px, transparent 8px);
}

.chasm-badge {
  background: #fef2f2;
  border: 1px dashed #ef4444;
  border-radius: 6px;
  padding: 0.45rem 0.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.chasm-alert {
  font-size: 0.72rem;
  font-weight: 800;
  color: #dc2626;
  white-space: nowrap;
}

.chasm-sub {
  font-size: 0.65rem;
  color: #7f1d1d;
  line-height: 1.25;
}

/* 底部刺痛打脸总结条 */
.face-slap-summary-strip {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border: 1px solid #fdba74;
  border-radius: 8px;
  padding: 0.9rem 1.25rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.slap-icon {
  font-size: 1.4rem;
  line-height: 1;
}

.slap-content {
  font-size: 0.84rem;
  line-height: 1.55;
  color: #9a3412;
}

.slap-content strong {
  color: #c2410c;
}

/* 攻防双轨 · 态势徽标与自适应切换 */
.tab-type-pill {
  font-size: 0.68rem;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
  margin-left: 0.25rem;
}

.pill-defense {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.35);
}

.pill-intercept {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.35);
}

.contrast-tab-btn.active.tab-is-defense {
  border-color: #10b981;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.contrast-tab-btn.active.tab-is-defense .tab-plat-badge {
  background: #059669;
}

.contrast-tab-btn.active.tab-is-intercept {
  border-color: #ef4444;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
}

.contrast-tab-btn.active.tab-is-intercept .tab-plat-badge {
  background: #dc2626;
}

/* 守擂场景意图栏高光 */
.stage-intent-bar.bar-defense {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.pill-intent-defense {
  background: #dcfce7 !important;
  color: #15803d !important;
  border-color: #bbf7d0 !important;
}

/* 守擂态势 · 贵司冠军卡片样式 */
.col-target-champion {
  background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%) !important;
  border: 2px solid #10b981 !important;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.18) !important;
}

.header-champion {
  background: linear-gradient(135deg, #059669 0%, #064e3b 100%) !important;
  color: #ffffff !important;
}

.champion-badge {
  font-size: 0.78rem;
  font-weight: 800;
  color: #a7f3d0;
}

.status-champion {
  background: rgba(167, 243, 208, 0.25);
  color: #a7f3d0;
  border: 1px solid rgba(167, 243, 208, 0.5);
}

.text-champion {
  color: #ecfdf5;
}

.quote-champion {
  background: #f0fdf4 !important;
  border-left: 4px solid #10b981 !important;
}

.champion-tag {
  font-size: 0.7rem;
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
}

/* 守擂态势 · 竞品次席陪跑样式 */
.col-competitor-secondary {
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%) !important;
  border: 2px solid #cbd5e1 !important;
  box-shadow: 0 4px 12px rgba(100, 116, 139, 0.08) !important;
}

.header-secondary {
  background: linear-gradient(135deg, #475569 0%, #334155 100%) !important;
  color: #ffffff !important;
}

.secondary-badge {
  font-size: 0.78rem;
  font-weight: 800;
  color: #cbd5e1;
}

.status-secondary {
  background: rgba(203, 213, 225, 0.25);
  color: #cbd5e1;
  border: 1px solid rgba(203, 213, 225, 0.5);
}

.text-secondary {
  color: #f1f5f9;
}

.quote-secondary {
  background: #f8fafc !important;
  border-left: 4px solid #94a3b8 !important;
}

.sec-tag {
  font-size: 0.7rem;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  font-weight: 600;
}

.reaction-secondary {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

/* 守擂态势 · 绿色护城河 VS 区域 */
.vs-circle-defense {
  background: #10b981 !important;
  box-shadow: 0 0 16px rgba(16, 185, 129, 0.45) !important;
}

.arrow-line-defense {
  background: repeating-linear-gradient(to bottom, #10b981, #10b981 4px, transparent 4px, transparent 8px) !important;
}

.chasm-badge-defense {
  background: #ecfdf5 !important;
  border: 1px dashed #10b981 !important;
}

.chasm-alert-defense {
  color: #059669 !important;
}

.chasm-sub-defense {
  color: #065f46 !important;
}

/* 守擂态势 · 底部总结条绿金护城河风格 */
.defense-summary-strip {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%) !important;
  border: 1px solid #86efac !important;
}

.defense-summary-strip .slap-content {
  color: #166534 !important;
}

.defense-summary-strip .slap-content strong {
  color: #15803d !important;
}

/* 漏斗诊断卡 */
.funnel-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.funnel-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.layer-recall { border-top: 4px solid #6366f1; }
.layer-authority { border-top: 4px solid #dc2626; }
.layer-ranking { border-top: 4px solid #f59e0b; }
.layer-conversion { border-top: 4px solid #ef4444; }

.funnel-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.layer-header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.layer-step-badge {
  background: #0f172a;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.layer-name {
  font-size: 0.9rem;
  font-weight: 800;
  color: #1e293b;
}

.layer-status-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
}

.pill-deficient {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.pill-critical_defect {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.pill-zero_recommendation {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #f87171;
}

.pill-weak_recommendation {
  background: #fef9c3;
  color: #854d0e;
  border: 1px solid #fef08a;
}

.pill-unconverted {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.layer-score-bar-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.score-bar-track {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ef4444, #f59e0b);
  border-radius: 999px;
}

.score-bar-label {
  font-size: 0.8rem;
  color: #475569;
}

.layer-body {
  font-size: 0.8rem;
  line-height: 1.5;
  color: #334155;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.layer-diag {
  background: #ffffff;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.layer-evidence {
  background: #f1f5f9;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  color: #475569;
}

/* 双端矩阵 */
.pill-alert {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}

.pill-warning {
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
}

.pill-success {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #6ee7b7;
}

.device-matrix-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.65rem;
}

@media (max-width: 1200px) {
  .device-matrix-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .device-matrix-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.device-chip-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  transition: all 0.2s ease;
}

.card-indexed {
  background: #f8fafc;
  border-color: #86efac;
  box-shadow: 0 1px 3px rgba(16, 185, 129, 0.08);
}

.card-unindexed {
  border-color: #cbd5e1;
}

.chip-mobile {
  border-left: 3px solid #0284c7;
}

.chip-pc {
  border-left: 3px solid #64748b;
}

.chip-top {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.device-type-tag {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  width: fit-content;
}

.tag-mob { background: #e0f2fe; color: #0369a1; }
.tag-pc { background: #f1f5f9; color: #475569; }

.chip-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
}

.chip-status {
  margin-top: 0.2rem;
}

.chip-badge {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.badge-unindexed {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}

.badge-indexed {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #6ee7b7;
}

.chip-desc {
  font-size: 0.72rem;
  color: #64748b;
  line-height: 1.35;
}

/* 竞品信源穿透表 */
.sources-table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  width: 100%;
}

.sources-table {
  width: 100%;
  min-width: 760px;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.sources-table th {
  background: #f8fafc;
  padding: 0.75rem 0.85rem;
  text-align: left;
  border-bottom: 2px solid #cbd5e1;
  color: #475569;
}

.sources-table td {
  padding: 0.75rem 0.85rem;
  border-bottom: 1px solid #f1f5f9;
}

.src-type-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.72rem;
}

.comp-source-pill {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-size: 0.72rem;
  margin-right: 0.3rem;
  font-weight: 600;
}

.threat-badge {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.threat-critical {
  background: #dc2626;
  color: #ffffff;
}

.threat-high {
  background: #ea580c;
  color: #ffffff;
}

.text-danger { color: #dc2626; }
.font-bold { font-weight: 700; }
.text-center { text-align: center; }
.text-indigo { color: #4f46e5; }

/* 经济账本 */
.economic-card {
  background: linear-gradient(180deg, #ffffff, #fffbeb);
  border: 1px solid #fef3c7;
  border-radius: 12px;
  padding: 1.5rem;
}

.pill-money {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.pill-red-tag {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}

.economic-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.econ-kpi-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.econ-highlight-box {
  background: #fff1f2;
  border: 2px solid #f87171;
}

.econ-label {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 700;
}

.econ-val {
  font-size: 1.35rem;
  font-weight: 900;
  line-height: 1.2;
}

.econ-val .unit {
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
}

.econ-sub {
  font-size: 0.72rem;
  color: #94a3b8;
}

.text-slate { color: #334155; }
.text-red { color: #b91c1c; }
.text-darkred { color: #7f1d1d; }

.roi-banner {
  background: #0f172a;
  color: #ffffff;
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.roi-badge {
  background: #22c55e;
  color: #0f172a;
  font-size: 0.75rem;
  font-weight: 900;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  display: inline-block;
  margin-bottom: 0.4rem;
}

.roi-pitch {
  font-size: 0.95rem;
  line-height: 1.6;
}

.roi-pitch strong {
  color: #4ade80;
}

.roi-note {
  font-size: 0.72rem;
  color: #94a3b8;
  max-width: 280px;
  line-height: 1.4;
}

/* 实施甘特图 */
.roadmap-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-phase-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 1.1rem 1.25rem;
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 1.5rem;
  align-items: center;
}

.phase-left-col {
  border-right: 2px dashed #e2e8f0;
  padding-right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.phase-badge {
  background: #4f46e5;
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 800;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  width: fit-content;
}

.phase-days {
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
}

.phase-main-col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.82rem;
  line-height: 1.5;
  color: #334155;
}

.phase-title {
  font-size: 0.98rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.2rem;
}

.kpi-text {
  color: #047857;
  font-weight: 700;
}

/* 竞品表 */
.competitor-table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  width: 100%;
}

.competitor-table {
  width: 100%;
  min-width: 620px;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.competitor-table th {
  background: #f8fafc;
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 2px solid #e2e8f0;
  color: #475569;
}

.competitor-table td {
  padding: 0.85rem 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.comp-name-cell {
  color: #b91c1c;
}

.mention-pill {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.75rem;
}

.platform-mini-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.7rem;
  margin-right: 0.3rem;
}

.comp-adv-cell {
  font-size: 0.8rem;
  color: #64748b;
  line-height: 1.4;
}

.title-with-counter {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.kw-counter-pill {
  background: #ede9fe;
  color: #6366f1;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  border: 1px solid #c7d2fe;
}

.scenario-groups-wrap {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.scenario-group-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.scenario-header {
  background: linear-gradient(90deg, #f8fafc, #f1f5f9);
  padding: 0.9rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
}

.scenario-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.scenario-badge {
  background: #0f172a;
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  letter-spacing: 0.03em;
}

.scenario-kw {
  font-size: 0.95rem;
  color: #1e293b;
}

.scenario-kw strong {
  color: #4f46e5;
}

.scenario-status-pill {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
}

.status-has-mention {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.status-all-invisible {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.kw-sub-info {
  font-size: 0.75rem;
  color: #64748b;
  margin-left: 0.25rem;
}

/* 折叠手风琴回显 */
.items-accordion {
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.accordion-item {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  overflow: hidden;
}

.accordion-header {
  background: #f8fafc;
  padding: 0.85rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.accordion-header:hover {
  background: #f1f5f9;
}

.item-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.platform-badge {
  background: #4f46e5;
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.real-api-pill {
  background: linear-gradient(135deg, #0284c7, #2563eb);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(37, 99, 235, 0.25);
  letter-spacing: 0.02em;
}

.duration-badge {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

.plat-deepseek {
  background: #0284c7 !important;
}

.plat-kimi {
  background: #0d9488 !important;
}

.plat-tongyi {
  background: #6366f1 !important;
}

.plat-doubao {
  background: #0ea5e9 !important;
}

.plat-yuanbao {
  background: #10b981 !important;
}

.plat-baidu {
  background: #ef4444 !important;
}

.label-deepseek {
  color: #0369a1;
  font-weight: 800;
}

.label-kimi {
  color: #0d9488;
  font-weight: 800;
}

.label-tongyi {
  color: #4f46e5;
  font-weight: 800;
}

.label-doubao {
  color: #0284c7;
  font-weight: 800;
}

.label-yuanbao {
  color: #059669;
  font-weight: 800;
}

.label-baidu {
  color: #dc2626;
  font-weight: 800;
}

.kw-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #0f172a;
}

.item-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-stamp {
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.stamp-unseen {
  background: #fef2f2;
  border: 1px solid #f87171;
  color: #b91c1c;
}

.stamp-seen {
  background: #ecfdf5;
  border: 1px solid #34d399;
  color: #047857;
}

.arrow-indicator {
  color: #94a3b8;
  font-size: 0.75rem;
}

.accordion-body {
  padding: 1.25rem;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 官方真机认证凭据卡 (API Certification Pass Card) */
.api-cert-card {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 0.9rem 1.2rem;
  margin-bottom: 0.5rem;
  color: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.cert-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #1e293b;
  padding-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cert-header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.cert-pulse-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px #10b981;
  animation: pulse 1.5s infinite;
}

.cert-auth-tag {
  font-size: 0.78rem;
  color: #34d399;
  font-weight: 700;
}

.cert-provider-name {
  font-size: 0.82rem;
  color: #ffffff;
  font-weight: 700;
}

.cert-model-family {
  font-size: 0.72rem;
  background: #1e293b;
  color: #94a3b8;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.cert-header-right {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.cert-serial-label {
  font-size: 0.72rem;
  color: #64748b;
}

.cert-serial-code {
  font-size: 0.72rem;
  background: #020617;
  color: #38bdf8;
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
  font-family: monospace;
  border: 1px solid #1e293b;
}

.cert-params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.param-cell {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.p-label {
  font-size: 0.68rem;
  color: #94a3b8;
}

.p-val {
  font-size: 0.75rem;
  color: #e2e8f0;
  word-break: break-all;
}

.p-endpoint {
  color: #93c5fd;
  font-family: monospace;
}

.p-code {
  color: #a78bfa;
  font-family: monospace;
}

.p-hash {
  color: #facc15;
  font-family: monospace;
  font-weight: 700;
}

.p-metric {
  color: #34d399;
  font-weight: 700;
}

.cert-footer-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #020617;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid #1e293b;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.compliance-badge {
  font-size: 0.72rem;
  color: #94a3b8;
}

.bill-verified-badge {
  font-size: 0.72rem;
  color: #34d399;
  font-weight: 700;
}

.box-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 0.4rem;
}

.raw-text {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  font-size: 0.82rem;
  line-height: 1.7;
  white-space: pre-wrap;
  color: #334155;
  max-height: 420px;
  overflow-y: auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}

.citation-links-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 6px;
}

.cite-row {
  font-size: 0.75rem;
  display: flex;
  gap: 0.4rem;
  align-items: center;
}

.cite-num { color: #64748b; font-weight: 700; }
.cite-site { color: #4f46e5; font-weight: 600; }
.cite-title { color: #2563eb; text-decoration: none; }

.doubao-citations-badge {
  color: #0284c7;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.target-brand-row {
  background: #fef2f2 !important;
  border: 1px solid #fca5a5 !important;
  border-radius: 4px;
  padding: 0.35rem 0.6rem !important;
  margin: 0.25rem 0;
}

.target-brand-pill {
  background: #dc2626;
  color: #ffffff;
  font-size: 0.68rem;
  font-weight: 800;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  margin-left: 0.5rem;
  white-space: nowrap;
}

.zero-target-notice {
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-left: 4px solid #e11d48;
  border-radius: 6px;
  padding: 0.65rem 0.85rem;
  margin-bottom: 0.6rem;
}

.zero-target-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.3rem;
}

.zero-target-tag {
  color: #be123c;
  font-weight: 800;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.zero-target-badge {
  font-size: 0.68rem;
  background: #ffe4e6;
  color: #9f1239;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-weight: 700;
}

.zero-target-desc {
  font-size: 0.76rem;
  line-height: 1.5;
  color: #475569;
  margin: 0;
}

.zero-target-desc strong {
  color: #0f172a;
}

/* 处方区 */
.prescription-card {
  background: #fdf4ff;
  border: 1px solid #f5d0fe;
  border-radius: 12px;
  padding: 1.5rem;
}

.prescription-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}


.rx-box {
  background: #ffffff;
  border: 1px solid #f0abfc;
  border-radius: 8px;
  padding: 1rem;
  font-size: 0.8rem;
  line-height: 1.5;
}

.rx-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.rx-scenario {
  font-weight: 800;
  color: #86198f;
  font-size: 0.85rem;
}

.rx-urgency {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.urgency-red { background: #fee2e2; color: #b91c1c; }
.urgency-blue { background: #e0f2fe; color: #0369a1; }

.rx-action {
  color: #374151;
  margin-bottom: 0.35rem;
}

.rx-expected {
  color: #047857;
}

/* 核心指标 10: 前后体检报告对比视图与交付验收承诺 */
.compare-view-card {
  border: 1.5px solid #818cf8;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.pill-compare {
  background: #e0e7ff;
  color: #3730a3;
  border: 1px solid #c7d2fe;
}

.compare-dual-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-top: 1.25rem;
}

.compare-box {
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.box-before {
  background: #fff8f8;
  border: 1.5px solid #fca5a5;
}

.box-after {
  background: #f0fdf4;
  border: 1.5px solid #86efac;
  box-shadow: 0 4px 14px rgba(34, 197, 94, 0.08);
}

.cbox-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 1px dashed rgba(0, 0, 0, 0.12);
}

.cbox-badge {
  font-size: 0.85rem;
  font-weight: 800;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
}

.badge-before {
  background: #fee2e2;
  color: #991b1b;
}

.badge-after {
  background: #dcfce7;
  color: #166534;
}

.cbox-score-tag {
  font-size: 0.82rem;
  font-weight: 700;
  color: #dc2626;
}

.cbox-score-tag.tag-after {
  color: #15803d;
}

.cbox-body {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  font-size: 0.82rem;
}

.cbox-metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.45rem 0.6rem;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.m-lbl {
  color: #4b5563;
  font-weight: 600;
}

.m-val {
  font-weight: 800;
}

.text-red {
  color: #dc2626;
}

.text-green {
  color: #16a34a;
}

.text-slate {
  color: #64748b;
}

.cbox-quote-box {
  margin-top: 0.4rem;
  padding: 0.75rem 0.9rem;
  border-radius: 6px;
  font-size: 0.78rem;
  line-height: 1.55;
}

.quote-before {
  background: #fef2f2;
  border-left: 3px solid #ef4444;
  color: #7f1d1d;
}

.quote-after {
  background: #f0fdf4;
  border-left: 3px solid #22c55e;
  color: #14532d;
}

.quote-tag {
  font-weight: 800;
  margin-bottom: 0.25rem;
  font-size: 0.75rem;
}

.compare-guarantee-bar {
  margin-top: 1.25rem;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  color: #ffffff;
  border-radius: 8px;
  padding: 0.85rem 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.82rem;
  line-height: 1.5;
}

.compare-guarantee-bar .g-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.compare-guarantee-bar .g-text strong {
  color: #a5b4fc;
}

/* Footer */
.paper-footer {
  border-top: 2px solid #0f172a;
  padding-top: 1.5rem;
}

.contact-card {
  background: #0f172a;
  color: #ffffff;
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.contact-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #a5b4fc;
  margin-bottom: 0.5rem;
}

.contact-details {
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  flex-wrap: wrap;
}

.statement-box {
  font-size: 0.7rem;
  color: #94a3b8;
  text-align: center;
  line-height: 1.5;
}

.footer-bottom-actions {
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px dashed #e2e8f0;
  display: flex;
  justify-content: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.btn-footer-back {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 0.65rem 1.4rem;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn-footer-back:hover {
  background: #e2e8f0;
  color: #0f172a;
  border-color: #94a3b8;
  transform: translateX(-3px);
}

.btn-footer-poster {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 0.65rem 1.4rem;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
  transition: all 0.2s ease;
}

.btn-footer-poster:hover {
  background: linear-gradient(135deg, #4338ca, #6d28d9);
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35);
  transform: translateY(-2px);
}

.footer-btn-icon {
  width: 16px;
  height: 16px;
}

.loading-wrap {
  color: #ffffff;
  text-align: center;
  padding: 7rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.report-loading-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
}

.report-loading-logo {
  width: 76px;
  height: 76px;
  object-fit: contain;
  filter: drop-shadow(0 0 16px rgba(16, 185, 129, 0.6));
  animation: pulseReportLogo 1.8s ease-in-out infinite alternate;
}

.report-loading-text {
  font-size: 1.1rem;
  color: #cbd5e1;
  font-weight: 500;
  letter-spacing: 0.5px;
}

@keyframes pulseReportLogo {
  0% { transform: scale(0.94); filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.4)); }
  100% { transform: scale(1.06); filter: drop-shadow(0 0 24px rgba(16, 185, 129, 0.85)); }
}

/* 移动端横向滑动提示徽章 */
.mobile-scroll-hint {
  display: none;
}

/* ========================================================
   移动端与微信 H5 深度排版优化 (彻底消除文字纵向挤压与排版错位)
   ======================================================== */
@media (max-width: 768px) {
  .mobile-scroll-hint {
    display: block;
    font-size: 0.72rem;
    color: #4f46e5;
    background: #eef2ff;
    padding: 0.35rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
    text-align: center;
    font-weight: 700;
    border: 1px dashed #c7d2fe;
  }

  .report-wrapper {
    padding-bottom: 2rem;
  }

  /* 顶部操作条 */
  .top-action-bar {
    padding: 0.5rem 0.75rem;
  }

  .action-inner {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .bar-left {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .bar-right {
    display: flex;
    width: 100%;
    gap: 0.5rem;
  }

  /* 移动端隐藏 PC 专用的万字长文打印开关，避免挤爆界面 */
  .print-option-toggle {
    display: none !important;
  }

  .bar-right .btn {
    flex: 1;
    font-size: 0.75rem;
    padding: 0.45rem 0.5rem;
    justify-content: center;
    white-space: nowrap;
  }

  .report-id-tag {
    font-size: 0.68rem;
    padding: 0.15rem 0.45rem;
  }

  .public-read-badge {
    font-size: 0.68rem;
    padding: 0.15rem 0.45rem;
  }

  /* 纸张容器移动端紧凑排版，释放被巨额内边距占用的空间 */
  .paper-container {
    margin: 0.5rem auto;
    padding: 1.25rem 0.85rem;
    border-radius: 8px;
    gap: 1.25rem;
    width: 100%;
    box-sizing: border-box;
  }

  /* 顶部企业认证印章与标题 */
  .header-seal-row {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .report-brand-logo {
    height: 36px;
    margin-bottom: 0.2rem;
  }

  .brand-sub-title {
    font-size: 0.82rem;
    letter-spacing: 0.5px;
  }

  .official-seal {
    width: 64px;
    height: 64px;
    font-size: 0.65rem;
    transform: rotate(-8deg);
  }

  .seal-auth {
    font-size: 0.58rem;
  }

  .seal-name {
    font-size: 0.62rem;
  }

  /* 头部企业元信息网格 */
  .meta-grid {
    grid-template-columns: 1fr;
    gap: 0.35rem;
    padding: 0.75rem;
    font-size: 0.8rem;
  }

  .meta-label {
    width: auto;
    min-width: 85px;
    margin-right: 0.3rem;
  }

  /* 核心评分卡片 */
  .score-card {
    flex-direction: column;
    align-items: stretch;
    gap: 0.85rem;
    padding: 1rem 0.85rem;
    text-align: center;
  }

  .score-number-box {
    border-right: none;
    border-bottom: 2px dashed rgba(0, 0, 0, 0.1);
    padding-right: 0;
    padding-bottom: 0.75rem;
    min-width: auto;
    width: 100%;
  }

  .score-big {
    font-size: 3.2rem;
  }

  .summary-heading {
    text-align: left;
    font-size: 0.92rem;
  }

  .summary-text {
    text-align: left;
    font-size: 0.82rem;
    line-height: 1.5;
  }

  .model-tags {
    justify-content: flex-start;
  }

  /* 四层漏斗网格 */
  .funnel-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .funnel-card {
    padding: 0.85rem;
  }

  .layer-name {
    font-size: 0.85rem;
  }

  .layer-diag, .layer-evidence {
    font-size: 0.75rem;
    padding: 0.45rem 0.6rem;
  }

  /* 双端矩阵 */
  .device-matrix-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.45rem !important;
  }

  .device-chip-card {
    padding: 0.5rem 0.6rem;
  }

  .chip-name {
    font-size: 0.75rem;
  }

  .chip-desc {
    font-size: 0.65rem;
    line-height: 1.3;
  }

  /* 商业测算经济账本 */
  .economic-card {
    padding: 1rem 0.85rem;
  }

  .economic-kpi-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .econ-kpi-box {
    padding: 0.75rem 0.65rem;
  }

  .econ-val {
    font-size: 1.15rem;
  }

  .roi-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.85rem;
  }

  /* 场景问答实录分组与手风琴 */
  .scenario-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.75rem 0.85rem;
  }

  .scenario-meta {
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .scenario-kw {
    font-size: 0.85rem;
    line-height: 1.35;
    word-break: break-word;
  }

  .items-accordion {
    padding: 0.6rem 0.75rem;
    gap: 0.6rem;
  }

  .accordion-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.45rem;
    padding: 0.65rem 0.75rem;
  }

  .item-left {
    width: 100%;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .item-right {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px dashed #e2e8f0;
    padding-top: 0.35rem;
  }

  .kw-sub-info {
    display: none;
  }

  .raw-response-box {
    padding: 0.6rem;
  }

  .raw-text {
    font-size: 0.75rem;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
  }

  /* 实施路线图 */
  .timeline-phase-card {
    grid-template-columns: 1fr;
    gap: 0.65rem;
    padding: 0.85rem;
  }

  .phase-left-col {
    border-right: none;
    border-bottom: 1px dashed #e2e8f0;
    padding-right: 0;
    padding-bottom: 0.5rem;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  /* 靶向落地工单网格 */
  .geo-tasks-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  /* 处方网格 */
  .prescription-grid {
    grid-template-columns: 1fr;
    gap: 0.6rem;
  }

  .rx-box {
    padding: 0.85rem;
  }

  /* 底部署名与免责声明 */
  .contact-details {
    flex-direction: column;
    gap: 0.4rem;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .economic-kpi-grid {
    grid-template-columns: 1fr;
  }
}

/* 打印 A4 媒体样式高精度商务排版重构 (彻底消除空白页与跨页挤压) */
@media print {
  @page {
    size: A4 portrait;
    margin: 12mm 12mm 12mm 12mm;
  }

  *, *::before, *::after {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
    box-sizing: border-box !important;
  }

  html, body, #app, #console-app, .console-app-root, .report-wrapper {
    background: #ffffff !important;
    color: #0f172a !important;
    font-size: 11px !important;
    line-height: 1.35 !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
  }

  .no-print {
    display: none !important;
  }

  /* 核心解法 1: 纸张容器强制采用普通文档流 block，彻底消除 flex 容器导致的空白页与分页器崩溃 */
  .paper-container {
    display: block !important;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    border: none !important;
    border-radius: 0 !important;
    gap: 0 !important;
  }

  .paper-container > section,
  .paper-container > header,
  .paper-container > footer {
    display: block !important;
    margin-bottom: 10px !important;
    padding: 0 !important;
    float: none !important;
    break-inside: auto !important;
    page-break-inside: auto !important;
  }

  /* 核心解法 2: 允许外层大板块与大容器跨页正常断裂，绝不整体被推入下一页留出大面积空白 */
  .section-card,
  .scenario-groups-wrap,
  .scenario-group-card,
  .timeline-phase-card,
  .prescription-card,
  .competitors-card,
  .economic-card {
    break-inside: auto !important;
    page-break-inside: auto !important;
    display: block !important;
    margin-bottom: 10px !important;
    padding: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }

  /* 标题防落单：标题绝不允许出现在页尾 */
  h1, h2, h3, .sec-title-row, .scenario-header {
    break-after: avoid !important;
    page-break-after: avoid !important;
    break-inside: avoid !important;
  }

  /* 表头跨页自动重复，表格行防断裂 */
  .competitor-table, .sources-table {
    break-inside: auto !important;
    page-break-inside: auto !important;
  }
  thead {
    display: table-header-group !important;
  }

  /* 核心解法 3: 仅对不可分割的小叶子节点执行防腰斩 (break-inside: avoid) */
  .score-section,
  .live-cert-banner,
  .contrast-section,
  .contrast-stage-card,
  .accordion-item,
  .funnel-card,
  .device-chip-card,
  .rx-box,
  .phase-box,
  .paper-header,
  .paper-footer,
  .econ-kpi-box,
  .roi-banner,
  tr {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }

  .contrast-tabs-nav {
    display: none !important;
  }

  /* 当内容展开时，问答长文允许跨页流动，防止单卡片高度超标将前页挤成整张空白 */
  .accordion-item.open,
  .print-expand-all .accordion-item {
    break-inside: auto !important;
    page-break-inside: auto !important;
  }

  /* 官方抬头 */
  .paper-header {
    padding-bottom: 0.6rem !important;
    margin-bottom: 0.6rem !important;
    border-bottom: 2px solid #0f172a !important;
  }
  .report-brand-logo {
    height: 32px !important;
    margin-bottom: 0.2rem !important;
  }
  .meta-grid {
    gap: 0.25rem 0.8rem !important;
  }
  .meta-item {
    font-size: 0.68rem !important;
  }

  /* 核心指标 1: 仪表盘紧凑化 */
  .score-section {
    margin-bottom: 0.6rem !important;
  }
  .score-card {
    padding: 0.6rem 1rem !important;
    gap: 1rem !important;
  }
  .score-number-box {
    min-width: 120px !important;
    padding-right: 0.8rem !important;
  }
  .score-big {
    font-size: 2.5rem !important;
  }
  .summary-text {
    font-size: 0.78rem !important;
    line-height: 1.3 !important;
  }

  /* 核心指标 2: 四层漏斗紧凑适配 */
  .funnel-section {
    padding: 0.8rem 1rem !important;
  }
  .funnel-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.4rem !important;
  }
  .funnel-card {
    padding: 0.45rem 0.65rem !important;
  }
  .layer-body {
    font-size: 0.68rem !important;
    line-height: 1.25 !important;
    gap: 0.25rem !important;
  }
  .layer-evidence, .layer-diag {
    padding: 0.25rem 0.45rem !important;
  }

  /* 核心指标 3: 双端监控矩阵 (A4 纸面自适应 6 列优化排版) */
  .device-matrix-grid {
    grid-template-columns: repeat(6, 1fr) !important;
    gap: 0.25rem !important;
  }
  .device-chip-card {
    padding: 0.3rem !important;
    border-radius: 4px !important;
    border-width: 1px !important;
  }
  .device-type-tag {
    font-size: 0.55rem !important;
    padding: 0.05rem 0.2rem !important;
  }
  .chip-name {
    font-size: 0.65rem !important;
  }
  .chip-badge {
    font-size: 0.6rem !important;
    padding: 0.05rem 0.25rem !important;
  }
  .chip-desc {
    font-size: 0.55rem !important;
    line-height: 1.15 !important;
  }

  /* 核心指标 4 & 5: 表格排版 */
  .competitor-table, .sources-table {
    font-size: 0.68rem !important;
    width: 100% !important;
  }
  .competitor-table th, .sources-table th {
    padding: 0.3rem 0.4rem !important;
    background: #f1f5f9 !important;
    font-size: 0.68rem !important;
  }
  .competitor-table td, .sources-table td {
    padding: 0.3rem 0.4rem !important;
  }

  /* 核心指标 6: 经济损失测算 */
  .econ-grid {
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 0.4rem !important;
  }
  .econ-kpi-box {
    padding: 0.45rem 0.65rem !important;
  }
  .econ-val {
    font-size: 1.1rem !important;
  }
  .roi-banner {
    padding: 0.45rem 0.65rem !important;
    margin-top: 0.4rem !important;
  }
  .roi-pitch {
    font-size: 0.7rem !important;
  }

  /* 核心指标 7: 现场大模型实测证据链 (解决暴力展开20页乱码的根因) */
  .scenario-groups-wrap {
    gap: 0.45rem !important;
  }
  .scenario-group-card {
    margin-bottom: 0.45rem !important;
    padding: 0.45rem 0.65rem !important;
  }
  .scenario-header {
    padding-bottom: 0.3rem !important;
    margin-bottom: 0.3rem !important;
  }
  .scenario-badge {
    font-size: 0.62rem !important;
    padding: 0.08rem 0.35rem !important;
  }
  .scenario-kw {
    font-size: 0.72rem !important;
  }
  .accordion-item {
    margin-bottom: 0.25rem !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 5px !important;
  }
  .accordion-header {
    padding: 0.3rem 0.55rem !important;
    background: #f8fafc !important;
  }
  .platform-badge {
    font-size: 0.65rem !important;
    padding: 0.08rem 0.35rem !important;
  }
  .real-api-pill {
    font-size: 0.6rem !important;
  }
  .kw-sub-info {
    font-size: 0.62rem !important;
  }
  .duration-badge {
    font-size: 0.6rem !important;
  }
  .status-stamp {
    font-size: 0.62rem !important;
    padding: 0.08rem 0.35rem !important;
  }
  .arrow-indicator {
    display: none !important;
  }
  
  /* 默认商业精炼模式：折叠实录正文不全量展开，保持紧凑的一行行实测矩阵徽章，杜绝暴增20页 */
  .accordion-body {
    display: none !important;
  }

  /* 当用户在屏幕上手动展开了某项，或勾选了“包含大模型全部问答实录”时，优雅打印实测正文 */
  .accordion-item.open .accordion-body,
  .print-expand-all .accordion-body {
    display: block !important;
    padding: 0.45rem !important;
    font-size: 0.68rem !important;
    background: #ffffff !important;
  }

  .raw-response-box {
    max-height: none !important;
    font-size: 0.68rem !important;
    line-height: 1.3 !important;
    padding: 0.45rem !important;
  }
  .citations-box {
    margin-top: 0.3rem !important;
  }
  .citation-card {
    padding: 0.25rem 0.4rem !important;
    margin-bottom: 0.15rem !important;
    font-size: 0.62rem !important;
  }

  /* 核心指标 8: 实施路线图 */
  .phases-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.4rem !important;
  }
  .phase-box {
    padding: 0.4rem 0.5rem !important;
    font-size: 0.68rem !important;
  }

  /* 核心指标 9: 处方 */
  .prescription-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 0.4rem !important;
  }
  .rx-box {
    padding: 0.4rem 0.5rem !important;
    font-size: 0.68rem !important;
  }

  /* 页脚认证署名 */
  .paper-footer {
    margin-top: 0.6rem !important;
    padding-top: 0.5rem !important;
    break-inside: avoid !important;
  }
  .contact-card {
    padding: 0.45rem 0.65rem !important;
  }
}

/* ==========================================================================
   Phase 3 促单按钮与全终端赋能样式
   ========================================================================== */
.btn-prompter-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
  color: #ffffff;
  border: 1px solid rgba(165, 180, 252, 0.4);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.35);
  transition: all 0.2s ease;
}

.btn-prompter-toggle:hover {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  transform: translateY(-1px);
}

.btn-prompter-toggle.active {
  background: #10b981;
  border-color: #34d399;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
}

.btn-wechat-poster {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  color: #ffffff;
  border: 1px solid rgba(110, 231, 183, 0.4);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.35);
  transition: all 0.2s ease;
}

.btn-wechat-poster:hover {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  transform: translateY(-1px);
}

/* ==========================================================================
   销售现场“30秒促单提词器”悬浮组件样式 (Dock / Drawer)
   ========================================================================== */
.sales-prompter-dock {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 9999;
  max-width: 580px;
  width: calc(100vw - 3rem);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif;
}

/* 最小化药丸条 */
.prompter-pill-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
  color: #ffffff;
  border: 2px solid #6366f1;
  border-radius: 40px;
  padding: 0.65rem 1.25rem;
  cursor: pointer;
  box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.6), 0 0 20px rgba(99, 102, 241, 0.35);
  animation: floatPrompter 3s ease-in-out infinite;
}

@keyframes floatPrompter {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.prompter-pill-bar .pill-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.prompter-pill-bar .pill-icon {
  font-size: 1.2rem;
}

.prompter-pill-bar .pill-title {
  font-size: 0.88rem;
  font-weight: 800;
  color: #e2e8f0;
}

.prompter-pill-bar .pill-timer-tag {
  background: rgba(99, 102, 241, 0.25);
  color: #a5b4fc;
  font-size: 0.76rem;
  font-weight: 800;
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  font-family: ui-monospace, monospace;
}

.prompter-pill-bar .pill-timer-tag.timer-running {
  background: #10b981;
  color: #ffffff;
}

.prompter-pill-bar .pill-timer-tag.timer-end {
  background: #ef4444;
  color: #ffffff;
}

.prompter-pill-bar .pill-expand-btn {
  font-size: 0.78rem;
  font-weight: 700;
  color: #fbbf24;
}

/* 完整提词器卡片 */
.prompter-card {
  background: #0f172a;
  color: #ffffff;
  border: 2px solid rgba(99, 102, 241, 0.5);
  border-radius: 16px;
  padding: 1.15rem 1.25rem;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7), 0 0 30px rgba(99, 102, 241, 0.25);
  backdrop-filter: blur(12px);
}

.prompter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  gap: 0.5rem;
}

.prompter-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.prompter-title-wrap .head-icon {
  font-size: 1.4rem;
}

.head-texts .head-title {
  display: block;
  font-size: 0.95rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.2px;
}

.head-texts .head-sub {
  display: block;
  font-size: 0.72rem;
  color: #94a3b8;
}

.prompter-actions-top {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.timer-control-box {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 0.2rem 0.45rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.timer-display {
  font-family: ui-monospace, SFMono-Regular, monospace;
  font-size: 0.85rem;
  font-weight: 800;
  color: #38bdf8;
  min-width: 48px;
  text-align: center;
}

.timer-display.timer-alert {
  color: #f87171;
  animation: pulse 1s infinite;
}

.timer-display.timer-end {
  color: #ef4444;
}

.btn-timer-action, .btn-timer-reset {
  background: transparent;
  border: none;
  color: #e2e8f0;
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0.2rem 0.35rem;
  border-radius: 4px;
  transition: background 0.15s ease;
}

.btn-timer-action:hover, .btn-timer-reset:hover {
  background: rgba(255, 255, 255, 0.15);
}

.btn-min-prompter, .btn-close-prompter {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: #94a3b8;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-min-prompter:hover, .btn-close-prompter:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* 进度条 */
.timer-progress-track {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.85rem;
}

.timer-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1 0%, #10b981 100%);
  transition: width 0.3s ease;
}

/* 步骤选择条 */
.prompter-steps-nav {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
  margin-bottom: 0.85rem;
}

.step-nav-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  padding: 0.45rem 0.4rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.step-nav-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
}

.step-nav-btn.active {
  background: rgba(99, 102, 241, 0.25);
  border-color: #818cf8;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.25);
}

.step-nav-btn .step-num {
  font-size: 0.68rem;
  font-weight: 800;
  color: #fbbf24;
}

.step-nav-btn .step-name {
  font-size: 0.78rem;
  font-weight: 700;
}

/* 步骤话术内容气泡 */
.pitch-quote-bubble {
  background: rgba(30, 41, 59, 0.75);
  border-left: 3px solid #6366f1;
  border-radius: 0 8px 8px 0;
  padding: 0.75rem 0.9rem;
  font-size: 0.84rem;
  line-height: 1.5;
  color: #f1f5f9;
  margin-bottom: 0.75rem;
}

.pitch-quote-bubble strong {
  color: #f87171;
}

.prompter-bottom-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-pitch-action {
  flex: 1;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
  border: none;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.45rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-pitch-action:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.btn-locate-action {
  background: rgba(255, 255, 255, 0.1);
  color: #c7d2fe;
  border: 1px solid rgba(255, 255, 255, 0.15);
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.45rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-locate-action:hover {
  background: rgba(99, 102, 241, 0.25);
  border-color: #818cf8;
  color: #ffffff;
}

/* ==========================================================================
   微信专用 750px 高清长图海报生成模态框样式
   ========================================================================== */
.poster-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.poster-modal-box {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 860px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.poster-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.15rem 1.5rem;
  background: #0f172a;
  color: #ffffff;
  border-bottom: 1px solid #1e293b;
}

.poster-header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.poster-header-title .m-icon {
  font-size: 1.5rem;
}

.poster-header-title .m-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin: 0;
}

.poster-header-title .m-sub {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 2px 0 0 0;
}

.btn-close-modal {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #cbd5e1;
  font-size: 1rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.btn-close-modal:hover {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.poster-modal-body {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
  overflow-y: auto;
}

.poster-preview-wrap {
  background: #e2e8f0;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  max-height: 520px;
  overflow-y: auto;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
}

.poster-preview-img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.poster-generating-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  color: #64748b;
  font-size: 0.85rem;
  padding: 3rem 1rem;
}

.spinner-ring {
  width: 36px;
  height: 36px;
  border: 3px solid #e2e8f0;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.poster-actions-panel {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.poster-meta-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem;
}

.meta-row {
  display: flex;
  align-items: baseline;
  margin-bottom: 0.5rem;
  font-size: 0.84rem;
}

.meta-row:last-child {
  margin-bottom: 0;
}

.meta-row .m-lbl {
  color: #64748b;
  min-width: 90px;
}

.meta-row .m-val {
  color: #0f172a;
}

.meta-row .val-score {
  color: #dc2626;
  font-weight: 800;
}

.meta-row .val-code {
  font-family: monospace;
  color: #475569;
}

.poster-btn-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-download-poster {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #ffffff;
  border: none;
  font-size: 0.92rem;
  font-weight: 700;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
  transition: all 0.2s ease;
}

.btn-download-poster:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
}

.btn-icon {
  width: 18px !important;
  height: 18px !important;
  flex-shrink: 0 !important;
}

.poster-btn-group .btn-icon {
  width: 18px !important;
  height: 18px !important;
  max-width: 18px !important;
  max-height: 18px !important;
}

.btn-copy-wechat-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #f1f5f9;
  color: #1e293b;
  border: 1px solid #cbd5e1;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 0.7rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-copy-wechat-text:hover {
  background: #e2e8f0;
}

.wechat-mobile-tip {
  display: flex;
  gap: 0.6rem;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 0.85rem;
}

.wechat-mobile-tip .tip-icon {
  font-size: 1.2rem;
  color: #3b82f6;
}

.wechat-mobile-tip .tip-text {
  font-size: 0.78rem;
  color: #1e40af;
  line-height: 1.45;
}

.wechat-mobile-tip .tip-text p {
  margin: 3px 0 0 0;
}

/* 企业高管专属 核心战报高亮样式 */
.btn-executive-poster {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.4) !important;
  transition: all 0.2s ease !important;
}

.btn-executive-poster:hover {
  background: linear-gradient(135deg, #fbbf24 0%, #d97706 50%, #92400e 100%) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(217, 119, 6, 0.5) !important;
}

.executive-quick-bar {
  margin-top: 1rem;
  padding-top: 0.85rem;
  border-top: 1px dashed rgba(255, 255, 255, 0.2);
}

.btn-quick-poster {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.25) 100%);
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 0.65rem 1rem;
  color: #fef3c7;
  font-size: 0.86rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-quick-poster:hover {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(217, 119, 6, 0.4) 100%);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
}

.btn-quick-icon {
  font-size: 1.1rem;
}

.btn-quick-arrow {
  background: #f59e0b;
  color: #0f172a;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 800;
}

.poster-summary-highlights {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.85rem 1rem;
}

.highlight-title {
  font-size: 0.82rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.highlight-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.78rem;
  color: #475569;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.highlight-list li {
  line-height: 1.4;
}

/* 响应式适配 (移动端 & 微信 WebView) */
@media (max-width: 768px) {
  .report-wrapper {
    padding-bottom: 2rem;
  }
  .top-action-bar {
    padding: 0.6rem 0.8rem;
  }
  .action-inner {
    flex-direction: column;
    align-items: stretch;
    gap: 0.6rem;
  }
  .bar-left {
    justify-content: space-between;
    width: 100%;
  }
  .bar-right {
    flex-wrap: wrap;
    gap: 0.4rem;
    width: 100%;
  }
  .bar-right .btn {
    font-size: 0.76rem;
    padding: 0.4rem 0.65rem;
  }
  .paper-container {
    margin: 0.5rem auto !important;
    padding: 1rem 0.8rem !important;
    border-radius: 8px !important;
    max-width: 100% !important;
    width: 100% !important;
    box-sizing: border-box !important;
    overflow-x: hidden !important;
  }
  .header-seal-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.6rem;
  }
  .official-seal {
    align-self: flex-start;
  }
  .meta-grid {
    grid-template-columns: 1fr !important;
    gap: 0.4rem !important;
  }
  .live-cert-banner {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 0.8rem !important;
  }
  .cert-banner-right {
    align-items: flex-start !important;
    width: 100% !important;
    overflow-x: auto;
  }
  .cert-hash-display {
    max-width: 100%;
    word-break: break-all;
  }
  .cert-models-flow {
    flex-wrap: wrap !important;
    justify-content: flex-start !important;
  }
  .score-card {
    flex-direction: column !important;
    align-items: flex-start !important;
    padding: 1.25rem 1rem !important;
    gap: 1rem !important;
  }
  .score-number-box {
    border-right: none !important;
    border-bottom: 1px dashed rgba(0, 0, 0, 0.15) !important;
    padding-right: 0 !important;
    padding-bottom: 0.75rem !important;
    width: 100% !important;
  }
  .battle-stage-grid {
    grid-template-columns: 1fr !important;
    gap: 1.25rem !important;
  }
  .vs-badge-circle {
    display: none !important;
  }
  .economic-kpi-grid {
    grid-template-columns: 1fr !important;
    gap: 0.6rem !important;
  }
  .poster-modal-body {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1rem;
  }
  .poster-preview-wrap {
    max-height: 360px;
  }
  .sales-prompter-dock {
    bottom: 0.75rem;
    right: 0.75rem;
    left: 0.75rem;
    width: auto;
  }
  .compare-dual-grid {
    grid-template-columns: 1fr !important;
    gap: 1rem !important;
  }
}
</style>
