import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

export default {
  // 报表公开端接口 (带 code 参数)
  getCompanyInfo(code) {
    return apiClient.get('/report/company-info', { params: { code } });
  },
  getSummary(code) {
    return apiClient.get('/report/summary', { params: { code } });
  },
  getPlatforms(code, taskType = 0) {
    return apiClient.get('/report/platforms', { params: { code, taskType } });
  },
  getTopKeywords(code) {
    return apiClient.get('/report/top-keywords', { params: { code } });
  },
  getRankings(code, data) {
    return apiClient.post('/report/rankings', data, { params: { code } });
  },
  getMatchDetail(code, rid) {
    return apiClient.get(`/report/match-detail/${rid}`, { params: { code } });
  },
  getTrend(code, days = 30) {
    return apiClient.get('/report/trend', { params: { code, days } });
  },
  
  // 售前体检引擎接口 (核心拓客开单，多大模型全网深度探测耗时较长，专属放宽至 180s)
  runDiagnostic(payload) {
    return apiClient.post('/diagnostic/run', payload, {
      timeout: 180000
    });
  },
  getDiagnosticReport(code) {
    return apiClient.get(`/diagnostic/${code}`);
  },
  getRecentDiagnostics() {
    return apiClient.get('/diagnostic/recent/list');
  },
  generateIntentQueries(payload) {
    return apiClient.post('/diagnostic/generate_queries', payload, {
      timeout: 120000
    });
  },
  getModelsBalance() {
    return apiClient.get('/diagnostic/models/balance');
  },
  clearRecentDiagnostics() {
    return apiClient.delete('/diagnostic/recent/clear', {
      headers: {
        'X-Console-Token': 'xunling-console-secure-access-2026'
      }
    });
  },

  // 基础管理接口
  getCompanies() {
    return apiClient.get('/companies/');
  },
  quickAudit(payload) {
    return apiClient.post('/companies/quick-audit', payload);
  }
};
