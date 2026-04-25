<template>
<div>
<div class="section-title mb-24">全部活动</div>
<div class="table-wrap">
<table>
<thead><tr><th>活动名称</th><th>发布者</th><th>类型</th><th>时间</th><th>报名</th><th>加分</th><th>状态</th><th>操作</th></tr></thead>
<tbody>
<tr v-for="a in all" :key="a.id">
<td style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',a.id)">{{a.title}}</td>
<td class="mono text-sm">{{getCreator(a.creatorId)?.name||'—'}}</td>
<td><span class="badge badge-blue">{{a.category}}</span></td>
<td class="mono text-sm">{{a.startTime}}</td>
<td class="mono text-sm">{{a.registeredCount}}/{{a.maxCount}}</td>
<td><span v-if="a.hasBonus" class="badge badge-amber">+{{a.bonusValue}}</span><span v-else>—</span></td>
<td><span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span></td>
<td><div v-if="a.status==='pending'" class="flex gap-8"><button class="btn btn-sm btn-green" @click="approve(a.id)">✓</button><button class="btn btn-sm btn-danger" @click="reject(a.id)">✕</button></div><button v-else class="btn btn-sm" @click="$emit('viewActivity',a.id)">查看</button></td>
</tr>
</tbody>
</table>
</div>
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_USERS,statusLabel,statusBadge} from '../mock/data'
defineProps<{user:any}>()
const emit=defineEmits(['viewActivity','navigate'])
const sl=statusLabel;const sb=statusBadge
const all=computed(()=>MOCK_ACTIVITIES)
function getCreator(id:string){return MOCK_USERS.find(u=>u.id===id)}
function approve(id:string){const a=MOCK_ACTIVITIES.find(x=>x.id===id);if(a){a.status='published';a.approvalStatus='approved'}}
function reject(id:string){const a=MOCK_ACTIVITIES.find(x=>x.id===id);if(a){a.status='rejected';a.approvalStatus='rejected'}}
</script>
