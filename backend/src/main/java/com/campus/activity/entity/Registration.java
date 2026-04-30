package com.campus.activity.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Registration {
    private Long id;
    private Long userId;
    private Long activityId;
    private String status;
    private LocalDateTime registeredAt;
}
