package com.campus.activity.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class ActivityDTO {
    private Long id;

    @NotBlank(message = "活动标题不能为空")
    private String title;

    private String category;

    private String description;

    @NotNull(message = "开始时间不能为空")
    private LocalDateTime startTime;

    @NotNull(message = "结束时间不能为空")
    private LocalDateTime endTime;

    @NotBlank(message = "活动地点不能为空")
    private String location;

    private String organizer;

    private String poster;

    private Integer maxCount;

    private BigDecimal fee;

    private Boolean hasBonus;

    private String bonusType;

    private BigDecimal bonusValue;

    private String college;
    private String club;
    private String tags;
    private String registrationLimitType;
    private String registrationLimitValue;
}
