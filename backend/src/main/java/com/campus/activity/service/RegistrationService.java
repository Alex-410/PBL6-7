package com.campus.activity.service;

import com.campus.activity.entity.Activity;
import com.campus.activity.entity.Registration;
import com.campus.activity.entity.Student;
import com.campus.activity.entity.User;
import com.campus.activity.mapper.RegistrationMapper;
import com.campus.activity.mapper.StudentMapper;
import com.campus.activity.mapper.UserMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class RegistrationService {

    private final RegistrationMapper registrationMapper;
    private final ActivityService activityService;
    private final StudentMapper studentMapper;
    private final UserMapper userMapper;

    @Transactional
    public Registration register(Long userId, Long activityId) {
        Registration existing = registrationMapper.findActiveByUserAndActivity(userId, activityId);
        if (existing != null) {
            throw new RuntimeException("你已报名该活动");
        }

        Activity activity = activityService.findById(activityId);
        if (activity == null) {
            throw new RuntimeException("活动不存在");
        }
        if (!"published".equals(activity.getStatus())) {
            throw new RuntimeException("该活动暂不可报名");
        }
        if (activity.getRegisteredCount() >= activity.getMaxCount()) {
            throw new RuntimeException("报名人数已满");
        }

        checkRegistrationRestriction(userId, activity);

        Registration cancelled = registrationMapper.findCancelledByUserAndActivity(userId, activityId);
        if (cancelled != null) {
            registrationMapper.reactivate(cancelled.getId(), "registered");
            activityService.updateRegisteredCount(activityId, 1);
            cancelled.setStatus("registered");
            return cancelled;
        }

        Registration reg = new Registration();
        reg.setUserId(userId);
        reg.setActivityId(activityId);
        reg.setStatus("registered");

        registrationMapper.insert(reg);
        activityService.updateRegisteredCount(activityId, 1);

        return reg;
    }

    @Transactional
    public void cancel(Long registrationId, Long userId) {
        List<Registration> regs = registrationMapper.findByUserId(userId);
        Registration target = regs.stream().filter(r -> r.getId().equals(registrationId)).findFirst()
                .orElseThrow(() -> new RuntimeException("报名记录不存在"));

        if (!"registered".equals(target.getStatus())) {
            throw new RuntimeException("当前状态不可取消");
        }

        registrationMapper.updateStatus(registrationId, "cancelled");
        activityService.updateRegisteredCount(target.getActivityId(), -1);
    }

    public List<Registration> findByUserId(Long userId) {
        return registrationMapper.findByUserId(userId);
    }

    public List<Registration> findByActivityId(Long activityId) {
        return registrationMapper.findByActivityId(activityId);
    }

    private void checkRegistrationRestriction(Long userId, Activity activity) {
        String limitType = activity.getRegistrationLimitType();
        if (limitType == null || "none".equals(limitType)) {
            return;
        }

        User user = userMapper.findById(userId);
        if (user == null) {
            throw new RuntimeException("用户不存在");
        }

        Student student = studentMapper.findByStudentNo(user.getUsername());

        if ("college".equals(limitType)) {
            String allowedCollege = activity.getRegistrationLimitValue();
            if (allowedCollege == null || allowedCollege.isEmpty()) {
                return;
            }
            String userCollege = student != null ? student.getCollegeName() : null;
            if (userCollege == null || !userCollege.equals(allowedCollege)) {
                throw new RuntimeException("该活动仅限【" + allowedCollege + "】报名");
            }
        } else if ("club".equals(limitType)) {
            String allowedClub = activity.getRegistrationLimitValue();
            if (allowedClub == null || allowedClub.isEmpty()) {
                return;
            }
            String userClub = student != null ? student.getClub() : user.getClub();
            if (userClub == null || !userClub.equals(allowedClub)) {
                throw new RuntimeException("该活动仅限【" + allowedClub + "】报名");
            }
        }
    }
}
