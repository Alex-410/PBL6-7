<template>
  <div class="rag-page">
    <!-- Header -->
    <div class="rag-header">
      <router-link to="/" class="back-btn">&larr; 返回首页</router-link>
      <div class="header-center">
        <h1>校规知识库</h1>
        <p class="subtitle">基于 RAG 的智能校规问答系统</p>
      </div>
      <div class="header-actions">
        <button class="action-btn" @click="showKbModal = true" title="知识库">
          知识库 <span class="badge" v-if="status.doc_count">{{ status.doc_count }}</span>
        </button>
        <button class="action-btn primary" @click="showUploadModal = true" title="上传文档">
          上传文档
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Conversations Sidebar -->
      <div class="conversations-sidebar">
        <button class="new-chat-btn" @click="createNewConversation">
          + 新建对话
        </button>
        <div class="conv-list">
          <div
            v-for="conv in conversations"
            :key="conv.id"
            class="conv-item"
            :class="{ active: conv.id === conversationId }"
            @click="switchConversation(conv.id)"
          >
            <span class="conv-title">{{ conv.title }}</span>
            <span class="conv-count">{{ conv.msg_count }} 条</span>
            <button class="conv-delete" @click.stop="deleteConversation(conv.id)" title="删除对话">×</button>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="chat-container">
      <div class="chat-messages" ref="messagesContainer">
        <!-- Welcome -->
        <div v-if="messages.length === 0" class="welcome">
          <div class="welcome-icon">📖</div>
          <h2>欢迎使用校规知识库</h2>
          <p>我可以回答关于学校规章制度的问题，试试下面的问题：</p>
          <div class="suggestions">
            <button v-for="q in suggestions" :key="q" @click="askSuggestion(q)">{{ q }}</button>
          </div>
        </div>

        <!-- Messages -->
        <div v-for="(msg, index) in messages" :key="index" class="message" :class="msg.role">
          <div class="msg-avatar">{{ msg.role === 'user' ? '👤' : '📖' }}</div>
          <div class="msg-body">
            <div class="msg-header">
              <div v-if="msg.role === 'assistant'" class="msg-bubble markdown-body" v-html="renderMarkdown(msg.content)"></div>
              <div v-else class="msg-bubble">{{ msg.content }}</div>
              <button class="msg-delete" @click="deleteMessage(index)" title="删除此消息">×</button>
            </div>
            <!-- RAG/LLM indicator -->
            <div v-if="msg.role === 'assistant'" class="msg-source">
              <span v-if="msg.isRulesRelated === true" class="source-badge rag">校规知识库</span>
              <span v-else-if="msg.isRulesRelated === false" class="source-badge llm">AI 直答</span>
            </div>
            <!-- Retrieved Chunks -->
            <div v-if="msg.role === 'assistant' && msg.retrieved?.length" class="retrieved">
              <button class="retrieved-toggle" @click="msg.showRetrieved = !msg.showRetrieved">
                检索结果 ({{ msg.retrieved.length }})
                <span :class="{ rotated: msg.showRetrieved }">▼</span>
              </button>
              <div v-if="msg.showRetrieved" class="retrieved-list">
                <div v-for="(chunk, ci) in msg.retrieved" :key="ci" class="retrieved-item">
                  <div class="chunk-header">
                    <span class="chunk-file">{{ chunk.filename }}</span>
                    <span class="chunk-score">相似度: {{ (1 - chunk.score).toFixed(2) }}</span>
                  </div>
                  <div class="chunk-content">{{ chunk.content }}</div>
                </div>
              </div>
            </div>
            <div class="msg-time">{{ msg.time }}</div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="message assistant">
          <div class="msg-avatar">📖</div>
          <div class="msg-body">
            <div class="msg-bubble loading">
              <span class="loading-dots"><span></span><span></span><span></span></span>
              正在检索校规文档并生成回答...
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input">
        <textarea
          v-model="question"
          placeholder="输入关于校规的问题..."
          @keydown.enter.exact.prevent="sendQuestion"
          :disabled="loading"
        ></textarea>
        <button @click="sendQuestion" :disabled="loading || !question.trim()">
          {{ loading ? '回答中...' : '发送' }}
        </button>
      </div>
    </div>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="modal-overlay" @click.self="showUploadModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>上传校规文档</h3>
          <button class="close-btn" @click="showUploadModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <!-- Mode Tabs -->
          <div class="tabs">
            <button :class="{ active: uploadMode === 'file' }" @click="uploadMode = 'file'">文件上传</button>
            <button :class="{ active: uploadMode === 'text' }" @click="uploadMode = 'text'">文本粘贴</button>
          </div>

          <!-- File Upload -->
          <div v-if="uploadMode === 'file'" class="upload-area">
            <label class="file-label">
              <input type="file" accept=".txt,.md,.pdf,.docx" @change="onFileChange" hidden />
              <span class="file-btn">选择文件</span>
              <span class="file-name">{{ selectedFile?.name || '支持 TXT / MD / PDF / DOCX' }}</span>
            </label>
          </div>

          <!-- Text Paste -->
          <div v-if="uploadMode === 'text'" class="upload-area">
            <textarea v-model="textInput" placeholder="粘贴校规文本内容..." rows="8"></textarea>
            <input v-model="textFilename" placeholder="文档名称（如：XX大学学生手册）" class="filename-input" />
          </div>

          <!-- Chunking Config -->
          <div class="chunk-config">
            <div class="config-row">
              <label>切片策略</label>
              <select v-model="chunkStrategy">
                <option value="fixed">固定长度</option>
                <option value="recursive">递归分割</option>
                <option value="parent">结构化分割</option>
              </select>
            </div>
            <div class="config-row">
              <label>切片大小</label>
              <input type="number" v-model.number="chunkSize" min="100" max="2000" />
            </div>
            <div class="config-row">
              <label>重叠长度</label>
              <input type="number" v-model.number="overlap" min="0" max="500" />
            </div>
          </div>

          <!-- Parse Button -->
          <button
            class="parse-btn"
            @click="parseDocument"
            :disabled="parsing || (!selectedFile && !textInput.trim())"
          >
            {{ parsing ? '解析中...' : '解析并预览切片' }}
          </button>

          <!-- Preview Chunks -->
          <div v-if="previewChunks.length" class="preview">
            <div class="preview-header">
              <span>预览切片 ({{ previewChunks.filter(c => c.selected).length }}/{{ previewChunks.length }})</span>
              <div>
                <button @click="previewChunks.forEach(c => c.selected = true)">全选</button>
                <button @click="previewChunks.forEach(c => c.selected = false)">全不选</button>
              </div>
            </div>
            <div class="preview-list">
              <div v-for="chunk in previewChunks" :key="chunk.index" class="preview-item">
                <label>
                  <input type="checkbox" v-model="chunk.selected" />
                  <span class="preview-idx">#{{ chunk.index + 1 }}</span>
                  <span class="preview-text">{{ chunk.content.slice(0, 100) }}...</span>
                </label>
              </div>
            </div>
            <button
              class="save-btn"
              @click="saveChunks"
              :disabled="saving || previewChunks.filter(c => c.selected).length === 0"
            >
              {{ saving ? '保存中...' : `保存 (${previewChunks.filter(c => c.selected).length} 个切片)` }}
            </button>
            <p v-if="saveSuccess" class="success-msg">保存成功！</p>
          </div>

          <p v-if="uploadError" class="error-msg">{{ uploadError }}</p>
        </div>
      </div>
    </div>

    <!-- KB Status Modal -->
    <div v-if="showKbModal" class="modal-overlay" @click.self="showKbModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>知识库管理</h3>
          <button class="close-btn" @click="showKbModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="kb-stats">
            <div class="stat-card">
              <div class="stat-value">{{ status.doc_count || 0 }}</div>
              <div class="stat-label">总切片数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ status.docs?.length || 0 }}</div>
              <div class="stat-label">文档数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ status.embedding_model || '-' }}</div>
              <div class="stat-label">嵌入模型</div>
            </div>
          </div>

          <div v-if="status.docs?.length" class="doc-list">
            <div v-for="doc in status.docs" :key="doc.filename" class="doc-item">
              <div class="doc-info">
                <span class="doc-name">{{ doc.filename }}</span>
                <span class="doc-count">{{ doc.count }} 个切片</span>
              </div>
              <button class="delete-btn" @click="deleteDoc(doc.filename)" title="删除">删除</button>
            </div>
          </div>
          <p v-else class="empty-msg">知识库为空，请上传文档。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, reactive } from 'vue'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  breaks: true
})

const RAG_API = 'http://localhost:9001'

interface RetrievedChunk {
  content: string
  filename: string
  score: number
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  time?: string
  retrieved?: RetrievedChunk[]
  showRetrieved?: boolean
  isRulesRelated?: boolean
}

// Chat state
const question = ref('')
const messages = ref<Message[]>([])
const loading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const conversationId = ref('')
const conversations = ref<any[]>([])

// Status
const status = reactive<any>({
  has_index: false,
  doc_count: 0,
  docs: [],
  embedding_model: ''
})

// Upload state
const showUploadModal = ref(false)
const uploadMode = ref<'file' | 'text'>('file')
const selectedFile = ref<File | null>(null)
const textInput = ref('')
const textFilename = ref('')
const chunkStrategy = ref('fixed')
const chunkSize = ref(500)
const overlap = ref(50)
const parsing = ref(false)
const previewChunks = ref<any[]>([])
const saving = ref(false)
const saveSuccess = ref(false)
const uploadError = ref('')
const uploadFilename = ref('')

// KB state
const showKbModal = ref(false)

const suggestions = [
  '考试作弊会有什么处分？',
  '宿舍管理有哪些规定？',
  '如何申请奖学金？',
  '学生有哪些权利和义务？',
  '图书馆借阅规则是什么？',
  '转专业需要什么条件？'
]

const formatTime = () => {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const renderMarkdown = (text: string) => {
  if (!text) return ''
  return md.render(text)
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const loadStatus = async () => {
  try {
    const res = await fetch(`${RAG_API}/api/rag/status/`)
    const data = await res.json()
    Object.assign(status, data)
  } catch (e) {
    console.error('Failed to load status:', e)
  }
}

const loadConversations = async () => {
  try {
    const res = await fetch(`${RAG_API}/api/rag/conversations/`)
    const data = await res.json()
    conversations.value = data || []
    if (data.length > 0 && !conversationId.value) {
      await switchConversation(data[0].id)
    }
  } catch (e) {
    console.error('Failed to load conversations:', e)
  }
}

const switchConversation = async (convId: string) => {
  conversationId.value = convId
  try {
    const msgRes = await fetch(`${RAG_API}/api/rag/conversations/${convId}/messages/`)
    const msgData = await msgRes.json()
    messages.value = (msgData.messages || []).map((m: any) => ({
      ...m,
      time: m.time || '',
      showRetrieved: false,
      isRulesRelated: m.is_rules_related
    }))
  } catch (e) {
    console.error('Failed to load messages:', e)
    messages.value = []
  }
}

const createNewConversation = async () => {
  try {
    const res = await fetch(`${RAG_API}/api/rag/conversations/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: '新对话' })
    })
    const data = await res.json()
    conversations.value.unshift(data)
    await switchConversation(data.id)
  } catch (e) {
    console.error('Failed to create conversation:', e)
  }
}

const deleteConversation = async (convId: string) => {
  if (!confirm('确定删除这个对话？')) return
  try {
    const res = await fetch(`${RAG_API}/api/rag/conversations/delete/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: convId })
    })
    const data = await res.json()
    if (data.success) {
      conversations.value = conversations.value.filter(c => c.id !== convId)
      if (conversationId.value === convId) {
        if (conversations.value.length > 0) {
          await switchConversation(conversations.value[0].id)
        } else {
          conversationId.value = ''
          messages.value = []
        }
      }
    }
  } catch (e) {
    console.error('Failed to delete conversation:', e)
  }
}

const deleteMessage = async (msgIndex: number) => {
  if (!confirm('确定删除这条消息及其回复？')) return
  try {
    const res = await fetch(`${RAG_API}/api/rag/conversations/delete_message/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        conversation_id: conversationId.value,
        index: msgIndex
      })
    })
    const data = await res.json()
    if (data.success) {
      messages.value = (data.messages || []).map((m: any) => ({
        ...m,
        time: m.time || '',
        showRetrieved: false,
        isRulesRelated: m.is_rules_related
      }))
      loadConversations()
    }
  } catch (e) {
    console.error('Failed to delete message:', e)
  }
}

const sendQuestion = async () => {
  if (!question.value.trim() || loading.value) return

  const q = question.value.trim()
  question.value = ''

  messages.value.push({
    role: 'user',
    content: q,
    time: formatTime()
  })
  scrollToBottom()

  loading.value = true

  try {
    const res = await fetch(`${RAG_API}/api/rag/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question: q,
        conversation_id: conversationId.value,
        selected_docs: []
      })
    })

    const data = await res.json()

    if (data.error) {
      messages.value.push({
        role: 'assistant',
        content: `错误: ${data.error}`,
        time: formatTime()
      })
    } else {
      conversationId.value = data.conversation_id || conversationId.value
      messages.value.push({
        role: 'assistant',
        content: data.answer,
        time: formatTime(),
        retrieved: data.retrieved_chunks || [],
        showRetrieved: false,
        isRulesRelated: data.is_rules_related
      })
      loadConversations()
    }
  } catch (e: any) {
    messages.value.push({
      role: 'assistant',
      content: `网络错误: ${e.message || '请检查 RAG 服务是否启动'}`,
      time: formatTime()
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

const askSuggestion = (q: string) => {
  question.value = q
  sendQuestion()
}

// Upload functions
const onFileChange = (e: Event) => {
  const input = e.target as HTMLInputElement
  selectedFile.value = input.files?.[0] || null
}

const parseDocument = async () => {
  parsing.value = true
  uploadError.value = ''
  previewChunks.value = []
  saveSuccess.value = false

  try {
    let res: Response

    if (uploadMode.value === 'file' && selectedFile.value) {
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      formData.append('strategy', chunkStrategy.value)
      formData.append('chunk_size', String(chunkSize.value))
      formData.append('overlap', String(overlap.value))

      res = await fetch(`${RAG_API}/api/rag/upload/`, {
        method: 'POST',
        body: formData
      })
    } else if (uploadMode.value === 'text' && textInput.value.trim()) {
      res = await fetch(`${RAG_API}/api/rag/upload_text/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: textInput.value,
          filename: textFilename.value || '手动输入.txt',
          strategy: chunkStrategy.value,
          chunk_size: chunkSize.value,
          overlap: overlap.value
        })
      })
    } else {
      uploadError.value = '请选择文件或输入文本'
      return
    }

    const data = await res.json()
    if (data.error) {
      uploadError.value = data.error
    } else {
      previewChunks.value = data.chunks || []
      uploadFilename.value = data.filename || ''
    }
  } catch (e: any) {
    uploadError.value = `请求失败: ${e.message}`
  } finally {
    parsing.value = false
  }
}

const saveChunks = async () => {
  saving.value = true
  saveSuccess.value = false
  uploadError.value = ''

  try {
    const selected = previewChunks.value.filter(c => c.selected).map(c => c.content)
    const res = await fetch(`${RAG_API}/api/rag/save/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: uploadFilename.value,
        strategy: chunkStrategy.value,
        selected_chunks: selected
      })
    })

    const data = await res.json()
    if (data.error) {
      uploadError.value = data.error
    } else {
      saveSuccess.value = true
      previewChunks.value = []
      selectedFile.value = null
      textInput.value = ''
      loadStatus()
    }
  } catch (e: any) {
    uploadError.value = `保存失败: ${e.message}`
  } finally {
    saving.value = false
  }
}

const deleteDoc = async (filename: string) => {
  if (!confirm(`确定删除文档 "${filename}" 及其所有切片？`)) return

  try {
    const res = await fetch(`${RAG_API}/api/rag/delete/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename })
    })
    const data = await res.json()
    if (data.success) {
      loadStatus()
    }
  } catch (e) {
    console.error('Delete failed:', e)
  }
}

onMounted(() => {
  loadStatus()
  loadConversations()
})
</script>

<style scoped>
.rag-page {
  min-height: 100vh;
  background: var(--bg, #F5F1EB);
  display: flex;
  flex-direction: column;
  font-family: var(--font-body, 'Noto Serif SC', Georgia, serif);
}

/* Header */
.rag-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: var(--surface, #fff);
  border-bottom: 1px solid var(--border-light, #e8e0d6);
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-btn {
  color: var(--ink-muted, #888);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: var(--ink, #2D2A26);
}

.header-center h1 {
  font-family: var(--font-display, 'Noto Serif SC', serif);
  font-size: 1.5rem;
  color: var(--ink, #2D2A26);
  margin: 0;
}

.subtitle {
  color: var(--ink-muted, #888);
  font-size: 0.8rem;
  margin: 2px 0 0;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  background: var(--surface-alt, #f0ebe4);
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  color: var(--ink, #2D2A26);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn:hover {
  background: var(--border-light, #e8e0d6);
}

.action-btn.primary {
  background: var(--accent, #6B4C3B);
  color: white;
  border-color: var(--accent, #6B4C3B);
}

.action-btn.primary:hover {
  opacity: 0.9;
}

.badge {
  background: var(--accent, #6B4C3B);
  color: white;
  font-size: 0.7rem;
  padding: 1px 6px;
  border-radius: 10px;
}

/* Main Content Layout */
.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* Conversations Sidebar */
.conversations-sidebar {
  width: 260px;
  background: var(--surface, #fff);
  border-right: 1px solid var(--border-light, #e8e0d6);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.new-chat-btn {
  margin: 16px;
  padding: 10px 16px;
  background: var(--accent, #6B4C3B);
  color: white;
  border: none;
  border-radius: var(--radius, 6px);
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.new-chat-btn:hover {
  opacity: 0.9;
}

.conv-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px 16px;
}

.conv-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: var(--radius, 6px);
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
}

.conv-item:hover {
  background: var(--surface-alt, #f0ebe4);
}

.conv-item.active {
  background: var(--surface-alt, #f0ebe4);
  border-left: 3px solid var(--accent, #6B4C3B);
}

.conv-title {
  flex: 1;
  font-size: 0.85rem;
  color: var(--ink, #2D2A26);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-count {
  font-size: 0.7rem;
  color: var(--ink-muted, #888);
  margin-left: 8px;
}

.conv-delete {
  opacity: 0;
  background: none;
  border: none;
  color: var(--ink-muted, #888);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 4px;
  transition: all 0.2s;
}

.conv-item:hover .conv-delete {
  opacity: 1;
}

.conv-delete:hover {
  color: #c0392b;
}

/* Chat Container */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
  padding: 0 16px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 400px;
}

/* Welcome */
.welcome {
  text-align: center;
  padding: 60px 20px;
}

.welcome-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.welcome h2 {
  font-family: var(--font-display, 'Noto Serif SC', serif);
  color: var(--ink, #2D2A26);
  margin-bottom: 8px;
}

.welcome p {
  color: var(--ink-muted, #888);
  margin-bottom: 24px;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.suggestions button {
  padding: 8px 16px;
  background: var(--surface, #fff);
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: 20px;
  color: var(--ink, #2D2A26);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.suggestions button:hover {
  border-color: var(--accent, #6B4C3B);
  color: var(--accent, #6B4C3B);
}

/* Messages */
.message {
  display: flex;
  gap: 10px;
  max-width: 80%;
  animation: msgIn 0.3s ease;
}

@keyframes msgIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--surface-alt, #f0ebe4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.msg-body {
  display: flex;
  flex-direction: column;
}

.msg-header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.msg-bubble {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  background: var(--surface-alt, #f0ebe4);
  color: var(--ink, #2D2A26);
  border-top-left-radius: 4px;
  flex: 1;
}

.msg-delete {
  opacity: 0;
  background: none;
  border: none;
  color: var(--ink-muted, #888);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.message:hover .msg-delete {
  opacity: 1;
}

.msg-delete:hover {
  color: #c0392b;
}

.message.user .msg-bubble {
  background: var(--accent, #6B4C3B);
  color: white;
  border-top-left-radius: 12px;
  border-top-right-radius: 4px;
}

.msg-bubble.loading {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Markdown 渲染样式 */
.markdown-body {
  line-height: 1.7;
}

.markdown-body p {
  margin: 0 0 10px 0;
}

.markdown-body p:last-child {
  margin-bottom: 0;
}

.markdown-body strong {
  font-weight: 600;
  color: var(--accent, #6B4C3B);
}

.markdown-body ol,
.markdown-body ul {
  margin: 8px 0;
  padding-left: 24px;
}

.markdown-body li {
  margin-bottom: 6px;
}

.markdown-body li:last-child {
  margin-bottom: 0;
}

.markdown-body code {
  background: rgba(0, 0, 0, 0.06);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: var(--font-mono, monospace);
}

.markdown-body pre {
  background: rgba(0, 0, 0, 0.06);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 8px 0;
}

.markdown-body pre code {
  background: none;
  padding: 0;
}

.markdown-body blockquote {
  border-left: 3px solid var(--accent, #6B4C3B);
  padding-left: 12px;
  margin: 8px 0;
  color: var(--ink-muted, #666);
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4 {
  margin: 12px 0 8px 0;
  font-weight: 600;
}

.markdown-body hr {
  border: none;
  border-top: 1px solid var(--border-light, #e8e0d6);
  margin: 12px 0;
}

.loading-dots {
  display: inline-flex;
  gap: 4px;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: var(--ink-muted, #888);
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

.msg-time {
  font-size: 0.7rem;
  color: var(--ink-muted, #888);
  margin-top: 4px;
  font-family: var(--font-mono, monospace);
}

/* Source Badge */
.msg-source {
  margin-top: 6px;
}

.source-badge {
  display: inline-block;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.source-badge.rag {
  background: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}

.source-badge.llm {
  background: #e3f2fd;
  color: #1565c0;
  border: 1px solid #bbdefb;
}

.message.user .msg-time {
  text-align: right;
}

/* Retrieved Chunks */
.retrieved {
  margin-top: 8px;
}

.retrieved-toggle {
  background: none;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  padding: 4px 10px;
  font-size: 0.78rem;
  color: var(--ink-muted, #888);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.retrieved-toggle span {
  font-size: 0.65rem;
  transition: transform 0.2s;
}

.retrieved-toggle span.rotated {
  transform: rotate(180deg);
}

.retrieved-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.retrieved-item {
  background: var(--surface, #fff);
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  padding: 8px 12px;
  font-size: 0.8rem;
}

.chunk-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.chunk-file {
  font-weight: 600;
  color: var(--ink, #2D2A26);
}

.chunk-score {
  color: var(--ink-muted, #888);
  font-family: var(--font-mono, monospace);
  font-size: 0.75rem;
}

.chunk-content {
  color: var(--ink-muted, #888);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Chat Input */
.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px 0 24px;
}

.chat-input textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  background: var(--surface, #fff);
  color: var(--ink, #2D2A26);
  font-size: 0.95rem;
  resize: none;
  min-height: 48px;
  max-height: 120px;
  font-family: inherit;
}

.chat-input textarea:focus {
  outline: none;
  border-color: var(--accent, #6B4C3B);
}

.chat-input button {
  padding: 12px 28px;
  background: var(--accent, #6B4C3B);
  color: white;
  border: none;
  border-radius: var(--radius, 6px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-end;
}

.chat-input button:hover:not(:disabled) {
  opacity: 0.9;
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: var(--surface, #fff);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light, #e8e0d6);
}

.modal-header h3 {
  font-family: var(--font-display, 'Noto Serif SC', serif);
  color: var(--ink, #2D2A26);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--ink-muted, #888);
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0;
  margin-bottom: 16px;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  overflow: hidden;
}

.tabs button {
  flex: 1;
  padding: 8px 16px;
  background: var(--surface-alt, #f0ebe4);
  border: none;
  color: var(--ink-muted, #888);
  cursor: pointer;
  transition: all 0.2s;
}

.tabs button.active {
  background: var(--accent, #6B4C3B);
  color: white;
}

/* Upload Area */
.upload-area {
  margin-bottom: 16px;
}

.file-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.file-btn {
  padding: 8px 16px;
  background: var(--accent, #6B4C3B);
  color: white;
  border-radius: var(--radius, 6px);
  font-size: 0.85rem;
}

.file-name {
  color: var(--ink-muted, #888);
  font-size: 0.85rem;
}

.upload-area textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  background: var(--surface-alt, #f0ebe4);
  color: var(--ink, #2D2A26);
  font-family: inherit;
  resize: vertical;
}

.upload-area textarea:focus {
  outline: none;
  border-color: var(--accent, #6B4C3B);
}

.filename-input {
  width: 100%;
  padding: 8px 12px;
  margin-top: 8px;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  background: var(--surface-alt, #f0ebe4);
  color: var(--ink, #2D2A26);
  font-size: 0.85rem;
}

.filename-input:focus {
  outline: none;
  border-color: var(--accent, #6B4C3B);
}

/* Chunk Config */
.chunk-config {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.config-row {
  flex: 1;
  min-width: 120px;
}

.config-row label {
  display: block;
  font-size: 0.78rem;
  color: var(--ink-muted, #888);
  margin-bottom: 4px;
}

.config-row select,
.config-row input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  background: var(--surface-alt, #f0ebe4);
  color: var(--ink, #2D2A26);
  font-size: 0.85rem;
}

.config-row select:focus,
.config-row input:focus {
  outline: none;
  border-color: var(--accent, #6B4C3B);
}

.parse-btn {
  width: 100%;
  padding: 10px;
  background: var(--accent, #6B4C3B);
  color: white;
  border: none;
  border-radius: var(--radius, 6px);
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.parse-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.parse-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Preview */
.preview {
  margin-top: 16px;
  border-top: 1px solid var(--border-light, #e8e0d6);
  padding-top: 16px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 0.85rem;
  color: var(--ink, #2D2A26);
}

.preview-header button {
  background: none;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  padding: 2px 8px;
  font-size: 0.78rem;
  color: var(--ink-muted, #888);
  cursor: pointer;
  margin-left: 6px;
}

.preview-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid var(--border-light, #e8e0d6);
  border-radius: var(--radius, 6px);
  margin-bottom: 12px;
}

.preview-item {
  padding: 6px 12px;
  border-bottom: 1px solid var(--border-light, #e8e0d6);
  font-size: 0.8rem;
}

.preview-item:last-child {
  border-bottom: none;
}

.preview-item label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
}

.preview-idx {
  color: var(--ink-muted, #888);
  font-family: var(--font-mono, monospace);
  white-space: nowrap;
}

.preview-text {
  color: var(--ink, #2D2A26);
  line-height: 1.4;
}

.save-btn {
  width: 100%;
  padding: 10px;
  background: var(--accent, #6B4C3B);
  color: white;
  border: none;
  border-radius: var(--radius, 6px);
  cursor: pointer;
  font-size: 0.9rem;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.success-msg {
  color: #3a7d44;
  text-align: center;
  font-size: 0.85rem;
  margin-top: 8px;
}

.error-msg {
  color: #c0392b;
  text-align: center;
  font-size: 0.85rem;
  margin-top: 8px;
}

/* KB Stats */
.kb-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-card {
  background: var(--surface-alt, #f0ebe4);
  border-radius: var(--radius, 6px);
  padding: 16px;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent, #6B4C3B);
  font-family: var(--font-mono, monospace);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--ink-muted, #888);
  margin-top: 4px;
}

.doc-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.doc-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: var(--surface-alt, #f0ebe4);
  border-radius: var(--radius, 6px);
}

.doc-info {
  display: flex;
  flex-direction: column;
}

.doc-name {
  font-weight: 600;
  color: var(--ink, #2D2A26);
  font-size: 0.9rem;
}

.doc-count {
  font-size: 0.75rem;
  color: var(--ink-muted, #888);
}

.delete-btn {
  padding: 4px 12px;
  background: none;
  border: 1px solid #c0392b;
  border-radius: var(--radius, 6px);
  color: #c0392b;
  cursor: pointer;
  font-size: 0.78rem;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: #c0392b;
  color: white;
}

.empty-msg {
  text-align: center;
  color: var(--ink-muted, #888);
  padding: 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .rag-header {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }

  .header-actions {
    width: 100%;
    justify-content: center;
  }

  .main-content {
    flex-direction: column;
  }

  .conversations-sidebar {
    width: 100%;
    max-height: 200px;
    border-right: none;
    border-bottom: 1px solid var(--border-light, #e8e0d6);
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

  .kb-stats {
    grid-template-columns: 1fr;
  }

  .chunk-config {
    flex-direction: column;
  }
}
</style>
