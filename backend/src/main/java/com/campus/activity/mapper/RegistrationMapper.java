package com.campus.activity.mapper;

import com.campus.activity.entity.Registration;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface RegistrationMapper {

    @Insert("INSERT INTO registration(user_id, activity_id, status) VALUES(#{userId}, #{activityId}, #{status})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Registration registration);

    @Update("UPDATE registration SET status=#{status} WHERE id=#{id}")
    int updateStatus(@Param("id") Long id, @Param("status") String status);

    @Select("SELECT * FROM registration WHERE user_id=#{userId} ORDER BY registered_at DESC")
    List<Registration> findByUserId(Long userId);

    @Select("SELECT * FROM registration WHERE activity_id=#{activityId}")
    List<Registration> findByActivityId(Long activityId);

    @Select("SELECT * FROM registration WHERE user_id=#{userId} AND activity_id=#{activityId} AND status IN ('registered', 'checked_in', 'completed')")
    Registration findActiveByUserAndActivity(@Param("userId") Long userId, @Param("activityId") Long activityId);

    @Select("SELECT * FROM registration WHERE user_id=#{userId} AND activity_id=#{activityId} AND status='cancelled'")
    Registration findCancelledByUserAndActivity(@Param("userId") Long userId, @Param("activityId") Long activityId);

    @Update("UPDATE registration SET status=#{status}, registered_at=NOW() WHERE id=#{id}")
    int reactivate(@Param("id") Long id, @Param("status") String status);
}
