<template>
  <div class="landing-container">
    <!-- 1. 绝对固定顶部导航栏 (Fixed Header) -->
    <header class="landing-header">
      <div class="header-inner">
        <!-- 品牌标识：自然呼吸光晕，无框束缚 -->
        <router-link to="/" class="brand-link" title="蜉蝣小宝 · AI 营销智能大脑">
          <div class="logo-aura-wrap">
            <div class="logo-soft-glow"></div>
            <img src="/logo-white.png" alt="蜉蝣小宝" class="logo-unconstrained" />
          </div>
          <span class="brand-badge-tag">GEO 2.0</span>
        </router-link>

        <nav class="nav-links">
          <!-- 1. 平台中枢 -->
          <div
            class="nav-item-group"
            :class="{ active: activeDropdown === 'platform' }"
            @mouseenter="handleMouseEnter('platform')"
            @mouseleave="handleMouseLeave"
          >
            <button class="nav-btn" @click="toggleDropdown('platform')">
              <span>平台与中枢</span>
              <svg class="nav-caret" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- 平台中枢 Mega Dropdown -->
            <transition name="mega-fade">
              <div v-if="activeDropdown === 'platform'" class="mega-dropdown align-left width-platform">
                <div class="dropdown-item-card" @click="scrollToSection('hero-search')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">GEO-RADAR 决策透视中枢</span>
                      <span class="item-badge blue">v2.6 实时</span>
                    </div>
                    <p class="item-desc">6 大主流基座大模型 24/7 探针直连，实时穿透高频采购推荐顺位与信源采信。</p>
                  </div>
                </div>

                <div class="dropdown-item-card" @click="scrollToSection('market-shift')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">AI 搜索流量断崖迁移洞察</span>
                      <span class="item-badge">趋势数据</span>
                    </div>
                    <p class="item-desc">直观透视采购客户从传统搜索向大模型提问的心智转移，测算商机流失。</p>
                  </div>
                </div>

                <div class="dropdown-item-card" @click="scrollToSection('architecture')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">GEO 认知工程底层架构防线</span>
                      <span class="item-badge blue">核心底层</span>
                    </div>
                    <p class="item-desc">全域知识资产蒸馏、权威证据注入与同业恶意截流三层防御体系。</p>
                  </div>
                </div>

                <div class="dropdown-footer">
                  <span>直连中国 6 大主流基座大模型 · 覆盖国家级权威信源</span>
                  <a href="javascript:void(0)" @click.stop="openLeadModal('nav_platform')">预约现场实测 ➔</a>
                </div>
              </div>
            </transition>
          </div>

          <!-- 2. 行业解决方案 -->
          <div
            class="nav-item-group"
            :class="{ active: activeDropdown === 'solutions' }"
            @mouseenter="handleMouseEnter('solutions')"
            @mouseleave="handleMouseLeave"
          >
            <button class="nav-btn" @click="toggleDropdown('solutions')">
              <span>行业解决方案</span>
              <svg class="nav-caret" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- 行业解决方案 Mega Dropdown -->
            <transition name="mega-fade">
              <div v-if="activeDropdown === 'solutions'" class="mega-dropdown align-center width-solutions">
                <div class="dropdown-grid-two">
                  <div class="dropdown-item-card" @click="handleNavIndustry(0)">
                    <div class="item-icon-box">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
                      </svg>
                    </div>
                    <div class="item-text-wrap">
                      <div class="item-title-row">
                        <span class="item-title">工业制造与切管机</span>
                        <span class="item-badge">无锡恒瑞</span>
                      </div>
                      <p class="item-desc">重型激光切管机精密选型，有效拦截同业快招截流</p>
                    </div>
                  </div>

                  <div class="dropdown-item-card" @click="handleNavIndustry(1)">
                    <div class="item-icon-box">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
                      </svg>
                    </div>
                    <div class="item-text-wrap">
                      <div class="item-title-row">
                        <span class="item-title">高端系统门窗定制</span>
                        <span class="item-badge">欧罗德门窗</span>
                      </div>
                      <p class="item-desc">断桥铝隔音隔热性能证据链，大宅别墅首选第一推荐</p>
                    </div>
                  </div>

                  <div class="dropdown-item-card" @click="handleNavIndustry(2)">
                    <div class="item-icon-box">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>
                      </svg>
                    </div>
                    <div class="item-text-wrap">
                      <div class="item-title-row">
                        <span class="item-title">餐饮连锁招商加盟</span>
                        <span class="item-badge">老乡鸡加盟</span>
                      </div>
                      <p class="item-desc">万店连锁标准化供应链，化解虚假快招信息拦截</p>
                    </div>
                  </div>

                  <div class="dropdown-item-card" @click="handleNavIndustry(3)">
                    <div class="item-icon-box">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                      </svg>
                    </div>
                    <div class="item-text-wrap">
                      <div class="item-title-row">
                        <span class="item-title">数字化专科医疗</span>
                        <span class="item-badge">瑞尔齿科</span>
                      </div>
                      <p class="item-desc">数字化正畸与种植专科，国家权威学术信源背书</p>
                    </div>
                  </div>

                  <div class="dropdown-item-card span-two" @click="handleNavIndustry(4)">
                    <div class="item-icon-box">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                      </svg>
                    </div>
                    <div class="item-text-wrap">
                      <div class="item-title-row">
                        <span class="item-title">商事争议与常年法务</span>
                        <span class="item-badge">君泽君律所</span>
                      </div>
                      <p class="item-desc">涉税合规民商争议仲裁第一梯队，民商裁判文书权威采信引用</p>
                    </div>
                  </div>
                </div>

                <div class="dropdown-footer">
                  <span>点击任意行业，首屏雷达控制台将自动同步联动切换实测数据</span>
                  <a href="javascript:void(0)" @click.stop="scrollToSection('solutions')">查看全部行业方案 ➔</a>
                </div>
              </div>
            </transition>
          </div>

          <!-- 3. 商业价值与交付 -->
          <div
            class="nav-item-group"
            :class="{ active: activeDropdown === 'delivery' }"
            @mouseenter="handleMouseEnter('delivery')"
            @mouseleave="handleMouseLeave"
          >
            <button class="nav-btn" @click="toggleDropdown('delivery')">
              <span>商业价值与交付</span>
              <svg class="nav-caret" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- 交付与价值 Mega Dropdown -->
            <transition name="mega-fade">
              <div v-if="activeDropdown === 'delivery'" class="mega-dropdown align-center width-delivery">
                <div class="dropdown-item-card" @click="scrollToSection('roadmap')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">30 天标准化交付路线图</span>
                      <span class="item-badge">4阶段保障</span>
                    </div>
                    <p class="item-desc">现状深度体检 ➔ 权威证据蒸馏 ➔ 知识图谱注入 ➔ 首推霸榜防御，清晰可控。</p>
                  </div>
                </div>

                <div class="dropdown-item-card" @click="scrollToSection('roi')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">企业获客成本对比账本</span>
                      <span class="item-badge blue">降本 80%+</span>
                    </div>
                    <p class="item-desc">对比传统高昂竞价单价，GEO 建立长期数字认知资产，边际获客成本大幅降低。</p>
                  </div>
                </div>

                <div class="dropdown-footer">
                  <span>提供 30 天首推达标承诺，专属行业顾问一对一跟踪进度</span>
                  <a href="javascript:void(0)" @click.stop="openLeadModal('nav_delivery')">获取定制排期表 ➔</a>
                </div>
              </div>
            </transition>
          </div>

          <!-- 4. 资源与保障 -->
          <div
            class="nav-item-group"
            :class="{ active: activeDropdown === 'trust' }"
            @mouseenter="handleMouseEnter('trust')"
            @mouseleave="handleMouseLeave"
          >
            <button class="nav-btn" @click="toggleDropdown('trust')">
              <span>资源与保障</span>
              <svg class="nav-caret" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- 资源与保障 Mega Dropdown -->
            <transition name="mega-fade">
              <div v-if="activeDropdown === 'trust'" class="mega-dropdown align-right width-trust">
                <div class="dropdown-item-card" @click="scrollToSection('faq')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">核心常见问答 (FAQ)</span>
                      <span class="item-badge">常见关切</span>
                    </div>
                    <p class="item-desc">基座大模型推荐机制、知识注入周期、品牌长效防御与合规答疑。</p>
                  </div>
                </div>

                <div class="dropdown-item-card" @click="openLeadModal('nav_security')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">商业数据安全与保密承诺</span>
                      <span class="item-badge blue">严格签署 NDA</span>
                    </div>
                    <p class="item-desc">严格遵循企业保密协议，所有诊断数据绝不向任何第三方公开透露。</p>
                  </div>
                </div>

                <div class="dropdown-item-card" @click="openLeadModal('nav_hotline')">
                  <div class="item-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                    </svg>
                  </div>
                  <div class="item-text-wrap">
                    <div class="item-title-row">
                      <span class="item-title">官方顾问咨询热线</span>
                      <span class="item-badge">400-800-2026</span>
                    </div>
                    <p class="item-desc">工作日 09:00 - 20:00 资深顾问在线响应，提供快速排期咨询。</p>
                  </div>
                </div>

                <div class="dropdown-footer">
                  <span>如需为集团或上市企业进行私密现场演示，可直接预约顾问</span>
                  <a href="javascript:void(0)" @click.stop="openLeadModal('nav_trust')">预约专属顾问 ➔</a>
                </div>
              </div>
            </transition>
          </div>
        </nav>

        <!-- 顶部操作区 (已移除标杆报告和工作台两个对外按钮) -->
        <div class="header-actions">
          <button class="btn-primary-nav" @click="openLeadModal('header')">
            <span class="btn-glow-bg"></span>
            <span class="btn-text">预约企业体检</span>
            <svg class="btn-svg-arrow" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- 2. 首屏暗黑深空区 (Hero Section - 方案 A：中央搜索 + 智能雷达交互中枢大屏 + 底端全宽跑马灯) -->
    <section class="hero-section">
      <!-- 动态深空背景光晕 -->
      <div class="ambient-glow orb-blue"></div>
      <div class="ambient-glow orb-purple"></div>
      <div class="grid-overlay"></div>

      <!-- 首屏核心内容区 (居中限制 1320px，饱满充实) -->
      <div class="section-inner hero-inner">
        <!-- 极简大气主标题 (已移除顶部白皮书胶囊) -->
        <h1 class="hero-headline">
          当 5 亿客户向 AI 提问<br />
          让您的品牌成为 <span class="text-gradient">第一推荐</span>
        </h1>

        <!-- 精炼副标题 -->
        <p class="hero-subtext">
          穿透豆包、DeepSeek、通义千问等主流大模型推荐决策层<br />
          测算潜在客源流失 · 构建专属于企业的权威知识资产护城河
        </p>

        <!-- Similarweb 风格交互式搜索框 -->
        <div id="hero-search" class="hero-search-wrapper">
          <div class="search-input-box">
            <div class="search-mode-select">
              <svg class="mode-svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4zm3 1h6v4H7V5zm8 8v2h1v-2h-1zm-2-2H7v4h6v-4zm2 0h1V9h-1v2zm1-4V5h-1v2h1zM5 5v2H4V5h1zm0 4h1v2H4V9zm1 4H4v2h1v-2z" clip-rule="evenodd" />
              </svg>
              <span class="mode-label">品牌全网诊断</span>
              <svg class="mode-caret-svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
            
            <div class="search-divider"></div>

            <div class="search-input-field">
              <input
                type="text"
                v-model="heroBrandInput"
                :placeholder="currentPlaceholder"
                @keyup.enter="handleHeroSubmit"
              />
            </div>

            <button class="btn-search-action" @click="handleHeroSubmit">
              <span class="action-glow"></span>
              <span class="action-content">
                <svg class="action-svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                </svg>
                <span class="action-label">立即透视</span>
              </span>
            </button>
          </div>

          <!-- 精炼标杆 Chips (与下方看板实时联动) -->
          <div class="quick-chips-row">
            <span class="chips-label">标杆行业实时案例：</span>
            <button
              v-for="(caseItem, cIdx) in consoleCases"
              :key="cIdx"
              class="chip-btn"
              :class="{ active: activeConsoleTab === cIdx }"
              @click="selectCase(cIdx)"
            >
              <span class="chip-dot"></span>
              <span class="chip-text">{{ caseItem.chipLabel }}</span>
            </button>
          </div>
        </div>

        <!-- ================= 方案 A 智能雷达交互中枢看板 (带 360° 全边框环绕流光) ================= -->
        <div class="hero-console-showcase">
          <!-- 360° 全周径全边框环绕流光 (Border Beam) -->
          <div class="console-border-beam" aria-hidden="true"></div>

          <!-- 内部悬浮环境流光光晕 -->
          <div class="console-streaming-glow"></div>

          <!-- 看板顶部门户状态条 -->
          <div class="console-top-bar">
            <div class="bar-left">
              <div class="traffic-lights">
                <span class="light red"></span>
                <span class="light yellow"></span>
                <span class="light green"></span>
              </div>
              <span class="console-title">GEO-RADAR v2.6 · 实时决策透视中枢</span>
              <span class="console-version-pill">LIVE RADAR</span>
            </div>
            <div class="bar-right">
              <div class="probe-live-indicator">
                <span class="pulse-ring"></span>
                <span class="pulse-core"></span>
                <span>6 大主流基座大模型 24/7 探针直连中</span>
              </div>
              <div class="active-sample-tag">
                <span class="sample-label">实时透视标杆：</span>
                <span class="sample-val">{{ currentCase.brandName }}</span>
              </div>
            </div>
          </div>

          <!-- 看板三栏式主体架构 -->
          <div class="console-body-grid">
            <!-- 第 1 栏：6 大基座大模型实时直连探针 -->
            <div class="console-col col-probes">
              <div class="col-head">
                <div class="col-head-title">
                  <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M12 3a9 9 0 0 1 9 9"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <span>基座大模型双端决策探针</span>
                </div>
                <span class="status-chip-live">实时召回率</span>
              </div>

              <div class="probes-list">
                <div
                  v-for="(model, mIdx) in currentCase.modelStats"
                  :key="mIdx"
                  class="probe-model-row"
                >
                  <div class="model-avatar" v-html="model.svg"></div>
                  <div class="model-info">
                    <div class="model-name-row">
                      <span class="m-name">{{ model.name }}</span>
                      <span class="m-ping">{{ model.latency }}</span>
                    </div>
                    <div class="model-track-row">
                      <div class="m-track">
                        <div class="m-fill" :style="{ width: model.score, background: model.color }"></div>
                      </div>
                      <span class="m-score" :style="{ color: model.color }">{{ model.score }}</span>
                    </div>
                  </div>
                  <span class="model-verdict-pill">{{ model.status }}</span>
                </div>
              </div>
            </div>

            <!-- 第 2 栏：AI 真实回答生成与第一推荐位流式呈现 -->
            <div class="console-col col-simulation">
              <div class="col-head">
                <div class="col-head-title">
                  <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                  </svg>
                  <span>大模型首选推荐决策生成</span>
                </div>
                <span class="status-chip-ai">客观采信</span>
              </div>

              <!-- 客户提问 Prompt 气泡 -->
              <div class="sim-prompt-box">
                <div class="prompt-speaker-bar">
                  <svg class="user-svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                  <span>采购决策者高频检索 Prompt：</span>
                </div>
                <p class="prompt-text">“{{ currentCase.queryPrompt }}”</p>
              </div>

              <!-- AI 大模型推荐答案卡片 -->
              <div class="sim-answer-card">
                <div class="answer-header-badge">
                  <div class="answer-left">
                    <span class="badge-rec-crown">
                      <svg viewBox="0 0 20 20" fill="currentColor">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    </span>
                    <span class="answer-rec-target">首推品牌：<strong>{{ currentCase.brandName }}</strong></span>
                  </div>
                  <span class="cert-pill">权威实体已确权</span>
                </div>
                <p class="answer-body-text">{{ currentCase.aiVerdict }}</p>
                
                <div class="interception-defense-banner">
                  <svg class="shield-svg" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  </svg>
                  <span>竞品截流防御：已成功拦截同业快招恶意诱导</span>
                </div>
              </div>
            </div>

            <!-- 第 3 栏：全网可见度雷达指数与公域确权资产 -->
            <div class="console-col col-metrics">
              <div class="col-head">
                <div class="col-head-title">
                  <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2">
                    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
                    <polyline points="16 7 22 7 22 13"></polyline>
                  </svg>
                  <span>GEO 全域知识资产健康度</span>
                </div>
                <span class="status-chip-score">综合评级：S 级</span>
              </div>

              <!-- 综合得分大指标卡片 -->
              <div class="metric-score-card">
                <div class="score-main">
                  <span class="score-number">{{ currentCase.overallScore }}</span>
                  <div class="score-meta">
                    <span class="score-label">全网 AI 可见度指数</span>
                    <span class="score-sub">远超行业 92% 竞争对手</span>
                  </div>
                </div>
                
                <div class="metrics-two-col">
                  <div class="metric-sub-item">
                    <span class="sub-lbl">竞品截流拦截率</span>
                    <span class="sub-val text-green">{{ currentCase.defenseRate }}</span>
                  </div>
                  <div class="metric-sub-item">
                    <span class="sub-lbl">商机边际成本</span>
                    <span class="sub-val text-brand">{{ currentCase.costReduction }}</span>
                  </div>
                </div>
              </div>

              <!-- 权威信源确权网格 -->
              <div class="sources-mesh-box">
                <span class="sources-title">大模型核心底层采信证据：</span>
                <div class="sources-grid">
                  <div
                    v-for="(src, sIdx) in currentCase.sources"
                    :key="sIdx"
                    class="source-node-pill"
                  >
                    <span class="node-dot"></span>
                    <span class="node-text">{{ src }}</span>
                  </div>
                </div>
              </div>

              <!-- 预约专家 1v1 演示 CTA 按钮 -->
              <button
                class="btn-console-explore"
                @click="openLeadModal('console_case', currentCase.brandName, currentCase.chipLabel)"
              >
                <span>预约该标杆案例专家演示</span>
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 首屏全宽跑马灯 (脱离 1280px 限制，贯穿全屏左右 100% 视口边缘) -->
      <div class="hero-trust-marquee-container">
        <div class="trust-marquee-header">
          <span class="trust-line"></span>
          <span class="trust-title-text">直连中国主流基座大模型 · 覆盖国家级及高权重权威信源生态</span>
          <span class="trust-line"></span>
        </div>

        <div class="trust-marquee-track-wrap">
          <div class="trust-marquee-track">
            <!-- 复制 3 组，确保在 4K/2K/超宽显示器下持续平滑无缝滚动 -->
            <div
              v-for="(brand, bIdx) in trustBrands"
              :key="'t1-' + bIdx"
              class="trust-brand-item"
            >
              <div class="brand-svg-symbol" v-html="brand.svg"></div>
              <div class="brand-meta">
                <span class="brand-title">{{ brand.name }}</span>
                <span class="brand-role">{{ brand.role }}</span>
              </div>
              <div class="brand-live-pulse" title="24/7 直连运行中"></div>
            </div>
            <div
              v-for="(brand, bIdx) in trustBrands"
              :key="'t2-' + bIdx"
              class="trust-brand-item"
            >
              <div class="brand-svg-symbol" v-html="brand.svg"></div>
              <div class="brand-meta">
                <span class="brand-title">{{ brand.name }}</span>
                <span class="brand-role">{{ brand.role }}</span>
              </div>
              <div class="brand-live-pulse" title="24/7 直连运行中"></div>
            </div>
            <div
              v-for="(brand, bIdx) in trustBrands"
              :key="'t3-' + bIdx"
              class="trust-brand-item"
            >
              <div class="brand-svg-symbol" v-html="brand.svg"></div>
              <div class="brand-meta">
                <span class="brand-title">{{ brand.name }}</span>
                <span class="brand-role">{{ brand.role }}</span>
              </div>
              <div class="brand-live-pulse" title="24/7 直连运行中"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. 白色/浅色清爽区域：流量转移趋势与简约数据图表 (切换为白底，消除疲劳，支持滑动渐显渐隐) -->
    <section id="market-shift" class="light-section-contrast">
      <div class="section-inner">
        <div class="section-header-center scroll-reveal">
          <span class="light-badge">行业格局演进 · PARADIGM SHIFT</span>
          <h2 class="light-title">
            从“网页点击”到“AI 推荐答案”：<br />
            不可逆转的 <span class="text-gradient-blue">流量转移与认知洗牌</span>
          </h2>
          <p class="light-sub">
            传统搜索链接点击率下滑 34%，而大模型对话式采购决策咨询暴涨 420%。客户向 AI 要的是确凿的选型建议，而不是一页翻不完的广告链接。
          </p>
        </div>

        <!-- 简约数据图表 1：AI 对话推荐意图爆发 VS 传统搜索有效点击 (SVG 极简趋势图) -->
        <div class="data-chart-card scroll-reveal delay-1">
          <div class="chart-card-header">
            <div class="chart-header-left">
              <h3 class="chart-title">2023 - 2026 全网采购决策与流量演化图谱</h3>
              <span class="chart-sub-note">基于 500+ 万次 B2B 制造、大宅定制、现代消费真实搜索与推荐样本测算</span>
            </div>
            <div class="chart-legend-group">
              <div class="legend-item">
                <span class="legend-line line-cyan"></span>
                <span>AI 大模型生成式推荐召回率 (+420%)</span>
              </div>
              <div class="legend-item">
                <span class="legend-line line-gray"></span>
                <span>传统搜索有效商机点击率 (-34%)</span>
              </div>
            </div>
          </div>

          <!-- SVG 简约折线/面积图表 -->
          <div class="svg-chart-container">
            <svg class="trend-chart-svg" viewBox="0 0 1000 320" preserveAspectRatio="none">
              <defs>
                <linearGradient id="cyanArea" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#0284C7" stop-opacity="0.25" />
                  <stop offset="100%" stop-color="#0284C7" stop-opacity="0.0" />
                </linearGradient>
                <linearGradient id="cyanLine" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#38BDF8" />
                  <stop offset="50%" stop-color="#2563EB" />
                  <stop offset="100%" stop-color="#7C3AED" />
                </linearGradient>
              </defs>

              <!-- 刻度参考背景线 -->
              <line x1="60" y1="50" x2="960" y2="50" stroke="#E2E8F0" stroke-dasharray="4 4" />
              <line x1="60" y1="120" x2="960" y2="120" stroke="#E2E8F0" stroke-dasharray="4 4" />
              <line x1="60" y1="190" x2="960" y2="190" stroke="#E2E8F0" stroke-dasharray="4 4" />
              <line x1="60" y1="260" x2="960" y2="260" stroke="#CBD5E1" stroke-width="1.5" />

              <!-- 面积渐变 -->
              <path d="M 60,240 C 260,230 460,190 660,105 C 800,45 960,30 960,30 L 960,260 L 60,260 Z" fill="url(#cyanArea)" />

              <!-- 传统搜索下跌线 (灰折线) -->
              <path d="M 60,70 C 260,85 460,120 660,175 C 800,215 960,245 960,245" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-dasharray="6 4" />

              <!-- AI 搜索暴涨曲线 (高饱和渐变实线) -->
              <path d="M 60,240 C 260,230 460,190 660,105 C 800,45 960,30 960,30" fill="none" stroke="url(#cyanLine)" stroke-width="4" />

              <!-- 数据标点 -->
              <circle cx="60" cy="240" r="5" fill="#0284C7" stroke="#ffffff" stroke-width="2.5" />
              <circle cx="660" cy="105" r="5" fill="#2563EB" stroke="#ffffff" stroke-width="2.5" />
              <circle cx="960" cy="30" r="7" fill="#7C3AED" stroke="#ffffff" stroke-width="3" />
            </svg>

            <!-- X 轴刻度文本 -->
            <div class="chart-x-axis">
              <span>2023 Q1 (传统搜索全盛)</span>
              <span>2024 Q2 (大模型多点开花)</span>
              <span>2025 Q3 (AI 对话成为主要决策入口)</span>
              <span class="highlight-axis">2026 当前 (GEO 全域知识确权节点)</span>
            </div>
          </div>
        </div>

        <!-- 范式转移 4 阶段对比滑块 (浅色高雅质感) -->
        <div class="light-shift-slider scroll-reveal delay-2">
          <div class="light-slider-tabs">
            <button
              v-for="(slide, sIdx) in shiftSlides"
              :key="sIdx"
              class="light-tab-btn"
              :class="{ active: currentSlideIndex === sIdx }"
              @click="switchSlide(sIdx)"
            >
              <div class="light-tab-progress">
                <div
                  class="light-progress-bar"
                  :style="{ width: currentSlideIndex === sIdx ? `${slideProgress}%` : (currentSlideIndex > sIdx ? '100%' : '0%') }"
                ></div>
              </div>
              <div class="light-tab-meta">
                <span class="tab-idx">0{{ sIdx + 1 }}</span>
                <span class="tab-txt">{{ slide.shortTitle }}</span>
              </div>
            </button>
          </div>

          <div class="light-slider-content">
            <div class="slide-left">
              <span class="slide-tag-pill">{{ currentSlide.tag }}</span>
              <h3 class="slide-title-clean">{{ currentSlide.headline }}</h3>
              <p class="slide-desc-clean">{{ currentSlide.description }}</p>

              <div class="slide-bullets">
                <div class="bullet-row" v-for="(p, pIdx) in currentSlide.points" :key="pIdx">
                  <svg class="bullet-check-svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                  <span>{{ p }}</span>
                </div>
              </div>
            </div>

            <div class="slide-right">
              <div class="slide-stat-panel">
                <div class="stat-highlight-box">
                  <div class="stat-big-num">{{ currentSlide.metricNum }}</div>
                  <div class="stat-big-lbl">{{ currentSlide.metricLabel }}</div>
                </div>

                <div class="stat-compare-table">
                  <div class="compare-col old-way">
                    <span class="col-head">传统搜索 (SEO/竞价)</span>
                    <span class="col-val">{{ currentSlide.oldStat }}</span>
                  </div>
                  <div class="compare-divider"></div>
                  <div class="compare-col new-way">
                    <span class="col-head">GEO 生成式引擎优化</span>
                    <span class="col-val text-brand">{{ currentSlide.newStat }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. 白色/浅色区域：行业落地场景解决方案 (优雅白底，消除疲劳，支持滑动渐显渐隐) -->
    <section id="solutions" class="light-solutions-section">
      <div class="section-inner">
        <div class="section-header-center scroll-reveal">
          <span class="light-badge">行业落地矩阵 · VERTICAL BLUEPRINTS</span>
          <h2 class="light-title">
            懂中国产业痛点，更懂主流基座大模型的 <span class="text-gradient-blue">真实推荐法则</span>
          </h2>
          <p class="light-sub">
            针对不同垂直行业的重决策属性，定制知识本体图谱与权威信源协同注入方案。
          </p>
        </div>

        <!-- 行业选择导航 (无 emoji，纯矢量高定图标) -->
        <div class="light-industry-nav scroll-reveal delay-1">
          <button
            v-for="(ind, iIdx) in industries"
            :key="ind.id"
            class="ind-nav-btn"
            :class="{ active: activeIndustryIndex === iIdx }"
            @click="activeIndustryIndex = iIdx"
          >
            <div class="ind-nav-icon" v-html="ind.svg"></div>
            <span class="ind-nav-title">{{ ind.name }}</span>
          </button>
        </div>

        <!-- 行业解法主卡片 (白底高对比度，配备极简对比进度条) -->
        <div class="light-solution-card scroll-reveal delay-2">
          <div class="sol-card-header">
            <div class="sol-header-left">
              <span class="sol-category-badge">{{ currentIndustry.category }}</span>
              <h3 class="sol-headline">{{ currentIndustry.headline }}</h3>
            </div>
            <div class="sol-header-right">
              <button
                class="btn-ind-try"
                @click="openLeadModal('industry', currentIndustry.defaultBrand, currentIndustry.category)"
              >
                <span>预约该行业现场实测演示</span>
                <svg class="btn-arrow" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <div class="sol-grid-layout">
            <!-- 客户真实提问提炼 -->
            <div class="sol-col-prompt">
              <div class="col-title-bar">
                <svg class="bar-svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
                </svg>
                <span>5 亿用户高频 Prompt 选型提问</span>
              </div>
              <div class="prompt-speech-bubble">
                <p>“{{ currentIndustry.samplePrompt }}”</p>
              </div>

              <!-- 30天关键攻坚战法 -->
              <div class="tactics-list">
                <div class="tactic-item" v-for="(t, tIdx) in currentIndustry.tactics" :key="tIdx">
                  <div class="tactic-num">{{ tIdx + 1 }}</div>
                  <div class="tactic-info">
                    <div class="tactic-t">{{ t.title }}</div>
                    <div class="tactic-d">{{ t.desc }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 数据可视化对比卡片 (极简进度条，替代繁复插画) -->
            <div class="sol-col-stats">
              <div class="stat-box-clean">
                <span class="box-tag">优化 30 天实测指标对比</span>
                <div class="stat-progress-group">
                  <div class="prog-item">
                    <div class="prog-label-row">
                      <span>品牌正向首推覆盖率</span>
                      <span class="prog-num font-bold text-blue">{{ currentIndustry.stats.rate }}</span>
                    </div>
                    <div class="prog-track">
                      <div class="prog-fill fill-blue" :style="{ width: currentIndustry.stats.rate }"></div>
                    </div>
                  </div>

                  <div class="prog-item">
                    <div class="prog-label-row">
                      <span>竞品恶意截流拦截率</span>
                      <span class="prog-num font-bold text-green">{{ currentIndustry.stats.retention }}</span>
                    </div>
                    <div class="prog-track">
                      <div class="prog-fill fill-green" :style="{ width: currentIndustry.stats.retention }"></div>
                    </div>
                  </div>

                  <div class="prog-item">
                    <div class="prog-label-row">
                      <span>单次精准获客边际成本降幅</span>
                      <span class="prog-num font-bold text-purple">{{ currentIndustry.stats.costSaving }}</span>
                    </div>
                    <div class="prog-track">
                      <div class="prog-fill fill-purple" :style="{ width: currentIndustry.stats.costSaving }"></div>
                    </div>
                  </div>
                </div>

                <div class="verified-source-row">
                  <span class="source-tag">核心采信来源：</span>
                  <span class="source-items">{{ currentIndustry.stats.sources }}</span>
                </div>

                <div class="client-quote">
                  <svg class="quote-svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
                  </svg>
                  <p class="quote-text">{{ currentIndustry.testimonial }}</p>
                  <span class="quote-author">{{ currentIndustry.author }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. 深色区域：AI 认知工程架构 (深色矩阵科技感，支持滑动渐显渐隐) -->
    <section id="architecture" class="dark-tech-section">
      <div class="tech-glow-top"></div>
      <div class="section-inner">
        <div class="section-header-center scroll-reveal">
          <span class="tech-badge">底层科技支撑 · GEO COGNITIVE ENGINE</span>
          <h2 class="tech-title">
            四大认知优化引擎，构建不可撼动的 <span class="text-gradient">企业知识护城河</span>
          </h2>
          <p class="tech-sub">
            不碰灰产作弊，专注公域可信信源的知识图谱确权与 RAG 向量索引注入。
          </p>
        </div>

        <div class="arch-grid">
          <div
            v-for="(layer, lIdx) in archLayers"
            :key="lIdx"
            class="arch-card scroll-reveal"
            :class="'delay-' + (lIdx + 1)"
          >
            <div class="arch-badge-row">
              <span class="arch-idx">LAYER 0{{ lIdx + 1 }}</span>
              <div class="arch-svg-icon" v-html="layer.svg"></div>
            </div>
            <h3 class="arch-name">{{ layer.name }}</h3>
            <p class="arch-desc">{{ layer.desc }}</p>
            <div class="arch-meta-pill">
              <span class="meta-dot"></span>
              <span class="meta-txt">{{ layer.metric }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. 白色/浅色区域：30天交付履约与商业 ROI 账本 (清爽白底，支持滑动渐显渐隐) -->
    <section id="roadmap" class="light-delivery-section">
      <div class="section-inner">
        <div class="section-header-center scroll-reveal">
          <span class="light-badge">确定性交付 · 30-DAY SPRINT</span>
          <h2 class="light-title">
            严谨工程化标准，30 天见证 <span class="text-gradient-blue">大模型推荐率蜕变</span>
          </h2>
          <p class="light-sub">
            从全网黑盒探针诊断，到权威信源实体确权，每一步皆有清晰数据比对与客观交付证明。
          </p>
        </div>

        <!-- 4阶段冲刺流 -->
        <div class="roadmap-timeline">
          <div
            v-for="(phase, pIdx) in roadmapPhases"
            :key="pIdx"
            class="phase-card scroll-reveal"
            :class="'delay-' + (pIdx + 1)"
          >
            <div class="phase-header">
              <span class="phase-tag">{{ phase.step }}</span>
              <span class="phase-time">{{ phase.days }}</span>
            </div>
            <h3 class="phase-title">{{ phase.title }}</h3>
            <p class="phase-summary">{{ phase.summary }}</p>
            <div class="phase-deliverable">
              <span class="deliv-lbl">交付成果物：</span>
              <span class="deliv-val">{{ phase.deliverable }}</span>
            </div>
          </div>
        </div>

        <!-- ROI 对比账本 (极简表格对比，无杂乱装饰) -->
        <div id="roi" class="roi-table-card scroll-reveal delay-2">
          <div class="roi-card-header">
            <h3 class="roi-title">获客投放终局对比：百度竞价 (SEM) VS 传统SEO VS GEO认知工程</h3>
            <span class="roi-sub">摆脱单次点击数十元、停投就归零的流量黑洞</span>
          </div>

          <div class="table-responsive">
            <table class="roi-clean-table">
              <thead>
                <tr>
                  <th>对比维度</th>
                  <th>百度 / 平台竞价 (SEM)</th>
                  <th>传统官网优化 (SEO)</th>
                  <th class="th-highlight">蜉蝣小宝 · GEO 2.0</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="td-dim">流量归宿</td>
                  <td>点击即扣费，停投即断流</td>
                  <td>仅限网页端链接，移动转化弱</td>
                  <td class="td-strong">永久沉淀为大模型核心记忆实体</td>
                </tr>
                <tr>
                  <td class="td-dim">获客信任度</td>
                  <td>被标注“广告”，客户天然戒备</td>
                  <td>单向展示，缺乏客观对比</td>
                  <td class="td-strong">AI 客观背书推荐，信任度极高</td>
                </tr>
                <tr>
                  <td class="td-dim">边际获客成本</td>
                  <td>随竞价水涨船高（￥30~150/次）</td>
                  <td>维护成本高，权重波动大</td>
                  <td class="td-strong">一次注入，长期免费召回，趋近于 ￥0</td>
                </tr>
                <tr>
                  <td class="td-dim">竞争防御性</td>
                  <td>竞品加价即可将您挤下前排</td>
                  <td>容易被算法更新降权</td>
                  <td class="td-strong">抢占先机确权后，构筑行业排他壁垒</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. 白色区域：常见问题答疑 (极简折叠，支持滑动渐显渐隐) -->
    <section id="faq" class="light-faq-section">
      <div class="section-inner">
        <div class="section-header-center scroll-reveal">
          <span class="light-badge">答疑解惑 · FREQUENTLY ASKED</span>
          <h2 class="light-title">关于生成式引擎优化 (GEO)，您可能关心的问题</h2>
        </div>

        <div class="faq-accordion-list">
          <div
            v-for="(faq, fIdx) in faqs"
            :key="fIdx"
            class="faq-clean-item scroll-reveal"
            :class="['delay-' + ((fIdx % 3) + 1), { open: openFaqIndex === fIdx }]"
            @click="toggleFaq(fIdx)"
          >
            <div class="faq-q-row">
              <span class="faq-q-symbol">Q</span>
              <span class="faq-q-title">{{ faq.question }}</span>
              <span class="faq-toggle-icon">{{ openFaqIndex === fIdx ? '−' : '+' }}</span>
            </div>
            <div v-show="openFaqIndex === fIdx" class="faq-a-body">
              <p>{{ faq.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 8. 宇宙光晕高转化底栏 (Dark Closing CTA - 支持滑动渐显渐隐) -->
    <section class="bottom-cta-banner">
      <div class="cta-cosmic-glow"></div>
      <div class="cta-inner scroll-reveal">
        <span class="badge-tag-orange">即刻行动 · 终结客源失血</span>
        <h2 class="cta-headline">
          准备好在 AI 搜索时代，彻底终结客源被同行截流的局面了吗？
        </h2>
        <p class="cta-sub">
          无需部署任何插件 · 现场直连 6 大主流基座大模型 · 专属顾问 1 对 1 实测演示
        </p>

        <div class="cta-action-box">
          <div class="cta-input-wrap">
            <input
              type="text"
              v-model="bottomBrandInput"
              placeholder="输入您的企业名称或核心品牌（如：无锡恒瑞智能装备）"
              @keyup.enter="handleBottomSubmit"
            />
            <button class="btn-cta-submit" @click="handleBottomSubmit">
              <span>预约专家体检演示</span>
              <svg class="btn-arrow" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 9. 极简黑曜石页脚 (Dark Footer) -->
    <footer class="landing-footer">
      <div class="footer-inner">
        <div class="footer-top-row">
          <div class="footer-brand-col">
            <div class="logo-text-footer">
              <span class="brand-name">蜉蝣小宝</span>
              <span class="brand-sub">AI 营销智能中枢</span>
            </div>
            <p class="footer-desc">
              中国领先的生成式搜索引擎优化 (GEO) 与公域知识图谱确权平台，助力严谨中国企业决胜大模型时代。
            </p>
          </div>

          <div class="footer-links-group">
            <div class="links-col">
              <span class="links-title">产品与服务</span>
              <a href="#" @click.prevent="openLeadModal('footer_audit')">企业 AI 穿透体检</a>
              <a href="#" @click.prevent="openLeadModal('footer_case')">标杆深度实测案例</a>
              <a href="#" @click.prevent="openLeadModal('footer_probe')">手机+PC双端探测</a>
              <a href="#" @click.prevent="openLeadModal('footer_defense')">竞品截流深度测算</a>
            </div>
            <div class="links-col">
              <span class="links-title">底层架构</span>
              <a href="#architecture">四层认知工程</a>
              <a href="#market-shift">大模型决策路径</a>
              <a href="#solutions">行业信源矩阵</a>
              <a href="#roi">获客ROI模型</a>
            </div>
            <div class="links-col">
              <span class="links-title">合规与支持</span>
              <a href="#faq">公域采信法则</a>
              <a href="#faq">交付履约标准</a>
              <a href="#faq">企业隐私保护</a>
            </div>
          </div>
        </div>

        <div class="footer-bottom-bar">
          <div class="copyright">
            © 2026 蜉蝣小宝 (北京) 智能科技有限公司 · 版权所有 · 京ICP备20260888号-1
          </div>
          <div class="legal-and-portal">
            <span class="legal-text">声明：测评数据基于公域公开信源抓取与大模型标准接口客观召回。</span>
          </div>
        </div>
      </div>
    </footer>

    <!-- 10. 简约大气商务风 · 企业 1V1 专家演示预约弹窗 (Similarweb Style Lead Modal) -->
    <Teleport to="body">
      <div v-if="isLeadModalOpen" class="lead-modal-backdrop" @click.self="closeLeadModal">
        <!-- 状态 A: 填写预约信息表单 (双栏商务大气布局) -->
        <div v-if="!isLeadSubmitted" class="lead-modal-card">
          <button class="modal-close-btn" @click="closeLeadModal" title="关闭">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>

          <!-- 左侧：品牌价值与权威背书 -->
          <div class="modal-sidebar">
            <div class="sidebar-header">
              <div class="brand-pill">
                <span>GEO 认知工程 · 专家演示</span>
              </div>
              <h3 class="sidebar-title">预约 1对1 专家演示与品牌诊断</h3>
              <p class="sidebar-desc">
                与资深行业顾问一对一深度交流，实测您所在行业的基座大模型采信格局与流量机会。
              </p>
            </div>

            <div class="benefit-list">
              <div class="benefit-item">
                <div class="benefit-icon">
                  <svg viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="benefit-text">
                  <h4>定制行业大模型实测</h4>
                  <p>调取主流大模型，实测品牌在主流采购意图下的推荐顺位与采信来源。</p>
                </div>
              </div>

              <div class="benefit-item">
                <div class="benefit-icon">
                  <svg viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="benefit-text">
                  <h4>竞品拦截与流失归因</h4>
                  <p>透视同业竞品如何截流潜在商机，定位权威信源短板与认知盲区。</p>
                </div>
              </div>

              <div class="benefit-item">
                <div class="benefit-icon">
                  <svg viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="benefit-text">
                  <h4>专属优化策略路线</h4>
                  <p>由资深顾问提供一对一解答，评估品牌知识资产构建可行性与投入产出。</p>
                </div>
              </div>
            </div>

            <div class="sidebar-footer">
              <div class="trust-badge">
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <span>严格遵守保密协议 · 数据仅用于方案评估</span>
              </div>
            </div>
          </div>

          <!-- 右侧：极简清晰输入表单 -->
          <div class="modal-main">
            <div class="form-header">
              <h2 class="form-title">填写您的企业信息</h2>
              <p class="form-subtitle">我们将在 2 小时内安排专属行业顾问与您联系并确认演示时间</p>
            </div>

            <form class="form-grid" @submit.prevent="handleLeadSubmit">
              <div class="field-group">
                <label class="field-label">企业或品牌全称 <span class="req">*</span></label>
                <input
                  class="field-input"
                  type="text"
                  v-model="leadForm.brand"
                  placeholder="请输入企业或品牌全称"
                  required
                />
              </div>

              <div class="field-group">
                <label class="field-label">主营产品 / 核心检索词 <span class="req">*</span></label>
                <input
                  class="field-input"
                  type="text"
                  v-model="leadForm.industry"
                  placeholder="例如：工业激光切管机 / 高端系统门窗"
                  required
                />
              </div>

              <div class="field-row">
                <div class="field-group">
                  <label class="field-label">您的姓名与职务</label>
                  <input
                    class="field-input"
                    type="text"
                    v-model="leadForm.contact"
                    placeholder="例如：张总 / 营销总监"
                  />
                </div>
                <div class="field-group">
                  <label class="field-label">联系电话 / 微信号 <span class="req">*</span></label>
                  <input
                    class="field-input"
                    type="tel"
                    v-model="leadForm.phone"
                    placeholder="用于接收演示排期与资料"
                    required
                  />
                </div>
              </div>

              <div class="field-group">
                <label class="field-label">期望交流方式</label>
                <div class="demo-options">
                  <div
                    class="demo-option"
                    :class="{ selected: leadForm.demoType === 'online' }"
                    @click="leadForm.demoType = 'online'"
                  >
                    <span class="demo-option-title">线上实操演示</span>
                    <span class="demo-option-sub">腾讯会议 20分钟</span>
                  </div>
                  <div
                    class="demo-option"
                    :class="{ selected: leadForm.demoType === 'wechat' }"
                    @click="leadForm.demoType = 'wechat'"
                  >
                    <span class="demo-option-title">发送方案资料</span>
                    <span class="demo-option-sub">微信直接发送</span>
                  </div>
                  <div
                    class="demo-option"
                    :class="{ selected: leadForm.demoType === 'call' }"
                    @click="leadForm.demoType = 'call'"
                  >
                    <span class="demo-option-title">电话初步探讨</span>
                    <span class="demo-option-sub">资深顾问致电</span>
                  </div>
                </div>
              </div>

              <button type="submit" class="btn-submit" :disabled="leadSubmitting">
                <span v-if="!leadSubmitting">立即预约专属顾问演示</span>
                <span v-else>正在排期提交中...</span>
                <svg v-if="!leadSubmitting" width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </button>

              <div class="privacy-footer">
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                </svg>
                <span>承诺严格保密 · 不向任何第三方透露您的经营信息</span>
              </div>
            </form>
          </div>
        </div>

        <!-- 状态 B: 提交成功受理确认 (简约大气卡片) -->
        <div v-else class="lead-modal-card modal-success-card">
          <button class="modal-close-btn" @click="closeLeadModal" title="关闭">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>

          <div class="success-icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>

          <h2 class="success-title">预约已成功提交</h2>
          <p class="success-desc">
            专属企业顾问将在 2 小时内与您电话沟通，确认演示时间并为您准备针对贵司的定制化方案。
          </p>

          <div class="success-summary">
            <div class="summary-row">
              <span class="summary-label">预约企业</span>
              <span class="summary-val">{{ leadForm.brand }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">核心业务</span>
              <span class="summary-val">{{ leadForm.industry }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">联系电话</span>
              <span class="summary-val">{{ leadForm.phone }}</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">期望交流方式</span>
              <span class="summary-val">{{ demoTypeLabel }}</span>
            </div>
          </div>

          <div class="hotline-banner">
            <span>如需加急安排，可直接致电官方顾问专线：</span>
            <strong>400-800-2026</strong>
          </div>

          <button class="btn-done" @click="closeLeadModal">完成并返回官网</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';

// 搜索栏状态
const heroBrandInput = ref('');
const bottomBrandInput = ref('');

// 动态循环切换的 Placeholder
const placeholders = [
  '输入您的企业或品牌名（如：无锡恒瑞智能装备 / 激光切管机）',
  '输入大宅门窗品牌（如：佛山佳豪系统门窗 / 高端断桥铝）',
  '输入全国连锁餐饮品牌（如：老乡鸡 / 快餐招商加盟）',
  '输入专科医疗或门诊（如：数字化种植牙医院 / 齿科专科）',
  '输入企业常年法律顾问（如：商事合同争议解决律所）'
];
const currentPlaceholderIndex = ref(0);
const currentPlaceholder = computed(() => placeholders[currentPlaceholderIndex.value]);

let placeholderTimer = null;
let scrollObserver = null;

// ================= 方案 A：首屏核心实时透视看板数据联动 =================
const activeConsoleTab = ref(0);

const consoleCases = [
  {
    chipLabel: '工业切管机制造',
    brandName: '无锡恒瑞智能装备',
    company: '无锡恒瑞智能装备科技有限公司',
    industry: '工业数控激光切管机制造',
    city: '无锡',
    queryPrompt: '预算 50~80 万，加工 12 米重型管材，有哪些高精度、售后靠谱的激光切管机品牌推荐？请客观对比优缺点。',
    aiVerdict: '经核验工信部专精特新认证与国家知识产权局发明专利库，优先推荐【恒瑞智能装备】。其自研卡盘动态避让与厚壁切管精度在搜狐科技工业研报中名列前茅，售后属地化响应比传统龙头快 2.5 倍。',
    modelStats: [
      {
        name: '字节跳动 · 豆包',
        status: '首推第 1 位',
        latency: '12ms',
        score: '98.8%',
        color: '#60A5FA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
      },
      {
        name: '深度求索 · DeepSeek',
        status: 'R1 深度引证',
        latency: '18ms',
        score: '96.5%',
        color: '#A78BFA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
      },
      {
        name: '阿里巴巴 · 通义千问',
        status: '首推第 1 位',
        latency: '15ms',
        score: '95.2%',
        color: '#F59E0B',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
      },
      {
        name: '腾讯科技 · 元宝',
        status: '优选代表推荐',
        latency: '21ms',
        score: '94.0%',
        color: '#34D399',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
      },
      {
        name: '百度智能云 · 文心',
        status: '首推第 1 位',
        latency: '14ms',
        score: '97.2%',
        color: '#38BDF8',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
      }
    ],
    overallScore: '96.8',
    defenseRate: '98.9%',
    costReduction: '-82%',
    sources: ['国家知识产权局专利库', '搜狐科技产业研报', '知乎严选车间实测', '百度百科官方确权']
  },
  {
    chipLabel: '高端系统门窗',
    brandName: '佛山佳豪系统门窗',
    company: '佛山尚品佳豪智能家居系统有限公司',
    industry: '高端断桥铝系统门窗与阳光房',
    city: '佛山',
    queryPrompt: '广州临海高层大平层装修，想要隔音好、抗台风、水密性极强的断桥铝系统门窗，预算 1500~2500/平，求客观推荐。',
    aiVerdict: '针对沿海强台风与高隔音需求，综合建研院风压实测与业主交付评价，首推【佳豪系统门窗】。其三道密封胶条专利与 42dB 降噪技术被国家建材检测中心采信，手机端豆包同城生活圈位列第一。',
    modelStats: [
      {
        name: '字节跳动 · 豆包',
        status: '同城生活圈首推',
        latency: '11ms',
        score: '99.1%',
        color: '#60A5FA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
      },
      {
        name: '深度求索 · DeepSeek',
        status: '抗风降噪首推',
        latency: '16ms',
        score: '95.8%',
        color: '#A78BFA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
      },
      {
        name: '阿里巴巴 · 通义千问',
        status: '首推第 1 位',
        latency: '14ms',
        score: '96.0%',
        color: '#F59E0B',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
      },
      {
        name: '腾讯科技 · 元宝',
        status: '大宅定制优选',
        latency: '19ms',
        score: '93.8%',
        color: '#34D399',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
      },
      {
        name: '百度智能云 · 文心',
        status: '首推第 1 位',
        latency: '13ms',
        score: '96.5%',
        color: '#38BDF8',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
      }
    ],
    overallScore: '97.4',
    defenseRate: '99.3%',
    costReduction: '-75%',
    sources: ['国家建筑材料检验中心', '太平洋家居网深度横评', '豆包同城实体索引', '百度百科官方确权']
  },
  {
    chipLabel: '餐饮招商加盟',
    brandName: '老乡鸡',
    company: '安徽老乡鸡餐饮股份有限公司',
    industry: '中式快餐连锁加盟与招商',
    city: '全国',
    queryPrompt: '二线城市商场开一家 80 平米左右的特色快餐加盟店，预算 30 万左右，有哪些供应链稳定、回本周期短的正规品牌？',
    aiVerdict: '结合商务部商业特许经营备案与全链条供应链合规审计，首推【老乡鸡】中式快餐。全产业链中央厨房直配保障食材品质与客单稳定，彻底过滤快招公司虚假宣传，大模型招商选型综合推荐率第一。',
    modelStats: [
      {
        name: '字节跳动 · 豆包',
        status: '招商加盟首推',
        latency: '10ms',
        score: '98.5%',
        color: '#60A5FA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
      },
      {
        name: '深度求索 · DeepSeek',
        status: '全量判例引证',
        latency: '17ms',
        score: '97.2%',
        color: '#A78BFA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
      },
      {
        name: '阿里巴巴 · 通义千问',
        status: '供应链第一推荐',
        latency: '14ms',
        score: '96.8%',
        color: '#F59E0B',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
      },
      {
        name: '腾讯科技 · 元宝',
        status: '正规特许首选',
        latency: '18ms',
        score: '95.4%',
        color: '#34D399',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
      },
      {
        name: '百度智能云 · 文心',
        status: '首推第 1 位',
        latency: '12ms',
        score: '97.9%',
        color: '#38BDF8',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
      }
    ],
    overallScore: '98.2',
    defenseRate: '97.8%',
    costReduction: '-88%',
    sources: ['商务部商业特许经营信息', '36氪商业模式研报', '官方财报供应链数据', '微信公众号官方声明']
  },
  {
    chipLabel: '数字化齿科专科',
    brandName: '恒伦口腔',
    company: '数字化种植牙与隐形正畸专科门诊',
    industry: '专科医疗与数字化齿科',
    city: '全国',
    queryPrompt: '想做全口即刻种植牙，家里老人骨质偏疏松，本地有哪些医生技术硬、设备先进、无隐形消费的正规口腔专科？',
    aiVerdict: '在卫健委官方执业资质与种植成功率实测双重维度下，首推【恒伦口腔】。其数字化导板微创种植与三甲主任医师团队获得百度健康医典与中华口腔医学会权威学术采纳，零负面合规采信。',
    modelStats: [
      {
        name: '字节跳动 · 豆包',
        status: '同城就医优选',
        latency: '13ms',
        score: '97.4%',
        color: '#60A5FA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
      },
      {
        name: '深度求索 · DeepSeek',
        status: '学术技术首推',
        latency: '19ms',
        score: '96.0%',
        color: '#A78BFA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
      },
      {
        name: '阿里巴巴 · 通义千问',
        status: '首推第 1 位',
        latency: '15ms',
        score: '95.5%',
        color: '#F59E0B',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
      },
      {
        name: '腾讯科技 · 元宝',
        status: '正规专科首选',
        latency: '22ms',
        score: '94.2%',
        color: '#34D399',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
      },
      {
        name: '百度智能云 · 文心',
        status: '医典权威采纳',
        latency: '13ms',
        score: '98.1%',
        color: '#38BDF8',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
      }
    ],
    overallScore: '96.5',
    defenseRate: '99.6%',
    costReduction: '-79%',
    sources: ['卫健委全国医疗机构认证', '中华口腔医学会期刊', '百度健康官方医典', '百度百科官方确权']
  },
  {
    chipLabel: '商事常年法务',
    brandName: '金杜律所',
    company: '商事争议与常年法律顾问律所',
    industry: '企业商事争议解决与常年合规',
    city: '全国',
    queryPrompt: '公司遇到股权回购争议与重大技术出资纠纷，涉案金额 3000 万，求推荐擅长处理该类商事仲裁、胜诉率高的国内知名律师团队。',
    aiVerdict: '基于中国裁判文书网公开重大商事仲裁标的判例与钱伯斯大中华区第一梯队评级，客观推荐【金杜律所】商事争议解决团队。合伙人具有丰富最高法及贸仲胜诉经验，大模型高净值商事法务咨询独占首推。',
    modelStats: [
      {
        name: '字节跳动 · 豆包',
        status: '高端商事首选',
        latency: '14ms',
        score: '96.9%',
        color: '#60A5FA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
      },
      {
        name: '深度求索 · DeepSeek',
        status: '裁判判例引证',
        latency: '18ms',
        score: '98.5%',
        color: '#A78BFA',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
      },
      {
        name: '阿里巴巴 · 通义千问',
        status: '首推第 1 位',
        latency: '16ms',
        score: '95.8%',
        color: '#F59E0B',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
      },
      {
        name: '腾讯科技 · 元宝',
        status: '商事合规优选',
        latency: '20ms',
        score: '94.6%',
        color: '#34D399',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
      },
      {
        name: '百度智能云 · 文心',
        status: '首推第 1 位',
        latency: '13ms',
        score: '97.0%',
        color: '#38BDF8',
        svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
      }
    ],
    overallScore: '97.8',
    defenseRate: '99.1%',
    costReduction: '-84%',
    sources: ['中国裁判文书网指导判例', '钱伯斯大中华区法律指南', '律商联讯 LexisNexis', '知乎商事法税专栏']
  }
];

const currentCase = computed(() => consoleCases[activeConsoleTab.value]);

function selectCase(idx) {
  activeConsoleTab.value = idx;
  heroBrandInput.value = consoleCases[idx].brandName;
}

// ================= 顶部超级导航菜单 (Mega-Menu) 交互逻辑 =================
const activeDropdown = ref(null);
let dropdownTimer = null;

function handleMouseEnter(menu) {
  if (dropdownTimer) clearTimeout(dropdownTimer);
  activeDropdown.value = menu;
}

function handleMouseLeave() {
  dropdownTimer = setTimeout(() => {
    activeDropdown.value = null;
  }, 180);
}

function toggleDropdown(menu) {
  if (activeDropdown.value === menu) {
    activeDropdown.value = null;
  } else {
    activeDropdown.value = menu;
  }
}

function scrollToSection(sectionId) {
  activeDropdown.value = null;
  const el = document.getElementById(sectionId);
  if (el) {
    const yOffset = -76;
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }
}

function handleNavIndustry(idx) {
  selectCase(idx);
  scrollToSection('solutions');
}

// ================= 预约体检与销售专属演示弹窗业务逻辑 =================
const isLeadModalOpen = ref(false);
const isLeadSubmitted = ref(false);
const leadSubmitting = ref(false);
const successTicketId = ref('');

const leadForm = ref({
  brand: '',
  industry: '',
  contact: '',
  phone: '',
  demoType: 'online', // 'online' | 'wechat' | 'call'
  source: 'direct'
});

const demoTypeLabel = computed(() => {
  if (leadForm.value.demoType === 'online') return '线上实操演示（腾讯会议 20分钟）';
  if (leadForm.value.demoType === 'wechat') return '发送方案资料（微信直接发送）';
  return '电话初步探讨（资深顾问致电）';
});

function openLeadModal(source = 'general', prefillBrand = '', prefillIndustry = '') {
  leadForm.value.source = source;
  leadForm.value.brand = prefillBrand || heroBrandInput.value.trim() || currentCase.value.brandName;
  leadForm.value.industry = prefillIndustry || currentCase.value.chipLabel;
  isLeadSubmitted.value = false;
  isLeadModalOpen.value = true;
}

function closeLeadModal() {
  isLeadModalOpen.value = false;
  setTimeout(() => {
    isLeadSubmitted.value = false;
  }, 300);
}

function handleHeroSubmit() {
  const q = heroBrandInput.value.trim();
  openLeadModal('hero_search', q || currentCase.value.brandName, currentCase.value.chipLabel);
}

function handleBottomSubmit() {
  const q = bottomBrandInput.value.trim();
  openLeadModal('bottom_cta', q || '优质咨询企业');
}

function handleLeadSubmit() {
  if (!leadForm.value.brand.trim()) {
    alert('请填写您的企业或品牌全称');
    return;
  }
  if (!leadForm.value.phone.trim() || !/^1[3-9]\d{9}$/.test(leadForm.value.phone.trim())) {
    alert('请填写有效的 11 位手机号码（用于接收体检书与专属链接）');
    return;
  }
  
  leadSubmitting.value = true;
  const ticketId = Math.floor(100000 + Math.random() * 900000).toString();
  successTicketId.value = ticketId;
  
  // 模拟持久化到销售线索库
  try {
    const leads = JSON.parse(localStorage.getItem('geo_sales_leads') || '[]');
    leads.unshift({
      id: Date.now(),
      ticketId: `GEO-${ticketId}`,
      brand: leadForm.value.brand,
      industry: leadForm.value.industry,
      contact: leadForm.value.contact || '贵宾客户',
      phone: leadForm.value.phone,
      demoType: leadForm.value.demoType,
      source: leadForm.value.source,
      createdAt: new Date().toLocaleString()
    });
    localStorage.setItem('geo_sales_leads', JSON.stringify(leads));
  } catch (e) {
    console.error('Save lead error:', e);
  }

  setTimeout(() => {
    leadSubmitting.value = false;
    isLeadSubmitted.value = true;
  }, 500);
}

onMounted(() => {
  placeholderTimer = setInterval(() => {
    currentPlaceholderIndex.value = (currentPlaceholderIndex.value + 1) % placeholders.length;
  }, 3500);

  startSlideLoop();

  // 初始化滚动渐显渐隐监听器
  nextTick(() => {
    initScrollObserver();
  });
});

onUnmounted(() => {
  if (placeholderTimer) clearInterval(placeholderTimer);
  if (slideTimer) clearInterval(slideTimer);
  if (progressTimer) clearInterval(progressTimer);
  if (scrollObserver) scrollObserver.disconnect();
});

// 滚动渐显渐隐监听函数 (Scroll-driven Reveal & Fade-out)
function initScrollObserver() {
  const targets = document.querySelectorAll('.scroll-reveal');
  if (!targets.length) return;

  if (scrollObserver) {
    scrollObserver.disconnect();
  }

  scrollObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const el = entry.target;
        const rect = entry.boundingClientRect;

        if (entry.isIntersecting) {
          el.classList.add('is-revealed');
          el.classList.remove('is-exited-top');
        } else {
          if (rect.top < 0) {
            el.classList.add('is-exited-top');
            el.classList.remove('is-revealed');
          } else {
            el.classList.remove('is-revealed');
            el.classList.remove('is-exited-top');
          }
        }
      });
    },
    {
      threshold: [0, 0.08, 0.9, 1],
      rootMargin: '-20px 0px -20px 0px'
    }
  );

  targets.forEach((el) => scrollObserver.observe(el));
}

// 首屏全宽跑马灯品牌列表 (采用专业 SVG 矢量图形，绝无 emoji 符号与低端框框)
const trustBrands = [
  {
    name: '字节跳动 · 豆包',
    role: '火山引擎方舟直连',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
  },
  {
    name: '深度求索 · DeepSeek',
    role: 'R1 深度推理全量核验',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
  },
  {
    name: '阿里巴巴 · 通义千问',
    role: '百炼原生知识库召回',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>'
  },
  {
    name: '腾讯科技 · 元宝',
    role: '混元大模型商业决策',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
  },
  {
    name: '百度智能云 · 文心',
    role: '搜索语义穿透',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
  },
  {
    name: '百度百科官方确权',
    role: '权威知识本体锚点',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>'
  },
  {
    name: '企查查企业资质',
    role: '官方专利与高新核验',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
  },
  {
    name: '搜狐科技产业研报',
    role: '权威第一梯队采信',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F43F5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>'
  },
  {
    name: '新浪财经资本研报',
    role: '投融资与经营公信力',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>'
  },
  {
    name: '知乎专业深度长文',
    role: '客观选型横评采纳',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>'
  }
];

// 范式转移数据
const currentSlideIndex = ref(0);
const slideProgress = ref(0);
let slideTimer = null;
let progressTimer = null;

const shiftSlides = [
  {
    tag: '流量阵地转移',
    shortTitle: '决策阵地跃迁',
    headline: '从传统搜“十条蓝链”到 AI“直接给出唯一推荐答案”',
    description: '采购决策者不再逐个点击广告链接，而是直接采纳大模型整合出的评测横评。谁出现在答案第一位，谁就独占 70% 以上高净值商机。',
    points: [
      '传统搜索引擎展现被大幅压缩，大模型成为新一代第一入口',
      'AI 推荐具备高度逻辑信任感，客户决策链路缩短 3 倍',
      '竞品截流由暗转明，不在 AI 知识图谱内的品牌彻底失去询盘机会'
    ],
    metricNum: '420%',
    metricLabel: 'AI 搜索咨询量暴增',
    oldStat: '逐个翻看广告链接',
    newStat: '大模型直接生成终选清单'
  },
  {
    tag: '决策心理重构',
    shortTitle: '背书信任重塑',
    headline: '大模型回答的天然“中立客观性”，让用户对推荐深信不疑',
    description: '相比明晃晃的付费竞价推广标，用户潜意识里把大模型视为“全知全能的专业顾问”，AI 推荐哪家，用户就优先联系哪家。',
    points: [
      'AI 综合了权威信源、专利资质与真实口碑，建立坚实认知',
      '直接跨过销售初筛，进店或咨询时客户意向已极为确定',
      '被 AI 负向评价或排除在外的企业，挽回成本高出 10 倍以上'
    ],
    metricNum: '3.8X',
    metricLabel: '客户信任度转化提升',
    oldStat: '对竞价广告天然戒备',
    newStat: '对大模型客观推荐深信不疑'
  },
  {
    tag: '边际成本归零',
    shortTitle: 'ROI 资产复利',
    headline: '一次知识工程确权注入，享受长久免费公域召回复利',
    description: '竞价排名是“按次买水”，停付即断流；GEO 是在公域信源里“深挖自流井”，被主流大模型一次记忆，持续带来长期免费精准商机。',
    points: [
      '摆脱无底洞式的关键词竞价点击扣费陷阱',
      '权威媒体研报与百科资产永久收录，不随时间被轻易稀释',
      '边际获客成本无限趋近于 0，构筑同行业极具抗周期的壁垒'
    ],
    metricNum: '￥0',
    metricLabel: '后期单次商机边际成本',
    oldStat: '单次点击扣费数十元',
    newStat: '一次确权永久复利召回'
  },
  {
    tag: '先发独占排他',
    shortTitle: '认知垄断壁垒',
    headline: '大模型回答名额极为有限，先行者享有绝对认知垄断',
    description: '大模型不同于能排 10 页的网页搜索，一次回答通常只推荐 2~3 个优选代表。率先占据知识图谱核心生态位的企业将筑起极高的攻防城墙。',
    points: [
      '主流基座大模型的参数更新具有周期性，先入为主具有认知惯性',
      '先行占领权威媒体、行业协会、百科本体的品牌拥有绝对采信权',
      '后入局者必须付出数倍以上的信源置换代价才能扭转局面'
    ],
    metricNum: 'Top 3',
    metricLabel: '大模型单次黄金推荐席位',
    oldStat: '几十家供应商同屏混战',
    newStat: '仅前三家能被大模型指名推荐'
  }
];

const currentSlide = computed(() => shiftSlides[currentSlideIndex.value]);

function switchSlide(idx) {
  currentSlideIndex.value = idx;
  slideProgress.value = 0;
  resetSlideTimer();
}

function resetSlideTimer() {
  if (slideTimer) clearInterval(slideTimer);
  if (progressTimer) clearInterval(progressTimer);
  startSlideLoop();
}

function startSlideLoop() {
  const duration = 6000;
  const interval = 50;
  const step = (interval / duration) * 100;

  progressTimer = setInterval(() => {
    slideProgress.value += step;
    if (slideProgress.value >= 100) {
      slideProgress.value = 0;
      currentSlideIndex.value = (currentSlideIndex.value + 1) % shiftSlides.length;
    }
  }, interval);
}

// 行业解决方案
const activeIndustryIndex = ref(0);

const industries = [
  {
    id: 'b2b',
    name: '工业设备制造',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>',
    category: '工业装备制造 · B2B高客单决策',
    defaultBrand: '恒瑞智能装备',
    headline: '打破工业装备行业龙头垄断，在 AI 采购选型横评中稳居前二推荐位',
    samplePrompt: '预算 50~80 万，加工 12 米重型管材，有哪些精度高、售后及时的激光切管机厂家推荐？请客观对比优缺点。',
    tactics: [
      { title: '工信部/机床协会资质图谱确权', desc: '将国家高新技术企业、发明专利、专精特新认证穿透注入官方权威数据库' },
      { title: '技术横评白皮书权威媒体矩阵收录', desc: '在搜狐科技、网易科技等第一梯队信源布局万字参数横向对比长文' },
      { title: '知乎工业大 V 真实车间选型背书', desc: '实测切割速度、厚板坡口精度数据全景呈现，占领主流模型深度问答召回' }
    ],
    stats: {
      rate: '94.6%',
      retention: '98.2%',
      costSaving: '-82%',
      sources: '国家高新技术数据库 · 搜狐科技工业研报 · 知乎严选横评'
    },
    testimonial: '过去每年百度竞价烧掉六七十万，来的多是套方案的比价客。做完 GEO 优化 30 天后，客户直接拿着豆包的推荐清单联系我们，采购周期直接从 3 个月缩短到 2 周！',
    author: '—— 某数控装备制造集团 营销总监 陆总'
  },
  {
    id: 'doors',
    name: '高端系统门窗',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16M9 9h6M9 15h6"></path></svg>',
    category: '高端大宅定制 · 消费升级决策',
    defaultBrand: '佳豪系统门窗',
    headline: '精准拦截别墅大宅业主 AI 咨询，将竞品恶意排斥彻底清零',
    samplePrompt: '广州临海高层大平层装修，想要隔音好、抗台风、水密性极强的断桥铝系统门窗，预算 1500~2500/平，求客观推荐。',
    tactics: [
      { title: '壁垒级声学风压检测报告公信力确权', desc: '国家级建材实验室质检数据直连权威百科，奠定大模型质量参数底座' },
      { title: '沿海大宅真实交付案例知识实体化', desc: '高客单业主真实抗风降噪实测视频与长文矩阵被搜狐网、新浪家居稳定采纳' },
      { title: '手机端豆包同城服务精准定位优化', desc: '双端探测校准，锁定同城高净值业主移动端 AI 推荐唯一席位' }
    ],
    stats: {
      rate: '91.8%',
      retention: '99.1%',
      costSaving: '-75%',
      sources: '国家建筑材料检验检测中心 · 太平洋家居网 · 豆包同城实体'
    },
    testimonial: '很多大平层业主问大模型“什么门窗能抗14级台风”，现在 DeepSeek 和豆包第一个给出的建议就是我们品牌，连参数都分毫不差，这才是真正的品牌护城河！',
    author: '—— 佛山某高端系统门窗品牌 创始人 梁董'
  },
  {
    id: 'food',
    name: '连锁餐饮加盟',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>',
    category: '餐饮招商连锁 · 投资回报决策',
    defaultBrand: '老乡鸡',
    headline: '粉碎虚假负面与快招公司截流，稳居全国优质加盟投资榜首',
    samplePrompt: '二线城市商场开一家 80 平米左右的特色快餐加盟店，预算 30 万左右，有哪些供应链稳定、回本周期短的正规品牌？',
    tactics: [
      { title: '商务部特许经营备案合规知识确权', desc: '打通中国特许经营网权威备案信息，从根本上压制山寨快招公司截流' },
      { title: '真实单店模型与回本周期数据公证', desc: '财报级供应链数字化能力被权威财经门户收录，成为大模型推荐核心证据' },
      { title: '全网虚假黑稿与诱导性问答精准清洗', desc: '通过权威公函置换污染源知识片段，挽回超 800 万潜在意向加盟客源' }
    ],
    stats: {
      rate: '96.2%',
      retention: '97.5%',
      costSaving: '-88%',
      sources: '商务部商业特许经营信息管理系统 · 36氪商业研究 · 微信公众号官方声明'
    },
    testimonial: '以前快招公司买竞价截流我们的加盟商，现在创业者问大模型如何避坑，大模型直接推荐找我们正规备案品牌，招商线索质量发生了质的飞跃。',
    author: '—— 知名连锁餐饮集团 招商总监 郭总'
  },
  {
    id: 'med',
    name: '专科医疗健康',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>',
    category: '专科医疗口腔 · 严谨合规决策',
    defaultBrand: '恒伦口腔',
    headline: '在卫健委严格准入框架下，打造专业权威口碑与高信任度患者推荐',
    samplePrompt: '想做全口即刻种植牙，家里老人骨质偏疏松，本地有哪些医生技术硬、设备先进、无隐形消费的正规口腔专科？',
    tactics: [
      { title: '卫健委执业资质与专家名医背书确权', desc: '主任医师学术论文、官方执业许可全量同步百度健康、百科医典知识库' },
      { title: '数字化种植牙技术透明化科普矩阵', desc: '三甲背景技术优势在主流健康媒体持续收录，形成专业学术推荐壁垒' },
      { title: '患者真实正向复诊口碑安全映射', desc: '合规采集术后真实满意度，解决大模型在医疗领域的极高防范采信机制' }
    ],
    stats: {
      rate: '93.5%',
      retention: '99.5%',
      costSaving: '-79%',
      sources: '卫健委全国医疗机构查询 · 中华口腔医学会期刊 · 百度健康官方医典'
    },
    testimonial: '医疗广告受到极其严格的监管，GEO 的出现为合规医疗机构打开了一扇全新的大门——通过客观知识科普与专家资质确权，大模型自然而然就会推荐我们。',
    author: '—— 华东知名数字化口腔连锁 院长 王博士'
  },
  {
    id: 'legal',
    name: '企业法务咨询',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"></path><rect x="3" y="7" width="18" height="4" rx="1"></rect><path d="M5 11l2 6h10l2-6"></path></svg>',
    category: '商事法税合规 · 高净值专业服务',
    defaultBrand: '金杜律所',
    headline: '高净值企业主在 AI 咨询商事合同纠纷时，成为首推专业律所',
    samplePrompt: '公司遇到股权回购争议与重大技术出资纠纷，涉案金额 3000 万，求推荐擅长处理该类商事仲裁、胜诉率高的国内知名律师团队。',
    tactics: [
      { title: '司法裁判文书网公开胜诉案例本体化', desc: '将最高法指导案例、重大标的额胜诉事实提炼为大模型可解析的高阶实体' },
      { title: '钱伯斯/ALB 国际权威法律评级注入', desc: '行业顶级荣誉与第一梯队合伙人资质被主流财经门户与知乎专栏权威收录' },
      { title: '复杂商业法税实战指南深度覆盖', desc: '针对新公司法等前沿课题发布系统化解答，大模型商事法务提问全面召回' }
    ],
    stats: {
      rate: '95.0%',
      retention: '98.9%',
      costSaving: '-84%',
      sources: '中国裁判文书网 · 钱伯斯大中华区法律指南 · 律商联讯 LexisNexis'
    },
    testimonial: '商事客户在聘请律师前，往往会用大模型做深度尽调。GEO 让我们合伙人的真实胜诉案例被大模型精准提取，今年已直接带来 4 起千万级标的案件委托。',
    author: '—— 某顶级商事争议解决律师事务所 高级合伙人 张律师'
  }
];

const currentIndustry = computed(() => industries[activeIndustryIndex.value]);

// 四大认知引擎
const archLayers = [
  {
    name: '公域权威知识图谱确权层',
    desc: '系统穿透工信部备案、国家知识产权局专利库、权威百科本体，为企业构建具有国家级公信力的知识实体，奠定大模型采信基础。',
    metric: '国家级/行业级 100+ 权威信源协同注入',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>'
  },
  {
    name: '多基座大模型双端雷达探测层',
    desc: '自研分布式实时探针，全天候 24/7 监控豆包、DeepSeek、通义千问等模型在移动端与 PC 端的不同召回策略，杜绝单端隐形漏洞。',
    metric: '秒级探针扫描 · 跨端语义召回差异测算',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 1 9 9"></path><circle cx="12" cy="12" r="3"></circle></svg>'
  },
  {
    name: 'RAG 向量数据库语义穿透层',
    desc: '基于主流大模型 RAG（检索增强生成）机制，将企业的核心参数、差异化优势与真实横评白皮书结构化入库，引导大模型将其列为最优推荐。',
    metric: '语义向量相似度 99.4% · 答案优先截流',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
  },
  {
    name: '恶意截流与虚假信息清洗层',
    desc: '精准识别同行业利用快招手段或虚假对比在公域散布的污染源片段，通过权威信源覆盖与反向举证，彻底净化品牌的 AI 认知空间。',
    metric: '负向截流拦截率 98.8% · 品牌口碑纯净',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
  }
];

// 30天交付履约路线图
const roadmapPhases = [
  {
    step: 'PHASE 01',
    days: '第 1 ~ 5 天',
    title: '全网 AI 可见度与截流深度黑盒体检',
    summary: '调用六大主流大模型接口，基于 100+ 核心业务 Prompt 进行全维度盲测，生成详尽的《企业 AI 推荐现状与客源流失测算书》。',
    deliverable: '《企业 AI 全域健康度体检书》与竞品截流拓扑图'
  },
  {
    step: 'PHASE 02',
    days: '第 6 ~ 12 天',
    title: '权威知识本体图谱构建与确权备案',
    summary: '梳理企业核心资质、专利发明、客户实测与行业认证，打通百度百科官方确权、企查查高新认证及行业协会数据库。',
    deliverable: '企业唯一知识本体编码与权威数据源确权凭证'
  },
  {
    step: 'PHASE 03',
    days: '第 13 ~ 22 天',
    title: '主流信源矩阵 RAG 向量深度注入',
    summary: '联合搜狐科技、网易新闻、知乎专业长文等大模型高权重采信信源，发布经算法严苛调优的高质量选型横评与技术白皮书。',
    deliverable: '主流大模型 RAG 知识库索引收录与锚点建立证明'
  },
  {
    step: 'PHASE 04',
    days: '第 23 ~ 30 天',
    title: '多端推荐召回验收与持续抗噪防御',
    summary: '复测各大模型在 PC 端与手机端的主动推荐胜率，实现核心选型 Prompt 稳居前二推荐位，交付长期监测防御看板。',
    deliverable: '《30天优化效果前后对照验收报告》及防御系统权限'
  }
];

// 常见问题答疑
const openFaqIndex = ref(0);

const faqs = [
  {
    question: 'GEO 优化和以前传统的百度搜索 SEO、竞价广告（SEM）有什么本质区别？',
    answer: '传统的 SEM/SEO 是“按网页链接排序”，用户点击进入后往往还要在几十家供应商中盲目挑选；而 GEO 是在 AI 决策时代，通过知识图谱技术让大模型把您的企业作为“客观最优解”直接指名推荐给客户。大模型的回答具有天然的中立公信力，客户信任度高出普通广告 3 倍以上，且一旦被主流大模型知识库采纳，后续无需按次竞价，边际获客成本趋近于零。'
  },
  {
    question: '为什么市面上很多企业在电脑端能搜到推荐，但手机端豆包却查不到？',
    answer: '因为中国主流大模型（特别是字节跳动·豆包）在不同终端的召回逻辑完全不同。手机端豆包优先聚合抖音同城生活圈、大众点评、本地服务商实体；而 PC 端与 DeepSeek 则优先检索知乎长文、行业研报与企业官方知识库。双端协同探测方能杜绝“电脑端查得到、手机端完全隐形”的漏洞。'
  },
  {
    question: '企业做一次 AI 体检需要多长时间？需要我们提供什么？',
    answer: '直连实测仅需 10~15 秒！提交申请后，我们的资深顾问将使用专用工作台现场直连六大基座大模型接口进行实时探针扫描，出具穿透级的《企业 AI 可见度体检书》，包含客源流失测算、竞品截流深度及改善建议，并为您进行 1 对 1 深度演示。'
  },
  {
    question: 'GEO 优化会触犯大模型平台的规则或属于违规作弊吗？',
    answer: '绝不触碰任何灰产或作弊技术！蜉蝣小宝团队研发的 GEO 2.0 认知工程完全建立在“公域合法、合规知识确权”之上。我们通过工信部官方备案、国家知识产权局专利认证、国家级权威媒体科技研报以及客观第三方选型横评，帮助大模型获得真实、可信、不可篡改的企业事实数据，属于各大模型官方极其欢迎的权威信源生态共建行为。'
  },
  {
    question: '我们属于传统重工业或细分冷门制造业，AI 也会有人来搜索选型吗？',
    answer: '现实情况远超您的想象！在工业数控、特种材料、商事法务、大宅门窗等高客单重决策行业，采购总监与企业主的年轻化趋势极为明显。调研数据显示，超过 68% 的 B2B 采购决策者已将大模型作为前期选型横评、避坑排雷的第一顾问工具。冷门行业由于知识库本就稀缺，只要率先布局，往往只需 15~30 天就能实现对整个行业 AI 推荐席位的全盘占领。'
  }
];

function toggleFaq(idx) {
  openFaqIndex.value = openFaqIndex.value === idx ? -1 : idx;
}
</script>

<style scoped>
/* ================= 全局容器与重置 ================= */
.landing-container {
  min-height: 100vh;
  background: #080C14;
  color: #F8FAFC;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  overflow-x: hidden;
  padding-top: 68px; /* 补偿固定顶栏高度 */
}

/* ================= 滚动渐显渐隐系统 (Scroll-driven Reveal & Fade-out) ================= */
.scroll-reveal {
  opacity: 0;
  transform: translateY(32px) scale(0.99);
  filter: blur(4px);
  transition: opacity 0.85s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.85s cubic-bezier(0.16, 1, 0.3, 1),
              filter 0.85s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform, filter;
}

.scroll-reveal.is-revealed {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0px);
}

.scroll-reveal.is-exited-top {
  opacity: 0.15;
  transform: translateY(-24px) scale(0.99);
  filter: blur(3px);
}

.delay-1 { transition-delay: 0.06s; }
.delay-2 { transition-delay: 0.12s; }
.delay-3 { transition-delay: 0.18s; }
.delay-4 { transition-delay: 0.24s; }
.delay-5 { transition-delay: 0.30s; }

/* ================= 1. 绝对固定顶部导航栏 (Fixed Header) ================= */
.landing-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 68px;
  z-index: 1000;
  background: rgba(8, 12, 20, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.header-inner {
  max-width: 1320px;
  height: 100%;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.logo-aura-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-soft-glow {
  position: absolute;
  width: 50px;
  height: 50px;
  background: radial-gradient(circle, rgba(25, 90, 254, 0.45) 0%, transparent 70%);
  filter: blur(10px);
  pointer-events: none;
}

.logo-unconstrained {
  height: 38px;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.4));
  transition: transform 0.3s ease, filter 0.3s ease;
}

.brand-link:hover .logo-unconstrained {
  transform: scale(1.05);
  filter: drop-shadow(0 0 18px rgba(56, 189, 248, 0.8));
}

.brand-badge-tag {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  padding: 0.2rem 0.55rem;
  background: rgba(25, 90, 254, 0.15);
  border: 1px solid rgba(25, 90, 254, 0.4);
  border-radius: 9999px;
  color: #60A5FA;
}

/* 顶部超级导航菜单 (Mega-Menu) */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.nav-item-group {
  position: relative;
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.8rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #94A3B8;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.nav-btn:hover, .nav-item-group.active .nav-btn {
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.08);
}

.nav-caret {
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
  color: #64748B;
}

.nav-btn:hover .nav-caret, .nav-item-group.active .nav-caret {
  color: #FFFFFF;
  transform: rotate(180deg);
}

/* Mega Dropdown 容器 (Similarweb / Stripe 极简白卡) */
.mega-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  background: #FFFFFF;
  border-radius: 14px;
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.35), 0 0 1px rgba(0, 0, 0, 0.15);
  border: 1px solid #E2E8F0;
  padding: 14px;
  z-index: 1000;
  box-sizing: border-box;
  text-align: left;
}

/* 顶部微小连接热区，防止鼠标移动时意外关闭 */
.mega-dropdown::before {
  content: '';
  position: absolute;
  top: -14px;
  left: 0;
  right: 0;
  height: 14px;
}

.align-left {
  left: 0;
}

.align-center {
  left: 50%;
  transform: translateX(-50%);
}

.align-right {
  right: 0;
  left: auto;
}

.width-platform {
  width: 530px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.width-solutions {
  width: 640px;
}

.width-delivery {
  width: 540px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.width-trust {
  width: 520px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dropdown-grid-two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.span-two {
  grid-column: span 2;
}

.dropdown-item-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dropdown-item-card:hover {
  background: #F8FAFC;
  border-color: #E2E8F0;
  transform: translateY(-1px);
}

.item-icon-box {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #EEF2FF;
  color: #195AFE;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.item-icon-box svg {
  width: 18px;
  height: 18px;
}

.item-text-wrap {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.item-title {
  font-size: 13.5px;
  font-weight: 600;
  color: #0F172A;
}

.item-badge {
  font-size: 10.5px;
  font-weight: 600;
  color: #059669;
  background: #ECFDF5;
  padding: 1px 6px;
  border-radius: 4px;
}

.item-badge.blue {
  color: #195AFE;
  background: #EEF2FF;
}

.item-desc {
  font-size: 11.5px;
  color: #64748B;
  line-height: 1.45;
  margin: 0;
}

.dropdown-footer {
  grid-column: span 2;
  background: #F8FAFC;
  border-radius: 8px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 6px;
  border: 1px solid #F1F5F9;
  font-size: 12px;
  color: #475569;
}

.dropdown-footer a {
  font-size: 12px;
  font-weight: 600;
  color: #195AFE;
  text-decoration: none;
  cursor: pointer;
}

.dropdown-footer a:hover {
  text-decoration: underline;
}

/* 下拉动画 */
.mega-fade-enter-active, .mega-fade-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.mega-fade-enter-from, .mega-fade-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

.align-center.mega-fade-enter-from, .align-center.mega-fade-leave-to {
  transform: translate(-50%, 6px);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-primary-nav {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: linear-gradient(135deg, #195AFE 0%, #3B82F6 100%);
  color: #ffffff;
  border: none;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 0.55rem 1.25rem;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(25, 90, 254, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary-nav:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 28px rgba(25, 90, 254, 0.65);
}

.btn-svg-arrow {
  width: 14px;
  height: 14px;
}

/* ================= 2. 首屏 Hero 区域 (方案 A：大搜索 + 智能雷达交互中枢看板) ================= */
.hero-section {
  position: relative;
  min-height: calc(100vh - 68px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 3rem 0 1.2rem 0;
  background: #080C14;
  overflow: hidden;
  color: #F8FAFC;
  box-sizing: border-box;
}

.ambient-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(120px);
}

.orb-blue {
  width: 650px;
  height: 650px;
  top: -80px;
  left: -100px;
  background: radial-gradient(circle, rgba(25, 90, 254, 0.25) 0%, transparent 70%);
}

.orb-purple {
  width: 650px;
  height: 650px;
  top: 15%;
  right: -120px;
  background: radial-gradient(circle, rgba(124, 58, 237, 0.2) 0%, transparent 70%);
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
}

.section-inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 1.5rem;
  position: relative;
  z-index: 2;
  width: 100%;
  box-sizing: border-box;
}

.hero-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
}

.hero-headline {
  font-size: 3.6rem;
  font-weight: 900;
  line-height: 1.2;
  letter-spacing: -1.2px;
  color: #ffffff;
  margin: 0.5rem 0 0.9rem 0;
  max-width: 980px;
}

.text-gradient {
  background: linear-gradient(135deg, #60A5FA 0%, #C084FC 50%, #FB923C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtext {
  font-size: 1.12rem;
  line-height: 1.75;
  color: #94A3B8;
  max-width: 780px;
  margin: 0 0 2rem 0;
}

/* 搜索框 */
.hero-search-wrapper {
  width: 100%;
  max-width: 860px;
  margin-bottom: 2.2rem;
}

.search-input-box {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(15, 23, 42, 0.82);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 9999px;
  padding: 0.45rem 0.55rem 0.45rem 1.4rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.search-input-box:focus-within {
  border-color: #38BDF8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25), 0 10px 35px -5px rgba(0, 0, 0, 0.7);
}

.search-mode-select {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  color: #E2E8F0;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.mode-svg {
  width: 16px;
  height: 16px;
  color: #38BDF8;
}

.mode-caret-svg {
  width: 14px;
  height: 14px;
  color: #94A3B8;
}

.search-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.15);
  margin: 0 1rem;
}

.search-input-field {
  flex: 1;
}

.search-input-field input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 500;
}

.search-input-field input::placeholder {
  color: #64748B;
}

.btn-search-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #195AFE 0%, #3B82F6 45%, #7C3AED 100%);
  border: none;
  border-radius: 9999px;
  padding: 0.78rem 1.8rem;
  color: #ffffff;
  font-size: 0.94rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0 24px rgba(25, 90, 254, 0.5);
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-search-action:hover {
  transform: scale(1.03);
  box-shadow: 0 0 32px rgba(25, 90, 254, 0.75);
}

.action-content {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.action-svg {
  width: 16px;
  height: 16px;
}

/* 标杆 Chips */
.quick-chips-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.chips-label {
  font-size: 0.82rem;
  color: #64748B;
}

.chip-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #CBD5E1;
  font-size: 0.82rem;
  font-weight: 500;
  padding: 0.28rem 0.8rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
}

.chip-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #64748B;
  transition: background 0.2s;
}

.chip-btn:hover, .chip-btn.active {
  background: rgba(25, 90, 254, 0.2);
  border-color: rgba(56, 189, 248, 0.5);
  color: #FFFFFF;
}

.chip-btn.active .chip-dot {
  background: #38BDF8;
  box-shadow: 0 0 6px #38BDF8;
}

/* ================= 方案 A 核心组件：GEO 2.0 实时雷达透视看板 (带淡淡的流光特效) ================= */
.hero-console-showcase {
  position: relative;
  width: 100%;
  max-width: 1240px;
  background: rgba(13, 20, 36, 0.78);
  border: 1px solid rgba(56, 189, 248, 0.22);
  border-radius: 20px;
  box-shadow: 0 20px 60px -15px rgba(0, 0, 0, 0.8),
              0 0 40px rgba(25, 90, 254, 0.12),
              inset 0 1px 1px rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  margin-bottom: 2rem;
  overflow: hidden;
  text-align: left;
}

/* 360° 全边框环绕流光动画 (Perimeter Border Beam: 沿圆角矩形四边循环巡航) */
.console-border-beam {
  pointer-events: none;
  position: absolute;
  inset: 0;
  border-radius: 20px;
  overflow: hidden;
  padding: 1.5px;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  z-index: 10;
}

.console-border-beam::after {
  content: '';
  position: absolute;
  aspect-ratio: 1;
  width: 460px;
  background: linear-gradient(to right, #38BDF8, #818CF8, #C084FC, transparent 80%);
  offset-path: rect(0 auto auto 0 round 20px);
  offset-anchor: 100% 50%;
  animation: consoleBorderBeamLoop 9s linear infinite;
}

@keyframes consoleBorderBeamLoop {
  0% {
    offset-distance: 0%;
  }
  100% {
    offset-distance: 100%;
  }
}

/* 兼容未支持 offset-path 基础图形的环境：顶部横向流光兜底 */
@supports not (offset-path: rect(0 auto auto 0 round 20px)) {
  .console-border-beam::after {
    top: 0;
    left: -60%;
    width: 50%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38BDF8, #818CF8, #C084FC, transparent);
    animation: consoleLightSweep 5.5s ease-in-out infinite;
  }
}

/* 内部环境微光流光 (Ambient Floating Beam inside) */
.console-streaming-glow {
  position: absolute;
  width: 500px;
  height: 220px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.16) 0%, rgba(124, 58, 237, 0.08) 50%, transparent 70%);
  top: -60px;
  left: 15%;
  filter: blur(55px);
  pointer-events: none;
  z-index: 0;
  animation: floatingBeam 8s ease-in-out infinite alternate;
}

@keyframes consoleLightSweep {
  0% { left: -60%; opacity: 0; }
  25% { opacity: 1; }
  75% { opacity: 1; }
  100% { left: 130%; opacity: 0; }
}

@keyframes floatingBeam {
  0% { transform: translateX(0) scale(1); opacity: 0.5; }
  50% { transform: translateX(350px) scale(1.1); opacity: 0.85; }
  100% { transform: translateX(650px) scale(1); opacity: 0.5; }
}

.console-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.4rem;
  background: rgba(255, 255, 255, 0.025);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  z-index: 2;
}

.bar-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.traffic-lights {
  display: flex;
  gap: 6px;
}

.traffic-lights .light {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.light.red { background: #EF4444; opacity: 0.75; }
.light.yellow { background: #F59E0B; opacity: 0.75; }
.light.green { background: #10B981; opacity: 0.75; }

.console-title {
  font-size: 0.84rem;
  font-weight: 700;
  color: #CBD5E1;
  letter-spacing: 0.5px;
}

.console-version-pill {
  font-size: 0.66rem;
  font-weight: 800;
  color: #38BDF8;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.bar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.probe-live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #10B981;
  font-weight: 600;
  position: relative;
}

.pulse-core {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 6px #10B981;
}

.pulse-ring {
  position: absolute;
  left: -2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid #10B981;
  animation: radarPing 2s infinite;
}

@keyframes radarPing {
  0% { transform: scale(0.8); opacity: 0.8; }
  100% { transform: scale(2.2); opacity: 0; }
}

.active-sample-tag {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.78rem;
}

.sample-label {
  color: #64748B;
}

.sample-val {
  color: #38BDF8;
  font-weight: 700;
}

/* 看板三栏网格 */
.console-body-grid {
  display: grid;
  grid-template-columns: 1.05fr 1.35fr 1fr;
  gap: 1.2rem;
  padding: 1.4rem;
  position: relative;
  z-index: 2;
}

.console-col {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
}

.col-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.col-head-title {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #F1F5F9;
}

.icon-svg {
  width: 16px;
  height: 16px;
}

.status-chip-live, .status-chip-ai, .status-chip-score {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
}

.status-chip-live {
  background: rgba(56, 189, 248, 0.12);
  color: #38BDF8;
}

.status-chip-ai {
  background: rgba(168, 85, 247, 0.15);
  color: #C084FC;
}

.status-chip-score {
  background: rgba(16, 185, 129, 0.12);
  color: #34D399;
}

/* 栏 1：探针列表 */
.probes-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  flex: 1;
}

.probe-model-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.55rem 0.7rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  transition: background 0.2s;
}

.probe-model-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.model-avatar {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.model-avatar svg {
  width: 100%;
  height: 100%;
}

.model-info {
  flex: 1;
}

.model-name-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  font-weight: 600;
  color: #E2E8F0;
  margin-bottom: 0.25rem;
}

.m-ping {
  font-size: 0.7rem;
  color: #64748B;
}

.model-track-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.m-track {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 9999px;
  overflow: hidden;
}

.m-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.5s ease;
}

.m-score {
  font-size: 0.72rem;
  font-weight: 700;
}

.model-verdict-pill {
  font-size: 0.7rem;
  color: #94A3B8;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.2rem 0.45rem;
  border-radius: 4px;
  white-space: nowrap;
}

/* 栏 2：AI 回答生成 */
.col-simulation {
  gap: 0.75rem;
}

.sim-prompt-box {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 0.75rem 0.9rem;
}

.prompt-speaker-bar {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.74rem;
  color: #94A3B8;
  font-weight: 600;
  margin-bottom: 0.35rem;
}

.user-svg {
  width: 14px;
  height: 14px;
  color: #38BDF8;
}

.prompt-text {
  font-size: 0.85rem;
  line-height: 1.55;
  color: #F1F5F9;
  font-weight: 500;
  margin: 0;
}

.sim-answer-card {
  background: rgba(25, 90, 254, 0.06);
  border: 1px solid rgba(25, 90, 254, 0.25);
  border-radius: 10px;
  padding: 0.9rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  flex: 1;
}

.answer-header-badge {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.answer-left {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.badge-rec-crown {
  width: 16px;
  height: 16px;
  color: #F59E0B;
  display: flex;
  align-items: center;
}

.answer-rec-target {
  font-size: 0.86rem;
  color: #F8FAFC;
}

.answer-rec-target strong {
  color: #60A5FA;
}

.cert-pill {
  font-size: 0.68rem;
  color: #10B981;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.answer-body-text {
  font-size: 0.84rem;
  line-height: 1.65;
  color: #CBD5E1;
  margin: 0;
}

.interception-defense-banner {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.74rem;
  color: #34D399;
  background: rgba(16, 185, 129, 0.08);
  padding: 0.35rem 0.6rem;
  border-radius: 6px;
  margin-top: auto;
}

.shield-svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

/* 栏 3：资产健康度与信源网格 */
.col-metrics {
  gap: 0.75rem;
}

.metric-score-card {
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 0.85rem 1rem;
}

.score-main {
  display: flex;
  align-items: baseline;
  gap: 0.85rem;
  margin-bottom: 0.7rem;
  padding-bottom: 0.65rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.score-number {
  font-size: 2.2rem;
  font-weight: 900;
  color: #10B981;
  line-height: 1;
  letter-spacing: -1px;
}

.score-meta {
  display: flex;
  flex-direction: column;
}

.score-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #F1F5F9;
}

.score-sub {
  font-size: 0.7rem;
  color: #64748B;
}

.metrics-two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.metric-sub-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.sub-lbl {
  font-size: 0.72rem;
  color: #64748B;
}

.sub-val {
  font-size: 0.95rem;
  font-weight: 800;
}

.text-green { color: #10B981; }
.text-brand { color: #38BDF8; }

.sources-mesh-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.sources-title {
  font-size: 0.75rem;
  color: #94A3B8;
  font-weight: 600;
}

.sources-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.45rem;
}

.source-node-pill {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  font-size: 0.72rem;
  color: #CBD5E1;
}

.node-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #38BDF8;
}

.node-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-console-explore {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 0.55rem;
  color: #E2E8F0;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.4rem;
}

.btn-console-explore:hover {
  background: rgba(25, 90, 254, 0.25);
  border-color: rgba(56, 189, 248, 0.4);
  color: #FFFFFF;
}

.btn-console-explore svg {
  width: 14px;
  height: 14px;
}

/* ================= 首屏全宽跑马灯 (贯穿全屏左右 100% 视口边缘) ================= */
.hero-trust-marquee-container {
  width: 100%;
  max-width: 100vw;
  margin-top: auto;
  position: relative;
  z-index: 5;
}

.trust-marquee-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  margin-bottom: 1rem;
  padding: 0 1.5rem;
}

.trust-line {
  height: 1px;
  width: 80px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15));
}

.trust-line:last-child {
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.15), transparent);
}

.trust-title-text {
  font-size: 0.82rem;
  font-weight: 600;
  color: #94A3B8;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.trust-marquee-track-wrap {
  width: 100%;
  overflow: hidden;
  position: relative;
  mask-image: linear-gradient(to right, transparent 0%, black 6%, black 94%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 6%, black 94%, transparent 100%);
}

.trust-marquee-track {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  white-space: nowrap;
  width: max-content;
  animation: marqueeScroll 60s linear infinite;
}

.trust-marquee-track-wrap:hover .trust-marquee-track {
  animation-play-state: paused;
}

@keyframes marqueeScroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(-100% / 3)); }
}

.trust-brand-item {
  display: inline-flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.6rem 1.2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.trust-brand-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(56, 189, 248, 0.35);
}

.brand-svg-symbol {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-svg-symbol svg {
  width: 100%;
  height: 100%;
}

.brand-meta {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.brand-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: #F1F5F9;
}

.brand-role {
  font-size: 0.74rem;
  color: #64748B;
}

.brand-live-pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 6px #10B981;
}

/* ================= 3. 浅色清爽区域：流量趋势与简约图表 ================= */
.light-section-contrast {
  background: #F8FAFC;
  padding: 6.5rem 0;
  color: #0F172A;
}

.section-header-center {
  text-align: center;
  max-width: 860px;
  margin: 0 auto 3.5rem;
}

.light-badge {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #0284C7;
  background: rgba(2, 132, 199, 0.08);
  border: 1px solid rgba(2, 132, 199, 0.2);
  padding: 0.28rem 0.9rem;
  border-radius: 9999px;
  margin-bottom: 1.2rem;
}

.light-title {
  font-size: 2.8rem;
  font-weight: 800;
  line-height: 1.25;
  color: #0F172A;
  margin: 0 0 1.2rem 0;
  letter-spacing: -0.6px;
}

.text-gradient-blue {
  background: linear-gradient(135deg, #0284C7 0%, #2563EB 50%, #7C3AED 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.light-sub {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #475569;
  margin: 0;
}

/* 简约数据图表卡片 */
.data-chart-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
  margin-bottom: 3.5rem;
}

.chart-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.chart-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 0.4rem 0;
}

.chart-sub-note {
  font-size: 0.85rem;
  color: #64748B;
}

.chart-legend-group {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: #334155;
  font-weight: 500;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-line {
  width: 24px;
  height: 3px;
  border-radius: 2px;
}

.line-cyan {
  background: linear-gradient(90deg, #38BDF8, #2563EB);
}

.line-gray {
  background: #94A3B8;
  border-top: 2px dashed #94A3B8;
  height: 0;
}

.svg-chart-container {
  width: 100%;
}

.trend-chart-svg {
  width: 100%;
  height: 280px;
  display: block;
}

.chart-x-axis {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 1px solid #E2E8F0;
  font-size: 0.82rem;
  color: #64748B;
  font-weight: 500;
}

.highlight-axis {
  color: #0284C7;
  font-weight: 700;
}

/* 4 阶段滑块 */
.light-shift-slider {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
}

.light-slider-tabs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.light-tab-btn {
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 1rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.light-tab-btn.active {
  background: #FFFFFF;
  border-color: #0284C7;
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12);
}

.light-tab-progress {
  width: 100%;
  height: 3px;
  background: #E2E8F0;
  border-radius: 2px;
  overflow: hidden;
}

.light-progress-bar {
  height: 100%;
  background: #0284C7;
  transition: width 0.05s linear;
}

.light-tab-meta {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.tab-idx {
  font-size: 0.78rem;
  font-weight: 800;
  color: #0284C7;
}

.tab-txt {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1E293B;
}

.light-slider-content {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 3rem;
  align-items: center;
}

.slide-tag-pill {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  color: #0284C7;
  background: #E0F2FE;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  margin-bottom: 0.8rem;
}

.slide-title-clean {
  font-size: 1.6rem;
  font-weight: 800;
  line-height: 1.35;
  color: #0F172A;
  margin: 0 0 1rem 0;
}

.slide-desc-clean {
  font-size: 1.02rem;
  line-height: 1.75;
  color: #475569;
  margin: 0 0 1.8rem 0;
}

.slide-bullets {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.bullet-row {
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  font-size: 0.94rem;
  color: #334155;
  font-weight: 500;
  line-height: 1.5;
}

.bullet-check-svg {
  width: 18px;
  height: 18px;
  color: #0284C7;
  flex-shrink: 0;
  margin-top: 2px;
}

.slide-stat-panel {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 2.2rem;
}

.stat-highlight-box {
  text-align: center;
  padding-bottom: 1.8rem;
  border-bottom: 1px solid #E2E8F0;
}

.stat-big-num {
  font-size: 3.6rem;
  font-weight: 900;
  color: #0284C7;
  line-height: 1;
  margin-bottom: 0.5rem;
  letter-spacing: -1px;
}

.stat-big-lbl {
  font-size: 0.92rem;
  font-weight: 600;
  color: #64748B;
}

.stat-compare-table {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding-top: 1.8rem;
  gap: 1rem;
}

.compare-col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.col-head {
  font-size: 0.78rem;
  color: #94A3B8;
  font-weight: 600;
}

.col-val {
  font-size: 0.92rem;
  font-weight: 700;
  color: #334155;
}

.compare-divider {
  width: 1px;
  height: 40px;
  background: #CBD5E1;
}

.text-brand {
  color: #0284C7;
}

/* ================= 4. 浅色区域：行业落地场景 ================= */
.light-solutions-section {
  background: #FFFFFF;
  padding: 6.5rem 0;
  border-top: 1px solid #E2E8F0;
  color: #0F172A;
}

.light-industry-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.ind-nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  padding: 0.75rem 1.4rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
  color: #475569;
  font-weight: 600;
  font-size: 0.94rem;
}

.ind-nav-btn:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
  color: #0F172A;
}

.ind-nav-btn.active {
  background: #0284C7;
  border-color: #0284C7;
  color: #FFFFFF;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
}

.ind-nav-icon {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.light-solution-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 12px 36px -12px rgba(0, 0, 0, 0.08);
}

.sol-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #E2E8F0;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.sol-category-badge {
  font-size: 0.8rem;
  font-weight: 700;
  color: #0284C7;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
  display: block;
}

.sol-headline {
  font-size: 1.7rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0;
  line-height: 1.35;
}

.btn-ind-try {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #0F172A;
  color: #FFFFFF;
  border: none;
  font-size: 0.92rem;
  font-weight: 600;
  padding: 0.65rem 1.4rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ind-try:hover {
  background: #1E293B;
  transform: translateY(-1px);
}

.sol-grid-layout {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 3.5rem;
}

.col-title-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #64748B;
  margin-bottom: 1rem;
}

.bar-svg {
  width: 16px;
  height: 16px;
  color: #0284C7;
}

.prompt-speech-bubble {
  background: #F8FAFC;
  border-left: 3px solid #0284C7;
  padding: 1.2rem 1.5rem;
  border-radius: 0 12px 12px 0;
  margin-bottom: 2rem;
}

.prompt-speech-bubble p {
  margin: 0;
  font-size: 1.02rem;
  font-weight: 600;
  color: #1E293B;
  line-height: 1.6;
}

.tactics-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.tactic-item {
  display: flex;
  gap: 1rem;
}

.tactic-num {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #E0F2FE;
  color: #0284C7;
  font-size: 0.82rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.tactic-t {
  font-size: 0.98rem;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 0.3rem;
}

.tactic-d {
  font-size: 0.88rem;
  line-height: 1.6;
  color: #64748B;
}

.stat-box-clean {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 2rem;
}

.box-tag {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748B;
  display: block;
  margin-bottom: 1.5rem;
}

.stat-progress-group {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
  margin-bottom: 1.8rem;
}

.prog-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.prog-label-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  color: #334155;
}

.prog-track {
  width: 100%;
  height: 6px;
  background: #E2E8F0;
  border-radius: 9999px;
  overflow: hidden;
}

.prog-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.6s ease;
}

.fill-blue { background: #0284C7; }
.fill-green { background: #10B981; }
.fill-purple { background: #8B5CF6; }

.text-blue { color: #0284C7; }
.text-green { color: #10B981; }
.text-purple { color: #8B5CF6; }

.verified-source-row {
  padding: 1rem 0;
  border-top: 1px solid #E2E8F0;
  border-bottom: 1px solid #E2E8F0;
  font-size: 0.82rem;
  margin-bottom: 1.5rem;
}

.source-tag {
  color: #94A3B8;
  font-weight: 600;
}

.source-items {
  color: #334155;
  font-weight: 500;
}

.client-quote {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.quote-svg {
  width: 24px;
  height: 24px;
  color: #CBD5E1;
}

.quote-text {
  font-size: 0.92rem;
  line-height: 1.7;
  color: #475569;
  font-style: italic;
  margin: 0;
}

.quote-author {
  font-size: 0.82rem;
  font-weight: 700;
  color: #0F172A;
}

/* ================= 5. 深色区域：认知工程技术架构 ================= */
.dark-tech-section {
  background: #080C14;
  padding: 7rem 0;
  position: relative;
  overflow: hidden;
  color: #F8FAFC;
}

.tech-glow-top {
  position: absolute;
  top: -100px;
  left: 50%;
  transform: translateX(-50%);
  width: 800px;
  height: 250px;
  background: radial-gradient(circle, rgba(25, 90, 254, 0.25) 0%, transparent 70%);
  filter: blur(80px);
  pointer-events: none;
}

.tech-badge {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #38BDF8;
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 0.28rem 0.9rem;
  border-radius: 9999px;
  margin-bottom: 1.2rem;
}

.tech-title {
  font-size: 2.8rem;
  font-weight: 800;
  line-height: 1.25;
  color: #FFFFFF;
  margin: 0 0 1.2rem 0;
  letter-spacing: -0.6px;
}

.tech-sub {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #94A3B8;
  margin: 0;
}

.arch-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.arch-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 2.2rem;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.arch-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(56, 189, 248, 0.4);
  transform: translateY(-4px);
}

.arch-badge-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.arch-idx {
  font-size: 0.76rem;
  font-weight: 800;
  color: #38BDF8;
  letter-spacing: 1px;
}

.arch-svg-icon {
  width: 24px;
  height: 24px;
}

.arch-name {
  font-size: 1.22rem;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 0.8rem 0;
}

.arch-desc {
  font-size: 0.88rem;
  line-height: 1.7;
  color: #94A3B8;
  margin: 0 0 1.8rem 0;
  flex: 1;
}

.arch-meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
}

.meta-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #38BDF8;
}

.meta-txt {
  font-size: 0.78rem;
  color: #CBD5E1;
  font-weight: 500;
}

/* ================= 6. 浅色区域：30天交付与 ROI 对比 ================= */
.light-delivery-section {
  background: #F8FAFC;
  padding: 6.5rem 0;
  color: #0F172A;
  border-top: 1px solid #E2E8F0;
}

.roadmap-timeline {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 4rem;
}

.phase-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 18px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
}

.phase-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.phase-tag {
  font-size: 0.75rem;
  font-weight: 800;
  color: #0284C7;
  letter-spacing: 0.5px;
}

.phase-time {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748B;
  background: #F1F5F9;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.phase-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 0.8rem 0;
  line-height: 1.4;
}

.phase-summary {
  font-size: 0.88rem;
  line-height: 1.65;
  color: #475569;
  margin: 0 0 1.5rem 0;
  flex: 1;
}

.phase-deliverable {
  padding-top: 1rem;
  border-top: 1px solid #F1F5F9;
  font-size: 0.82rem;
}

.deliv-lbl {
  color: #94A3B8;
  font-weight: 600;
  display: block;
  margin-bottom: 0.2rem;
}

.deliv-val {
  color: #0284C7;
  font-weight: 700;
}

.roi-table-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
}

.roi-card-header {
  margin-bottom: 2rem;
}

.roi-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 0.4rem 0;
}

.roi-sub {
  font-size: 0.92rem;
  color: #64748B;
}

.roi-clean-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.roi-clean-table th {
  padding: 1rem 1.2rem;
  font-size: 0.88rem;
  font-weight: 700;
  color: #475569;
  border-bottom: 2px solid #E2E8F0;
  background: #F8FAFC;
}

.th-highlight {
  color: #0284C7 !important;
  background: #E0F2FE !important;
}

.roi-clean-table td {
  padding: 1.2rem;
  font-size: 0.92rem;
  color: #334155;
  border-bottom: 1px solid #F1F5F9;
  line-height: 1.6;
}

.td-dim {
  font-weight: 700;
  color: #0F172A;
}

.td-strong {
  font-weight: 700;
  color: #0284C7;
  background: rgba(2, 132, 199, 0.03);
}

/* ================= 7. 浅色区域：常见问题 ================= */
.light-faq-section {
  background: #FFFFFF;
  padding: 6.5rem 0;
  color: #0F172A;
}

.faq-accordion-list {
  max-width: 920px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-clean-item {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 1.4rem 1.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.faq-clean-item:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
}

.faq-clean-item.open {
  background: #FFFFFF;
  border-color: #0284C7;
  box-shadow: 0 4px 16px rgba(2, 132, 199, 0.08);
}

.faq-q-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.faq-q-symbol {
  font-size: 1.1rem;
  font-weight: 900;
  color: #0284C7;
}

.faq-q-title {
  flex: 1;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0F172A;
}

.faq-toggle-icon {
  font-size: 1.4rem;
  color: #94A3B8;
  font-weight: 300;
}

.faq-a-body {
  padding-top: 1rem;
  margin-top: 1rem;
  border-top: 1px solid #F1F5F9;
}

.faq-a-body p {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.8;
  color: #475569;
}

/* ================= 8. 暗夜宇宙光晕 CTA Banner ================= */
.bottom-cta-banner {
  position: relative;
  background: #080C14;
  padding: 7rem 1.5rem;
  overflow: hidden;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cta-cosmic-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 900px;
  height: 400px;
  background: radial-gradient(circle, rgba(25, 90, 254, 0.3) 0%, rgba(124, 58, 237, 0.15) 50%, transparent 70%);
  filter: blur(90px);
  pointer-events: none;
}

.cta-inner {
  position: relative;
  z-index: 2;
  max-width: 820px;
  margin: 0 auto;
}

.badge-tag-orange {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 700;
  color: #FB923C;
  background: rgba(251, 146, 60, 0.1);
  border: 1px solid rgba(251, 146, 60, 0.3);
  padding: 0.3rem 1rem;
  border-radius: 9999px;
  margin-bottom: 1.5rem;
}

.cta-headline {
  font-size: 2.8rem;
  font-weight: 900;
  line-height: 1.3;
  color: #FFFFFF;
  margin: 0 0 1.2rem 0;
  letter-spacing: -0.6px;
}

.cta-sub {
  font-size: 1.1rem;
  line-height: 1.75;
  color: #94A3B8;
  margin: 0 0 2.8rem 0;
}

.cta-action-box {
  display: flex;
  justify-content: center;
}

.cta-input-wrap {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 680px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9999px;
  padding: 0.45rem 0.5rem 0.45rem 1.4rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.cta-input-wrap input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 0.98rem;
}

.cta-input-wrap input::placeholder {
  color: #64748B;
}

.btn-cta-submit {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #195AFE 0%, #3B82F6 50%, #7C3AED 100%);
  border: none;
  border-radius: 9999px;
  padding: 0.8rem 1.8rem;
  color: #ffffff;
  font-size: 0.94rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  box-shadow: 0 0 24px rgba(25, 90, 254, 0.5);
  transition: all 0.2s;
}

.btn-cta-submit:hover {
  transform: scale(1.03);
  box-shadow: 0 0 32px rgba(25, 90, 254, 0.75);
}

.btn-arrow {
  width: 16px;
  height: 16px;
}

/* ================= 9. 黑曜石页脚 ================= */
.landing-footer {
  background: #04070D;
  padding: 5rem 0 3rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  color: #64748B;
}

.footer-inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.footer-top-row {
  display: grid;
  grid-template-columns: 1.2fr 1.8fr;
  gap: 4rem;
  margin-bottom: 4rem;
}

.logo-text-footer {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  margin-bottom: 1.2rem;
}

.brand-name {
  font-size: 1.3rem;
  font-weight: 800;
  color: #FFFFFF;
}

.brand-sub {
  font-size: 0.85rem;
  color: #60A5FA;
  font-weight: 600;
}

.footer-desc {
  font-size: 0.9rem;
  line-height: 1.7;
  color: #64748B;
  margin: 0;
  max-width: 380px;
}

.footer-links-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.links-col {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.links-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #F1F5F9;
  margin-bottom: 0.4rem;
}

.links-col a {
  color: #64748B;
  text-decoration: none;
  font-size: 0.86rem;
  transition: color 0.2s;
}

.links-col a:hover {
  color: #38BDF8;
}

.footer-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.82rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.legal-and-portal {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.legal-text {
  color: #475569;
}

.portal-sep {
  color: #334155;
}

.sales-portal-link {
  color: #475569;
  text-decoration: none;
  font-size: 0.8rem;
  transition: color 0.2s;
}

.sales-portal-link:hover {
  color: #38BDF8;
}

/* ================= 10. 企业 AI 体检预约弹窗样式 (Lead Modal) ================= */
/* ================= 简约大气商务风 · 企业顾问预约弹窗 (Similarweb / Stripe 风格) ================= */
.lead-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  box-sizing: border-box;
}

.lead-modal-card {
  position: relative;
  width: 100%;
  max-width: 860px;
  background: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.3), 0 0 1px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: grid;
  grid-template-columns: 340px 1fr;
  box-sizing: border-box;
  text-align: left;
}

/* 关闭按钮 */
.modal-close-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #F1F5F9;
  color: #64748B;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  z-index: 10;
}

.modal-close-btn:hover {
  background: #E2E8F0;
  color: #0F172A;
}

.modal-close-btn svg {
  width: 16px;
  height: 16px;
}

/* 左侧栏：品牌价值亮点 */
.modal-sidebar {
  background: #F8FAFC;
  border-right: 1px solid #E2E8F0;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

.sidebar-header {
  margin-bottom: 24px;
}

.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #195AFE;
  background: #EEF2FF;
  padding: 4px 10px;
  border-radius: 6px;
  margin-bottom: 16px;
  letter-spacing: 0.3px;
}

.sidebar-title {
  font-size: 20px;
  font-weight: 700;
  color: #0F172A;
  line-height: 1.35;
  margin: 0 0 10px 0;
  letter-spacing: -0.3px;
}

.sidebar-desc {
  font-size: 13px;
  color: #64748B;
  line-height: 1.6;
  margin: 0;
}

.benefit-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-bottom: 24px;
}

.benefit-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.benefit-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #E0E7FF;
  color: #195AFE;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
}

.benefit-icon svg {
  width: 12px;
  height: 12px;
}

.benefit-text h4 {
  font-size: 13px;
  font-weight: 600;
  color: #1E293B;
  margin: 0 0 3px 0;
}

.benefit-text p {
  font-size: 12px;
  color: #64748B;
  line-height: 1.5;
  margin: 0;
}

.sidebar-footer {
  border-top: 1px solid #E2E8F0;
  padding-top: 18px;
}

.trust-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #475569;
  font-weight: 500;
}

.trust-badge svg {
  width: 16px;
  height: 16px;
  color: #10B981;
  flex-shrink: 0;
}

/* 右侧主表单区 */
.modal-main {
  padding: 40px 36px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.form-header {
  margin-bottom: 24px;
}

.form-title {
  font-size: 20px;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 6px 0;
  letter-spacing: -0.3px;
}

.form-subtitle {
  font-size: 13px;
  color: #64748B;
  margin: 0;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.req {
  color: #EF4444;
  margin-left: 2px;
}

.field-input {
  width: 100%;
  height: 42px;
  padding: 0 14px;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  font-size: 14px;
  color: #0F172A;
  background: #FFFFFF;
  box-sizing: border-box;
  transition: all 0.15s ease;
  outline: none;
}

.field-input:focus {
  border-color: #195AFE;
  box-shadow: 0 0 0 3px rgba(25, 90, 254, 0.12);
}

.field-input::placeholder {
  color: #9CA3AF;
}

/* 交流方式单选选项 */
.demo-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 2px;
}

.demo-option {
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 10px 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s ease;
  background: #FAFAFA;
}

.demo-option:hover {
  border-color: #CBD5E1;
  background: #F1F5F9;
}

.demo-option.selected {
  border-color: #195AFE;
  background: #EEF2FF;
}

.demo-option-title {
  font-size: 13px;
  font-weight: 600;
  color: #1E293B;
  display: block;
  margin-bottom: 2px;
}

.demo-option.selected .demo-option-title {
  color: #195AFE;
}

.demo-option-sub {
  font-size: 11px;
  color: #64748B;
  display: block;
}

.demo-option.selected .demo-option-sub {
  color: #4F46E5;
}

/* 提交按钮 */
.btn-submit {
  width: 100%;
  height: 46px;
  background: #195AFE;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 6px;
}

.btn-submit:hover:not(:disabled) {
  background: #0D47E0;
  box-shadow: 0 4px 12px rgba(25, 90, 254, 0.25);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.privacy-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 10px;
  font-size: 12px;
  color: #64748B;
}

.privacy-footer svg {
  width: 14px;
  height: 14px;
  color: #94A3B8;
  flex-shrink: 0;
}

/* 成功状态卡片 */
.modal-success-card {
  display: block;
  max-width: 560px;
  padding: 48px 40px;
  text-align: center;
}

.success-icon-box {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  color: #059669;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px auto;
}

.success-icon-box svg {
  width: 32px;
  height: 32px;
}

.success-title {
  font-size: 22px;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 8px 0;
  letter-spacing: -0.3px;
}

.success-desc {
  font-size: 14px;
  color: #64748B;
  line-height: 1.6;
  max-width: 440px;
  margin: 0 auto 28px auto;
}

.success-summary {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 16px 20px;
  text-align: left;
  margin-bottom: 24px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 13px;
  border-bottom: 1px dashed #E2E8F0;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-label {
  color: #64748B;
}

.summary-val {
  color: #0F172A;
  font-weight: 600;
}

.hotline-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
  margin-bottom: 24px;
}

.hotline-banner strong {
  color: #195AFE;
}

.btn-done {
  width: 100%;
  height: 44px;
  background: #0F172A;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-done:hover {
  background: #1E293B;
}

/* 弹窗移动端适配 */
@media (max-width: 768px) {
  .lead-modal-card {
    grid-template-columns: 1fr;
    max-height: 90vh;
    overflow-y: auto;
  }
  .modal-sidebar {
    padding: 24px 20px;
    border-right: none;
    border-bottom: 1px solid #E2E8F0;
  }
  .modal-main {
    padding: 24px 20px;
  }
  .field-row {
    grid-template-columns: 1fr;
  }
  .demo-options {
    grid-template-columns: 1fr;
  }
  .modal-success-card {
    padding: 32px 20px;
  }
}

/* ================= 响应式处理 ================= */
@media (max-width: 1200px) {
  .console-body-grid { grid-template-columns: 1fr; gap: 1rem; }
  .hero-headline { font-size: 2.8rem; }
}

@media (max-width: 1024px) {
  .hero-headline { font-size: 2.6rem; }
  .light-title, .tech-title, .cta-headline { font-size: 2.2rem; }
  .arch-grid, .roadmap-timeline { grid-template-columns: repeat(2, 1fr); }
  .light-slider-tabs { grid-template-columns: repeat(2, 1fr); }
  .light-slider-content { grid-template-columns: 1fr; }
  .sol-grid-layout { grid-template-columns: 1fr; }
  .footer-top-row { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .nav-links { display: none; }
  .hero-section { min-height: auto; padding-top: 2rem; }
  .hero-headline { font-size: 2.1rem; }
  .arch-grid, .roadmap-timeline { grid-template-columns: 1fr; }
  .light-slider-tabs { grid-template-columns: 1fr; }
  .search-input-box { flex-direction: column; border-radius: 18px; padding: 1rem; gap: 0.8rem; }
  .search-divider { display: none; }
  .search-input-field { width: 100%; }
  .btn-search-action { width: 100%; }
  .cta-input-wrap { flex-direction: column; border-radius: 18px; padding: 1rem; gap: 0.8rem; }
  .btn-cta-submit { width: 100%; }
  .footer-links-group { grid-template-columns: 1fr 1fr; }
  .console-top-bar { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
  .bar-right { flex-direction: column; align-items: flex-start; gap: 0.4rem; }
  .form-row-two { grid-template-columns: 1fr; }
  .demo-type-grid { grid-template-columns: 1fr; }
}
</style>
