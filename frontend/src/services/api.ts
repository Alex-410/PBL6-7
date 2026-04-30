import axios from 'axios';

const rawApi = axios.create({
  baseURL: 'http://localhost:8080/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

rawApi.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

rawApi.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    return Promise.reject(error);
  }
);

const api = rawApi as unknown as {
  get: <T = any>(url: string, config?: any) => Promise<T>;
  post: <T = any>(url: string, data?: any, config?: any) => Promise<T>;
  put: <T = any>(url: string, data?: any, config?: any) => Promise<T>;
  delete: <T = any>(url: string, config?: any) => Promise<T>;
};

export const authApi = {
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data)
};

export const activityApi = {
  list: (status?: string) => api.get('/activities', { params: status ? { status } : {} }),
  detail: (id: number) => api.get(`/activities/${id}`),
  create: (data: any) => api.post('/activities', data),
  audit: (id: number, action: 'approve' | 'reject', comment?: string) =>
    api.put(`/activities/${id}/audit`, null, { params: { action, comment } }),
  delete: (id: number) => api.delete(`/activities/${id}`),
};

export const registrationApi = {
  register: (activityId: number) => api.post('/registrations', null, { params: { activityId } }),
  cancel: (id: number) => api.delete(`/registrations/${id}`),
  myRegistrations: () => api.get('/registrations/me'),
  byActivity: (activityId: number) => api.get(`/registrations/activity/${activityId}`),
};

export default api;
