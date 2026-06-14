package com.campus.activity.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Map;

@RestController
@RequestMapping("/api/rag")
@CrossOrigin
public class RagController {

    @Value("${rag.script.path:../campus-rag/main.py}")
    private String ragScriptPath;

    @Value("${rag.python:python}")
    private String pythonCmd;

    @Value("${rag.port:9001}")
    private int ragPort;

    private static volatile Process ragProcess = null;

    /**
     * 检查 RAG 服务是否在线
     */
    @GetMapping("/check")
    public Map<String, Object> checkRagStatus() {
        boolean online = isRagOnline();
        return Map.of("online", online, "port", ragPort);
    }

    /**
     * 启动 RAG 服务
     */
    @PostMapping("/start")
    public Map<String, Object> startRag() {
        // 先检查是否已在线
        if (isRagOnline()) {
            return Map.of("success", true, "message", "RAG 服务已在运行", "alreadyRunning", true);
        }

        // 检查是否已有进程在启动
        if (ragProcess != null && ragProcess.isAlive()) {
            return Map.of("success", true, "message", "RAG 服务正在启动中", "starting", true);
        }

        try {
            // 解析脚本路径
            File scriptFile = new File(ragScriptPath).getCanonicalFile();
            if (!scriptFile.exists()) {
                return Map.of("success", false, "message", "RAG 脚本不存在: " + scriptFile.getAbsolutePath());
            }

            File workDir = scriptFile.getParentFile();

            // 启动进程
            ProcessBuilder pb = new ProcessBuilder(pythonCmd, scriptFile.getName());
            pb.directory(workDir);
            pb.redirectErrorStream(true);

            // 将输出重定向到文件，避免阻塞
            File logFile = new File(workDir, "rag_server.log");
            pb.redirectOutput(ProcessBuilder.Redirect.appendTo(logFile));

            ragProcess = pb.start();

            return Map.of(
                "success", true,
                "message", "RAG 服务启动中",
                "pid", ragProcess.pid(),
                "logFile", logFile.getAbsolutePath()
            );
        } catch (Exception e) {
            return Map.of("success", false, "message", "启动失败: " + e.getMessage());
        }
    }

    /**
     * 停止 RAG 服务
     */
    @PostMapping("/stop")
    public Map<String, Object> stopRag() {
        if (ragProcess != null && ragProcess.isAlive()) {
            ragProcess.destroyForcibly();
            ragProcess = null;
            return Map.of("success", true, "message", "RAG 服务已停止");
        }
        return Map.of("success", false, "message", "RAG 服务未在运行");
    }

    private boolean isRagOnline() {
        try {
            URL url = new URL("http://localhost:" + ragPort + "/api/rag/status/");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(2000);
            conn.setReadTimeout(2000);
            int code = conn.getResponseCode();
            conn.disconnect();
            return code == 200;
        } catch (Exception e) {
            return false;
        }
    }
}
