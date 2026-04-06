import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.3.27:8000/api/v1"
});

api.interceptors.request.use((config) => {
  if (global.token) {
    config.headers.Authorization = `Bearer ${global.token}`;
  }
  return config;
});

export default api;