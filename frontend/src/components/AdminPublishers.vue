<template>
<div>
<div class="section-title mb-24">发布者管理</div>
<div class="grid-3 mb-24">
<div class="stat-card"><div class="stat-value">{{publishers.length}}</div><div class="stat-label">已入驻发布者</div></div>
<div class="stat-card"><div class="stat-value">{{activeCount}}</div><div class="stat-label">活跃发布者</div></div>
<div class="stat-card"><div class="stat-value">0</div><div class="stat-label">待审核入驻</div></div>
</div>
<div v-if="loading" class="card mb-16"><div class="card-body text-center mono text-muted">加载中...</div></div>
<div v-else-if="publishers.length===0" class="card mb-16"><div class="card-body text-center mono text-muted">暂无发布者</div></div>
<div v-for="p in publishers" :key="p.id" class="card mb-16">
<div class="card-body" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px">
<div class="flex items-center gap-12">
<div class="avatar avatar-lg">{{p.avatar}}</div>
<div>
<div style="font-family:var(--font-display);font-size:1.2rem">{{p.name}}</div>
<div class="mono text-sm text-muted">{{p.college}}</div>
<div class="flex gap-6 mt-8">
<span class="badge badge-blue">{{getPublisherActs(p.id).length}} 个活动</span>
<span class="badge badge-green">{{getPublisherActs(p.id).filter(a=>a.status==='published').length}} 已发布</span>
</div>
</div>
</div>
<div class="flex gap-8">
<button class="btn btn-sm">查看详情</button>
<button class="btn btn-sm btn-danger" @click="toggleStatus(p)">{{ p.status===0?'解冻账号':'冻结账号' }}</button>
</div>
</div>
</div>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted,computed} from 'vue'
import {userApi,activityApi} from '../services/api'
import {adaptUser,adaptActivity} from '../utils/adapters'

defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])

const publishers=ref<any[]>([])
const activities=ref<any[]>([])
const loading=ref(true)

const activeCount=computed(()=>publishers.value.filter(p=>activities.value.some(a=>String(a.userId)===p.id&&a.status==='published')).length)

function getPublisherActs(userId:string){return activities.value.filter(a=>String(a.userId)===userId)}

async function toggleStatus(p:any){
const newStatus=p.status===0?1:0
try{
await userApi.updateStatus(Number(p.id),newStatus)
p.status=newStatus
}catch(e:any){
alert(e?.response?.data?.message||'操作失败')
}
}

onMounted(async()=>{
try{
const [userRes,actRes]=await Promise.all([
userApi.list('PUBLISHER'),
activityApi.list()
])
if(userRes.code===200)publishers.value=(userRes.data||[]).map(adaptUser)
if(actRes.code===200)activities.value=(actRes.data||[]).map(adaptActivity)
}catch(e){
console.error('加载发布者数据失败:',e)
}finally{
loading.value=false
}
})
</script>
