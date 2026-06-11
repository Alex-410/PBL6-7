<template>
<div>
<div class="section-title mb-24">全部活动</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<template v-else>
<!-- Desktop -->
<div class="table-wrap desktop-only">
<table>
<thead><tr><th>活动名称</th><th>发布者</th><th>类型</th><th>时间</th><th>报名</th><th>加分</th><th>状态</th><th>操作</th></tr></thead>
<tbody>
<tr v-for="a in activities" :key="a.id">
<td style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',a.id)">{{a.title}}</td>
<td class="mono text-sm">{{a.organizer}}</td>
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
<!-- Mobile -->
<div class="mobile-cards mobile-only">
<div class="mobile-act-card" v-for="a in activities" :key="a.id">
<div class="act-card-header">
<div class="act-card-title" @click="$emit('viewActivity',a.id)">{{a.title}}</div>
<span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span>
</div>
<div class="act-card-meta">
<span class="badge badge-blue">{{a.category}}</span>
<span class="mono text-sm">{{a.organizer}}</span>
<span class="mono text-sm">{{a.startTime}}</span>
<span class="mono text-sm">{{a.registeredCount}}/{{a.maxCount}}人</span>
<span v-if="a.hasBonus" class="badge badge-amber">+{{a.bonusValue}}</span>
</div>
<div class="act-card-actions">
<div v-if="a.status==='pending'" class="flex gap-8">
<button class="btn btn-sm btn-green" @click="approve(a.id)">通过</button>
<button class="btn btn-sm btn-danger" @click="reject(a.id)">驳回</button>
</div>
<button v-else class="btn btn-sm" @click="$emit('viewActivity',a.id)">查看</button>
</div>
</div>
</div>
</template>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {activityApi} from '../services/api'
import {adaptActivity} from '../utils/adapters'
import {statusLabel,statusBadge} from '../mock/data'
defineProps<{user:any}>()
const emit=defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const sl=statusLabel;const sb=statusBadge
async function load(){
try{const res=await activityApi.list();if(res.code===200)activities.value=(res.data||[]).map(adaptActivity)}catch(e){console.error(e)}
finally{loading.value=false}
}
async function approve(id:string){try{await activityApi.audit(Number(id),'approve');await load()}catch(e){console.error(e)}}
async function reject(id:string){try{await activityApi.audit(Number(id),'reject');await load()}catch(e){console.error(e)}}
onMounted(load)
</script>

<style scoped>
.desktop-only { display: block; }
.mobile-only { display: none; }
.mobile-act-card {
  background: var(--surface);
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius);
  padding: 14px;
  margin-bottom: 10px;
}
.act-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}
.act-card-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  line-height: 1.3;
}
.act-card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  margin-bottom: 8px;
}
.act-card-actions {
  display: flex;
  gap: 8px;
}
@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: block; }
}
</style>
