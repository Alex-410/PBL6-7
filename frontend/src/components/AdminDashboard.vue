<template>
<div>
<div class="section-title mb-24">平台概览</div>
<div class="grid-4 mb-24">
<div class="stat-card anim-in anim-in-1"><div class="stat-value">{{totalActs}}</div><div class="stat-label">活动总数</div></div>
<div class="stat-card anim-in anim-in-2"><div class="stat-value">{{published}}</div><div class="stat-label">已发布</div></div>
<div class="stat-card anim-in anim-in-3"><div class="stat-value">{{pending}}</div><div class="stat-label">待审批</div></div>
<div class="stat-card anim-in anim-in-4"><div class="stat-value">{{totalRegs}}</div><div class="stat-label">报名总数</div></div>
</div>
<div class="grid-2 mb-24">
<div class="card"><div class="card-header">待审批活动 <span class="badge badge-amber">{{pending}}</span></div>
<div class="card-body" style="padding:0">
<div v-if="pendingActs.length===0" class="empty-state" style="padding:30px"><p>暂无待审批活动</p></div>
<div v-for="a in pendingActs" :key="a.id" style="padding:12px 20px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;justify-content:space-between">
<div><div style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',a.id)">{{a.title}}</div>
<div class="mono text-xs text-muted">{{a.college}} · {{a.startTime}}</div></div>
<div class="flex gap-8"><button class="btn btn-sm btn-green" @click="approve(a.id)">通过</button>
<button class="btn btn-sm btn-danger" @click="reject(a.id)">驳回</button></div>
</div></div></div>
<div class="card"><div class="card-header">平台统计</div><div class="card-body">
<div style="margin-bottom:16px">
<div v-for="cat in catStats" :key="cat.name" style="margin-bottom:8px">
<div class="flex justify-between mono text-xs"><span>{{cat.name}}</span><span>{{cat.count}} ({{cat.pct}}%)</span></div>
<div class="progress-bar"><div class="progress-bar-fill" :style="{width:cat.pct+'%'}"></div></div>
</div></div>
<div style="padding-top:12px;border-top:1px solid var(--border-light)"><div class="grid-2 gap-12">
<div><div class="mono text-xs text-muted">加分活动</div><div style="font-family:var(--font-display);font-size:1.3rem">{{bonusActs}}</div></div>
<div><div class="mono text-xs text-muted">总用户数</div><div style="font-family:var(--font-display);font-size:1.3rem">{{totalUsers}}</div></div>
</div></div>
</div></div>
</div>
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_REGISTRATIONS,MOCK_USERS} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const totalActs=computed(()=>MOCK_ACTIVITIES.length)
const published=computed(()=>MOCK_ACTIVITIES.filter(a=>a.status==='published').length)
const pending=computed(()=>MOCK_ACTIVITIES.filter(a=>a.status==='pending').length)
const totalRegs=computed(()=>MOCK_REGISTRATIONS.length)
const totalUsers=computed(()=>MOCK_USERS.length)
const bonusActs=computed(()=>MOCK_ACTIVITIES.filter(a=>a.hasBonus).length)
const pendingActs=computed(()=>MOCK_ACTIVITIES.filter(a=>a.status==='pending'))
const catStats=computed(()=>{
const cats=['学术','文艺','体育','公益','社交','就业','讲座']
return cats.map(c=>{const count=MOCK_ACTIVITIES.filter(a=>a.category===c).length;return{name:c,count,pct:totalActs.value?Math.round(count/totalActs.value*100):0}})
})
function approve(id:string){const a=MOCK_ACTIVITIES.find(x=>x.id===id);if(a){a.status='published';a.approvalStatus='approved'}}
function reject(id:string){const a=MOCK_ACTIVITIES.find(x=>x.id===id);if(a){a.status='rejected';a.approvalStatus='rejected'}}
</script>
