<template>
<div>
<div class="section-title mb-24">报名管理</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="activities.length===0" class="empty-state"><div class="empty-icon">👥</div><p>暂无活动</p></div>
<div v-else>
<div v-for="a in activities" :key="a.id" class="card mb-16">
<div class="card-header" style="display:flex;align-items:center;justify-content:space-between">
<span>{{a.title}} <span class="badge" :class="sb(a.status)" style="margin-left:8px">{{sl(a.status)}}</span></span>
<span class="mono text-sm text-muted">{{a.registeredCount}}/{{a.maxCount||'∞'}}人</span>
</div>
<div class="card-body" style="padding:0">
<div v-if="!regsMap[a.id]||regsMap[a.id].length===0" class="empty-state" style="padding:20px"><p class="text-muted">暂无报名</p></div>
<table v-else><thead><tr><th>报名人</th><th>状态</th><th>报名时间</th></tr></thead>
<tbody><tr v-for="r in regsMap[a.id]" :key="r.id">
<td>{{r.username||'用户'+r.userId}}</td>
<td><span class="badge" :class="rsb(r.status)">{{rsl(r.status)}}</span></td>
<td class="mono text-sm">{{r.createTime||'—'}}</td>
</tr></tbody></table>
</div>
</div>
</div>
</div>
</template>
<script setup lang="ts">
import {ref,reactive,onMounted} from 'vue'
import {activityApi,registrationApi} from '../services/api'
import {adaptActivity,adaptRegistration} from '../utils/adapters'
import {statusLabel,statusBadge,regStatusLabel,regStatusBadge} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const regsMap=reactive<Record<string,any[]>>({})
const sl=statusLabel;const sb=statusBadge;const rsl=regStatusLabel;const rsb=regStatusBadge
async function load(){
try{
const actRes=await activityApi.list()
if(actRes.code===200)activities.value=(actRes.data||[]).map(adaptActivity)
for(const a of activities.value){
try{
const rRes=await registrationApi.byActivity(Number(a.id))
if(rRes.code===200)regsMap[a.id]=(rRes.data||[]).map(adaptRegistration)
else regsMap[a.id]=[]
}catch{regsMap[a.id]=[]}
}
}catch(e){console.error(e)}
finally{loading.value=false}
}
onMounted(load)
</script>
