/*
 Navicat Premium Data Transfer

 Source Server         : aliyun-mysql
 Source Server Type    : MySQL
 Source Server Version : 80018 (8.0.18)
 Source Host           : rm-bp181adf0phw2o0r05o.mysql.rds.aliyuncs.com:3306
 Source Schema         : test_kinit

 Target Server Type    : MySQL
 Target Server Version : 80018 (8.0.18)
 File Encoding         : 65001

 Date: 23/11/2022 22:25:06
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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('');

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
  `hidden` tinyint(1) NULL DEFAULT NULL COMMENT '是否隐藏',
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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `alwaysShow` tinyint(1) NULL DEFAULT NULL COMMENT '当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式，\n    只有一个时，会将那个子路由当做根路由显示在侧边栏，若你想不管路由下面的 children 声明的个数都显示你的根路由，\n    你可以设置 alwaysShow: true，这样它就会忽略之前定义的规则，一直显示根路由(默认 true)',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_menu_id`(`id` ASC) USING BTREE,
  INDEX `parent_id`(`parent_id` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_menu_perms`(`perms` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_menu_title`(`title` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `vadmin_auth_menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_auth_menu
-- ----------------------------

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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_role_id`(`id` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_role_name`(`name` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_role_role_key`(`role_key` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_auth_role
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_auth_role_menus
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_role_menus`;
CREATE TABLE `vadmin_auth_role_menus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  PRIMARY KEY (`id`, `role_id`, `menu_id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_role_menus_id`(`id` ASC) USING BTREE,
  INDEX `menu_id`(`menu_id` ASC) USING BTREE,
  INDEX `role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_role_menus_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `vadmin_auth_menu` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_role_menus_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 47 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_user_id`(`id` ASC) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_user_telephone`(`telephone` ASC) USING BTREE,
  INDEX `ix_vadmin_auth_user_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_auth_user_roles
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_auth_user_roles`;
CREATE TABLE `vadmin_auth_user_roles`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `role_id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_auth_user_roles_id`(`id` ASC) USING BTREE,
  INDEX `role_id`(`role_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_auth_user_roles_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `vadmin_auth_role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `vadmin_auth_user_roles_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_auth_user_roles
-- ----------------------------

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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家',
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '县',
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '城市',
  `county` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '区/县',
  `operator` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运营商',
  `postal_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮政编码',
  `area_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地区区号',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_record_login_id`(`id` ASC) USING BTREE,
  INDEX `ix_vadmin_record_login_telephone`(`telephone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 531 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '登录记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_record_login
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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_record_sms_send_id`(`id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_record_sms_send_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `vadmin_auth_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '短信发送记录表' ROW_FORMAT = DYNAMIC;

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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_dict_details_id`(`id` ASC) USING BTREE,
  INDEX `dict_type_id`(`dict_type_id` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_details_label`(`label` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_details_value`(`value` ASC) USING BTREE,
  CONSTRAINT `vadmin_system_dict_details_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `vadmin_system_dict_type` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典详情表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_system_dict_details
-- ----------------------------

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
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_dict_type_id`(`id` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_type_dict_name`(`dict_name` ASC) USING BTREE,
  INDEX `ix_vadmin_system_dict_type_dict_type`(`dict_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典类型表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_system_dict_type
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_system_settings
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_settings`;
CREATE TABLE `vadmin_system_settings`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `config_label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '配置表标签',
  `config_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '配置表键',
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '配置表内容',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注信息',
  `tab_id` int(11) NULL DEFAULT NULL COMMENT '关联tab标签',
  `disabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否禁用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_settings_id`(`id` ASC) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_settings_config_key`(`config_key` ASC) USING BTREE,
  INDEX `tab_id`(`tab_id` ASC) USING BTREE,
  CONSTRAINT `vadmin_system_settings_ibfk_1` FOREIGN KEY (`tab_id`) REFERENCES `vadmin_system_settings_tab` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_system_settings
-- ----------------------------

-- ----------------------------
-- Table structure for vadmin_system_settings_tab
-- ----------------------------
DROP TABLE IF EXISTS `vadmin_system_settings_tab`;
CREATE TABLE `vadmin_system_settings_tab`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `create_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '标题',
  `tab_label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'tab标题',
  `hidden` tinyint(1) NULL DEFAULT NULL COMMENT '是否隐藏',
  `classify` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类键',
  `tab_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'tab标识符',
  `disabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否禁用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_settings_tab_id`(`id` ASC) USING BTREE,
  UNIQUE INDEX `ix_vadmin_system_settings_tab_tab_name`(`tab_name` ASC) USING BTREE,
  INDEX `ix_vadmin_system_settings_tab_classify`(`classify` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统配置分类表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of vadmin_system_settings_tab
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
