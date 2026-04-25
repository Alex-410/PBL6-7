<template>
<div>
<div class="section-title mb-24">我的报名</div>
<div v-if="regs.length===0" class="empty-state"><div class="empty-icon">📌</div><p>还没有报名任何活动</p></div>
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
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_REGISTRATIONS,regStatusLabel,regStatusBadge} from '../mock/data'
const props=defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const rsl=regStatusLabel;const rsb=regStatusBadge
const regs=computed(()=>MOCK_REGISTRATIONS.filter(r=>r.userId===props.user.id))
function getAct(id:string){return MOCK_ACTIVITIES.find(a=>a.id===id)}
function cancel(id:string){const r=MOCK_REGISTRATIONS.find(x=>x.id===id);if(r){r.status='cancelled';const a=getAct(r.activityId);if(a)a.registeredCount=Math.max(0,a.registeredCount-1)}}
</script>
