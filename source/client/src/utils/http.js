import axios from 'axios'
import qs from 'qs'

import { Notice } from "view-ui-plus";

// 从环境变量获取API地址，如果没有则使用默认值
const getBaseURL = () => {
	// 优先使用环境变量（Docker环境）
	if (process.env.VUE_APP_API_BASE_URL) {
		return `${process.env.VUE_APP_API_BASE_URL}/api`
	}
	// 开发环境：使用代理（vue.config.js中配置）
	// 生产环境：直接使用完整URL
	if (process.env.NODE_ENV === 'production') {
		return 'http://127.0.0.1:8000/api'
	}
	// 开发环境使用代理，baseURL设为相对路径
	return '/api'
}

const service = axios.create({
	baseURL: getBaseURL(),
	timeout: 30000,  // 增加超时时间到30秒
	withCredentials: false  // 开发环境不需要credentials
})

service.interceptors.request.use(config => {
	
    if(config.method === "post"){
        // 若是 FormData 则不做 qs 序列化（用于文件上传/导出）
        const isFormData = (typeof FormData !== 'undefined') && (config.data instanceof FormData);
        if(!isFormData){
            // 允许通过 config.headers['Content-Type'] = 'application/json' 发送 JSON
            const isJson = (config.headers && String(config.headers['Content-Type']).includes('application/json'))
            if (!isJson){
                config.data = qs.stringify(config.data,  { indices: false });
            }
        }
    }
	
	return config;
}, error => {
	Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
    success => {
        // 文件下载/纯文本透传
        if (typeof success.data === 'string' || success.request?.responseType === 'blob'){
            return success;
        }

        if (success.data.code == 0) {
            return success.data;
        }else if (success.data.code == 1){
            return success.data;
        } else {
            // 对退出接口做静默处理：即使后端返回非0也不弹错，直接视为成功退出
            const url = success?.config?.url || '';
            if (url.includes('/exit/')) {
                return { code: 0, msg: '退出成功', data: {} };
            }
            Notice.error({
                duration: 3,
                title: success.data.msg
            });
            return Promise.reject(success.data);
		}
	},
	error => {
        // 对退出接口做静默处理：网络异常也按成功退出处理
        const url = error?.config?.url || '';
        if (url.includes('/exit/')) {
            return Promise.resolve({ code: 0, msg: '退出成功', data: {} });
        }
        
        // 详细的错误信息
        let errorMessage = '系统异常，请求中断';
        
        if (error.code === 'ECONNABORTED') {
            errorMessage = '请求超时，请检查网络连接或稍后重试';
        } else if (error.message === 'Network Error') {
            errorMessage = '网络连接失败，请检查：\n1. 后端服务是否已启动（http://127.0.0.1:8000）\n2. 防火墙是否阻止连接\n3. 端口是否被占用';
        } else if (error.response) {
            // 服务器返回了错误响应
            const status = error.response.status;
            if (status === 404) {
                errorMessage = '请求的接口不存在（404）';
            } else if (status === 500) {
                errorMessage = '服务器内部错误（500），请查看后端日志';
            } else if (status === 403) {
                errorMessage = '访问被拒绝（403），请检查权限';
            } else {
                errorMessage = `服务器错误（${status}）`;
            }
        } else if (error.request) {
            // 请求已发出但没有收到响应
            errorMessage = '无法连接到服务器，请确认后端服务已启动';
        }
        
        console.error('API请求错误:', {
            message: error.message,
            code: error.code,
            config: error.config,
            response: error.response,
            request: error.request
        });
        
        Notice.error({
            duration: 5,
            title: errorMessage,
            desc: error.message || '请检查控制台获取详细信息'
        });
        
        return Promise.reject(error);
	}
)

export default service
