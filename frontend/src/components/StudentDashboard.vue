<template>
<div>
<div class="section-title mb-24">活动广场</div>
<div class="filter-bar">
<div class="search-input"><input type="text" placeholder="搜索活动名称、标签..." v-model="q"></div>
<button class="filter-chip" :class="{active:f===c}" v-for="c in cats" :key="c" @click="f=c">{{c}}</button>
</div>
<div v-if="loading" class="empty-state"><p>加载中...</p></div>
<div v-else-if="filtered.length===0" class="empty-state"><div class="empty-icon">📭</div><p>没有找到相关活动</p></div>
<div v-else class="grid-3">
<div class="activity-card" :class="'anim-in anim-in-'+(i%6)" v-for="(a,i) in filtered" :key="a.id" @click="$emit('viewActivity',a.id)">
<div class="activity-card-img" :style="{background:colors[i%colors.length]}">
<span class="placeholder-icon">{{icons[a.category]||'📌'}}</span>
<div class="activity-card-badges">
<span class="badge badge-blue">{{a.category}}</span>
<span class="badge badge-amber" v-if="a.hasBonus">🎖 可加分</span>
<span class="badge badge-purple" v-if="a.fee>0">¥{{a.fee}}</span>
<span class="badge badge-orange" v-if="a.registrationLimitType==='college'">🎓 限{{a.registrationLimitValue}}</span>
<span class="badge badge-orange" v-else-if="a.registrationLimitType==='club'">🏅 限{{a.registrationLimitValue}}</span>
</div>
</div>
<div class="activity-card-body">
<div class="activity-card-title">{{a.title}}</div>
<div class="activity-card-meta">
<span>🕐 {{a.startTime}}</span><span>📍 {{a.location}}</span><span>🏫 {{a.college}}</span>
</div>
</div>
<div class="activity-card-footer">
<div class="spots"><strong>{{a.registeredCount}}</strong> / {{a.maxCount}} 人已报名</div>
<span class="badge badge-red" v-if="a.registeredCount>=a.maxCount">已满</span>
<span class="badge badge-green" v-else-if="regIds.has(a.id)">已报名</span>
</div>
</div>
</div>
</div>
</template>
<script setup lang="ts">
import {ref,computed,onMounted} from 'vue'
import {activityApi,registrationApi} from '../services/api'
import {adaptActivity} from '../utils/adapters'
import {COLORS,CAT_ICONS} from '../mock/data'
defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const loading=ref(true)
const activities=ref<any[]>([])
const regIds=ref(new Set<string>())
const q=ref('');const f=ref('全部')
const cats=['全部','学术','文艺','体育','公益','社交','就业','讲座']
const colors=COLORS;const icons=CAT_ICONS
const filtered=computed(()=>{
let a=activities.value.filter(x=>x.status==='published'||x.status==='completed')
if(f.value!=='全部')a=a.filter(x=>x.category===f.value)
if(q.value){const s=q.value.toLowerCase();a=a.filter(x=>x.title.toLowerCase().includes(s)||x.tags.some((t:string)=>t.includes(s))||(x.college||'').includes(s))}
return a
})
onMounted(async()=>{
try{
const[actRes,regRes]=await Promise.all([activityApi.list(),registrationApi.myRegistrations()])
if(actRes.code===200)activities.value=(actRes.data||[]).map(adaptActivity)
if(regRes.code===200){regIds.value=new Set((regRes.data||[]).filter((r:any)=>['registered','checked_in','completed'].includes(r.status)).map((r:any)=>String(r.activityId)))}
}catch(e){console.error('load activities failed',e)}
finally{loading.value=false}
})
</script>
