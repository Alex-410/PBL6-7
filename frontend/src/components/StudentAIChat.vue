<template>
  <div class="ai-chat">
    <div class="chat-header">
      <div class="ai-icon">🤖</div>
      <h2>AI智能助手</h2>
      <p>选择一个模型开始对话</p>
    </div>

    <div class="model-selector">
      <label>选择AI模型:</label>
      <select v-model="selectedModel" class="model-select">
        <option value="doubao-seed-1-8-251228">豆包1.8 (doubao-seed-1-8-251228)</option>
        <option value="doubao-seed-2-0-lite-260428">豆包lite (doubao-seed-2-0-lite-260428)</option>
        <option value="deepseek-v3-2-251201">DeepSeek V3 (deepseek-v3-2-251201)</option>
        <option value="glm-4-7-251222">GLM-4 (glm-4-7-251222)</option>
      </select>
    </div>

    <div class="chat-container">
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          class="message"
          :class="msg.role"
        >
          <div class="message-avatar">
            {{ msg.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div class="message-text">{{ msg.content }}</div>
            <div class="message-time" v-if="msg.time">{{ msg.time }}</div>
          </div>
        </div>
        <div v-if="loading" class="message assistant">
          <div class="message-avatar">🤖</div>
          <div class="message-content">
            <div class="message-text loading">
              <span class="loading-dots">
                <span></span><span></span><span></span>
              </span>
              AI正在思考...
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <textarea 
          v-model="inputMessage" 
          placeholder="输入你想问的问题..."
          @keydown.enter.exact.prevent="sendMessage"
          :disabled="loading"
        ></textarea>
        <button @click="sendMessage" :disabled="loading || !inputMessage.trim()">
          发送
        </button>
      </div>
    </div>

    <div class="chat-actions">
      <button class="clear-btn" @click="clearChat">清空对话</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  time?: string
}

const AI_CONFIG = {
  baseURL: 'https://ark.cn-beijing.volces.com/api/v3',
  apiKey: 'ark-809c6b18-909a-4bb5-8fb8-3e2dd56584c0-c4e20'
}

const selectedModel = ref('doubao-seed-1-8-251228')
const inputMessage = ref('')
const messages = ref<ChatMessage[]>([])
const loading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const formatTime = () => {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  messages.value.push({
    role: 'user',
    content: userMessage,
    time: formatTime()
  })
  scrollToBottom()

  loading.value = true

  try {
    const conversationHistory = messages.value.map(m => ({
      role: m.role,
      content: m.content
    }))

    const response = await fetch(`${AI_CONFIG.baseURL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AI_CONFIG.apiKey}`
      },
      body: JSON.stringify({
        model: selectedModel.value,
        messages: conversationHistory,
        temperature: 0.7
      })
    })

    const data = await response.json()
    console.log('AI响应:', data)

    if (data.choices && data.choices[0]?.message?.content) {
      const aiContent = data.choices[0].message.content
      messages.value.push({
        role: 'assistant',
        content: aiContent,
        time: formatTime()
      })
    } else if (data.error) {
      messages.value.push({
        role: 'assistant',
        content: `错误: ${data.error.message || '未知错误'}`,
        time: formatTime()
      })
    } else {
      messages.value.push({
        role: 'assistant',
        content: '抱歉，我暂时无法回答这个问题，请稍后重试。',
        time: formatTime()
      })
    }
  } catch (e: any) {
    console.error('AI调用失败:', e)
    messages.value.push({
      role: 'assistant',
      content: `网络错误: ${e.message || '请检查网络连接'}`,
      time: formatTime()
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

const clearChat = () => {
  messages.value = []
}

onMounted(() => {
  messages.value.push({
    role: 'assistant',
    content: '你好！我是AI智能助手。你可以问我关于校园活动的问题，或者使用AI推荐功能发现感兴趣的活动。选择一个模型开始对话吧！',
    time: formatTime()
  })
})
</script>

<style scoped>
.ai-chat {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
}

.chat-header {
  text-align: center;
  margin-bottom: 20px;
}

.chat-header .ai-icon {
  font-size: 48px;
}

.chat-header h2 {
  font-size: 1.8rem;
  margin-bottom: 8px;
  color: var(--ink);
}

.chat-header p {
  color: var(--ink-muted);
}

.model-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: var(--surface-alt);
  border-radius: var(--radius);
}

.model-selector label {
  font-weight: 500;
  color: var(--ink);
}

.model-select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--ink);
  font-size: 0.9rem;
  cursor: pointer;
}

.model-select:focus {
  outline: none;
  border-color: var(--accent);
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  overflow: hidden;
  min-height: 400px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--surface-alt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message.assistant .message-avatar {
  background: linear-gradient(135deg, #667eea20, #764ba220);
}

.message-content {
  background: var(--surface-alt);
  padding: 12px 16px;
  border-radius: 12px;
  border-top-left-radius: 4px;
}

.message.user .message-content {
  background: var(--accent);
  color: white;
  border-top-left-radius: 12px;
  border-top-right-radius: 4px;
}

.message-text {
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-time {
  font-size: 0.7rem;
  color: var(--ink-muted);
  margin-top: 6px;
}

.message.user .message-time {
  color: rgba(255,255,255,0.7);
}

.loading-dots {
  display: inline-flex;
  gap: 4px;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: var(--ink-muted);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.loading-dots span:nth-child(1) { animation-delay: 0s; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--surface-alt);
  border-top: 1px solid var(--border-light);
}

.chat-input textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--ink);
  font-size: 0.95rem;
  resize: none;
  min-height: 44px;
  max-height: 120px;
  font-family: inherit;
}

.chat-input textarea:focus {
  outline: none;
  border-color: var(--accent);
}

.chat-input textarea::placeholder {
  color: var(--ink-muted);
}

.chat-input button {
  padding: 12px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-end;
}

.chat-input button:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-actions {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

.clear-btn {
  padding: 8px 20px;
  background: var(--surface-alt);
  color: var(--ink-muted);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: var(--border-light);
  color: var(--ink);
}

@media (max-width: 768px) {
  .ai-chat {
    height: calc(100vh - 140px);
  }
  
  .message {
    max-width: 95%;
  }
  
  .chat-input {
    flex-direction: column;
  }
  
  .chat-input button {
    width: 100%;
  }

  .model-selector {
    flex-direction: column;
    gap: 8px;
  }

  .model-select {
    width: 100%;
  }
}
</style>