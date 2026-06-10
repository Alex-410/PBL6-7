<template>
<DashboardLayout :user="cu" :view="view" :nav-sections="navSections" :mobile-nav="mobileNav" :view-title="viewTitle" @go="go" @logout="logout">
<component :is="currentComp" :user="cu" :key="view" @viewActivity="viewAct" @navigate="go"/>
</DashboardLayout>
</template>
<script setup lang="ts">
import {ref,computed,onMounted,defineAsyncComponent} from 'vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import {useCurrentUser} from '../composables/useCurrentUser'
const PublisherDashboard=defineAsyncComponent(()=>import('../components/PublisherDashboard.vue'))
const PublisherCreateActivity=defineAsyncComponent(()=>import('../components/PublisherCreateActivity.vue'))
const PublisherMyActivities=defineAsyncComponent(()=>import('../components/PublisherMyActivities.vue'))
const PublisherRegistrations=defineAsyncComponent(()=>import('../components/PublisherRegistrations.vue'))
const ProfileView=defineAsyncComponent(()=>import('../components/ProfileView.vue'))
const ActivityDetail=defineAsyncComponent(()=>import('../components/ActivityDetail.vue'))
const {cu,load,logout}=useCurrentUser()
const view=ref('dashboard')
const selectedAct=ref<string|null>(null)
const titles:Record<string,string>={dashboard:'数据概览','create-activity':'发布活动','my-activities':'我的活动',registrations:'报名管理',profile:'账号设置','activity-detail':'活动详情'}
const viewTitle=computed(()=>titles[view.value]||'集趣')
const navSections=[{section:'概览',items:[{id:'dashboard',icon:'📊',label:'数据概览'}]},{section:'活动管理',items:[{id:'create-activity',icon:'✚',label:'发布活动'},{id:'my-activities',icon:'📋',label:'我的活动'},{id:'registrations',icon:'👥',label:'报名管理'}]},{section:'账号',items:[{id:'profile',icon:'👤',label:'账号设置'}]}]
const mobileNav=[{id:'dashboard',icon:'📊',label:'概览'},{id:'create-activity',icon:'✚',label:'发布'},{id:'my-activities',icon:'📋',label:'活动'},{id:'profile',icon:'👤',label:'我的'}]
const currentComp=computed(()=>{
if(selectedAct.value)return ActivityDetail
if(view.value==='dashboard')return PublisherDashboard
if(view.value==='create-activity')return PublisherCreateActivity
if(view.value==='my-activities')return PublisherMyActivities
if(view.value==='registrations')return PublisherRegistrations
if(view.value==='profile')return ProfileView
return PublisherDashboard
})
function go(v:string){view.value=v;selectedAct.value=null;sessionStorage.removeItem('selectedActivity')}
function viewAct(id:string){sessionStorage.setItem('selectedActivity',id);selectedAct.value=id;view.value='activity-detail'}
onMounted(load)
</script>
