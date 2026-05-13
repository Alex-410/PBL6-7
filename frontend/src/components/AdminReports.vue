<template>
<div>
<div class="section-title mb-24">数据报表</div>
<div v-if="loading" class="card"><div class="card-body text-center mono text-muted">加载中...</div></div>
<template v-else>
<div class="grid-2 mb-24">
<div class="card"><div class="card-header">活动类型分布</div><div class="card-body">
<div v-for="[cat,count] in catEntries" :key="cat" style="margin-bottom:12px">
<div class="flex justify-between mono text-sm mb-8"><span>{{icons[cat]||'📌'}} {{cat}}</span><span>{{count}} 个</span></div>
<div class="progress-bar"><div class="progress-bar-fill" :style="{width:Math.round(count/maxCat*100)+'%'}"></div></div>
</div>
<div v-if="catEntries.length===0" class="mono text-sm text-muted text-center">暂无数据</div>
</div></div>
<div class="card"><div class="card-header">报名排行 Top 5</div><div class="card-body" style="padding:0">
<div v-for="(a,i) in top5" :key="a.id" style="padding:12px 20px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;gap:12px">
<span style="font-family:var(--font-display);font-size:1.4rem;width:28px" :style="{color:i===0?'var(--accent)':i===1?'var(--amber)':'var(--ink-muted)'}">{{Number(i)+1}}</span>
<div style="flex:1"><div style="font-weight:500;font-size:.88rem">{{a.title}}</div><div class="mono text-xs text-muted">{{a.category}} · {{a.college}}</div></div>
<span class="mono text-sm" style="font-weight:500">{{a.registeredCount}}人</span>
</div>
<div v-if="top5.length===0" class="mono text-sm text-muted text-center" style="padding:20px">暂无数据</div>
</div></div>
</div>
<div class="card"><div class="card-header">关键指标</div><div class="card-body">
<div class="grid-4">
<div><div class="mono text-xs text-muted">平均报名率</div><div style="font-family:var(--font-display);font-size:1.6rem">{{avgRegRate}}%</div></div>
<div><div class="mono text-xs text-muted">人均报名</div><div style="font-family:var(--font-display);font-size:1.6rem">{{avgPerStudent}}</div></div>
<div><div class="mono text-xs text-muted">加分覆盖率</div><div style="font-family:var(--font-display);font-size:1.6rem">{{bonusCoverage}}%</div></div>
<div><div class="mono text-xs text-muted">审批通过率</div><div style="font-family:var(--font-display);font-size:1.6rem">{{approvalRate}}%</div></div>
</div>
</div></div>
</template>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted,computed} from 'vue'
import {adminApi} from '../services/api'
import {adaptActivity} from '../utils/adapters'
import {CAT_ICONS} from '../mock/data'

defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])

const icons=CAT_ICONS
const loading=ref(true)
const stats=ref<any>({})

const catEntries=computed(()=>{
const dist=stats.value.categoryDistribution||[]
return dist.map((d:any)=>[d.category||d.CATEGORY,d.count||d.COUNT]).sort((a:[string,number],b:[string,number])=>b[1]-a[1])
})
const maxCat=computed(()=>{const vals=catEntries.value.map((e:[string,number])=>e[1]);return Math.max(...vals,1)})
const top5=computed(()=>(stats.value.topActivities||[]).map(adaptActivity).slice(0,5))
const avgRegRate=computed(()=>{
const cap=stats.value.totalCapacity||0
const reg=stats.value.totalRegistered||0
return cap?Math.round(reg/cap*100):0
})
const avgPerStudent=computed(()=>{
const sc=stats.value.studentCount||0
const tr=stats.value.totalRegistrations||0
return sc?(tr/sc).toFixed(1):'0'
})
const bonusCoverage=computed(()=>{
const total=stats.value.totalActivities||0
const bonus=stats.value.bonusActivities||0
return total?Math.round(bonus/total*100):0
})
const approvalRate=computed(()=>{
const published=stats.value.publishedActivities||0
const rejected=stats.value.rejectedActivities||0
const total=published+rejected+(stats.value.pendingActivities||0)
return total?Math.round(published/total*100):0
})

onMounted(async()=>{
try{
const res=await adminApi.stats()
if(res.code===200)stats.value=res.data||{}
}catch(e){
console.error('加载统计数据失败:',e)
}finally{
loading.value=false
}
})
</script>
