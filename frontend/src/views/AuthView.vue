<template>
  <div class="login-page">
    <div class="login-brand">
      <h1>集趣</h1>
      <p class="tagline">校园活动一站式管理平台<br>发现 · 参与 · 记录你的每一次校园体验</p>
      <div class="edition">CAMPUS EDITION · 2026</div>
    </div>
    <div class="login-right">
      <div class="login-form-container">
        <h2 v-if="isLogin">登录</h2>
        <h2 v-else>注册</h2>
        <p class="subtitle" v-if="isLogin">使用你的平台账号登录</p>
        <p class="subtitle" v-else>创建你的平台账号</p>

        <!-- 登录表单 -->
        <template v-if="isLogin">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" id="login-user" v-model="loginForm.username" placeholder="请输入用户名" autocomplete="off">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" id="login-pass" v-model="loginForm.password" placeholder="请输入密码">
          </div>
          <button class="btn btn-primary" @click="handleLogin" :disabled="loginLoading">
            {{ loginLoading ? '登录中...' : '登 录' }}
          </button>
          <div style="text-align:center;margin-top:20px">
            <span class="mono text-sm text-muted">还没有账号？</span>
            <a href="#" class="mono text-sm" @click.prevent="isLogin = false" style="margin-left:6px">立即注册 →</a>
          </div>
        </template>

        <!-- 注册表单 -->
        <template v-else>
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="registerForm.username" placeholder="请输入用户名（3-20个字符）" autocomplete="off">
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input type="email" v-model="registerForm.email" placeholder="请输入邮箱">
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input type="tel" v-model="registerForm.phone" placeholder="请输入手机号">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="registerForm.password" placeholder="请输入密码（至少6位）">
          </div>
          <div class="form-group">
            <label>确认密码</label>
            <input type="password" v-model="registerForm.confirmPassword" placeholder="请再次输入密码">
          </div>
          <button class="btn btn-primary" @click="handleRegister" :disabled="registerLoading">
            {{ registerLoading ? '注册中...' : '立即注册' }}
          </button>
          <div style="text-align:center;margin-top:20px">
            <span class="mono text-sm text-muted">已有账号？</span>
            <a href="#" class="mono text-sm" @click.prevent="isLogin = true" style="margin-left:6px">返回登录 →</a>
          </div>
        </template>

        <!-- 演示账号 -->
        <div class="demo-accounts" v-if="isLogin">
          <div class="demo-accounts-header">演示账号 · 点击自动填入</div>
          <div class="demo-account" v-for="acc in demoAccounts" :key="acc.username" @click="fillLogin(acc)">
            <div>
              <div class="role-name">{{ acc.name }} <span style="color:var(--ink-muted);font-weight:400">· {{ acc.role }}</span></div>
              <div class="creds">{{ acc.username }} / {{ acc.password }}</div>
            </div>
            <span class="fill-hint">点击填入 →</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()
const isLogin = ref(true)
const loginLoading = ref(false)
const registerLoading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
})

const registerForm = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const demoAccounts = [
  { name: '张小明', role: '学生', username: '20230102526', password: '102526' },
  { name: '李管理', role: '管理员', username: 'testuser', password: 'password123' },
  { name: '王组织', role: '活动发布者', username: 'test11', password: '123456' },
]

function fillLogin(acc: typeof demoAccounts[0]) {
  loginForm.username = acc.username
  loginForm.password = acc.password
}

function showToast(msg: string, type: 'success' | 'error' = 'success') {
  const el = document.createElement('div')
  el.className = `toast toast-${type}`
  el.innerHTML = `${type === 'success' ? '✓' : '✕'} ${msg}`
  document.body.appendChild(el)
  setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity .3s'; setTimeout(() => el.remove(), 300) }, 2500)
}

async function handleLogin() {
  if (!loginForm.username || !loginForm.password) {
    showToast('请输入用户名和密码', 'error')
    return
  }
  loginLoading.value = true
  try {
    const response = await authApi.login(loginForm)
    if (response.code === 200) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data))
      showToast('登录成功')
      router.push('/dashboard')
    } else {
      showToast(response.message || '登录失败', 'error')
    }
  } catch {
    showToast('登录失败，请检查网络连接', 'error')
  } finally {
    loginLoading.value = false
  }
}

async function handleRegister() {
  if (!registerForm.username || !registerForm.password) {
    showToast('请填写必要信息', 'error')
    return
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    showToast('两次输入的密码不一致', 'error')
    return
  }
  registerLoading.value = true
  try {
    const response = await authApi.register(registerForm)
    if (response.code === 200) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data))
      showToast('注册成功')
      router.push('/dashboard')
    } else {
      showToast(response.message || '注册失败', 'error')
    }
  } catch {
    showToast('注册失败，请检查网络连接', 'error')
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.login-page{min-height:100vh;display:grid;grid-template-columns:1fr 1fr}
.login-brand{background:var(--ink);color:var(--surface);display:flex;flex-direction:column;justify-content:center;padding:60px;position:relative;overflow:hidden}
.login-brand::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:repeating-linear-gradient(45deg,transparent,transparent 30px,rgba(255,255,255,.02) 30px,rgba(255,255,255,.02) 60px)}
.login-brand h1{font-family:var(--font-display);font-size:3.8rem;line-height:1;margin-bottom:16px;position:relative}
.login-brand .tagline{font-family:var(--font-mono);font-size:.88rem;color:rgba(255,255,255,.6);max-width:380px;line-height:1.7;position:relative}
.login-brand .edition{position:absolute;bottom:40px;left:60px;font-family:var(--font-mono);font-size:.72rem;color:rgba(255,255,255,.3);letter-spacing:.12em;text-transform:uppercase}
.login-right{display:flex;flex-direction:column;justify-content:center;padding:60px;background:var(--bg)}
.login-form-container{max-width:400px;width:100%;margin:0 auto}
.login-form-container h2{font-family:var(--font-display);font-size:1.8rem;margin-bottom:8px}
.login-form-container .subtitle{font-family:var(--font-mono);font-size:.78rem;color:var(--ink-muted);margin-bottom:32px}
.login-form-container .form-group input{padding:12px 14px}
.login-form-container .btn{width:100%;justify-content:center;padding:13px;font-size:.88rem;margin-top:8px}
.demo-accounts{margin-top:36px;border:2px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-sm)}
.demo-accounts-header{padding:10px 14px;background:var(--ink);color:var(--surface);font-family:var(--font-mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;display:flex;align-items:center;gap:8px}
.demo-accounts-header::before{content:'>'}
.demo-account{padding:12px 14px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;justify-content:space-between;cursor:pointer;transition:background .1s;font-family:var(--font-mono);font-size:.78rem}
.demo-account:last-child{border-bottom:none}
.demo-account:hover{background:var(--surface-alt)}
.demo-account .role-name{font-weight:500}
.demo-account .creds{color:var(--ink-muted);font-size:.72rem}
.demo-account .fill-hint{font-size:.68rem;color:var(--accent);opacity:0;transition:opacity .15s}
.demo-account:hover .fill-hint{opacity:1}

@media(max-width:768px){
  .login-page{grid-template-columns:1fr}
  .login-brand{display:none}
  .login-right{padding:30px 20px;min-height:100vh}
}
</style>
