import { createRouter, createWebHashHistory } from 'vue-router';

const HomeLanding = () => import('../views/HomeLanding.vue');
const AiReport = () => import('../views/AiReport.vue');
const DiagnosticReport = () => import('../views/DiagnosticReport.vue');

const routes = [
  {
    path: '/',
    name: 'HomeLanding',
    component: HomeLanding,
    meta: { title: '蜉蝣小宝 · GEO 新一代生成式 AI 搜索引擎商业认知与拓客中枢' }
  },
  {
    path: '/console',
    name: 'ConsoleRedirect',
    beforeEnter() {
      window.location.href = '/console.html';
    }
  },
  {
    path: '/diagnostic',
    name: 'DiagnosticRedirect',
    beforeEnter() {
      window.location.href = '/console.html';
    }
  },
  {
    path: '/ai_report',
    name: 'AiReport',
    component: AiReport,
    meta: { title: '蜉蝣小宝 · GEO 智能搜索排名与推荐优化看板' }
  },
  {
    path: '/diagnostic_report',
    name: 'DiagnosticReport',
    component: DiagnosticReport,
    meta: { title: '蜉蝣小宝 · 企业 AI 搜索引擎可见度诊断体检书' }
  },
  {
    path: '/diagnostic/report/:code?',
    name: 'DiagnosticReportParam',
    component: DiagnosticReport,
    meta: { title: '蜉蝣小宝 · 企业 AI 搜索引擎可见度诊断体检书' }
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});

export default router;
