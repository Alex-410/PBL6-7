<template>
<div>
<div class="section-title mb-24">数据报表</div>
<div class="grid-2 mb-24">
<div class="card"><div class="card-header">活动类型分布</div><div class="card-body">
<div v-for="[cat,count] in catEntries" :key="cat" style="margin-bottom:12px">
<div class="flex justify-between mono text-sm mb-8"><span>{{icons[cat]||'📌'}} {{cat}}</span><span>{{count}} 个</span></div>
<div class="progress-bar"><div class="progress-bar-fill" :style="{width:Math.round(count/maxCat*100)+'%'}"></div></div>
</div>
</div></div>
<div class="card"><div class="card-header">报名排行 Top 5</div><div class="card-body" style="padding:0">
<div v-for="(a,i) in top5" :key="a.id" style="padding:12px 20px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;gap:12px">
<span style="font-family:var(--font-display);font-size:1.4rem;width:28px" :style="{color:i===0?'var(--accent)':i===1?'var(--amber)':'var(--ink-muted)'}">{{i+1}}</span>
<div style="flex:1"><div style="font-weight:500;font-size:.88rem">{{a.title}}</div><div class="mono text-xs text-muted">{{a.category}} · {{a.college}}</div></div>
<span class="mono text-sm" style="font-weight:500">{{a.registeredCount}}人</span>
</div>
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
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_REGISTRATIONS,MOCK_USERS,CAT_ICONS} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const icons=CAT_ICONS
const catCounts=computed(()=>{
const m:Record<string,number>={}
MOCK_ACTIVITIES.forEach(a=>{m[a.category]=(m[a.category]||0)+1})
return m
})
const catEntries=computed(()=>Object.entries(catCounts.value).sort((a,b)=>b[1]-a[1]))
const maxCat=computed(()=>Math.max(...Object.values(catCounts.value),1))
const top5=computed(()=>[...MOCK_ACTIVITIES].sort((a,b)=>b.registeredCount-a.registeredCount).slice(0,5))
const publishedActs=computed(()=>MOCK_ACTIVITIES.filter(a=>a.status==='published'))
const avgRegRate=computed(()=>{
const p=publishedActs.value
if(p.length===0)return 0
const total=p.reduce((s,a)=>s+a.registeredCount,0)
const cap=p.reduce((s,a)=>s+a.maxCount,0)
return cap?Math.round(total/cap*100):0
})
const avgPerStudent=computed(()=>{
const sc=MOCK_USERS.filter(u=>u.role==='student').length
return sc?(MOCK_REGISTRATIONS.length/sc).toFixed(1):'0'
})
const bonusCoverage=computed(()=>{
const t=MOCK_ACTIVITIES.length
return t?Math.round(MOCK_ACTIVITIES.filter(a=>a.hasBonus).length/t*100):0
})
const approvalRate=computed(()=>{
const total=MOCK_ACTIVITIES.filter(a=>a.approvalStatus!=='draft').length
return total?Math.round(MOCK_ACTIVITIES.filter(a=>a.approvalStatus==='approved').length/total*100):0
})
</script>
