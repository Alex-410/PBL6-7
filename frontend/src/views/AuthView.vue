<template>
  <div class="auth-container">
    <div class="auth-card" :class="{ 'hover-left': hoverSide === 'left', 'hover-right': hoverSide === 'right' }">
      <div 
        class="side left-side"
        @mouseenter="hoverSide = 'left'"
        @mouseleave="hoverSide = null"
      >
        <div class="side-content">
          <div class="side-overlay" :class="{ active: hoverSide === 'left' }"></div>
          <div class="form-wrapper" :class="{ active: hoverSide === 'left' }">
            <h2 class="side-title">注册账号</h2>
            <div v-if="hoverSide === 'left'" class="form-container">
              <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef" label-width="0">
                <el-form-item prop="username">
                  <el-input 
                    v-model="registerForm.username" 
                    placeholder="用户名" 
                    prefix-icon="User"
                    size="large"
                  />
                </el-form-item>
                <el-form-item prop="email">
                  <el-input 
                    v-model="registerForm.email" 
                    placeholder="邮箱" 
                    prefix-icon="Message"
                    size="large"
                  />
                </el-form-item>
                <el-form-item prop="phone">
                  <el-input 
                    v-model="registerForm.phone" 
                    placeholder="手机号" 
                    prefix-icon="Phone"
                    size="large"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input 
                    v-model="registerForm.password" 
                    type="password" 
                    placeholder="密码" 
                    prefix-icon="Lock"
                    size="large"
                    show-password
                  />
                </el-form-item>
                <el-form-item prop="confirmPassword">
                  <el-input 
                    v-model="registerForm.confirmPassword" 
                    type="password" 
                    placeholder="确认密码" 
                    prefix-icon="Lock"
                    size="large"
                    show-password
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" size="large" class="submit-btn" @click="handleRegister" :loading="registerLoading">
                    立即注册
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div 
        class="side right-side"
        @mouseenter="hoverSide = 'right'"
        @mouseleave="hoverSide = null"
      >
        <div class="side-content">
          <div class="side-overlay" :class="{ active: hoverSide === 'right' }"></div>
          <div class="form-wrapper" :class="{ active: hoverSide === 'right' }">
            <h2 class="side-title">登录账号</h2>
            <div v-if="hoverSide === 'right'" class="form-container">
              <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="0">
                <el-form-item prop="username">
                  <el-input 
                    v-model="loginForm.username" 
                    placeholder="用户名" 
                    prefix-icon="User"
                    size="large"
                  />
                </el-form-item>
                <el-form-item prop="password">
                  <el-input 
                    v-model="loginForm.password" 
                    type="password" 
                    placeholder="密码" 
                    prefix-icon="Lock"
                    size="large"
                    show-password
                  />
                </el-form-item>
                <el-form-item>
                  <div class="form-options">
                    <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
                    <a href="#" class="forgot-link">忘记密码？</a>
                  </div>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" size="large" class="submit-btn" @click="handleLogin" :loading="loginLoading">
                    立即登录
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const hoverSide = ref<string | null>(null)
const registerFormRef = ref<FormInstance>()
const loginFormRef = ref<FormInstance>()
const registerLoading = ref(false)
const loginLoading = ref(false)

const registerForm = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      registerLoading.value = true
      try {
        ElMessage.success('注册功能开发中...')
      } catch (error) {
        ElMessage.error('注册失败')
      } finally {
        registerLoading.value = false
      }
    }
  })
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loginLoading.value = true
      try {
        ElMessage.success('登录功能开发中...')
      } catch (error) {
        ElMessage.error('登录失败')
      } finally {
        loginLoading.value = false
      }
    }
  })
}
</script>

<style scoped lang="scss">
.auth-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #f5f7fa;
}

.auth-card {
  width: 100%;
  max-width: 900px;
  height: 560px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  display: flex;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);

  &.hover-left {
    .left-side {
      flex: 0 0 70%;
      transform: scale(1.02);
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
    }
    .right-side {
      flex: 0 0 30%;
    }
  }

  &.hover-right {
    .left-side {
      flex: 0 0 30%;
    }
    .right-side {
      flex: 0 0 70%;
      transform: scale(1.02);
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
    }
  }
}

.side {
  flex: 0 0 50%;
  position: relative;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  &.left-side {
    background: linear-gradient(135deg, #eef2f7 0%, #dfe7f0 100%);
    clip-path: polygon(0 0, 100% 0, 85% 100%, 0 100%);
  }

  &.right-side {
    background: linear-gradient(135deg, #f8f9fa 0%, #f1f3f5 100%);
    clip-path: polygon(15% 0, 100% 0, 100% 100%, 0 100%);
  }
}

.divider {
  position: absolute;
  left: 50%;
  top: 10px;
  bottom: 10px;
  width: 1.5px;
  background: #495057;
  transform: translateX(-50%) skewX(-15deg);
  z-index: 10;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  transition: left 0.5s cubic-bezier(0.4, 0, 0.2, 1);

  .auth-card.hover-left & {
    left: 70%;
  }

  .auth-card.hover-right & {
    left: 30%;
  }
}

.side-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 60px 40px;
}

.side-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease;

  &.active {
    opacity: 1;
  }
}

.form-wrapper {
  z-index: 5;
  text-align: center;
  width: 100%;
  max-width: 350px;
  transition: all 0.3s ease;
  opacity: 0.9;

  &.active {
    opacity: 1;
  }
}

.side-title {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 18px;
  font-weight: 500;
  color: #212529;
  margin-bottom: 40px;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.form-container {
  width: 100%;
  transition: opacity 0.3s ease, transform 0.3s ease;
  opacity: 0;
  transform: translateY(10px);

  .form-wrapper.active & {
    opacity: 1;
    transform: translateY(0);
  }
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-input__wrapper) {
  border-radius: 4px;
  padding: 8px 15px;
  background: white;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
  box-shadow: none;

  &:hover {
    border-color: #adb5bd;
  }

  &.is-focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }
}

.submit-btn {
  width: 100%;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  height: 48px;
  margin-top: 15px;
  background: #2563eb;
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
  transition: all 0.3s ease;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    background: #1d4ed8 !important;
    color: white !important;
  }
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 15px;
}

.forgot-link {
  color: #495057;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  &:hover {
    color: #2563eb;
    text-decoration: underline;
  }
}

:deep(.el-checkbox__label) {
  color: #495057;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
}

:deep(.el-checkbox__inner) {
  background: white;
  border: 1px solid #dee2e6;

  &:hover {
    border-color: #2563eb;
  }
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #2563eb;
  border-color: #2563eb;
}

:deep(.el-input__placeholder) {
  color: #adb5bd;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
