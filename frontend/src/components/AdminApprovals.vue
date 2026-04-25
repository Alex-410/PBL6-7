<template>
<div>
<div class="section-title mb-24">活动审批</div>
<div class="filter-bar mb-16">
<button class="filter-chip active">待审批 ({{pending.length}})</button>
<button class="filter-chip" @click="$emit('navigate','all-activities')">查看全部</button>
</div>
<div v-if="pending.length===0" class="empty-state"><div class="empty-icon">✅</div><p>所有活动已审批完毕</p></div>
<div v-else class="table-wrap">
<table>
<thead><tr><th>活动名称</th><th>发布者</th><th>类型</th><th>时间</th><th>人数</th><th>加分</th><th>操作</th></tr></thead>
<tbody>
<tr v-for="a in pending" :key="a.id">
<td style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',a.id)">{{a.title}}</td>
<td class="mono text-sm">{{getCreator(a.creatorId)?.name||'—'}}</td>
<td><span class="badge badge-blue">{{a.category}}</span></td>
<td class="mono text-sm">{{a.startTime}}</td>
<td class="mono text-sm">{{a.maxCount}}</td>
<td><span v-if="a.hasBonus" class="badge badge-amber">{{a.bonusType}} +{{a.bonusValue}}</span><span v-else>—</span></td>
<td><div class="flex gap-8"><button class="btn btn-sm btn-green" @click="approve(a.id)">通过</button><button class="btn btn-sm btn-danger" @click="reject(a.id)">驳回</button></div></td>
</tr>
</tbody>
</table>
</div>
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_USERS} from '../mock/data'
defineProps<{user:any}>()
const emit=defineEmits(['viewActivity','navigate'])
const pending=computed(()=>MOCK_ACTIVITIES.filter(a=>a.status==='pending'))
function getCreator(id:string){return MOCK_USERS.find(u=>u.id===id)}
function approve(id:string){const a=MOCK_ACTIVITIES.find(x=>x.id===id);if(a){a.status='published';a.approvalStatus='approved'}}
function reject(id:string){const a=MOCK_ACTIVITIES.find(x=>x.id===id);if(a){a.status='rejected';a.approvalStatus='rejected'}}
</script>
