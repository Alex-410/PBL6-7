package com.campus.activity.controller;

import com.campus.activity.common.Result;
import com.campus.activity.service.UserService;
import com.campus.activity.vo.UserVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public Result<List<UserVO>> list(@RequestParam(required = false) String role) {
        List<UserVO> users;
        if (role != null && !role.isEmpty()) {
            users = userService.findByRole(role);
        } else {
            users = userService.findAll();
        }
        return Result.success(users);
    }

    @GetMapping("/{id}")
    public Result<UserVO> detail(@PathVariable Long id) {
        UserVO user = userService.findById(id);
        if (user == null) {
            return Result.error("用户不存在");
        }
        return Result.success(user);
    }

    @PutMapping("/{id}/status")
    public Result<Void> updateStatus(@PathVariable Long id, @RequestBody Map<String, Object> body) {
        Integer status = (Integer) body.get("status");
        if (status == null) {
            return Result.error("状态不能为空");
        }
        userService.updateStatus(id, status);
        return Result.success();
    }

    @PutMapping("/{id}/role")
    public Result<Void> updateRole(@PathVariable Long id, @RequestBody Map<String, String> body) {
        String role = body.get("role");
        if (role == null || role.isEmpty()) {
            return Result.error("角色不能为空");
        }
        String error = userService.updateRole(id, role);
        if (error != null) {
            return Result.error(error);
        }
        return Result.success();
    }
}
