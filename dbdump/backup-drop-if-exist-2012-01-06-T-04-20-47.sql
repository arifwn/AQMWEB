-- MySQL dump 10.13  Distrib 5.5.16, for Linux (i686)
--
-- Host: localhost    Database: aqmweb
-- ------------------------------------------------------
-- Server version	5.5.16-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aqm_web_server`
--

DROP TABLE IF EXISTS `aqm_web_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aqm_web_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `address` varchar(100) NOT NULL,
  `port` int(11) NOT NULL,
  `server_task_id` int(11) NOT NULL,
  `server_info_id` int(11) NOT NULL,
  `server_status_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `aqm_web_server_52094d6e` (`name`),
  KEY `aqm_web_server_162a655c` (`server_task_id`),
  KEY `aqm_web_server_1c05d3b` (`server_info_id`),
  KEY `aqm_web_server_604dc6e7` (`server_status_id`),
  CONSTRAINT `server_info_id_refs_id_57930b27` FOREIGN KEY (`server_info_id`) REFERENCES `aqm_web_serverinfo` (`id`),
  CONSTRAINT `server_status_id_refs_id_17e94f2b` FOREIGN KEY (`server_status_id`) REFERENCES `aqm_web_serverstatus` (`id`),
  CONSTRAINT `server_task_id_refs_id_4e06beba` FOREIGN KEY (`server_task_id`) REFERENCES `aqm_web_servertask` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aqm_web_server`
--

LOCK TABLES `aqm_web_server` WRITE;
/*!40000 ALTER TABLE `aqm_web_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `aqm_web_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aqm_web_serverinfo`
--

DROP TABLE IF EXISTS `aqm_web_serverinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aqm_web_serverinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `max_cpu` int(11) NOT NULL,
  `max_memory` int(11) NOT NULL,
  `max_storage` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aqm_web_serverinfo`
--

LOCK TABLES `aqm_web_serverinfo` WRITE;
/*!40000 ALTER TABLE `aqm_web_serverinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `aqm_web_serverinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aqm_web_serverstatus`
--

DROP TABLE IF EXISTS `aqm_web_serverstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aqm_web_serverstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cpu` int(11) NOT NULL,
  `memory` int(11) NOT NULL,
  `storage` int(11) NOT NULL,
  `uptime` time NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aqm_web_serverstatus`
--

LOCK TABLES `aqm_web_serverstatus` WRITE;
/*!40000 ALTER TABLE `aqm_web_serverstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `aqm_web_serverstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aqm_web_servertask`
--

DROP TABLE IF EXISTS `aqm_web_servertask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aqm_web_servertask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_capacity` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aqm_web_servertask`
--

LOCK TABLES `aqm_web_servertask` WRITE;
/*!40000 ALTER TABLE `aqm_web_servertask` DISABLE KEYS */;
/*!40000 ALTER TABLE `aqm_web_servertask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aqm_web_servertask_current_queue`
--

DROP TABLE IF EXISTS `aqm_web_servertask_current_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aqm_web_servertask_current_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `servertask_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `servertask_id` (`servertask_id`,`task_id`),
  KEY `aqm_web_servertask_current_queue_36304d74` (`servertask_id`),
  KEY `aqm_web_servertask_current_queue_3ff01bab` (`task_id`),
  CONSTRAINT `servertask_id_refs_id_1bdb0879` FOREIGN KEY (`servertask_id`) REFERENCES `aqm_web_servertask` (`id`),
  CONSTRAINT `task_id_refs_id_4b5157c3` FOREIGN KEY (`task_id`) REFERENCES `wrf_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aqm_web_servertask_current_queue`
--

LOCK TABLES `aqm_web_servertask_current_queue` WRITE;
/*!40000 ALTER TABLE `aqm_web_servertask_current_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `aqm_web_servertask_current_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_5886d21f` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`),
  CONSTRAINT `user_id_refs_id_650f49a6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add flat page',8,'add_flatpage'),(23,'Can change flat page',8,'change_flatpage'),(24,'Can delete flat page',8,'delete_flatpage'),(25,'Can add log entry',9,'add_logentry'),(26,'Can change log entry',9,'change_logentry'),(27,'Can delete log entry',9,'delete_logentry'),(28,'Can add server task',10,'add_servertask'),(29,'Can change server task',10,'change_servertask'),(30,'Can delete server task',10,'delete_servertask'),(31,'Can add server info',11,'add_serverinfo'),(32,'Can change server info',11,'change_serverinfo'),(33,'Can delete server info',11,'delete_serverinfo'),(34,'Can add server status',12,'add_serverstatus'),(35,'Can change server status',12,'change_serverstatus'),(36,'Can delete server status',12,'delete_serverstatus'),(37,'Can add Server',13,'add_server'),(38,'Can change Server',13,'change_server'),(39,'Can delete Server',13,'delete_server'),(40,'Can add Domain',14,'add_domain'),(41,'Can change Domain',14,'change_domain'),(42,'Can delete Domain',14,'delete_domain'),(43,'Can add Setting',15,'add_setting'),(44,'Can change Setting',15,'change_setting'),(45,'Can delete Setting',15,'delete_setting'),(46,'Can add BaseSetting',16,'add_basesetting'),(47,'Can change BaseSetting',16,'change_basesetting'),(48,'Can delete BaseSetting',16,'delete_basesetting'),(49,'Can add PollutantParam',17,'add_pollutantparam'),(50,'Can change PollutantParam',17,'change_pollutantparam'),(51,'Can delete PollutantParam',17,'delete_pollutantparam'),(52,'Can add ChemData',18,'add_chemdata'),(53,'Can change ChemData',18,'change_chemdata'),(54,'Can delete ChemData',18,'delete_chemdata'),(55,'Can add AltMeteoData',19,'add_altmeteodata'),(56,'Can change AltMeteoData',19,'change_altmeteodata'),(57,'Can delete AltMeteoData',19,'delete_altmeteodata'),(58,'Can add Task',20,'add_task'),(59,'Can change Task',20,'change_task'),(60,'Can delete Task',20,'delete_task'),(61,'Can add TaskGroup',21,'add_taskgroup'),(62,'Can change TaskGroup',21,'change_taskgroup'),(63,'Can delete TaskGroup',21,'delete_taskgroup'),(64,'Can add TaskQueue',22,'add_taskqueue'),(65,'Can change TaskQueue',22,'change_taskqueue'),(66,'Can delete TaskQueue',22,'delete_taskqueue'),(67,'Can add profile',23,'add_profile'),(68,'Can change profile',23,'change_profile'),(69,'Can delete profile',23,'delete_profile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'arif','Arif Widi','Nugroho','arif@sainsmograf.com','sha1$b335d$27f2ed3f8f661a0deb68d8c476ab8c32cba5a3ad',1,1,1,'2012-01-06 01:58:01','2011-12-14 22:01:12');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`),
  CONSTRAINT `group_id_refs_id_f116770` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_7ceef80f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_dfbab7d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'flat page','flatpages','flatpage'),(9,'log entry','admin','logentry'),(10,'server task','aqm_web','servertask'),(11,'server info','aqm_web','serverinfo'),(12,'server status','aqm_web','serverstatus'),(13,'Server','aqm_web','server'),(14,'Domain','wrf','domain'),(15,'Setting','wrf','setting'),(16,'BaseSetting','wrf','basesetting'),(17,'PollutantParam','wrf','pollutantparam'),(18,'ChemData','wrf','chemdata'),(19,'AltMeteoData','wrf','altmeteodata'),(20,'Task','wrf','task'),(21,'TaskGroup','wrf','taskgroup'),(22,'TaskQueue','wrf','taskqueue'),(23,'profile','user_profile','profile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage`
--

DROP TABLE IF EXISTS `django_flatpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_a4b49ab` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage`
--

LOCK TABLES `django_flatpage` WRITE;
/*!40000 ALTER TABLE `django_flatpage` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_flatpage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage_sites`
--

DROP TABLE IF EXISTS `django_flatpage_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `flatpage_id` (`flatpage_id`,`site_id`),
  KEY `django_flatpage_sites_21210108` (`flatpage_id`),
  KEY `django_flatpage_sites_6223029` (`site_id`),
  CONSTRAINT `flatpage_id_refs_id_3f17b0a6` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`),
  CONSTRAINT `site_id_refs_id_4e3eeb57` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage_sites`
--

LOCK TABLES `django_flatpage_sites` WRITE;
/*!40000 ALTER TABLE `django_flatpage_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_flatpage_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('126a65524ec410dacd4119480302520c','ZDEzMTAxOTdmNWYzNDAwNmRlMDQ2OTRjZTg1ZWExZDk3MzU1MGE5MjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-01-16 01:52:03'),('496c2b7307ac91bbe64a896881d5d603','YmYwNDRmY2RjNzc2MmFjNTI1ZTk2YzQwZTczNDMwN2FlODVjMzVjNDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-01-18 12:07:39'),('e6b389a03ca4a827d535e0ff98a08172','ZDEzMTAxOTdmNWYzNDAwNmRlMDQ2OTRjZTg1ZWExZDk3MzU1MGE5MjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2012-01-20 01:58:01');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'localhost:8000','localhost');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_profile`
--

DROP TABLE IF EXISTS `user_profile_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_5bd41b6d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_profile`
--

LOCK TABLES `user_profile_profile` WRITE;
/*!40000 ALTER TABLE `user_profile_profile` DISABLE KEYS */;
INSERT INTO `user_profile_profile` VALUES (1,1,'image/profile/arif_pic.jpg');
/*!40000 ALTER TABLE `user_profile_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_altmeteodata`
--

DROP TABLE IF EXISTS `wrf_altmeteodata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_altmeteodata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `data` varchar(200) NOT NULL,
  `data_type` varchar(10) NOT NULL,
  `removed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_altmeteodata_52094d6e` (`name`),
  KEY `wrf_altmeteodata_403f60f` (`user_id`),
  KEY `wrf_altmeteodata_6c0716b5` (`data_type`),
  KEY `wrf_altmeteodata_733edf24` (`removed`),
  CONSTRAINT `user_id_refs_id_27dd8f39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_altmeteodata`
--

LOCK TABLES `wrf_altmeteodata` WRITE;
/*!40000 ALTER TABLE `wrf_altmeteodata` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_altmeteodata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_basesetting`
--

DROP TABLE IF EXISTS `wrf_basesetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_basesetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `namelist_wrf` longtext NOT NULL,
  `namelist_wps` longtext NOT NULL,
  `removed` tinyint(1) NOT NULL,
  `default` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_basesetting_52094d6e` (`name`),
  KEY `wrf_basesetting_403f60f` (`user_id`),
  KEY `wrf_basesetting_733edf24` (`removed`),
  KEY `wrf_basesetting_2b62b3d5` (`default`),
  CONSTRAINT `user_id_refs_id_710aa020` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_basesetting`
--

LOCK TABLES `wrf_basesetting` WRITE;
/*!40000 ALTER TABLE `wrf_basesetting` DISABLE KEYS */;
INSERT INTO `wrf_basesetting` VALUES (1,'Test Base Setting',1,'<p>Default WRF settings.</p>',' &time_control\r\n run_days                            = 0,\r\n run_hours                           = 48,\r\n run_minutes                         = 0,\r\n run_seconds                         = 0,\r\n start_year                          = 2010, 2010, 2010,\r\n start_month                         = 01,   01,   01,\r\n start_day                           = 14,   14,   14,\r\n start_hour                          = 00,   00,   00,\r\n start_minute                        = 00,   00,   00,\r\n start_second                        = 00,   00,   00,\r\n end_year                            = 2010, 2010, 2010,\r\n end_month                           = 01,   01,   01,\r\n end_day                             = 16,   16,   16,\r\n end_hour                            = 00,   00,   00,\r\n end_minute                          = 00,   00,   00,\r\n end_second                          = 00,   00,   00,\r\n interval_seconds                    = 21600\r\n input_from_file                     = .true.,.true.,.true.,\r\n history_interval                    = 60,   60,   60,\r\n frames_per_outfile                  = 19992, 1000, 1000,\r\n restart                             = .false.,\r\n restart_interval                    = 5000,\r\n auxinput5_interval_m                = 60, 60, 60\r\n io_form_history                     = 2\r\n io_form_restart                     = 2\r\n io_form_input                       = 2\r\n io_form_boundary                    = 2\r\n io_form_auxinput4                   = 0\r\n io_form_auxinput5                   = 0\r\n debug_level                         = 00\r\n /\r\n\r\n &domains\r\n time_step                           = 120,\r\n time_step_fract_num                 = 0,\r\n time_step_fract_den                 = 1,\r\n max_dom                             = 3,\r\n e_we                                = 122,   187,  157,\r\n e_sn                                = 122,   187,  157,\r\n e_vert                              = 28,    28,    28,\r\n dx                                  = 9000, 3000, 1000,\r\n dy                                  = 9000, 3000, 1000,\r\n p_top_requested                     = 5000,\r\n num_metgrid_levels                  = 27,\r\n num_metgrid_soil_levels             = 4,\r\n grid_id                             = 1,     2,     3,\r\n parent_id                           = 0,     1,     2,\r\n i_parent_start                      = 1,     31,    67,\r\n j_parent_start                      = 1,     31,    67,\r\n parent_grid_ratio                   = 1,     3,     3,\r\n parent_time_step_ratio              = 1,     3,     3,\r\n feedback                            = 1,\r\n smooth_option                       = 0\r\n /\r\n\r\n &physics\r\n mp_physics                          = 2,     2,     2,\r\n progn                               = 0,     0,     0,\r\n naer                                = 1e9\r\n ra_lw_physics                       = 1,     1,     1,\r\n ra_sw_physics                       = 2,     2,     2,\r\n radt                                = 30,    10,    10,\r\n sf_sfclay_physics                   = 1,     1,     1,\r\n sf_surface_physics                  = 2,     2,     2,\r\n bl_pbl_physics                      = 1,     1,     1,\r\n bldt                                = 1,     0,     0,\r\n cu_physics                          = 5,     5,     0,\r\n cudt                                = 1,     1,     1,\r\n isfflx                              = 1,\r\n ifsnow                              = 1,\r\n icloud                              = 1,\r\n surface_input_source                = 1,\r\n num_soil_layers                     = 4,\r\n sf_urban_physics                    = 0,     0,     0,\r\n maxiens                             = 1,\r\n maxens                              = 3,\r\n maxens2                             = 3,\r\n maxens3                             = 16,\r\n ensdim                              = 144,\r\n cu_rad_feedback                     = .true.,\r\n /\r\n\r\n &fdda\r\n /\r\n\r\n &dynamics\r\n w_damping                           = 1,\r\n diff_opt                            = 1,\r\n km_opt                              = 4,\r\n diff_6th_opt                        = 0,      0,      0,\r\n diff_6th_factor                     = 0.12,   0.12,   0.12,\r\n base_temp                           = 290.\r\n damp_opt                            = 0,\r\n zdamp                               = 5000.,  5000.,  5000.,\r\n dampcoef                            = 0.2,    0.2,    0.2\r\n khdif                               = 0,      0,      0,\r\n kvdif                               = 0,      0,      0,\r\n non_hydrostatic                     = .true., .true., .true.,\r\n moist_adv_opt                       = 1,      1,      1,     \r\n scalar_adv_opt                      = 1,      1,      1,     \r\n chem_adv_opt                        = 1,      1,      1,     \r\n /\r\n\r\n &bdy_control\r\n spec_bdy_width                      = 5,\r\n spec_zone                           = 1,\r\n relax_zone                          = 4,\r\n specified                           = .true., .false.,.false.,\r\n nested                              = .false., .true., .true.,\r\n /\r\n\r\n &grib2\r\n /\r\n\r\n &chem\r\n kemit                               = 19,\r\n chem_opt                            = 1,        1,	1,\r\n bioemdt                             = 30,       30,	30,\r\n photdt                              = 30,       30,	30,\r\n chemdt                              = 2.,       2.,	2.,\r\n frames_per_emissfile                = 36,\r\n io_style_emissions                  = 1,\r\n emiss_inpt_opt                      = 1,        1,	1,\r\n emiss_opt                           = 3,        3,	3,\r\n chem_in_opt                         = 0,        0,	0,\r\n phot_opt                            = 1,        1,	1,\r\n gas_drydep_opt                      = 1,        1,	1,\r\n aer_drydep_opt                      = 1,        1,	1,\r\n bio_emiss_opt                       = 1,        1,	1,\r\n dust_opt                            = 0,\r\n dmsemis_opt                         = 0,\r\n seas_opt                            = 0,\r\n gas_bc_opt                          = 1,        1,	1,\r\n gas_ic_opt                          = 1,        1,	1,\r\n aer_bc_opt                          = 1,        1,	1,\r\n aer_ic_opt                          = 1,        1,	1,\r\n gaschem_onoff                       = 1,        1,	1,\r\n aerchem_onoff                       = 1,        1,	1,\r\n wetscav_onoff                       = 0,        0,	0,\r\n cldchem_onoff                       = 0,        0,	0,\r\n vertmix_onoff                       = 1,        1,	1,\r\n chem_conv_tr                        = 1,        1,	1,\r\n biomass_burn_opt                    = 0,        0,	0,\r\n plumerisefire_frq                   = 30,       30,	30,\r\n aer_ra_feedback                     = 0,        0,	0,\r\n have_bcs_chem                       = .false., .false.,	.false.,\r\n /\r\n\r\n &namelist_quilt\r\n nio_tasks_per_group = 0,\r\n nio_groups = 1,\r\n /\r\n','&share\r\n wrf_core = \'ARW\',\r\n max_dom = 3,\r\n start_date = \'2010-01-14_00:00:00\',\'2010-01-14_00:00:00\',\'2010-01-14_00:00:00\',\'2010-01-14_00:00:00\',\'2010-01-14_00:00:00\',\r\n end_date   = \'2010-01-16_00:00:00\',\'2010-01-16_00:00:00\',\'2010-01-16_00:00:00\',\'2010-01-16_00:00:00\',\'2010-01-16_00:00:00\',\r\n interval_seconds = 21600\r\n io_form_geogrid = 2,\r\n/\r\n\r\n&geogrid\r\n parent_id         = 1,  1,   2,   \r\n parent_grid_ratio = 1,  3,   3,  \r\n i_parent_start    = 1,  31,  67,  \r\n j_parent_start    = 1,  31,  67,  \r\n e_we              = 122, 187,  157,  91,\r\n e_sn              = 122, 187,  157,  91,\r\n geog_data_res     = \'10m\', \'2m\',\'2m\',\r\n dx = 9000,\r\n dy = 9000,\r\n map_proj = \'mercator\',\r\n ref_lat   =  -6.9,\r\n ref_lon   = 107.58,\r\n truelat1  =  -15.0,\r\n truelat2  =  15.0,\r\n stand_lon = -98.0,\r\n geog_data_path = \'/backup/Documents/WRF/wps_data/geog\'\r\n opt_geogrid_tbl_path = \'geogrid/\'\r\n/\r\n\r\n&ungrib\r\n out_format = \'WPS\',\r\n prefix = \'FILE\',\r\n/\r\n\r\n&metgrid\r\n fg_name = \'FILE\'\r\n io_form_metgrid = 2, \r\n/\r\n',0,1);
/*!40000 ALTER TABLE `wrf_basesetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_chemdata`
--

DROP TABLE IF EXISTS `wrf_chemdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_chemdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `data` varchar(200) NOT NULL,
  `worksheets` longtext NOT NULL,
  `removed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_chemdata_52094d6e` (`name`),
  KEY `wrf_chemdata_403f60f` (`user_id`),
  KEY `wrf_chemdata_733edf24` (`removed`),
  CONSTRAINT `user_id_refs_id_7cba91e1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_chemdata`
--

LOCK TABLES `wrf_chemdata` WRITE;
/*!40000 ALTER TABLE `wrf_chemdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_chemdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_chemdata_parameters`
--

DROP TABLE IF EXISTS `wrf_chemdata_parameters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_chemdata_parameters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chemdata_id` int(11) NOT NULL,
  `pollutantparam_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chemdata_id` (`chemdata_id`,`pollutantparam_id`),
  KEY `wrf_chemdata_parameters_7ada4309` (`chemdata_id`),
  KEY `wrf_chemdata_parameters_48f40070` (`pollutantparam_id`),
  CONSTRAINT `chemdata_id_refs_id_25672aad` FOREIGN KEY (`chemdata_id`) REFERENCES `wrf_chemdata` (`id`),
  CONSTRAINT `pollutantparam_id_refs_id_6c288486` FOREIGN KEY (`pollutantparam_id`) REFERENCES `wrf_pollutantparam` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_chemdata_parameters`
--

LOCK TABLES `wrf_chemdata_parameters` WRITE;
/*!40000 ALTER TABLE `wrf_chemdata_parameters` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_chemdata_parameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_domain`
--

DROP TABLE IF EXISTS `wrf_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `dx` double DEFAULT NULL,
  `dy` double DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `ratio` int(11) DEFAULT NULL,
  `i_parent_start` int(11) DEFAULT NULL,
  `j_parent_start` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_domain_52094d6e` (`name`),
  KEY `wrf_domain_403f60f` (`user_id`),
  KEY `wrf_domain_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_id_56a6a88d` FOREIGN KEY (`parent_id`) REFERENCES `wrf_domain` (`id`),
  CONSTRAINT `user_id_refs_id_63db84a0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_domain`
--

LOCK TABLES `wrf_domain` WRITE;
/*!40000 ALTER TABLE `wrf_domain` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_pollutantparam`
--

DROP TABLE IF EXISTS `wrf_pollutantparam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_pollutantparam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pollutant` varchar(20) NOT NULL,
  `x` varchar(50) NOT NULL,
  `y` varchar(50) NOT NULL,
  `lat` varchar(50) NOT NULL,
  `lon` varchar(50) NOT NULL,
  `value` varchar(50) NOT NULL,
  `conversion_factor` double NOT NULL,
  `worksheet` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_pollutantparam`
--

LOCK TABLES `wrf_pollutantparam` WRITE;
/*!40000 ALTER TABLE `wrf_pollutantparam` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_pollutantparam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_setting`
--

DROP TABLE IF EXISTS `wrf_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `setting_json` longtext NOT NULL,
  `setting_version` longtext NOT NULL,
  `generated_namelist` longtext NOT NULL,
  `user_namelist_wrf` longtext NOT NULL,
  `user_namelist_wps` longtext NOT NULL,
  `base_setting_id` int(11) NOT NULL,
  `removed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_setting_52094d6e` (`name`),
  KEY `wrf_setting_403f60f` (`user_id`),
  KEY `wrf_setting_61c00162` (`base_setting_id`),
  KEY `wrf_setting_733edf24` (`removed`),
  CONSTRAINT `base_setting_id_refs_id_21d0aeae` FOREIGN KEY (`base_setting_id`) REFERENCES `wrf_basesetting` (`id`),
  CONSTRAINT `user_id_refs_id_6f28e09b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_setting`
--

LOCK TABLES `wrf_setting` WRITE;
/*!40000 ALTER TABLE `wrf_setting` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_task`
--

DROP TABLE IF EXISTS `wrf_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `period_start` datetime NOT NULL,
  `period_end` datetime NOT NULL,
  `projection` varchar(20) NOT NULL,
  `true_lat_1` double DEFAULT NULL,
  `true_lat_2` double DEFAULT NULL,
  `stand_lon` double DEFAULT NULL,
  `pole_lat` double DEFAULT NULL,
  `pole_lon` double DEFAULT NULL,
  `setting_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_task_52094d6e` (`name`),
  KEY `wrf_task_403f60f` (`user_id`),
  KEY `wrf_task_c0d3063` (`setting_id`),
  CONSTRAINT `setting_id_refs_id_502ed61` FOREIGN KEY (`setting_id`) REFERENCES `wrf_setting` (`id`),
  CONSTRAINT `user_id_refs_id_6cf674a9` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_task`
--

LOCK TABLES `wrf_task` WRITE;
/*!40000 ALTER TABLE `wrf_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_task_domains`
--

DROP TABLE IF EXISTS `wrf_task_domains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_task_domains` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`,`domain_id`),
  KEY `wrf_task_domains_3ff01bab` (`task_id`),
  KEY `wrf_task_domains_a2431ea` (`domain_id`),
  CONSTRAINT `domain_id_refs_id_21b1d404` FOREIGN KEY (`domain_id`) REFERENCES `wrf_domain` (`id`),
  CONSTRAINT `task_id_refs_id_591d5913` FOREIGN KEY (`task_id`) REFERENCES `wrf_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_task_domains`
--

LOCK TABLES `wrf_task_domains` WRITE;
/*!40000 ALTER TABLE `wrf_task_domains` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_task_domains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_taskgroup`
--

DROP TABLE IF EXISTS `wrf_taskgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_taskgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `running` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_taskgroup_52094d6e` (`name`),
  KEY `wrf_taskgroup_403f60f` (`user_id`),
  CONSTRAINT `user_id_refs_id_1c96fc7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_taskgroup`
--

LOCK TABLES `wrf_taskgroup` WRITE;
/*!40000 ALTER TABLE `wrf_taskgroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_taskgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_taskgroup_tasks`
--

DROP TABLE IF EXISTS `wrf_taskgroup_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_taskgroup_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskgroup_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskgroup_id` (`taskgroup_id`,`task_id`),
  KEY `wrf_taskgroup_tasks_3e06d245` (`taskgroup_id`),
  KEY `wrf_taskgroup_tasks_3ff01bab` (`task_id`),
  CONSTRAINT `taskgroup_id_refs_id_1ec107c0` FOREIGN KEY (`taskgroup_id`) REFERENCES `wrf_taskgroup` (`id`),
  CONSTRAINT `task_id_refs_id_564e01c6` FOREIGN KEY (`task_id`) REFERENCES `wrf_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_taskgroup_tasks`
--

LOCK TABLES `wrf_taskgroup_tasks` WRITE;
/*!40000 ALTER TABLE `wrf_taskgroup_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_taskgroup_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wrf_taskqueue`
--

DROP TABLE IF EXISTS `wrf_taskqueue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wrf_taskqueue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submitted_date` datetime NOT NULL,
  `processed_date` datetime DEFAULT NULL,
  `finished_date` datetime DEFAULT NULL,
  `is_running` tinyint(1) NOT NULL,
  `is_finished` tinyint(1) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wrf_taskqueue_6c84939d` (`submitted_date`),
  KEY `wrf_taskqueue_4c8cf863` (`is_running`),
  KEY `wrf_taskqueue_23950081` (`is_finished`),
  KEY `wrf_taskqueue_3ff01bab` (`task_id`),
  CONSTRAINT `task_id_refs_id_6ac909a3` FOREIGN KEY (`task_id`) REFERENCES `wrf_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wrf_taskqueue`
--

LOCK TABLES `wrf_taskqueue` WRITE;
/*!40000 ALTER TABLE `wrf_taskqueue` DISABLE KEYS */;
/*!40000 ALTER TABLE `wrf_taskqueue` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-01-06  4:20:48
