package com.campus.activity.mapper;

import com.campus.activity.entity.Student;
import org.apache.ibatis.annotations.*;

@Mapper
public interface StudentMapper {
    @Select("SELECT id, student_no AS studentNo, name, age, gender, college_name AS collegeName, club, major_name AS majorName, class_no AS classNo, enrollment_year AS enrollmentYear, grade, user_id AS userId, create_time AS createTime, update_time AS updateTime FROM student WHERE student_no = #{studentNo}")
    Student findByStudentNo(String studentNo);
}