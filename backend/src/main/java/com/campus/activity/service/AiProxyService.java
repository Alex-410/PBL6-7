package com.campus.activity.service;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

/**
 * AI 代理服务。
 * <p>
 * 接收前端透传的 OpenAI/Ark 风格请求体，注入服务端密钥后转发到火山方舟（豆包），
 * 避免密钥暴露到浏览器。
 */
@Service
@RequiredArgsConstructor
public class AiProxyService {

    private final RestTemplate restTemplate;

    @Value("${ai.ark.base-url}")
    private String baseUrl;

    @Value("${ai.ark.api-key}")
    private String apiKey;

    /**
     * 透传 chat/completions 请求到上游 LLM。
     *
     * @param requestBody 上游约定的请求体（model / messages / temperature 等字段原样转发）
     * @return 上游响应体（包含 choices 等字段）
     */
    public Map<String, Object> chat(Map<String, Object> requestBody) {
        if (apiKey == null || apiKey.isBlank()) {
            throw new IllegalStateException("AI 服务未配置密钥（ARK_API_KEY）");
        }
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(apiKey);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        String url = baseUrl + "/chat/completions";
        try {
            ResponseEntity<Map> resp = restTemplate.postForEntity(url, entity, Map.class);
            if (resp.getStatusCode().is2xxSuccessful() && resp.getBody() != null) {
                return resp.getBody();
            }
            throw new RuntimeException("AI 上游返回 " + resp.getStatusCode());
        } catch (RestClientException e) {
            throw new RuntimeException("调用 AI 服务失败：" + e.getMessage(), e);
        }
    }
}
