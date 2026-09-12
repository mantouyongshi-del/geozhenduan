<template>
  <div class="console-container">
    <!-- 头部品牌条 -->
    <header class="console-header">
      <div class="header-inner">
        <div class="brand-badge">
          <!-- 舒展大气的品牌 Logo (无小气方框束缚) -->
          <router-link to="/" class="brand-logo-free" title="蜉蝣小宝 · AI 营销智能大脑 (点击回到品牌官网)">
            <div class="logo-soft-aura"></div>
            <img src="/logo-white.png" alt="蜉蝣小宝" class="brand-logo-img" />
          </router-link>
          <span class="brand-tag">全国企业智能营销云 · 售前拓客引擎</span>
          <span class="live-status-pill">
            <span class="pulse-dot"></span>
            官方六大引擎直连在线
          </span>
        </div>
        <div class="header-nav">
          <button 
            type="button" 
            class="nav-fuel-btn" 
            :class="{ 'has-warning': hasBalanceWarning }"
            @click="showFuelModal = true"
            title="查看 6 大 AI 大模型实时算力配额、充值对账与投屏脱敏"
          >
            <span class="pulse-dot" :class="{ 'dot-warning': hasBalanceWarning }"></span>
            <span class="fuel-text">⚡ 诊断算力燃料池</span>
            <span class="fuel-pill-num" v-if="modelsBalance && !isPrivacyMode">
              ¥{{ (modelsBalance.total_cny_balance !== undefined ? modelsBalance.total_cny_balance.toFixed(2) : '20.56') }}
            </span>
            <span class="fuel-pill-num" v-else-if="isPrivacyMode">¥ •••</span>
            <span class="fuel-arrow">↗</span>
          </button>
          <router-link to="/" class="nav-link nav-home-link">🏠 品牌官网</router-link>
          <router-link to="/ai_report" class="nav-link">📊 客户报表看板</router-link>
          <router-link to="/diagnostic" class="nav-link active">🎯 准客户 AI 可见度体检</router-link>
        </div>
      </div>
    </header>

    <main class="console-main">
      <!-- 权威公信力 Hero 区域 -->
      <div class="hero-section">
        <div class="hero-pill-tag">⚡ 2026 企业级 GEO 智能搜索引擎优化与攻防巡检系统</div>
        <h1 class="hero-title">企业 AI 搜索引擎可见度 · 售前全网诊断工作台</h1>
        <p class="hero-sub">
          现场直连 <strong>字节跳动豆包 · 深度求索DeepSeek · 月之暗面Kimi · 阿里通义千问 · 腾讯元宝 · 百度智能搜索</strong>，出具穿透级《企业 AI 可见度体检报告》，用铁证向老板证明“潜在客户已被同行截流”！
        </p>

        <!-- 官方大模型品牌矩阵徽章墙 -->
        <div class="model-wall">
          <div class="model-badge badge-doubao">
            <span class="m-icon">⚡</span>
            <div class="m-info">
              <span class="m-name">字节跳动 · 豆包</span>
              <span class="m-desc">火山引擎方舟直连 · 抖音生态</span>
            </div>
          </div>
          <div class="model-badge badge-deepseek">
            <span class="m-icon">🧠</span>
            <div class="m-info">
              <span class="m-name">深度求索 · DeepSeek</span>
              <span class="m-desc">官方开放平台 · 深度推理链</span>
            </div>
          </div>
          <div class="model-badge badge-kimi">
            <span class="m-icon">🌙</span>
            <div class="m-info">
              <span class="m-name">月之暗面 · Kimi</span>
              <span class="m-desc">Moonshot 直连 · 深度长文/研报</span>
            </div>
          </div>
          <div class="model-badge badge-tongyi">
            <span class="m-icon">🌐</span>
            <div class="m-info">
              <span class="m-name">阿里巴巴 · 通义千问</span>
              <span class="m-desc">百炼原生全网检索 · B2B</span>
            </div>
          </div>
          <div class="model-badge badge-yuanbao">
            <span class="m-icon">💬</span>
            <div class="m-info">
              <span class="m-name">腾讯科技 · 腾讯元宝</span>
              <span class="m-desc">混元内核 · 微信公众号生态</span>
            </div>
          </div>
          <div class="model-badge badge-baidu">
            <span class="m-icon">🔍</span>
            <div class="m-info">
              <span class="m-name">百度智能 · 百度搜索</span>
              <span class="m-desc">知识图谱 · 权威词条收录</span>
            </div>
          </div>
        </div>

        <!-- 平台公信力指标条 -->
        <div class="trust-stats-row">
          <div class="trust-stat-item">
            <div class="ts-num">6 大</div>
            <div class="ts-label">主流 AI 搜索真机直连</div>
          </div>
          <div class="trust-stat-divider"></div>
          <div class="trust-stat-item">
            <div class="ts-num">100%</div>
            <div class="ts-label">双端(PC/移动)真机穿透</div>
          </div>
          <div class="trust-stat-divider"></div>
          <div class="trust-stat-item">
            <div class="ts-num">2,840+</div>
            <div class="ts-label">实体企业已出具体检书</div>
          </div>
          <div class="trust-stat-divider"></div>
          <div class="trust-stat-item">
            <div class="ts-num">98.6%</div>
            <div class="ts-label">同行隐形截流实体识别率</div>
          </div>
        </div>
      </div>

      <!-- 销售现场“30秒极速促单演示通道” (免等待直接调出国家大模型真机打脸样本) -->
      <section class="fast-demo-banner">
        <div class="demo-banner-content">
          <div class="demo-banner-left">
            <div class="demo-tag-row">
              <span class="demo-badge">⚡ 销售拜访 · 展会面谈实战利器</span>
              <span class="demo-sub-tag">无需等待 15 秒算力并发 · 即开即讲</span>
            </div>
            <h2 class="demo-title">🎙️ 销售现场“30秒极速促单演示模式”</h2>
            <p class="demo-desc">
              专为销售顾问现场面谈与展会打单定制：<strong>10秒打脸定性 ➔ 20秒红黑对比 ➔ 30秒ROI回本促单</strong>。内置真实高危企业诊断样本，直接出具带防伪存证与促单提词器的实战报告！
            </p>
            
            <div class="demo-cases-pills">
              <span class="case-label">经典实战案例库：</span>
              <button 
                type="button" 
                class="demo-case-btn active-case" 
                @click="launchFastDemo('FYXB-1788971230-2154')"
                title="厨电制造高危样本：综合得分仅16分，被方太/老板全额截流"
              >
                <span class="case-fire">🔥</span>
                <span class="case-name">宁波博西尼厨卫 (厨电制造 · 16分高危)</span>
                <span class="case-arrow">➔</span>
              </button>
              <button 
                type="button" 
                class="demo-case-btn" 
                @click="launchFastDemo('FYXB-1788971173-7426')"
                title="备用实测样本：27分截流样本"
              >
                <span class="case-icon">🏭</span>
                <span class="case-name">博西尼集成灶 (对比样本 · 27分)</span>
                <span class="case-arrow">➔</span>
              </button>
            </div>
          </div>

          <div class="demo-banner-right">
            <div class="demo-action-card">
              <div class="demo-card-head">
                <span class="clock-icon">⏱️</span>
                <span class="card-head-title">30 秒签单必杀闭环</span>
                <span class="speed-pill">免等0秒</span>
              </div>
              <div class="demo-steps-mini">
                <div class="mini-step">
                  <span class="step-idx">① 10s</span>
                  <span class="step-txt"><strong>打脸定性</strong>：综合得分仅16分，全网0%推荐</span>
                </div>
                <div class="mini-step">
                  <span class="step-idx">② 20s</span>
                  <span class="step-txt"><strong>红黑打脸</strong>：AI把竞品当标杆，劝客户对贵司谨慎</span>
                </div>
                <div class="mini-step">
                  <span class="step-idx">③ 30s</span>
                  <span class="step-txt"><strong>ROI促单</strong>：每月截回2单即100%回本，锁定签约</span>
                </div>
              </div>
              <button 
                type="button" 
                class="btn-launch-demo" 
                @click="launchFastDemo('FYXB-1788971230-2154')"
              >
                <span>🚀 立即调出【30秒现场极速演示报告】</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <div class="content-grid">
        <!-- 左侧: 诊断输入表单 -->
        <div class="card form-card">
          <div class="card-header-row">
            <h2 class="card-title">📝 录入准客户信息</h2>
            <span class="card-tip-pill">快速出具体检单 · 现场打脸促单</span>
          </div>

          <form @submit.prevent="handleStartDiagnostic">
            <!-- 销售录入精准度防失真指引横幅 -->
            <div class="sales-input-guidance-banner">
              <div class="guidance-badge">⚠️ 销售顾问录入规范与事实基准严谨须知</div>
              <div class="guidance-content">
                <strong>企业全称与事实标尺必须 100% 客观精准对应单体实体：</strong>
                <span>① 以酒旅与连锁品牌为例，请严格录入单体物业全称（如<strong>“长沙岳麓万豪酒店”</strong>），<strong>切勿录入泛指名称“长沙万豪酒店”</strong>；<br>
                ② 真实事实标尺中的<strong>展业地/所属板块</strong>必须严谨准确（例如长沙岳麓万豪酒店位于<strong>金星中路18号·西湖公园/咸嘉湖板块</strong>，切勿与滨江新城的<strong>湘江FFC万豪</strong>混淆），系统将以此作为官方基准并直接合成 P0 落地工单！</span>
              </div>
            </div>

            <div class="form-group poi-relative-group">
              <div class="form-label-row">
                <label class="form-label">准客户工商全称 (必填)</label>
                <span class="poi-shield-tag" title="高德开放平台 Web服务直连，输入自动精准匹配官方标准实体与门牌地址">
                  🛰️ 高德地图 POI 智能联想
                </span>
              </div>
              <div class="input-with-poi-wrap">
                <input 
                  v-model="form.target_company" 
                  @input="onCompanyInput"
                  @focus="onCompanyInput"
                  @blur="closePoiDropdown"
                  required 
                  placeholder="输入企业或品牌名称，高德将自动联想官方实体与准确地址..." 
                  class="form-input" 
                />
                <span class="poi-loading-spinner" v-if="isSearchingPoi && activePoiField === 'company'">⏳</span>
              </div>

              <!-- 高德 POI 智能联想候选浮层 -->
              <div 
                class="poi-suggestions-dropdown" 
                v-if="showPoiDropdown && activePoiField === 'company' && poiSuggestions.length"
              >
                <div class="dropdown-header">
                  <span>🛰️ 高德地图官方实体库 (点击一键反填标准全称与真实事实标尺)</span>
                  <span class="dropdown-count">{{ poiSuggestions.length }} 个官方候选</span>
                </div>
                <div 
                  class="poi-item" 
                  v-for="poi in poiSuggestions" 
                  :key="poi.id || poi.name"
                  @mousedown.prevent="selectPoi(poi)"
                >
                  <div class="poi-item-main">
                    <div class="poi-name-row">
                      <span class="poi-badge">高德 POI 认证</span>
                      <strong class="poi-name">{{ poi.name }}</strong>
                    </div>
                    <div class="poi-addr-row" v-if="poi.full_address">
                      <span class="poi-icon">📍</span>
                      <span class="poi-addr-text">{{ poi.full_address }}</span>
                    </div>
                  </div>
                  <div class="poi-action-col">
                    <span class="poi-apply-pill">一键带入标尺 ↵</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 多门店 / 连锁消歧拦截告警胶囊 -->
            <div class="disambiguation-alert-banner" v-if="poiDisambiguation.isChainGeneric">
              <div class="dis-icon">⚠️</div>
              <div class="dis-body">
                <div class="dis-title">连锁/集团多门店实体消歧拦截提醒</div>
                <div class="dis-desc">{{ poiDisambiguation.warningMessage }}</div>
                <div class="dis-pills" v-if="poiDisambiguation.candidateBranches.length">
                  <span class="dis-pills-label">检测到具体单体物业（点击一键替换）：</span>
                  <button 
                    type="button" 
                    v-for="branch in poiDisambiguation.candidateBranches" 
                    :key="branch" 
                    class="dis-pill-btn"
                    @click="selectBranchQuickly(branch)"
                  >
                    🏨 {{ branch }}
                  </button>
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group poi-relative-group">
                <label class="form-label">品牌简称/常用名 (必填)</label>
                <div class="input-with-poi-wrap">
                  <input 
                    v-model="form.brand_name" 
                    @input="onBrandInput"
                    @focus="onBrandInput"
                    @blur="closePoiDropdown"
                    required 
                    placeholder="例如: 长沙岳麓万豪酒店 / 恒达门窗" 
                    class="form-input" 
                  />
                  <span class="poi-loading-spinner" v-if="isSearchingPoi && activePoiField === 'brand'">⏳</span>
                </div>

                <!-- 品牌名 POI 联想浮层 -->
                <div 
                  class="poi-suggestions-dropdown" 
                  v-if="showPoiDropdown && activePoiField === 'brand' && poiSuggestions.length"
                >
                  <div class="dropdown-header">
                    <span>🛰️ 高德地图官方实体库</span>
                  </div>
                  <div 
                    class="poi-item" 
                    v-for="poi in poiSuggestions" 
                    :key="poi.id || poi.name"
                    @mousedown.prevent="selectPoi(poi)"
                  >
                    <div class="poi-item-main">
                      <div class="poi-name-row">
                        <span class="poi-badge">POI 认证</span>
                        <strong class="poi-name">{{ poi.name }}</strong>
                      </div>
                      <div class="poi-addr-row" v-if="poi.full_address">
                        <span class="poi-icon">📍</span>
                        <span class="poi-addr-text">{{ poi.full_address }}</span>
                      </div>
                    </div>
                    <div class="poi-action-col">
                      <span class="poi-apply-pill">一键带入 ↵</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">所属行业领域 (必填)</label>
                <input 
                  v-model="form.industry" 
                  required 
                  placeholder="例如: 高端五星级豪华酒店 / 定制门窗" 
                  class="form-input" 
                />
              </div>
              <div class="form-group">
                <label class="form-label">展业城市/地区</label>
                <input 
                  v-model="form.city" 
                  placeholder="例如: 怀化 / 杭州 / 嘉兴" 
                  class="form-input" 
                />
              </div>
            </div>

            <!-- 快捷行业词模版 -->
            <div class="preset-templates">
              <span class="preset-label">实测案例快速填入:</span>
              <button 
                type="button" 
                v-for="tpl in industryTemplates" 
                :key="tpl.name" 
                class="preset-btn"
                @click="applyTemplate(tpl)"
              >
                {{ tpl.name }}
              </button>
            </div>

            <!-- 核心测试词输入区 + 智能生成按钮 -->
            <div class="form-group">
              <div class="form-label-row">
                <label class="form-label">核心测试搜索词 (提示词，每行一个)</label>
                <button 
                  type="button" 
                  class="btn-smart-gen" 
                  @click="generateSmartKeywords"
                  :disabled="isGeneratingKws"
                >
                  <span v-if="isGeneratingKws">✨ 正在根据 GEO 决策意图生成...</span>
                  <span v-else>✨ 一键生成行业高频截流词</span>
                </button>
              </div>

              <!-- 城市拓展意图深度动态指示与区县快速带入胶囊 -->
              <div class="geo-intent-box" :class="geoIntentInfo.isNational ? 'is-national' : 'is-regional'">
                <div class="intent-meta-row">
                  <div class="intent-badge-pill" :class="geoIntentInfo.isNational ? 'pill-national' : 'pill-regional'">
                    <span v-if="geoIntentInfo.isNational">🌐 {{ geoIntentInfo.modeLabel }}</span>
                    <span v-else>🏙️ {{ geoIntentInfo.modeLabel }}</span>
                  </div>
                  <div class="intent-desc-text">
                    {{ geoIntentInfo.modeDesc }}
                  </div>
                </div>

                <!-- 如果属于区域城市且有下辖区县，展示快速胶囊列表 -->
                <div class="district-capsules-wrap" v-if="!geoIntentInfo.isNational && geoIntentInfo.districts && geoIntentInfo.districts.length > 0">
                  <span class="capsules-tip">点击带入区县下沉词:</span>
                  <div class="capsules-scroll">
                    <button
                      type="button"
                      v-for="dist in geoIntentInfo.districts"
                      :key="dist"
                      class="capsule-btn"
                      @click="appendDistrictKeyword(dist)"
                      :title="`点击将【${dist}】精准截流词追加至下方测试列表`"
                    >
                      <span class="capsule-plus">+</span>
                      <span>{{ dist }}</span>
                    </button>
                  </div>
                </div>
              </div>

              <textarea 
                v-model="keywordsStr" 
                rows="4" 
                required
                placeholder="例如:&#10;全国十大知名激光切管机品牌实力横评对比&#10;激光切管机全国源头生产厂家直供批量采购评测&#10;采购激光切管机全国源头厂家直采避坑选型指南与真实ROI"
                class="form-textarea"
              ></textarea>
              <span class="form-tip">建议保留 3~5 组高转化意图词。在全国模式下聚焦头部榜单与供应链；在城市模式下向下穿透区县，实现全域拦截。</span>
            </div>

            <!-- 企业真实事实基准标尺 (用于 DeepSeek 事实核验与抓包) -->
            <div class="facts-benchmark-box">
              <div class="box-title-row clickable" @click="showFactsSetting = !showFactsSetting">
                <div class="box-title">
                  <span>🎯 企业真实事实基准标尺 (可选 · 用于大模型事实核验与防幻觉)</span>
                  <span class="benchmark-pill">DeepSeek Flash 裁判比对</span>
                </div>
                <span class="toggle-indicator">{{ showFactsSetting ? '▲ 收起' : '▼ 展开核验设置' }}</span>
              </div>

              <div v-show="showFactsSetting" class="facts-setting-body">
                <div class="facts-intro-tip">
                  💡 输入企业真实指标，系统将驱动 <strong>DeepSeek Flash 裁判中枢</strong> 逐一核验 6 大外部大模型是否存在张冠李戴、年份混淆或资质遗漏，并在体检书生成专属《原子事实纠错看板》！
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">成立年份 / 开业时间</label>
                    <input v-model="formFacts.founded_year" placeholder="例如: 2018年" class="form-input" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">企业总部 / 核心展业地</label>
                    <input v-model="formFacts.headquarters" placeholder="例如: 湖南长沙" class="form-input" />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">核心定位与业务规格</label>
                    <input v-model="formFacts.key_features" placeholder="例如: 拥有400间云端景观客房与全套商务宴会设施" class="form-input" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">官方资质与权威荣誉</label>
                    <input v-model="formFacts.certifications" placeholder="例如: 国家五星级豪华饭店评定 / 国际金钥匙联盟" class="form-input" />
                  </div>
                </div>
              </div>
            </div>

            <!-- 加盟商授权署名设置 (持久化记忆) -->
            <div class="agency-settings-box">
              <div class="box-title-row">
                <div class="box-title">🏢 加盟商授权署名设置 (打印及分享时展示)</div>
                <span class="saved-indicator" v-if="infoSaved">✓ 本地已持久化记忆</span>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">授权服务中心名称</label>
                  <input v-model="form.agency_name" @input="saveAgencyInfo" class="form-input" />
                </div>
                <div class="form-group">
                  <label class="form-label">认证数字化顾问姓名</label>
                  <input v-model="form.consultant_name" @input="saveAgencyInfo" class="form-input" />
                </div>
              </div>
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label">顾问联系电话/微信 (展示在体检单底部)</label>
                <input v-model="form.consultant_phone" @input="saveAgencyInfo" placeholder="例如: 138-0000-8888" class="form-input" />
              </div>
            </div>

            <button type="submit" class="btn btn-submit" :disabled="isRunning">
              <span v-if="isRunning">📡 正在并发调度各大模型真实检索中...</span>
              <span v-else>🚀 立即启动全网六大 AI 搜索引擎体检</span>
            </button>
          </form>
        </div>

        <!-- 右侧: 签单谈资秘籍 & 最近体检历史 -->
        <div class="side-col">
          <!-- 签单销售打法指引卡 (带 Tab 切换) -->
          <div class="card pitch-card">
            <div class="pitch-tab-header">
              <button 
                type="button" 
                class="pitch-tab-btn" 
                :class="{ active: activePitchTab === 'close' }"
                @click="activePitchTab = 'close'"
              >
                ⚡ 30秒促单闭环
              </button>
              <button 
                type="button" 
                class="pitch-tab-btn" 
                :class="{ active: activePitchTab === 'rebuttal' }"
                @click="activePitchTab = 'rebuttal'"
              >
                💬 客户异议反客为主
              </button>
            </div>

            <div v-if="activePitchTab === 'close'" class="pitch-tab-body">
              <ul class="pitch-list">
                <li>
                  <strong>① 现场打脸痛点：</strong> 递过手机或打印件，指着 19 分（极度高危）：“王总，搜您全名确实有微量结果，但买家搜‘哪家好’时，6 大主流 AI 对您的推荐率是 0%！”
                </li>
                <li>
                  <strong>② 竞品截流取证：</strong> 指着报告上的竞品名字：“豆包和 DeepSeek 正在把您本地的准客户，全额白白送给这 3 家对手，每一天都在流失商机！”
                </li>
                <li>
                  <strong>③ 顺水推舟促单：</strong> 翻到 ROI 回本测算页：“我们这套四维 GEO 知识工程服务，您一个月只要截留回 1~2 单，当月就能把全款收回来，剩下 11 个月全是白赚！”
                </li>
              </ul>
            </div>

            <div v-else class="pitch-tab-body">
              <ul class="pitch-list">
                <li>
                  <strong>若客户说：“我们全靠老客户转介绍，不做线上”：</strong><br>
                  <em>反制话术：</em> “王总，老客户给朋友转介绍完，新客户回家第一件事就是打开豆包或 DeepSeek 搜一句‘某某品牌靠谱吗’。AI 一旦说‘未检索到权威报道、缺乏第三方背书’，那单就当场黄了！做 GEO 不是为了投广告，是为了不让老客户转介绍的单子被 AI 截走！”
                </li>
                <li>
                  <strong>若客户说：“我们已经在做传统搜索或短视频投流了”：</strong><br>
                  <em>反制话术：</em> “投流是‘停水就断电’，买一次点击扣一次钱；GEO 是向各大模型注入结构化知识资产，大模型一次收录，一年 365 天在自然对话流里免费为您推荐，ROI 是传统投流的 10 倍以上！”
                </li>
              </ul>
            </div>
          </div>

          <!-- 最近体检历史记录 -->
          <div class="card history-card">
            <div class="history-header">
              <div class="history-title-wrap">
                <h3 class="history-title">⏱️ 本地最近体检记录</h3>
                <span class="history-count" v-if="recentHistory.length">({{ recentHistory.length }} 份)</span>
              </div>
              <div class="history-header-right">
                <span class="scroll-tip-tag" v-if="recentHistory.length > 3">🖱️ 滚动浏览</span>
                <button v-if="recentHistory.length" class="btn-clear" @click="handleClearHistory" title="清空全部历史记录">🗑️ 清空</button>
                <button class="btn-refresh" @click="loadHistory">🔄 刷新</button>
              </div>
            </div>

            <div class="history-list">
              <div v-for="h in recentHistory" :key="h.report_code" class="history-item">
                <div class="history-top">
                  <span class="h-company" :title="h.target_company">{{ h.target_company }}</span>
                  <span class="h-score" :class="h.visibility_score < 30 ? 'score-danger' : (h.visibility_score < 60 ? 'score-warn' : 'score-ok')">
                    {{ h.visibility_score }} 分
                  </span>
                </div>
                <div class="history-bottom">
                  <span class="h-ind">{{ h.industry }} · {{ h.city || '全国' }}</span>
                  <div class="h-actions">
                    <button class="btn-copy-sm" @click="copyHistoryLink(h.report_code)">
                      {{ copiedCode === h.report_code ? '已复制 ✓' : '📋 复制链接' }}
                    </button>
                    <router-link :to="`/diagnostic_report?code=${h.report_code}`" class="h-link">
                      查看体检书 ➔
                    </router-link>
                  </div>
                </div>
              </div>
              <div v-if="recentHistory.length === 0" class="history-empty">
                暂无历史诊断记录，快为第一家客户体检吧！
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 正在体检全屏雷达遮罩 (5 步流水线震撼呈现) -->
    <div v-if="isRunning" class="radar-backdrop">
      <div class="radar-box">
        <div class="radar-scanner-wrap">
          <div class="radar-scanner-halo"></div>
          <div class="radar-scanner"></div>
          <img src="/logo-icon.png" alt="蜉蝣小宝" class="radar-center-logo" />
        </div>
        
        <h3 class="radar-title">正在全网穿透探测中...</h3>
        <p class="radar-sub">已连接 字节豆包 · DeepSeek · Kimi · 阿里千问 · 腾讯元宝 · 百度搜索</p>
        <div class="radar-timer">已探测：{{ elapsedSeconds }} 秒 (全流程预计 12~15 秒)</div>

        <!-- 5 步递进式流水线 -->
        <div class="radar-pipeline">
          <div 
            v-for="(step, sIdx) in radarSteps" 
            :key="sIdx" 
            class="pipeline-step"
            :class="{
              'step-done': currentStepIndex > sIdx,
              'step-active': currentStepIndex === sIdx,
              'step-waiting': currentStepIndex < sIdx
            }"
          >
            <div class="step-icon">
              <span v-if="currentStepIndex > sIdx">✓</span>
              <span v-else-if="currentStepIndex === sIdx" class="step-spinner">⚡</span>
              <span v-else>{{ sIdx + 1 }}</span>
            </div>
            <div class="step-text">{{ step.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 诊断算力燃料池 · 六大 AI 大模型实时配额沉浸式管理弹窗 -->
    <div 
      v-if="showFuelModal" 
      class="fuel-modal-backdrop" 
      @click.self="showFuelModal = false"
    >
      <div class="fuel-modal-window">
        <!-- 弹窗头部 -->
        <div class="fuel-modal-header">
          <div class="fmodal-title-wrap">
            <div class="fmodal-badge-row">
              <span class="pulse-dot" :class="{ 'dot-warning': hasBalanceWarning }"></span>
              <span class="fmodal-tag">官方商业 API 实时联机对账池</span>
              <span class="fmodal-sub-tag">6 大合规引擎直连</span>
            </div>
            <h3 class="fmodal-title">⚡ 诊断算力燃料池 · 六大 AI 大模型实时配额</h3>
          </div>
          <button type="button" class="btn-close-fmodal" @click="showFuelModal = false" title="关闭 (Esc)">✕</button>
        </div>

        <!-- 控制工具栏 -->
        <div class="fuel-modal-toolbar">
          <div class="toolbar-left">
            <div class="total-balance-pill" v-if="modelsBalance">
              <span class="total-label">全网可用燃料总池:</span>
              <span class="total-amount">¥ {{ isPrivacyMode ? '•••.••' : (modelsBalance.total_cny_balance !== undefined ? modelsBalance.total_cny_balance.toFixed(2) : '20.56') }}</span>
            </div>
            <button 
              type="button" 
              class="btn-privacy-toggle"
              :class="{ active: isPrivacyMode }"
              @click="isPrivacyMode = !isPrivacyMode"
              title="投屏或面谈时一键隐藏具体金额，防止底层成本底牌外露"
            >
              <span>{{ isPrivacyMode ? '🔒 投屏脱敏中 (已遮罩)' : '👁️ 投屏防窥脱敏' }}</span>
            </button>
          </div>

          <div class="toolbar-right">
            <span class="balance-update-time" v-if="balanceLastUpdated">
              🕒 对账更新: {{ balanceLastUpdated }}
            </span>
            <button 
              type="button" 
              class="btn-refresh-balance" 
              :class="{ 'is-refreshing': isLoadingBalance }" 
              @click="fetchModelsBalance"
              :disabled="isLoadingBalance"
              title="重新获取各大模型官方账单与额度"
            >
              <span class="refresh-icon">🔄</span>
              <span>{{ isLoadingBalance ? '获取中...' : '刷新实时余额' }}</span>
            </button>
          </div>
        </div>

        <!-- 6大模型卡片网格 -->
        <div class="fuel-modal-body">
          <div class="balance-cards-grid" v-if="modelsBalance && modelsBalance.models">
            <div 
              v-for="model in modelsBalance.models" 
              :key="model.platform" 
              class="balance-card"
              :class="[
                'provider-' + model.platform,
                'level-' + model.status_level
              ]"
            >
              <div class="card-top">
                <div class="model-info">
                  <div class="model-icon">{{ model.icon || getModelIcon(model.platform) }}</div>
                  <div class="model-text">
                    <div class="model-name">{{ model.platform_name }}</div>
                    <div class="model-cat" :title="model.model_name">{{ model.model_name }}</div>
                  </div>
                </div>
                <span class="status-indicator" :class="model.status_level">
                  {{ model.status_level === 'normal' ? '● 正常' : (model.status_level === 'warning' ? '▲ 预警' : '✕ 异常') }}
                </span>
              </div>

              <div class="card-balance-box">
                <div class="balance-label-row">
                  <span class="sub-label">账户实时可用额度</span>
                  <span class="tag-live" v-if="model.total_balance !== null">官方实时联机</span>
                  <span class="tag-cloud" v-else>云端签约配额</span>
                </div>
                
                <div class="main-balance" :class="{ 'live-number': model.total_balance !== null }">
                  <template v-if="model.total_balance !== null">
                    <span class="currency">¥</span>
                    <span class="num">{{ isPrivacyMode ? '•••' : model.total_balance.toFixed(2) }}</span>
                  </template>
                  <template v-else>
                    <span class="num non-live-text">{{ model.status_text }}</span>
                  </template>
                </div>

                <!-- 赠金与充值细分 breakdown (支持投屏隐私脱敏) -->
                <div class="balance-breakdown" v-if="model.total_balance !== null">
                  <div class="breakdown-item">
                    <span class="b-label">赠金:</span>
                    <span class="b-val">{{ isPrivacyMode ? '¥•••' : '¥' + (model.granted_balance || 0).toFixed(2) }}</span>
                    <span class="b-sep">|</span>
                    <span class="b-label">充值:</span>
                    <span class="b-val highlight">{{ isPrivacyMode ? '¥•••' : '¥' + (model.topped_up_balance || 0).toFixed(2) }}</span>
                  </div>
                </div>
                <div class="balance-breakdown note-mode" v-else>
                  <span class="b-note" :title="model.billing_type">{{ model.billing_type }}</span>
                </div>
              </div>

              <div class="card-footer">
                <span class="key-hint" :title="model.masked_key">
                  🔑 {{ model.masked_key }}
                </span>
                <a 
                  v-if="model.console_url" 
                  :href="model.console_url" 
                  target="_blank" 
                  rel="noopener" 
                  class="link-console"
                >
                  官方充值 ↗
                </a>
              </div>
            </div>
          </div>

          <!-- 骨架屏 / 加载态 -->
          <div class="balance-cards-grid skeleton-grid" v-else-if="isLoadingBalance">
            <div class="balance-card skeleton-card" v-for="i in 6" :key="i">
              <div class="sk-line sk-title"></div>
              <div class="sk-line sk-big"></div>
              <div class="sk-line sk-sub"></div>
            </div>
          </div>
        </div>

        <!-- 弹窗底部说明 -->
        <div class="fuel-modal-footer">
          <div class="fmodal-tip">
            💡 <strong>商业对账说明：</strong>数据采信自火山引擎、阿里云百炼、月之暗面、百度千帆等各模型官方计费 API。单模型额度告急将自动触发状态预警。
          </div>
          <button type="button" class="btn-fmodal-close" @click="showFuelModal = false">
            关闭面板 (Esc)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import geoApi from '../api/geo';
import {
  resolveCityAndDistricts,
  generateMultiTierKeywords,
  generateSingleDistrictKeyword,
  cleanIndustryToCategory
} from '../utils/geoDistricts';

const router = useRouter();
const route = useRoute();

const form = ref({
  target_company: '',
  brand_name: '',
  industry: '',
  city: '全国',
  agency_name: '蜉蝣小宝 · 官方直营授权运营中心',
  consultant_name: '金牌数字化营销顾问',
  consultant_phone: '138-0000-8888'
});

// 动态解析城市意图深度与下辖区县拓扑
const geoIntentInfo = computed(() => {
  return resolveCityAndDistricts(form.value.city);
});

const keywordsStr = ref('');
const isRunning = ref(false);
const recentHistory = ref([]);
const activePitchTab = ref('close');
const isGeneratingKws = ref(false);
const infoSaved = ref(false);
const copiedCode = ref(null);

// 事实核验基准设置状态
const showFactsSetting = ref(false);
const formFacts = ref({
  founded_year: '',
  headquarters: '',
  key_features: '',
  certifications: ''
});

// 高德地图权威 POI 智能联想与多门店消歧防呆状态
const poiSuggestions = ref([]);
const isSearchingPoi = ref(false);
const showPoiDropdown = ref(false);
const activePoiField = ref('company'); // 'company' | 'brand'
const poiDisambiguation = ref({
  isChainGeneric: false,
  warningMessage: '',
  candidateBranches: []
});
let poiDebounceTimer = null;

function onCompanyInput() {
  activePoiField.value = 'company';
  triggerPoiSearch(form.value.target_company);
}

function onBrandInput() {
  activePoiField.value = 'brand';
  triggerPoiSearch(form.value.brand_name);
}

function triggerPoiSearch(query) {
  if (poiDebounceTimer) clearTimeout(poiDebounceTimer);
  if (!query || query.trim().length < 2) {
    poiSuggestions.value = [];
    showPoiDropdown.value = false;
    poiDisambiguation.value = { isChainGeneric: false, warningMessage: '', candidateBranches: [] };
    return;
  }

  poiDebounceTimer = setTimeout(async () => {
    isSearchingPoi.value = true;
    try {
      const cityParam = form.value.city && form.value.city !== '全国' ? encodeURIComponent(form.value.city) : '';
      const url = `http://127.0.0.1:8001/api/v1/diagnostic/poi_suggest?keywords=${encodeURIComponent(query.trim())}&city=${cityParam}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        poiSuggestions.value = data.suggestions || [];
        showPoiDropdown.value = poiSuggestions.value.length > 0;
        poiDisambiguation.value = {
          isChainGeneric: Boolean(data.is_chain_generic),
          warningMessage: data.warning_message || '',
          candidateBranches: data.candidate_branches || []
        };
      }
    } catch (err) {
      console.warn('POI search failed:', err);
    } finally {
      isSearchingPoi.value = false;
    }
  }, 260);
}

async function selectPoi(poi) {
  form.value.target_company = poi.name;
  form.value.brand_name = poi.name;
  if (poi.cityname) {
    form.value.city = poi.cityname.replace('市', '');
  }
  showPoiDropdown.value = false;

  // 自动将高德权威官方地址与行政板块反填至事实标尺
  showFactsSetting.value = true;
  formFacts.value.headquarters = poi.full_address || `${poi.district} ${poi.address}`;

  // 尝试拉取深层详情 (官方电话、星级分类)
  if (poi.id) {
    try {
      const detailRes = await fetch(`http://127.0.0.1:8001/api/v1/diagnostic/poi_detail?poi_id=${poi.id}&name=${encodeURIComponent(poi.name)}`);
      if (detailRes.ok) {
        const detail = await detailRes.json();
        const tags = [];
        if (detail.type_tag) tags.push(detail.type_tag);
        if (detail.tel) tags.push(`官方直拨电话: ${detail.tel}`);
        if (tags.length) {
          formFacts.value.key_features = tags.join(' · ');
        }
      }
    } catch (err) {
      console.warn('POI detail load error:', err);
    }
  }

  // 选定具体单体物业后解除泛称警告
  poiDisambiguation.value.isChainGeneric = false;
}

function selectBranchQuickly(branchName) {
  form.value.target_company = branchName;
  form.value.brand_name = branchName;
  poiDisambiguation.value.isChainGeneric = false;
  triggerPoiSearch(branchName);
}

function closePoiDropdown() {
  setTimeout(() => {
    showPoiDropdown.value = false;
  }, 220);
}

// 大模型实时余额与配额监控
const modelsBalance = ref(null);
const isLoadingBalance = ref(false);
const balanceLastUpdated = ref('');
const showFuelModal = ref(false);
const isPrivacyMode = ref(false); // 投屏防窥脱敏模式

const hasBalanceWarning = computed(() => {
  if (!modelsBalance.value?.models) return false;
  return modelsBalance.value.models.some(m => m.status_level === 'warning' || m.status_level === 'danger');
});

// 雷达流水线步骤
const elapsedSeconds = ref(0);
const currentStepIndex = ref(0);
let timerInterval = null;

const radarSteps = [
  { label: '向公网权威知识库发起全网实时探针检索与索引召回' },
  { label: '穿透 字节跳动·豆包 手机端生态，动态召回全网及抖音生活圈公域信源' },
  { label: '连线 DeepSeek & Kimi 深度推理与长文本引擎核验公信力文献与研报' },
  { label: '穿透 阿里千问 & 腾讯元宝 & 百度 知识图谱，萃取竞品霸屏实体' },
  { label: '计算 GEO 四层渗透漏斗与商业经济流失模型' }
];

const industryTemplates = [
  {
    name: '🏨 高端酒旅(长沙岳麓)',
    industry: '高端五星级豪华酒店',
    city: '长沙',
    company: '长沙岳麓万豪酒店有限公司',
    brand: '长沙岳麓万豪酒店',
    keywords: '长沙岳麓区正规高端五星级酒店哪家好推荐\n长沙适合商务宴请的高端豪华酒店排名\n长沙核心商圈品质豪华酒店排名',
    facts: {
      founded_year: '2019年',
      headquarters: '湖南省长沙市岳麓区金星中路18号（西湖公园/市府咸嘉湖板块）',
      key_features: '拥有283间全景景观客房与逾2000平米会议空间，背靠岳麓山，毗邻西湖公园',
      certifications: '国家五星级旅游饭店评定 · 国际金钥匙酒店联盟'
    }
  },
  {
    name: '🌐 全国战略(全国)',
    industry: '工业数控激光切管机制造',
    city: '全国',
    company: '广东大族光电智能装备股份有限公司',
    brand: '大族激光',
    keywords: '全国十大知名激光切管机品牌实力横评对比\n激光切管机全国源头生产厂家直供批量采购评测\n采购激光切管机全国源头厂家直采避坑选型指南与真实ROI',
    facts: {
      founded_year: '1996年',
      headquarters: '广东省深圳市南山区',
      key_features: '全球知名的工业激光智能制造设备上市集团',
      certifications: '国家重点高新技术企业 · 制造业单项冠军示范企业'
    }
  },
  {
    name: '🤖 少儿科创(怀化)',
    industry: '少儿机器人编程培训',
    city: '怀化',
    company: '怀化博创智汇科教文化有限公司',
    brand: '博创少儿机器人',
    keywords: '怀化鹤城区正规少儿机器人编程机构哪家口碑好校区大\n中方县及周边到怀化选少儿机器人编程优质机构综合实力排行榜\n洪江市及怀化周边学少儿机器人编程收费价格明细与避坑选课指南',
    facts: {
      founded_year: '2020年',
      headquarters: '湖南省怀化市鹤城区',
      key_features: '本地少儿机器人与科创编程连锁示范基地',
      certifications: '全国青少年创客教育合规会员单位'
    }
  },
  {
    name: '🏭 智能制造(无锡)',
    industry: '工业数控激光切管机制造',
    city: '无锡',
    company: '无锡恒瑞智能装备科技有限公司',
    brand: '恒瑞智能装备',
    keywords: '无锡梁溪区激光切管机实体厂家哪家口碑好实力强\n锡山区及周边去无锡选激光切管机知名品牌综合实力排名\n惠山区及无锡周边采购激光切管机收费价格与避坑选型指南'
  },
  {
    name: '🏡 系统门窗(佛山)',
    industry: '高端断桥铝系统门窗与阳光房',
    city: '佛山',
    company: '佛山尚品佳豪智能家居系统有限公司',
    brand: '佳豪系统门窗',
    keywords: '佛山禅城区系统门窗实体厂家哪家口碑好实力强\n南海区及周边去佛山选系统门窗知名品牌综合实力排名\n顺德区及佛山周边采购系统门窗收费价格与避坑选型指南'
  },
  {
    name: '🦷 专科医疗(杭州)',
    industry: '数字化种植牙与微创正畸',
    city: '杭州',
    company: '杭州美莱数字化口腔门诊连锁有限公司',
    brand: '美莱齿科',
    keywords: '杭州上城区正规种植牙哪家口碑好技术强\n拱墅区及周边去杭州看种植牙知名专科实力排名\n西湖区及杭州本地做种植牙真实收费价格与避坑指南'
  },
  {
    name: '⚖️ 商务律所(广州)',
    industry: '企业常年法律顾问与商事纠纷',
    city: '广州',
    company: '广东中律律师事务所',
    brand: '中律律所',
    keywords: '广州天河区专业企业常年法律顾问团队哪家口碑好信誉高\n番禺区及周边到广州选企业常年法律顾问知名律师团队排名\n海珠区及广州企业聘请企业常年法律顾问收费标准与避坑手册'
  },
  {
    name: '📜 资质申报(深圳)',
    industry: '国家高新技术企业申报与专精特新',
    city: '深圳',
    company: '深圳市知远科创知识产权服务有限公司',
    brand: '知远科创',
    keywords: '深圳南山区高新企业认定专业代办哪家通过率高口碑好\n福田区及周边委托深圳高新企业认定服务机构实力综合排名\n宝安区及深圳申报高新企业认定补贴政策与审核避坑指南'
  }
];

function applyTemplate(tpl) {
  form.value.target_company = tpl.company;
  form.value.brand_name = tpl.brand;
  form.value.industry = tpl.industry;
  form.value.city = tpl.city || '全国';
  keywordsStr.value = tpl.keywords;
  if (tpl.facts) {
    formFacts.value = { ...tpl.facts };
    showFactsSetting.value = true;
  } else {
    formFacts.value = { founded_year: '', headquarters: '', key_features: '', certifications: '' };
  }
}

// 智能生成核心高频截流词（基于 DeepSeek Flash 内部裁判中枢 · 8大意图维度）
async function generateSmartKeywords() {
  if (!form.value.brand_name || !form.value.industry) {
    alert('请先填写品牌简称与所属行业');
    return;
  }
  isGeneratingKws.value = true;
  try {
    const res = await geoApi.generateIntentQueries({
      brand_name: form.value.brand_name.trim(),
      industry: form.value.industry.trim(),
      city: form.value.city || '全国',
      company_name: form.value.target_company?.trim() || form.value.brand_name.trim(),
      count: 6
    });
    if (res.data?.queries?.length) {
      keywordsStr.value = res.data.queries.map(q => q.query_text).join('\n');
      isGeneratingKws.value = false;
      return;
    }
  } catch (e) {
    console.warn('DeepSeek 动态生成失败，启用本地智能启发式兜底:', e);
  }

  // 本地兜底
  const kws = generateMultiTierKeywords({
    city: form.value.city,
    industry: form.value.industry,
    brand: form.value.brand_name
  });
  keywordsStr.value = kws.join('\n');
  isGeneratingKws.value = false;
}

// 点击区县胶囊快速追加下沉定向截流词
function appendDistrictKeyword(dist) {
  const kw = generateSingleDistrictKeyword({
    city: form.value.city,
    district: dist,
    industry: form.value.industry,
    brand: form.value.brand_name
  });
  
  const currentLines = keywordsStr.value
    .split('\n')
    .map(s => s.trim())
    .filter(Boolean);

  if (!currentLines.includes(kw)) {
    currentLines.push(kw);
    keywordsStr.value = currentLines.join('\n');
  }
}

// 顾问信息持久化
function saveAgencyInfo() {
  try {
    localStorage.setItem('geo_agency_name', form.value.agency_name);
    localStorage.setItem('geo_consultant_name', form.value.consultant_name);
    localStorage.setItem('geo_consultant_phone', form.value.consultant_phone);
    infoSaved.value = true;
    setTimeout(() => {
      infoSaved.value = false;
    }, 2000);
  } catch (e) {
    console.error(e);
  }
}

function loadAgencyInfo() {
  try {
    const a = localStorage.getItem('geo_agency_name');
    const c = localStorage.getItem('geo_consultant_name');
    const p = localStorage.getItem('geo_consultant_phone');
    if (a) form.value.agency_name = a;
    if (c) form.value.consultant_name = c;
    if (p) form.value.consultant_phone = p;
  } catch (e) {
    console.error(e);
  }
}

function startRadarTimer() {
  elapsedSeconds.value = 0;
  currentStepIndex.value = 0;
  if (timerInterval) clearInterval(timerInterval);

  timerInterval = setInterval(() => {
    elapsedSeconds.value++;
    if (elapsedSeconds.value <= 3) {
      currentStepIndex.value = 0;
    } else if (elapsedSeconds.value <= 7) {
      currentStepIndex.value = 1;
    } else if (elapsedSeconds.value <= 10) {
      currentStepIndex.value = 2;
    } else if (elapsedSeconds.value <= 13) {
      currentStepIndex.value = 3;
    } else {
      currentStepIndex.value = 4;
    }
  }, 1000);
}

function stopRadarTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

async function handleStartDiagnostic() {
  const targetComp = form.value.target_company?.trim() || '';
  const targetBrand = form.value.brand_name?.trim() || '';

  // 实体消歧与多门店连锁泛称拦截防呆 (严禁录入“万豪酒店”等未带分店的泛称)
  const genericTokens = ['万豪酒店', '万豪', '希尔顿酒店', '希尔顿', '喜来登酒店', '喜来登', '凯悦酒店', '洲际酒店', '香格里拉酒店', '保时捷', '海底捞', '肯德基', '麦当劳'];
  const isGeneric = genericTokens.includes(targetComp) || genericTokens.includes(targetBrand);
  if (isGeneric && poiDisambiguation.value.candidateBranches?.length > 0) {
    const recommended = poiDisambiguation.value.candidateBranches[0];
    alert(`【实体消歧防呆拦截】\n\n检测到录入的企业名称【${targetComp || targetBrand}】为泛指的集团品牌，未具体到单体物业/分店。\n\nAI 大模型在评测泛指品牌时会混合不同门店数据导致体检书失真！\n\n请在表单上方候选名单中点击具体单体门店（例如：${recommended}），或补充具体分店名称后再行体检！`);
    return;
  }

  const kws = keywordsStr.value.split('\n').map(k => k.trim()).filter(Boolean);
  if (!kws.length) {
    alert('请输入至少一个测试关键词');
    return;
  }

  isRunning.value = true;
  startRadarTimer();

  const customFacts = [];
  if (formFacts.value.founded_year?.trim()) {
    customFacts.push({ fact_type: '企业历史', fact_key: '成立时间/开业年份', fact_value: formFacts.value.founded_year.trim() });
  }
  if (formFacts.value.headquarters?.trim()) {
    customFacts.push({ fact_type: '地理归属', fact_key: '企业总部/核心展业地', fact_value: formFacts.value.headquarters.trim() });
  }
  if (formFacts.value.key_features?.trim()) {
    customFacts.push({ fact_type: '业务规格', fact_key: '核心定位与业务规模', fact_value: formFacts.value.key_features.trim() });
  }
  if (formFacts.value.certifications?.trim()) {
    customFacts.push({ fact_type: '资质荣誉', fact_key: '官方资质与权威背书', fact_value: formFacts.value.certifications.trim() });
  }

  try {
    const res = await geoApi.runDiagnostic({
      target_company: form.value.target_company.trim(),
      brand_name: form.value.brand_name.trim(),
      industry: form.value.industry.trim(),
      city: form.value.city || '全国',
      keywords: kws,
      agency_name: form.value.agency_name,
      consultant_name: form.value.consultant_name,
      consultant_phone: form.value.consultant_phone,
      brand_facts: customFacts.length ? customFacts : null
    });

    // 诊断完成，直接跳转至体检报告页面
    router.push({
      path: '/diagnostic_report',
      query: { code: res.data.report_code }
    });
  } catch (err) {
    // 自动重查防呆兜底：如果前端发生网络超时，但后端已在后台完成生成并写入历史库
    try {
      await new Promise(r => setTimeout(r, 1000));
      const historyRes = await geoApi.getRecentDiagnostics();
      const targetCmp = form.value.target_company.trim();
      const found = (historyRes.data || []).find(item => item.target_company === targetCmp);
      if (found && found.report_code) {
        router.push({
          path: '/diagnostic_report',
          query: { code: found.report_code }
        });
        return;
      }
    } catch (_) {}

    const errMsg = err.response?.data?.detail || err.message;
    if (errMsg && errMsg.includes('timeout')) {
      alert('体检探测提示：由于 6 大大模型全网深度探针与实时语义裁判计算量较大，后端可能正在完成生成。您可在下方历史记录中查看，或稍候重试。');
      loadHistory();
    } else {
      alert('体检执行失败: ' + errMsg);
    }
  } finally {
    isRunning.value = false;
    stopRadarTimer();
  }
}

async function loadHistory() {
  try {
    const res = await geoApi.getRecentDiagnostics();
    recentHistory.value = res.data;
  } catch (e) {
    console.error(e);
  }
}

async function handleClearHistory() {
  if (!confirm('确定要清空全部本地历史体检记录吗？此操作不可恢复。')) {
    return;
  }
  try {
    const res = await geoApi.clearRecentDiagnostics();
    if (res.data && res.data.success) {
      recentHistory.value = [];
      alert('已成功清空所有历史体检记录！');
    }
  } catch (e) {
    console.error('清空历史记录失败:', e);
    alert('清空失败，请稍后重试');
  }
}

function copyHistoryLink(code) {
  const url = `${window.location.origin}/#/diagnostic_report?code=${code}`;
  navigator.clipboard.writeText(url).then(() => {
    copiedCode.value = code;
    setTimeout(() => {
      copiedCode.value = null;
    }, 2500);
  });
}

function getModelIcon(provider) {
  const map = {
    deepseek: '🐋',
    moonshot: '🌙',
    dashscope: '⚡',
    volcengine: '🌋',
    tencent: '🐧',
    baidu: '🐾'
  };
  return map[provider] || '🤖';
}

async function fetchModelsBalance() {
  isLoadingBalance.value = true;
  try {
    const res = await geoApi.getModelsBalance();
    if (res.data) {
      modelsBalance.value = res.data;
      if (res.data.updated_at) {
        const d = new Date(res.data.updated_at * 1000);
        balanceLastUpdated.value = d.toLocaleTimeString();
      } else {
        balanceLastUpdated.value = new Date().toLocaleTimeString();
      }
    }
  } catch (err) {
    console.error('获取各大模型实时余额失败:', err);
  } finally {
    isLoadingBalance.value = false;
  }
}

function launchFastDemo(code = 'FYXB-1788971230-2154') {
  router.push(`/diagnostic_report?code=${code}&demo=true`);
}

function onGlobalKeyDown(e) {
  if (e.key === 'Escape' && showFuelModal.value) {
    showFuelModal.value = false;
  }
}

onMounted(() => {
  window.addEventListener('keydown', onGlobalKeyDown);
  loadAgencyInfo();
  loadHistory();
  fetchModelsBalance();
  if (route.query.brand || route.query.industry || route.query.company) {
    if (route.query.brand) form.value.brand_name = route.query.brand;
    if (route.query.company) form.value.target_company = route.query.company;
    else if (route.query.brand) form.value.target_company = route.query.brand;
    if (route.query.industry) form.value.industry = route.query.industry;
    if (route.query.city) form.value.city = route.query.city;
    if (route.query.keywords) {
      keywordsStr.value = Array.isArray(route.query.keywords) 
        ? route.query.keywords.join('\n') 
        : route.query.keywords.replace(/,/g, '\n');
    } else {
      generateSmartKeywords();
    }
  } else {
    applyTemplate(industryTemplates[0]);
  }
});

onUnmounted(() => {
  window.removeEventListener('keydown', onGlobalKeyDown);
  stopRadarTimer();
});
</script>

<style scoped>
/* 销售顾问录入规范指引横幅 */
.sales-input-guidance-banner {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1px solid #fde68a;
  border-left: 4px solid #f59e0b;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 1.25rem;
  font-size: 0.82rem;
  line-height: 1.55;
  box-shadow: 0 1px 3px rgba(245, 158, 11, 0.08);
}
.guidance-badge {
  display: inline-block;
  font-weight: 700;
  color: #b45309;
  background: #fef3c7;
  border: 1px solid #fcd34d;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.35rem;
  font-size: 0.75rem;
  letter-spacing: 0.02em;
}
.guidance-content strong {
  color: #92400e;
  font-weight: 700;
}
.guidance-content span {
  color: #4b5563;
}

.console-container {
  min-height: 100vh;
  background-color: #f8fafc;
}

/* Header */
.console-header {
  background: #0f172a;
  color: #ffffff;
  padding: 0.9rem 2rem;
  border-bottom: 2px solid #6366f1;
}

.header-inner {
  max-width: 1320px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* 舒展大气的品牌 Logo 容器 (无小气硬边框) */
.brand-logo-free {
  position: relative;
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
  padding: 4px 6px;
  transition: transform 0.25s ease;
}

.brand-logo-free:hover {
  transform: scale(1.04);
}

.logo-soft-aura {
  position: absolute;
  inset: -10px -18px;
  background: radial-gradient(ellipse at center, rgba(56, 189, 248, 0.45) 0%, rgba(99, 102, 241, 0.25) 50%, transparent 72%);
  filter: blur(14px);
  pointer-events: none;
  opacity: 0.75;
  transition: opacity 0.3s ease;
}

.brand-logo-free:hover .logo-soft-aura {
  opacity: 1;
}

.brand-logo-img {
  position: relative;
  height: 38px;
  width: auto;
  max-width: 155px;
  object-fit: contain;
  display: block;
  filter: drop-shadow(0 2px 12px rgba(56, 189, 248, 0.35));
}

.brand-logo-text {
  font-size: 1.35rem;
  font-weight: 900;
  background: linear-gradient(135deg, #a5b4fc 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}

.brand-tag {
  background: #1e293b;
  border: 1px solid #334155;
  color: #cbd5e1;
  font-size: 0.75rem;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.live-status-pill {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #34d399;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.live-status-pill.clickable-pill {
  cursor: pointer;
  transition: all 0.2s ease;
}

.live-status-pill.clickable-pill:hover {
  background: rgba(16, 185, 129, 0.25);
  border-color: #34d399;
  transform: translateY(-1px);
}

.pill-chip {
  background: rgba(0, 0, 0, 0.35);
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 700;
  color: #a5b4fc;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.nav-fuel-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.22) 0%, rgba(16, 185, 129, 0.16) 100%);
  border: 1px solid rgba(99, 102, 241, 0.45);
  border-radius: 9999px;
  padding: 0.35rem 0.85rem;
  color: #e2e8f0;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.nav-fuel-btn:hover {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.35) 0%, rgba(16, 185, 129, 0.28) 100%);
  border-color: #818cf8;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
}

.nav-fuel-btn.has-warning {
  border-color: #f59e0b;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(239, 68, 68, 0.2) 100%);
}

.nav-fuel-btn .fuel-pill-num {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  color: #4cd964;
  font-weight: 800;
  background: rgba(0, 0, 0, 0.35);
  padding: 1px 7px;
  border-radius: 4px;
}

.nav-fuel-btn .fuel-arrow {
  color: #818cf8;
  font-size: 0.82rem;
  transition: transform 0.2s;
}

.nav-fuel-btn:hover .fuel-arrow {
  transform: translate(2px, -2px);
}

.nav-link {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  transition: all 0.15s;
}

.nav-link:hover, .nav-link.active {
  color: #ffffff;
  background: #1e293b;
}

/* Main */
.console-main {
  max-width: 1320px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

/* Hero Section */
.hero-section {
  text-align: center;
  margin-bottom: 2.25rem;
}

.hero-pill-tag {
  display: inline-block;
  background: #e0e7ff;
  color: #4338ca;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.25rem 0.85rem;
  border-radius: 999px;
  margin-bottom: 0.75rem;
}

.hero-title {
  font-size: 2.2rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.5px;
}

.hero-sub {
  font-size: 1.05rem;
  color: #64748b;
  margin-top: 0.6rem;
  max-width: 820px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

/* Model Wall */
.model-wall {
  display: flex;
  justify-content: center;
  gap: 0.85rem;
  margin: 1.5rem auto 1.25rem;
  flex-wrap: wrap;
  max-width: 1100px;
}

.model-badge {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.55rem 0.95rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  transition: all 0.2s ease;
}

.model-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.06);
}

.badge-doubao { border-left: 4px solid #00c4b4; }
.badge-deepseek { border-left: 4px solid #1e40af; }
.badge-kimi { border-left: 4px solid #0d9488; }
.badge-tongyi { border-left: 4px solid #f97316; }
.badge-yuanbao { border-left: 4px solid #7c3aed; }
.badge-baidu { border-left: 4px solid #ef4444; }

.m-icon {
  font-size: 1.2rem;
}

.m-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.m-name {
  font-size: 0.85rem;
  font-weight: 800;
  color: #1e293b;
}

.m-desc {
  font-size: 0.7rem;
  color: #64748b;
}

/* Trust Stats Bar */
.trust-stats-row {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem 2rem;
  max-width: 960px;
  margin: 0 auto;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}

.trust-stat-item {
  text-align: center;
  flex: 1;
}

.trust-stat-clickable {
  cursor: pointer;
  border-radius: 8px;
  padding: 0.25rem 0.4rem;
  transition: all 0.2s ease;
}

.trust-stat-clickable:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
}

.ts-fuel-chip {
  display: inline-block;
  font-size: 0.65rem;
  background: #e0e7ff;
  color: #4338ca;
  padding: 1px 6px;
  border-radius: 4px;
  vertical-align: middle;
  font-weight: 700;
  margin-left: 4px;
}

.ts-num {
  font-size: 1.4rem;
  font-weight: 900;
  color: #4f46e5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.ts-label {
  font-size: 0.78rem;
  color: #64748b;
  margin-top: 0.2rem;
  font-weight: 500;
}

.trust-stat-divider {
  width: 1px;
  height: 32px;
  background: #e2e8f0;
}

/* Grid Layout */
.content-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 1.75rem;
  margin-top: 2rem;
}

@media (max-width: 960px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.card {
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  padding: 1.6rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.card-tip-pill {
  font-size: 0.75rem;
  color: #6366f1;
  background: #eef2ff;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-weight: 600;
}

/* Form Styles */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.1rem;
}

.form-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #334155;
}

.btn-smart-gen {
  background: #f0fdf4;
  border: 1px solid #86efac;
  color: #166534;
  font-size: 0.76rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-smart-gen:hover {
  background: #dcfce7;
  border-color: #4ade80;
}

/* 城市拓展意图深度动态指示与区县带入 */
.geo-intent-box {
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  margin-top: 0.35rem;
  margin-bottom: 0.5rem;
  transition: all 0.25s ease;
}

.geo-intent-box.is-national {
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
}

.geo-intent-box.is-regional {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.intent-meta-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
}

.intent-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: 4px;
}

.intent-badge-pill.pill-national {
  background: #6366f1;
  color: #ffffff;
}

.intent-badge-pill.pill-regional {
  background: #059669;
  color: #ffffff;
}

.intent-desc-text {
  font-size: 0.76rem;
  color: #334155;
  line-height: 1.4;
  flex: 1;
  font-weight: 500;
}

.district-capsules-wrap {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 0.55rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #cbd5e1;
}

.capsules-tip {
  font-size: 0.72rem;
  color: #64748b;
  font-weight: 600;
  white-space: nowrap;
}

.capsules-scroll {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  overflow-x: auto;
  padding-bottom: 2px;
}

.capsule-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.18rem 0.55rem;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.capsule-btn:hover {
  background: #ecfdf5;
  border-color: #059669;
  color: #059669;
  transform: translateY(-1px);
}

.capsule-plus {
  font-weight: 800;
  color: #059669;
}

.form-input, .form-textarea {
  padding: 0.65rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.15s;
}

.form-input:focus, .form-textarea:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.form-tip {
  font-size: 0.75rem;
  color: #94a3b8;
}

.preset-templates {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.1rem;
  flex-wrap: wrap;
}

.preset-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.preset-btn {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-size: 0.76rem;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s;
}

.preset-btn:hover {
  background: #eef2ff;
  color: #4f46e5;
  border-color: #818cf8;
}

.facts-benchmark-box {
  background: #f0fdf4;
  border: 1.5px solid #86efac;
  border-radius: 10px;
  padding: 1.1rem;
  margin: 1.25rem 0;
  transition: all 0.2s ease;
}

.benchmark-pill {
  font-size: 0.68rem;
  font-weight: 700;
  color: #15803d;
  background: #dcfce7;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  margin-left: 0.5rem;
  border: 1px solid #bbf7d0;
}

.clickable {
  cursor: pointer;
  user-select: none;
}

.toggle-indicator {
  font-size: 0.75rem;
  color: #16a34a;
  font-weight: 700;
}

.facts-intro-tip {
  font-size: 0.78rem;
  color: #166534;
  background: #ffffff;
  border: 1px dashed #86efac;
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  margin-bottom: 0.85rem;
  line-height: 1.5;
}

.agency-settings-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1.1rem;
  margin: 1.25rem 0;
}

.box-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.85rem;
}

.box-title {
  font-size: 0.82rem;
  font-weight: 800;
  color: #334155;
}

.saved-indicator {
  font-size: 0.72rem;
  color: #10b981;
  font-weight: 700;
  background: #ecfdf5;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.btn-submit {
  width: 100%;
  padding: 0.95rem;
  font-size: 1.05rem;
  font-weight: 800;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.35);
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(79, 70, 229, 0.45);
}

.btn-submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Side Column */
.side-col {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

/* Pitch Card */
.pitch-card {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1px solid #fde68a;
  padding: 1.35rem;
}

.pitch-tab-header {
  display: flex;
  gap: 0.5rem;
  border-bottom: 1px solid #fde68a;
  padding-bottom: 0.6rem;
  margin-bottom: 0.85rem;
}

.pitch-tab-btn {
  background: none;
  border: none;
  font-size: 0.82rem;
  font-weight: 800;
  color: #b45309;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
}

.pitch-tab-btn.active {
  background: #f59e0b;
  color: #ffffff;
}

.pitch-tab-body {
  font-size: 0.85rem;
  color: #78350f;
  line-height: 1.7;
}

.pitch-list {
  padding-left: 1.2rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

/* History Card */
.history-card {
  flex: 1;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.history-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.history-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.history-count {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.history-header-right {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.scroll-tip-tag {
  font-size: 0.7rem;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.btn-clear {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.btn-clear:hover {
  background: rgba(239, 68, 68, 0.16);
  border-color: #ef4444;
  transform: translateY(-1px);
}

.btn-refresh {
  background: none;
  border: none;
  font-size: 0.8rem;
  color: #6366f1;
  cursor: pointer;
  font-weight: 700;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  max-height: 380px;
  overflow-y: auto;
  padding-right: 0.35rem;
}

.history-list::-webkit-scrollbar {
  width: 5px;
}

.history-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.history-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.history-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.history-item {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.65rem 0.75rem;
  background: #f8fafc;
  transition: all 0.15s;
}

.history-item:hover {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.history-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.h-company {
  font-size: 0.88rem;
  font-weight: 800;
  color: #0f172a;
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.h-score {
  font-size: 0.85rem;
  font-weight: 900;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
}

.score-danger { background: #fee2e2; color: #b91c1c; }
.score-warn { background: #fef3c7; color: #b45309; }
.score-ok { background: #dcfce7; color: #15803d; }

.history-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #64748b;
}

.h-actions {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.btn-copy-sm {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  font-size: 0.72rem;
  color: #475569;
  padding: 0.15rem 0.45rem;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-copy-sm:hover {
  background: #e0e7ff;
  color: #4338ca;
  border-color: #a5b4fc;
}

.h-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 700;
}

.history-empty {
  font-size: 0.85rem;
  color: #94a3b8;
  text-align: center;
  padding: 2.5rem 0;
}

/* Radar Animation Backdrop */
.radar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.radar-box {
  text-align: center;
  color: #ffffff;
  max-width: 520px;
  width: 90%;
  padding: 2rem;
}

.radar-scanner-wrap {
  position: relative;
  width: 110px;
  height: 110px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-scanner-halo {
  position: absolute;
  inset: -14px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.35) 0%, rgba(16, 185, 129, 0) 70%);
  animation: pulseHalo 2.2s ease-in-out infinite alternate;
  pointer-events: none;
}

.radar-scanner {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 3px solid rgba(16, 185, 129, 0.2);
  border-top-color: #10b981;
  border-right-color: #34d399;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.25);
  animation: spin 1.4s linear infinite;
}

.radar-center-logo {
  width: 70px;
  height: 70px;
  object-fit: contain;
  z-index: 2;
  filter: drop-shadow(0 0 14px rgba(16, 185, 129, 0.5));
  animation: pulseLogo 2s ease-in-out infinite alternate;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulseLogo {
  0% {
    transform: scale(0.95);
    filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.4));
  }
  100% {
    transform: scale(1.05);
    filter: drop-shadow(0 0 24px rgba(16, 185, 129, 0.85));
  }
}

@keyframes pulseHalo {
  0% {
    transform: scale(0.88);
    opacity: 0.35;
  }
  100% {
    transform: scale(1.18);
    opacity: 0.85;
  }
}

.radar-title {
  font-size: 1.6rem;
  font-weight: 900;
  letter-spacing: -0.5px;
}

.radar-sub {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-top: 0.4rem;
}

.radar-timer {
  font-size: 0.82rem;
  color: #cbd5e1;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.4);
  padding: 0.35rem 0.95rem;
  border-radius: 999px;
  margin: 1rem auto 1.5rem;
  display: inline-block;
  font-weight: 600;
}

/* 5 步递进式流水线 */
.radar-pipeline {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  text-align: left;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(51, 65, 85, 0.8);
  border-radius: 12px;
  padding: 1.1rem;
}

.pipeline-step {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
  transition: all 0.25s ease;
}

.step-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
  flex-shrink: 0;
}

.step-done {
  color: #34d399;
}
.step-done .step-icon {
  background: #065f46;
  color: #34d399;
}

.step-active {
  color: #ffffff;
  font-weight: 700;
}
.step-active .step-icon {
  background: #4f46e5;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.8);
}

.step-waiting {
  color: #64748b;
}
.step-waiting .step-icon {
  background: #1e293b;
  color: #64748b;
  border: 1px solid #334155;
}

.step-spinner {
  animation: pulse 1s infinite alternate;
}

@keyframes pulse {
  from { opacity: 0.6; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1.1); }
}

/* ==========================================================================
   诊断算力燃料池 · 沉浸式弹窗 (Modal) 与状态按钮样式
   ========================================================================== */
.fuel-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(15, 23, 42, 0.78);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  animation: modalFadeIn 0.2s ease-out;
}

@keyframes modalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fuel-modal-window {
  max-width: 1260px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  background: linear-gradient(135deg, #0b1120 0%, #111827 100%);
  border: 1px solid rgba(99, 102, 241, 0.35);
  border-radius: 18px;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 40px rgba(99, 102, 241, 0.15);
  color: #ffffff;
  animation: modalScaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalScaleUp {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.fuel-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.fmodal-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.fmodal-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.fmodal-tag {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #34d399;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 9999px;
}

.fmodal-sub-tag {
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.35);
  color: #a5b4fc;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 9999px;
}

.fmodal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-close-fmodal {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-close-fmodal:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border-color: rgba(239, 68, 68, 0.4);
}

.fuel-modal-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 0.75rem 1rem;
  border-radius: 10px;
  margin-bottom: 1.25rem;
}

.toolbar-left, .toolbar-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.btn-privacy-toggle {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  background: #1e293b;
  border: 1px solid rgba(99, 102, 241, 0.35);
  border-radius: 8px;
  color: #cbd5e1;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-privacy-toggle:hover {
  border-color: #818cf8;
  color: #ffffff;
}

.btn-privacy-toggle.active {
  background: rgba(245, 158, 11, 0.18);
  border-color: #f59e0b;
  color: #fbbf24;
}

.fuel-modal-body {
  margin-bottom: 1.25rem;
}

.fuel-modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 1rem;
}

.fmodal-tip {
  font-size: 0.78rem;
  color: #94a3b8;
  line-height: 1.5;
}

.fmodal-tip strong {
  color: #e2e8f0;
}

.btn-fmodal-close {
  padding: 0.45rem 1.25rem;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-fmodal-close:hover {
  background: #334155;
  border-color: #818cf8;
}

.dot-warning {
  background-color: #f59e0b !important;
  box-shadow: 0 0 8px #f59e0b !important;
}

.balance-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.15rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.balance-title-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.balance-badge-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.35);
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #34d399;
  letter-spacing: 0.5px;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: pulseDot 1.6s infinite;
}

@keyframes pulseDot {
  0% { transform: scale(0.9); opacity: 0.6; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.6; }
}

.balance-title {
  margin: 0;
  font-size: 1.08rem;
  font-weight: 800;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 6px;
}

.balance-meta-group {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.total-balance-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 4px 12px;
  border-radius: 8px;
}

.total-balance-pill .total-label {
  font-size: 0.75rem;
  color: #94a3b8;
}

.total-balance-pill .total-amount {
  font-family: ui-monospace, SFMono-Regular, "SF Pro Display", Menlo, monospace;
  font-size: 1.05rem;
  font-weight: 800;
  color: #4CD964;
  letter-spacing: 0.5px;
}

.balance-update-time {
  font-size: 0.75rem;
  color: #8E8E93;
}

.btn-refresh-balance {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #cbd5e1;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-refresh-balance:hover:not(:disabled) {
  background: #334155;
  color: #ffffff;
  border-color: #6366f1;
}

.btn-refresh-balance:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-refresh-balance.is-refreshing .refresh-icon {
  animation: spinIcon 1s linear infinite;
}

@keyframes spinIcon {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 6 大模型卡片网格 */
.balance-cards-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 0.65rem;
}

@media (max-width: 1280px) {
  .balance-cards-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
  }
}

@media (max-width: 768px) {
  .balance-cards-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.65rem;
  }
  .fuel-modal-window {
    padding: 1rem;
    max-height: 95vh;
  }
  .fuel-modal-toolbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .balance-cards-grid {
    grid-template-columns: 1fr;
  }
}

/* 单个模型卡片 (Apple Scriptable Widget 风格) */
.balance-card {
  min-width: 0;
  background: #151d2c;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 12px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  transition: all 0.2s ease;
}

.balance-card:hover {
  transform: translateY(-2px);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.6rem;
}

.model-info {
  display: flex;
  align-items: center;
  gap: 6px;
  overflow: hidden;
}

.model-icon {
  font-size: 1.25rem;
  line-height: 1;
  flex-shrink: 0;
}

.model-text {
  min-width: 0;
}

.model-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.model-cat {
  font-size: 0.68rem;
  color: #8E8E93;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 1px;
}

.status-indicator {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-indicator.active,
.status-indicator.normal {
  color: #4CD964;
  background: rgba(76, 217, 100, 0.12);
  border: 1px solid rgba(76, 217, 100, 0.25);
}

.status-indicator.warning {
  color: #FFCC00;
  background: rgba(255, 204, 0, 0.12);
  border: 1px solid rgba(255, 204, 0, 0.25);
}

.status-indicator.error {
  color: #FF3B30;
  background: rgba(255, 59, 48, 0.12);
  border: 1px solid rgba(255, 59, 48, 0.25);
}

/* 余额显示区域 */
.card-balance-box {
  background: rgba(0, 0, 0, 0.22);
  border-radius: 8px;
  padding: 0.6rem 0.65rem;
  margin-bottom: 0.65rem;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.balance-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 3px;
}

.balance-label-row .sub-label {
  font-size: 0.65rem;
  color: #8E8E93;
}

.tag-live {
  font-size: 0.6rem;
  color: #34d399;
  background: rgba(16, 185, 129, 0.15);
  padding: 1px 5px;
  border-radius: 3px;
  font-weight: 600;
}

.tag-cloud {
  font-size: 0.6rem;
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.15);
  padding: 1px 5px;
  border-radius: 3px;
  font-weight: 600;
}

.main-balance {
  font-family: ui-monospace, SFMono-Regular, "SF Pro Display", Menlo, monospace;
  font-size: 1.25rem;
  font-weight: 800;
  color: #e2e8f0;
  margin-bottom: 4px;
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.main-balance.live-number {
  color: #4CD964; /* Apple Scriptable neon green */
  font-size: 1.35rem;
  letter-spacing: -0.5px;
}

.main-balance .currency {
  font-size: 0.85rem;
  font-weight: 600;
  opacity: 0.85;
}

.main-balance .non-live-text {
  font-size: 0.82rem;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* 赠金/充值 Breakdown */
.balance-breakdown {
  font-size: 0.65rem;
  background: rgba(255, 255, 255, 0.03);
  padding: 3px 6px;
  border-radius: 4px;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 3px;
  color: #8E8E93;
  font-size: 0.62rem;
  white-space: nowrap;
}

.breakdown-item .b-val {
  color: #cbd5e1;
  font-family: monospace;
}

.breakdown-item .b-val.highlight {
  color: #FFCC00; /* Apple amber */
  font-weight: 700;
}

.breakdown-item .b-sep {
  color: #475569;
}

.balance-breakdown.note-mode .b-note {
  color: #94a3b8;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 底部秘钥与链接 */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.68rem;
  color: #64748b;
  padding-top: 2px;
}

.key-hint {
  font-family: monospace;
  font-size: 0.62rem;
  color: #8E8E93;
  max-width: 76px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.link-console {
  color: #007AFF; /* Apple blue */
  text-decoration: none;
  font-weight: 600;
  transition: color 0.15s ease;
}

.link-console:hover {
  color: #38bdf8;
  text-decoration: underline;
}

/* 骨架屏占位 */
.skeleton-card {
  min-height: 125px;
  background: #151d2c;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
}

.sk-line {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  animation: skPulse 1.5s ease-in-out infinite alternate;
}

.sk-title { width: 60%; height: 16px; }
.sk-big { width: 80%; height: 26px; }
.sk-sub { width: 90%; height: 12px; }

@keyframes skPulse {
  0% { opacity: 0.3; }
  100% { opacity: 0.7; }
}

/* ==========================================================================
   销售现场“30秒极速促单演示模式”横幅样式
   ========================================================================== */
.fast-demo-banner {
  max-width: 1320px;
  margin: 0 auto 1.5rem auto;
  background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
  border: 1px solid rgba(129, 140, 248, 0.35);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 10px 30px -5px rgba(30, 27, 75, 0.4), 0 4px 12px rgba(0, 0, 0, 0.2);
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

.fast-demo-banner::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 320px;
  height: 100%;
  background: radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.15), transparent 70%);
  pointer-events: none;
}

.demo-banner-content {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 1.5rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.demo-tag-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.demo-badge {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}

.demo-sub-tag {
  background: rgba(255, 255, 255, 0.1);
  color: #c7d2fe;
  font-size: 0.72rem;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.demo-title {
  font-size: 1.28rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.4rem;
  letter-spacing: -0.3px;
}

.demo-desc {
  font-size: 0.82rem;
  color: #94a3b8;
  line-height: 1.45;
  margin-bottom: 0.9rem;
}

.demo-desc strong {
  color: #fbbf24;
}

.demo-cases-pills {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.case-label {
  font-size: 0.75rem;
  color: #a5b4fc;
  font-weight: 600;
}

.demo-case-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #e2e8f0;
  font-size: 0.76rem;
  padding: 0.3rem 0.7rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.demo-case-btn:hover {
  background: rgba(99, 102, 241, 0.25);
  border-color: #818cf8;
  color: #ffffff;
  transform: translateY(-1px);
}

.demo-case-btn.active-case {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
  color: #fca5a5;
}

.case-arrow {
  color: #fbbf24;
  font-weight: 800;
}

/* 右侧闭环卡片 */
.demo-action-card {
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 0.9rem 1.1rem;
  backdrop-filter: blur(10px);
}

.demo-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.6rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.card-head-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #e2e8f0;
  flex: 1;
  margin-left: 0.35rem;
}

.speed-pill {
  background: #10b981;
  color: #ffffff;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.demo-steps-mini {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-bottom: 0.75rem;
}

.mini-step {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  font-size: 0.74rem;
  color: #cbd5e1;
}

.step-idx {
  font-size: 0.68rem;
  font-weight: 700;
  background: rgba(99, 102, 241, 0.25);
  color: #a5b4fc;
  padding: 0.08rem 0.35rem;
  border-radius: 4px;
  white-space: nowrap;
}

.mini-step strong {
  color: #f1f5f9;
}

.btn-launch-demo {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: #ffffff;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
  transition: all 0.2s ease;
}

.btn-launch-demo:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.5);
}

@media (max-width: 900px) {
  .demo-banner-content {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
}

/* -------------------------------------------------------------
   高德地图 POI 智能联想与多门店消歧防呆组件样式
   ------------------------------------------------------------- */
.poi-relative-group {
  position: relative;
}

.poi-shield-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.input-with-poi-wrap {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.poi-loading-spinner {
  position: absolute;
  right: 12px;
  font-size: 0.85rem;
  animation: spin 1.2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.poi-suggestions-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  z-index: 999;
  background: #0f172a;
  border: 1px solid #3b82f6;
  border-radius: 10px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75), 0 0 16px rgba(59, 130, 246, 0.25);
  overflow: hidden;
  max-height: 380px;
  overflow-y: auto;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 0.85rem;
  background: rgba(30, 41, 59, 0.95);
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
  font-size: 0.74rem;
  font-weight: 700;
  color: #93c5fd;
}

.dropdown-count {
  background: rgba(59, 130, 246, 0.25);
  color: #60a5fa;
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
}

.poi-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.7rem 0.85rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: all 0.15s ease;
}

.poi-item:last-child {
  border-bottom: none;
}

.poi-item:hover {
  background: rgba(59, 130, 246, 0.15);
  border-left: 3px solid #3b82f6;
}

.poi-item-main {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.poi-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.poi-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.35);
}

.poi-name {
  font-size: 0.86rem;
  color: #f8fafc;
}

.poi-addr-row {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

.poi-action-col {
  margin-left: 0.75rem;
}

.poi-apply-pill {
  font-size: 0.72rem;
  font-weight: 600;
  color: #60a5fa;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  padding: 0.25rem 0.55rem;
  border-radius: 6px;
  white-space: nowrap;
}

.poi-item:hover .poi-apply-pill {
  background: #3b82f6;
  color: #ffffff;
}

/* -------------------------------------------------------------
   连锁/多门店消歧拦截告警胶囊
   ------------------------------------------------------------- */
.disambiguation-alert-banner {
  display: flex;
  gap: 0.75rem;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(217, 119, 6, 0.08) 100%);
  border: 1.5px solid rgba(245, 158, 11, 0.45);
  border-radius: 10px;
  padding: 0.8rem 1rem;
  margin: 0.75rem 0 1.1rem 0;
  animation: slideInDown 0.25s ease-out;
}

@keyframes slideInDown {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.dis-icon {
  font-size: 1.3rem;
  line-height: 1.2;
}

.dis-body {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
}

.dis-title {
  font-size: 0.84rem;
  font-weight: 700;
  color: #f59e0b;
}

.dis-desc {
  font-size: 0.78rem;
  color: #fef3c7;
  line-height: 1.45;
}

.dis-pills {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.25rem;
}

.dis-pills-label {
  font-size: 0.74rem;
  color: #fbbf24;
  font-weight: 600;
}

.dis-pill-btn {
  background: rgba(245, 158, 11, 0.2);
  border: 1px solid rgba(245, 158, 11, 0.5);
  color: #fffbeb;
  font-size: 0.76rem;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dis-pill-btn:hover {
  background: #f59e0b;
  color: #0f172a;
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(245, 158, 11, 0.4);
}
</style>
