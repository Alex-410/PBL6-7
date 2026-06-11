package com.campus.activity.service;

import com.campus.activity.dto.LoginDTO;
import com.campus.activity.dto.RegisterDTO;
import com.campus.activity.entity.Student;
import com.campus.activity.entity.User;
import com.campus.activity.mapper.StudentMapper;
import com.campus.activity.mapper.UserMapper;
import com.campus.activity.utils.JwtUtil;
import com.campus.activity.vo.UserVO;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.ConcurrentHashMap;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserMapper userMapper;
    private final StudentMapper studentMapper;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    private static final int MAX_LOGIN_ATTEMPTS = 5;
    private static final long LOCK_TIME_MS = 15 * 60 * 1000;
    private final ConcurrentHashMap<String, long[]> loginAttempts = new ConcurrentHashMap<>();

    @Transactional
    public UserVO register(RegisterDTO registerDTO) {
        if (!registerDTO.getPassword().equals(registerDTO.getConfirmPassword())) {
            throw new RuntimeException("两次输入的密码不一致");
        }

        if (userMapper.findByUsername(registerDTO.getUsername()) != null) {
            throw new RuntimeException("用户名已存在");
        }

        if (userMapper.findByEmail(registerDTO.getEmail()) != null) {
            throw new RuntimeException("邮箱已被注册");
        }

        if (userMapper.findByPhone(registerDTO.getPhone()) != null) {
            throw new RuntimeException("手机号已被注册");
        }

        User user = new User();
        user.setUsername(registerDTO.getUsername());
        user.setPassword(passwordEncoder.encode(registerDTO.getPassword()));
        user.setEmail(registerDTO.getEmail());
        user.setPhone(registerDTO.getPhone());
        user.setNickname(registerDTO.getUsername());
        user.setRole("USER");
        user.setStatus(1);

        userMapper.insert(user);

        String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole());

        return convertToVO(user, token);
    }

    public UserVO login(LoginDTO loginDTO) {
        checkLoginRateLimit(loginDTO.getUsername());
        Student student = studentMapper.findByStudentNo(loginDTO.getUsername());

        if (student != null) {
            String expectedPassword = student.getStudentNo().substring(student.getStudentNo().length() - 6);
            if (!loginDTO.getPassword().equals(expectedPassword)) {
                recordLoginFailure(loginDTO.getUsername());
                throw new RuntimeException("学号或密码错误");
            }

            User user = userMapper.findByUsername(student.getStudentNo());
            if (user == null) {
                user = new User();
                user.setUsername(student.getStudentNo());
                user.setPassword(passwordEncoder.encode(expectedPassword));
                user.setNickname(student.getName());
                user.setRole("USER");
                user.setStatus(1);
                userMapper.insert(user);
            }

            if (user.getStatus() == 0) {
                throw new RuntimeException("账号已被禁用");
            }

            String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole());
            UserVO userVO = convertToVO(user, token);
            userVO.setCollege(student.getCollegeName());
            userVO.setClub(student.getClub());
            userVO.setGrade(student.getGrade());
            resetLoginAttempts(loginDTO.getUsername());
            return userVO;
        }

        User user = userMapper.findByUsername(loginDTO.getUsername());
        if (user == null) {
            recordLoginFailure(loginDTO.getUsername());
            throw new RuntimeException("用户名或学号不存在");
        }

        if (!passwordEncoder.matches(loginDTO.getPassword(), user.getPassword())) {
            recordLoginFailure(loginDTO.getUsername());
            throw new RuntimeException("用户名或密码错误");
        }

        if (user.getStatus() == 0) {
            throw new RuntimeException("账号已被禁用");
        }

        String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole());
        resetLoginAttempts(loginDTO.getUsername());
        return convertToVO(user, token);
    }

    private UserVO convertToVO(User user, String token) {
        UserVO userVO = new UserVO();
        userVO.setId(user.getId());
        userVO.setUsername(user.getUsername());
        userVO.setEmail(user.getEmail());
        userVO.setPhone(user.getPhone());
        userVO.setNickname(user.getNickname());
        userVO.setAvatar(user.getAvatar());
        userVO.setRole(user.getRole());
        userVO.setClub(user.getClub());
        userVO.setToken(token);
        return userVO;
    }

    private void checkLoginRateLimit(String username) {
        long[] record = loginAttempts.get(username);
        if (record != null) {
            long elapsed = System.currentTimeMillis() - record[1];
            if ((int) record[0] >= MAX_LOGIN_ATTEMPTS && elapsed < LOCK_TIME_MS) {
                long waitMinutes = (LOCK_TIME_MS - elapsed) / 60000 + 1;
                throw new RuntimeException("登录尝试次数过多，请" + waitMinutes + "分钟后重试");
            }
            if (elapsed >= LOCK_TIME_MS) {
                loginAttempts.remove(username);
            }
        }
    }

    private void recordLoginFailure(String username) {
        loginAttempts.compute(username, (k, v) -> {
            if (v == null) {
                return new long[]{1, System.currentTimeMillis()};
            }
            v[0]++;
            return v;
        });
    }

    private void resetLoginAttempts(String username) {
        loginAttempts.remove(username);
    }
}

