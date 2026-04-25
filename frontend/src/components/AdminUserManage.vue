<template>
<div>
<div class="section-title mb-24">用户管理</div>
<div class="grid-3 mb-24">
<div class="stat-card"><div class="stat-value">{{MOCK_USERS.length}}</div><div class="stat-label">总用户</div></div>
<div class="stat-card"><div class="stat-value">{{studentCount}}</div><div class="stat-label">学生</div></div>
<div class="stat-card"><div class="stat-value">{{publisherCount}}</div><div class="stat-label">发布者</div></div>
</div>
<div class="table-wrap">
<table>
<thead><tr><th>用户</th><th>用户名</th><th>角色</th><th>院系</th><th>操作</th></tr></thead>
<tbody>
<tr v-for="u in MOCK_USERS" :key="u.id">
<td><div class="flex items-center gap-8"><div class="avatar" style="width:28px;height:28px;font-size:.72rem">{{u.avatar}}</div><span style="font-weight:500">{{u.name}}</span></div></td>
<td class="mono text-sm">{{u.username}}</td>
<td><span class="badge" :class="u.role==='admin'?'badge-purple':u.role==='publisher'?'badge-amber':'badge-blue'">{{roleLabel(u.role)}}</span></td>
<td class="mono text-sm">{{u.college}}</td>
<td><button class="btn btn-sm">编辑</button></td>
</tr>
</tbody>
</table>
</div>
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_USERS,roleLabel} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const studentCount=computed(()=>MOCK_USERS.filter(u=>u.role==='student').length)
const publisherCount=computed(()=>MOCK_USERS.filter(u=>u.role==='publisher').length)
</script>
