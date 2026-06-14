package com.campus.activity.controller;

import com.campus.activity.common.Result;
import com.campus.activity.service.AiProxyService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * AI 代理接口。
 * <p>
 * 路径 /api/ai/** 不在 permitAll() 列表内，默认走 JWT 校验，
 * 密钥在服务端注入，前端无需也无法接触到。
 */
@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiProxyService aiProxyService;

    @PostMapping("/chat")
    public Result<Map<String, Object>> chat(@RequestBody Map<String, Object> body,
                                            Authentication authentication) {
        // principal 为登录时写入的 userId（Long），此处保留以备后续做用户级限流/审计
        Long userId = (Long) authentication.getPrincipal();
        try {
            Map<String, Object> resp = aiProxyService.chat(body);
            return Result.success(resp);
        } catch (Exception e) {
            return Result.error("AI 服务暂不可用：" + e.getMessage());
        }
    }
}
