<template>
<div>
<div class="section-title mb-24">加分记录</div>
<div v-if="regs.length===0" class="empty-state"><div class="empty-icon">🎖️</div><p>暂无加分记录</p></div>
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
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_REGISTRATIONS} from '../mock/data'
const props=defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const regs=computed(()=>MOCK_REGISTRATIONS.filter(r=>{const a=getAct(r.activityId);return r.userId===props.user.id&&a?.hasBonus&&['completed','checked_in'].includes(r.status)}))
const total=computed(()=>regs.value.reduce((s,r)=>s+(getAct(r.activityId)?.bonusValue||0),0).toFixed(1))
const volHours=computed(()=>regs.value.filter(r=>getAct(r.activityId)?.bonusType==='志愿时长').reduce((s,r)=>s+(getAct(r.activityId)?.bonusValue||0),0))
function getAct(id:string){return MOCK_ACTIVITIES.find(a=>a.id===id)}
</script>
