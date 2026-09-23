-- 测试数据（seed = 种子数据）
-- 用途：首次部署、或想把测试数据重置回初始状态时执行
-- 特点：开头 truncate 清空，可反复执行（幂等），结果始终一致
-- 注意：只放"最终值"，不要放中间的 update 打补丁语句

use course_selection;

truncate table `course`;

insert into `course`(course_name, teacher_id, credit, capacity) values
('数据结构',   2, 4.0, 60),
('计算机网络', 2, 3.0, 50),
('操作系统',   2, 3.5, 40),
('数据库原理', 2, 3.0, 45),
('软件工程',   2, 2.0, 80);
