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
    private String collegeName;
    private String majorName;
    private String classNo;
    private String enrollmentYear;
    private String grade;
    private Long userId;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}