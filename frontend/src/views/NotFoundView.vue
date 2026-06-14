<template>
  <div class="not-found">
    <div class="nf-content">
      <div class="nf-code">404</div>
      <h1>页面未找到</h1>
      <p>你访问的页面不存在或已被移除</p>
      <router-link to="/" class="nf-btn">返回首页</router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg, #F5F1EB);
  font-family: var(--font-body, 'Noto Serif SC', Georgia, serif);
}

.nf-content {
  text-align: center;
  padding: 40px;
}

.nf-code {
  font-family: var(--font-display, 'Noto Serif SC', serif);
  font-size: 8rem;
  font-weight: 700;
  color: var(--accent, #6B4C3B);
  opacity: 0.2;
  line-height: 1;
  margin-bottom: -20px;
}

h1 {
  font-family: var(--font-display, 'Noto Serif SC', serif);
  font-size: 1.8rem;
  color: var(--ink, #2D2A26);
  margin-bottom: 12px;
}

p {
  color: var(--ink-muted, #888);
  font-size: 0.95rem;
  margin-bottom: 32px;
}

.nf-btn {
  display: inline-block;
  padding: 12px 32px;
  background: var(--accent, #6B4C3B);
  color: white;
  text-decoration: none;
  border-radius: var(--radius, 6px);
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.nf-btn:hover {
  opacity: 0.9;
}
</style>
