<template>
<DashboardLayout :user="cu" :view="view" :nav-sections="navSections" :mobile-nav="mobileNav" :view-title="viewTitle" @go="go" @logout="logout">
<component :is="currentComp" :user="cu" :key="view" @viewActivity="viewAct" @navigate="go"/>
</DashboardLayout>
</template>
<script setup lang="ts">
import {ref,computed,onMounted,defineAsyncComponent} from 'vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import {useCurrentUser} from '../composables/useCurrentUser'
const AdminDashboard=defineAsyncComponent(()=>import('../components/AdminDashboard.vue'))
const AdminApprovals=defineAsyncComponent(()=>import('../components/AdminApprovals.vue'))
const AdminAllActivities=defineAsyncComponent(()=>import('../components/AdminAllActivities.vue'))
const AdminUserManage=defineAsyncComponent(()=>import('../components/AdminUserManage.vue'))
const AdminReports=defineAsyncComponent(()=>import('../components/AdminReports.vue'))
const AdminPublishers=defineAsyncComponent(()=>import('../components/AdminPublishers.vue'))
const ActivityDetail=defineAsyncComponent(()=>import('../components/ActivityDetail.vue'))
const {cu,load,logout}=useCurrentUser()
const view=ref('dashboard')
const selectedAct=ref<string|null>(null)
const titles:Record<string,string>={dashboard:'平台概览',approvals:'活动审批','all-activities':'全部活动',users:'用户管理',publishers:'发布者管理',reports:'数据报表','activity-detail':'活动详情'}
const viewTitle=computed(()=>titles[view.value]||'集趣')
const navSections=[{section:'概览',items:[{id:'dashboard',icon:'📊',label:'平台概览'}]},{section:'审核管理',items:[{id:'approvals',icon:'✅',label:'活动审批'},{id:'all-activities',icon:'📋',label:'全部活动'}]},{section:'用户管理',items:[{id:'users',icon:'👥',label:'用户管理'},{id:'publishers',icon:'🏢',label:'发布者管理'}]},{section:'数据',items:[{id:'reports',icon:'📈',label:'数据报表'}]}]
const mobileNav=[{id:'dashboard',icon:'📊',label:'概览'},{id:'approvals',icon:'✅',label:'审批'},{id:'all-activities',icon:'📋',label:'活动'},{id:'users',icon:'👥',label:'用户'}]
const currentComp=computed(()=>{
if(selectedAct.value)return ActivityDetail
if(view.value==='dashboard')return AdminDashboard
if(view.value==='approvals')return AdminApprovals
if(view.value==='all-activities')return AdminAllActivities
if(view.value==='users')return AdminUserManage
if(view.value==='reports')return AdminReports
if(view.value==='publishers')return AdminPublishers
return AdminDashboard
})
function go(v:string){view.value=v;selectedAct.value=null;sessionStorage.removeItem('selectedActivity')}
function viewAct(id:string){sessionStorage.setItem('selectedActivity',id);selectedAct.value=id;view.value='activity-detail'}
onMounted(load)
</script>
