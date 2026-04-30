<template>
<div>
<div class="section-title mb-24">数据概览</div>
<div class="grid-4 mb-24">
<div class="stat-card anim-in anim-in-1"><div class="stat-value">{{myActs.length}}</div><div class="stat-label">活动总数</div></div>
<div class="stat-card anim-in anim-in-2"><div class="stat-value">{{pubCount}}</div><div class="stat-label">已发布</div></div>
<div class="stat-card anim-in anim-in-3"><div class="stat-value">{{totalReg}}</div><div class="stat-label">总报名人次</div></div>
<div class="stat-card anim-in anim-in-4"><div class="stat-value">{{pendCount}}</div><div class="stat-label">待审批</div></div>
</div>
<div class="grid-2">
<div class="card"><div class="card-header">近期活动</div><div class="card-body" style="padding:0">
<div v-if="loading" class="empty-state" style="padding:30px"><p>加载中...</p></div>
<div v-else-if="myActs.length===0" class="empty-state" style="padding:30px"><p>暂无活动，点击右侧发布新活动</p></div>
<div v-for="a in myActs.slice(0,5)" :key="a.id" style="padding:12px 20px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;justify-content:space-between;cursor:pointer" @click="$emit('viewActivity',a.id)">
<div><div style="font-weight:500;font-size:.88rem">{{a.title}}</div>
<div class="mono text-xs text-muted">{{a.startTime}} · {{a.registeredCount}}/{{a.maxCount}}人</div></div>
<span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span>
</div></div></div>
<div class="card"><div class="card-header">快捷操作</div><div class="card-body">
<button class="btn w-full mb-8" @click="$emit('navigate','create-activity')">✚ 发布新活动</button>
<button class="btn w-full mb-8" @click="$emit('navigate','my-activities')">📋 管理我的活动</button>
<button class="btn w-full" @click="$emit('navigate','registrations')">👥 查看报名数据</button>
<div style="margin-top:20px;padding:14px;border:1.5px dashed var(--border-light);border-radius:var(--radius)">
<div class="mono text-xs text-muted" style="margin-bottom:4px">💡 提示</div>
<div class="text-sm text-muted">作为活动发布者，你可以发布活动供学生报名参与。所有活动需经管理员审批后发布。</div>
</div></div></div>
</div>
</div>
</template>
<script setup lang="ts">
import {ref,computed,onMounted} from 'vue'
import {activityApi} from '../services/api'
import {adaptActivity} from '../utils/adapters'
import {statusLabel,statusBadge} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const sl=statusLabel;const sb=statusBadge
const myActs=computed(()=>activities.value)
const pubCount=computed(()=>myActs.value.filter(a=>a.status==='published').length)
const pendCount=computed(()=>myActs.value.filter(a=>a.status==='pending').length)
const totalReg=computed(()=>myActs.value.reduce((s,a)=>s+a.registeredCount,0))
onMounted(async()=>{
try{const res=await activityApi.list();if(res.code===200)activities.value=(res.data||[]).map(adaptActivity)}catch(e){console.error(e)}
finally{loading.value=false}
})
</script>
