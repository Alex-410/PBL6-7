<template>
<div>
<button class="btn btn-ghost mb-16" @click="$emit('navigate','dashboard')">← 返回</button>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="!a" class="empty-state"><p>活动未找到</p></div>
<template v-else>
<div class="detail-header">
<div class="detail-img" :style="{background:colors[Number(a.id)%colors.length]}">
<span style="font-size:5rem;opacity:.3">{{icons[a.category]||'📌'}}</span>
</div>
<div class="detail-info">
<div class="flex gap-8 mb-8" style="flex-wrap:wrap">
<span class="badge badge-blue">{{a.category}}</span>
<span class="badge" :class="sb(a.status)">{{sl(a.status)}}</span>
<span class="badge badge-amber" v-if="a.hasBonus">🎖 {{a.bonusType}} +{{a.bonusValue}}</span>
<span class="badge badge-purple" v-if="a.fee>0">¥{{a.fee}}</span>
<span class="badge badge-orange" v-if="a.registrationLimitType==='college'">🎓 限{{a.registrationLimitValue}}报名</span>
<span class="badge badge-orange" v-else-if="a.registrationLimitType==='club'">🏅 限{{a.registrationLimitValue}}报名</span>
</div>
<h1 style="font-family:var(--font-display);font-size:2rem;margin-bottom:8px">{{a.title}}</h1>
<div class="detail-meta">
<span class="detail-meta-item">🏫 {{a.college}}</span>
</div>
<div class="detail-meta">
<span class="detail-meta-item">🕐 {{a.startTime}} ~ {{a.endTime}}</span>
<span class="detail-meta-item">📍 {{a.location}}</span>
<span class="detail-meta-item">👥 {{a.registeredCount}} / {{a.maxCount}} 人</span>
</div>
<div style="margin:12px 0"><div class="progress-bar" style="height:6px"><div class="progress-bar-fill" :style="{width:pct+'%',...(full?{background:'var(--accent)'}:{})}"></div></div></div>
<div v-if="user.role==='student'" class="detail-actions">
<span v-if="a.status==='completed'" class="badge badge-gray">活动已结束</span>
<span v-else-if="full&&!isReg" class="badge badge-red">报名已满</span>
<button v-else-if="isReg" class="btn btn-accent" @click="cancelReg">取消报名</button>
<button v-else class="btn btn-primary" @click="doReg">立即报名</button>
</div>
<div v-if="errMsg" style="margin-top:12px;padding:10px 14px;border-radius:var(--radius);font-size:.82rem;background:var(--accent-bg);color:var(--accent);display:flex;align-items:center;gap:8px">
<span>⚠️ {{errMsg}}</span>
<button class="btn btn-sm btn-ghost" style="margin-left:auto" @click="errMsg=''">✕</button>
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
<div class="flex items-center gap-12 mb-16"><div class="avatar avatar-lg">👤</div><div>
<div style="font-weight:500;font-size:1rem">{{a.organizer}}</div>
<div class="mono text-sm text-muted">{{a.college}}</div>
</div></div>
</div></div></div>
</div>
</template>
</div>
</template>
<script setup lang="ts">
import {ref,computed,onMounted} from 'vue'
import {activityApi,registrationApi} from '../services/api'
import {adaptActivity} from '../utils/adapters'
import {COLORS,CAT_ICONS,statusLabel,statusBadge} from '../mock/data'
defineProps<{user:any}>()
const emit=defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activity=ref<any>(null)
const regId=ref<string|null>(null)
const errMsg=ref('')
const colors=COLORS;const icons=CAT_ICONS;const sl=statusLabel;const sb=statusBadge
const a=computed(()=>activity.value)
const full=computed(()=>a.value?(a.value.registeredCount>=a.value.maxCount):false)
const pct=computed(()=>a.value&&a.value.maxCount>0?Math.min(100,Math.round(a.value.registeredCount/a.value.maxCount*100)):0)
const isReg=computed(()=>regId.value!==null)
async function load(){
const actId=sessionStorage.getItem('selectedActivity')
if(!actId){loading.value=false;return}
try{
const[actRes,regRes]=await Promise.all([activityApi.detail(Number(actId)),registrationApi.myRegistrations()])
if(actRes.code===200&&actRes.data){activity.value=adaptActivity(actRes.data)}
if(regRes.code===200){
const match=(regRes.data||[]).find((r:any)=>String(r.activityId)===actId&&['registered','checked_in','completed'].includes(r.status))
regId.value=match?String(match.id):null
}
}catch(e){console.error('load detail failed',e)}
finally{loading.value=false}
}
async function doReg(){
if(!a.value)return
errMsg.value=''
try{
const res=await registrationApi.register(Number(a.value.id))
if(res.code===200){await load()}
else{errMsg.value=res.message||'报名失败'}
}catch(e:any){errMsg.value=e?.response?.data?.message||'报名失败，请重试'}
}
async function cancelReg(){
if(!regId.value)return
try{
const res=await registrationApi.cancel(Number(regId.value))
if(res.code===200){await load()}
}catch(e){console.error('cancel failed',e)}
}
onMounted(load)
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
