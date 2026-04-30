<template>
<div>
<div class="section-title mb-24">个人中心</div>
<div style="max-width:560px">
<div class="card mb-24"><div class="card-body" style="display:flex;gap:20px;align-items:center">
<div class="avatar avatar-lg">{{user.avatar}}</div>
<div><div style="font-family:var(--font-display);font-size:1.4rem">{{user.name}}</div>
<div class="mono text-sm text-muted">{{user.college}} · {{user.grade}}</div></div>
</div></div>
<div class="card mb-24"><div class="card-header">基本信息</div><div class="card-body">
<div class="form-group"><label>用户名</label><input :value="user.username" disabled style="background:var(--surface-alt)"></div>
<div class="form-group"><label>邮箱</label><input :value="user.email"></div>
<div class="form-group"><label>手机</label><input :value="user.phone"></div>
<div class="form-group"><label>兴趣标签</label>
<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">
<span class="tag" v-for="t in (user.tags||[])" :key="t">{{t}}</span>
<span class="tag" style="cursor:pointer;border-style:dashed;color:var(--accent)">+ 添加</span>
</div></div>
<button class="btn btn-primary mt-8">保存修改</button>
</div></div>
<div class="card"><div class="card-header">账号统计</div><div class="card-body"><div class="grid-2">
<div><div class="mono text-sm text-muted">已报名活动</div><div style="font-family:var(--font-display);font-size:1.6rem">{{regCount}}</div></div>
<div><div class="mono text-sm text-muted">已完成活动</div><div style="font-family:var(--font-display);font-size:1.6rem">{{doneCount}}</div></div>
</div></div></div>
</div>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {registrationApi} from '../services/api'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const regCount=ref(0)
const doneCount=ref(0)
onMounted(async()=>{
try{
const res=await registrationApi.myRegistrations()
if(res.code===200){
const regs=res.data||[]
regCount.value=regs.length
doneCount.value=regs.filter((r:any)=>r.status==='completed').length
}
}catch(e){console.error(e)}
})
</script>
