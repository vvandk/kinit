/*
 Navicat Premium Data Transfer

 Source Server         : mysql8.0 aliyun
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : rm-bp181adf0phw2o0r05o.mysql.rds.aliyuncs.com:3306
 Source Schema         : kinit

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 11/10/2022 09:04:38
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
INSERT INTO `alembic_version` VALUES ('203b11efd025');

-- ----------------------------
-- Table structure for vadmin_auth_menu
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_menu`;
CREATE TABLE `vadmin_auth_menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `component` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '前端组件地址',
  `path` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '前端路由地址',
  `hidden` tinyint(1) NULL DEFAULT NULL COMMENT '是否显示',
  `menu_type` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单类型',
  `parent_id` int(11) NULL DEFAULT NULL COMMENT '父菜单',
  `perms` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识',
  `order` int(11) NULL DEFAULT NULL COMMENT '排序',
  `disabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否禁用',
  `redirect` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '重定向地址',
  `noCache` tinyint(1) NULL DEFAULT NULL COMMENT '如果设置为true，则不会被 <keep-alive> 缓存(默认 false)',
  `breadcrumb` tinyint(1) NULL DEFAULT NULL COMMENT '如果设置为false，则不会在breadcrumb面包屑中显示(默认 true)',
  `affix` tinyint(1) NULL DEFAULT NULL COMMENT '如果设置为true，则会一直固定在tag项中(默认 false)',
  `noTagsView` tinyint(1) NULL DEFAULT NULL COMMENT '如果设置为true，则不会出现在tag中(默认 false)',
  `canTo` tinyint(1) NULL DEFAULT NULL COMMENT '设置为true即使hidden为true，也依然可以进行路由跳转(默认 false)',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_menu_id`(`id`) USING BTREE,
  INDEX `parent_id`(`parent_id`) USING BTREE,
  INDEX `ix_vadmin_auth_menu_perms`(`perms`) USING BTREE,
  INDEX `ix_vadmin_auth_menu_title`(`title`) USING BTREE,
  CONSTRAINT `vadmin_auth_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `vadmin_auth_menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_menu
-- ----------------------------
INSERT INTO `vadmin_auth_menu` VALUES (1, '2022-08-13 10:56:32', '2022-08-13 10:56:32', 'ant-design:dashboard-filled', '#', '/dashboard', 0, '0', NULL, NULL, 0, 0, '/dashboard/workbench', 0, 1, 0, 0, 0, 'router.dashboard');
INSERT INTO `vadmin_auth_menu` VALUES (4, '2022-08-13 11:22:47', '2022-08-13 11:22:47', NULL, 'views/Dashboard/Workplace', 'workbench', 0, '1', 1, NULL, 1, 0, NULL, 0, 1, 0, 0, 0, 'router.workplace');
INSERT INTO `vadmin_auth_menu` VALUES (9, '2022-09-22 17:21:30', '2022-09-22 17:21:30', '', 'views/vadmin/auth/menu/index', 'menu', 0, '1', 10, NULL, 1, 0, NULL, 0, 1, 0, 0, 0, 'router.menu');
INSERT INTO `vadmin_auth_menu` VALUES (10, '2022-09-22 22:53:52', '2022-09-22 22:53:52', 'ep:lock', '#', '/auth', 0, '0', NULL, NULL, 1, 0, '/auth/menu', 0, 1, 0, 0, 0, 'router.auth');
INSERT INTO `vadmin_auth_menu` VALUES (11, '2022-09-22 17:21:30', '2022-09-22 17:21:30', '', 'views/vadmin/auth/role/index', 'role', 0, '1', 10, NULL, 2, 0, NULL, 0, 1, 0, 0, 0, 'router.role');
INSERT INTO `vadmin_auth_menu` VALUES (12, '2022-09-22 17:21:30', '2022-10-01 15:39:00', '', 'views/vadmin/auth/user/index', 'user', 0, '1', 10, NULL, 3, 0, NULL, 0, 1, 0, 0, 0, 'router.user');
INSERT INTO `vadmin_auth_menu` VALUES (14, '2022-10-04 20:58:18', '2022-10-04 20:58:34', 'ant-design:setting-filled', '#', '/system', 0, '0', NULL, NULL, 2, 0, NULL, 0, 1, 0, 0, 0, '系统配置');
INSERT INTO `vadmin_auth_menu` VALUES (15, '2022-10-04 21:02:55', '2022-10-04 21:03:03', NULL, 'views/vadmin/system/dict/index', 'dict', 0, '1', 14, NULL, 0, 0, NULL, 0, 1, 0, 0, 0, '字典配置');
INSERT INTO `vadmin_auth_menu` VALUES (16, '2022-10-05 22:25:26', '2022-10-05 22:25:26', NULL, 'views/vadmin/system/dict/detail', 'dict/detail', 1, '1', 14, NULL, 2, 0, NULL, 0, 1, 0, 0, 0, '字典详情');
INSERT INTO `vadmin_auth_menu` VALUES (17, '2022-10-10 09:51:32', '2022-10-10 09:51:32', NULL, 'views/Home/Home', 'home', 1, '1', 14, NULL, 0, 0, NULL, 0, 1, 0, 0, 0, '个人主页');

-- ----------------------------
-- Table structure for vadmin_auth_role
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_role`;
CREATE TABLE `vadmin_auth_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称',
  `role_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '权限字符',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `is_admin` tinyint(1) NULL DEFAULT NULL COMMENT '是否为超级角色',
  `order` int(11) NULL DEFAULT NULL COMMENT '排序',
  `disabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否禁用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_role_id`(`id`) USING BTREE,
  INDEX `ix_vadmin_auth_role_name`(`name`) USING BTREE,
  INDEX `ix_vadmin_auth_role_role_key`(`role_key`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_role
-- ----------------------------
INSERT INTO `vadmin_auth_role` VALUES (1, '2022-08-13 10:58:18', '2022-10-09 15:03:34', '管理员', 'admin', NULL, 1, 0, 0);

-- ----------------------------
-- Table structure for vadmin_auth_role_menus
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_role_menus`;
CREATE TABLE `vadmin_auth_role_menus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  PRIMARY KEY (`id`, `role_id`, `menu_id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_role_menus_id`(`id`) USING BTREE,
  INDEX `menu_id`(`menu_id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  CONSTRAINT `vadmin_auth_role_menus_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `vadmin_auth_menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_role_menus_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_role_menus
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_auth_user
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_user`;
CREATE TABLE `vadmin_auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `telephone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `nickname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '昵称',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像',
  `gender` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否可用',
  `is_cancel` tinyint(1) NULL DEFAULT NULL COMMENT '是否注销',
  `is_reset_password` tinyint(1) NULL DEFAULT NULL COMMENT '是否已经重置密码，没有重置的，登陆系统后必须重置密码',
  `last_ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最后一次登录IP',
  `last_login` datetime NULL DEFAULT NULL COMMENT '最近一次登录时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_user_id`(`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_user_telephone`(`telephone`) USING BTREE,
  INDEX `ix_vadmin_auth_user_name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_user
-- ----------------------------
INSERT INTO `vadmin_auth_user` VALUES (3, '2022-08-11 20:17:04', '2022-10-10 20:56:11', '15020221010', 'kinit', 'admin', '$2b$12$Ce7eSUKIIl8DMKeDyNHyr.Dp4aesQCM70RePigRVEny1Eql31R0Cq', NULL, '1', 1, 0, 1, NULL, NULL);

-- ----------------------------
-- Table structure for vadmin_auth_user_roles
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_user_roles`;
CREATE TABLE `vadmin_auth_user_roles`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `role_id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_user_roles_id`(`id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `vadmin_auth_user_roles_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_user_roles_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_auth_user_roles
-- ----------------------------
INSERT INTO `vadmin_auth_user_roles` VALUES (1, 3, 1);

-- ----------------------------
-- Table structure for vadmin_record_login
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_record_login`;
CREATE TABLE `vadmin_record_login`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `telephone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `status` tinyint(1) NULL DEFAULT NULL COMMENT '是否登录成功',
  `ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登陆地址',
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登陆地点',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '浏览器',
  `system` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作系统',
  `response` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '响应信息',
  `request` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求信息',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_record_login_id`(`id`) USING BTREE,
  INDEX `ix_vadmin_record_login_telephone`(`telephone`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 174 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '登录记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_record_login
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_record_operation
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_record_operation`;
CREATE TABLE `vadmin_record_operation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `user` int(11) NULL DEFAULT NULL COMMENT '操作人',
  `status` tinyint(1) NULL DEFAULT NULL COMMENT '操作结果状态',
  `ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登陆地址',
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登陆地点',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '浏览器',
  `system` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作系统',
  `response` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '响应信息',
  `request` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求信息',
  `request_api` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求接口',
  `request_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求方式',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_record_operation_id`(`id`) USING BTREE,
  INDEX `user`(`user`) USING BTREE,
  CONSTRAINT `vadmin_record_operation_ibfk_1` FOREIGN KEY (`user`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '操作记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_record_operation
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_record_sms_send
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_record_sms_send`;
CREATE TABLE `vadmin_record_sms_send`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '操作人',
  `status` tinyint(1) NULL DEFAULT NULL COMMENT '发送状态',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '发送内容',
  `telephone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '目标手机号',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '失败描述',
  `scene` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '发送场景',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_record_sms_send_id`(`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `vadmin_record_sms_send_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '短信发送记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_record_sms_send
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_system_dict_details
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_dict_details`;
CREATE TABLE `vadmin_system_dict_details`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_default` tinyint(1) NULL DEFAULT NULL COMMENT '是否默认',
  `dict_type_id` int(11) NULL DEFAULT NULL COMMENT '关联字典类型',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `disabled` tinyint(1) NULL DEFAULT NULL COMMENT '字典状态，是否禁用',
  `order` int(11) NULL DEFAULT NULL COMMENT '字典排序',
  `label` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典标签',
  `value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典键值',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_dict_details_id`(`id`) USING BTREE,
  INDEX `dict_type_id`(`dict_type_id`) USING BTREE,
  INDEX `ix_vadmin_system_dict_details_label`(`label`) USING BTREE,
  INDEX `ix_vadmin_system_dict_details_value`(`value`) USING BTREE,
  CONSTRAINT `vadmin_system_dict_details_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `vadmin_system_dict_type` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典详情表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_system_dict_details
-- ----------------------------
INSERT INTO `vadmin_system_dict_details` VALUES (1, '2022-10-07 12:05:19', '2022-10-07 12:05:19', 0, NULL, NULL, 0, 0, '男', '0');
INSERT INTO `vadmin_system_dict_details` VALUES (2, '2022-10-07 12:07:43', '2022-10-07 12:08:02', 0, 1, NULL, 0, 0, '男', '0');
INSERT INTO `vadmin_system_dict_details` VALUES (4, '2022-10-08 13:55:32', '2022-10-08 13:55:32', 0, 1, NULL, 0, 1, '女', '1');
INSERT INTO `vadmin_system_dict_details` VALUES (5, '2022-10-08 14:05:15', '2022-10-08 14:05:38', 1, 2, NULL, 0, 0, '目录', '0');
INSERT INTO `vadmin_system_dict_details` VALUES (6, '2022-10-08 14:05:24', '2022-10-08 14:05:24', 0, 2, NULL, 0, 1, '菜单', '1');
INSERT INTO `vadmin_system_dict_details` VALUES (7, '2022-10-08 14:05:32', '2022-10-08 14:05:32', 0, 2, NULL, 0, 2, '按钮', '2');

-- ----------------------------
-- Table structure for vadmin_system_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_dict_type`;
CREATE TABLE `vadmin_system_dict_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `dict_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典名称',
  `dict_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字典类型',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `disabled` tinyint(1) NULL DEFAULT NULL COMMENT '字典状态，是否禁用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_dict_type_id`(`id`) USING BTREE,
  INDEX `ix_vadmin_system_dict_type_dict_name`(`dict_name`) USING BTREE,
  INDEX `ix_vadmin_system_dict_type_dict_type`(`dict_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典类型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vadmin_system_dict_type
-- ----------------------------
INSERT INTO `vadmin_system_dict_type` VALUES (1, '2022-10-05 22:03:43', '2022-10-08 13:57:16', '性别', 'sys_vadmin_gender', '', 0);
INSERT INTO `vadmin_system_dict_type` VALUES (2, '2022-10-08 13:57:32', '2022-10-08 13:57:32', '菜单类型', 'sys_vadmin_menu_type', NULL, 0);

SET FOREIGN_KEY_CHECKS = 1;
