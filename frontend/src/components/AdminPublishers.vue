<template>
<div>
<div class="section-title mb-24">发布者管理</div>
<div class="grid-3 mb-24">
<div class="stat-card"><div class="stat-value">{{publishers.length}}</div><div class="stat-label">已入驻发布者</div></div>
<div class="stat-card"><div class="stat-value">{{activeCount}}</div><div class="stat-label">活跃发布者</div></div>
<div class="stat-card"><div class="stat-value">0</div><div class="stat-label">待审核入驻</div></div>
</div>
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
<button class="btn btn-sm btn-danger">冻结账号</button>
</div>
</div>
</div>
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_USERS,MOCK_ACTIVITIES} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const publishers=computed(()=>MOCK_USERS.filter(u=>u.role==='publisher'))
const activeCount=computed(()=>publishers.value.filter(p=>MOCK_ACTIVITIES.some(a=>a.creatorId===p.id&&a.status==='published')).length)
function getPublisherActs(id:string){return MOCK_ACTIVITIES.filter(a=>a.creatorId===id)}
</script>
