<template>
<div>
<div class="section-title mb-24">我的报名</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="regs.length===0" class="empty-state"><div class="empty-icon">📌</div><p>还没有报名任何活动</p></div>
<template v-else>
<!-- Desktop table -->
<div class="table-wrap desktop-only"><table>
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
<!-- Mobile cards -->
<div class="mobile-cards mobile-only">
<div class="mobile-reg-card" v-for="r in regs" :key="r.id" @click="$emit('viewActivity',r.activityId)">
<div class="reg-card-title">{{getAct(r.activityId)?.title}}</div>
<div class="reg-card-meta">
<span>🕐 {{getAct(r.activityId)?.startTime}}</span>
<span>📍 {{getAct(r.activityId)?.location}}</span>
</div>
<div class="reg-card-footer">
<span class="badge" :class="rsb(r.status)">{{rsl(r.status)}}</span>
<button v-if="r.status==='registered'" class="btn btn-sm btn-danger" @click.stop="cancel(r.id)">取消</button>
<span v-else-if="r.status==='completed'&&getAct(r.activityId)?.hasBonus" class="badge badge-amber">已加分</span>
</div>
</div>
</div>
</template>
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

<style scoped>
.desktop-only { display: block; }
.mobile-only { display: none; }

.mobile-reg-card {
  background: var(--surface);
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius);
  padding: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all .12s;
}
.mobile-reg-card:hover { border-color: var(--border); }

.reg-card-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 6px;
  line-height: 1.3;
}

.reg-card-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-family: var(--font-mono);
  font-size: .72rem;
  color: var(--ink-muted);
  margin-bottom: 8px;
}

.reg-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: block; }
}
</style>
