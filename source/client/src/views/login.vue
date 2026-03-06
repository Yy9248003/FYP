<template>
    <div class="login-body">
        <div class="login-container">
            <div class="login-card">
                <div class="login-header">
                    <h2>在线考试管理系统</h2>
                    <p>欢迎使用智能考试平台</p>
                </div>
                <div class="login-form">
                    <Form ref="loginForm" :rules="rules" :model="loginForm" :label-width="0">
                        <FormItem prop="userName">
                            <Input 
                                v-model="loginForm.userName" 
                                placeholder="请输入您的账号"
                                size="large"
                                prefix="ios-person"
                                class="login-input">
                            </Input>
                        </FormItem>
                        <FormItem prop="passWord">
                            <Input 
                                type="password" 
                                v-model="loginForm.passWord" 
                                placeholder="请输入您的密码"
                                size="large"
                                prefix="ios-lock"
                                class="login-input">
                            </Input>
                        </FormItem>
                        <FormItem style="margin-top: 30px;">
                            <Button 
                                style="width: 100%; height: 45px; font-size: 16px;" 
                                @click="submitForm('loginForm')"  
                                class="login-btn" 
                                type="primary">
                                登录系统
                            </Button>
                        </FormItem>
                    </Form>
                </div>
                <div class="login-footer">
                    <p>© 2024 在线考试管理系统 - 让学习更高效</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.login-body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}

.login-body::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url(../assets/2.jpg) center/cover;
    opacity: 0.1;
    z-index: 1;
}

.login-container {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 400px;
    padding: 20px;
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
    text-align: center;
    margin-bottom: 30px;
}

.login-header h2 {
    color: #333;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.login-header p {
    color: #666;
    font-size: 14px;
    margin: 0;
}

.login-form {
    margin-bottom: 20px;
}

.login-input {
    border-radius: 10px;
    border: 2px solid #e8eaec;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.8);
}

.login-input:hover {
    border-color: #667eea;
}

.login-input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    background: #fff;
}

.login-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.login-footer {
    text-align: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

.login-footer p {
    color: #999;
    font-size: 12px;
    margin: 0;
}

/* 响应式设计 */
@media (max-width: 480px) {
    .login-container {
        padding: 10px;
    }
    
    .login-card {
        padding: 30px 20px;
    }
    
    .login-header h2 {
        font-size: 24px;
    }
}
</style>

<script>
import initMenu from "../utils/menus.js";
import { login } from '../api/index.js';
export default {
    data() {

        return {
            loginForm: {
                userName: '',
                passWord: '',
            },
            rules: {
                userName: [
                    { required: true, message: '用户账号必须输入', trigger: 'blur' }
                ],
                passWord: [
                    { required: true, message: '用户密码必须输入', trigger: 'blur' }
                ],
            }
        }
    },
    methods: {
        submitForm (formName) {

            this.$refs[formName].validate((valid) => {
                if (valid) {

                    login(this.loginForm).then(res => {
                        
                        if(res.code == 0){

                            this.$store.commit('setToken', res.data.token);
                            sessionStorage.setItem("token", res.data.token);
                            initMenu(this.$router, this.$store);
                            this.$router.push('/welcome');
                        }else{

                            this.$Message.warning(res.msg);
                        }
                    });
                } else {

                    return false;
                }
            })
        }
    },
}
</script>
