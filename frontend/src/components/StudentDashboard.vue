<template>
<div>
<div class="section-title mb-24">活动广场</div>
<div class="filter-bar">
<div class="search-input"><input type="text" placeholder="搜索活动名称、标签..." v-model="q"></div>
<button class="filter-chip" :class="{active:f===c}" v-for="c in cats" :key="c" @click="f=c">{{c}}</button>
</div>
<div v-if="filtered.length===0" class="empty-state"><div class="empty-icon">📭</div><p>没有找到相关活动</p></div>
<div v-else class="grid-3">
<div class="activity-card" :class="'anim-in anim-in-'+(i%6)" v-for="(a,i) in filtered" :key="a.id" @click="$emit('viewActivity',a.id)">
<div class="activity-card-img" :style="{background:colors[Number(a.id.replace('a',''))%colors.length]}">
<span class="placeholder-icon">{{icons[a.category]||'📌'}}</span>
<div class="activity-card-badges">
<span class="badge badge-blue">{{a.category}}</span>
<span class="badge badge-amber" v-if="a.hasBonus">🎖 可加分</span>
<span class="badge badge-purple" v-if="a.fee>0">¥{{a.fee}}</span>
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
<span class="badge badge-green" v-else-if="isReg(a.id)">已报名</span>
</div>
</div>
</div>
</div>
</template>
<script setup lang="ts">
import {ref,computed} from 'vue'
import {MOCK_ACTIVITIES,MOCK_REGISTRATIONS,COLORS,CAT_ICONS} from '../mock/data'
const props=defineProps<{user:any}>()
defineEmits(['viewActivity','navigate'])
const q=ref('');const f=ref('全部')
const cats=['全部','学术','文艺','体育','公益','社交','就业','讲座']
const colors=COLORS;const icons=CAT_ICONS
const filtered=computed(()=>{
let a=MOCK_ACTIVITIES.filter(x=>x.status==='published'||x.status==='completed')
if(f.value!=='全部')a=a.filter(x=>x.category===f.value)
if(q.value){const s=q.value.toLowerCase();a=a.filter(x=>x.title.toLowerCase().includes(s)||x.tags.some(t=>t.includes(s))||x.college.includes(s))}
return a
})
function isReg(id:string){return MOCK_REGISTRATIONS.some(r=>r.userId===props.user.id&&r.activityId===id&&['registered','checked_in','completed'].includes(r.status))}
</script>
