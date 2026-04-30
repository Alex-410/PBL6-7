package com.campus.activity.entity;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class Activity {
    private Long id;
    private String title;
    private String category;
    private String description;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String location;
    private String organizer;
    private String poster;
    private Integer maxCount;
    private Integer registeredCount;
    private BigDecimal fee;
    private String status;
    private Long userId;
    private Boolean hasBonus;
    private String bonusType;
    private BigDecimal bonusValue;
    private String college;
    private String club;
    private String tags;
    private String registrationLimitType;
    private String registrationLimitValue;
    private Long auditUserId;
    private LocalDateTime auditTime;
    private String auditComment;
    private Boolean aiAudited;
    private String aiAuditResult;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}
