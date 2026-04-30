<template>
<div>
<div class="section-title mb-24">我的活动</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="activities.length===0" class="empty-state"><div class="empty-icon">📋</div><p>暂无活动</p></div>
<div v-else class="table-wrap"><table>
<thead><tr><th>活动名称</th><th>类别</th><th>时间</th><th>人数</th><th>状态</th><th>操作</th></tr></thead>
<tbody><tr v-for="a in activities" :key="a.id">
<td style="font-weight:500;cursor:pointer" @click="$emit('viewActivity',a.id)">{{a.title}}</td>
<td>{{a.category}}</td>
<td class="mono text-sm">{{a.startTime||'—'}}</td>
<td class="mono text-sm">{{a.registeredCount}}/{{a.maxCount||'∞'}}</td>
<td><span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span></td>
<td>
<button v-if="a.status==='draft'" class="btn btn-sm" @click="del(a.id)">删除</button>
<span v-else>—</span>
</td>
</tr></tbody>
</table></div>
</div>
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {activityApi} from '../services/api'
import {adaptActivity} from '../utils/adapters'
import {statusLabel,statusBadge} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const sl=statusLabel;const sb=statusBadge
async function load(){
try{
const res=await activityApi.list()
if(res.code===200)activities.value=(res.data||[]).map(adaptActivity)
}catch(e){console.error(e)}
finally{loading.value=false}
}
async function del(id:number){
if(!confirm('确定删除该活动？'))return
try{const res=await activityApi.delete(id);if(res.code===200)await load()}catch(e){console.error(e)}
}
onMounted(load)
</script>
