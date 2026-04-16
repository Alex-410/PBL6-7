<template>
  <div class="welcome-container">
    <div class="welcome-card">
      <div class="welcome-header">
        <h1>欢迎回来！</h1>
        <p>登录成功，您已进入校园活动发布平台</p>
      </div>
      <div class="welcome-content">
        <div class="user-info">
          <div class="avatar">
            <img v-if="user.avatar" :src="user.avatar" alt="用户头像">
            <div v-else class="avatar-placeholder">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>
          </div>
          <div class="user-details">
            <h2>{{ user.username }}</h2>
            <p>{{ user.email }}</p>
          </div>
        </div>
        <el-button type="primary" @click="handleLogout">退出登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const router = useRouter();
const user = ref({
  username: '',
  email: '',
  avatar: null
});

onMounted(() => {
  // 从localStorage获取用户信息
  const userInfo = localStorage.getItem('user');
  if (userInfo) {
    user.value = JSON.parse(userInfo);
  } else {
    // 如果没有用户信息，跳转到登录页面
    router.push('/');
  }
});

const handleLogout = () => {
  // 清除localStorage中的数据
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  ElMessage.success('退出登录成功');
  // 跳转到登录页面
  router.push('/');
};
</script>

<style scoped lang="scss">
.welcome-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #f5f7fa;
}

.welcome-card {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  padding: 60px;
  text-align: center;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
  }
}

.welcome-header {
  margin-bottom: 40px;

  h1 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 28px;
    font-weight: 600;
    color: #212529;
    margin-bottom: 10px;
  }

  p {
    font-size: 16px;
    color: #6c757d;
    margin: 0;
  }
}

.welcome-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 30px;
  background: #f8f9fa;
  border-radius: 8px;
  width: 100%;
  justify-content: center;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  background: #e9ecef;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 600;
    color: #6c757d;
    background: linear-gradient(135deg, #eef2f7 0%, #dfe7f0 100%);
  }
}

.user-details {
  text-align: left;

  h2 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 20px;
    font-weight: 500;
    color: #212529;
    margin: 0 0 5px 0;
  }

  p {
    font-size: 14px;
    color: #6c757d;
    margin: 0;
  }
}

.el-button {
  width: 200px;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 4px;
  background: #2563eb;
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    background: #1d4ed8 !important;
    color: white !important;
  }
}
</style>