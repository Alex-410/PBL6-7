#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
import time

BASE_URL = 'http://localhost:8080/api'
RAG_URL = 'http://localhost:9001/api/rag'

print('=' * 60)
print('校园活动发布平台 - 完整测试报告')
print('=' * 60)
print()

bugs = []
passed = 0
failed = 0

def test(name, condition, bug=None):
    global passed, failed
    status = 'PASS' if condition else 'FAIL'
    print(f'[{status}] {name}')
    if bug and not condition:
        print(f'      BUG: {bug}')
        bugs.append(bug)
    if condition:
        passed += 1
    else:
        failed += 1

# ============ 认证模块 ============
print('=' * 40)
print('认证模块测试')
print('=' * 40)

ts = str(int(time.time()))[-4:]

# TC-001: 正常注册
data = {'username': f'u{ts}', 'password': 'Test123456', 'confirmPassword': 'Test123456',
        'email': f'u{ts}@test.com', 'phone': f'1390000{ts}'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data)
r = resp.json()
test('TC-001: 正常注册', r.get('code') == 200 and r.get('data') is not None)
user_token = r.get('data', {}).get('token') if r.get('data') else None

# TC-002: 重复用户名
data2 = {'username': f'u{ts}', 'password': 'Test123456', 'confirmPassword': 'Test123456',
         'email': 'other@test.com', 'phone': '13900009999'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data2)
test('TC-002: 重复用户名注册应拒绝', resp.json().get('code') != 200)

# TC-003: 密码不一致
ts2 = str(int(time.time())+1)[-4:]
data3 = {'username': f'u{ts2}', 'password': 'Test123456', 'confirmPassword': 'Different',
         'email': f'u{ts2}@test.com', 'phone': f'1390001{ts2}'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data3)
test('TC-003: 密码不一致应拒绝', resp.json().get('code') != 200)

# TC-004: 弱密码
data4 = {'username': f'w{ts2}', 'password': '123', 'confirmPassword': '123',
         'email': f'w{ts2}@test.com', 'phone': f'1390002{ts2}'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data4)
test('TC-004: 弱密码应拒绝', resp.json().get('code') != 200)

# TC-005: 无效邮箱
data5 = {'username': f'e{ts2}', 'password': 'Test123456', 'confirmPassword': 'Test123456',
         'email': 'not-an-email', 'phone': f'1390003{ts2}'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data5)
test('TC-005: 无效邮箱应拒绝', resp.json().get('code') != 200)

# TC-006: 无效手机号
data6 = {'username': f'p{ts2}', 'password': 'Test123456', 'confirmPassword': 'Test123456',
         'email': f'p{ts2}@test.com', 'phone': '123'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data6)
test('TC-006: 无效手机号应拒绝', resp.json().get('code') != 200)

# TC-007: 不存在用户登录
resp = requests.post(f'{BASE_URL}/auth/login', json={'username': 'nonexist', 'password': 'test'})
test('TC-007: 不存在用户登录应拒绝', resp.json().get('code') != 200)

# TC-008: 错误密码
resp = requests.post(f'{BASE_URL}/auth/login', json={'username': f'u{ts}', 'password': 'wrong'})
test('TC-008: 错误密码应拒绝', resp.json().get('code') != 200)

# TC-009: 正确登录
resp = requests.post(f'{BASE_URL}/auth/login', json={'username': f'u{ts}', 'password': 'Test123456'})
test('TC-009: 正确登录', resp.json().get('code') == 200)

# TC-010: 登录暴力破解防护
blocked = False
for i in range(10):
    resp = requests.post(f'{BASE_URL}/auth/login', json={'username': 'admin', 'password': 'wrong'})
    if resp.status_code == 429 or '尝试次数' in str(resp.json().get('message', '')):
        blocked = True
        break
test('TC-010: 登录频率限制', blocked, '无登录失败频率限制，可暴力破解密码')

print()

# ============ 活动模块 ============
print('=' * 40)
print('活动模块测试')
print('=' * 40)

headers = {'Authorization': f'Bearer {user_token}'} if user_token else {}

# TC-011: 未认证访问
resp = requests.get(f'{BASE_URL}/activities')
test('TC-011: 未认证访问应被拒绝', resp.status_code in [401, 403])

# TC-012: 认证后访问
resp = requests.get(f'{BASE_URL}/activities', headers=headers)
test('TC-012: 认证后访问活动列表', resp.json().get('code') == 200)

# TC-013: 创建活动
act_data = {'title': f'测试活动{ts}', 'category': '学术讲座', 'description': '测试',
            'startTime': '2026-06-15T10:00:00', 'endTime': '2026-06-15T12:00:00',
            'location': 'A101', 'organizer': '测试', 'maxCount': 100}
resp = requests.post(f'{BASE_URL}/activities', json=act_data, headers=headers)
r = resp.json()
test('TC-013: 创建活动', r.get('code') == 200)
activity_id = r.get('data', {}).get('id') if r.get('data') else None

# TC-014: 缺少必填字段
resp = requests.post(f'{BASE_URL}/activities', json={'category': 'test'}, headers=headers)
test('TC-014: 缺少标题创建活动应失败', resp.json().get('code') != 200)

# TC-015: 获取活动详情
if activity_id:
    resp = requests.get(f'{BASE_URL}/activities/{activity_id}', headers=headers)
    test('TC-015: 获取活动详情', resp.json().get('code') == 200)

# TC-016: 审核活动（普通用户）
if activity_id:
    resp = requests.put(f'{BASE_URL}/activities/{activity_id}/audit?action=approve', headers=headers)
    test('TC-016: 非管理员审核活动应拒绝', resp.json().get('code') != 200,
         '任何用户都能审核活动，缺少权限检查' if resp.json().get('code') == 200 else None)

# TC-017: 无效审核操作
if activity_id:
    resp = requests.put(f'{BASE_URL}/activities/{activity_id}/audit?action=invalid', headers=headers)
    test('TC-017: 无效审核操作应拒绝', resp.json().get('code') != 200,
         '无效action参数默认为rejected，缺少验证' if resp.json().get('code') == 200 else None)

# TC-018: 删除他人活动
if activity_id:
    resp = requests.delete(f'{BASE_URL}/activities/{activity_id}', headers=headers)
    test('TC-018: 删除活动权限检查', resp.json().get('code') != 200,
         '任何用户都能删除任意活动，缺少权限检查' if resp.json().get('code') == 200 else None)

print()

# ============ 报名模块 ============
print('=' * 40)
print('报名模块测试')
print('=' * 40)

# TC-019: 查看我的报名
resp = requests.get(f'{BASE_URL}/registrations/me', headers=headers)
test('TC-019: 查看我的报名', resp.json().get('code') == 200)

# TC-020: 报名不存在的活动
resp = requests.post(f'{BASE_URL}/registrations?activityId=99999', headers=headers)
test('TC-020: 报名不存在活动应拒绝', resp.json().get('code') != 200)

print()

# ============ 用户管理 ============
print('=' * 40)
print('用户管理测试')
print('=' * 40)

# TC-021: 普通用户查看用户列表
resp = requests.get(f'{BASE_URL}/users', headers=headers)
test('TC-021: 普通用户查看用户列表应拒绝', resp.json().get('code') != 200,
     '普通用户可以查看所有用户列表，缺少权限控制' if resp.json().get('code') == 200 else None)

# TC-022: 更新用户状态（无效类型）
resp = requests.put(f'{BASE_URL}/users/1/status', json={'status': 'invalid'}, headers=headers)
test('TC-022: 无效状态类型应返回友好错误', resp.status_code != 500,
     '无效状态类型导致500服务器错误' if resp.status_code == 500 else None)

# TC-023: 获取不存在用户
resp = requests.get(f'{BASE_URL}/users/99999', headers=headers)
test('TC-023: 获取不存在用户', resp.json().get('code') != 200)

print()

# ============ RAG系统 ============
print('=' * 40)
print('RAG系统测试')
print('=' * 40)

try:
    resp = requests.get(f'{RAG_URL}/status/', timeout=5)
    test('TC-024: RAG服务状态', resp.status_code == 200)
    rag_ok = True
except:
    test('TC-024: RAG服务状态', False, 'RAG服务未启动')
    rag_ok = False

if rag_ok:
    # TC-025: 空问题
    resp = requests.post(f'{RAG_URL}/chat/', json={'question': ''})
    test('TC-025: 空问题应返回400', resp.status_code == 400)

    # TC-026: 创建对话
    resp = requests.post(f'{RAG_URL}/conversations/', json={'title': '测试'})
    test('TC-026: 创建对话', resp.status_code == 201)

    # TC-027: 删除不存在文档
    resp = requests.post(f'{RAG_URL}/delete/', json={'filename': 'nonexist.txt'})
    test('TC-027: 删除不存在文档应返回错误', resp.status_code == 400)

# TC-028: chunk_text无限循环风险
test('TC-028: chunk_text无限循环风险', False,
     'chunk_size=overlap时fixed策略无限循环 (main.py:104-108)')

print()

# ============ 安全测试 ============
print('=' * 40)
print('安全测试')
print('=' * 40)

# TC-029: SQL注入
resp = requests.post(f'{BASE_URL}/auth/login', json={'username': "admin' OR '1'='1", 'password': 'x'})
test('TC-029: SQL注入防护', resp.json().get('code') != 200)

# TC-030: JWT篡改
resp = requests.get(f'{BASE_URL}/activities', headers={'Authorization': 'Bearer fake.token.here'})
test('TC-030: JWT篡改防护', resp.status_code in [401, 403])

# TC-031: 禁用用户后token有效性
test('TC-031: 禁用用户后token仍有效', False,
     '禁用用户后JWT token仍然有效，缺少token失效机制')

# TC-032: XSS防护
if user_token:
    xss_data = {'title': '<script>alert(1)</script>', 'category': 'test', 'description': 'xss',
                'startTime': '2026-06-15T10:00:00', 'endTime': '2026-06-15T12:00:00',
                'location': 'test', 'organizer': 'test'}
    resp = requests.post(f'{BASE_URL}/activities', json=xss_data, headers=headers)
    title = resp.json().get('data', {}).get('title', '') if resp.json().get('data') else ''
    test('TC-032: XSS防护', '<script>' not in title,
         '活动标题未转义HTML标签' if '<script>' in title else None)

print()

# ============ 汇总 ============
print('=' * 60)
print('测试结果汇总')
print('=' * 60)
print(f'通过: {passed}')
print(f'失败: {failed}')
print(f'总计: {passed + failed}')
print()

if bugs:
    print('发现的BUG清单:')
    print('-' * 40)
    for i, bug in enumerate(bugs, 1):
        print(f'{i}. {bug}')
else:
    print('未发现BUG')

print()
print('=' * 60)
