<template>
  <div class="homepage">
    <!-- 导航栏 -->
    <header class="nav-header">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="brand-icon">校</div>
          <div>
            <div class="brand-name">电子科技大学成都学院</div>
            <div class="brand-sub">UESTC Chengdu College</div>
          </div>
        </div>
        <nav class="nav-links" :class="{ open: menuOpen }">
          <a class="nav-link active" @click.prevent="scrollTo('hero')">首页</a>
          <a class="nav-link" @click.prevent="scrollTo('news')">新闻公告</a>
          <a class="nav-link" @click.prevent="scrollTo('activities')">校园活动</a>
          <a class="nav-link" @click.prevent="scrollTo('campus')">校园风采</a>
          <router-link class="nav-link accent" to="/login">活动发布</router-link>
          <a class="nav-link" href="javascript:void(0)" title="敬请期待">工具箱</a>
        </nav>
        <button class="menu-toggle" @click="menuOpen = !menuOpen">☰</button>
      </div>
    </header>

    <!-- Hero 轮播 -->
    <section class="hero" id="hero">
      <div class="hero-slides">
        <div class="hero-slide" v-for="(s, i) in heroSlides" :key="i"
          :class="{ active: currentSlide === i }">
          <div class="hero-img" :style="{ backgroundImage: `url(${s.img})` }"></div>
          <div class="hero-overlay"></div>
          <div class="hero-content">
            <div class="hero-badge">{{ s.badge }}</div>
            <h1>{{ s.title }}</h1>
            <p>{{ s.desc }}</p>
          </div>
        </div>
      </div>
      <div class="hero-dots">
        <button v-for="(_, i) in heroSlides" :key="i"
          :class="{ active: currentSlide === i }" @click="currentSlide = i"></button>
      </div>
    </section>

    <!-- 快捷入口 -->
    <section class="quick-links">
      <div class="container">
        <div class="links-grid">
          <div class="link-card" v-for="l in quickLinks" :key="l.label">
            <div class="link-icon">{{ l.icon }}</div>
            <div class="link-label">{{ l.label }}</div>
            <div class="link-desc">{{ l.desc }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 新闻公告 -->
    <section class="section" id="news">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">新闻公告</h2>
          <div class="section-tabs">
            <button :class="{ active: newsTab === 'all' }" @click="newsTab = 'all'">全部</button>
            <button :class="{ active: newsTab === 'news' }" @click="newsTab = 'news'">校园新闻</button>
            <button :class="{ active: newsTab === 'notice' }" @click="newsTab = 'notice'">通知公告</button>
          </div>
        </div>
        <div class="news-grid">
          <div class="news-featured" v-if="filteredNews.length">
            <div class="news-card featured">
              <div class="news-img" :style="{ backgroundImage: `url(${filteredNews[0].img})` }">
                <div class="news-tag">{{ filteredNews[0].tag }}</div>
              </div>
              <div class="news-body">
                <h3>{{ filteredNews[0].title }}</h3>
                <p>{{ filteredNews[0].summary }}</p>
                <div class="news-meta">
                  <span>{{ filteredNews[0].date }}</span>
                  <span>{{ filteredNews[0].source }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="news-list">
            <div class="news-item" v-for="n in filteredNews.slice(1)" :key="n.title">
              <div class="news-item-date">
                <span class="day">{{ n.date.split('-')[2] }}</span>
                <span class="month">{{ n.date.split('-').slice(0, 2).join('-') }}</span>
              </div>
              <div class="news-item-body">
                <div class="news-item-tag badge" :class="n.tagClass">{{ n.tag }}</div>
                <h4>{{ n.title }}</h4>
                <p>{{ n.summary }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 校园活动 -->
    <section class="section alt" id="activities">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">校园活动</h2>
          <router-link to="/login" class="btn btn-sm">查看全部 →</router-link>
        </div>
        <div class="activity-grid">
          <div class="activity-card" v-for="a in activities" :key="a.title">
            <div class="activity-img" :style="{ backgroundImage: `url(${a.img})` }">
              <div class="activity-badge badge" :class="a.badgeClass">{{ a.badge }}</div>
            </div>
            <div class="activity-body">
              <h3>{{ a.title }}</h3>
              <div class="activity-meta">
                <span>📅 {{ a.date }}</span>
                <span>📍 {{ a.location }}</span>
              </div>
              <p>{{ a.desc }}</p>
            </div>
            <div class="activity-footer">
              <span class="spots">剩余 <strong>{{ a.spots }}</strong> 个名额</span>
              <router-link to="/login" class="btn btn-sm btn-accent">立即报名</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 校园风采 -->
    <section class="section" id="campus">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">校园风采</h2>
        </div>
        <div class="gallery-grid">
          <div class="gallery-item" v-for="(g, i) in gallery" :key="i" :class="g.size">
            <div class="gallery-img" :style="{ backgroundImage: `url(${g.img})` }">
              <div class="gallery-caption">
                <h4>{{ g.title }}</h4>
                <p>{{ g.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 数据展示 -->
    <section class="section stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item" v-for="s in stats" :key="s.label">
            <div class="stat-number">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <div class="footer-logo">
              <div class="brand-icon">校</div>
              <span>电子科技大学成都学院</span>
            </div>
            <p>学校地址：四川省成都市高新西区百叶路1号</p>
            <p>邮编：611731</p>
            <p>电话：028-87825015</p>
          </div>
          <div class="footer-links">
            <h4>快速链接</h4>
            <a href="#">学校概况</a>
            <a href="#">院系设置</a>
            <a href="#">招生就业</a>
            <a href="#">科学研究</a>
          </div>
          <div class="footer-links">
            <h4>学生服务</h4>
            <a href="#">教务系统</a>
            <a href="#">图书馆</a>
            <a href="#">学生事务</a>
            <router-link to="/login">活动平台</router-link>
          </div>
          <div class="footer-links">
            <h4>关注我们</h4>
            <a href="#">官方微信</a>
            <a href="#">官方微博</a>
            <a href="#">抖音号</a>
            <a href="#">B站</a>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 电子科技大学成都学院 版权所有 · 蜀ICP备XXXXXXXX号</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const menuOpen = ref(false)
const currentSlide = ref(0)
const newsTab = ref('all')

const heroSlides = [
  {
    img: 'https://picsum.photos/seed/campus1/1600/700',
    badge: '欢迎来到',
    title: '电子科技大学成都学院',
    desc: '厚德笃学 · 求实创新 — 培养具有国际视野的高素质应用型人才'
  },
  {
    img: 'https://picsum.photos/seed/campus2/1600/700',
    badge: '2026年招生',
    title: '欢迎报考我校',
    desc: '涵盖工、管、文、艺等多学科门类，开启你的大学新篇章'
  },
  {
    img: 'https://picsum.photos/seed/campus3/1600/700',
    badge: '校园活动',
    title: '丰富多彩的校园生活',
    desc: '加入集趣平台，发现精彩活动，记录你的每一次校园体验'
  }
]

const quickLinks = [
  { icon: '📚', label: '教务系统', desc: '选课·成绩·课表' },
  { icon: '📖', label: '图书馆', desc: '馆藏·借阅·电子资源' },
  { icon: '🎓', label: '招生就业', desc: '招生·实习·就业' },
  { icon: '🏠', label: '学生事务', desc: '宿舍·奖助·社团' },
  { icon: '🔬', label: '科研创新', desc: '项目·竞赛·专利' },
  { icon: '🌐', label: '国际交流', desc: '留学·交换·访学' },
]

const newsItems = [
  { type: 'news', tag: '校园新闻', tagClass: 'badge-blue', title: '我校学子在第十五届全国大学生数学竞赛中斩获佳绩', summary: '近日，第十五届全国大学生数学竞赛决赛成绩揭晓，我校学生获得一等奖2项、二等奖5项、三等奖8项的优异成绩。', date: '2026-06-03', source: '教务处', img: 'https://picsum.photos/seed/news1/800/500' },
  { type: 'notice', tag: '通知公告', tagClass: 'badge-amber', title: '关于2026年暑假放假安排的通知', summary: '根据学校校历安排，2026年暑假放假时间为7月15日至8月31日，请各部门做好相关工作安排。', date: '2026-06-02', source: '校办', img: 'https://picsum.photos/seed/news2/800/500' },
  { type: 'news', tag: '校园新闻', tagClass: 'badge-blue', title: '计算机学院与华为公司签署产教融合合作协议', summary: '6月1日，我校计算机学院与华为技术有限公司正式签署产教融合合作协议，共同培养ICT领域人才。', date: '2026-06-01', source: '计算机学院', img: 'https://picsum.photos/seed/news3/800/500' },
  { type: 'notice', tag: '通知公告', tagClass: 'badge-amber', title: '关于开展2026年大学生创新创业训练计划项目申报的通知', summary: '为培养大学生创新创业能力，现开展2026年大学生创新创业训练计划项目申报工作，请各学院积极组织。', date: '2026-05-30', source: '创新创业中心', img: 'https://picsum.photos/seed/news4/800/500' },
  { type: 'news', tag: '校园新闻', tagClass: 'badge-blue', title: '我校举办第十二届校园科技文化节', summary: '5月28日，我校第十二届校园科技文化节开幕式在学术报告厅举行，本届科技文化节以"创新引领未来"为主题。', date: '2026-05-28', source: '团委', img: 'https://picsum.photos/seed/news5/800/500' },
]

const activities = [
  { title: '2026年校园歌手大赛', date: '2026-06-15', location: '大学生活动中心', desc: '展现你的歌唱才华，用音乐点亮青春舞台', spots: 50, img: 'https://picsum.photos/seed/act1/600/400', badge: '热门', badgeClass: 'badge-red' },
  { title: 'ACM程序设计竞赛校赛', date: '2026-06-20', location: '计算机实验室', desc: '以赛促学，提升编程能力，选拔优秀选手参加省赛', spots: 30, img: 'https://picsum.photos/seed/act2/600/400', badge: '竞赛', badgeClass: 'badge-blue' },
  { title: '大学生志愿服务进社区', date: '2026-06-22', location: '周边社区', desc: '走进社区，服务群众，在实践中锻炼自我', spots: 40, img: 'https://picsum.photos/seed/act3/600/400', badge: '志愿', badgeClass: 'badge-green' },
  { title: '创新创业大赛宣讲会', date: '2026-06-18', location: '学术报告厅', desc: '了解大赛规则，激发创新思维，开启创业之旅', spots: 100, img: 'https://picsum.photos/seed/act4/600/400', badge: '讲座', badgeClass: 'badge-purple' },
]

const gallery = [
  { img: 'https://picsum.photos/seed/g1/800/600', title: '校园全景', desc: '美丽的校园风光', size: 'wide' },
  { img: 'https://picsum.photos/seed/g2/600/600', title: '图书馆', desc: '知识的殿堂', size: '' },
  { img: 'https://picsum.photos/seed/g3/600/600', title: '运动场', desc: '挥洒汗水的地方', size: '' },
  { img: 'https://picsum.photos/seed/g4/800/600', title: '实验室', desc: '探索科学的奥秘', size: 'wide' },
  { img: 'https://picsum.photos/seed/g5/600/600', title: '学生活动', desc: '丰富多彩的课余生活', size: '' },
  { img: 'https://picsum.photos/seed/g6/600/600', title: '校园夜景', desc: '灯火阑珊的夜晚', size: '' },
]

const stats = [
  { value: '20,000+', label: '在校学生' },
  { value: '1,200+', label: '教职工' },
  { value: '50+', label: '本科专业' },
  { value: '100+', label: '学生社团' },
]

const filteredNews = computed(() => {
  if (newsTab.value === 'all') return newsItems
  return newsItems.filter(n => n.type === newsTab.value)
})

let timer: ReturnType<typeof setInterval>
onMounted(() => {
  timer = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % heroSlides.length
  }, 5000)
})
onUnmounted(() => clearInterval(timer))

function scrollTo(id: string) {
  menuOpen.value = false
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.homepage {
  --nav-h: 64px;
  background: var(--bg);
  min-height: 100vh;
}

/* 导航栏 */
.nav-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--nav-h);
  background: var(--ink);
  z-index: 1000;
  border-bottom: 2px solid rgba(255,255,255,.08);
}
.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 28px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--surface);
}
.brand-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), #E8590C);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
}
.brand-name {
  font-family: var(--font-display);
  font-size: 1.15rem;
  line-height: 1.2;
}
.brand-sub {
  font-family: var(--font-mono);
  font-size: .62rem;
  color: rgba(255,255,255,.4);
  letter-spacing: .08em;
  text-transform: uppercase;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
}
.nav-link {
  padding: 8px 16px;
  color: rgba(255,255,255,.65);
  font-family: var(--font-mono);
  font-size: .8rem;
  border-radius: var(--radius);
  transition: all .15s;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
}
.nav-link:hover { color: var(--surface); background: rgba(255,255,255,.08); }
.nav-link.active { color: var(--surface); background: rgba(255,255,255,.12); }
.nav-link.accent { color: var(--accent); border: 1.5px solid var(--accent); }
.nav-link.accent:hover { background: var(--accent); color: #fff; }
.menu-toggle {
  display: none;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  color: var(--surface);
  background: none;
  border: none;
  cursor: pointer;
}

/* Hero */
.hero {
  margin-top: var(--nav-h);
  position: relative;
  height: 520px;
  overflow: hidden;
}
.hero-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity .8s;
}
.hero-slide.active { opacity: 1; }
.hero-img {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
}
.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(26,22,19,.7), rgba(26,22,19,.3));
}
.hero-content {
  position: absolute;
  bottom: 80px;
  left: 0;
  right: 0;
  text-align: center;
  color: var(--surface);
  padding: 0 28px;
}
.hero-badge {
  font-family: var(--font-mono);
  font-size: .75rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: rgba(255,255,255,.6);
  margin-bottom: 12px;
}
.hero-content h1 {
  font-family: var(--font-display);
  font-size: 2.8rem;
  margin-bottom: 12px;
  text-shadow: 0 2px 12px rgba(0,0,0,.3);
}
.hero-content p {
  font-family: var(--font-mono);
  font-size: .92rem;
  color: rgba(255,255,255,.8);
  max-width: 600px;
  margin: 0 auto;
}
.hero-dots {
  position: absolute;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}
.hero-dots button {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,.5);
  background: transparent;
  cursor: pointer;
  transition: all .2s;
}
.hero-dots button.active {
  background: var(--surface);
  border-color: var(--surface);
  transform: scale(1.2);
}

/* 快捷入口 */
.quick-links {
  padding: 48px 0;
  background: var(--surface);
  border-bottom: 2px solid var(--border);
}
.links-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
}
.link-card {
  text-align: center;
  padding: 24px 16px;
  border: 2px solid var(--border-light);
  border-radius: var(--radius);
  transition: all .15s;
  cursor: pointer;
}
.link-card:hover {
  transform: translateY(-3px);
  border-color: var(--accent);
  box-shadow: var(--shadow-sm);
}
.link-icon { font-size: 2rem; margin-bottom: 10px; }
.link-label {
  font-family: var(--font-display);
  font-size: 1rem;
  margin-bottom: 4px;
}
.link-desc {
  font-family: var(--font-mono);
  font-size: .68rem;
  color: var(--ink-muted);
}

/* 通用 Section */
.container { max-width: 1200px; margin: 0 auto; padding: 0 28px; }
.section { padding: 64px 0; }
.section.alt { background: var(--surface); border-top: 2px solid var(--border); border-bottom: 2px solid var(--border); }
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 36px;
  flex-wrap: wrap;
  gap: 16px;
}
.section-title {
  font-family: var(--font-display);
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  gap: 12px;
}
.section-title::after {
  content: '';
  width: 60px;
  height: 3px;
  background: var(--accent);
  border-radius: 2px;
}
.section-tabs {
  display: flex;
  gap: 4px;
}
.section-tabs button {
  padding: 7px 16px;
  font-family: var(--font-mono);
  font-size: .75rem;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius);
  background: var(--surface);
  cursor: pointer;
  transition: all .12s;
}
.section-tabs button:hover { border-color: var(--border); }
.section-tabs button.active { background: var(--ink); color: var(--surface); border-color: var(--ink); }

/* 新闻 */
.news-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
.news-card.featured {
  border: 2px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--surface);
  box-shadow: var(--shadow);
  transition: all .15s;
}
.news-card.featured:hover { transform: translate(-2px,-2px); box-shadow: 5px 5px 0 var(--border); }
.news-img {
  height: 240px;
  background-size: cover;
  background-position: center;
  position: relative;
}
.news-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  font-family: var(--font-mono);
  font-size: .68rem;
  padding: 4px 10px;
  background: var(--accent);
  color: #fff;
  border-radius: 2px;
}
.news-body { padding: 20px; }
.news-body h3 {
  font-family: var(--font-display);
  font-size: 1.2rem;
  margin-bottom: 10px;
  line-height: 1.4;
}
.news-body p {
  font-size: .85rem;
  color: var(--ink-muted);
  line-height: 1.6;
  margin-bottom: 12px;
}
.news-meta {
  display: flex;
  gap: 16px;
  font-family: var(--font-mono);
  font-size: .7rem;
  color: var(--ink-light);
}

.news-list { display: flex; flex-direction: column; gap: 0; }
.news-item {
  display: flex;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-light);
  transition: background .12s;
  cursor: pointer;
}
.news-item:hover { background: var(--bg); }
.news-item:last-child { border-bottom: none; }
.news-item-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 50px;
  padding-top: 4px;
}
.news-item-date .day {
  font-family: var(--font-display);
  font-size: 1.6rem;
  line-height: 1;
  color: var(--accent);
}
.news-item-date .month {
  font-family: var(--font-mono);
  font-size: .65rem;
  color: var(--ink-muted);
}
.news-item-body h4 {
  font-family: var(--font-display);
  font-size: .95rem;
  margin: 6px 0;
  line-height: 1.4;
}
.news-item-body p {
  font-size: .78rem;
  color: var(--ink-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 活动 */
.activity-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.activity-card {
  border: 2px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all .15s;
}
.activity-card:hover { transform: translate(-2px,-2px); box-shadow: 5px 5px 0 var(--border); }
.activity-img {
  height: 180px;
  background-size: cover;
  background-position: center;
  position: relative;
}
.activity-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: .65rem;
}
.activity-body { padding: 16px; }
.activity-body h3 {
  font-family: var(--font-display);
  font-size: 1.1rem;
  margin-bottom: 8px;
}
.activity-meta {
  display: flex;
  gap: 16px;
  font-family: var(--font-mono);
  font-size: .72rem;
  color: var(--ink-muted);
  margin-bottom: 8px;
}
.activity-body p {
  font-size: .82rem;
  color: var(--ink-muted);
  line-height: 1.5;
}
.activity-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.activity-footer .spots {
  font-family: var(--font-mono);
  font-size: .75rem;
  color: var(--ink-muted);
}
.activity-footer .spots strong { color: var(--accent); }

/* 校园风采 */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 220px;
  gap: 16px;
}
.gallery-item.wide { grid-column: span 2; }
.gallery-img {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  border: 2px solid var(--border);
  border-radius: var(--radius);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all .15s;
}
.gallery-img:hover { transform: scale(1.02); }
.gallery-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: linear-gradient(transparent, rgba(26,22,19,.8));
  color: var(--surface);
  transform: translateY(100%);
  transition: transform .25s;
}
.gallery-img:hover .gallery-caption { transform: translateY(0); }
.gallery-caption h4 { font-family: var(--font-display); font-size: 1rem; margin-bottom: 4px; }
.gallery-caption p { font-family: var(--font-mono); font-size: .72rem; color: rgba(255,255,255,.7); }

/* 数据展示 */
.stats-section {
  background: var(--ink);
  color: var(--surface);
  padding: 56px 0;
  border: none;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 28px;
  text-align: center;
}
.stat-number {
  font-family: var(--font-display);
  font-size: 2.6rem;
  line-height: 1;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #fff, #E8A87C);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.stat-label {
  font-family: var(--font-mono);
  font-size: .78rem;
  color: rgba(255,255,255,.5);
  letter-spacing: .08em;
}

/* 页脚 */
.footer {
  background: #1A1613;
  color: rgba(255,255,255,.6);
  padding: 56px 0 0;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--surface);
  font-family: var(--font-display);
  font-size: 1.1rem;
  margin-bottom: 16px;
}
.footer-logo .brand-icon { width: 36px; height: 36px; font-size: .9rem; }
.footer-brand p {
  font-family: var(--font-mono);
  font-size: .78rem;
  margin-bottom: 6px;
  line-height: 1.6;
}
.footer-links h4 {
  color: var(--surface);
  font-family: var(--font-display);
  font-size: 1rem;
  margin-bottom: 16px;
}
.footer-links a {
  display: block;
  color: rgba(255,255,255,.5);
  font-family: var(--font-mono);
  font-size: .78rem;
  padding: 5px 0;
  transition: color .12s;
  text-decoration: none;
}
.footer-links a:hover { color: var(--surface); }
.footer-bottom {
  padding: 20px 0;
  text-align: center;
}
.footer-bottom p {
  font-family: var(--font-mono);
  font-size: .7rem;
  color: rgba(255,255,255,.3);
}

/* 响应式 */
@media (max-width: 1024px) {
  .links-grid { grid-template-columns: repeat(3, 1fr); }
  .activity-grid { grid-template-columns: 1fr; }
  .gallery-grid { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 180px; }
}
@media (max-width: 768px) {
  .nav-links {
    display: none;
    position: fixed;
    top: var(--nav-h);
    left: 0;
    right: 0;
    background: var(--ink);
    flex-direction: column;
    padding: 16px;
    border-bottom: 2px solid rgba(255,255,255,.08);
    gap: 4px;
  }
  .nav-links.open { display: flex; }
  .menu-toggle { display: flex; }
  .hero { height: 380px; }
  .hero-content h1 { font-size: 1.8rem; }
  .links-grid { grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .link-card { padding: 16px 8px; }
  .link-icon { font-size: 1.5rem; }
  .news-grid { grid-template-columns: 1fr; }
  .gallery-grid { grid-template-columns: 1fr 1fr; grid-auto-rows: 160px; }
  .gallery-item.wide { grid-column: span 1; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 28px; }
}
@media (max-width: 480px) {
  .links-grid { grid-template-columns: repeat(2, 1fr); }
  .hero { height: 300px; }
  .hero-content h1 { font-size: 1.4rem; }
  .section-title { font-size: 1.4rem; }
  .gallery-grid { grid-template-columns: 1fr; }
}
</style>
