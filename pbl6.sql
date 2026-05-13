/*
Navicat MySQL Data Transfer

Source Server         : 1
Source Server Version : 80040
Source Host           : localhost:3306
Source Database       : pbl6

Target Server Type    : MYSQL
Target Server Version : 80040
File Encoding         : 65001

Date: 2026-05-13 21:55:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `activity`
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `max_count` int NOT NULL DEFAULT '0',
  `registered_count` int NOT NULL DEFAULT '0',
  `fee` decimal(10,2) NOT NULL DEFAULT '0.00',
  `has_bonus` tinyint(1) NOT NULL DEFAULT '0',
  `bonus_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bonus_value` decimal(10,2) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `organizer` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `college` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `club` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tags` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `registration_limit_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'none',
  `registration_limit_value` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `poster` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  `audit_user_id` bigint DEFAULT NULL,
  `audit_time` datetime DEFAULT NULL,
  `audit_comment` text COLLATE utf8mb4_unicode_ci,
  `ai_audited` tinyint(1) NOT NULL,
  `ai_audit_result` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `audit_user_id` (`audit_user_id`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `activity_ibfk_2` FOREIGN KEY (`audit_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of activity
-- ----------------------------
INSERT INTO `activity` VALUES ('1', '人工智能前沿技术分享会', '学术', '邀请校内外AI领域专家，分享大模型、多模态、具身智能等前沿方向的最新进展。', '200', '155', '0.00', '1', '综测加分', '0.50', '2026-05-10 14:00:00', '2026-05-10 17:00:00', '图书馆学术报告厅A301', '计算机学院', '计算机学院', '计算机学院', 'AI,大模型,技术', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('2', '第二十届校园歌手大赛', '文艺', '一年一度的校园歌手大赛海选正式开启！', '500', '342', '0.00', '1', '二课学分', '1.00', '2026-05-15 18:30:00', '2026-05-15 21:30:00', '大学生活动中心剧场', '校团委', '校团委', '校团委', '歌唱,比赛,海选', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('3', '院际篮球友谊赛', '体育', '计算机学院 vs 电子工程学院篮球友谊赛。', '300', '88', '0.00', '0', null, null, '2026-05-08 15:00:00', '2026-05-08 17:30:00', '北区体育馆篮球场', '体育部', '体育部', '体育部', '篮球,友谊赛,体育', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('4', '敬老院关爱志愿活动', '公益', '前往阳光敬老院开展志愿服务。', '30', '27', '0.00', '1', '志愿时长', '4.00', '2026-05-11 08:30:00', '2026-05-11 12:00:00', '阳光敬老院（校车接送）', '青年志愿者协会', '青年志愿者协会', '青年志愿者协会', '志愿,敬老,公益', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('5', '创业经验分享沙龙', '就业', '邀请三位成功创业的校友回到母校，分享创业历程。', '80', '13', '0.00', '1', '综测加分', '0.30', '2026-05-18 14:00:00', '2026-05-18 16:30:00', '创新创业中心208室', '创业学院', '创业学院', '创业学院', '创业,校友,分享', 'none', null, null, null, 'published', '1', '1', '2026-05-01 00:54:14', null, '0', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('6', '手机摄影技巧工坊', '文艺', '零基础也能拍大片！专业摄影师带你掌握手机构图技巧。', '40', '38', '10.00', '0', null, null, '2026-05-12 19:00:00', '2026-05-12 21:00:00', '艺术楼多媒体教室B201', '艺术学院', '艺术学院', '艺术学院', '摄影,工坊,手机', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('7', 'English Corner Weekly', '社交', '每周三晚的英语角活动！', '50', '23', '0.00', '0', null, null, '2026-05-07 19:00:00', '2026-05-07 21:00:00', '外语楼一楼大厅', '外国语学院', '外国语学院', '外国语学院', '英语,口语,社交', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('8', '大学生心理健康讲座', '讲座', '心理咨询中心特邀专家开展主题讲座。', '300', '167', '0.00', '1', '综测加分', '0.20', '2026-05-09 14:00:00', '2026-05-09 16:00:00', '综合楼学术报告厅', '学生处', '学生处', '学生处', '心理,健康,讲座', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('9', '48小时编程马拉松', '学术', 'HackCampus 2026春季编程马拉松！', '120', '77', '0.00', '1', '综测加分', '1.50', '2026-05-20 18:00:00', '2026-05-22 18:00:00', '工程训练中心三楼', '计算机学院', '计算机学院', '计算机学院', '编程,马拉松,比赛', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('10', '2026迎新晚会', '文艺', '欢迎2026级新生的盛大晚会！', '800', '756', '0.00', '0', null, null, '2026-03-01 19:00:00', '2026-03-01 22:00:00', '大学生活动中心剧场', '校学生会', '校学生会', '校学生会', '迎新,晚会', 'none', null, null, null, 'completed', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('11', '读书分享会', '学术', '本月共读书目《人类简史》。', '25', '18', '0.00', '0', null, null, '2026-05-14 19:00:00', '2026-05-14 21:00:00', '图书馆研讨室305', '图书馆', '图书馆', '图书馆', '读书,分享,人文', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('12', '瑜伽入门体验课', '体育', '专业瑜伽老师带你体验基础瑜伽。', '20', '20', '15.00', '0', null, null, '2026-05-13 18:00:00', '2026-05-13 19:30:00', '体育馆二楼舞蹈房', '体育部', '体育部', '体育部', '瑜伽,体验,健身', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('13', '校园环保快闪行动', '公益', '响应世界环境日，发起校园环保快闪。', '100', '0', '0.00', '1', '志愿时长', '2.00', '2026-06-05 10:00:00', '2026-06-05 12:00:00', '校中心广场', '环保协会', '环保协会', '环保协会', '环保,快闪', 'none', null, null, null, 'rejected', '1', null, null, null, '0', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('14', '经典电影放映夜', '文艺', '露天电影放映活动！', '150', '89', '0.00', '0', null, null, '2026-05-16 19:30:00', '2026-05-16 22:30:00', '南区草坪', '电影社', '电影社', '电影社', '电影,户外,科幻', 'none', null, null, null, 'published', '1', null, null, null, '1', null, '2026-05-01 00:26:28', '2026-05-01 01:54:27');
INSERT INTO `activity` VALUES ('15', '简历诊断与面试模拟工坊', '就业', 'HR亲临现场，一对一简历诊断+模拟面试。', '20', '15', '0.00', '0', null, null, '2026-05-19 14:00:00', '2026-05-19 17:00:00', '就业指导中心面试室', '就业中心', '就业中心', '就业中心', '简历,面试,就业', 'none', null, null, null, 'published', '1', '1', '2026-05-01 00:54:15', null, '0', null, '2026-05-01 00:26:28', '2026-05-01 02:11:58');
INSERT INTO `activity` VALUES ('16', 'test11', '学术', '111', '100', '0', '0.00', '1', null, null, '2026-05-16 01:35:00', '2026-05-27 06:35:00', '11', '111', null, null, '11', 'none', null, null, null, 'published', '9', '1', '2026-05-01 01:35:56', null, '0', null, '2026-05-01 01:35:50', '2026-05-01 02:11:29');
INSERT INTO `activity` VALUES ('17', '限制学院身份测试', '学术', '111', '100', '0', '0.00', '1', '综合素质', '2.00', '2026-06-05 02:03:00', '2026-05-28 02:03:00', '111', '111', null, null, '111', 'college', '计算机科学与技术学院', null, null, 'published', '9', '1', '2026-05-01 02:05:06', null, '0', null, '2026-05-01 02:03:45', '2026-05-01 02:07:13');
INSERT INTO `activity` VALUES ('18', '限制社团身份测试', '学术', '111', '100', '0', '0.00', '1', '第二课堂', '1.50', '2026-05-01 02:05:00', '2026-05-21 02:04:00', '11', '11', null, null, '11', 'club', '校学生会', null, null, 'published', '9', '1', '2026-05-01 02:05:06', null, '0', null, '2026-05-01 02:05:00', '2026-05-01 02:11:02');
INSERT INTO `activity` VALUES ('19', '人数测试', '学术', '11', '1', '1', '0.00', '0', '', '0.00', '2026-05-30 02:12:00', '2026-05-27 02:12:00', '11', '11', null, null, '11', 'none', '', null, null, 'published', '9', '1', '2026-05-01 02:12:45', null, '0', null, '2026-05-01 02:12:37', '2026-05-01 10:51:43');
INSERT INTO `activity` VALUES ('20', '加分测试', '学术', '11', '100', '1', '0.00', '0', '', '0.00', '2026-05-01 10:50:00', '2026-05-01 10:51:00', '1', '11', null, null, '1', 'none', '', null, null, 'published', '1', '1', '2026-05-01 10:50:55', null, '0', null, '2026-05-01 10:50:48', '2026-05-09 16:01:07');

-- ----------------------------
-- Table structure for `audit_settings`
-- ----------------------------
DROP TABLE IF EXISTS `audit_settings`;
CREATE TABLE `audit_settings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ai_enabled` tinyint(1) NOT NULL,
  `ai_threshold` double NOT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of audit_settings
-- ----------------------------

-- ----------------------------
-- Table structure for `notification`
-- ----------------------------
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ead` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of notification
-- ----------------------------

-- ----------------------------
-- Table structure for `registration`
-- ----------------------------
DROP TABLE IF EXISTS `registration`;
CREATE TABLE `registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `activity_id` bigint NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'registered',
  `registered_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_activity` (`user_id`,`activity_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_activity_id` (`activity_id`),
  CONSTRAINT `reg_fk_activity` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`id`),
  CONSTRAINT `reg_fk_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of registration
-- ----------------------------
INSERT INTO `registration` VALUES ('1', '3', '1', 'cancelled', '2026-05-01 01:30:18');
INSERT INTO `registration` VALUES ('2', '3', '4', 'cancelled', '2026-04-22 09:00:00');
INSERT INTO `registration` VALUES ('3', '3', '8', 'checked_in', '2026-04-17 08:00:00');
INSERT INTO `registration` VALUES ('4', '3', '10', 'completed', '2026-02-25 10:00:00');
INSERT INTO `registration` VALUES ('5', '3', '9', 'cancelled', '2026-05-01 01:30:33');
INSERT INTO `registration` VALUES ('10', '3', '2', 'cancelled', '2026-05-01 01:30:39');
INSERT INTO `registration` VALUES ('24', '3', '3', 'cancelled', '2026-05-01 01:29:40');
INSERT INTO `registration` VALUES ('48', '3', '15', 'cancelled', '2026-05-01 01:13:11');
INSERT INTO `registration` VALUES ('84', '1', '3', 'registered', '2026-05-01 01:22:45');
INSERT INTO `registration` VALUES ('85', '1', '5', 'registered', '2026-05-01 01:24:46');
INSERT INTO `registration` VALUES ('87', '3', '17', 'cancelled', '2026-05-01 02:07:12');
INSERT INTO `registration` VALUES ('88', '3', '18', 'cancelled', '2026-05-01 02:11:01');
INSERT INTO `registration` VALUES ('89', '3', '16', 'cancelled', '2026-05-01 02:07:24');
INSERT INTO `registration` VALUES ('90', '4', '16', 'cancelled', '2026-05-01 02:11:29');
INSERT INTO `registration` VALUES ('91', '4', '15', 'cancelled', '2026-05-01 02:11:57');
INSERT INTO `registration` VALUES ('92', '3', '19', 'registered', '2026-05-01 10:51:43');
INSERT INTO `registration` VALUES ('93', '3', '20', 'registered', '2026-05-09 16:01:07');

-- ----------------------------
-- Table structure for `student`
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `student_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `college_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `club` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `major_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `class_no` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enrollment_year` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `grade` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_no` (`student_no`),
  KEY `user_id` (`user_id`),
  KEY `idx_student_no` (`student_no`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('1', '20230102526', '张三', '20', '男', '计算机科学与技术学院', '校学生会', '人工智能', '5', '2023', '大一', null, '2026-04-18 01:49:21', '2026-05-01 02:06:31');
INSERT INTO `student` VALUES ('2', '20230102527', '李四', '20', '男', '机械工程学院', '机械工程学院', '计算机科学与技术', '5', '2023', '大一', null, '2026-04-18 02:04:53', '2026-05-01 01:54:27');
INSERT INTO `student` VALUES ('3', '20230102101', '王五', '20', '男', '外国语学院', '外国语学院', '会计学', '1', '2023', '大一', null, '2026-04-18 02:15:24', '2026-05-01 01:54:27');
INSERT INTO `student` VALUES ('4', '20230101111', '丽丽', '21', '男', '计算机科学与技术学院', '计算机科学与技术学院', '英语', '1', '2023', '大一', null, '2026-04-20 14:33:39', '2026-05-01 01:54:27');
INSERT INTO `student` VALUES ('5', '20230304555', '玩玩', '22', '男', '外国语学院', '外国语学院', '软件工程', '5', '2023', '大一', null, '2026-04-24 21:28:49', '2026-05-01 01:54:27');

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nickname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `club` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int NOT NULL DEFAULT '1',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_username` (`username`),
  KEY `idx_email` (`email`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'testuser', '$2a$10$frxgoRDmAMLxAVnQIxwOcebTP7HMlP78PG7vr/bcl2np9VtcCty1G', 'test@example.com', '13800138000', 'testuser', null, 'ADMIN', null, '1', '2026-04-16 22:03:10', '2026-04-24 21:37:31');
INSERT INTO `user` VALUES ('2', 'soare02', '$2a$10$iYMYGBqqyXU1LJuyhd8VsO0u/t4mgT5u/fz.gkuWPaDrWFpv.y/4q', '2426882433@qq.com', '18683279836', 'soare02', null, 'USER', null, '1', '2026-04-16 22:13:06', '2026-05-09 16:51:50');
INSERT INTO `user` VALUES ('3', '20230102526', '$2a$10$7L5CzqJiFkqobSgCCXa5KOyOV9lWbWcD0x709G8XVN2khIymTxNXW', null, null, '张三', null, 'USER', '校学生会', '1', '2026-04-18 02:03:34', '2026-05-09 16:54:37');
INSERT INTO `user` VALUES ('4', '20230102527', '$2a$10$fAzVMWGIk9WrfxMFvMK42.Rj6CkUkuuS2J9EOUtH5g9D494EOlCAO', null, null, '李四', null, 'USER', '机械工程学院', '1', '2026-04-18 02:05:19', '2026-05-01 01:55:12');
INSERT INTO `user` VALUES ('5', '20230102101', '$2a$10$u8Q7wQrp7YERrkd9ovsqtO38pvptLD/JIffK1.OxCVTyXCLR/i9ge', null, null, '王五', null, 'USER', '外国语学院', '0', '2026-04-18 02:15:43', '2026-05-09 16:54:22');
INSERT INTO `user` VALUES ('6', '20230101111', '$2a$10$fVcxz8NfbMoqrLiV8ArauOT8r/eTVZpJsYfhpDGFlstEHQC54akpK', null, null, '丽丽', null, 'USER', '计算机科学与技术学院', '1', '2026-04-20 14:35:18', '2026-05-09 16:54:20');
INSERT INTO `user` VALUES ('7', '20230304555', '$2a$10$AkGtQfCKEmsAgQ9sxIO0BuoDdpR9B6HIefv/lyVHf13FiZfRZYHre', null, null, '玩玩', null, 'USER', '外国语学院', '1', '2026-04-24 21:34:02', '2026-05-09 16:54:19');
INSERT INTO `user` VALUES ('9', 'test11', '$2a$10$hxP80dNcYFGGSRubaCgJ8O3/UeuTza8jups3B/hQ2NTkrIJaDd44O', '111@qq.com', '18683279833', 'test11', null, 'PUBLISHER', null, '1', '2026-04-24 21:35:08', '2026-05-09 16:08:36');
