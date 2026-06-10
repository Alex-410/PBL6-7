<template>
<div class="app-layout">
<div class="sidebar" :class="{open:sidebarOpen}">
<div class="sidebar-brand"><h2>集趣</h2><div class="role-tag">{{roleLabelText}}端</div></div>
<div class="sidebar-nav">
<div class="sidebar-section" v-for="s in navSections" :key="s.section">
<div class="sidebar-section-title">{{s.section}}</div>
<div class="nav-item" :class="{active:view===i.id}" v-for="i in s.items" :key="i.id" @click="onGo(i.id)">
<span class="nav-icon">{{i.icon}}</span><span>{{i.label}}</span>
</div>
</div>
</div>
<div class="sidebar-footer">
<div class="user-info"><div class="avatar">{{user.avatar||'?'}}</div><div><div class="user-name">{{user.name}}</div><div class="user-role">{{user.college}}</div></div></div>
<button class="logout-btn" @click="$emit('logout')">⏻ 退出登录</button>
</div>
</div>
<div class="sidebar-overlay" :class="{show:sidebarOpen}" @click="sidebarOpen=false"></div>
<div class="main-area">
<div class="topbar">
<div class="topbar-left"><button class="hamburger" @click="sidebarOpen=!sidebarOpen">☰</button><span class="topbar-title">{{viewTitle}}</span></div>
<div class="topbar-right"><span class="topbar-date mono text-sm text-muted">{{dateStr}}</span>
<button class="notif-btn" @click="showNotif=!showNotif">🔔<span class="notif-badge" v-if="unread>0">{{unread}}</span></button>
</div>
</div>
<div class="content">
<slot></slot>
</div>
</div>
<div class="bottom-nav"><div class="bottom-nav-items">
<button class="bottom-nav-item" :class="{active:view===i.id}" v-for="i in mobileNav" :key="i.id" @click="onGo(i.id)">
<span class="nav-icon">{{i.icon}}</span><span>{{i.label}}</span>
</button>
</div></div>
</div>
</template>
<script setup lang="ts">
import {ref,computed} from 'vue'
import {MOCK_NOTIFICATIONS,roleLabel,todayStr} from '../mock/data'
const props=defineProps<{
  user:any
  view:string
  navSections:any[]
  mobileNav:any[]
  viewTitle:string
}>()
const emit=defineEmits(['go','logout'])
const sidebarOpen=ref(false)
const showNotif=ref(false)
const dateStr=computed(()=>todayStr())
const roleLabelText=computed(()=>roleLabel(props.user.role||''))
const unread=computed(()=>MOCK_NOTIFICATIONS.filter(n=>n.userId===props.user.id&&!n.read).length)
function onGo(v:string){emit('go',v);sidebarOpen.value=false;showNotif.value=false}
</script>
<style scoped>
.app-layout{display:flex;min-height:100vh}
.sidebar{width:var(--sidebar-w);background:var(--ink);color:var(--surface);position:fixed;top:0;left:0;bottom:0;display:flex;flex-direction:column;z-index:100;transition:transform .25s}
.sidebar-brand{padding:20px 20px 16px;border-bottom:1px solid rgba(255,255,255,.1)}
.sidebar-brand h2{font-family:var(--font-display);font-size:1.4rem;color:var(--surface)}
.sidebar-brand .role-tag{font-family:var(--font-mono);font-size:.68rem;color:rgba(255,255,255,.4);margin-top:2px;text-transform:uppercase;letter-spacing:.1em}
.sidebar-nav{flex:1;padding:16px 12px;overflow-y:auto}
.sidebar-section{margin-bottom:20px}
.sidebar-section-title{font-family:var(--font-mono);font-size:.65rem;color:rgba(255,255,255,.3);text-transform:uppercase;letter-spacing:.12em;padding:0 8px;margin-bottom:6px}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:var(--radius);font-family:var(--font-mono);font-size:.8rem;color:rgba(255,255,255,.6);cursor:pointer;transition:all .12s;margin-bottom:2px}
.nav-item:hover{color:var(--surface);background:rgba(255,255,255,.08)}
.nav-item.active{color:var(--surface);background:rgba(255,255,255,.12);font-weight:500}
.nav-item .nav-icon{width:20px;text-align:center;font-size:1rem}
.sidebar-footer{padding:16px 12px;border-top:1px solid rgba(255,255,255,.1)}
.sidebar-footer .user-info{display:flex;align-items:center;gap:10px;padding:8px;margin-bottom:8px}
.sidebar-footer .user-info .avatar{border-color:rgba(255,255,255,.2);background:rgba(255,255,255,.1);color:var(--surface);width:32px;height:32px;font-size:.82rem}
.sidebar-footer .user-name{font-family:var(--font-mono);font-size:.78rem;color:var(--surface)}
.sidebar-footer .user-role{font-size:.68rem;color:rgba(255,255,255,.4)}
.sidebar-footer .logout-btn{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--radius);font-family:var(--font-mono);font-size:.78rem;color:rgba(255,255,255,.5);cursor:pointer;width:100%;transition:all .12s;border:none;background:none}
.sidebar-footer .logout-btn:hover{color:var(--accent);background:rgba(185,28,28,.15)}
.main-area{flex:1;margin-left:var(--sidebar-w);min-height:100vh;display:flex;flex-direction:column}
.topbar{height:var(--header-h);border-bottom:2px solid var(--border);background:var(--surface);display:flex;align-items:center;justify-content:space-between;padding:0 28px;position:sticky;top:0;z-index:50}
.topbar-left{display:flex;align-items:center;gap:16px}
.topbar-title{font-family:var(--font-display);font-size:1.2rem}
.topbar-right{display:flex;align-items:center;gap:12px}
.notif-btn{position:relative;width:36px;height:36px;display:flex;align-items:center;justify-content:center;border-radius:var(--radius);border:1.5px solid var(--border-light);font-size:1.1rem;transition:all .12s;background:none;cursor:pointer}
.notif-btn:hover{border-color:var(--border);background:var(--surface-alt)}
.notif-badge{position:absolute;top:-4px;right:-4px;width:18px;height:18px;border-radius:50%;background:var(--accent);color:#fff;font-family:var(--font-mono);font-size:.6rem;display:flex;align-items:center;justify-content:center;border:2px solid var(--surface)}
.hamburger{display:none;width:36px;height:36px;align-items:center;justify-content:center;border:1.5px solid var(--border-light);border-radius:var(--radius);font-size:1.2rem;cursor:pointer;background:none}
.content{flex:1;padding:28px}
.sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(26,22,19,.5);z-index:99}
.bottom-nav{display:none;position:fixed;bottom:0;left:0;right:0;background:var(--ink);border-top:2px solid rgba(255,255,255,.1);z-index:100;padding:6px 0}
.bottom-nav-items{display:flex;justify-content:space-around}
.bottom-nav-item{display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 12px;color:rgba(255,255,255,.45);font-family:var(--font-mono);font-size:.6rem;cursor:pointer;border:none;background:none}
.bottom-nav-item.active{color:var(--surface)}
.bottom-nav-item .nav-icon{font-size:1.2rem}
@media(max-width:768px){
.sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.sidebar-overlay.show{display:block}
.main-area{margin-left:0}.hamburger{display:flex}.content{padding:16px;padding-bottom:80px}.bottom-nav{display:block}.topbar{padding:0 16px}
}
</style>
