-- 活动表增加字段
SET NAMES utf8mb4;
ALTER TABLE activity ADD COLUMN category VARCHAR(50) DEFAULT NULL AFTER title;
ALTER TABLE activity ADD COLUMN max_count INT NOT NULL DEFAULT 0 AFTER description;
ALTER TABLE activity ADD COLUMN registered_count INT NOT NULL DEFAULT 0 AFTER max_count;
ALTER TABLE activity ADD COLUMN fee DECIMAL(10,2) NOT NULL DEFAULT 0.00 AFTER registered_count;
ALTER TABLE activity ADD COLUMN has_bonus TINYINT(1) NOT NULL DEFAULT 0 AFTER fee;
ALTER TABLE activity ADD COLUMN bonus_type VARCHAR(50) DEFAULT NULL AFTER has_bonus;
ALTER TABLE activity ADD COLUMN bonus_value DECIMAL(10,2) DEFAULT NULL AFTER bonus_type;
ALTER TABLE activity ADD COLUMN college VARCHAR(100) DEFAULT NULL AFTER organizer;
ALTER TABLE activity ADD COLUMN tags VARCHAR(500) DEFAULT NULL AFTER college;

-- 报名表
CREATE TABLE IF NOT EXISTS registration (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    activity_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'registered',
    registered_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_user_id (user_id),
    KEY idx_activity_id (activity_id),
    UNIQUE KEY uk_user_activity (user_id, activity_id),
    CONSTRAINT reg_fk_user FOREIGN KEY (user_id) REFERENCES user (id),
    CONSTRAINT reg_fk_activity FOREIGN KEY (activity_id) REFERENCES activity (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 演示活动数据
INSERT INTO activity (title, category, description, start_time, end_time, location, organizer, max_count, registered_count, fee, status, user_id, has_bonus, bonus_type, bonus_value, college, tags, ai_audited) VALUES
('人工智能前沿技术分享会', '学术', '邀请校内外AI领域专家，分享大模型、多模态、具身智能等前沿方向的最新进展。', '2026-05-10 14:00:00', '2026-05-10 17:00:00', '图书馆学术报告厅A301', '计算机学院', 200, 156, 0, 'published', 1, 1, '综测加分', 0.5, '计算机学院', 'AI,大模型,技术', 1),
('第二十届校园歌手大赛', '文艺', '一年一度的校园歌手大赛海选正式开启！设置独唱、合唱两个赛道。', '2026-05-15 18:30:00', '2026-05-15 21:30:00', '大学生活动中心剧场', '校团委', 500, 342, 0, 'published', 1, 1, '二课学分', 1, '校团委', '歌唱,比赛,海选', 1),
('院际篮球友谊赛', '体育', '计算机学院 vs 电子工程学院篮球友谊赛。', '2026-05-08 15:00:00', '2026-05-08 17:30:00', '北区体育馆篮球场', '体育部', 300, 87, 0, 'published', 1, 0, NULL, NULL, '体育部', '篮球,友谊赛,体育', 1),
('敬老院关爱志愿活动', '公益', '前往阳光敬老院开展志愿服务。', '2026-05-11 08:30:00', '2026-05-11 12:00:00', '阳光敬老院（校车接送）', '青年志愿者协会', 30, 28, 0, 'published', 1, 1, '志愿时长', 4, '青年志愿者协会', '志愿,敬老,公益', 1),
('创业经验分享沙龙', '就业', '邀请三位成功创业的校友回到母校，分享创业历程。', '2026-05-18 14:00:00', '2026-05-18 16:30:00', '创新创业中心208室', '创业学院', 80, 12, 0, 'pending', 1, 1, '综测加分', 0.3, '创业学院', '创业,校友,分享', 0),
('手机摄影技巧工坊', '文艺', '零基础也能拍大片！专业摄影师带你掌握手机构图技巧。', '2026-05-12 19:00:00', '2026-05-12 21:00:00', '艺术楼多媒体教室B201', '艺术学院', 40, 38, 10, 'published', 1, 0, NULL, NULL, '艺术学院', '摄影,工坊,手机', 1),
('English Corner Weekly', '社交', '每周三晚的英语角活动！本周话题：The Future of Work。', '2026-05-07 19:00:00', '2026-05-07 21:00:00', '外语楼一楼大厅', '外国语学院', 50, 23, 0, 'published', 1, 0, NULL, NULL, '外国语学院', '英语,口语,社交', 1),
('大学生心理健康讲座', '讲座', '心理咨询中心特邀专家开展主题讲座。', '2026-05-09 14:00:00', '2026-05-09 16:00:00', '综合楼学术报告厅', '学生处', 300, 167, 0, 'published', 1, 1, '综测加分', 0.2, '学生处', '心理,健康,讲座', 1),
('48小时编程马拉松', '学术', 'HackCampus 2026春季编程马拉松！组队挑战真实项目。', '2026-05-20 18:00:00', '2026-05-22 18:00:00', '工程训练中心三楼', '计算机学院', 120, 78, 0, 'published', 1, 1, '综测加分', 1.5, '计算机学院', '编程,马拉松,比赛', 1),
('2026迎新晚会', '文艺', '欢迎2026级新生的盛大晚会！', '2026-03-01 19:00:00', '2026-03-01 22:00:00', '大学生活动中心剧场', '校学生会', 800, 756, 0, 'completed', 1, 0, NULL, NULL, '校学生会', '迎新,晚会', 1),
('读书分享会·四月', '学术', '本月共读书目《人类简史》。', '2026-05-14 19:00:00', '2026-05-14 21:00:00', '图书馆研讨室305', '图书馆', 25, 18, 0, 'published', 1, 0, NULL, NULL, '图书馆', '读书,分享,人文', 1),
('瑜伽入门体验课', '体育', '专业瑜伽老师带你体验基础瑜伽。', '2026-05-13 18:00:00', '2026-05-13 19:30:00', '体育馆二楼舞蹈房', '体育部', 20, 20, 15, 'published', 1, 0, NULL, NULL, '体育部', '瑜伽,体验,健身', 1),
('校园环保快闪行动', '公益', '响应世界环境日，发起校园环保快闪。', '2026-06-05 10:00:00', '2026-06-05 12:00:00', '校中心广场', '环保协会', 100, 0, 0, 'rejected', 1, 1, '志愿时长', 2, '环保协会', '环保,快闪', 0),
('经典电影放映夜·《星际穿越》', '文艺', '露天电影放映活动！', '2026-05-16 19:30:00', '2026-05-16 22:30:00', '南区草坪', '电影社', 150, 89, 0, 'published', 1, 0, NULL, NULL, '电影社', '电影,户外,科幻', 1),
('简历诊断与面试模拟工坊', '就业', 'HR亲临现场，一对一简历诊断+模拟面试。', '2026-05-19 14:00:00', '2026-05-19 17:00:00', '就业指导中心面试室', '就业中心', 20, 15, 0, 'pending', 1, 0, NULL, NULL, '就业中心', '简历,面试,就业', 0);

-- 演示报名数据（user_id=3 是学号20230102526的用户）
INSERT INTO registration (user_id, activity_id, status, registered_at) VALUES
(3, 1, 'registered', '2026-04-21 10:00:00'),
(3, 4, 'registered', '2026-04-22 09:00:00'),
(3, 8, 'checked_in', '2026-04-17 08:00:00'),
(3, 10, 'completed', '2026-02-25 10:00:00'),
(3, 9, 'registered', '2026-04-15 14:00:00');
