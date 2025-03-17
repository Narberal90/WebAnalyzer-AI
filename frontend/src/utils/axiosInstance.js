import axios from "axios";
import { BASE_URL } from "../config";

const axiosInstance = axios.create({
  baseURL: BASE_URL,
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.log("Token expired or invalid. Redirecting to login...");
      localStorage.removeItem("access_token");
      
      window.location.href = "/";
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
