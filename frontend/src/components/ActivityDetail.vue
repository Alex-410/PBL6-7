<template>
<div>
<button class="btn btn-ghost mb-16" @click="$emit('navigate','dashboard')">← 返回</button>
<div v-if="!a" class="empty-state"><p>活动未找到</p></div>
<template v-else>
<div class="detail-header">
<div class="detail-img" :style="{background:colors[Number(a.id.replace('a',''))%colors.length]}">
<span style="font-size:5rem;opacity:.3">{{icons[a.category]||'📌'}}</span>
</div>
<div class="detail-info">
<div class="flex gap-8 mb-8" style="flex-wrap:wrap">
<span class="badge badge-blue">{{a.category}}</span>
<span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span>
<span class="badge badge-amber" v-if="a.hasBonus">🎖 {{a.bonusType}} +{{a.bonusValue}}</span>
<span class="badge badge-purple" v-if="a.fee>0">¥{{a.fee}}</span>
</div>
<h1 style="font-family:var(--font-display);font-size:2rem;margin-bottom:8px">{{a.title}}</h1>
<div class="detail-meta">
<span class="detail-meta-item">🏫 {{a.college}}</span>
<span class="detail-meta-item">👤 {{creator?.name||'—'}}</span>
</div>
<div class="detail-meta">
<span class="detail-meta-item">🕐 {{a.startTime}} ~ {{a.endTime}}</span>
<span class="detail-meta-item">📍 {{a.location}}</span>
<span class="detail-meta-item">👥 {{a.registeredCount}} / {{a.maxCount}} 人</span>
</div>
<div style="margin:12px 0"><div class="progress-bar" style="height:6px"><div class="progress-bar-fill" :style="{width:pct+'%',...(full?{background:'var(--accent)'}:{})}"></div></div></div>
<div v-if="user.role==='student'" class="detail-actions">
<span v-if="a.status==='completed'" class="badge badge-gray">活动已结束</span>
<span v-else-if="full&&!reg" class="badge badge-red">报名已满</span>
<button v-else-if="reg" class="btn btn-accent" @click="cancelReg">取消报名</button>
<button v-else class="btn btn-primary" @click="doReg">立即报名</button>
</div>
</div>
</div>
<div class="grid-2" style="gap:24px">
<div>
<div class="card mb-16"><div class="card-header">活动详情</div><div class="card-body">
<p style="line-height:1.9;font-size:.92rem">{{a.description}}</p>
<div v-if="a.tags.length" style="margin-top:16px"><span class="tag" v-for="t in a.tags" :key="t">{{t}}</span></div>
</div></div>
<div v-if="a.hasBonus" class="card"><div class="card-header">加分信息</div><div class="card-body"><div class="grid-2">
<div><div class="mono text-xs text-muted">加分类型</div><div style="font-weight:500;margin-top:4px">{{a.bonusType}}</div></div>
<div><div class="mono text-xs text-muted">加分分值</div><div style="font-weight:500;margin-top:4px">+{{a.bonusValue}}</div></div>
</div></div></div>
</div>
<div><div class="card"><div class="card-header">组织者信息</div><div class="card-body">
<div class="flex items-center gap-12 mb-16"><div class="avatar avatar-lg">{{creator?.avatar||'?'}}</div><div>
<div style="font-weight:500;font-size:1rem">{{creator?.name||'—'}}</div>
<div class="mono text-sm text-muted">{{creator?.college||'—'}}</div>
</div></div>
<div class="mono text-sm text-muted">{{creator?.email||'—'}}</div>
</div></div></div>
</div>
</template>
</div>
</template>
<script setup lang="ts">
import {computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_REGISTRATIONS,MOCK_USERS,MOCK_NOTIFICATIONS,COLORS,CAT_ICONS,statusLabel,statusBadge,today} from '../mock/data'
const props=defineProps<{user:any}>()
const emit=defineEmits(['viewActivity','navigate'])
const colors=COLORS;const icons=CAT_ICONS;const sl=statusLabel;const sb=statusBadge
const actId=computed(()=>{const last=MOCK_ACTIVITIES.find(x=>true);return last?.id||''})
// We receive activityId via a reactive approach - find the selected one
const a=computed(()=>{
// Get from the last navigation - we use a simple trick: find the activity that was clicked
// In real app this would be a prop or route param
const stored=sessionStorage.getItem('selectedActivity')
return stored?MOCK_ACTIVITIES.find(x=>x.id===stored):null
})
const creator=computed(()=>a.value?MOCK_USERS.find(u=>u.id===a.value!.creatorId):null)
const full=computed(()=>a.value?(a.value.registeredCount>=a.value.maxCount):false)
const pct=computed(()=>a.value?Math.min(100,Math.round(a.value.registeredCount/a.value.maxCount*100)):0)
const reg=computed(()=>a.value?MOCK_REGISTRATIONS.some(r=>r.userId===props.user.id&&r.activityId===a.value!.id&&['registered','checked_in','completed'].includes(r.status)):false)
function doReg(){
if(!a.value)return
MOCK_REGISTRATIONS.push({id:'r'+Date.now(),userId:props.user.id,activityId:a.value.id,status:'registered',registeredAt:today()})
a.value.registeredCount++
MOCK_NOTIFICATIONS.unshift({id:'n'+Date.now(),userId:props.user.id,title:'报名成功',content:`你已成功报名「${a.value.title}」`,time:new Date().toLocaleString('zh-CN'),read:false})
}
function cancelReg(){
if(!a.value)return
const r=MOCK_REGISTRATIONS.find(x=>x.userId===props.user.id&&x.activityId===a.value!.id&&x.status==='registered')
if(r){r.status='cancelled';a.value.registeredCount=Math.max(0,a.value.registeredCount-1)}
}
</script>
<style scoped>
.detail-header{display:flex;gap:24px;margin-bottom:24px}
.detail-img{width:320px;height:220px;border:2px solid var(--border);border-radius:var(--radius);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.detail-info{flex:1}
.detail-meta{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:16px}
.detail-meta-item{display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:.8rem;color:var(--ink-muted)}
.detail-actions{display:flex;gap:10px;flex-wrap:wrap}
@media(max-width:1024px){.detail-header{flex-direction:column}.detail-img{width:100%}}
</style>
