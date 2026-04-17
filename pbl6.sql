/*
Navicat MySQL Data Transfer

Source Server         : 1
Source Server Version : 80040
Source Host           : localhost:3306
Source Database       : pbl6

Target Server Type    : MYSQL
Target Server Version : 80040
File Encoding         : 65001

Date: 2026-04-18 02:17:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `activity`
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `organizer` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of activity
-- ----------------------------

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
-- Table structure for `student`
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `student_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `college_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `major_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `class_no` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enrollment_year` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_no` (`student_no`),
  KEY `user_id` (`user_id`),
  KEY `idx_student_no` (`student_no`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('1', '20230102526', '张三', '20', '男', '01', '02', '5', '2023', null, '2026-04-18 01:49:21', '2026-04-18 01:49:21');
INSERT INTO `student` VALUES ('2', '20230102527', '李四', '20', '男', '01', '02', '5', '2023', null, '2026-04-18 02:04:53', '2026-04-18 02:04:53');
INSERT INTO `student` VALUES ('3', '20230102101', '王五', '20', '男', '01', '01', '1', '2023', null, '2026-04-18 02:15:24', '2026-04-18 02:15:24');

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'testuser', '$2a$10$frxgoRDmAMLxAVnQIxwOcebTP7HMlP78PG7vr/bcl2np9VtcCty1G', 'test@example.com', '13800138000', 'testuser', null, 'USER', '1', '2026-04-16 22:03:10', '2026-04-16 22:03:10');
INSERT INTO `user` VALUES ('2', 'soare02', '$2a$10$iYMYGBqqyXU1LJuyhd8VsO0u/t4mgT5u/fz.gkuWPaDrWFpv.y/4q', '2426882433@qq.com', '18683279836', 'soare02', null, 'USER', '1', '2026-04-16 22:13:06', '2026-04-16 22:13:06');
INSERT INTO `user` VALUES ('3', '20230102526', '$2a$10$7L5CzqJiFkqobSgCCXa5KOyOV9lWbWcD0x709G8XVN2khIymTxNXW', null, null, '张三', null, 'USER', '1', '2026-04-18 02:03:34', '2026-04-18 02:03:34');
INSERT INTO `user` VALUES ('4', '20230102527', '$2a$10$fAzVMWGIk9WrfxMFvMK42.Rj6CkUkuuS2J9EOUtH5g9D494EOlCAO', null, null, '李四', null, 'USER', '1', '2026-04-18 02:05:19', '2026-04-18 02:05:19');
INSERT INTO `user` VALUES ('5', '20230102101', '$2a$10$u8Q7wQrp7YERrkd9ovsqtO38pvptLD/JIffK1.OxCVTyXCLR/i9ge', null, null, '王五', null, 'USER', '1', '2026-04-18 02:15:43', '2026-04-18 02:15:43');
