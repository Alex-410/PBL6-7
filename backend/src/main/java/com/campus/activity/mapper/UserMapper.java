package com.campus.activity.mapper;

import com.campus.activity.entity.User;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface UserMapper {

    @Insert("INSERT INTO user(username, password, email, phone, nickname, role, status, create_time, update_time) VALUES(#{username}, #{password}, #{email}, #{phone}, #{nickname}, #{role}, #{status}, NOW(), NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);

    @Select("SELECT * FROM user WHERE username = #{username}")
    User findByUsername(String username);

    @Select("SELECT * FROM user WHERE email = #{email}")
    User findByEmail(String email);

    @Select("SELECT * FROM user WHERE phone = #{phone}")
    User findByPhone(String phone);

    @Select("SELECT * FROM user WHERE id = #{id}")
    User findById(Long id);

    @Select("SELECT * FROM user ORDER BY create_time DESC")
    List<User> findAll();

    @Select("SELECT * FROM user WHERE role = #{role} ORDER BY create_time DESC")
    List<User> findByRole(String role);

    @Select("<script>SELECT * FROM user WHERE role IN <foreach item='r' collection='roles' open='(' separator=',' close=')'>#{r}</foreach> ORDER BY create_time DESC</script>")
    List<User> findByRoles(@Param("roles") List<String> roles);

    @Select("SELECT COUNT(*) FROM user")
    int countAll();

    @Select("SELECT COUNT(*) FROM user WHERE role = #{role}")
    int countByRole(String role);

    @Select("<script>SELECT COUNT(*) FROM user WHERE role IN <foreach item='r' collection='roles' open='(' separator=',' close=')'>#{r}</foreach></script>")
    int countByRoles(@Param("roles") List<String> roles);

    @Update("UPDATE user SET status = #{status}, update_time = NOW() WHERE id = #{id}")
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    @Update("UPDATE user SET role = #{role}, update_time = NOW() WHERE id = #{id}")
    int updateRole(@Param("id") Long id, @Param("role") String role);
}

