// ==================== MOCK DATA ====================

export interface User {
  id: string; username: string; password: string; role: 'student' | 'admin' | 'publisher';
  name: string; college: string; grade: string; avatar: string; email: string; phone: string; tags: string[];
}

export interface Activity {
  id: string; creatorId: string; title: string; category: string; description: string; cover: string;
  startTime: string; endTime: string; location: string; maxCount: number; registeredCount: number;
  fee: number; status: string; hasBonus: boolean; bonusType: string; bonusValue: number;
  approvalStatus: string; tags: string[]; createdAt: string; college: string;
}

export interface Registration {
  id: string; userId: string; activityId: string; status: string; registeredAt: string;
}

export interface Notification {
  id: string; userId: string; title: string; content: string; time: string; read: boolean;
}

export const MOCK_USERS: User[] = [
  { id:'u1', username:'student', password:'123456', role:'student', name:'张小明', college:'计算机科学与技术学院', grade:'大三', avatar:'明', email:'zhangxm@campus.edu', phone:'138****6789', tags:['编程','AI','篮球'] },
  { id:'u2', username:'admin', password:'123456', role:'admin', name:'李管理', college:'教务处', grade:'—', avatar:'李', email:'admin@campus.edu', phone:'139****0000', tags:[] },
  { id:'u3', username:'publisher', password:'123456', role:'publisher', name:'王组织', college:'校学生会', grade:'—', avatar:'王', email:'publisher@campus.edu', phone:'137****1111', tags:['活动策划'] },
];

export const COLORS = ['#E8D5B7','#B7D5E8','#D5E8B7','#E8B7C9','#C9B7E8','#B7E8D5','#E8CBB7','#B7CBE8'];
export const CAT_ICONS: Record<string, string> = { '学术':'📖','文艺':'🎭','体育':'⚽','公益':'🤝','社交':'💬','就业':'💼','讲座':'🎓','其他':'📌' };

export const MOCK_ACTIVITIES: Activity[] = [
  { id:'a1', creatorId:'u3', title:'人工智能前沿技术分享会', category:'学术', description:'邀请校内外AI领域专家，分享大模型、多模态、具身智能等前沿方向的最新进展。面向全校师生开放，欢迎对AI感兴趣的同学参加。', cover:'', startTime:'2026-05-10 14:00', endTime:'2026-05-10 17:00', location:'图书馆学术报告厅A301', maxCount:200, registeredCount:156, fee:0, status:'published', hasBonus:true, bonusType:'综测加分', bonusValue:0.5, approvalStatus:'approved', tags:['AI','大模型','技术'], createdAt:'2026-04-20', college:'计算机学院' },
  { id:'a2', creatorId:'u3', title:'第二十届校园歌手大赛', category:'文艺', description:'一年一度的校园歌手大赛海选正式开启！无论你是实力唱将还是音乐爱好者，这里都是你的舞台。本次大赛设置独唱、合唱两个赛道。', cover:'', startTime:'2026-05-15 18:30', endTime:'2026-05-15 21:30', location:'大学生活动中心剧场', maxCount:500, registeredCount:342, fee:0, status:'published', hasBonus:true, bonusType:'二课学分', bonusValue:1, approvalStatus:'approved', tags:['歌唱','比赛','海选'], createdAt:'2026-04-18', college:'校团委' },
  { id:'a3', creatorId:'u3', title:'院际篮球友谊赛', category:'体育', description:'计算机学院 vs 电子工程学院篮球友谊赛。欢迎两院同学前来观赛助威！现场设有互动抽奖环节。', cover:'', startTime:'2026-05-08 15:00', endTime:'2026-05-08 17:30', location:'北区体育馆篮球场', maxCount:300, registeredCount:87, fee:0, status:'published', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['篮球','友谊赛','体育'], createdAt:'2026-04-19', college:'体育部' },
  { id:'a4', creatorId:'u3', title:'敬老院关爱志愿活动', category:'公益', description:'本周六前往阳光敬老院开展志愿服务，陪伴老人聊天、协助整理内务、表演文艺节目。集合地点：校门口。请准时到达。', cover:'', startTime:'2026-05-11 08:30', endTime:'2026-05-11 12:00', location:'阳光敬老院（校车接送）', maxCount:30, registeredCount:28, fee:0, status:'published', hasBonus:true, bonusType:'志愿时长', bonusValue:4, approvalStatus:'approved', tags:['志愿','敬老','公益'], createdAt:'2026-04-21', college:'青年志愿者协会' },
  { id:'a5', creatorId:'u3', title:'创业经验分享沙龙', category:'就业', description:'邀请三位成功创业的校友回到母校，分享他们从0到1的创业历程、踩过的坑和宝贵经验。圆桌对话+自由交流。', cover:'', startTime:'2026-05-18 14:00', endTime:'2026-05-18 16:30', location:'创新创业中心208室', maxCount:80, registeredCount:12, fee:0, status:'pending', hasBonus:true, bonusType:'综测加分', bonusValue:0.3, approvalStatus:'pending', tags:['创业','校友','分享'], createdAt:'2026-04-22', college:'创业学院' },
  { id:'a6', creatorId:'u3', title:'手机摄影技巧工坊', category:'文艺', description:'零基础也能拍大片！专业摄影师带你掌握手机构图、光线运用和后期修图技巧。请提前下载Snapseed。', cover:'', startTime:'2026-05-12 19:00', endTime:'2026-05-12 21:00', location:'艺术楼多媒体教室B201', maxCount:40, registeredCount:38, fee:10, status:'published', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['摄影','工坊','手机'], createdAt:'2026-04-17', college:'艺术学院' },
  { id:'a7', creatorId:'u3', title:'English Corner Weekly', category:'社交', description:'每周三晚的英语角活动！本周话题：The Future of Work。外教Tom和Sarah将到场与大家交流。茶歇提供。', cover:'', startTime:'2026-05-07 19:00', endTime:'2026-05-07 21:00', location:'外语楼一楼大厅', maxCount:50, registeredCount:23, fee:0, status:'published', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['英语','口语','社交'], createdAt:'2026-04-15', college:'外国语学院' },
  { id:'a8', creatorId:'u3', title:'大学生心理健康讲座', category:'讲座', description:'心理咨询中心特邀专家开展「压力管理与情绪调节」主题讲座，帮助同学们更好地应对学业和生活压力。', cover:'', startTime:'2026-05-09 14:00', endTime:'2026-05-09 16:00', location:'综合楼学术报告厅', maxCount:300, registeredCount:167, fee:0, status:'published', hasBonus:true, bonusType:'综测加分', bonusValue:0.2, approvalStatus:'approved', tags:['心理','健康','讲座'], createdAt:'2026-04-16', college:'学生处' },
  { id:'a9', creatorId:'u3', title:'48小时编程马拉松', category:'学术', description:'HackCampus 2026春季编程马拉松！组队挑战真实项目，48小时内从创意到原型。丰厚奖金等你来拿！', cover:'', startTime:'2026-05-20 18:00', endTime:'2026-05-22 18:00', location:'工程训练中心三楼', maxCount:120, registeredCount:78, fee:0, status:'published', hasBonus:true, bonusType:'综测加分', bonusValue:1.5, approvalStatus:'approved', tags:['编程','马拉松','比赛'], createdAt:'2026-04-14', college:'计算机学院' },
  { id:'a10', creatorId:'u3', title:'2026迎新晚会', category:'文艺', description:'欢迎2026级新生的盛大晚会！歌舞、小品、魔术精彩纷呈。', cover:'', startTime:'2026-03-01 19:00', endTime:'2026-03-01 22:00', location:'大学生活动中心剧场', maxCount:800, registeredCount:756, fee:0, status:'completed', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['迎新','晚会'], createdAt:'2026-02-20', college:'校学生会' },
  { id:'a11', creatorId:'u3', title:'读书分享会·四月', category:'学术', description:'本月共读书目《人类简史》。欢迎分享你的阅读感悟，碰撞思想火花。', cover:'', startTime:'2026-05-14 19:00', endTime:'2026-05-14 21:00', location:'图书馆研讨室305', maxCount:25, registeredCount:18, fee:0, status:'published', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['读书','分享','人文'], createdAt:'2026-04-10', college:'图书馆' },
  { id:'a12', creatorId:'u3', title:'瑜伽入门体验课', category:'体育', description:'专业瑜伽老师带你体验基础瑜伽。适合零基础，自备瑜伽垫或使用场馆提供的垫子。', cover:'', startTime:'2026-05-13 18:00', endTime:'2026-05-13 19:30', location:'体育馆二楼舞蹈房', maxCount:20, registeredCount:20, fee:15, status:'published', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['瑜伽','体验','健身'], createdAt:'2026-04-12', college:'体育部' },
  { id:'a13', creatorId:'u3', title:'校园环保快闪行动', category:'公益', description:'响应世界环境日，发起校园环保快闪。捡拾垃圾+环保知识问答+创意DIY。', cover:'', startTime:'2026-06-05 10:00', endTime:'2026-06-05 12:00', location:'校中心广场', maxCount:100, registeredCount:0, fee:0, status:'rejected', hasBonus:true, bonusType:'志愿时长', bonusValue:2, approvalStatus:'rejected', tags:['环保','快闪'], createdAt:'2026-04-23', college:'环保协会' },
  { id:'a14', creatorId:'u3', title:'经典电影放映夜·《星际穿越》', category:'文艺', description:'露天电影放映活动！本期放映诺兰经典科幻片《星际穿越》。提供爆米花和饮品。', cover:'', startTime:'2026-05-16 19:30', endTime:'2026-05-16 22:30', location:'南区草坪（遇雨移至活动中心）', maxCount:150, registeredCount:89, fee:0, status:'published', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'approved', tags:['电影','户外','科幻'], createdAt:'2026-04-11', college:'电影社' },
  { id:'a15', creatorId:'u3', title:'简历诊断与面试模拟工坊', category:'就业', description:'HR亲临现场，一对一简历诊断+模拟面试。名额有限，先到先得！', cover:'', startTime:'2026-05-19 14:00', endTime:'2026-05-19 17:00', location:'就业指导中心面试室', maxCount:20, registeredCount:15, fee:0, status:'pending', hasBonus:false, bonusType:'', bonusValue:0, approvalStatus:'pending', tags:['简历','面试','就业'], createdAt:'2026-04-23', college:'就业中心' },
];

export const MOCK_REGISTRATIONS: Registration[] = [
  { id:'r1', userId:'u1', activityId:'a1', status:'registered', registeredAt:'2026-04-21' },
  { id:'r2', userId:'u1', activityId:'a4', status:'registered', registeredAt:'2026-04-22' },
  { id:'r3', userId:'u1', activityId:'a8', status:'checked_in', registeredAt:'2026-04-17' },
  { id:'r4', userId:'u1', activityId:'a10', status:'completed', registeredAt:'2026-02-25' },
  { id:'r5', userId:'u1', activityId:'a9', status:'registered', registeredAt:'2026-04-15' },
];

export const MOCK_NOTIFICATIONS: Notification[] = [
  { id:'n1', userId:'u1', title:'报名成功', content:'你已成功报名「人工智能前沿技术分享会」', time:'2026-04-21 10:30', read:false },
  { id:'n2', userId:'u1', title:'活动提醒', content:'「敬老院关爱志愿活动」将于明天8:30开始，请准时到达校门口集合', time:'2026-04-23 20:00', read:false },
  { id:'n3', userId:'u1', title:'加分到账', content:'参加「2026迎新晚会」获得综测加分 0.2 分', time:'2026-03-02 09:00', read:true },
];

// ==================== UTILS ====================
export const roleLabel = (r: string) => ({ student:'学生', admin:'管理员', publisher:'活动发布者' }[r] || r);
export const statusLabel = (s: string) => ({ published:'已发布', pending:'待审批', rejected:'已驳回', completed:'已结束', cancelled:'已取消', draft:'草稿' }[s] || s);
export const statusBadge = (s: string) => ({ published:'badge-green', pending:'badge-amber', rejected:'badge-red', completed:'badge-gray', cancelled:'badge-gray', draft:'badge-gray' }[s] || 'badge-gray');
export const regStatusLabel = (s: string) => ({ registered:'已报名', checked_in:'已签到', completed:'已完成', cancelled:'已取消' }[s] || s);
export const regStatusBadge = (s: string) => ({ registered:'badge-blue', checked_in:'badge-green', completed:'badge-purple', cancelled:'badge-gray' }[s] || 'badge-gray');

export function todayStr() {
  const d = new Date();
  const days = ['日','一','二','三','四','五','六'];
  return `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日 星期${days[d.getDay()]}`;
}

export function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
