from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import re
import requests
from pathlib import Path
import uuid
import gc

app = Flask(__name__)
CORS(app)

env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Try project-local vector_db first, fallback to user home
PROJECT_DIR = os.path.dirname(__file__)
LOCAL_VECTOR_DB = os.path.join(PROJECT_DIR, 'vector_db')
USER_DATA_DIR = os.path.join(os.path.expanduser('~'), 'campus-rag-data')

# Use local vector_db if it exists, otherwise use user home
if os.path.exists(os.path.join(LOCAL_VECTOR_DB, 'faiss_index.index')):
    RAG_DATA_DIR = LOCAL_VECTOR_DB
else:
    RAG_DATA_DIR = USER_DATA_DIR
    os.makedirs(RAG_DATA_DIR, exist_ok=True)

FAISS_INDEX_FILE = os.path.join(RAG_DATA_DIR, 'faiss_index')
DOCS_FILE = os.path.join(RAG_DATA_DIR, 'documents.json')
CONVERSATIONS_FILE = os.path.join(USER_DATA_DIR, 'conversations.json')  # Always use user dir for conversations
DOC_META_FILE = os.path.join(USER_DATA_DIR, 'doc_meta.json')
DEMO_RULES_FILE = os.path.join(PROJECT_DIR, 'rag_data', 'demo_rules.txt')

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'qwen3-embedding:0.6b')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')
LLM_MODEL = os.getenv('LLM_MODEL', 'deepseek-chat')
LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://api.deepseek.com')

# Lazy-loaded globals - only loaded when needed
_faiss_index = None
_documents = None
_index_loaded = False


def get_embeddings(texts):
    url = f'{OLLAMA_BASE_URL}/api/embed'
    vectors = []
    for text in texts:
        try:
            resp = requests.post(url, json={'model': EMBEDDING_MODEL, 'input': text}, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if 'embedding' in result:
                vectors.append(result['embedding'])
            elif 'embeddings' in result:
                vectors.append(result['embeddings'][0])
            else:
                raise Exception(f'Ollama响应缺少embedding字段: {result}')
        except requests.exceptions.RequestException as e:
            raise Exception(f'连接Ollama失败: {str(e)}')
        except (KeyError, ValueError, IndexError) as e:
            raise Exception(f'Ollama响应格式错误: {str(e)}')
    return vectors


def _sentence_boundary(text, low, high):
    if low >= high:
        return high
    candidates = []
    for ch in '。！？.!?\n':
        pos = text.rfind(ch, low, high)
        if pos >= low:
            candidates.append(pos + 1)
    if candidates:
        return max(candidates)
    for ch in '；;，,）)》":：':
        pos = text.rfind(ch, low, high)
        if pos >= low:
            return pos + 1
    return high


def chunk_text(text, strategy='fixed', chunk_size=500, overlap=50):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()
    if not text:
        return []

    if strategy == 'fixed':
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            if end < len(text):
                search_start = max(start + chunk_size * 3 // 4, start)
                boundary = _sentence_boundary(text, search_start, end)
                if boundary > search_start:
                    end = boundary
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if overlap <= 0:
                start = end
            else:
                start = start + chunk_size - overlap
            if start >= len(text):
                break
            if start <= 0 and overlap > 0:
                break
        return chunks

    elif strategy == 'recursive':
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not paragraphs:
            return [text]
        chunks = []
        current = ''
        for para in paragraphs:
            if len(current) + len(para) + 2 <= chunk_size:
                current += ('\n\n' if current else '') + para
            else:
                if current:
                    chunks.append(current)
                if len(para) > chunk_size:
                    sub_start = 0
                    while sub_start < len(para):
                        sub_end = min(sub_start + chunk_size, len(para))
                        if sub_end < len(para):
                            s = max(sub_start, sub_end - overlap - 50)
                            b = _sentence_boundary(para, s, sub_end)
                            if b > s:
                                sub_end = b
                        sub = para[sub_start:sub_end].strip()
                        if sub:
                            chunks.append(sub)
                        sub_start = sub_end - overlap
                        if sub_start <= 0:
                            break
                    current = ''
                else:
                    current = para
        if current:
            chunks.append(current)
        return chunks

    elif strategy == 'parent':
        lines = text.split('\n')
        sections = []
        heading = ''
        body = []

        def flush_section():
            nonlocal heading, body
            content = '\n'.join(body).strip() if body else ''
            if heading or content:
                sections.append((heading, content))
            heading = ''
            body = []

        for line in lines:
            stripped = line.strip()
            if re.match(r'^#{1,6}\s+\S', stripped) or \
               re.match(r'^(\d+|[IVXLCDM]+)[\.、\)]\s+\S', stripped):
                flush_section()
                heading = stripped
            else:
                body.append(line)
        flush_section()

        if not sections or (len(sections) == 1 and not sections[0][0]):
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
            sections = [('', p) for p in paragraphs]

        chunks = []
        buffer = []
        buf_len = 0

        def emit():
            nonlocal buffer, buf_len
            if buffer:
                text_out = '\n\n'.join(buffer)
                if text_out.strip():
                    chunks.append(text_out.strip())
                buffer = []
                buf_len = 0

        for h, body_text in sections:
            seg = (h + '\n' + body_text) if h else body_text
            seg = seg.strip()
            if not seg:
                continue
            if len(seg) > chunk_size:
                emit()
                sub = chunk_text(seg, 'recursive', chunk_size, overlap)
                chunks.extend(sub)
            elif buf_len + len(seg) + 2 <= chunk_size:
                entry = (h + '\n' + body_text) if h else body_text
                buffer.append(entry)
                buf_len += len(entry)
            else:
                emit()
                buffer.append((h + '\n' + body_text) if h else body_text)
                buf_len = len(seg)
        emit()
        return chunks

    return [text]


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ''

    if ext in ['.txt', '.md']:
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                break
            except UnicodeDecodeError:
                continue
        if not text:
            return '', '无法解码文件，请确保文件是UTF-8编码'

    elif ext == '.pdf':
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
        except Exception:
            pass
        if not text.strip():
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + '\n'
            except Exception as e:
                return '', str(e)

    elif ext == '.docx':
        try:
            from docx import Document
            doc = Document(file_path)
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + '\n'
        except Exception as e:
            return '', str(e)

    return text, None


def load_faiss_index():
    global _faiss_index, _documents, _index_loaded
    if _index_loaded:
        return _faiss_index, _documents

    if os.path.exists(FAISS_INDEX_FILE + '.index'):
        import faiss
        _faiss_index = faiss.read_index(FAISS_INDEX_FILE + '.index')
    if os.path.exists(DOCS_FILE):
        with open(DOCS_FILE, 'r', encoding='utf-8') as f:
            _documents = json.load(f)
    else:
        _documents = []

    _index_loaded = True
    return _faiss_index, _documents


def save_faiss_index():
    import faiss
    faiss.write_index(_faiss_index, FAISS_INDEX_FILE + '.index')
    with open(DOCS_FILE, 'w', encoding='utf-8') as f:
        json.dump(_documents, f, ensure_ascii=False, indent=2)


def load_demo_rules():
    global _faiss_index, _documents, _index_loaded
    load_faiss_index()
    if _faiss_index is not None and _documents and len(_documents) > 0:
        print(f'Knowledge base already has {len(_documents)} chunks, skipping demo load.')
        return

    if not os.path.exists(DEMO_RULES_FILE):
        print('No demo rules file found, skipping.')
        return

    print('Loading demo school rules into knowledge base...')
    with open(DEMO_RULES_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    if not text.strip():
        print('Demo rules file is empty, skipping.')
        return

    chunks = chunk_text(text, strategy='fixed', chunk_size=500, overlap=50)
    print(f'Chunked demo rules into {len(chunks)} pieces. Generating embeddings...')

    try:
        vectors = get_embeddings(chunks)
    except Exception as e:
        print(f'Failed to generate embeddings: {e}')
        print('Please make sure Ollama is running and the embedding model is pulled:')
        print(f'  ollama pull {EMBEDDING_MODEL}')
        return

    import numpy as np
    import faiss
    vectors = np.array(vectors).astype('float32')
    dim = vectors.shape[1]
    _faiss_index = faiss.IndexFlatL2(dim)
    _faiss_index.add(vectors)
    del vectors
    gc.collect()

    _documents = []
    for i, chunk in enumerate(chunks):
        _documents.append({
            'id': f'demo_{i}',
            'filename': 'demo_rules.txt',
            'chunk_index': i,
            'content': chunk,
            'strategy': 'fixed'
        })

    _index_loaded = True
    save_faiss_index()
    print(f'Demo rules loaded successfully: {len(chunks)} chunks indexed.')


def load_conversations():
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_conversations(conversations):
    with open(CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)


def load_doc_meta():
    if os.path.exists(DOC_META_FILE):
        with open(DOC_META_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_doc_meta(meta):
    with open(DOC_META_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


# ─── API Endpoints ───

@app.route('/api/rag/status/', methods=['GET'])
def get_status():
    idx, docs = load_faiss_index()

    docs_list = []
    if docs:
        file_names = sorted(set(d['filename'] for d in docs))
        for fname in file_names:
            count = sum(1 for d in docs if d['filename'] == fname)
            docs_list.append({'filename': fname, 'count': count})

    return jsonify({
        'has_index': idx is not None,
        'doc_count': len(docs) if docs else 0,
        'docs': docs_list,
        'embedding_model': EMBEDDING_MODEL,
    })


@app.route('/api/rag/upload/', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': '请上传文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '请上传文件'}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.txt', '.md', '.pdf', '.docx']:
        return jsonify({'error': '不支持的文件类型，仅支持 TXT/MD/PDF/DOCX'}), 400

    strategy = request.form.get('strategy', 'fixed')
    chunk_size = int(request.form.get('chunk_size', 500))
    overlap = int(request.form.get('overlap', 50))

    filename = file.filename
    temp_filename = f"{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(RAG_DATA_DIR, temp_filename)
    file.save(temp_path)

    text, error = extract_text_from_file(temp_path)
    os.remove(temp_path)

    if error:
        return jsonify({'error': f'解析文件失败: {error}'}), 500

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()

    if not text:
        return jsonify({'error': '无法从文件中提取到文本内容'}), 400

    chunks = chunk_text(text, strategy, chunk_size, overlap)
    preview_chunks = [{'index': i, 'content': chunk, 'selected': True} for i, chunk in enumerate(chunks)]

    return jsonify({
        'preview': True,
        'filename': filename,
        'chunks': preview_chunks,
        'strategy': strategy
    })


@app.route('/api/rag/upload_text/', methods=['POST'])
def upload_text():
    data = request.get_json()
    text = data.get('text', '').strip()
    filename = data.get('filename', '手动输入.txt')
    strategy = data.get('strategy', 'fixed')
    chunk_size = int(data.get('chunk_size', 500))
    overlap = int(data.get('overlap', 50))

    if not text:
        return jsonify({'error': '请输入文本内容'}), 400

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()

    chunks = chunk_text(text, strategy, chunk_size, overlap)
    preview_chunks = [{'index': i, 'content': chunk, 'selected': True} for i, chunk in enumerate(chunks)]

    return jsonify({
        'preview': True,
        'filename': filename,
        'chunks': preview_chunks,
        'strategy': strategy
    })


@app.route('/api/rag/save/', methods=['POST'])
def save_chunks():
    data = request.get_json()
    filename = data.get('filename', '')
    strategy = data.get('strategy', 'fixed')
    selected_chunks = data.get('selected_chunks', [])

    if not selected_chunks:
        return jsonify({'error': '请至少选择一个切片'}), 400

    global _faiss_index, _documents, _index_loaded

    try:
        vectors = get_embeddings(selected_chunks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    import numpy as np
    vectors = np.array(vectors).astype('float32')

    if _faiss_index is None:
        import faiss
        dim = vectors.shape[1]
        _faiss_index = faiss.IndexFlatL2(dim)

    _faiss_index.add(vectors)
    del vectors

    if _documents is None:
        _documents = []

    doc_id = len(_documents)
    for i, chunk in enumerate(selected_chunks):
        _documents.append({
            'id': f'{doc_id}_{i}',
            'filename': filename,
            'chunk_index': i,
            'content': chunk,
            'strategy': strategy
        })

    _index_loaded = True
    save_faiss_index()
    gc.collect()

    return jsonify({
        'success': True,
        'filename': filename,
        'chunks': len(selected_chunks),
        'strategy': strategy
    })


@app.route('/api/rag/delete/', methods=['POST'])
def delete_document():
    global _faiss_index, _documents, _index_loaded
    data = request.get_json()
    filename = data.get('filename', '')

    if not filename:
        return jsonify({'error': '请指定要删除的文件'}), 400

    load_faiss_index()

    if _faiss_index is None:
        return jsonify({'error': '知识库为空'}), 400

    indices_to_keep = [i for i, d in enumerate(_documents) if d['filename'] != filename]

    if len(indices_to_keep) == len(_documents):
        return jsonify({'error': '文件不存在'}), 400

    if len(indices_to_keep) == 0:
        _faiss_index = None
        _documents = []
        _index_loaded = False
        if os.path.exists(FAISS_INDEX_FILE + '.index'):
            os.remove(FAISS_INDEX_FILE + '.index')
        if os.path.exists(DOCS_FILE):
            os.remove(DOCS_FILE)
    else:
        import faiss
        dim = _faiss_index.d
        new_index = faiss.IndexFlatL2(dim)

        new_docs = []
        for i in indices_to_keep:
            new_docs.append(_documents[i])
            vec = _faiss_index.reconstruct(i)
            new_index.add(vec.reshape(1, -1))

        _faiss_index = new_index
        _documents = new_docs
        save_faiss_index()

    gc.collect()
    return jsonify({'success': True})


SCHOOL_RULES_KEYWORDS = [
    '校规', '校纪', '处分', '违纪', '违规', '作弊', '考试', '补考', '重修',
    '学籍', '注册', '休学', '复学', '退学', '转专业', '转学', '毕业', '结业',
    '宿舍', '寝室', '晚归', '门禁', '卫生', '大功率', '电器',
    '图书馆', '借阅', '续借', '逾期', '赔偿',
    '奖学金', '助学金', '助学贷款', '勤工助学', '困难补助', '减免学费',
    '学分', '绩点', '成绩', '升级', '留级', '降级',
    '学生证', '校园卡', '请假', '考勤', '迟到', '旷课',
    '开除', '记过', '警告', '严重警告', '留校察看', '申诉',
    '行为规范', '文明', '酗酒', '打架', '赌博', '吸烟',
    '安全', '消防', '治安', '保卫',
    '社团', '学生组织', '集会',
    '权利', '义务', '学生手册', '管理规定',
    '选课', '辅修', '学制', '学年', '学期',
    '体测', '体育课', '保健课',
    '心理咨询', '心理健康',
    '学费', '缴费', '欠费',
]


def is_school_rules_question(question):
    """Check if question is related to school rules using keyword matching."""
    for kw in SCHOOL_RULES_KEYWORDS:
        if kw in question:
            return True
    return False


def rewrite_queries(question):
    """Generate multiple search queries for better retrieval."""
    queries = [question]

    # Add domain-specific reformulations
    if any(w in question for w in ['处分', '违纪', '违规', '处罚']):
        queries.append('纪律处分 警告 记过 留校察看 开除学籍')
        queries.append('违纪行为 处分程序 申诉')
    elif any(w in question for w in ['考试', '作弊', '补考', '重修']):
        queries.append('考试纪律 考场规则 违纪处理')
        queries.append('成绩记载 补考 重修 学分')
    elif any(w in question for w in ['宿舍', '寝室', '住宿', '晚归']):
        queries.append('宿舍管理 住宿规定 门禁 安全')
        queries.append('卫生检查 用电安全 违禁物品')
    elif any(w in question for w in ['奖学金', '助学金', '补助', '贷款']):
        queries.append('奖学金评定条件 申请程序')
        queries.append('助学贷款 勤工助学 困难补助 学费减免')
    elif any(w in question for w in ['转专业', '转学', '休学', '复学', '退学']):
        queries.append('学籍管理 转专业 转学 休学 复学 退学')
        queries.append('学籍变动 申请条件 审批程序')
    elif any(w in question for w in ['图书馆', '借阅', '续借']):
        queries.append('图书馆管理 借阅规则 逾期费')
        queries.append('入馆须知 赔偿标准 电子资源')
    elif any(w in question for w in ['毕业', '结业', '肄业', '学位']):
        queries.append('毕业条件 学位授予 学历证书')
        queries.append('结业 肄业 最长学习年限')
    elif any(w in question for w in ['学分', '绩点', '成绩', '选课']):
        queries.append('考核与成绩记载 考试 考查 学分')
        queries.append('辅修 选课 升级 留级')

    return queries


def call_llm(messages, temperature=0.3):
    """Call DeepSeek LLM API."""
    llm_url = f'{LLM_BASE_URL}/v1/chat/completions'
    payload = {
        'model': LLM_MODEL,
        'messages': messages,
        'temperature': temperature,
        'top_p': 0.85
    }
    resp = requests.post(llm_url, json=payload, headers={
        'Authorization': f'Bearer {LLM_API_KEY}',
        'Content-Type': 'application/json'
    }, timeout=60)
    result = resp.json()
    return result['choices'][0]['message']['content']


@app.route('/api/rag/chat/', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': '请输入问题'}), 400

    selected_docs = data.get('selected_docs', [])
    conversation_id = data.get('conversation_id', '')

    conversations = load_conversations()
    conv = None
    for c in conversations:
        if c['id'] == conversation_id:
            conv = c
            break
    if conv is None:
        conv = {
            'id': conversation_id or uuid.uuid4().hex[:8],
            'title': '新对话',
            'messages': [],
            'config': {'selected_docs': []}
        }
        conversations.append(conv)

    # ─── Step 1: Classify question ───
    is_rules_related = is_school_rules_question(question)

    # ─── Step 2: Route to appropriate handler ───
    if is_rules_related:
        # School rules path: RAG retrieval + LLM
        answer, retrieved_chunks = handle_school_rules_question(question, selected_docs)
    else:
        # General path: LLM only (no RAG)
        answer, retrieved_chunks = handle_general_question(question)

    # Save messages
    saved_retrieved = [{
        'content': c['content'],
        'filename': c['filename'],
        'score': c['score'],
    } for c in retrieved_chunks[:5]]

    conv['messages'].append({'role': 'user', 'content': question})
    conv['messages'].append({'role': 'assistant', 'content': answer, 'retrieved': saved_retrieved, 'is_rules_related': is_rules_related})
    if conv['title'] == '新对话' and len(question) > 0:
        conv['title'] = (question[:20] + '…') if len(question) > 20 else question
    save_conversations(conversations)

    return jsonify({
        'answer': answer,
        'retrieved_chunks': retrieved_chunks[:5],
        'conversation_id': conv['id'],
        'messages': conv['messages'],
        'is_rules_related': is_rules_related,
    })


def handle_school_rules_question(question, selected_docs):
    """Handle school rules questions with RAG retrieval."""
    idx, docs = load_faiss_index()

    if idx is None or not docs or len(docs) == 0:
        return '知识库为空，请先上传校规文档。', []

    # ─── Multi-query retrieval ───
    search_queries = rewrite_queries(question)

    try:
        all_vectors = get_embeddings(search_queries)
    except Exception as e:
        return f'向量化失败: {str(e)}', []

    import numpy as np
    all_vectors = np.array(all_vectors).astype('float32')

    top_k = min(15, len(docs))
    seen_indices = set()
    retrieved_chunks = []

    for vec in all_vectors:
        distances, indices = idx.search(vec.reshape(1, -1), top_k)
        for i, doc_idx in enumerate(indices[0]):
            doc_idx = int(doc_idx)
            if 0 <= doc_idx < len(docs) and doc_idx not in seen_indices:
                seen_indices.add(doc_idx)
                retrieved_chunks.append({
                    'content': docs[doc_idx]['content'],
                    'filename': docs[doc_idx]['filename'],
                    'score': float(distances[0][i]),
                    'index': doc_idx
                })

    # Sort by score (lower = better for L2 distance)
    retrieved_chunks.sort(key=lambda x: x['score'])

    # Filter by selected docs if specified
    if selected_docs:
        filtered = [c for c in retrieved_chunks if c['filename'] in selected_docs]
        if filtered:
            retrieved_chunks = filtered

    # Take top results
    top_chunks = retrieved_chunks[:8]
    context = '\n\n'.join([f'[来源: {c["filename"]}]\n{c["content"]}' for c in top_chunks])

    prompt = f'''请基于以下校规校纪文档片段回答问题。这些片段来自学校规章制度的不同章节。

要求：
- 仔细阅读所有片段，将不同片段中相关的信息进行关联和综合
- 回答要准确、简洁，引用具体的规章制度条款（如"根据第X章第X条"）
- 如果知识库中没有相关信息，诚实说明并建议咨询学校相关部门
- 回答使用中文

知识库片段：
{context}

问题：{question}

回答：'''

    try:
        answer = call_llm([
            {'role': 'system', 'content': '你是校规知识库助手。根据提供的校规校纪文档片段回答问题。要求：仔细关联和综合不同片段中的信息，引用具体条款。如果没有相关信息，诚实说明并建议咨询学校相关部门。回答简洁准确，使用中文。'},
            {'role': 'user', 'content': prompt}
        ], temperature=0.3)
    except Exception as e:
        answer = f'调用LLM失败: {str(e)}'

    return answer, top_chunks


def handle_general_question(question):
    """Handle general questions without RAG (direct LLM call)."""
    try:
        answer = call_llm([
            {'role': 'system', 'content': '你是一个智能助手，可以回答各种问题。回答要准确、有帮助、简洁。使用中文回答。'},
            {'role': 'user', 'content': question}
        ], temperature=0.7)
    except Exception as e:
        answer = f'调用LLM失败: {str(e)}'

    return answer, []


@app.route('/api/rag/conversations/', methods=['GET'])
def get_conversations():
    conversations = load_conversations()
    return jsonify([{
        'id': c['id'],
        'title': c['title'],
        'msg_count': len(c['messages']),
        'config': c.get('config', {'selected_docs': []})
    } for c in conversations])


@app.route('/api/rag/conversations/', methods=['POST'])
def create_conversation():
    data = request.get_json() or {}
    conversations = load_conversations()
    conv = {
        'id': uuid.uuid4().hex[:8],
        'title': data.get('title', '新对话'),
        'messages': [],
        'config': {'selected_docs': []}
    }
    conversations.append(conv)
    save_conversations(conversations)
    return jsonify(conv), 201


@app.route('/api/rag/conversations/<conv_id>/messages/', methods=['GET'])
def get_conversation_messages(conv_id):
    conversations = load_conversations()
    for c in conversations:
        if c['id'] == conv_id:
            return jsonify({'messages': c['messages']})
    return jsonify({'error': '未找到对话'}), 404


@app.route('/api/rag/conversations/delete/', methods=['POST'])
def delete_conversation():
    data = request.get_json()
    conv_id = data.get('id', '')
    conversations = load_conversations()
    conversations = [c for c in conversations if c['id'] != conv_id]
    save_conversations(conversations)
    return jsonify({'success': True})


@app.route('/api/rag/conversations/delete_message/', methods=['POST'])
def delete_message():
    data = request.get_json()
    conv_id = data.get('conversation_id', '')
    msg_index = data.get('index', -1)
    conversations = load_conversations()
    for c in conversations:
        if c['id'] == conv_id:
            if 0 <= msg_index < len(c['messages']):
                c['messages'].pop(msg_index)
                save_conversations(conversations)
                return jsonify({'success': True, 'messages': c['messages']})
            break
    return jsonify({'error': '未找到消息'}), 404


@app.route('/api/rag/conversations/config/', methods=['POST'])
def update_conversation_config():
    data = request.get_json()
    conv_id = data.get('id', '')
    config = data.get('config', {})
    conversations = load_conversations()
    for c in conversations:
        if c['id'] == conv_id:
            c['config'] = config
            save_conversations(conversations)
            return jsonify({'success': True, 'config': config})
    return jsonify({'error': '未找到对话'}), 404


@app.route('/api/rag/docs/meta/', methods=['GET'])
def get_doc_meta():
    return jsonify(load_doc_meta())


@app.route('/api/rag/docs/meta/', methods=['POST'])
def update_doc_meta():
    data = request.get_json()
    filename = data.get('filename', '')
    description = data.get('description', '')
    meta = load_doc_meta()
    if filename:
        if description:
            meta[filename] = description
        else:
            meta.pop(filename, None)
        save_doc_meta(meta)
        return jsonify({'success': True})
    return jsonify({'error': '缺少 filename'}), 400


if __name__ == '__main__':
    port = int(os.getenv('PORT', 9001))
    load_demo_rules()
    print(f'Starting RAG server on port {port}...')
    app.run(host='0.0.0.0', port=port, debug=False)
