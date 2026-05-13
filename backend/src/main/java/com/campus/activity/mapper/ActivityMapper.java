package com.campus.activity.mapper;

import com.campus.activity.entity.Activity;
import org.apache.ibatis.annotations.*;

import java.util.List;
import java.util.Map;

@Mapper
public interface ActivityMapper {

    @Insert("INSERT INTO activity(title, category, description, start_time, end_time, location, organizer, poster, max_count, registered_count, fee, status, user_id, has_bonus, bonus_type, bonus_value, college, club, tags, registration_limit_type, registration_limit_value, ai_audited) VALUES(#{title}, #{category}, #{description}, #{startTime}, #{endTime}, #{location}, #{organizer}, #{poster}, #{maxCount}, #{registeredCount}, #{fee}, #{status}, #{userId}, #{hasBonus}, #{bonusType}, #{bonusValue}, #{college}, #{club}, #{tags}, #{registrationLimitType}, #{registrationLimitValue}, 0)")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Activity activity);

    @Update("UPDATE activity SET title=#{title}, category=#{category}, description=#{description}, start_time=#{startTime}, end_time=#{endTime}, location=#{location}, organizer=#{organizer}, poster=#{poster}, max_count=#{maxCount}, fee=#{fee}, has_bonus=#{hasBonus}, bonus_type=#{bonusType}, bonus_value=#{bonusValue}, college=#{college}, tags=#{tags} WHERE id=#{id}")
    int update(Activity activity);

    @Update("UPDATE activity SET status=#{status}, audit_user_id=#{auditUserId}, audit_time=NOW(), audit_comment=#{auditComment} WHERE id=#{id}")
    int audit(@Param("id") Long id, @Param("status") String status, @Param("auditUserId") Long auditUserId, @Param("auditComment") String auditComment);

    @Update("UPDATE activity SET registered_count=registered_count+#{delta} WHERE id=#{id}")
    int updateRegisteredCount(@Param("id") Long id, @Param("delta") int delta);

    @Delete("DELETE FROM activity WHERE id=#{id}")
    int deleteById(Long id);

    @Select("SELECT * FROM activity WHERE id=#{id}")
    Activity findById(Long id);

    @Select("SELECT * FROM activity ORDER BY create_time DESC")
    List<Activity> findAll();

    @Select("SELECT * FROM activity WHERE user_id=#{userId} ORDER BY create_time DESC")
    List<Activity> findByUserId(Long userId);

    @Select("SELECT * FROM activity WHERE status=#{status} ORDER BY create_time DESC")
    List<Activity> findByStatus(String status);

    @Select("SELECT COUNT(*) FROM activity WHERE status = #{status}")
    int countByStatus(String status);

    @Select("SELECT COUNT(*) FROM activity WHERE has_bonus = true")
    int countHasBonus();

    @Select("SELECT category, COUNT(*) AS count FROM activity GROUP BY category ORDER BY count DESC")
    List<Map<String, Object>> countByCategory();

    @Select("SELECT * FROM activity ORDER BY registered_count DESC LIMIT #{limit}")
    List<Activity> findTopByRegistrationCount(int limit);

    @Select("SELECT COALESCE(SUM(registered_count), 0) FROM activity WHERE status = 'published'")
    int sumRegisteredCountPublished();

    @Select("SELECT COALESCE(SUM(max_count), 0) FROM activity WHERE status = 'published'")
    int sumMaxCountPublished();
}
