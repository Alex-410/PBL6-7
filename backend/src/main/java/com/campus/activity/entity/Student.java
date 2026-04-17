package com.campus.activity.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Student {
    private Long id;
    private String studentNo;
    private String name;
    private Integer age;
    private String gender;
    private String collegeCode;
    private String majorCode;
    private String classNo;
    private String enrollmentYear;
    private Long userId;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}