<template>
<div>
<div class="section-title mb-24">我的报名</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="regs.length===0" class="empty-state"><div class="empty-icon">📌</div><p>还没有报名任何活动</p></div>
<div v-else class="table-wrap"><table>
<thead><tr><th>活动名称</th><th>时间</th><th>地点</th><th>状态</th><th>操作</th></tr></thead>
<tbody><tr v-for="r in regs" :key="r.id">
<td style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',r.activityId)">{{getAct(r.activityId)?.title}}</td>
<td class="mono text-sm">{{getAct(r.activityId)?.startTime}}</td>
<td class="mono text-sm">{{getAct(r.activityId)?.location}}</td>
<td><span class="badge" :class="rsb(r.status)">{{rsl(r.status)}}</span></td>
<td><button v-if="r.status==='registered'" class="btn btn-sm btn-danger" @click="cancel(r.id)">取消报名</button>
<span v-else-if="r.status==='completed'&&getAct(r.activityId)?.hasBonus" class="badge badge-amber">已加分</span>
<span v-else>—</span></td>
</tr></tbody>
</table></div>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {activityApi,registrationApi} from '../services/api'
import {adaptActivity,adaptRegistration} from '../utils/adapters'
import {regStatusLabel,regStatusBadge} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const regs=ref<any[]>([])
const rsl=regStatusLabel;const rsb=regStatusBadge
function getAct(id:string){return activities.value.find(a=>a.id===id)}
async function load(){
try{
const[actRes,regRes]=await Promise.all([activityApi.list(),registrationApi.myRegistrations()])
if(actRes.code===200)activities.value=(actRes.data||[]).map(adaptActivity)
if(regRes.code===200)regs.value=(regRes.data||[]).map(adaptRegistration)
}catch(e){console.error('load failed',e)}
finally{loading.value=false}
}
async function cancel(id:string){
try{
const res=await registrationApi.cancel(Number(id))
if(res.code===200){await load()}
}catch(e){console.error('cancel failed',e)}
}
onMounted(load)
</script>
