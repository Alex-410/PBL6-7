<template>
<div>
<div class="flex justify-between items-center mb-24">
<div class="section-title">活动日历 · {{ currentYear }}年{{ currentMonth + 1 }}月</div>
<div class="flex gap-8">
<button class="btn btn-sm" @click="prevMonth">← 上月</button>
<button class="btn btn-sm" @click="goToday" :disabled="isCurrentMonth">今天</button>
<button class="btn btn-sm" @click="nextMonth">下月 →</button>
</div>
</div>
<div class="calendar-wrapper">
<div class="calendar-grid">
<div class="calendar-header-cell" v-for="d in dayNames" :key="d">{{ d }}</div>
<div class="calendar-cell calendar-cell-empty" v-for="i in firstDayOfMonth" :key="'e'+i"></div>
<div class="calendar-cell" :class="{ 'calendar-cell-today': d === todayDate && isCurrentMonth }" v-for="d in daysInMonth" :key="d" @click="onDayClick(d)">
<div class="day-num">{{ d }}</div>
<template v-if="getDayActivities(d).length">
<div class="calendar-events">
<div class="event-dot" v-for="act in getDayActivities(d).slice(0, 8)" :key="act.id" :style="{ background: getEventColor(act) }" :title="act.title"></div>
</div>
<div class="event-title" v-for="act in getDayActivities(d).slice(0, 2)" :key="'t'+act.id" @click.stop="$emit('viewActivity', act.id)">
{{ act.title.length > 8 ? act.title.slice(0, 8) + '…' : act.title }}
</div>
<div class="event-more" v-if="getDayActivities(d).length > 2" @click.stop="selectedDay=d">+{{ getDayActivities(d).length - 2 }} 更多</div>
</template>
</div>
</div>
</div>

<div v-if="selectedDay" class="modal-overlay" @click.self="selectedDay=null">
<div class="modal">
<div class="modal-header"><h3>{{ currentYear }}年{{ currentMonth + 1 }}月{{ selectedDay }}日 活动</h3><button class="btn btn-sm btn-ghost" @click="selectedDay=null">✕</button></div>
<div class="card-body" style="padding:0">
<div v-if="getDayActivities(selectedDay).length === 0" class="empty-state" style="padding:30px"><p>该日暂无活动</p></div>
<div v-for="act in getDayActivities(selectedDay)" :key="act.id" style="padding:14px 20px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;justify-content:space-between;cursor:pointer" @click="$emit('viewActivity', act.id);selectedDay=null">
<div>
<div style="font-weight:500;font-size:.88rem">{{ act.title }}</div>
<div class="mono text-xs text-muted">{{ act.startTime }} · {{ act.location }}</div>
</div>
<span class="badge badge-blue">{{ act.category }}</span>
</div>
</div>
<div class="modal-footer"><button class="btn btn-sm" @click="selectedDay=null">关闭</button></div>
</div>
</div>
</div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { activityApi } from '../services/api'
import { adaptActivity } from '../utils/adapters'

defineProps<{ user: any }>()
const emit = defineEmits(['viewActivity', 'navigate'])

const activities = ref<any[]>([])
const now = ref(new Date())
const currentYear = computed(() => now.value.getFullYear())
const currentMonth = computed(() => now.value.getMonth())
const todayDate = new Date().getDate()
const isCurrentMonth = computed(() => {
  const n = new Date()
  return n.getFullYear() === currentYear.value && n.getMonth() === currentMonth.value
})
const dayNames = ['日', '一', '二', '三', '四', '五', '六']
const firstDayOfMonth = computed(() => new Date(currentYear.value, currentMonth.value, 1).getDay())
const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())
const selectedDay = ref<number | null>(null)

const monthActivities = computed(() => {
  return activities.value.filter(a => {
    if (a.status !== 'published' && a.status !== 'completed') return false
    const d = new Date(a.startTime)
    return d.getFullYear() === currentYear.value && d.getMonth() === currentMonth.value
  })
})

function getDayActivities(day: number) {
  return monthActivities.value.filter(a => new Date(a.startTime).getDate() === day)
}

function getEventColor(act: any) {
  const idx = ['学术', '文艺', '体育', '公益', '社交', '就业', '讲座'].indexOf(act.category)
  const colors = ['#1E40AF', '#7E22CE', '#166534', '#B91C1C', '#A16207', '#1E40AF', '#7E22CE']
  return colors[idx >= 0 ? idx : 0]
}

function onDayClick(day: number) {
  if (getDayActivities(day).length > 0) {
    selectedDay.value = day
  }
}

function prevMonth() { now.value = new Date(currentYear.value, currentMonth.value - 1, 1) }
function nextMonth() { now.value = new Date(currentYear.value, currentMonth.value + 1, 1) }
function goToday() { now.value = new Date() }

onMounted(async () => {
  try {
    const res = await activityApi.list()
    if (res.code === 200) activities.value = (res.data || []).map(adaptActivity)
  } catch (e) { console.error('load activities failed', e) }
})
</script>
<style scoped>
.calendar-wrapper { border: 2px solid var(--border); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-sm); background: var(--surface); }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 1px; background: var(--border-light); }
.calendar-header-cell { padding: 10px 8px; text-align: center; font-family: var(--font-mono); font-size: .72rem; font-weight: 500; color: var(--ink-muted); text-transform: uppercase; background: var(--surface-alt); }
.calendar-cell { min-height: 90px; padding: 6px 8px; background: var(--surface); font-family: var(--font-mono); font-size: .72rem; position: relative; cursor: pointer; transition: background .1s; }
.calendar-cell:hover { background: #FAF8F5; }
.calendar-cell-empty { background: var(--surface-alt); cursor: default; }
.calendar-cell-empty:hover { background: var(--surface-alt); }
.calendar-cell-today { background: var(--amber-bg); }
.calendar-cell-today:hover { background: #FFF8E7; }
.day-num { font-weight: 500; margin-bottom: 2px; font-size: .78rem; }
.calendar-events { display: flex; flex-wrap: wrap; gap: 2px; margin: 2px 0; }
.event-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.event-title { font-size: .65rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-top: 2px; cursor: pointer; color: var(--ink); line-height: 1.4; }
.event-title:hover { color: var(--accent); }
.event-more { font-size: .6rem; color: var(--ink-muted); cursor: pointer; margin-top: 2px; }
.event-more:hover { color: var(--accent); }
</style>
