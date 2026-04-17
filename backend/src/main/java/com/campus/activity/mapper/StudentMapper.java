package com.campus.activity.mapper;

import com.campus.activity.entity.Student;
import org.apache.ibatis.annotations.*;

@Mapper
public interface StudentMapper {
    @Select("SELECT id, student_no AS studentNo, name, age, gender, college_code AS collegeCode, major_code AS majorCode, class_no AS classNo, enrollment_year AS enrollmentYear, user_id AS userId, create_time AS createTime, update_time AS updateTime FROM student WHERE student_no = #{studentNo}")
    Student findByStudentNo(String studentNo);
}