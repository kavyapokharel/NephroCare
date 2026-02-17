import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.144.131:8000/api/",
  timeout: 100000,
});

export default api;
