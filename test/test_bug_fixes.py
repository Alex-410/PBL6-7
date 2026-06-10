#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUG修复验证测试 - 用于验证修复后的代码是否解决了问题
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
import time

BASE_URL = 'http://localhost:8080/api'
RAG_URL = 'http://localhost:9001/api/rag'

print('=' * 60)
print('BUG修复验证测试')
print('用于验证代码修复后BUG是否已解决')
print('=' * 60)
print()

bugs_fixed = 0
bugs_remaining = 0

def check_bug(bug_id, bug_name, is_fixed, details):
    global bugs_fixed, bugs_remaining
    status = 'FIXED' if is_fixed else 'STILL EXISTS'
    print(f'[{status}] {bug_id}: {bug_name}')
    print(f'        {details}')
    if is_fixed:
        bugs_fixed += 1
    else:
        bugs_remaining += 1
    print()

# 获取测试用token
ts = str(int(time.time()))[-4:]
data = {'username': f'fix{ts}', 'password': 'Test123456', 'confirmPassword': 'Test123456',
        'email': f'fix{ts}@t.com', 'phone': f'1390000{ts}'}
resp = requests.post(f'{BASE_URL}/auth/register', json=data)
user_token = resp.json().get('data', {}).get('token')
headers = {'Authorization': f'Bearer {user_token}'} if user_token else {}

# 创建测试活动
act_data = {'title': 'fix_test', 'category': 'test', 'description': 'test',
            'startTime': '2026-06-15T10:00:00', 'endTime': '2026-06-15T12:00:00',
            'location': 'test', 'organizer': 'test', 'maxCount': 100}
resp = requests.post(f'{BASE_URL}/activities', json=act_data, headers=headers)
activity_id = resp.json().get('data', {}).get('id')

print('=' * 40)
print('验证8个BUG的修复状态')
print('=' * 40)
print()

# ============ BUG-1: 登录频率限制 ============
print('--- 测试 BUG-1: 登录频率限制 ---')
blocked = False
block_msg = ''
for i in range(10):
    resp = requests.post(f'{BASE_URL}/auth/login', json={'username': 'admin', 'password': 'wrong'})
    msg = resp.json().get('message', '')
    # 检测各种可能的限制响应
    if (resp.status_code == 429 or
        resp.status_code == 403 or
        '锁定' in msg or '限制' in msg or '尝试' in msg or
        '次数' in msg or '频繁' in msg or 'too many' in msg.lower()):
        blocked = True
        block_msg = f'第{i+1}次被拦截: status={resp.status_code}, msg={msg}'
        break
check_bug('BUG-1', '登录频率限制', blocked,
          block_msg if blocked else '10次错误密码登录均未被限制')

# ============ BUG-2: 禁用用户后token失效 ============
print('--- 测试 BUG-2: 禁用用户后token失效 ---')
# 用当前token访问应该成功
resp1 = requests.get(f'{BASE_URL}/activities', headers=headers)
token_works_before = resp1.json().get('code') == 200

# 尝试获取当前用户ID并禁用（需要管理员权限，这里模拟检测逻辑）
# 实际测试：如果token有效但用户被禁用，应该返回401/403
# 我们通过检查是否有用户状态校验来判断
resp2 = requests.get(f'{BASE_URL}/users/me', headers=headers) if user_token else None
has_user_status_check = resp2 is not None and resp2.status_code in [401, 403, 404]

# 更直接的检测：查看JwtAuthenticationFilter是否检查用户状态
# 如果修复了，即使token有效，被禁用用户也会被拒绝
# 这里我们只能检测当前行为，实际修复需要代码审查
check_bug('BUG-2', '禁用用户后token失效', False,
          '需要代码审查JwtAuthenticationFilter是否添加用户状态检查')

# ============ BUG-3: XSS注入 ============
print('--- 测试 BUG-3: XSS注入防护 ---')
xss_data = {'title': '<script>alert(1)</script>', 'category': 'test', 'description': 'test',
            'startTime': '2026-06-15T10:00:00', 'endTime': '2026-06-15T12:00:00',
            'location': 'test', 'organizer': 'test'}
resp = requests.post(f'{BASE_URL}/activities', json=xss_data, headers=headers)
title = resp.json().get('data', {}).get('title', '') if resp.json().get('data') else ''
xss_fixed = '<script>' not in title and '&lt;' in title
check_bug('BUG-3', 'XSS注入防护', xss_fixed,
          f'返回标题: "{title}"' + (' (已转义)' if xss_fixed else ' (未转义，仍可注入)'))

# ============ BUG-4: 非管理员审核活动 ============
print('--- 测试 BUG-4: 非管理员审核活动 ---')
if activity_id:
    resp = requests.put(f'{BASE_URL}/activities/{activity_id}/audit?action=approve', headers=headers)
    audit_rejected = resp.status_code in [401, 403] or resp.json().get('code') in [401, 403]
    check_bug('BUG-4', '非管理员审核活动', audit_rejected,
              f'status={resp.status_code}, code={resp.json().get("code")}, msg={resp.json().get("message", "")}')
else:
    check_bug('BUG-4', '非管理员审核活动', False, '无测试活动ID')

# ============ BUG-5: 删除他人活动 ============
print('--- 测试 BUG-5: 删除他人活动 ---')
# 创建一个新活动用于删除测试
act_data2 = {'title': 'delete_test', 'category': 'test', 'description': 'test',
             'startTime': '2026-06-15T10:00:00', 'endTime': '2026-06-15T12:00:00',
             'location': 'test', 'organizer': 'test', 'maxCount': 10}
resp = requests.post(f'{BASE_URL}/activities', json=act_data2, headers=headers)
del_activity_id = resp.json().get('data', {}).get('id')
if del_activity_id:
    resp = requests.delete(f'{BASE_URL}/activities/{del_activity_id}', headers=headers)
    delete_rejected = resp.status_code in [401, 403] or resp.json().get('code') in [401, 403]
    check_bug('BUG-5', '删除活动权限检查', delete_rejected,
              f'status={resp.status_code}, code={resp.json().get("code")}')
else:
    check_bug('BUG-5', '删除活动权限检查', False, '无法创建测试活动')

# ============ BUG-6: 普通用户查看用户列表 ============
print('--- 测试 BUG-6: 普通用户查看用户列表 ---')
resp = requests.get(f'{BASE_URL}/users', headers=headers)
users_rejected = resp.status_code in [401, 403] or resp.json().get('code') in [401, 403]
check_bug('BUG-6', '普通用户查看用户列表', users_rejected,
          f'status={resp.status_code}, code={resp.json().get("code")}, 用户数={len(resp.json().get("data", []))}')

# ============ BUG-7: 无效审核操作 ============
print('--- 测试 BUG-7: 无效审核操作 ---')
if activity_id:
    resp = requests.put(f'{BASE_URL}/activities/{activity_id}/audit?action=invalid_action', headers=headers)
    invalid_rejected = resp.status_code == 400 or resp.json().get('code') == 400
    check_bug('BUG-7', '无效审核操作', invalid_rejected,
              f'status={resp.status_code}, code={resp.json().get("code")}, msg={resp.json().get("message", "")}')
else:
    check_bug('BUG-7', '无效审核操作', False, '无测试活动ID')

# ============ BUG-8: chunk_text无限循环 ============
print('--- 测试 BUG-8: chunk_text无限循环 ---')
print('    需要代码审查或单元测试验证')
print('    检查campus-rag/main.py中chunk_text函数是否有参数验证')
check_bug('BUG-8', 'chunk_text无限循环', False,
          '需要代码审查main.py是否添加overlap < chunk_size验证')

# ============ 汇总 ============
print('=' * 60)
print('修复验证汇总')
print('=' * 60)
print(f'已修复: {bugs_fixed}')
print(f'未修复: {bugs_remaining}')
print(f'总计: {bugs_fixed + bugs_remaining}')
print()

if bugs_fixed > 0:
    print('已修复的BUG:')
    print('  重新运行测试应该显示为PASS')
print()
print('=' * 60)
