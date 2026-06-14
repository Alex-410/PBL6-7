<template>
<div>
<div class="section-title mb-24">我的活动</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="activities.length===0" class="empty-state"><div class="empty-icon">📋</div><p>暂无活动</p></div>
<template v-else>
<!-- Desktop -->
<div class="table-wrap desktop-only"><table>
<thead><tr><th>活动名称</th><th>类别</th><th>时间</th><th>人数</th><th>状态</th><th>操作</th></tr></thead>
<tbody><tr v-for="a in activities" :key="a.id">
<td style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',a.id)">{{a.title}}</td>
<td>{{a.category}}</td>
<td class="mono text-sm">{{a.startTime||'—'}}</td>
<td class="mono text-sm">{{a.registeredCount}}/{{a.maxCount||'∞'}}</td>
<td><span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span></td>
<td><button v-if="a.status==='draft'" class="btn btn-sm" @click="del(a.id)">删除</button><span v-else>—</span></td>
</tr></tbody>
</table></div>
<!-- Mobile -->
<div class="mobile-cards mobile-only">
<div class="mobile-act-card" v-for="a in activities" :key="a.id" @click="$emit('viewActivity',a.id)">
<div class="act-card-header">
<div class="act-card-title">{{a.title}}</div>
<span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span>
</div>
<div class="act-card-meta">
<span>{{a.category}}</span>
<span>{{a.startTime||'—'}}</span>
<span>{{a.registeredCount}}/{{a.maxCount||'∞'}}人</span>
</div>
<button v-if="a.status==='draft'" class="btn btn-sm" @click.stop="del(a.id)">删除</button>
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
defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const sl=statusLabel;const sb=statusBadge
async function load(){
try{
const res=await activityApi.my()
if(res.code===200)activities.value=(res.data||[]).map(adaptActivity)
}catch(e){console.error(e)}
finally{loading.value=false}
}
async function del(id:number){
if(!confirm('确定删除该活动？'))return
try{const res=await activityApi.delete(id);if(res.code===200)await load()}catch(e){console.error(e)}
}
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
  cursor: pointer;
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
  line-height: 1.3;
}
.act-card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: .72rem;
  color: var(--ink-muted);
  margin-bottom: 8px;
}
@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: block; }
}
</style>
