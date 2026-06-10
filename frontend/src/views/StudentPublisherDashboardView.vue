<template>
<DashboardLayout :user="cu" :view="view" :nav-sections="navSections" :mobile-nav="mobileNav" :view-title="viewTitle" @go="go" @logout="logout">
<component :is="currentComp" :user="cu" :key="view" @viewActivity="viewAct" @navigate="go"/>
</DashboardLayout>
</template>
<script setup lang="ts">
import {ref,computed,onMounted,defineAsyncComponent} from 'vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import {useCurrentUser} from '../composables/useCurrentUser'
const StudentDashboard=defineAsyncComponent(()=>import('../components/StudentDashboard.vue'))
const StudentCalendar=defineAsyncComponent(()=>import('../components/StudentCalendar.vue'))
const StudentActivities=defineAsyncComponent(()=>import('../components/StudentActivities.vue'))
const StudentBonus=defineAsyncComponent(()=>import('../components/StudentBonus.vue'))
const StudentAIRecommend=defineAsyncComponent(()=>import('../components/StudentAIRecommend.vue'))
const StudentAIChat=defineAsyncComponent(()=>import('../components/StudentAIChat.vue'))
const PublisherCreateActivity=defineAsyncComponent(()=>import('../components/PublisherCreateActivity.vue'))
const PublisherMyActivities=defineAsyncComponent(()=>import('../components/PublisherMyActivities.vue'))
const PublisherRegistrations=defineAsyncComponent(()=>import('../components/PublisherRegistrations.vue'))
const ProfileView=defineAsyncComponent(()=>import('../components/ProfileView.vue'))
const ActivityDetail=defineAsyncComponent(()=>import('../components/ActivityDetail.vue'))
const {cu,load,logout}=useCurrentUser()
const view=ref('dashboard')
const selectedAct=ref<string|null>(null)
const titles:Record<string,string>={dashboard:'活动广场',calendar:'日历视图','ai-recommend':'AI智能推荐','ai-chat':'AI聊天助手','my-registrations':'我的报名','my-bonus':'加分记录','create-activity':'发布活动','my-activities':'我的活动',registrations:'报名管理',profile:'个人中心','activity-detail':'活动详情'}
const viewTitle=computed(()=>titles[view.value]||'集趣')
const navSections=[{section:'发现',items:[{id:'dashboard',icon:'📋',label:'活动广场'},{id:'calendar',icon:'📅',label:'日历视图'},{id:'ai-recommend',icon:'🤖',label:'AI推荐'},{id:'ai-chat',icon:'💬',label:'AI聊天'}]},{section:'我的',items:[{id:'my-registrations',icon:'📌',label:'我的报名'},{id:'my-bonus',icon:'🎖️',label:'加分记录'}]},{section:'活动管理',items:[{id:'create-activity',icon:'✚',label:'发布活动'},{id:'my-activities',icon:'📋',label:'我的活动'},{id:'registrations',icon:'👥',label:'报名管理'}]},{section:'账号',items:[{id:'profile',icon:'👤',label:'个人中心'}]}]
const mobileNav=[{id:'dashboard',icon:'📋',label:'广场'},{id:'ai-recommend',icon:'🤖',label:'AI'},{id:'ai-chat',icon:'💬',label:'聊天'},{id:'create-activity',icon:'✚',label:'发布'},{id:'my-registrations',icon:'📌',label:'报名'},{id:'profile',icon:'👤',label:'我的'}]
const currentComp=computed(()=>{
if(selectedAct.value)return ActivityDetail
if(view.value==='dashboard')return StudentDashboard
if(view.value==='calendar')return StudentCalendar
if(view.value==='ai-recommend')return StudentAIRecommend
if(view.value==='ai-chat')return StudentAIChat
if(view.value==='my-registrations')return StudentActivities
if(view.value==='my-bonus')return StudentBonus
if(view.value==='create-activity')return PublisherCreateActivity
if(view.value==='my-activities')return PublisherMyActivities
if(view.value==='registrations')return PublisherRegistrations
if(view.value==='profile')return ProfileView
return StudentDashboard
})
function go(v:string){view.value=v;selectedAct.value=null;sessionStorage.removeItem('selectedActivity')}
function viewAct(id:string){sessionStorage.setItem('selectedActivity',id);selectedAct.value=id;view.value='activity-detail'}
onMounted(load)
</script>
