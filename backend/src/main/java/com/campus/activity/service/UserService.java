package com.campus.activity.service;

import com.campus.activity.entity.Student;
import com.campus.activity.entity.User;
import com.campus.activity.mapper.ActivityMapper;
import com.campus.activity.mapper.RegistrationMapper;
import com.campus.activity.mapper.StudentMapper;
import com.campus.activity.mapper.UserMapper;
import com.campus.activity.vo.UserVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserMapper userMapper;
    private final StudentMapper studentMapper;
    private final ActivityMapper activityMapper;
    private final RegistrationMapper registrationMapper;

    public List<UserVO> findAll() {
        List<User> users = userMapper.findAll();
        return convertToVOList(users);
    }

    public List<UserVO> findByRole(String role) {
        List<User> users;
        if ("PUBLISHER".equals(role)) {
            users = userMapper.findByRoles(Arrays.asList("PUBLISHER", "STUDENT_PUBLISHER"));
        } else {
            users = userMapper.findByRole(role);
        }
        return convertToVOList(users);
    }

    public UserVO findById(Long id) {
        User user = userMapper.findById(id);
        if (user == null) return null;
        return convertToVO(user);
    }

    public void updateStatus(Long id, Integer status) {
        userMapper.updateStatus(id, status);
    }

    public String updateRole(Long id, String newRole) {
        User user = userMapper.findById(id);
        if (user == null) {
            return "用户不存在";
        }
        String currentRole = user.getRole();
        if ("ADMIN".equals(currentRole)) {
            return "不能修改管理员角色";
        }
        if ("ADMIN".equals(newRole)) {
            return "不能将用户提升为管理员";
        }
        if (!("USER".equals(currentRole) || "STUDENT_PUBLISHER".equals(currentRole) || "PUBLISHER".equals(currentRole))) {
            return "当前角色不支持此操作";
        }
        if (!("USER".equals(newRole) || "STUDENT_PUBLISHER".equals(newRole) || "PUBLISHER".equals(newRole))) {
            return "目标角色无效";
        }
        userMapper.updateRole(id, newRole);
        return null;
    }

    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalUsers", userMapper.countAll());
        stats.put("studentCount", userMapper.countByRoles(Arrays.asList("USER", "STUDENT_PUBLISHER")));
        stats.put("publisherCount", userMapper.countByRoles(Arrays.asList("PUBLISHER", "STUDENT_PUBLISHER")));
        stats.put("adminCount", userMapper.countByRole("ADMIN"));
        stats.put("totalActivities", activityMapper.findAll().size());
        stats.put("publishedActivities", activityMapper.countByStatus("published"));
        stats.put("pendingActivities", activityMapper.countByStatus("pending"));
        stats.put("rejectedActivities", activityMapper.countByStatus("rejected"));
        stats.put("completedActivities", activityMapper.countByStatus("completed"));
        stats.put("totalRegistrations", registrationMapper.countAll());
        stats.put("bonusActivities", activityMapper.countHasBonus());
        stats.put("categoryDistribution", activityMapper.countByCategory());
        stats.put("topActivities", activityMapper.findTopByRegistrationCount(5));
        int sumRegistered = activityMapper.sumRegisteredCountPublished();
        int sumMaxCount = activityMapper.sumMaxCountPublished();
        stats.put("totalRegistered", sumRegistered);
        stats.put("totalCapacity", sumMaxCount);
        return stats;
    }

    private List<UserVO> convertToVOList(List<User> users) {
        List<UserVO> result = new ArrayList<>();
        for (User user : users) {
            result.add(convertToVO(user));
        }
        return result;
    }

    private UserVO convertToVO(User user) {
        UserVO vo = new UserVO();
        vo.setId(user.getId());
        vo.setUsername(user.getUsername());
        vo.setEmail(user.getEmail());
        vo.setPhone(user.getPhone());
        vo.setNickname(user.getNickname());
        vo.setAvatar(user.getAvatar());
        vo.setRole(user.getRole());
        vo.setClub(user.getClub());

        if ("USER".equals(user.getRole()) || "STUDENT_PUBLISHER".equals(user.getRole())) {
            Student student = studentMapper.findByStudentNo(user.getUsername());
            if (student != null) {
                vo.setCollege(student.getCollegeName());
                vo.setGrade(student.getGrade());
                if (vo.getNickname() == null || vo.getNickname().isEmpty()) {
                    vo.setNickname(student.getName());
                }
            }
        }

        return vo;
    }
}
