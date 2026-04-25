<template>
<div class="app-layout">
<div class="sidebar" :class="{open:sidebarOpen}">
<div class="sidebar-brand"><h2>集趣</h2><div class="role-tag">{{rl}}端</div></div>
<div class="sidebar-nav">
<div class="sidebar-section" v-for="s in navSections" :key="s.section">
<div class="sidebar-section-title">{{s.section}}</div>
<div class="nav-item" :class="{active:view===i.id}" v-for="i in s.items" :key="i.id" @click="go(i.id)">
<span class="nav-icon">{{i.icon}}</span><span>{{i.label}}</span>
</div>
</div>
</div>
<div class="sidebar-footer">
<div class="user-info"><div class="avatar">{{cu.avatar||'?'}}</div><div><div class="user-name">{{cu.name}}</div><div class="user-role">{{cu.college}}</div></div></div>
<button class="logout-btn" @click="logout">⏻ 退出登录</button>
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
<component :is="currentComp" :user="cu" :key="view" @viewActivity="viewAct" @navigate="go"/>
</div>
</div>
<div class="bottom-nav"><div class="bottom-nav-items">
<button class="bottom-nav-item" :class="{active:view===i.id}" v-for="i in mobileNav" :key="i.id" @click="go(i.id)">
<span class="nav-icon">{{i.icon}}</span><span>{{i.label}}</span>
</button>
</div></div>
</div>
</template>
<script setup lang="ts">
import {ref,computed,onMounted,defineAsyncComponent} from 'vue'
import {useRouter} from 'vue-router'
import {MOCK_NOTIFICATIONS,roleLabel,todayStr} from '../mock/data'
const StudentDashboard=defineAsyncComponent(()=>import('../components/StudentDashboard.vue'))
const StudentCalendar=defineAsyncComponent(()=>import('../components/StudentCalendar.vue'))
const StudentActivities=defineAsyncComponent(()=>import('../components/StudentActivities.vue'))
const StudentBonus=defineAsyncComponent(()=>import('../components/StudentBonus.vue'))
const ProfileView=defineAsyncComponent(()=>import('../components/ProfileView.vue'))
const ActivityDetail=defineAsyncComponent(()=>import('../components/ActivityDetail.vue'))
const AdminDashboard=defineAsyncComponent(()=>import('../components/AdminDashboard.vue'))
const AdminApprovals=defineAsyncComponent(()=>import('../components/AdminApprovals.vue'))
const AdminAllActivities=defineAsyncComponent(()=>import('../components/AdminAllActivities.vue'))
const AdminUserManage=defineAsyncComponent(()=>import('../components/AdminUserManage.vue'))
const AdminReports=defineAsyncComponent(()=>import('../components/AdminReports.vue'))
const AdminPublishers=defineAsyncComponent(()=>import('../components/AdminPublishers.vue'))
const PublisherDashboard=defineAsyncComponent(()=>import('../components/PublisherDashboard.vue'))
const router=useRouter()
const cu=ref<any>({})
const view=ref('dashboard')
const sidebarOpen=ref(false)
const showNotif=ref(false)
const selectedAct=ref<string|null>(null)
const dateStr=computed(()=>todayStr())
const rl=computed(()=>roleLabel(cu.value.role||''))
const unread=computed(()=>MOCK_NOTIFICATIONS.filter(n=>n.userId===cu.value.id&&!n.read).length)
const viewTitle=computed(()=>{
const m:Record<string,string>={dashboard:cu.value.role==='student'?'活动广场':cu.value.role==='admin'?'平台概览':'数据概览',
'my-activities':cu.value.role==='student'?'我的报名':'我的活动','my-bonus':'加分记录',profile:'个人中心',
'activity-detail':'活动详情','approvals':'活动审批','all-activities':'全部活动','users':'用户管理',
'create-activity':'发布活动','registrations':'报名管理','calendar':'日历视图','publishers':'发布者管理','reports':'数据报表'}
return m[view.value]||'集趣'
})
const navSections=computed(()=>{
const r=cu.value.role
if(r==='student')return[{section:'发现',items:[{id:'dashboard',icon:'📋',label:'活动广场'},{id:'calendar',icon:'📅',label:'日历视图'}]},{section:'我的',items:[{id:'my-activities',icon:'📌',label:'我的报名'},{id:'my-bonus',icon:'🎖️',label:'加分记录'},{id:'profile',icon:'👤',label:'个人中心'}]}]
if(r==='publisher')return[{section:'概览',items:[{id:'dashboard',icon:'📊',label:'数据概览'}]},{section:'活动管理',items:[{id:'create-activity',icon:'✚',label:'发布活动'},{id:'my-activities',icon:'📋',label:'我的活动'},{id:'registrations',icon:'👥',label:'报名管理'}]},{section:'账号',items:[{id:'profile',icon:'👤',label:'账号设置'}]}]
if(r==='admin')return[{section:'概览',items:[{id:'dashboard',icon:'📊',label:'平台概览'}]},{section:'审核管理',items:[{id:'approvals',icon:'✅',label:'活动审批'},{id:'all-activities',icon:'📋',label:'全部活动'}]},{section:'用户管理',items:[{id:'users',icon:'👥',label:'用户管理'},{id:'publishers',icon:'🏢',label:'发布者管理'}]},{section:'数据',items:[{id:'reports',icon:'📈',label:'数据报表'}]}]
return[]
})
const mobileNav=computed(()=>{
const r=cu.value.role
if(r==='student')return[{id:'dashboard',icon:'📋',label:'广场'},{id:'calendar',icon:'📅',label:'日历'},{id:'my-activities',icon:'📌',label:'我的'},{id:'profile',icon:'👤',label:'账号'}]
if(r==='publisher')return[{id:'dashboard',icon:'📊',label:'概览'},{id:'create-activity',icon:'✚',label:'发布'},{id:'my-activities',icon:'📋',label:'活动'},{id:'profile',icon:'👤',label:'我的'}]
return[{id:'dashboard',icon:'📊',label:'概览'},{id:'approvals',icon:'✅',label:'审批'},{id:'all-activities',icon:'📋',label:'活动'},{id:'users',icon:'👥',label:'用户'}]
})
const currentComp=computed(()=>{
if(selectedAct.value)return ActivityDetail
const r=cu.value.role
if(r==='student'){
if(view.value==='dashboard')return StudentDashboard
if(view.value==='calendar')return StudentCalendar
if(view.value==='my-activities')return StudentActivities
if(view.value==='my-bonus')return StudentBonus
if(view.value==='profile')return ProfileView
}
if(r==='admin'){
if(view.value==='dashboard')return AdminDashboard
if(view.value==='approvals')return AdminApprovals
if(view.value==='all-activities')return AdminAllActivities
if(view.value==='users')return AdminUserManage
if(view.value==='reports')return AdminReports
if(view.value==='publishers')return AdminPublishers
return AdminDashboard
}
if(r==='publisher')return PublisherDashboard
return StudentDashboard
})
function go(v:string){view.value=v;sidebarOpen.value=false;showNotif.value=false;selectedAct.value=null}
function viewAct(id:string){selectedAct.value=id;view.value='activity-detail'}
function logout(){localStorage.removeItem('token');localStorage.removeItem('user');router.push('/')}
onMounted(()=>{
const s=localStorage.getItem('user')
if(s){
try{const u=JSON.parse(s);const rawRole=(u.role||'student').toLowerCase();const roleMap:Record<string,string>={user:'student',admin:'admin',publisher:'publisher'};const mappedRole=roleMap[rawRole]||'student';cu.value={...u,role:mappedRole,name:u.nickname||u.username,college:u.college||'未知',grade:u.grade||'—',avatar:u.avatar||u.username?.charAt(0)||'?',tags:u.tags||[]}}catch{router.push('/')}
}else{router.push('/')}
})
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
