package com.campus.activity.service;

import com.campus.activity.dto.ActivityDTO;
import com.campus.activity.entity.Activity;
import com.campus.activity.mapper.ActivityMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ActivityService {

    private final ActivityMapper activityMapper;

    @Transactional
    public Activity create(ActivityDTO dto, Long userId) {
        Activity activity = new Activity();
        activity.setTitle(dto.getTitle());
        activity.setCategory(dto.getCategory());
        activity.setDescription(dto.getDescription());
        activity.setStartTime(dto.getStartTime());
        activity.setEndTime(dto.getEndTime());
        activity.setLocation(dto.getLocation());
        activity.setOrganizer(dto.getOrganizer());
        activity.setPoster(dto.getPoster());
        activity.setMaxCount(dto.getMaxCount() != null ? dto.getMaxCount() : 0);
        activity.setRegisteredCount(0);
        activity.setFee(dto.getFee() != null ? dto.getFee() : BigDecimal.ZERO);
        activity.setStatus("pending");
        activity.setUserId(userId);
        activity.setHasBonus(dto.getHasBonus() != null ? dto.getHasBonus() : false);
        activity.setBonusType(dto.getBonusType());
        activity.setBonusValue(dto.getBonusValue());
        activity.setCollege(dto.getCollege());
        activity.setClub(dto.getClub());
        activity.setTags(dto.getTags());
        activity.setRegistrationLimitType(dto.getRegistrationLimitType() != null ? dto.getRegistrationLimitType() : "none");
        activity.setRegistrationLimitValue(dto.getRegistrationLimitValue());

        activityMapper.insert(activity);
        return activity;
    }

    @Transactional
    public void audit(Long activityId, String status, Long auditUserId, String auditComment) {
        activityMapper.audit(activityId, status, auditUserId, auditComment);
    }

    @Transactional
    public void updateRegisteredCount(Long activityId, int delta) {
        activityMapper.updateRegisteredCount(activityId, delta);
    }

    public Activity findById(Long id) {
        return activityMapper.findById(id);
    }

    public List<Activity> findAll() {
        return activityMapper.findAll();
    }

    public List<Activity> findByUserId(Long userId) {
        return activityMapper.findByUserId(userId);
    }

    public List<Activity> findByStatus(String status) {
        return activityMapper.findByStatus(status);
    }

    @Transactional
    public void deleteById(Long id) {
        activityMapper.deleteById(id);
    }
}
