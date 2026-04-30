package com.campus.activity.controller;

import com.campus.activity.common.Result;
import com.campus.activity.dto.ActivityDTO;
import com.campus.activity.entity.Activity;
import com.campus.activity.service.ActivityService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/activities")
@RequiredArgsConstructor
public class ActivityController {

    private final ActivityService activityService;

    @GetMapping
    public Result<List<Activity>> list(@RequestParam(required = false) String status) {
        List<Activity> list;
        if (status != null && !status.isEmpty()) {
            list = activityService.findByStatus(status);
        } else {
            list = activityService.findAll();
        }
        return Result.success(list);
    }

    @GetMapping("/{id}")
    public Result<Activity> detail(@PathVariable Long id) {
        Activity activity = activityService.findById(id);
        if (activity == null) {
            return Result.error("活动不存在");
        }
        return Result.success(activity);
    }

    @PostMapping
    public Result<Activity> create(@Valid @RequestBody ActivityDTO dto, Authentication authentication) {
        Long userId = (Long) authentication.getPrincipal();
        Activity activity = activityService.create(dto, userId);
        return Result.success(activity);
    }

    @PutMapping("/{id}/audit")
    public Result<Void> audit(@PathVariable Long id, @RequestParam String action,
                              @RequestParam(required = false) String comment,
                              Authentication authentication) {
        Long auditUserId = (Long) authentication.getPrincipal();
        String status = "approve".equals(action) ? "published" : "rejected";
        activityService.audit(id, status, auditUserId, comment);
        return Result.success();
    }

    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) {
        activityService.deleteById(id);
        return Result.success();
    }
}
