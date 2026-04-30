package com.campus.activity.controller;

import com.campus.activity.common.Result;
import com.campus.activity.entity.Registration;
import com.campus.activity.service.RegistrationService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/registrations")
@RequiredArgsConstructor
public class RegistrationController {

    private final RegistrationService registrationService;

    @PostMapping
    public Result<Registration> register(@RequestParam Long activityId, Authentication authentication) {
        Long userId = (Long) authentication.getPrincipal();
        Registration reg = registrationService.register(userId, activityId);
        return Result.success(reg);
    }

    @DeleteMapping("/{id}")
    public Result<Void> cancel(@PathVariable Long id, Authentication authentication) {
        Long userId = (Long) authentication.getPrincipal();
        registrationService.cancel(id, userId);
        return Result.success();
    }

    @GetMapping("/me")
    public Result<List<Registration>> myRegistrations(Authentication authentication) {
        Long userId = (Long) authentication.getPrincipal();
        return Result.success(registrationService.findByUserId(userId));
    }

    @GetMapping("/activity/{activityId}")
    public Result<List<Registration>> byActivity(@PathVariable Long activityId) {
        return Result.success(registrationService.findByActivityId(activityId));
    }
}
