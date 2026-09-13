import { createRouter, createWebHashHistory } from 'vue-router';
import DiagnosticConsole from '../views/DiagnosticConsole.vue';
import DiagnosticReport from '../views/DiagnosticReport.vue';
import AiReport from '../views/AiReport.vue';
import SalesConsole from '../views/SalesConsole.vue';

const routes = [
  {
    path: '/',
    name: 'DiagnosticConsole',
    component: DiagnosticConsole,
    meta: { title: '蜉蝣小宝 · 企业 AI 搜索引擎可见度 · 售前全网诊断工作台' }
  },
  {
    path: '/diagnostic',
    redirect: '/'
  },
  {
    path: '/console',
    redirect: '/'
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
  },
  {
    path: '/sales',
    name: 'SalesConsole',
    component: SalesConsole,
    meta: { title: '蜉蝣小宝 · 销售拓客与实战演示台' }
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
