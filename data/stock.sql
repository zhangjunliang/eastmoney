-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.26 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 stock 的数据库结构
CREATE DATABASE IF NOT EXISTS `stock` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `stock`;

-- 导出  表 stock.bk 结构
CREATE TABLE IF NOT EXISTS `bk` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `bk_name` varchar(200) DEFAULT '' COMMENT '板块名称',
  `bk_code` varchar(6) DEFAULT '' COMMENT '板块代码',
  `rate` decimal(10,2) DEFAULT '0.00' COMMENT '涨幅',
  `rate_3` decimal(10,2) DEFAULT '0.00' COMMENT '3日涨幅',
  `weight` tinyint(1) DEFAULT '0' COMMENT '权重',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `bk_code` (`bk_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1025 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 stock.daily_hot 结构
CREATE TABLE IF NOT EXISTS `daily_hot` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT '' COMMENT '名称',
  `code` varchar(6) DEFAULT '0' COMMENT '代码',
  `market` tinyint(1) DEFAULT '0' COMMENT '市场:0深证,1上证',
  `rank` tinyint(3) DEFAULT '0',
  `updated` date DEFAULT NULL COMMENT '更新时间',
  `price` decimal(10,2) DEFAULT NULL COMMENT '价格',
  `rate` decimal(10,2) DEFAULT '0.00' COMMENT '波动',
  `max_rate` decimal(10,2) DEFAULT '0.00' COMMENT '最大波动',
  `max_price` decimal(10,2) DEFAULT '0.00' COMMENT '最高价格',
  `min_price` decimal(10,2) DEFAULT '0.00' COMMENT '最低价格',
  `top_price` decimal(10,2) DEFAULT '0.00' COMMENT '当日最高价格',
  `low_price` decimal(10,2) DEFAULT '0.00' COMMENT '当日足底价格',
  `is_top` tinyint(1) DEFAULT '0' COMMENT '是否涨停:0否1是',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`updated`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 stock.daily_lhb 结构
CREATE TABLE IF NOT EXISTS `daily_lhb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT '' COMMENT '名称',
  `code` varchar(6) DEFAULT '0' COMMENT '代码',
  `market` tinyint(1) DEFAULT '0' COMMENT '市场:0深证,1上证',
  `remark` text,
  `updated` date DEFAULT NULL COMMENT '更新时间',
  `price` decimal(10,2) DEFAULT NULL COMMENT '价格',
  `rate` decimal(10,2) DEFAULT '0.00' COMMENT '波动',
  `max_rate` decimal(10,2) DEFAULT '0.00' COMMENT '最大波动',
  `max_price` decimal(10,2) DEFAULT '0.00' COMMENT '最高价格',
  `min_price` decimal(10,2) DEFAULT '0.00' COMMENT '最低价格',
  `top_price` decimal(10,2) DEFAULT '0.00' COMMENT '当日最高价格',
  `low_price` decimal(10,2) DEFAULT '0.00' COMMENT '当日足底价格',
  `is_top` tinyint(1) DEFAULT '0' COMMENT '是否涨停:0否1是',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`updated`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=307 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 stock.daily_lhb_list 结构
CREATE TABLE IF NOT EXISTS `daily_lhb_list` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(6) DEFAULT '0' COMMENT '代码',
  `department_code` varchar(20) DEFAULT '0' COMMENT '机构代码',
  `department_name` varchar(200) DEFAULT '' COMMENT '机构名称',
  `net` decimal(20,2) DEFAULT '0.00' COMMENT '净值',
  `buy` decimal(20,2) DEFAULT '0.00' COMMENT '买入',
  `sell` decimal(20,2) DEFAULT '0.00' COMMENT '卖出',
  `is_buy` tinyint(1) DEFAULT '0' COMMENT '是否买入:0否1是',
  `updated` date DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `lhb_code` (`code`,`department_name`,`department_code`,`net`,`buy`,`sell`,`updated`,`is_buy`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1807 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 stock.daily_top 结构
CREATE TABLE IF NOT EXISTS `daily_top` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT '' COMMENT '名称',
  `code` varchar(6) DEFAULT '0' COMMENT '代码',
  `market` tinyint(1) DEFAULT '0' COMMENT '市场:0深证,1上证',
  `updated` date DEFAULT NULL COMMENT '更新时间',
  `price` decimal(10,2) DEFAULT NULL COMMENT '价格',
  `rate` decimal(10,2) DEFAULT '0.00' COMMENT '波动',
  `max_rate` decimal(10,2) DEFAULT '0.00' COMMENT '最大波动',
  `max_price` decimal(10,2) DEFAULT '0.00' COMMENT '最高价格',
  `min_price` decimal(10,2) DEFAULT '0.00' COMMENT '最低价格',
  `top_price` decimal(10,2) DEFAULT '0.00' COMMENT '当日最高价格',
  `low_price` decimal(10,2) DEFAULT '0.00' COMMENT '当日足底价格',
  `is_top` tinyint(1) DEFAULT '0' COMMENT '是否涨停:0否1是',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`updated`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  函数 stock.fromat_rate 结构
DELIMITER //
CREATE FUNCTION `fromat_rate`(rate DECIMAL(10,2)) RETURNS int(11)
begin 
    declare r int;
				select CASE 
					WHEN rate > 9 THEN
							 9
					WHEN rate > 5 THEN
							 5
					WHEN rate > 0 THEN
							 0
					WHEN rate > -5 THEN
							 -5
					WHEN rate > -9 THEN
							 -9				
					ELSE
							 -10
					END as r into r;
    return r;
end//
DELIMITER ;

-- 导出  表 stock.stock 结构
CREATE TABLE IF NOT EXISTS `stock` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT '' COMMENT '名称',
  `code` varchar(6) DEFAULT '0' COMMENT '代码',
  `market` tinyint(1) DEFAULT '0' COMMENT '市场:0深证,1上证',
  `price` decimal(10,2) DEFAULT '0.00' COMMENT '价格',
  `rate` decimal(10,2) DEFAULT '0.00' COMMENT '波动',
  `weight` int(10) DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6259 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 stock.stock_bk 结构
CREATE TABLE IF NOT EXISTS `stock_bk` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT '' COMMENT '名称',
  `code` varchar(6) DEFAULT '0' COMMENT '代码',
  `market` tinyint(1) DEFAULT '0' COMMENT '市场:0深证,1上证',
  `bk_name` varchar(200) DEFAULT '' COMMENT '板块名称',
  `bk_code` varchar(6) DEFAULT '' COMMENT '板块代码',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code_bk` (`code`,`bk_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=86998 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
