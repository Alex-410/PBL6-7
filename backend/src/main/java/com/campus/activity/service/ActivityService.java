package com.campus.activity.service;

import com.campus.activity.dto.ActivityDTO;
import com.campus.activity.entity.Activity;
import com.campus.activity.mapper.ActivityMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.util.HtmlUtils;

import java.math.BigDecimal;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ActivityService {

    private final ActivityMapper activityMapper;

    /** 转义用户输入中的 HTML 特殊字符，防止 XSS。null 原样返回。 */
    private static String esc(String s) {
        return s == null ? null : HtmlUtils.htmlEscape(s);
    }

    @Transactional
    public Activity create(ActivityDTO dto, Long userId) {
        Activity activity = new Activity();
        activity.setTitle(esc(dto.getTitle()));
        activity.setCategory(esc(dto.getCategory()));
        activity.setDescription(esc(dto.getDescription()));
        activity.setStartTime(dto.getStartTime());
        activity.setEndTime(dto.getEndTime());
        activity.setLocation(esc(dto.getLocation()));
        activity.setOrganizer(esc(dto.getOrganizer()));
        activity.setPoster(dto.getPoster());
        activity.setMaxCount(dto.getMaxCount() != null ? dto.getMaxCount() : 0);
        activity.setRegisteredCount(0);
        activity.setFee(dto.getFee() != null ? dto.getFee() : BigDecimal.ZERO);
        activity.setStatus("pending");
        activity.setUserId(userId);
        activity.setHasBonus(dto.getHasBonus() != null ? dto.getHasBonus() : false);
        activity.setBonusType(dto.getBonusType());
        activity.setBonusValue(dto.getBonusValue());
        activity.setCollege(esc(dto.getCollege()));
        activity.setClub(esc(dto.getClub()));
        activity.setTags(esc(dto.getTags()));
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
