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
<!-- Desktop table -->
<div class="table-wrap desktop-only"><table>
<thead><tr><th>活动</th><th>加分类型</th><th>分值</th><th>时间</th></tr></thead>
<tbody><tr v-for="r in regs" :key="r.id">
<td style="font-weight:500">{{getAct(r.activityId)?.title}}</td>
<td><span class="badge badge-amber">{{getAct(r.activityId)?.bonusType}}</span></td>
<td class="mono">+{{getAct(r.activityId)?.bonusValue}}</td>
<td class="mono text-sm">{{getAct(r.activityId)?.startTime}}</td>
</tr></tbody>
</table></div>
<!-- Mobile cards -->
<div class="mobile-cards mobile-only">
<div class="mobile-bonus-card" v-for="r in regs" :key="r.id">
<div class="bonus-card-title">{{getAct(r.activityId)?.title}}</div>
<div class="bonus-card-meta">
<span class="badge badge-amber">{{getAct(r.activityId)?.bonusType}}</span>
<span class="mono" style="font-weight:600;color:var(--accent)">+{{getAct(r.activityId)?.bonusValue}}</span>
</div>
<div class="bonus-card-time mono text-sm text-muted">{{getAct(r.activityId)?.startTime}}</div>
</div>
</div>
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

<style scoped>
.desktop-only { display: block; }
.mobile-only { display: none; }

.mobile-bonus-card {
  background: var(--surface);
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius);
  padding: 14px;
  margin-bottom: 10px;
}

.bonus-card-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 6px;
  line-height: 1.3;
}

.bonus-card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}

.bonus-card-time {
  font-size: .72rem;
}

@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: block; }
}
</style>
