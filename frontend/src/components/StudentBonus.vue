<template>
<div>
<div class="section-title mb-24">加分记录</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="regs.length===0" class="empty-state"><div class="empty-icon">🎖️</div><p>暂无加分记录</p></div>
<template v-else>
<div class="grid-3 mb-24">
<div class="stat-card"><div class="stat-value">{{regs.length}}</div><div class="stat-label">加分活动</div></div>
<div class="stat-card"><div class="stat-value">{{total}}</div><div class="stat-label">累计加分</div></div>
<div class="stat-card"><div class="stat-value">{{volHours}}</div><div class="stat-label">志愿时长(h)</div></div>
</div>
<div class="table-wrap"><table>
<thead><tr><th>活动</th><th>加分类型</th><th>分值</th><th>时间</th></tr></thead>
<tbody><tr v-for="r in regs" :key="r.id">
<td style="font-weight:500">{{getAct(r.activityId)?.title}}</td>
<td><span class="badge badge-amber">{{getAct(r.activityId)?.bonusType}}</span></td>
<td class="mono">+{{getAct(r.activityId)?.bonusValue}}</td>
<td class="mono text-sm">{{getAct(r.activityId)?.startTime}}</td>
</tr></tbody>
</table></div>
</template>
</div>
</template>
<script setup lang="ts">
import {ref,computed,onMounted} from 'vue'
import {activityApi,registrationApi} from '../services/api'
import {adaptActivity,adaptRegistration} from '../utils/adapters'
const loading=ref(true)
const activities=ref<any[]>([])
const regs=ref<any[]>([])
defineEmits(['viewActivity','navigate'])
function getAct(id:string){return activities.value.find(a=>a.id===id)}
const total=computed(()=>regs.value.reduce((s,r)=>s+(getAct(r.activityId)?.bonusValue||0),0).toFixed(1))
const volHours=computed(()=>regs.value.filter(r=>getAct(r.activityId)?.bonusType==='志愿时长').reduce((s,r)=>s+(getAct(r.activityId)?.bonusValue||0),0))
onMounted(async()=>{
try{
const[actRes,regRes]=await Promise.all([activityApi.list(),registrationApi.myRegistrations()])
if(actRes.code===200)activities.value=(actRes.data||[]).map(adaptActivity)
if(regRes.code===200){
const all=(regRes.data||[]).map(adaptRegistration)
regs.value=all.filter((r:any)=>{
const a=activities.value.find(x=>x.id===r.activityId)
return a?.hasBonus&&['completed','checked_in'].includes(r.status)
})
}
}catch(e){console.error('load failed',e)}
finally{loading.value=false}
})
</script>
