/*
 Navicat Premium Data Transfer

 Source Server         : 101.133.230.27
 Source Server Type    : MySQL
 Source Server Version : 80200
 Source Host           : 101.133.230.27:3306
 Source Schema         : kinit_first

 Target Server Type    : MySQL
 Target Server Version : 80200
 File Encoding         : 65001

 Date: 27/08/2024 10:42:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('4abeb646159c');

-- ----------------------------
-- Table structure for vadmin_auth_dept
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_dept`;
CREATE TABLE `vadmin_auth_dept`  (
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '部门名称',
  `dept_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '部门标识',
  `disabled` tinyint(1) NOT NULL COMMENT '是否禁用',
  `order` int NULL DEFAULT NULL COMMENT '显示排序',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `owner` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '负责人',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `parent_id` int NULL DEFAULT NULL COMMENT '上级部门',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `parent_id`(`parent_id` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_dept_dept_key`(`dept_key` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_dept_name`(`name` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `vadmin_auth_dept` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '部门表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_dept
-- ----------------------------
INSERT INTO `vadmin_auth_dept` VALUES ('kinit 开发团队', 'total_group', 0, 1, NULL, NULL, NULL, NULL, NULL, 1, '2023-12-18 22:51:07', '2023-12-21 17:57:42', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_auth_menu
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_menu`;
CREATE TABLE `vadmin_auth_menu`  (
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称',
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `redirect` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '重定向地址',
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '前端组件地址',
  `path` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '前端路由地址',
  `disabled` tinyint(1) NOT NULL COMMENT '是否禁用',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏',
  `order` int NOT NULL COMMENT '排序',
  `menu_type` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '菜单类型',
  `parent_id` int NULL DEFAULT NULL COMMENT '父菜单',
  `perms` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识',
  `noCache` tinyint(1) NOT NULL COMMENT '如果设置为true，则不会被 <keep-alive> 缓存(默认 false)',
  `breadcrumb` tinyint(1) NOT NULL COMMENT '如果设置为false，则不会在breadcrumb面包屑中显示(默认 true)',
  `affix` tinyint(1) NOT NULL COMMENT '如果设置为true，则会一直固定在tag项中(默认 false)',
  `noTagsView` tinyint(1) NOT NULL COMMENT '如果设置为true，则不会出现在tag中(默认 false)',
  `canTo` tinyint(1) NOT NULL COMMENT '设置为true即使hidden为true，也依然可以进行路由跳转(默认 false)',
  `alwaysShow` tinyint(1) NOT NULL COMMENT '当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式，\n    只有一个时，会将那个子路由当做根路由显示在侧边栏，若你想不管路由下面的 children 声明的个数都显示你的根路由，\n    你可以设置 alwaysShow: true，这样它就会忽略之前定义的规则，一直显示根路由(默认 true)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `parent_id`(`parent_id` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_menu_perms`(`perms` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `vadmin_auth_menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 82 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_menu
-- ----------------------------
INSERT INTO `vadmin_auth_menu` VALUES ('仪表盘', 'ant-design:dashboard-filled', '/dashboard/workplace', '#', '/dashboard', 0, 0, 0, '0', NULL, NULL, 0, 1, 0, 0, 0, 0, 1, '2022-08-13 10:56:32', '2023-10-05 02:21:30', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('权限管理', 'ep:lock', '/auth/menu', '#', '/auth', 0, 0, 1, '0', NULL, NULL, 0, 1, 0, 0, 0, 0, 2, '2022-09-22 22:53:52', '2023-10-05 02:22:38', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('系统管理', 'ant-design:setting-filled', NULL, '#', '/system', 0, 0, 2, '0', NULL, NULL, 0, 1, 0, 0, 0, 0, 3, '2022-10-04 20:58:18', '2022-10-28 21:28:13', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('工作台', NULL, NULL, 'views/Dashboard/Workplace', 'workplace', 0, 0, 0, '1', 1, NULL, 0, 1, 0, 0, 0, 0, 4, '2022-10-12 16:59:27', '2022-11-18 10:25:35', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('数据概览', NULL, NULL, 'views/Dashboard/Analysis/Analysis', 'analysis', 0, 0, 1, '1', 1, NULL, 0, 1, 0, 0, 0, 0, 5, '2022-11-05 12:55:59', '2023-09-14 16:10:08', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('用户分布', NULL, NULL, 'views/Dashboard/Map', 'map', 0, 0, 2, '1', 1, NULL, 0, 1, 0, 0, 0, 0, 6, '2022-11-16 18:39:17', '2022-11-17 20:45:35', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('菜单管理', NULL, NULL, 'views/Vadmin/Auth/Menu/Menu', 'menu', 0, 0, 1, '1', 2, NULL, 0, 1, 0, 0, 0, 0, 7, '2022-09-22 17:21:30', '2022-11-18 10:26:42', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('角色管理', NULL, NULL, 'views/Vadmin/Auth/Role/Role', 'role', 0, 0, 2, '1', 2, NULL, 0, 1, 0, 0, 0, 0, 8, '2022-09-22 17:21:30', '2022-11-18 10:26:56', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('用户管理', NULL, NULL, 'views/Vadmin/Auth/User/User', 'user', 0, 0, 3, '1', 2, NULL, 0, 1, 0, 0, 0, 0, 9, '2022-09-22 17:21:30', '2023-09-11 16:24:37', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('字典配置', NULL, NULL, 'views/Vadmin/System/Dict/Dict', 'dict', 0, 0, 1, '1', 3, NULL, 0, 1, 0, 0, 0, 0, 10, '2022-10-04 21:02:55', '2023-09-12 15:07:25', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('日志管理', 'tdesign:catalog', NULL, '#', '/record', 0, 0, 99, '0', NULL, NULL, 0, 1, 0, 0, 0, 0, 13, '2022-10-28 21:29:56', '2023-10-05 03:40:05', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('系统配置', NULL, NULL, 'views/Vadmin/System/Settings/Settings', 'settings', 0, 0, 0, '1', 3, NULL, 0, 1, 0, 0, 0, 0, 14, '2022-10-30 17:35:50', '2022-10-30 17:35:50', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('登录日志', NULL, NULL, 'views/Vadmin/System/Record/Login/Login', 'login', 0, 0, 0, '1', 13, NULL, 0, 1, 0, 0, 0, 0, 15, '2022-10-28 21:34:47', '2022-10-28 21:36:05', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('操作日志', NULL, NULL, 'views/Vadmin/System/Record/Operation/Operation', 'operation', 0, 0, 1, '1', 13, NULL, 0, 1, 0, 0, 0, 0, 16, '2022-10-28 22:12:15', '2022-10-29 13:39:46', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('新增菜单', NULL, NULL, NULL, NULL, 0, 0, 0, '2', 7, 'auth.menu.create', 0, 1, 0, 0, 0, 0, 17, '2022-11-18 14:21:26', '2022-11-18 14:29:51', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('编辑菜单', NULL, NULL, NULL, NULL, 0, 0, 1, '2', 7, 'auth.menu.update', 0, 1, 0, 0, 0, 0, 18, '2022-11-18 15:23:05', '2022-11-18 15:23:05', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('删除菜单', NULL, NULL, NULL, NULL, 0, 0, 2, '2', 7, 'auth.menu.delete', 0, 1, 0, 0, 0, 0, 19, '2022-11-18 15:23:27', '2022-11-18 15:23:27', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('新增角色', NULL, NULL, NULL, NULL, 0, 0, 0, '2', 8, 'auth.role.create', 0, 1, 0, 0, 0, 0, 20, '2022-11-18 15:11:55', '2022-11-18 15:11:55', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('编辑角色', NULL, NULL, NULL, NULL, 0, 0, 1, '2', 8, 'auth.role.update', 0, 1, 0, 0, 0, 0, 21, '2022-11-18 15:23:56', '2022-11-18 15:23:56', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('删除角色', NULL, NULL, NULL, NULL, 0, 0, 2, '2', 8, 'auth.role.delete', 0, 1, 0, 0, 0, 0, 22, '2022-11-18 15:24:11', '2023-08-24 15:41:23', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('新增用户', NULL, NULL, NULL, NULL, 0, 0, 0, '2', 9, 'auth.user.create', 0, 1, 0, 0, 0, 0, 23, '2022-11-18 15:26:19', '2022-11-18 15:31:00', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('编辑用户', NULL, NULL, NULL, NULL, 0, 0, 1, '2', 9, 'auth.user.update', 0, 1, 0, 0, 0, 0, 24, '2022-11-18 15:26:41', '2022-11-18 15:26:41', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('删除用户', NULL, NULL, NULL, NULL, 0, 0, 2, '2', 9, 'auth.user.delete', 0, 1, 0, 0, 0, 0, 25, '2022-11-18 15:27:06', '2022-11-18 15:27:06', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('批量导入用户', NULL, NULL, NULL, NULL, 0, 0, 3, '2', 9, 'auth.user.import', 0, 1, 0, 0, 0, 0, 26, '2022-11-18 15:27:36', '2022-11-18 15:27:36', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('导出筛选用户', NULL, NULL, NULL, NULL, 0, 0, 4, '2', 9, 'auth.user.export', 0, 1, 0, 0, 0, 0, 27, '2022-11-18 15:27:55', '2022-11-18 15:27:55', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('重置密码通知短信', NULL, NULL, NULL, NULL, 0, 0, 5, '2', 9, 'auth.user.reset', 0, 1, 0, 0, 0, 0, 28, '2022-11-18 15:28:38', '2022-11-18 15:28:38', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('帮助中心', 'material-symbols:help-rounded', NULL, '#', '/help', 0, 0, 100, '0', NULL, NULL, 0, 1, 0, 0, 0, 1, 38, '2023-02-16 16:33:03', '2023-02-16 16:35:00', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('常见问题类别', NULL, NULL, 'views/Vadmin/Help/IssueCategory/IssueCategory', 'issue/category', 0, 0, 0, '1', 38, NULL, 0, 1, 0, 0, 0, 0, 39, '2023-02-16 16:34:00', '2023-09-11 12:32:06', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('常见问题', NULL, NULL, 'views/Vadmin/Help/Issue/Issue', 'issue', 0, 0, 1, '1', 38, NULL, 0, 1, 0, 0, 0, 0, 40, '2023-02-16 17:12:53', '2023-09-11 12:32:26', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('常见问题表单', NULL, NULL, 'views/Vadmin/Help/Issue/components/Write', 'issue/form', 0, 1, 99, '1', 38, NULL, 0, 1, 0, 0, 0, 0, 42, '2023-02-21 23:41:24', '2023-09-11 12:32:43', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('智慧大屏', 'icon-park-solid:data-sheet', '/screen/air', NULL, '/screen', 0, 0, 3, '0', NULL, NULL, 0, 1, 0, 0, 0, 1, 68, '2022-11-24 15:07:23', '2022-11-24 15:23:27', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('空气质量', NULL, NULL, 'views/Vadmin/Screen/Air/Air', 'air', 0, 0, 0, '1', 68, NULL, 0, 1, 0, 0, 0, 0, 69, '2022-11-24 15:08:09', '2023-09-18 09:52:39', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('定时任务', NULL, NULL, 'views/Vadmin/System/Task/Task', 'task', 0, 0, 1, '1', 3, NULL, 1, 1, 0, 0, 0, 0, 73, '2023-06-25 14:44:36', '2023-09-18 15:47:06', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('调度日志', NULL, NULL, 'views/Vadmin/System/Record/Task/Task', 'task', 0, 0, 2, '1', 13, NULL, 0, 1, 0, 0, 0, 0, 74, '2023-06-28 10:53:58', '2023-09-13 17:22:22', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('获取菜单列表', NULL, NULL, NULL, NULL, 0, 0, 3, '2', 7, 'auth.menu.list', 0, 1, 0, 0, 0, 0, 76, '2023-08-24 15:40:23', '2023-08-24 15:40:23', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('获取角色列表', NULL, NULL, NULL, NULL, 0, 0, 3, '2', 8, 'auth.role.list', 0, 1, 0, 0, 0, 0, 77, '2023-08-24 15:40:47', '2023-08-24 15:40:47', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('获取用户列表', NULL, NULL, NULL, NULL, 0, 0, 6, '2', 9, 'auth.user.list', 0, 1, 0, 0, 0, 0, 78, '2023-08-24 15:41:16', '2023-08-24 15:41:16', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('资源管理', 'line-md:image', NULL, '#', '/resource', 0, 0, 4, '0', NULL, NULL, 0, 1, 0, 0, 0, 1, 79, '2023-08-25 13:56:25', '2023-08-25 13:56:25', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('图片资源', NULL, NULL, 'views/Vadmin/Resource/Image/Image', 'images', 0, 0, 1, '1', 79, NULL, 0, 1, 0, 0, 0, 0, 80, '2023-08-25 13:57:19', '2023-09-14 11:11:32', NULL, 0);
INSERT INTO `vadmin_auth_menu` VALUES ('部门管理', NULL, NULL, 'views/Vadmin/Auth/Dept/Dept', 'dept', 0, 0, 0, '1', 2, NULL, 0, 1, 0, 0, 0, 0, 81, '2023-12-18 22:49:01', '2023-12-18 22:49:01', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_auth_role
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_role`;
CREATE TABLE `vadmin_auth_role`  (
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称',
  `role_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '权限字符',
  `data_range` int NOT NULL COMMENT '数据权限范围',
  `disabled` tinyint(1) NOT NULL COMMENT '是否禁用',
  `order` int NULL DEFAULT NULL COMMENT '排序',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `is_admin` tinyint(1) NOT NULL COMMENT '是否为超级角色',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_vadmin_auth_role_name`(`name` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_role_role_key`(`role_key` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_role
-- ----------------------------
INSERT INTO `vadmin_auth_role` VALUES ('管理员', 'admin', 4, 0, 0, NULL, 1, 1, '2022-08-13 10:58:18', '2022-10-09 15:03:34', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_auth_role_depts
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_role_depts`;
CREATE TABLE `vadmin_auth_role_depts`  (
  `role_id` int NULL DEFAULT NULL,
  `dept_id` int NULL DEFAULT NULL,
  INDEX `dept_id`(`dept_id` ASC) USING BTREE,
  INDEX `role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_role_depts_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `vadmin_auth_dept` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_role_depts_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_role_depts
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_auth_role_menus
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_role_menus`;
CREATE TABLE `vadmin_auth_role_menus`  (
  `role_id` int NULL DEFAULT NULL,
  `menu_id` int NULL DEFAULT NULL,
  INDEX `menu_id`(`menu_id` ASC) USING BTREE,
  INDEX `role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_role_menus_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `vadmin_auth_menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_role_menus_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_role_menus
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_auth_user
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_user`;
CREATE TABLE `vadmin_auth_user`  (
  `avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像',
  `telephone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱地址',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '昵称',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `gender` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `is_active` tinyint(1) NOT NULL COMMENT '是否可用',
  `is_reset_password` tinyint(1) NOT NULL COMMENT '是否已经重置密码，没有重置的，登陆系统后必须重置密码',
  `last_ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最后一次登录IP',
  `last_login` datetime NULL DEFAULT NULL COMMENT '最近一次登录时间',
  `is_staff` tinyint(1) NOT NULL COMMENT '是否为工作人员',
  `wx_server_openid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '服务端微信平台openid',
  `is_wx_server_openid` tinyint(1) NOT NULL COMMENT '是否已有服务端微信平台openid',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_vadmin_auth_user_name`(`name` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_user_telephone`(`telephone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_user
-- ----------------------------
INSERT INTO `vadmin_auth_user` VALUES (NULL, '15020221010', NULL, 'kinit', 'admin', '$2b$12$Ce7eSUKIIl8DMKeDyNHyr.Dp4aesQCM70RePigRVEny1Eql31R0Cq', '1', 1, 1, '127.0.0.1', '2024-01-20 11:08:06', 1, NULL, 0, 1, '2022-08-11 20:17:04', '2024-01-20 11:08:03', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_auth_user_depts
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_user_depts`;
CREATE TABLE `vadmin_auth_user_depts`  (
  `user_id` int NULL DEFAULT NULL,
  `dept_id` int NULL DEFAULT NULL,
  INDEX `dept_id`(`dept_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_user_depts_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `vadmin_auth_dept` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_user_depts_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_user_depts
-- ----------------------------
INSERT INTO `vadmin_auth_user_depts` VALUES (1, 1);

-- ----------------------------
-- Table structure for vadmin_auth_user_roles
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_user_roles`;
CREATE TABLE `vadmin_auth_user_roles`  (
  `user_id` int NULL DEFAULT NULL,
  `role_id` int NULL DEFAULT NULL,
  INDEX `role_id`(`role_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_user_roles_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_user_roles_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_user_roles
-- ----------------------------
INSERT INTO `vadmin_auth_user_roles` VALUES (1, 1);

-- ----------------------------
-- Table structure for vadmin_help_issue
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_help_issue`;
CREATE TABLE `vadmin_help_issue`  (
  `category_id` int NOT NULL COMMENT '类别',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '内容',
  `view_number` int NOT NULL COMMENT '查看次数',
  `is_active` tinyint(1) NOT NULL COMMENT '是否可见',
  `create_user_id` int NOT NULL COMMENT '创建人',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id` ASC) USING BTREE,
  INDEX `create_user_id`(`create_user_id` ASC) USING BTREE,
  INDEX `ix_vadmin_help_issue_title`(`title` ASC) USING BTREE,
  CONSTRAINT `vadmin_help_issue_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `vadmin_help_issue_category` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_help_issue_ibfk_2` FOREIGN KEY (`create_user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '常见问题记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_help_issue
-- ----------------------------
INSERT INTO `vadmin_help_issue` VALUES (3, 'KINIT-UNI 是使用若依-移动端进行的二次开发吗？', '<p>是的，是在若依-移动端的基础上进行的二次开发，在此感谢若依团队！二次开发中我们重新将接口请求改为 luch-request 组件，项目结构也有所改动，并且加入了 uView UI 组件，uni-simple-router 路由拦截。</p>', 0, 1, 1, 6, '2023-02-27 15:46:19', '2023-08-04 17:42:00', NULL, 0);
INSERT INTO `vadmin_help_issue` VALUES (3, 'KINIT 开源吗？', '<p>开源</p>', 0, 1, 1, 7, '2023-02-27 15:46:34', '2023-08-04 17:41:54', NULL, 0);
INSERT INTO `vadmin_help_issue` VALUES (3, 'KINIT 可以商用吗？', '<p>可以</p>', 0, 1, 1, 8, '2023-02-27 15:46:44', '2023-08-04 17:41:56', NULL, 0);
INSERT INTO `vadmin_help_issue` VALUES (3, 'KINIT 源码地址多少？', '<p> <a href=\"https://gitee.com/ktianc/kinit\" target=\"_blank\">https://gitee.com/ktianc/kinit</a> </p>', 0, 1, 1, 9, '2023-02-27 15:46:55', '2023-08-04 17:41:58', NULL, 0);
INSERT INTO `vadmin_help_issue` VALUES (4, '如何退出登录？', '<p>请点击[我的] - [应用设置] - [退出登录]即可退出登录</p>', 0, 1, 1, 10, '2023-02-27 15:47:07', '2023-08-03 00:31:24', NULL, 0);
INSERT INTO `vadmin_help_issue` VALUES (4, '如何修改用户头像？', '<p>请点击[我的] - [选择头像] - [点击提交]即可更换用户头像</p>', 0, 1, 1, 11, '2023-02-27 15:47:18', '2023-07-22 17:57:11', NULL, 0);
INSERT INTO `vadmin_help_issue` VALUES (4, '如何修改登录密码？', '<p>请点击[我的] - [应用设置] - [修改密码]即可修改登录密码</p>', 0, 1, 1, 12, '2023-02-27 15:47:28', '2023-08-04 17:41:52', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_help_issue_category
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_help_issue_category`;
CREATE TABLE `vadmin_help_issue_category`  (
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类别名称',
  `platform` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '展示平台',
  `is_active` tinyint(1) NOT NULL COMMENT '是否可见',
  `create_user_id` int NOT NULL COMMENT '创建人',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `create_user_id`(`create_user_id` ASC) USING BTREE,
  INDEX `ix_vadmin_help_issue_category_name`(`name` ASC) USING BTREE,
  INDEX `ix_vadmin_help_issue_category_platform`(`platform` ASC) USING BTREE,
  CONSTRAINT `vadmin_help_issue_category_ibfk_1` FOREIGN KEY (`create_user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '常见问题类别表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_help_issue_category
-- ----------------------------
INSERT INTO `vadmin_help_issue_category` VALUES ('KINIT 问题', '1', 1, 1, 3, '2023-02-27 15:45:29', '2023-02-27 15:45:29', NULL, 0);
INSERT INTO `vadmin_help_issue_category` VALUES ('其他问题', '1', 1, 1, 4, '2023-02-27 15:45:35', '2023-02-27 15:45:35', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_record_login
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_record_login`;
CREATE TABLE `vadmin_record_login`  (
  `telephone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `status` tinyint(1) NOT NULL COMMENT '是否登录成功',
  `platform` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登陆平台',
  `login_method` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '认证方式',
  `ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登陆地址',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登陆地点',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '县',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '城市',
  `county` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '区/县',
  `operator` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运营商',
  `postal_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮政编码',
  `area_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地区区号',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '浏览器',
  `system` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作系统',
  `response` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '响应信息',
  `request` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求信息',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_vadmin_record_login_telephone`(`telephone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '登录记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_record_login
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_record_sms_send
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_record_sms_send`;
CREATE TABLE `vadmin_record_sms_send`  (
  `user_id` int NOT NULL COMMENT '操作人',
  `status` tinyint(1) NOT NULL COMMENT '发送状态',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '发送内容',
  `telephone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '目标手机号',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '失败描述',
  `scene` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '发送场景',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_record_sms_send_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '短信发送记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_record_sms_send
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_resource_images
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_resource_images`;
CREATE TABLE `vadmin_resource_images`  (
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '原图片名称',
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片链接',
  `create_user_id` int NOT NULL COMMENT '创建人',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `create_user_id`(`create_user_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_resource_images_ibfk_1` FOREIGN KEY (`create_user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '图片素材表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_resource_images
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_system_dict_details
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_dict_details`;
CREATE TABLE `vadmin_system_dict_details`  (
  `label` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典标签',
  `value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典键值',
  `disabled` tinyint(1) NOT NULL COMMENT '字典状态，是否禁用',
  `is_default` tinyint(1) NOT NULL COMMENT '是否默认',
  `order` int NOT NULL COMMENT '字典排序',
  `dict_type_id` int NOT NULL COMMENT '关联字典类型',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `dict_type_id`(`dict_type_id` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_details_label`(`label` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_details_value`(`value` ASC) USING BTREE,
  CONSTRAINT `vadmin_system_dict_details_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `vadmin_system_dict_type` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典详情表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_system_dict_details
-- ----------------------------
INSERT INTO `vadmin_system_dict_details` VALUES ('男', '0', 0, 0, 0, 1, NULL, 2, '2022-10-07 12:07:43', '2022-10-07 12:08:02', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('女', '1', 0, 0, 1, 1, NULL, 4, '2022-10-08 13:55:32', '2022-10-08 13:55:32', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('目录', '0', 0, 1, 0, 2, NULL, 5, '2022-10-08 14:05:15', '2022-10-08 14:05:38', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('菜单', '1', 0, 0, 1, 2, NULL, 6, '2022-10-08 14:05:24', '2022-10-08 14:05:24', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('按钮', '2', 0, 0, 2, 2, NULL, 7, '2022-10-08 14:05:32', '2022-10-08 14:05:32', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('密码登录', '0', 0, 0, 0, 3, NULL, 8, '2022-12-03 23:48:33', '2022-12-03 23:48:33', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('短信登录', '1', 0, 0, 1, 3, NULL, 9, '2022-12-03 23:48:47', '2022-12-03 23:48:47', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('PC端管理系统', '0', 0, 0, 0, 4, NULL, 10, '2022-12-03 23:49:24', '2022-12-03 23:49:24', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('移动端管理系统', '1', 0, 0, 1, 4, NULL, 11, '2022-12-03 23:49:41', '2022-12-03 23:49:41', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('微信一键登录', '2', 0, 0, 2, 3, NULL, 12, '2023-02-23 22:48:57', '2023-02-23 22:53:26', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('时间间隔(interval)', 'interval', 0, 0, 0, 5, NULL, 14, '2023-06-25 16:56:10', '2023-06-26 15:52:15', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('Cron 表达式', 'cron', 0, 0, 1, 5, NULL, 15, '2023-06-25 16:57:28', '2023-06-25 16:57:28', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('指定日期时间(date)', 'date', 0, 0, 2, 5, NULL, 16, '2023-06-25 16:57:41', '2023-06-26 15:52:25', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('仅本人数据权限', '0', 0, 0, 0, 6, NULL, 17, '2023-12-21 18:39:42', '2023-11-27 15:36:42', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('本部门数据权限', '1', 0, 0, 1, 6, NULL, 18, '2023-12-21 18:39:56', '2023-11-27 15:38:02', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('本部门及以下数据权限', '2', 0, 0, 2, 6, NULL, 19, '2023-12-21 18:40:06', '2023-11-27 15:38:13', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('自定义数据权限', '3', 0, 0, 3, 6, NULL, 20, '2023-12-21 18:40:15', '2023-11-27 15:38:18', NULL, 0);
INSERT INTO `vadmin_system_dict_details` VALUES ('全部数据权限', '4', 0, 0, 4, 6, NULL, 21, '2023-12-21 18:40:26', '2023-11-27 15:38:23', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_system_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_dict_type`;
CREATE TABLE `vadmin_system_dict_type`  (
  `dict_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典名称',
  `dict_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典类型',
  `disabled` tinyint(1) NOT NULL COMMENT '字典状态，是否禁用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_vadmin_system_dict_type_dict_name`(`dict_name` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_type_dict_type`(`dict_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典类型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_system_dict_type
-- ----------------------------
INSERT INTO `vadmin_system_dict_type` VALUES ('性别', 'sys_vadmin_gender', 0, NULL, 1, '2022-10-05 22:03:43', '2022-10-08 13:57:16', NULL, 0);
INSERT INTO `vadmin_system_dict_type` VALUES ('菜单类型', 'sys_vadmin_menu_type', 0, NULL, 2, '2022-10-08 13:57:32', '2022-10-08 13:57:32', NULL, 0);
INSERT INTO `vadmin_system_dict_type` VALUES ('认证方式', 'sys_vadmin_login_method', 0, NULL, 3, '2022-12-03 23:48:09', '2022-12-03 23:48:09', NULL, 0);
INSERT INTO `vadmin_system_dict_type` VALUES ('登录平台', 'sys_vadmin_platform', 0, NULL, 4, '2022-12-03 23:49:11', '2022-12-03 23:49:11', NULL, 0);
INSERT INTO `vadmin_system_dict_type` VALUES ('定时任务执行策略', 'vadmin_system_task_exec_strategy', 0, '与定时任务中有约定，请勿随意更改', 5, '2023-06-25 16:55:20', '2023-06-30 09:23:29', NULL, 0);
INSERT INTO `vadmin_system_dict_type` VALUES ('数据权限范围', 'sys_vadmin_data_range', 0, NULL, 6, '2023-12-21 18:36:56', '2023-12-21 18:36:56', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_system_settings
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_settings`;
CREATE TABLE `vadmin_system_settings`  (
  `config_label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '配置表标签',
  `config_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '配置表键',
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '配置表内容',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注信息',
  `disabled` tinyint(1) NOT NULL COMMENT '是否禁用',
  `tab_id` int NOT NULL COMMENT '关联tab标签',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_settings_config_key`(`config_key` ASC) USING BTREE,
  INDEX `tab_id`(`tab_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_system_settings_ibfk_1` FOREIGN KEY (`tab_id`) REFERENCES `vadmin_system_settings_tab` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_system_settings
-- ----------------------------
INSERT INTO `vadmin_system_settings` VALUES ('系统标题', 'web_title', 'Kinit', NULL, 0, 1, 1, '2022-10-31 20:47:43', '2023-02-27 09:36:07', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('系统LOGO', 'web_logo', '/media/system/logo.png', NULL, 0, 1, 2, '2022-10-31 20:47:43', '2023-02-27 09:36:07', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('系统描述', 'web_desc', 'Kinit 是一套开箱即用的中后台解决方案，可以作为新项目的启动模版。', NULL, 0, 1, 3, '2022-10-31 20:47:43', '2023-02-27 09:36:07', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('ICO图标', 'web_ico', '/media/system/favicon.ico', NULL, 0, 1, 4, '2022-10-31 20:47:43', '2023-01-16 18:10:07', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('备案号', 'web_icp_number', '豫ICP备19033601号-1', NULL, 0, 1, 5, '2022-10-31 20:47:43', '2023-02-27 09:36:07', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('版权信息', 'web_copyright', 'Copyright ©2022-present K', NULL, 0, 1, 6, '2022-10-31 20:47:43', '2023-02-27 09:36:07', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('百度统计代码', 'web_baidu', NULL, '（当前无法生效，已停用该配置）不包含<script>标签，只需要复制<script>标签内的内容即可', 1, 2, 7, '2022-10-31 20:49:58', '2022-11-22 16:35:43', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('隐私协议', 'web_privacy', '<p>更新日期：XXXX年XX月XX日</p><p>生效日期：XXXX年XX月XX日</p><p>【公司名称】（以下简称“我们”或“XXX”） 非常重视您的隐私和个人信息保护，我们将按业界成熟的安全标准，采取相应的安全保护措施来保护您的个人信息。</p><p>本《隐私政策》适用于XXX的产品及服务（包括未设独立隐私政策的的产品/服务）。这些产品/服务包括但不限于XXXX网站、移动应用、客户端、相关微信开放平台帐号或小程序以及供第三方网站和应用程序使用的我们软件开发工具包（SDK）和应用程序编程接口（API）。</p><p>您在使用我们的产品或服务时，我们可能会收集和使用您的相关信息。我们希望通过本《隐私政策》向您说明，在使用我们的产品或服务时，我们如何收集、使用、储存、分享和保护这些信息，以及我们为您提供的了解、更新、控制和保护这些信息的方式。 </p><p>本隐私政策将帮助您了解以下内容：</p><p>一、个人信息定义及范围</p><p>二、我们可能如何收集和使用您的个人信息</p><p>三、我们可能如何使用 Cookies 和同类技术</p><p>四、我们可能如何共享、转让、公开披露您的个人信息</p><p>五、我们可能如何保护和保存您的个人信息</p><p>六、您的权利</p><p>七、我们如何处理儿童的个人信息</p><p>八、本隐私政策如何更新</p><p>九、如何联系我们</p><p>一、个人信息定义及范围</p><p> 1、个人信息：指以电子或者其他方式记录的能够单独或者与其他信息结合识别特定自然人身份或者反映特定自然人活动情况的各种信息。本隐私政策中涉及的个人信息包括自然人的基本资料（包括姓名、性别、电话号码）、网络身份标识信息（包括系统账号、IP地址以）、个人财产信息（包括交易和消费记录、虚拟货币、虚拟交易等虚拟财产信息）、个人常用设备信息（包括硬件序列号、硬件型号、设备MAC地址、操作系统类型、软件列表、唯一设备标识符）、个人位置信息（包括大概地理位置信息）。我们实际具体收集的个人信息种类以下文描述为准。</p><p>2、个人敏感信息：指一旦泄露、非法提供或滥用可能危害人身和财产安全，极易导致个人名誉、身心健康受到损害或歧视性待遇等的个人信息。本隐私政策中涉及的个人敏感信息包括您的个人身份信息、网络身份标识信息。我们实际具体收集的个人敏感信息种类以下文描述为准。您同意您的个人敏感信息按本政策所述的目的和方式来处理。</p><p>二、我们可能如何收集和使用您的个人信息</p><p>1.账号注册</p><p>创建账号时，您需要提供手机号码（个人敏感信息，用于接受验证码匹配个人身份）。您只有提供真实准确的上述信息，才能成功注册账号并使用产品和/或服务的核心功能。如果您选择不提供上述为实现核心产品功能的必备信息，或将导致我们无法为您提供该核心产品功能。我们的产品支持您使用第三方平台的账号（微信账号）进行登录，如您使用第三方平台的账号登录的，我们将根据您的授权获取该第三方账号下的相关信息（包括：用户名、昵称、头像等）以及身份验证信息（个人敏感信息）。我们承诺，收集上述信息是用于为您提供账号注册、登录服务以及保障您的账号安全，防范安全风险。如您拒绝授权此类信息，则您将无法使用第三方平台的账号登录我们平台，但不影响我们提供的其他产品和服务的正常使用。</p><p>同时，您需理解，手机号码的验证码匹配结果属于您的个人敏感信息，我们收集该类信息是基于法律法规的相关要求，如您拒绝提供可能导致您无法注册账号并使用相关产品功能，请您谨慎考虑后再选择是否提供。</p><p>2、搜课报班</p><p>您在购买我们的产品或服务中准备消费支付时，需要使用到支付功能。在支付过程中，您需要向我们提供一些与完成交易相关联的信息，包括如下：购买的课程或服务信息、收货人信息（收货人姓名、收货地址及其联系电话）（个人敏感信息）。我们收集这些信息是为了帮助您顺利完成交易、保障您的交易安全、查询订单信息、提供客户服务等。您可以选择我们合作的第三方支付机构（如微信支付、支付宝）所提供的支付服务。支付功能本身并不收集您的个人信息，但我们需要将您的订单信息及对账信息与这些支付机构共享以确认您的支付指令并完成支付。</p><p>3、上课</p><p>为了您可以观看已经购买的课程的直播和回放视频，以及直播过程中参与授课老师的互动教学，例如跟读、语音/视频上麦，我们需要获取您的麦克风、摄像头权限。</p><p>4、信息发布</p><p>您主动对我们的产品/服务进行评价或发布其他内容（如发表评论信息）时，我们将收集您发布的信息，并展示您的昵称、头像和发布内容。您还可以通过主动上传图片、视频等方式授权我们访问您的相机、照片和麦克风，以便于您通过拍照、拍视频、上传照片或上传视频等方式发布内容。当您需要关闭该功能时，大多数移动设备都会支持您的这项需求，具体方法请参考或联系您移动设备的服务商或生产商。</p><p>5、客服售后</p><p>当您在使用我们的客服、产品或服务的售后功能时，为了保障您的账号与系统安全，我们可能需要您先行向我们提供账号信息，并与您之前的个人信息相匹配以验证您的用户身份。同时，为了方便与您联系或帮助您解决问题，我们可能还需要您提供姓名、手机号码、电子邮件及其他联系方式等个人信息。另外，我们还会收集您与我们的沟通信息（包括文字/图片/音视频/通话记录形式）、与您的需求相关联的其他必要信息。我们收集这些信息是为了帮助您解决问题，如您拒绝提供上述信息，我们可能无法向您及时反馈投诉、申诉或咨询结果。</p><p>6、邮寄</p><p>当您使用邮寄（例如邮寄课程随材）服务时，您需要提供收件人的姓名、手机号码、通信地址（个人敏感信息），以便于您的订单能够安全准确送达。</p><p>8、个性化营销</p><p>在您事先同意的情况下，我们会要求您提供个人信息，包括职业、教育、年龄、性别信息，以便提升我们的产品、服务、宣传 成效。我们可能会利用此类个人信息，来制作有关用户群的整体报告，此类个人信息及整体报告皆为不具名形式，不会包含能识别您的内容。</p><p>9、日志信息</p><p>当您使用平台的网站或客户端提供的产品或服务时，平台会自动收集您对平台服务的详细使用情况，作为有关网络日志保存（您的搜索查询内容、IP地址、浏览器的类型、电信运营商、使用的语言、访问日期和时间、您访问的网页记录、通话状态信息）。</p><p>请注意，单独的设备信息、日志信息等是无法识别特定自然人身份的信息。如果平台将这类非个人信息与其他信息结合用于识别特定自然人身份，或者将其与个人信息结合使用，则在结合使用期间，这类非个人信息将被视为个人信息，除取得您授权或法律法规另有规定外，平台会将该类个人信息做匿名化处理。</p><p>10、为向您提供平台相应功能，平台需获取的权限包括如下：</p><p>读取及写入存储器权限：当您进入本平台，为了正常使用应用内运行所需资源、图片、视频、文件、资料、讲义下载/图片预览/图片扫描/文件上传/日志缓存/磁盘空间判断，以及使用课程下载、资料上传功能，平台需要获取您的读取及写入存储器权限。如不开启权限，您将不能使用与此权限相关的特定功能，但不影响您使用我们平台提供的其他服务。</p><p>位置信息权限：当您使用地区选择课程等功能时，为了基于所在地点位置接受服务推荐，平台需要获取您的位置信息权限。如不开启权限，平台将不能基于您所在地点位置进行服务推荐，但不影响您使用平台提供的其他服务。您也可以在平台手动设置城市信息，以便您查看对应的城市服务推荐内容。</p><p>摄像头权限及相册权限：当您使用头像图片设置、拍照搜题、直播视频连麦、题目纠错传图等功能时，为了您进行实时拍摄或图片/视频上传，平台需要获取您的摄像头权限和/或相册权限。如不开启权限，您将无法使用与实时拍摄或图片/视频上传相关的特定功能，但不影响您使用我们平台提供的其他服务。</p><p>麦克风权限：当您使用直播连麦、自习室等功能时，为了使用麦克风设备进行语音输入，平台需要获取您的麦克风权限。如不开启权限，您将无法使用与语音输入相关的特定功能，但不影响您使用我们平台提供的其他服务。</p><p>我们仅会出于以下目的，收集和使用您的个人信息：</p><p>1. 为您提供相关产品或服务所必要的信息；</p><p>2. 在提供产品或服务时，用于安全验证、身份认证、安全防范、诈骗检测、存档和备份的必要信息，以确保产品和服务的安全性；</p><p>3. 帮助我们设计新产品或服务，改善我们现有产品或服务；</p><p>4. 向您提供与您更加相关的广告以替代普遍投放的广告；</p><p>5. 评估我们服务中的广告和其他促销及推广活动的效果，并加以改善；</p><p>6. 软件认证或管理软件升级；让你参与有关我们产品和服务的调查；</p><p>7. 设备权限调用</p><p>您在产品使用过程中，可能会需要您的一些设备授权。以下是可能调用的权限及对应的业务功能、目的及调用前向您询问的情况。您可以在设备的设置功能中选择关闭部分或全部权限，但可能会影响到部分功能使用。在不同设备中，权限显示方式及关闭方式可能有所不同，具体请参考设备及系统开发方说明或指引。</p><p>为了向您提供更好的服务，我们的产品可能会更新和变化，当我们可能将您的隐私信息用于本隐私政策未载明的其它用途时，我们会事先征求您的明示同意，例如：通过界面提示、邮件等方式向您详细说明信息收集的目的、方式、范围，并征求您的同意。若您不同意提供前述信息，您可能无法使用特定的产品或服务。</p><p>三、我们可能如何使用Cookie类数据</p><p>为确保网站正常高效运转、为您获得更轻松的访问体验、向您推荐您可能感兴趣的内容，我们可能会在您的设备上存储Cookie类数据。Cookie通常包含标识符、站点名称以及一些号码等字符。借助于此类数据，产品能够存储您的偏好或身份等数据,以便提供更好的持续性的、针对性的功能或服务，我们不会将此类数据用于本政策所述目的之外的任何用途。您可根据自己的偏好管理或删除 Cookie。您可以清除计算机或移动设备上保存的所有 Cookie，您有权接受或拒绝Cookie。大多数浏览器会自动接受Cookie，但您通常可根据自己的需要来修改浏览器的设置以拒绝Cookie;另外，您也可以清除软件内保存的所有Cookie。但您可能因此无法完全体验我们某些便捷性和安全性的服务功能。</p><p>四、我们可能如何共享、转让、公开披露您的个人信息</p><p>（一）共享</p><p>为了更好的给您提供服务，我们以及我们的关联公司，可能将您的个人信息与我们的关联公司、合作伙伴及第三方服务供应商、承包商及代理分享，具体说明如下：</p><p>1、在获取明确同意的情况下共享：获得您的明确同意后，我们会与其他方共享您的个人信息。</p><p>2、我们可能会根据法律法规规定，或按政府主管部门的强制性要求，对外共享您的个人信息。</p><p>3、与授权合作伙伴共享：仅为实现本隐私政策中声明的目的，我们的某些服务将由授权合作伙伴提供。我可能会与合作伙伴共享您的某些个人信息，以提供更好的客户服务和用户体验。例如，我们聘请来提供第三方数据统计和分析服务的公司可能需要采集和访问个人数据以进行数据统计和分析。在这种情况下，这些公司必须遵守我们的数据隐私和安全要求。我们仅会出于合法、正当、必要、特定、明确的目的共享您的个人信息，并且只会共享提供服务所必要的个人信息。</p><p>4、对我们与之共享个人信息的公司、组织和个人，我们会与其签署严格的保密协定，要求他们按照我们的说明、本隐私政策以及其他任何相关的保密和安全措施来处理个人信息。</p><p>5、如我们或我们的关联公司与任何第三方（详见附录）分享您的个人信息，我们将确保该第三方在使用您的个人信息时遵守本《隐私政策》及我们要求其遵守的其他适当的保密和安全措施。</p><p>（二）转让</p><p>我们不会将您的个人信息转让给任何公司、组织和个人，但以下情况除外：</p><p>1、在获取明确同意的情况下转让：获得您的明确同意后，我们会向其他方转让您的个人信息；</p><p>2、在涉及合并、收购或破产清算时，如涉及到个人信息转让，我们会在要求新的持有您个人信息的公司、组织继续受此隐私政策的约束，否则我们将要求该公司、组织重新向您征求授权同意。</p><p>（三）公开披露</p><p>根据相关法律法规及国家标准，在以下情形中，我们可能会依法收集并使用您的个人信息并且无需征得您的同意:</p><p>1、与国家安全、国防安全直接相关的；</p><p>2、与公共安全、公共卫生、重大公共利益直接相关的；</p><p>3、与犯罪侦查、起诉、审判和判决执行等直接相关的；</p><p>4、出于维护您或他人的生命、财产等重大合法权益但又很难得到您本人同意的；</p><p>5、所收集的个人信息是您自行向社会公众公开的；</p><p>6、从合法公开披露的信息中收集个人信息，例如：合法的新闻报道、政府信息公开等渠道；</p><p>7、根据您的要求签订和履行合同所必需的；</p><p>8、用于维护所提供的服务的安全稳定运行所必需的，例如：发现、处置产品或服务的故障；</p><p>9、为合法的新闻报道所必需的；</p><p>10、学术研究机构基于公共利益开展统计或学术研究所必要，且对外提供学术研究或描述的结果时，对结果中所包含的个人信息进行去标识化处理的；</p><p>11、法律法规规定的其他情形。</p><p>五、我们可能如何保护和保存您的个人信息</p><p>（一）我们使用符合业界标准的安全防护措施保护您提供的个人信息，防止数据遭到未经授权访问、公开披露、使用、修改、损坏或丢失。我们会采取合理可行的措施，保护您的个人信息。例如：使用加密技术确保“客户端”与“服务”之间数据交换时的保密性；对数据流转的各个环节所涉及的设备、文件、人员等进行严格控制；举办安全和隐私保护培训课程。</p><p>（二）我们会采取合理可行的措施，确保收集的个人信息,只在达成本政策所述目的所需的期限内保留，除非需要延长保留期或受到法律的允许。</p><p>（三）互联网内很多通讯工具都并非足够安全，我们强烈建议您不要通过此类工具发送个人的隐私信息和安全信息，使用复杂密码，以保证您的账号安全。</p><p>（四）我们将尽力确保您发送给我们的信息的相关安全性。如果我们的物理、技术或管理防护设施遭到破坏，导致信息被非授权访问、公开披露、篡改、或毁坏，导致您的合法权益受损，我们将承担相应的法律责任。</p><p>（五）如果不幸的发生了个人信息安全事件，我们将按照法律法规的要求，及时向您告知：安全事件的基本情况和可能的影响、我们已采取或将要采取的处置措施、您可自主防范和降低风险的建议、对您的补救措施等。我们将及时将事件相关情况以邮件、信函、电话、推送通知等方式告知您，难以逐一告知个人信息主体时，我们会采取合理、有效的方式发布公告。同时，我们还将按照监管部门要求，主动上报个人信息安全事件的处置情况。</p><p>（六）个人信息的保存：</p><p>1、您的个人信息将存储于中华人民共和国境内。</p><p>2、在您使用我们的产品服务期间，您的个人信息将在为了实现本政策所述目的之期限内保存，同时将结合法律有强制的留存要求期限的规定确定，如《中华人民共和国电子商务法》要求商品和服务信息、交易信息保存时间自交易完成之日起不少于三年。在超出保存期间后，根据适用法律的要求,我们会可能删除您的个人信息。</p><p>3、如果我们终止服务或运营，我们会至少提前三十日向您通知，并在终止服务或运营后对您的个人信息进行删除处理。</p><p>六、您的权利</p><p>按照中国相关的法律、法规、标准，以及其他国家、地区的通行做法，您有权对自己的个人信息行使以下权利：</p><p>（一）访问或修改</p><p>您可以通过登录我们产品使用相关功能，访问或控制您个人的隐私信息，例如：个人资料信息修改、密码更改等；其它与您的权益重要相关，或者服务正常运行必须依赖的隐私信息,例如:学习记录、订单记录、交易记录等，如果需要访问、修正、回收，请发送电子邮件至XXXXX，我们将在30天内回复您的请求。</p><p>（二）删除</p><p>在以下情形中，您可以向我们提出删除个人信息的请求：</p><p>1、如果我们处理个人信息的行为违反法律法规；</p><p>2、如果我们收集、使用您的个人信息，却未征得您的同意；</p><p>3、如果我们处理个人信息的行为违反了与您的约定；</p><p>4、如果您不再使用我们的产品或服务，或您注销了账号；</p><p>5、如果我们不再为您提供产品或服务。</p><p>若我们决定响应您的删除请求，我们还将同时通知从我们获得您的个人信息的实体，要求其及时删除，除非法律法规另有规定，或这些实体获得您的独立授权。</p><p>当您的信息被执行删除后，我们将不再使用该数据，但可能会为了适应必要的相关法律政策要求，或为了保障服务正常运行所必须的数据完整性，我们可能无法立即删除，在必要的时段内存储或备份，但在该时间段后及时删除这些数据。</p><p>（三）约束信息系统自动决策</p><p>在某些业务功能中，我们可能会依据信息系统、算法等在内的非人工自动决策机制做出决定。如果这些决定影响您的合法权益，您有权要求我们做出解释或处理。</p><p>（四）上述请求响应</p><p>为保障隐私数据的安全，必要情况下，我们可能会先要求您验证自己的身份，然后再处理您的请求。例如：需要您提供书面请求或以其他方式证明您的身份。</p><p>一般情况我们不会收取费用，对于某些请求处理可能涉及到不能忽略的成本，我们会出示合理合法的依据，需要您承担相应的费用。对于某些请求，可能不适用法律、或涉及处理成本过高、或给他人合法权益带来风险等，我们可能会拒绝处理或不能及时处理。</p><p>按照法律法规要求，我们可能将无法响应以下请求：</p><p>1、与国家安全、国防安全有关的；</p><p>2、与公共安全、公共卫生、重大公共利益有关的；</p><p>3、与犯罪侦查、起诉和审判等有关的；</p><p>4、有充分证据表明您存在主观恶意或滥用权利的；</p><p>5、响应您的请求将导致您或其他个人、组织的合法权益受到严重损害的。</p><p>七、本隐私政策如何更新</p><p>本隐私政策可能变更。</p><p>我们通常会在我们官网发布通告或声明的形式发布对本政策所做的任何变更。如果您不同意相关变更，应立即停止使用相关服务；否则，自该隐私政策生效日期起，若您继续登录、查看或以其他形式使用我们的产品或服务，即表示您同意接受修订后的隐私政策约束，对于争执，原则上我们会保留您的合法权益。</p><p>八、如何联系我们</p><p>如果您对本隐私政策有任何疑问、意见或建议，可以随时通过拨打客服电话、登录产品等各种方式与我们联系，我们会积极进行查证、处理并尽快答复。</p><p>个人信息保护负责人邮箱XXXXXX</p><p>本隐私政策版本更新日期为XXXX年XX月XX日，将于XXXX年XX月XX日正式生效。</p>', NULL, 0, 4, 8, '2022-11-04 13:50:21', '2023-02-08 10:50:54', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('用户协议', 'web_agreement', '<p>《用户注册协议》（以下简称“本协议”）是由您与XXXXXXX（以下简称“XXX”）以数据电文形式共同缔结的协议，请您务必审慎阅读、充分理解各条款内容，限制、免责条款可能以黑体加粗形式提示您注意。当您在线点击/勾选“同意”或“接受”键后，视为您已详细阅读并同意遵守本协议，本协议生效，则XXX根据本协议为您提供网上服务。因此，除非您已阅读并接受本协议所有条款，否则您无权使用XXX网上服务。</p><p>若您未满18周岁，请在法定监护人的陪同下阅读本协议，并特别注意未成年人使用条款。</p><p>XXX有权在必要时更新协议内容并以通知、公告、声明或其它形式通知您。若您不同意修改内容，应立即停止使用相关服务；否则，您的任何对相关服务的登录、查看、使用等行为将被视为您对修改内容的理解和接受。</p><p>1.定义</p><p>如无特别说明，下列术语在本协议中的含义为：</p><p>1.1.您：指注册成功并使用XXX网上服务的完全民事行为能力人，又称“学员”或“用户”。</p><p>1.2.XXX：是“XXXX公司名称”在本协议中的简称。</p><p>1.3.网上服务：指由XXX运营的、通过计算机客户端、网页端、移动端等端口向您提供的各项网上服务的统称，服务内容包括但不限于考试资讯，资料中心，模考系统，公开课，付费课。</p><p>1.4.XXX网络平台：是指XXX借以向您提供各项网上服务的综合服务系统。</p><p>1.5.XXX组成元素：指XXX各端口页面所包含的及与XXX相关的软件、文字、图片、音频、视频、图标、标识、界面设计、版面框架、编排方式、有关数据或电子文档等内容和信息。</p><p>1.6.本协议：指《用户注册协议》正文及其修订版本。上述内容一经正式发布，即为本协议不可分割的组成部分。</p><p>2.注册账号</p><p>2.1.您将在完成注册程序后获得XXX网上服务的账号。您享有该账号的使用权。XXX享有该账号的所有权。XXX有权对账号的权限设计进行调整。</p><p>2.2.XXX有理由认为该账号下的所有行为都是您的真实意思表示。您享有该账号下行为产生的所有权利，同时应承担该账号下所有行为及事件产生的义务及责任。若您账号下的行为对您、XXX或第三方造成的损害，您将负全部责任。</p><p>若该账号通过XXX网上服务展示任何违法、不道德或XXX认为不合适的资料；或者XXX有理由怀疑该资料属于程序或恶意操作，XXX有权暂停或终止您的帐号，并拒绝您于现在和未来使用本服务之全部或任何部分。</p><p>2.3.账号的取得</p><p>2.3.1.您应当按照XXX网络平台注册页面的要求完成注册程序，并保证填写的个人信息与您的身份信息一致，否则XXX有权拒绝向您提供相关服务或承担任何义务。</p><p>2.3.2.除非您在个人信息中填写真实身份信息，否则您无权购买XXX提供的网上付费服务（例如购买课程、题库等）。</p><p>2.3.3.XXX有权核实您注册账号时所提供的身份信息是否真实、有效。若您违反注册要求，未使用您本人的真实身份信息进行注册，XXX有权随时关闭您的账号。</p><p>2.3.4.XXX有权采取技术与管理等合理措施保障您账号的安全、有效。</p><p>2.4.授权协助注册</p><p>若您在注册过程中主动向XXX或其工作人员寻求支持和帮助，则您提出要求及指示的行为即视为您对XXX协助您注册账号的委托授权，因此产生的后果及责任由您承担。</p><p>2.5.注册信息的修改</p><p>若您在注册成功并获得XXX网络平台的账号后，需要修改注册信息，请按照XXX出于安全考虑设置的相关修改程序操作。若XXX有合理理由怀疑您提交的相关资料或信息属于恶意程序或恶意操作，则XXX有权关闭您的账号，并有权拒绝您于现在和将来使用XXX所提供服务之全部或任何部分。</p><p>2.6.账号的使用和保管</p><p>2.6.1.您有义务妥善保管并安全使用您的账号及密码并承担相关责任。若您未保管好自己的帐号和密码，因此而产生的任何损失或损害，XXX无法也不承担任何责任。</p><p>2.6.2.若您发现您的账号使用出现异常（被他人盗用等任何安全问题），应立即通知XXX并提供您的个人有效身份信息以供核实账户身份。经核实身份一致的，XXX应当及时采取措施暂停该账号的登录和使用；身份不一致或者您拒绝提供个人有效身份证明的，XXX有权拒绝您提出的关于该账号的管理请求。</p><p>2.6.3.您在XXX注册的账号，仅限您个人使用，不得将账号与第三人共享或将账号转让、赠与他人等。否则，XXX有权关闭您的账号。</p><p>2.7.若XXX发现您的帐号存在异常状况(包括但不限于异地登陆、IP地址异常变动、发送注册信息变更请求等)，XXX则有权依据其合理判断采取相应措施(包括但不限于要求用户进行手机实名认证、进行面部识别等)以保护帐号安全。</p><p>3.服务内容</p><p>3.1.基于自身的经营自主权，XXX有权自主决定通过互联网提供的服务（产品）类型及内容。</p><p>XXX网上服务目前包含以下内容：</p><p>3.1.1.基础服务：即XXX网络平台上提供的非付费的网上服务，包括：免费考试相关网上咨询；免费发布考试资讯，免费提供部分考试资料，免费提供部分考试的在线模考系统，免费提供部分直播视频公开课，免费提供部分视频公开课等非付费网上服务。</p><p>3.1.2.增值服务：即付费服务，是XXX为有需要的用户提供的、用户可以依据相关产品协议在网络平台上购买并享受的服务（产品）。例如，XXX网络平台的网上付费课程。</p><p>3.1.3.其他服务：XXX通过网络平台为您提供的其他服务。</p><p>3.2.XXX网上服务的具体内容以XXX在您使用时实际提供给您的情况和版本为准。</p><p>3.3.XXX在此许可您依本协议而获得XXX网上服务之基础服务的使用权。</p><p>3.4.除非另有其它明示规定，XXX网络平台内所增加或强化的任何新功能，包括所推出的新产品，均受到本使用协议之规范。</p><p>3.5.XXX提供的资讯信息类服务，例如与培训课程有关的报名、考试信息等资讯服务，其内容均应以有权主管部门公布的信息为准。XXX及其代表不提供对报名、考试信息的任何形式的承诺或保证，也不存在任何形式的保过、密题、内幕信息或类似承诺。用户应独立收集信息并进行判断，并承担相关后果。如因与相关培训课程有关的报名、考试信息发生变动而造成用户学习成本上升、丧失考试资格等损失，XXX及格XXX网络平台不负有任何责任。</p><p>3.6.XXX有随时调整各项服务费用收取标准的权利，但已完成支付的订单不受影响；您有权自主决定是否购买XXX提供的网上增值服务（产品）。</p><p>3.7.针对增值服务(付费类课程产品和服务)的特别约定</p><p>用户可根据自身实际需求选择免费服务（产品）或有偿、付费服务（产品）。针对有偿课程服务（产品），用户请注意下述特别事项：</p><p>3.7.1.您可通过XXX的计算机客户端、网页端、移动端等端口购买XXX提供的有偿服务（产品）。根据您所订购产品的具体信息(以订购当时XXX官网公示为准)，包括但不限于课程内容、课程安排、价格、退款政策等，在您支付完成后，将由XXX系统后台生成1份电子订单，该电子订单系本协议之有效组成部分，是确定用户与XXX各自权利义务的有效依据。支付完成后您即可根据所购买课程享受XXX提供的各项服务。XXX针对部分课程，可能会需要向您邮寄提供教材、讲义等课程资料，因此请您在提交订单前务必仔细核对收货人、收货地址及联系电话等信息。收货人与用户本人不一致的，收货人的行为和意思表示即视为用户的行为和意思表示，用户应对收货人的行为及意思表示的法律后果承担连带责任。</p><p>3.7.2.XXX的任何一个帐号都只能由同一个用户使用，禁止多个用户使用同一个帐号。若XXX有合理理由认为您的账号可能存在用户帐号被盗取、被盗用情形的，则XXX有权将此帐号暂时或永久作无效处理并保留追究法律责任的权利。若您将帐号借给他人使用，您应承担由此产生的全部责任，并与实际使用人承担连带责任。</p><p>3.7.3.您应在享受课程服务过程中自觉维护课堂秩序，不得作出、参与任何影响课堂正常秩序的行为。否则，XXX保留追究您责任的权利。情节严重者，XXX有权关闭其账号且不承担任何责任。</p><p>4.双方权利义务</p><p>4.1.XXX仅负责通过网络平台向您提供网上服务，除此之外与相关网络服务有关的设备(如个人电脑、手机、及其他与接入互联网或移动网有关的装置)及所需的费用(如为接入互联网而支付的电话费及上网费、为使用移动网而支付的手机费)均应由您自行负担。</p><p>4.2.您在XXX网络平台享有的部分网上服务（包括但不限于付费课程）可能受到有效期的限制，一旦有效期届满，该服务将会自动失效。请您在付费前仔细阅读相关条款。</p><p>4.3.您可以选择购买XXX提供的增值（付费）服务。您应当在付费前仔细阅读并同意关于该付费服务的相关条款，包括但不限于按照XXX的要求进行实名认证并同意将所填写的信息交由第三方机构进行校验。您应保证您所提供的资料和信息是真实、完整、有效的。</p><p>4.4.若您选择通过第三方支付平台等方式进行费用支付，在支付过程中因您自身原因或第三方支付平台原因造成的异常使您的帐号无法正常使用或遭受损失的，XXX对此概不负责。</p><p>4.5.XXX对于其通过网络平台所提供的网上服务的种类及内容拥有自主权。XXX有权随时更改经营模式、管理应用程序及内部功能。</p><p>4.5.1.由于考试大纲变化、师资变动等原因，XXX有权调整培训内容、授课老师。</p><p>4.5.2.XXX有权根据实际情况的变化调整课程设置，也有权调整服务提供流程 (包括但不限于退课、换课、赠课流程等)。</p><p>4.6.XXX可能会通过应用官方网站、客服电话、管理员、或者其他的途径，向您提供诸如课程说明、课程锁定或解除锁定、帐号申诉等客户服务，以上服务的提供应建立在以下前提条件之上：</p><p>(1)您应通过XXX客服官方网站或者提供的其他途径了解这些客户服务的内容、要求以及资费，谨慎选择是否需要享受相应的客户服务，向XXX真实地准确地表达您的需求；</p><p>(2)您应同意并接受XXX关于该等客户服务的专门协议或条款。</p><p>4.7.为高效利用服务器资源，若您长期未使用账号登录XXX网站，XXX有权视需要，在提前通知的情况下，对该账号及其账号下的数据及相关信息采取删除等处置措施，上述处置可能导致您对该账号下相关权益的丧失，对此XXX不承担任何责任。</p><p>4.8.您充分理解并同意接受XXX通过短信或其他方式向您发送XXX的相关商业信息。如您希望停止接收相关信息，可通过XXX官方网站公布的联系方式与XXX联系，XXX将在核实您的身份后取消推送。</p><p>5.用户行为规范</p><p>5.1.您除了可以按照本协议的约定使用XXX网上服务之外，不得进行任何侵犯XXX及组成元素相关的知识产权的行为，也不得进行任何其他有损于XXX或其他第三方合法权益的行为。</p><p>5.2.您仅可为非商业目的使用XXX网上服务，包括但不限于接收、下载、安装、启动、升级、登录、显示、运行和/或截屏XXX网站服务。</p><p>5.3.您不得以任何形式公开XXX提供的网上课程（包括但不限于向任何第三方透露学习课程、与他人共享账号、将自己的账号提供给第三方使用、将学习课程公开播放或以任何方式供多人同时使用）。上述情况一经发现，XXX有权立即关闭相应账号的学习权限，同时XXX会进一步追究您违规使用账号引起的法律责任。</p><p>5.4.在使用XXX网上服务的过程中，您必须遵守相关服务的具体使用规则，同时遵守以下基本行为规范，否则，XXX有权立即关闭相应账号的学习权限，并进一步追究您行为的法律责任。</p><p>(1)不得为任何非法目的而使用网络服务系统；</p><p>(2)遵守所有与网络服务有关的网络协议、规定和程序；</p><p>(3)不得利用XXX网络平台进行任何可能对互联网的正常运转造成不利影响的行为；</p><p>(4)不得利用XXX网络平台进行任何对该平台不利的行为。</p><p>5.5.您应当保证对您所发表或者上传于XXX网络平台的所有信息(即属于《中华人民共和国著作权法》规定的作品，包括但不限于文字、图片、音乐、电影、表演和录音录像制品和电脑程序等)均享有完整的知识产权，或者已经得到相关权利人的合法授权；若您违反本条规定造成本公司被第三人索赔的，您应全额补偿本公司一切费用(包括但不限于各种赔偿费、诉讼代理费及为此支出的其它合理费用)；当第三方认为您发表或者上传于XXX网络平台的信息侵犯其权利，并根据《信息网络传播权保护条例》或者相关法律规定向本公司发送权利通知书时，您同意本公司可以自行判断决定删除涉嫌侵权信息，除非您提交书面证据材料排除侵权的可能性，本公司将不会自动恢复上述删除的信息。</p><p>5.6.若因您违反本协议或相关服务条款的规定，导致或产生第三方主张的任何索赔、要求或损失，您应当独立承担责任；XXX因此遭受损失的，您也应当一并赔偿。</p><p>5.7.您必须严格遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国计算机信息系统安全保护条例》、《计算机软件保护条例》、《最高人民法院关于审理涉及计算机网络著作权纠纷案件适用法律若干问题的解释(法释[2004]1号)》、《全国人大常委会关于维护互联网安全的决定》、《互联网电子公告服务管理规定》、《互联网新闻信息服务管理规定》、《互联网著作权行政保护办法》和《信息网络传播权保护条例》等有关计算机互联网规定和知识产权的法律和法规、实施办法。</p><p>5.8.您不得在使用XXX网上服务的过程中在XXX网络平台的任何页面发布、转载、传送含有下列内容之一的信息：</p><p>（1）危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的；</p><p>（2）损害国家荣誉和利益的；</p><p>（3）煽动民族仇恨、民族歧视、破坏民族团结的；</p><p>（4）破坏国家宗教政策，宣扬邪教和封建迷信的；</p><p>（5）散布谣言、淫秽、色情、赌博、暴力、凶杀、恐怖或者教唆犯罪的；</p><p>（6）侮辱、诽谤他人，或侵害他人合法权利的；</p><p>（7）煽动非法集会、结社、游行、示威、聚众扰乱社会秩序的；</p><p>（8）其他违反法律、法规、规章、条例以及社会道德规范所限制或禁止的内容的。</p><p>5.9.若您在使用XXX网上服务的过程中违反上述任何规定，则XXX有权要求您改正或直接采取一切必要的措施(包括但不限于警告、限制或禁止使用全部或部分功能、账号封禁直至注销)以减轻不当行为而造成的影响，并公告处理结果；对于违反法律法规的行为，XXX有权向有关部门报告，您应独自承担由此产生的一切法律责任。因此导致的您账号下数据及相关信息被删除以及相关权益丧失的，该损失由您自行承担，对此XXX不承担任何责任。</p><p>5.10.您必须承担一切因您个人行为而直接或间接导致的法律责任。若您的行为给XXX造成损失的，应承担赔偿责任。</p><p>6.权利声明</p><p>6.1.所有XXX网络平台上的及XXX在提供网上服务的过程中使用的组成元素均属于XXX所有，并受版权、商标、专利和其它财产所有权法律的保护。严禁任何个人或单位在未经XXX许可的情况下对上述内容进行翻版、复制、转载、篡改等一切侵权行为。您只有在本公司授权下才能为自用目的合理使用这些内容，而不能擅自复制、再造这些内容、或创造与这些内容有关的衍生作品或产品，否则，将承担法律责任。</p><p>6.2.XXX对其专有内容、原创内容和其他通过授权取得的独占或者独家内容享有知识产权。未经XXX书面许可，任何单位和个人不得私自予以转载、传播或者有任何其他侵犯XXX知识产权的行为。否则，将承担法律责任。</p><p>6.3.若您使用XXX网络平台的任何内容，均应注明其“来源于XXX”并署上作者姓名，且与此相关的一切法律责任由您独立承担。XXX对所有作品享有用于其它用途的优先权，包括但不限于网站、电子杂志、平面出版等，但在使用前会通知作者，并按同行业的标准支付稿酬。您将该账号在任何时间段发表的任何形式的内容的著作财产权无偿授权给XXX使用，同时许可XXX有权就任何主体侵权而单独提起诉讼，并获得赔偿。本协议已经构成《著作权法》第二十五条所规定的书面协议，其效力及于您在XXX网站发布的任何受著作权法保护的内容。</p><p>6.4.您应保证您是在XXX上传或发表内容的著作权人或已取得合法授权，并且该内容不会侵犯任何第三方的合法权益。若第三方提出关于著作权的异议，XXX有权根据实际情况删除相关的内容，且有权追究您的法律责任。您的上述行为给XXX或任何第三方造成损失的，应负责全额赔偿。</p><p>6.5.为营造公平、健康的网络环境，在您使用XXX网上服务的过程中，XXX有权通过技术手段了解您的相关终端设备信息。一经发现有任何未经授权、危害XXX网上服务正常运营的相关程序，XXX将收集所有与此有关的信息并采取合理措施予以打击。</p><p>6.6.本站所有内容仅代表作者自己的立场和观点，与本站无关，由作者本人承担一切法律责任。恶意转载XXX网络平台上内容的，本站保留将其诉诸法律的权利。</p><p>6.7.“XXX”为XXX及其关联公司的注册商标，受中国法律保护。 对于“XXX”等商标，任何人不得擅自使用。违反上述声明而给XXX造成损失的，XXX将依法追究其法律责任。</p><p>7.免责声明</p><p>7.1.由于互联网各个环节存在不稳定因素，XXX无法保证其提供的网络服务一定能满足用户的要求，也不保证网络服务的及时性、安全性、准确性。</p><p>7.2.为方便用户，XXX网络平台可能会提供其他国际互联网网站或资源的链接，但XXX不保证前述网站或资源是否可以利用，亦不保证外部链接的准确性和完整性。同时，对于该等外部链接指向的不由XXX实际控制的任何网页上的内容，XXX不承担任何责任。若您因使用或依赖上述网站或资源受到损失或损害，XXX及XXX网络平台不承担任何责任。</p><p>7.3.对于因不可抗力或XXX不能控制的原因造成的网络服务中断或其它缺陷造成的损失，XXX不承担任何责任。由于地震、台风、洪水、火灾、战争、政府禁令以及其他不能预见并且对其发生和后果不能防止或避免的不可抗力原因，或互联网上的黑客攻击事件、计算机病毒、电信管制、停电，用户操作不当等非XXX原因，导致本服务条款不能履行或不能完全履行，XXX不承担责任。</p><p>7.4.XXX有权于任何时间暂时或永久修改或终止部分或全部非付费服务，而无论其通知与否，XXX对您和任何第三人均无需承担任何责任。</p><p>7.5.XXX可根据知悉或掌握的信息独立决定随时变更、终止、中止您对任何XXX网上服务的使用，无须向您发出任何提前通知，但根据法律法规规定、本协议或具体服务规则需要提前通知的除外。XXX无需向您承担与此相关的任何责任，且有权要求您承担相应责任。</p><p>7.6.XXX网上服务可能因软件漏洞、缺陷、版本更新缺陷、第三方病毒攻击、互联网连接或其他任何因素导致您的账号数据发生异常。在数据异常的原因未得到查明前，XXX有权暂时冻结账号，且XXX无须向您承担任何责任。</p><p>7.7.XXX不对您与第三方交易的行为负责，包括但不限于您通过购买、接受赠与或者其他的方式从任何第三方获得产品、服务等，并且不受理因任何第三方交易发生纠纷而带来的申诉。</p><p>7.8.在您使用XXX网上服务期间所存在的风险及一切后果将完全由用户本人承担。XXX对此不承担任何责任。</p><p>7.8.1.在使用本协议项下服务的过程中，您可能会遇到网络信息或其他用户行为带来的风险，XXX不对任何信息的真实性、适用性、合法性承担责任，也不对因侵权行为给用户造成的损害负责。这些风险包括但不限于：来自他人匿名或冒名的含有威胁、诽谤、令人反感或非法内容的信息；遭受他人误导、欺骗或其他导致或可能导致的任何心理、生理上的伤害以及经济上的损失；其他因网络信息或用户行为引起的风险。</p><p>7.8.2.您经由XXX网络平台与广告商进行通讯联系或商业往来或参与促销活动的行为，完全属于您与广告商之间的行为，与XXX及XXX网络平台没有任何关系。若您因上述行为受到任何损害或损失，XXX或XXX网络平台不承担任何责任。</p><p>8.隐私政策</p><p>8.1.个人信息的范围包括但不限于：</p><p>(1)您在注册、报名或以其他形式使用XXX的网上服务时，根据XXX的要求提供的个人信息；</p><p>(2) 您在使用XXX网上服务、参加XXX活动或访问XXX网络平台时，XXX网络平台自动采集的技术信息，包括但不限于IP地址信息、位置信息、设备及软件信息等；</p><p>(3)XXX收集到的您使用XXX网络平台服务的有关数据，包括但不限于购买培训课程、参加培训课程、通过XXX网络平台分享的信息等；</p><p>(4)XXX通过其它合法途径获得的个人数据。</p><p>8.2.个人信息使用规则</p><p>8.3.您同意并授权XXX为履行本协议之目的收集和使用您的个人信息。XXX可能基于以下目的使用用户的个人信息：</p><p>(1)为提供服务的要求所必须；</p><p>(2)改进产品或服务；</p><p>(3)提供或推广XXX及其合作伙伴的产品和服务。</p><p>8.4.XXX承诺对您的注册资料严格保密，不以任何形式公开、透露注册用户的真实姓名、地址、电子邮箱等信息，但以下情况除外：</p><p>(1)事先获得用户的明确授权；</p><p>(2)为提供本协议项下的服务所必须；</p><p>(3)适用法律、法规、司法机关命令、法律程序或政府机关要求；</p><p>(4)因XXX自身合并、收购、资产转让或类似的交易导致用户信息转移；</p><p>(5)与XXX关联公司、合作方、为提供服务所必需的供应商分享。</p><p>(6)为维护社会公众的利益。</p><p>8.5.XXX不允许任何第三方以任何手段收集、编辑、出售或者无偿传播用户的个人信息。任何用户若从事上述活动，一经发现，XXX有权立即终止与该用户的服务协议，查封其账号。</p><p>8.6.XXX在对应用程序更新的过程中，可能自动调取、收集您的客户端软件版本信息等信息进行替换、修改、删除和/或补充。此种行为是软件更新的所必须的一种操作或步骤，若您不同意进行此种操作，请您不要进行更新；您的使用行为即视为您同意XXX进行此种操作。</p><p>8.7.XXX可能会与第三方合作向用户提供相关的网络服务，在此情况下，若该第三方同意承担与XXX同等的保护用户隐私的责任，则XXX有权将用户的注册资料等提供给该第三方。</p><p>9.管辖与法律适用</p><p>9.1.本协议的签订地为中华人民共和国湖南省长沙市。</p><p>9.2.出现本协议引起或与本协议有关争议时，双方应首先通过友好协商解决争议；协商不成的，可以向合同签订地人民法院提起诉讼。</p><p>9.3.本协议条款无论因何种原因部分无效或不具有执行力，其余条款仍有效并具有约束力。</p><p>9.4.本公司不行使、未能及时行使或者未充分行使本协议或者按照法律规定所享有的权利，不应被视为放弃该权利，也不影响本公司在将来行使该权利。</p><p>9.5.本协议根据现行中华人民共和国法律法规制定。如发生协议条款与中华人民共和国法律法规相抵触时，则这些条款将完全按法律法规的规定重新解释，但本协议的其它条款仍对XXX和用户具有法律约束力。</p><p>9.6.本协议解释权及修订权归XXX公司所有。</p><p>XXX有限公司</p><p>XXXX年XX月XX日</p>', NULL, 0, 5, 9, '2022-11-04 13:50:56', '2022-11-04 16:18:39', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('AccessKey', 'sms_access_key', NULL, NULL, 0, 6, 10, '2022-11-08 09:27:48', '2022-11-08 09:27:48', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('AccessKeySecret', 'sms_access_key_secret', NULL, NULL, 0, 6, 11, '2022-11-08 09:28:36', '2022-11-08 09:28:36', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('签名1', 'sms_sign_name_1', NULL, '短信验证码签名', 0, 6, 12, '2022-11-08 09:32:53', '2022-11-08 09:32:53', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('模板CODE1', 'sms_template_code_1', NULL, '模板内容：\n您的验证码为：${code}，祝您生活愉快。', 0, 6, 13, '2022-11-08 09:43:01', '2022-11-08 09:43:01', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('发送频率', 'sms_send_interval', '60', NULL, 0, 6, 14, '2022-11-08 22:45:24', '2022-11-08 22:45:24', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('有效时间', 'sms_valid_time', '180', NULL, 0, 6, 15, '2022-11-08 22:46:00', '2022-11-08 22:46:00', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('签名2', 'sms_sign_name_2', NULL, '通用短信签名', 0, 6, 16, '2022-11-15 22:33:51', '2022-11-15 22:33:51', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('模板CODE2', 'sms_template_code_2', NULL, '模板内容：您好，您的密码已经重置为${password}，请及时登录并修改密码。', 0, 6, 17, '2022-11-15 22:35:38', '2022-11-15 22:35:38', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('开发者Key', 'map_key', NULL, '申请好的Web端开发者Key，首次调用 load 时必填', 0, 8, 18, '2022-11-17 19:18:22', '2022-11-17 19:18:22', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('中心点位置', 'map_center', '[105.602725, 37.076636]', '设置地图的显示样式', 0, 8, 19, '2022-11-17 19:19:45', '2022-11-17 19:19:45', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('显示样式', 'map_style', 'amap://styles/normal', '初始化地图中心点位置', 0, 8, 20, '2022-11-17 19:20:16', '2022-11-17 19:20:16', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('地图级别', 'map_zoom', '5', '初始化地图级别', 0, 8, 21, '2022-11-17 19:33:01', '2022-11-17 19:33:01', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('地图模式', 'map_view_mode', '3D', '是否为3D地图模式', 0, 8, 22, '2022-11-17 19:34:04', '2022-11-17 19:34:04', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('俯仰角度', 'map_pitch', '20', '地图初始俯仰角度，有效范围 0 度- 83 度', 0, 8, 23, '2022-11-17 19:36:02', '2022-11-17 19:36:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('官方邮箱', 'wx_server_email', '2445667550@qq.com', NULL, 0, 9, 25, '2023-02-14 22:55:09', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('服务热线', 'wx_server_phone', NULL, NULL, 0, 9, 26, '2023-02-14 22:55:57', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('公司官网', 'wx_server_site', 'https://kinit.ktianc.top', NULL, 0, 9, 27, '2023-02-14 22:56:45', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('AppID', 'wx_server_app_id', NULL, NULL, 0, 9, 28, '2023-02-26 22:01:19', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('AppSecret', 'wx_server_app_secret', NULL, NULL, 0, 9, 29, '2023-02-26 22:01:46', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('邮箱账号', 'email_access', NULL, NULL, 0, 10, 34, '2023-02-26 22:01:46', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('邮箱口令', 'email_password', NULL, NULL, 0, 10, 35, '2023-02-26 22:01:46', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('邮箱服务器', 'email_server', 'smtp.163.com', NULL, 0, 10, 36, '2023-02-26 22:01:46', '2023-02-27 09:50:02', NULL, 0);
INSERT INTO `vadmin_system_settings` VALUES ('邮箱端口', 'email_port', '25', NULL, 0, 10, 37, '2023-02-26 22:01:46', '2023-02-27 09:50:02', NULL, 0);

-- ----------------------------
-- Table structure for vadmin_system_settings_tab
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_settings_tab`;
CREATE TABLE `vadmin_system_settings_tab`  (
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标题',
  `classify` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类键',
  `tab_label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'tab标题',
  `tab_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'tab标识符',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏',
  `disabled` tinyint(1) NOT NULL COMMENT '是否禁用',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_settings_tab_tab_name`(`tab_name` ASC) USING BTREE,
  INDEX `ix_vadmin_system_settings_tab_classify`(`classify` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统配置分类表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_system_settings_tab
-- ----------------------------
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '基础配置', 'web_basic', 0, 0, 1, '2022-10-31 19:52:45', '2022-10-31 19:52:45', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '百度统计', 'web_baidu', 1, 1, 2, '2022-10-31 19:52:45', '2022-10-31 19:52:45', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '关于我们', 'web_about', 1, 0, 3, '2022-10-31 19:52:45', '2022-10-31 19:52:45', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '隐私政策', 'web_privacy', 0, 0, 4, '2022-10-31 19:52:45', '2022-10-31 19:52:45', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '用户协议', 'web_agreement', 0, 0, 5, '2022-10-31 19:52:45', '2022-10-31 19:52:45', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('阿里云配置', 'aliyun', '短信配置', 'aliyun_sms', 0, 0, 6, '2022-11-08 09:26:15', '2022-11-08 09:26:15', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('阿里云配置', 'aliyun', '对象存储', 'aliyun_oss', 1, 0, 7, '2022-11-08 09:26:34', '2022-11-08 09:26:34', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('地图配置', 'map', '用户分布', 'map_distribution', 1, 0, 8, '2022-11-17 19:16:59', '2022-11-17 19:16:59', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '微信服务端小程序', 'wx_server', 0, 0, 9, '2023-02-14 22:53:18', '2023-02-14 22:53:18', NULL, 0);
INSERT INTO `vadmin_system_settings_tab` VALUES ('系统配置', 'web', '邮箱配置', 'web_email', 0, 0, 10, '2023-02-14 22:53:18', '2023-02-14 22:53:18', NULL, 0);

SET FOREIGN_KEY_CHECKS = 1;
