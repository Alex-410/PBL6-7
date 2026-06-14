<template>
  <div class="ai-recommend">
    <div class="ai-header">
      <div class="ai-icon">🤖</div>
      <h2>AI智能推荐</h2>
      <p>基于你的兴趣和活动余量，AI为你推荐以下活动</p>
    </div>

    <div class="loading-state" v-if="loading">
      <div class="loading-spinner"></div>
      <p>AI正在分析活动，生成推荐中...</p>
    </div>

    <div class="error-state" v-else-if="error">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="fetchAIRecommend">重试</button>
    </div>

    <div class="recommend-result" v-else-if="recommendations.length > 0">
      <div 
        v-for="item in recommendations"
        :key="item.activity.id" 
        class="activity-card"
        @click="viewActivity(item.activity.id)"
      >
        <div class="activity-poster">
          <img v-if="item.activity.poster" :src="item.activity.poster" :alt="item.activity.title">
          <div v-else class="poster-placeholder">📋</div>
          <div class="credit-badge" v-if="item.activity.has_bonus">可加分</div>
        </div>
        <div class="activity-info">
          <h3>{{ item.activity.title }}</h3>
          <div class="activity-meta">
            <span>📅 {{ formatDate(item.activity.start_time) }}</span>
            <span>📍 {{ item.activity.location }}</span>
          </div>
          <div class="activity-stats">
            <span>剩余名额: {{ item.activity.max_count - item.activity.registered_count }}/{{ item.activity.max_count }}</span>
          </div>
          <div class="ai-reason">
            <span class="ai-tag">🤖 AI推荐理由:</span>
            <p>{{ item.reason }}</p>
          </div>
          <button 
            class="register-btn" 
            :disabled="item.activity.registered"
            @click.stop="registerActivity(item.activity.id)"
          >
            {{ item.activity.registered ? '已报名' : '立即报名' }}
          </button>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon">📭</div>
      <p>暂无推荐活动</p>
      <p class="empty-hint">当前没有符合条件的活动可以推荐</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { activityApi, registrationApi, aiApi } from '../services/api'

interface Activity {
  id: number
  title: string
  description: string
  poster: string
  start_time: string
  end_time: string
  location: string
  organizer: string
  max_count: number
  registered_count: number
  has_bonus: boolean
  bonus_type: string
  bonus_value: number
  status: string
  registered?: boolean
}

interface RecommendItem {
  activity: Activity
  reason: string
}

const emit = defineEmits(['viewActivity'])

const loading = ref(false)
const error = ref('')
const recommendations = ref<RecommendItem[]>([])
const activities = ref<Activity[]>([])

const RECOMMEND_MODEL = 'doubao-seed-2-0-code-preview-260215'

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { 
    month: '2-digit', 
    day: '2-digit', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const fetchActivities = async () => {
  try {
    const res = await activityApi.list('published')
    console.log('API返回数据:', res)
    if (res.code === 200 && res.data) {
      console.log('第一个活动的字段:', Object.keys(res.data[0] || {}))
      activities.value = res.data
        .map((a: any) => ({ 
          ...a, 
          registered: false,
          max_count: a.maxCount || a.max_count || 0,
          registered_count: a.registeredCount || a.registered_count || 0
        }))
      console.log('筛选后活动数:', activities.value.length, activities.value[0])
    }
  } catch (e) {
    console.error('获取活动失败:', e)
  }
}

const fetchAIRecommend = async () => {
  loading.value = true
  error.value = ''
  
  try {
    if (activities.value.length === 0) {
      await fetchActivities()
    }

    if (activities.value.length === 0) {
      error.value = '暂无可推荐的活动'
      loading.value = false
      return
    }

    const activitiesInfo = activities.value.slice(0, 10).map(a => ({
      id: a.id,
      title: a.title,
      category: a.description?.substring(0, 50) || '',
      has_bonus: a.has_bonus,
      bonus_type: a.bonus_type,
      remaining: a.max_count - a.registered_count
    }))

    const prompt = `你是一个校园活动推荐助手。请从以下活动中随机选择1-3个推荐给用户，并为每个活动生成一句简洁的推荐理由（50字以内）。
    
活动列表：
${activitiesInfo.map((a: any, i: number) => `${i+1}. ${a.title} - ${a.category} ${a.has_bonus ? '(可加分:'+a.bonus_type+')' : ''} 剩余名额:${a.remaining}`).join('\n')}

请按以下JSON格式返回推荐结果：
{"recommendations":[{"activity_id":活动ID,"reason":"推荐理由"},{"activity_id":活动ID,"reason":"推荐理由"}]}`

    const res: any = await aiApi.chat({
      model: RECOMMEND_MODEL,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7
    })
    // 响应拦截器已 unwrap，res 即后端 Result envelope；res.data 为上游 Ark 响应体
    const data = res.data
    console.log('AI API返回数据:', data)

    if (data && data.choices && data.choices[0]?.message?.content) {
      const content = data.choices[0].message.content
      console.log('AI返回内容:', content)
      const match = content.match(/\{[\s\S]*\}/)
      if (match) {
        const result = JSON.parse(match[0])
        console.log('解析后的JSON:', result)
        if (result.recommendations && Array.isArray(result.recommendations)) {
          recommendations.value = result.recommendations.map((r: any) => {
            const activity = activities.value.find((a: Activity) => a.id === r.activity_id)
            return {
              activity: activity || activities.value[0],
              reason: r.reason
            }
          }).filter((item: RecommendItem) => item.activity)
        }
      }
    }

    if (recommendations.value.length === 0) {
      recommendations.value = activities.value.slice(0, 3).map((a: Activity) => ({
        activity: a,
        reason: '这是一个值得参与的活动，快来报名吧！'
      }))
    }
  } catch (e: any) {
    console.error('AI推荐失败:', e)
    error.value = 'AI推荐服务暂时不可用，请稍后重试'
    
    recommendations.value = activities.value.slice(0, 3).map((a: Activity) => ({
      activity: a,
      reason: '这是一个值得参与的活动，快来报名吧！'
    }))
  } finally {
    loading.value = false
  }
}

const viewActivity = (id: number) => {
  emit('viewActivity', id)
}

const registerActivity = async (activityId: number) => {
  try {
    const res = await registrationApi.register(activityId)
    if (res.code === 200) {
      alert('报名成功！')
      const item = recommendations.value.find(r => r.activity.id === activityId)
      if (item) {
        item.activity.registered = true
      }
    } else {
      alert(res.message || '报名失败')
    }
  } catch (e: any) {
    alert(e.response?.data?.message || '报名失败')
  }
}

onMounted(() => {
  fetchAIRecommend()
})
</script>

<style scoped>
.ai-recommend {
  max-width: 900px;
  margin: 0 auto;
}

.ai-header {
  text-align: center;
  margin-bottom: 32px;
}

.ai-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.ai-header h2 {
  font-size: 1.8rem;
  margin-bottom: 8px;
  color: var(--ink);
}

.ai-header p {
  color: var(--ink-muted);
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-light);
  border-top-color: var(--accent);
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 40px 20px;
  background: var(--surface-alt);
  border-radius: var(--radius);
}

.error-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
}

.recommend-result {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.activity-card {
  display: flex;
  gap: 20px;
  background: var(--surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.activity-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.activity-poster {
  width: 200px;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  position: relative;
  background: var(--surface-alt);
}

.activity-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
}

.credit-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--success);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
}

.activity-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-info h3 {
  font-size: 1.2rem;
  margin-bottom: 8px;
}

.activity-meta {
  display: flex;
  gap: 16px;
  color: var(--ink-muted);
  font-size: 0.875rem;
  margin-bottom: 8px;
}

.activity-stats {
  font-size: 0.875rem;
  color: var(--ink-muted);
  margin-bottom: 12px;
}

.ai-reason {
  background: linear-gradient(135deg, #667eea10, #764ba210);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.ai-tag {
  font-weight: 600;
  color: #667eea;
  font-size: 0.875rem;
}

.ai-reason p {
  margin: 4px 0 0;
  color: var(--ink);
  font-size: 0.9rem;
}

.register-btn {
  align-self: flex-start;
  padding: 8px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-weight: 500;
}

.register-btn:disabled {
  background: var(--border);
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-hint {
  color: var(--ink-muted);
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .activity-card {
    flex-direction: column;
  }
  
  .activity-poster {
    width: 100%;
    height: 180px;
  }

  .ai-header h2 {
    font-size: 1.4rem;
  }

  .activity-meta {
    flex-direction: column;
    gap: 4px;
  }
}
</style>