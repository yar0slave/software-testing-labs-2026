import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500'], checks: ['rate==1'] },
};
export default function () {
  const response = http.get(`${__ENV.BASE_URL || 'http://127.0.0.1:8765'}/api/health`);
  check(response, {
    'status 200': r => r.status === 200,
    'body status ok': r => { try { return r.json('status') === 'ok'; } catch (_) { return false; } },
  });
  sleep(0.1);
}
