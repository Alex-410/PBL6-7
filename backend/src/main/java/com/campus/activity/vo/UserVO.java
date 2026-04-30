package com.campus.activity.vo;

import lombok.Data;

@Data
public class UserVO {
    private Long id;
    private String username;
    private String email;
    private String phone;
    private String nickname;
    private String avatar;
    private String role;
    private String token;
    private String college;
    private String club;
    private String grade;
}
