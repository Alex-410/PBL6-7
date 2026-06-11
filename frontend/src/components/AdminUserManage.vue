<template>
<div>
<div class="section-title mb-24">用户管理</div>
<div class="grid-3 mb-24">
<div class="stat-card"><div class="stat-value">{{users.length}}</div><div class="stat-label">总用户</div></div>
<div class="stat-card"><div class="stat-value">{{studentCount}}</div><div class="stat-label">学生</div></div>
<div class="stat-card"><div class="stat-value">{{publisherCount}}</div><div class="stat-label">发布者</div></div>
</div>
<div v-if="loading" class="card"><div class="card-body text-center mono text-muted">加载中...</div></div>
<template v-else>
<!-- Desktop -->
<div class="table-wrap desktop-only">
<table>
<thead><tr><th>用户</th><th>用户名</th><th>角色</th><th>院系</th><th>操作</th></tr></thead>
<tbody>
<tr v-for="u in users" :key="u.id">
<td><div class="flex items-center gap-8"><div class="avatar" style="width:28px;height:28px;font-size:.72rem">{{u.avatar}}</div><span style="font-weight:500">{{u.name}}</span></div></td>
<td class="mono text-sm">{{u.username}}</td>
<td><span class="badge" :class="u.role==='ADMIN'?'badge-purple':u.role==='PUBLISHER'?'badge-amber':u.role==='STUDENT_PUBLISHER'?'badge-green':'badge-blue'">{{roleLabel(u.role)}}</span></td>
<td class="mono text-sm">{{u.college}}</td>
<td><button v-if="u.role==='USER'||u.role==='STUDENT_PUBLISHER'" class="btn btn-sm" :class="u.role==='USER'?'btn-primary':'btn-outline'" @click="changeRole(u)">{{u.role==='USER'?'授予权限':'撤销权限'}}</button></td>
</tr>
</tbody>
</table>
</div>
<!-- Mobile -->
<div class="mobile-cards mobile-only">
<div class="mobile-user-card" v-for="u in users" :key="u.id">
<div class="user-card-header">
<div class="flex items-center gap-8">
<div class="avatar" style="width:32px;height:32px;font-size:.8rem">{{u.avatar}}</div>
<div>
<div style="font-weight:500;font-size:.9rem">{{u.name}}</div>
<div class="mono text-xs text-muted">{{u.username}}</div>
</div>
</div>
<span class="badge" :class="u.role==='ADMIN'?'badge-purple':u.role==='PUBLISHER'?'badge-amber':u.role==='STUDENT_PUBLISHER'?'badge-green':'badge-blue'">{{roleLabel(u.role)}}</span>
</div>
<div class="user-card-meta mono text-sm text-muted">{{u.college}}</div>
<button v-if="u.role==='USER'||u.role==='STUDENT_PUBLISHER'" class="btn btn-sm mt-8" :class="u.role==='USER'?'btn-primary':'btn-outline'" @click="changeRole(u)">{{u.role==='USER'?'授予权限':'撤销权限'}}</button>
</div>
</div>
</template>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted,computed} from 'vue'
import {userApi} from '../services/api'
import {adaptUser} from '../utils/adapters'

defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])

const users=ref<any[]>([])
const loading=ref(true)

const studentCount=computed(()=>users.value.filter(u=>u.role==='USER'||u.role==='STUDENT_PUBLISHER').length)
const publisherCount=computed(()=>users.value.filter(u=>u.role==='PUBLISHER'||u.role==='STUDENT_PUBLISHER').length)

function roleLabel(r:string){
const m:Record<string,string>={USER:'学生',ADMIN:'管理员',PUBLISHER:'发布者',STUDENT_PUBLISHER:'学生·发布者'}
return m[r]||r
}

async function changeRole(u:any){
const newRole=u.role==='USER'?'STUDENT_PUBLISHER':'USER'
const actionLabel=newRole==='STUDENT_PUBLISHER'?'授予活动发布权限':'撤销活动发布权限'
try{
const res=await userApi.updateRole(Number(u.id),newRole)
if(res.code===200){
u.role=newRole
alert(`${actionLabel}成功`)
}else{
alert(res.message||'操作失败')
}
}catch(e:any){
alert(e?.response?.data?.message||'操作失败')
}
}

onMounted(async()=>{
try{
const res=await userApi.list()
if(res.code===200)users.value=(res.data||[]).map(adaptUser)
}catch(e){
console.error('加载用户数据失败:',e)
}finally{
loading.value=false
}
})
</script>

<style scoped>
.desktop-only { display: block; }
.mobile-only { display: none; }
.mobile-user-card {
  background: var(--surface);
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius);
  padding: 14px;
  margin-bottom: 10px;
}
.user-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.user-card-meta {
  font-size: .72rem;
}
@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: block; }
}
</style>
