-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: landt60mt-2station
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `abrs_result_status`
--

DROP TABLE IF EXISTS `abrs_result_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abrs_result_status` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `SERIAL_NO` varchar(100) DEFAULT NULL,
  `ASSEMBLY_NO` varchar(100) DEFAULT NULL,
  `STATUS` int DEFAULT NULL,
  `COL1_NAME` varchar(255) DEFAULT 'OPEN TORQUE',
  `COL1_VALUE` varchar(255) DEFAULT NULL,
  `COL2_NAME` varchar(255) DEFAULT 'CLOSE TORQUE',
  `COL2_VALUE` varchar(255) DEFAULT NULL,
  `COL3_NAME` varchar(255) DEFAULT 'VALVE CYCLE TEST',
  `COL3_VALUE` varchar(255) DEFAULT NULL,
  `COL4_NAME` varchar(255) DEFAULT 'HYDRO SHELL TEST RESULT',
  `COL4_VALUE` varchar(255) DEFAULT NULL,
  `COL5_NAME` varchar(255) DEFAULT 'HYDRO SHELL TEST DURATION',
  `COL5_VALUE` varchar(255) DEFAULT NULL,
  `COL6_NAME` varchar(255) DEFAULT 'HYDRO SEAT P TEST RESULT',
  `COL6_VALUE` varchar(255) DEFAULT NULL,
  `COL7_NAME` varchar(255) DEFAULT 'HYDRO SEAT P TEST DURATION',
  `COL7_VALUE` varchar(255) DEFAULT NULL,
  `COL8_NAME` varchar(255) DEFAULT 'HYDRO SEAT N TEST RESULT',
  `COL8_VALUE` varchar(255) DEFAULT NULL,
  `COL9_NAME` varchar(255) DEFAULT 'HYDRO SEAT N TEST DURATION',
  `COL9_VALUE` varchar(255) DEFAULT NULL,
  `COL10_NAME` varchar(255) DEFAULT 'AIR SEAT P TEST RESULT',
  `COL10_VALUE` varchar(255) DEFAULT NULL,
  `COL11_NAME` varchar(255) DEFAULT 'AIR SEAT P TEST DURATION',
  `COL11_VALUE` varchar(255) DEFAULT NULL,
  `COL12_NAME` varchar(255) DEFAULT 'AIR SEAT N TEST RESULT',
  `COL12_VALUE` varchar(255) DEFAULT NULL,
  `COL13_NAME` varchar(255) DEFAULT 'AIR SEAT N TEST DURATION',
  `COL13_VALUE` varchar(255) DEFAULT NULL,
  `COL14_NAME` varchar(255) DEFAULT NULL,
  `COL14_VALUE` varchar(255) DEFAULT NULL,
  `COL15_NAME` varchar(255) DEFAULT NULL,
  `COL15_VALUE` varchar(255) DEFAULT NULL,
  `COL16_NAME` varchar(255) DEFAULT NULL,
  `COL16_VALUE` varchar(255) DEFAULT NULL,
  `COL17_NAME` varchar(255) DEFAULT NULL,
  `COL17_VALUE` varchar(255) DEFAULT NULL,
  `COL18_NAME` varchar(255) DEFAULT NULL,
  `COL18_VALUE` varchar(255) DEFAULT NULL,
  `COL19_NAME` varchar(255) DEFAULT NULL,
  `COL19_VALUE` varchar(255) DEFAULT NULL,
  `COL20_NAME` varchar(255) DEFAULT NULL,
  `COL20_VALUE` varchar(255) DEFAULT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT NULL,
  `CREATED_BY` varchar(100) DEFAULT NULL,
  `PUSHED_COLUMNS` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abrs_result_status`
--

LOCK TABLES `abrs_result_status` WRITE;
/*!40000 ALTER TABLE `abrs_result_status` DISABLE KEYS */;
INSERT INTO `abrs_result_status` VALUES (1,'877',NULL,0,'OPEN TORQUE',NULL,'CLOSE TORQUE',NULL,'VALVE CYCLE TEST',NULL,'HYDRO SHELL TEST RESULT',NULL,'HYDRO SHELL TEST DURATION',NULL,'HYDRO SEAT P TEST RESULT',NULL,'HYDRO SEAT P TEST DURATION',NULL,'HYDRO SEAT N TEST RESULT',NULL,'HYDRO SEAT N TEST DURATION',NULL,'AIR SEAT P TEST RESULT',NULL,'AIR SEAT P TEST DURATION',NULL,'AIR SEAT N TEST RESULT',NULL,'AIR SEAT N TEST DURATION',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'q12',NULL,0,'OPEN TORQUE',NULL,'CLOSE TORQUE',NULL,'VALVE CYCLE TEST',NULL,'HYDRO SHELL TEST RESULT',NULL,'HYDRO SHELL TEST DURATION',NULL,'HYDRO SEAT P TEST RESULT',NULL,'HYDRO SEAT P TEST DURATION',NULL,'HYDRO SEAT N TEST RESULT',NULL,'HYDRO SEAT N TEST DURATION',NULL,'AIR SEAT P TEST RESULT',NULL,'AIR SEAT P TEST DURATION',NULL,'AIR SEAT N TEST RESULT',NULL,'AIR SEAT N TEST DURATION',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'jkj',NULL,0,'OPEN TORQUE',NULL,'CLOSE TORQUE',NULL,'VALVE CYCLE TEST',NULL,'HYDRO SHELL TEST RESULT',NULL,'HYDRO SHELL TEST DURATION',NULL,'HYDRO SEAT P TEST RESULT',NULL,'HYDRO SEAT P TEST DURATION',NULL,'HYDRO SEAT N TEST RESULT',NULL,'HYDRO SEAT N TEST DURATION',NULL,'AIR SEAT P TEST RESULT',NULL,'AIR SEAT P TEST DURATION',NULL,'AIR SEAT N TEST RESULT',NULL,'AIR SEAT N TEST DURATION',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `abrs_result_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `abrs_value_table`
--

DROP TABLE IF EXISTS `abrs_value_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abrs_value_table` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `COL1_NAME` varchar(50) DEFAULT NULL,
  `COL1_VALUE` int DEFAULT NULL,
  `COL2_NAME` varchar(50) DEFAULT NULL,
  `COL2_VALUE` int DEFAULT NULL,
  `COL3_NAME` varchar(50) DEFAULT NULL,
  `COL3_VALUE` int DEFAULT NULL,
  `COL4_NAME` varchar(50) DEFAULT NULL,
  `COL4_VALUE` int DEFAULT NULL,
  `COL5_NAME` varchar(50) DEFAULT NULL,
  `COL5_VALUE` int DEFAULT NULL,
  `COL6_NAME` varchar(50) DEFAULT NULL,
  `COL6_VALUE` int DEFAULT NULL,
  `COL7_NAME` varchar(50) DEFAULT NULL,
  `COL7_VALUE` int DEFAULT NULL,
  `COL8_NAME` varchar(50) DEFAULT NULL,
  `COL8_VALUE` int DEFAULT NULL,
  `COL9_NAME` varchar(60) DEFAULT NULL,
  `COL9_VALUE` int DEFAULT NULL,
  `COL10_NAME` varchar(60) DEFAULT NULL,
  `COL10_VALUE` int DEFAULT NULL,
  `COL11_NAME` varchar(60) DEFAULT NULL,
  `COL11_VALUE` int DEFAULT NULL,
  `COL12_NAME` varchar(60) DEFAULT NULL,
  `COL12_VALUE` int DEFAULT NULL,
  `COL13_NAME` varchar(70) DEFAULT NULL,
  `COL13_VALUE` int DEFAULT NULL,
  `COL14_NAME` varchar(50) DEFAULT NULL,
  `COL14_VALUE` int DEFAULT NULL,
  `COL15_NAME` varchar(50) DEFAULT NULL,
  `COL15_VALUE` int DEFAULT NULL,
  `COL16_NAME` varchar(50) DEFAULT NULL,
  `COL16_VALUE` int DEFAULT NULL,
  `COL17_NAME` varchar(50) DEFAULT NULL,
  `COL17_VALUE` int DEFAULT NULL,
  `COL18_NAME` varchar(50) DEFAULT NULL,
  `COL18_VALUE` int DEFAULT NULL,
  `COL19_NAME` varchar(50) DEFAULT NULL,
  `COL19_VALUE` int DEFAULT NULL,
  `COL20_NAME` varchar(50) DEFAULT NULL,
  `COL20_VALUE` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abrs_value_table`
--

LOCK TABLES `abrs_value_table` WRITE;
/*!40000 ALTER TABLE `abrs_value_table` DISABLE KEYS */;
INSERT INTO `abrs_value_table` VALUES (1,'OPENING TORQUE TEST-OBSERVED',10,'CLOSE TORQUE TEST-OBSERVED',2,'VALVE CYCLES TEST-PERFORMED',30,'HIGH PRESSURE SHELL WATER TEST-WATER',4,'HIGH PRESSURE SHELL WATER TEST-DURATION',5,'HIGH PRESSURE PREFERRED SEAT WATER TEST-WATER',6,'HIGH PRESSURE PREFERRED SEAT WATER TEST-DURATION',7,'HIGH PRESSURE NON-PREFERRED SEAT WATER TEST-WATER',8,'HIGH PRESSURE NON-PREFERRED SEAT WATER TEST-DURATION',90,'LOW PRESSURE PREFERRED SEAT AIR/NITROGEN TEST-AIR',10,'LOW PRESSURE PREFERRED SEAT AIR/NITROGEN TEST-DURATION',11,'LOW PRESSURE NON-PREFERRED SEAT AIR/NITROGEN TEST-AIR',12,'LOW PRESSURE NON-PREFERRED SEAT AIR/NITROGEN TEST-DURATION',13,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `abrs_value_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alarm`
--

DROP TABLE IF EXISTS `alarm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alarm` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ALARM_ID` varchar(255) NOT NULL,
  `ALARM_NAME` varchar(255) NOT NULL,
  `ALARM_STATUS` varchar(45) NOT NULL,
  `ALARM_SEVERITY_LEVEL` varchar(45) NOT NULL,
  `CREATED_AT` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ALARM_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm`
--

LOCK TABLES `alarm` WRITE;
/*!40000 ALTER TABLE `alarm` DISABLE KEYS */;
INSERT INTO `alarm` VALUES (9,'ll','ujj','Enabled','Low','2026-02-07 09:57:35','2026-02-07 09:57:35');
/*!40000 ALTER TABLE `alarm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alarm_status`
--

DROP TABLE IF EXISTS `alarm_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alarm_status` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ALARM_CODE` int DEFAULT NULL,
  `ALARM_NAME` varchar(40) DEFAULT NULL,
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm_status`
--

LOCK TABLES `alarm_status` WRITE;
/*!40000 ALTER TABLE `alarm_status` DISABLE KEYS */;
INSERT INTO `alarm_status` VALUES (1,2,'LOW PRESSURE','2025-12-12 08:50:23'),(2,1,'Emergency Alarm','2025-12-12 08:52:23'),(3,1,'Emergency Alarm','2025-12-12 08:54:21'),(4,1,'Emergency Alarm','2025-12-12 08:56:19'),(5,1,'Emergency Alarm','2025-12-12 08:56:58'),(6,3,'high pressure','2025-12-12 09:11:53'),(7,1,'Emergency Alarm','2025-12-12 09:36:52'),(8,1,'Emergency Alarm','2025-12-12 09:54:18'),(9,1,'Emergency Alarm','2025-12-12 09:57:19'),(10,1,'Emergency Alarm','2025-12-12 10:05:19'),(11,1,'Emergency Alarm','2025-12-12 10:16:23'),(12,2,'LOW PRESSURE','2025-01-12 10:16:23'),(13,1,'Emergency Alarm','2025-01-12 10:16:23'),(14,2,'LOW PRESSURE','2026-01-12 08:31:58'),(15,1,'Emergency Alarm','2026-01-12 08:32:28'),(16,1,'Emergency Alarm','2026-01-12 08:46:38'),(17,2,'LOW PRESSURE','2026-01-12 08:47:12'),(18,2,'LOW PRESSURE','2026-01-12 08:48:47'),(19,2,'LOW PRESSURE','2026-01-12 08:50:25'),(20,2,'LOW PRESSURE','2026-01-12 08:50:48'),(21,1,'Emergency Alarm','2026-01-21 05:53:08'),(22,2,'LOW PRESSURE','2026-01-21 05:53:14'),(23,2,'LOW PRESSURE','2026-01-21 05:56:31'),(24,2,'LOW PRESSURE','2026-01-21 05:56:36'),(25,2,'LOW PRESSURE','2026-01-21 05:56:40'),(26,2,'LOW PRESSURE','2026-01-21 05:56:52'),(27,2,'LOW PRESSURE','2026-01-21 05:57:13'),(28,2,'LOW PRESSURE','2026-01-21 06:04:20'),(29,1,'Emergency Alarm','2026-01-21 06:15:49'),(30,2,'LOW PRESSURE','2026-01-21 06:15:55'),(31,3,'high pressure','2026-01-21 06:15:58'),(32,4,'Air Leak','2026-01-21 06:16:01'),(33,5,NULL,'2026-01-21 06:16:04'),(34,1,'Emergency Alarm','2026-01-21 06:16:10'),(35,1,'Emergency Alarm','2026-01-21 06:19:47'),(36,1,'Emergency Alarm','2026-01-30 11:47:41'),(37,2,'LOW PRESSURE','2026-01-30 11:47:47'),(38,2,'LOW PRESSURE','2026-01-30 11:51:05'),(39,2,'LOW PRESSURE','2026-01-30 12:08:35'),(40,2,'LOW PRESSURE','2026-01-30 12:12:24'),(41,2,'LOW PRESSURE','2026-01-30 12:12:32'),(42,2,'LOW PRESSURE','2026-01-30 12:14:30'),(43,2,'LOW PRESSURE','2026-01-30 12:19:18');
/*!40000 ALTER TABLE `alarm_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `TEST_CATEGORY_ID` int NOT NULL,
  `TEST_CATEGORY_NAME` varchar(255) DEFAULT NULL,
  `TEST_CATEGORY_MEDIUM` varchar(45) DEFAULT NULL,
  `PRESSURE_COLUMN_NAME` varchar(255) DEFAULT NULL,
  `DURATION_COLUMN_NAME` varchar(255) DEFAULT NULL,
  `CATEGORY_STATUS` varchar(45) DEFAULT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT NULL,
  `UPDATED_DATE` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`TEST_CATEGORY_ID`),
  UNIQUE KEY `CATEGORY_ID_UNIQUE` (`TEST_CATEGORY_ID`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,1,'HYDRO SHELL','Hydro','COL1_PRE','COL1_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(2,2,'AIR SHELL','Air','COL2_PRE','COL2_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(3,3,'AIR SEAT','Air','COL3_PRE','COL3_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(4,4,'HYDRO SEAT','Hydro','COL4_PRE','COL4_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(5,5,'BACK SEAT','Hydro','COL5_PRE','COL5_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(6,6,'DBB','Air','COL6_PRE','COL6_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(7,7,'DIB',NULL,'COL7_PRE','COL7_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(8,8,'CAVITY RELIEF','Air','COL8_PRE','COL8_DUR','ENABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(9,9,'GAS SHELL',NULL,'COL9_PRE','COL9_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(10,10,'GAS SEAT',NULL,'COL10_PRE','COL10_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(11,11,'SPARE 1',NULL,'COL11_PRE','COL11_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(12,12,'SPARE 2',NULL,'COL12_PRE','COL12_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(13,13,'SPARE 3',NULL,'COL13_PRE','COL13_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(14,14,'SPARE 4',NULL,'COL14_PRE','COL14_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22'),(15,15,'SPARE 5',NULL,'COL15_PRE','COL15_DUR','DISABLE','2025-10-25 05:30:49','2026-05-05 11:56:22');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `column_preferences`
--

DROP TABLE IF EXISTS `column_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `column_preferences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `table_key` varchar(100) NOT NULL,
  `order_json` text NOT NULL,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_table` (`username`,`table_key`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `column_preferences`
--

LOCK TABLES `column_preferences` WRITE;
/*!40000 ALTER TABLE `column_preferences` DISABLE KEYS */;
INSERT INTO `column_preferences` VALUES (1,'admin','shell_material','[\"SHELL MATERIAL NAME\", \"SHELL MATERIAL ID\", \"SHELL MATERIAL DESC\"]','2025-11-04 14:31:52');
/*!40000 ALTER TABLE `column_preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configuration_table`
--

DROP TABLE IF EXISTS `configuration_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuration_table` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `HMI_CONNECTION` varchar(20) DEFAULT NULL,
  `ABRS_CONNECTION` varchar(20) DEFAULT NULL,
  `GRAPH_PDF_REPORT` varchar(20) DEFAULT NULL,
  `VTR_PDF_REPORT` varchar(20) DEFAULT NULL,
  `VTR_CSV_REPORT` varchar(20) DEFAULT NULL,
  `REPORT_PATH` longtext,
  `AUTO_DB_BACKUP` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration_table`
--

LOCK TABLES `configuration_table` WRITE;
/*!40000 ALTER TABLE `configuration_table` DISABLE KEYS */;
INSERT INTO `configuration_table` VALUES (1,'Enabled','Enabled','Enabled','Enabled','Enabled','P:\\Bray_Reports','Enabled');
/*!40000 ALTER TABLE `configuration_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `current_status`
--

DROP TABLE IF EXISTS `current_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `current_status` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SERIAL_NO` varchar(255) DEFAULT NULL,
  `PRESSURE` decimal(18,3) DEFAULT NULL,
  `CLAMPING_PRESSURE` decimal(18,3) DEFAULT NULL,
  `TEST_ID` int DEFAULT NULL,
  `TEST_NAME` varchar(255) DEFAULT NULL,
  `DATE_TIME` timestamp NULL DEFAULT NULL,
  `CYCLE_COMPLETE` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_status`
--

LOCK TABLES `current_status` WRITE;
/*!40000 ALTER TABLE `current_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `current_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `current_status_station1`
--

DROP TABLE IF EXISTS `current_status_station1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `current_status_station1` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SERIAL_NO` varchar(255) DEFAULT NULL,
  `STATION` varchar(45) DEFAULT NULL,
  `PRESSURE` decimal(18,3) DEFAULT NULL,
  `CLAMPING_PRESSURE` decimal(18,3) DEFAULT NULL,
  `TEST_ID` int DEFAULT NULL,
  `TEST_NAME` varchar(255) DEFAULT NULL,
  `DATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `CYCLE_COMPLETE` int DEFAULT NULL,
  `TIMER_STATUS` int DEFAULT NULL,
  `TIMER_ON_OFF` varchar(50) DEFAULT NULL,
  `RESULT` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_test_valve` (`TEST_ID`,`VALVE_SERIAL_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_status_station1`
--

LOCK TABLES `current_status_station1` WRITE;
/*!40000 ALTER TABLE `current_status_station1` DISABLE KEYS */;
/*!40000 ALTER TABLE `current_status_station1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `current_status_station2`
--

DROP TABLE IF EXISTS `current_status_station2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `current_status_station2` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SERIAL_NO` varchar(255) DEFAULT NULL,
  `STATION` varchar(45) DEFAULT NULL,
  `PRESSURE` decimal(18,3) DEFAULT NULL,
  `CLAMPING_PRESSURE` decimal(18,3) DEFAULT NULL,
  `TEST_ID` int DEFAULT NULL,
  `TEST_NAME` varchar(255) DEFAULT NULL,
  `DATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `CYCLE_COMPLETE` int DEFAULT NULL,
  `TIMER_STATUS` int DEFAULT NULL,
  `TIMER_ON_OFF` varchar(50) DEFAULT NULL,
  `RESULT` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_test_valve` (`TEST_ID`,`VALVE_SERIAL_NO`),
  KEY `idx_test_valve_s2` (`TEST_ID`,`VALVE_SERIAL_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_status_station2`
--

LOCK TABLES `current_status_station2` WRITE;
/*!40000 ALTER TABLE `current_status_station2` DISABLE KEYS */;
/*!40000 ALTER TABLE `current_status_station2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-01 08:33:30.098367'),(2,'auth','0001_initial','2025-12-01 08:33:30.657403'),(3,'admin','0001_initial','2025-12-01 08:33:30.814445'),(4,'admin','0002_logentry_remove_auto_add','2025-12-01 08:33:30.821930'),(5,'admin','0003_logentry_add_action_flag_choices','2025-12-01 08:33:30.827373'),(6,'contenttypes','0002_remove_content_type_name','2025-12-01 08:33:30.931172'),(7,'auth','0002_alter_permission_name_max_length','2025-12-01 08:33:30.990815'),(8,'auth','0003_alter_user_email_max_length','2025-12-01 08:33:31.011012'),(9,'auth','0004_alter_user_username_opts','2025-12-01 08:33:31.016424'),(10,'auth','0005_alter_user_last_login_null','2025-12-01 08:33:31.076759'),(11,'auth','0006_require_contenttypes_0002','2025-12-01 08:33:31.080986'),(12,'auth','0007_alter_validators_add_error_messages','2025-12-01 08:33:31.088183'),(13,'auth','0008_alter_user_username_max_length','2025-12-01 08:33:31.159931'),(14,'auth','0009_alter_user_last_name_max_length','2025-12-01 08:33:31.225716'),(15,'auth','0010_alter_group_name_max_length','2025-12-01 08:33:31.243694'),(16,'auth','0011_update_proxy_permissions','2025-12-01 08:33:31.251468'),(17,'auth','0012_alter_user_first_name_max_length','2025-12-01 08:33:31.328428');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('07fa5ajlt7gr6zn9nuvoc56bobk2onb1','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.044295'),('0chwbtisxgm0km4524kwxl12927nf7nc','.eJwdzc0KgkAUBeB3ubhLKC2jhBZKLfrBokWUG5n0qpM6yb2jUdG7N3V258Dhe4PkRHS6RKVlKjRm4Gvq0AbCHAkJfBiCDR0jKdGgqSJrpDJTK5gfdzIHaK9VlrsJl8L1ppYz-sdylJqdi0sROLNecxqqoxuL1BrvWC83Ubgumz6Os-mhGg3KwV47gbeNwvy1uj2PtT6dCXlhGO5apB8PvmtDfS-kSghTAyfS2PPJ5wshwEEK:1voL8j:j89v-9yjRVpBnCshOimkMc6sQ76MJOUZJ5rVi98GCBY','2026-02-07 12:40:49.186784'),('0e0fxpbanfyhdhuw1ap06uu840owp5fg','e30:1vvtwY:5USB42gxci0paMdydLJAW5qq9EcEjo6xm1uAOiPY32Q','2026-02-28 09:15:30.758653'),('0kqxzden66nsl129jvf46sr4928emwxv','.eJwdzcFOwzAQBNB_WeXWiNhGLcESh0ZwaEEF9VCVXCyTbGLTxLXsTVBB_HsNO7fVaN4P2Kj0RAYd2UYTtiApTJhDwA4DBpBgiLwsCi7ublgKlyVjrJj1MKOii8cCcpgiBqdHTHXdjtall9cxfp1DGgT_cWo7oaLRYrnKOPu_jDtXHvv3fs3LmWJTub2odZPdvkR63O6qjRnnum5Xbye2MItX4uvl867qvp8-L_uBDseA8SExcfIY_niQIofh3FunAjYJVjbZ9_z3CkMhSoQ:1voZyF:qEtCIbpPWETtr0fItrwULclGA-40hr9nvIOZqs8vHHk','2026-02-08 04:30:59.207919'),('0nn8zb3qzbe9ia16gc19685gil64s3z7','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxfQ:1vLZ42:dl8igQmROcqogtOpPEUv4Ojglb0jf6M19TfXK4v0M9s','2025-12-03 03:41:02.207562'),('0ty688cf4d1qbpgmixmsgrzi0j7l37x6','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vQdrR:aa9K_kdoZvDFgt7mCFOfCOO49ksWUpwgbLywcZ_GUdM','2025-12-17 03:49:01.006411'),('0vm5zzvld05gzuf0xn34c675z7kcsg2z','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.273135'),('13ekrdruwqtpxzsj3cny9w94fba0bl25','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.175510'),('15k6h2x4nl4nntwbyjl3daiw8d4wq3rs','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxfQ:1vOvxn:0I6TFs4vCT9bDZ5Kuusmda7fjvobsJS3oVdxU21gAtw','2025-12-12 10:44:31.480361'),('1fqr4gpfjdm9dufvqx58my2fhvjrpow8','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1vky7l:XRlFkbGxXVpYe7SHznLR_X70jshqip8fPYvNmDhv6iU','2026-01-29 05:29:53.506123'),('1qhsraj8era0xxooe734v9fljm2fiv9r','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.250873'),('1qkpmegcxwbuj03euzbtv84gua8m0m15','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.200720'),('1unsekowqmoq4y1hn84bppot7varh7a8','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.376104'),('1uxwsbm6i1gdejxb8q4qpv21lptxy8wn','.eJyrViotTi3KS8xNVbICMw2VdJSKSwtSi0AcJStDIC81JzW5JDUlvjgjM60kPjMFqBKsCiZelphTlhpfUlmQCpE0UqoFADQEHhg:1vHh5A:hqSsxzNT_wPHRSN5tg1-9E2b-sN9nvYctYybGscFrTE','2025-11-22 11:26:12.025652'),('1x5rzwwtlbw87b3v9a6vwsuo0k83rxxz','.eJwdzUsLgkAUBeD_cnGnkNoDEVoktehBhYswNzLpVad0lHvHoqL_3tTZnQOH7w2SMzHoGpWWudBYQKhpQAcISyQkCGEEDgyMpESLpoqilcpMvWB-dGQO0F9uRelnXAt_OrM89x_LUypIqnO18IK75jxSsZ-K3BrvWC83-2hdt_c0LWbHm2vX9kF7i-l2H5Wv1fUZN_qUEPLcMDz0SD8eQt-BpqukyghzA2fS2MHk8wUhvUEJ:1vnc9j:rdF4NZJe2I9sIiuBz65lRSH5dtwiodt3_3v0FcOFHUM','2026-02-05 12:38:51.796137'),('20blfvugt8zwh83071r6lnjuvmzb00g9','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwic3VwZXJ1c2VyIjoyfQ:1vOwSx:nL1LKde4C7umgocQI2t1UMwdBXjGOz0MlL8wemmQWLQ','2025-12-12 11:16:43.626647'),('236khs0q0vset8y3794uaqx29i1zmy3q','e30:1w4YnU:tWuYZQgtPVu8ONnrlV6dJtizer_jK1pETMmG4LIhk3s','2026-03-24 06:29:56.853784'),('2743l72f1htz0gznr7z1uao0xzu62tmo','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.528918'),('2al3wnzdgfabd4relwk3vd3n05wjxb1c','e30:1vV4z5:wRA1zjGwyvd9nsE_JzEtDuREwfyy3v-xygAUVDppk6k','2025-12-16 09:35:15.754909'),('2f6499pdnqv9kg5wjvhxzucg550h0tox','.eJwdzU9Pg0AQBfDvMuFWIrtrQELSQ4ke_JNqejCVC9nCwK4tWzIz1Kjxu7s67zZ5eb9v8NzaRRwG8Z0V7KESWjAFwgEJCSpwInOVZdrcXKkYXZVKqcweiDNIYWGkYCeMRdtPPsTXbJk_zhSnYD4c-8G07KzJi0Sr_0t0COV-fBs3urwId3XYmcZ2yfUTy-3Dtr5306Vp-uLlqFZu9Sx6kz9u6-Hr7v1zd5LXPSGvI8PLjPTHQ2VSOJ1HH1rCLsKtj3Ze_PwCI3xH7g:1vjF5y:wb8Zym2bbGbouvizYQO3XEBF8s5x7jFmL9Fl4mK7-ts','2026-01-24 11:12:54.708941'),('2f7eg9gvbwqvbsrou7qbjwmb3a7fyj72','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZX0:1vKStr:Mye0dgaCjsMBxfUc3xzQY0osCBb4u40goTlN5rb21Ac','2025-11-30 02:53:59.751873'),('2nxs0wban5t2857yty752qfy8xbyxoo7','e30:1voL3t:OfJEHeqjbrD18k95h4f29Uedf3qWqrV52MWe5Edo74A','2026-02-07 12:35:49.658663'),('2ogud1yspoew8p8yjr3xicuuf99mbzsw','.eJwdzcFOwzAQBNB_sXJrRGyjlMgSh0ZwKKCCekAlF8skG9tt4lreTREg_h3Dzm01mvfNPGqzkINAvjcEA1OUFihZghESJKaYI4qqqoS8ueI5QjWc8wp9sBPoaCxUrGQLQgpmhtw3w-xDfkWD-HFOeZHF99MwSo3OyHpdCP5_hQihOdg3uxHNhbBvw152pi-un5DuHnbt1s2XrhvWLye-cqtnEpv6cdeOX_fHz_1Er4cEeJsZXCKkP54pWbLpbH3QCfoMa5_tWv78AoDQSsA:1vitzs:l38QICiVHpIH71-PZd0oRdwbvakZKn_8qs1mONtqUV0','2026-01-23 12:41:12.899680'),('2pf52inzwnfa4k7legy8gob46paxrt9r','e30:1vvtwY:5USB42gxci0paMdydLJAW5qq9EcEjo6xm1uAOiPY32Q','2026-02-28 09:15:30.758653'),('2qzzy333lcwuz8n3r1z4f0kg8gijrwrs','.eJwdzc1OwzAQBOB3WeXWiNhGbYMlDo3gwI8K6gGVXCI33sSmjROtN0WAeHdMd26r0Xw_4GNjZnYY2LeG0YJmmjEHwg4JCTQ45kkXhVTrK5EidSmEKKyJ7jAasgXkMEekYAZMbWMHH9JrMjF-jpT2YDocbaea6IxarjIpLpfJEMp9_95vZHnm2FZhp2rTZtfPke8et9WDG851bVevR7FwixeWm-XTtuq-7z--did-2xPG28TEeUL650GrHE5j70ND2Ca48cle3_z-Ac1JSfM:1vm4wo:VlJYve5zT3khAYEKph5i3QnJMipilW35UaenteJabwo','2026-02-01 06:59:10.962514'),('3621995hqfr649gsz1lobly2ysqh0awf','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.083471'),('3fg5tqln9c6h9tdjvb1vx17py91f3buw','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.466023'),('3wru2vwpi2kwcjg833qsrw0n5h9z4vtg','.eJwdzc0KgkAUBeB3ubhLyDGKEFooteiHChdhbmTSq07mJPeORkXv3tTZnQOH7w2KM9mbGrVRuTRYQGCoRxcISyQkCGAMLvSMpGWLtsqiVdpOnWR-3MkeoLs0RelnXEt_OnOE948jtJ4n1bkKxXwwnEc69lOZO5Mdm-VmH63rdkjTYnZsvFE9OhgRTrf7qHytrs_4Zk4JIS8sw32H9OMh8F243SulM8LcwpmytvDE5wtig0Ev:1vql64:cxE17iC-nzO-94Elufcg3gbTZUF58KhzzZuTFsEU_3Q','2026-02-14 04:48:04.755583'),('41f8fjqznfeicuyu040klb1iwn0xvzv5','.eJwdzc0KgkAUBeB3ubhLKKeMEFooteiHihZRbmTSq07qKPeORUXv3tTZnQOH7w2KE9mbErVRqTSYQWCoRxcIcyQkCGAILvSMpGWDtsqsUdpOnWR-tGQP0F2rLBcJl1L4U8cb_eN4Ws_OxaUIvdndcBrpo4hl6oy3bBbrXbQqm3scZ9NDNRqUg73xQn-zi_LX8vY81uZ0JuS5ZbjvkH48BMKFui2UTghTCyfK2hPx-QIhrUED:1viAz8:F-cQKnuBy6fY4iOWhlnqBt-kQ8Ulb5JgOOtlqfdvbBM','2026-01-21 12:37:26.110570'),('45nfky9mty6vyldoi822pklwtucmnx79','.eJxNyjsOgCAQhOGrmK1ttPQM3oEQGJGEh3FZE2O8u6CN5Xz_XBSyy1JUBLN2oInmFzoWY6otEqgnYexJx5a1jT5VYtmwN6dprAsBpsAqXv1SlLf1OdDPDx0OqHJu-OJI9wPpuyvY:1vIO6f:nw77omB3dJzu0r6vvsS_ycpPBJWllCtMSZ99EnM7tts','2025-11-24 09:22:37.085640'),('467crvc0mvyzkm4cdqmqvbmiw3jb7es0','.eJwdzUsLgkAUBeD_cnGnkGMPQmih1KIHFS7C3MikV53KSe4di4r-e1Nndw4cvjcozmVvGtRGFdJgCaGhHj0grJCQIIQBeNAzkpYt2irLVmk7dZL5cSN7gO50Kasg50YG44kj_H8cofU0rY91JKZ3w0WskyCThTPcsJmvtvGyae9ZVk72F99t3J0R0Xi9javX4vxMruaQEvLMMtx3SD8ewsCD661WOicsLJwra4_E5wshq0EC:1vhoX6:iPsGxsvrDW4VzxNCe_8MLkbIk1qQEaAGQItbUjwglXA','2026-01-20 12:39:00.470886'),('46dbx61npbtex5bxvpwcc7hf48or9e6x','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.246847'),('47x320vhvh1ltxwt7wc35y7rq62fcmcr','.eJwdzU9Lw0AQBfDvMuTWYHZXW8NCkQY9-IcqPUjNJazJJFnbbMLMpKLid3frvNvAe78f8Fy5WXoM4msn2IAVmjEFwhYJCSz0IpPNMm2uL1SMtrlSKmtHGrIbFid-DOsrSGFmpOAGjBXXDD7E1-SYP0eKozC9H5rWVNw7s1wlWv1fokPI991bt9H5Sbguws6Urk4un1huH7bFfT-cyrJZvRzUol88i94sH7dF-3338bU7yuuekNeR4XlCOvNgTQrHsfOhIqwjXPloa5P__gGhkEvc:1w4YjO:SwhtQcK-nO4bwVZvGLySgZ9MBFrcKMtWVma2vKpyWBE','2026-03-24 06:25:42.546611'),('4egst90c6p81lcu7owrrh76fomcfk6rk','.eJwdzc1OwzAQBOB3sXJrRGxXLZGlHhrBgR8V1AMquVgm2dimiWt5N0W04t0x7NxWo_muzKM2MzkI5DtD0DNFaYaSJRggQWKKOaKoqkrI2xueI1TNOa_QBzuCjsZCxUo2I6RgJsh9008-5Fc0iF-nlBdZ_Dj2g9TojFytC8H_rxAh1Af7breiPhN2TdjL1nTF8hnp7nHXPLjp3Lb9-vXIF27xQmK7eto1w-X-83s_0tshAW4yg3OE9MczJUs2nqwPOkGXYe2zLZc_v4DJSr4:1vZTUy:KWir4CW6BQmaq4J4sWVsHaTu4_N7F6bXHTjbNpX8il4','2025-12-28 12:34:20.823504'),('4h1kqok35a8wnk3366kurgizkdo77wk3','.eJyrViotTi3KS8xNVbJSKkstKcpU0lEqLi1ILQKJK1kZAnmpOanJJakp8cUZmWkl8ZkpQJWGSkjiZYk5ZanxJZUFqRBJC6VaAEPqHlg:1vEjR6:wx9ILwgM8tg5XdgmER53kF_-bbyedlPTN4UqwAcrKxE','2025-11-14 07:20:36.285786'),('4le0ew31cnlok9qmwewipjo4ie1seigb','.eJwdzc1OwzAQBOB3WeXWSHGCGgVLHBrBgR8V1AMquUSuvYlNEzvybooA8e4Y5jgazfcNjnq1skXPTitGA5LjijlEHDBiBAmWeZFFMQWtJhuIZSOEKIwiewoqmgJyWAmjVzOmtTKz86laFNFHiOkPltPZDFVPVlXbOivFf7LS--Y4vo27srkw6dYfqk7p7OqJ-PZh397b-dJ1pn45i43dPHO52z7u2-Hr7v3zMPHrMSLdJIbWBeMfD7LKYQqj831EneDeJfu6_vkFQxJMBg:1vp1Hj:xIGeiWYCOgLRqgzxM7H7rDbFx-pzHyMSVfqPsXiMg8k','2026-02-09 09:40:55.571466'),('4lhungrymhf0w8s53do6j9l45vb3doxo','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.569192'),('4m753gvw1bvngjbh5r1sg7iguoj18pmk','.eJwdzc0KgkAUBeB3ubhLyJlIQmiR1KIfKlpEuZFJrzqZo9w7FhW9e1Nndw4cvjdoTlVvKzRWZ8piDpGlHn0gLJCQIIIh-NAzklENuqryRhs3dYr50ZI7QHep80KmXCk5Dj0R_OMJYyan8lzOxORuOYvNQSYq80YbtvPVNl5WzT1J8nBfB4NqsLNiNl5v4-K1uD4PN3s8EfLUMdx3SD8eIunDrS21SQkzB6fa2UIGny9ih0Ew:1vyjcz:5OFZW7ID_HAYIbt0IJ97VH-VlwtYegqNKFtFvVlvDqI','2026-03-08 04:51:01.562672'),('4om7msxbg1hiofifpmrweai16sqzwrd3','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.921993'),('4wlqqhe9otnki4a54c1l5earviqccd46','.eJyrVsrJT88vLYnPTS0uTkxPVbJS8gELKBSXJicDxdJKc5R0lEqLU4vyEnNB0mWpJUWZQKHi0oLUIpC4kpVhLQCxmxm0:1vDawM:neJorvuYxn20yaySLwjDidlllDqcHC_YtHc5kBWbtWE','2025-11-11 04:04:10.846378'),('52p8j28fr87qz7jboapckjnek9uakw5i','eyJ1c2VybmFtZSI6InZldHJpIiwic3VwZXJ1c2VyIjoxfQ:1vDbSV:SrYdk0uHUwTKsblxZEZE6WDYGDKcdcb9w1yTaQbe8tk','2025-11-11 04:37:23.692885'),('540hl0dudcoug6z1mj1acfspph0wy335','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Ii8ifQ:1vzTvy:EEDLb6lA8PZeGr75nBRL9onehNVvJApJomOdQTJ4YZA','2026-03-10 06:17:42.603186'),('5k2lho8nxopjwbitkdio6n0v3xir0pzv','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.270619'),('5mmym138pka0ga81ppcmm4ud5q6fe11k','.eJwdjc1uwjAQhN9llRtRY7sCIksciMqhP6KIQ0VzsVxnExuIE9kbKqj67jWdOc1oNN8PuKj0RBY9OaMJG5AUJswhYIsBA0iwRKMsCi6WDyyZy5IxVkwRgzKDb11XQA736HWPaa-b3vlUjTrG7yGkRxi_Tk0rVLRazBcZZ__KuPflofvs1ry8UDSV34tam-zxLdLTy7Z6tv2lrpvF7sRmdvZOfD1_3VbtbXO87s_0cQgYVwkTpxHDHQ9S5HAeOudVQJPAyiU2F_z3D9mySwM:1vyqrK:tsa1xvVkOi_hGD7Wo_FjFgfZ245aru8bPOJfyJDOLQo','2026-03-08 12:34:18.216833'),('5qbumxkhu4kfrhe80ex9a3zfuwip73wd','.eJwdzcFOwzAQBNB_WeXWiNhGLcESh0ZwaEEF9VCVXCyTbGLTxLXsTSpA_HsNO7eVZt4P2Kj0RAYd2UYTtiApTJhDwA4DBpBgiLwsCi7ublgKlyVjrHB4UYOdUXndYwE5TBGD0yOmhm5H69LL6xgv55A2wX-c2k6oaLRYrjLO_i_jzpXH_r1f83Km2FRuL2rdZLcvkR63u2pjxrmu29XbiS3M4pX4evm8q7rvp8-v_UCHY8D4kJg4eQx_PEiRw3DurVMBmwQrm2wu7n-vgbNLzA:1w4Zfi:G7UH63bpBVkC98s1F4jVaDRKY3KkFAe7Tky-LuVjZVs','2026-03-24 07:25:58.820151'),('5qdezgagazhhhd0g4igkp6xumxsfp478','.eJyrViotTi3KS8xNVbICMw2VdJSKSwtSi0AcJStDIC81JzW5JDUlvjgjM60kPjMFqBKsCiZelphTlhpfUlmQCpOsBQA0AR4X:1vHdLJ:RDVxuEN5WB7pcyPi3_ijk_rKcrQL0Bh9iooN6BnSsfo','2025-11-22 07:26:37.729746'),('62pi6d4qoboj8kvmq90e0l0ilojluw0v','.eJwdzc1OwzAQBOB3WeXWiNhGKcESh0btgR8V1AMquVjG2cSmjWvZm6KCeHcMO7fVaL5vcEnpmSx6ckYT9iApzlhCxAEjRpBgiYKsKi5urlgOlw1jrEoXb1TQI1ZQwpwwej1hbut-cj6_gk7p8xTzHoT3Qz8IlawW9bLg7P8K7n2zH9_GFW_OlEzrd6LTprh-SrR-2Lb3djp3Xb98ObCFXTwTX9WP23b42nxcdkd63UdMd5lJc8D4x4MUJRxPo_Mqosmwctmub39-AdjJSgI:1vkfkI:ow4tBcpF_WKQQ8g0N4z_1S7jUId37HE-A0zqqf0sqZE','2026-01-28 09:52:26.603132'),('65266ikuzx57y64thuetgoqrgif0xbx3','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.524906'),('67bqi8q9w416hfyp25daqk2hztbjt8m2','.eJwdzc0KgkAUBeB3ubhLqJlIRGiR1KIfKlpEuZFJrzqZk9w7GhW9e1Nndw4cvjdoTlVnKzRWZ8piDpGlDn0gLJCQIIIh-NAxklENuqryRhs3tYr5cSd3gPZS54VMuVJyEnhi9I8njAlP5bmcibC3nMXmIBOVeeMN2_lqGy-rpk-SPNjXo0E12Fkxm6y3cfFaXJ-Hmz2eCHnqGO5apB8PkfThdi-1SQkzB6fa2UIGny9ik0E2:1w0uXn:THUAGfKURES4g3solw4joonSOZnYjBHLmq4q-L7U5Yc','2026-03-14 04:54:39.763304'),('6ainxkwd981u9keploke7q7ethpz1gzs','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.920481'),('6ej1h5xovalkpma1fjc8pqs9zs3c7sv1','.eJyrViotTi3KS8xNVbICMw2VdJSKSwtSi0AcJStDIC81JzW5JDUlvjgjM60kPjMFqBKsCiZelphTlhpfUlmQCpE0UqoFADQEHhg:1vHekv:LywHAZKeKtkbusSW5RtI7XJNrhpPD4qIuLreHCsYxY4','2025-11-22 08:57:09.333184'),('6kwhhximsnpg8q0234wooulyr96a6t7x','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.010815'),('6kxp031qfewjc1znmxpcldkk38sq4hu4','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.083471'),('6qesvaa9eo3u9um1l1vwv3jjgkbog8d5','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9kYXNoYm9hcmQvIn0:1vSuNf:dpwPHrRQuGAIUU_HwwoxmhvnR216hyBPL35KB62oP3E','2025-12-10 09:51:39.118981'),('6qivj8dxpnocf4ye7fm5e6wq42reujsc','.eJwdzc1OwzAQBOB3WeXWiNhGbaNIPTSCAz8qqAdUcolMvIlNGzfa3RQB4t0x7NxWo_m-IXBrZ_EYJXRW0EElNGMOhD0SElTgRaaqKLRZX6kUXZVKqYLFRmfJcQE5zIwU7Yipbd0YYnpNlvnjTGkPprej603L3prlKtPq_zIdY3kYXoetLi_CXR33prFddv3IcnO_q-_8eGkat3o-qoVfPIneLh92df91-_65P8nLgZA3ieF5QvrjoTI5nM5DiC1hl-A2JLtc__wC34VKDg:1vnwjQ:QyVEn70Z7AzbP33scl_sad83t9yzavQupO4cfWV6ZSs','2026-02-06 10:37:04.799539'),('7qbg7fyfxxiq5oepa62wtctoe3znygvf','eyJ1c2VybmFtZSI6ImFkbWluIiwic3VwZXJ1c2VyIjoyLCJpc19hdXRoZW50aWNhdGVkIjp0cnVlfQ:1vml3L:bAMcCCmPXa18KD7ec658R4E-pGFMGGDUe_cXKpW4aJE','2026-02-16 03:56:43.002982'),('7sqhzh7pk9u88m47sh60719ec8u0vl02','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1voL3t:QWRnk-7B_uKJOQF6iRO9UF4ErfRi6TSu0g8fjWnfp8A','2026-02-07 12:35:49.549482'),('7v899sgm506539n09kqq5qlj975fj1cj','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.382028'),('86ukvm7hrwztlcq64f0nz9kne4xt8y90','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.400249'),('8716txxw2u2q7d74qg3e12f4h2j0bgsb','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwic3VwZXJ1c2VyIjoyfQ:1vQ0xA:egnnJimCpWL3O1MDxE4ncQx05W0egZTOy5QoqY5WxFo','2025-12-15 10:16:20.123382'),('8dsn2773k463u7agxqlbl4i4j2a57w2s','e30:1vxjby:_xR-c13pS9Ud9adJBIxZ36l_S4NLNdfIs47L_ie5JcE','2026-03-05 10:37:50.419719'),('8l5sk84a2gr421rskkssymep9k7cdzqg','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1ve6Az:TMvIzsE07FhlD9gZS6f90Hdk7fjxtm1tqyJ1CDx838I','2026-01-10 06:40:49.729336'),('8ozt7rwlsoy6ztbkd1my08hqlw66duih','.eJwdzc0KgkAUBeB3ubhLKBWjhBZKLfqhokWUm2HSq07qJPeORUXv3tTZnQOH7w2KhexNhdqoTBrMITLUowuEBRISRDAEF3pG0rJFW2XeKm2nTjI_bmQP0F3qvPAFV9IPx443-sfxtJ6cynMZe5O74SzRBz-VmRNs2MxX22RZtfc0zcf7ejSoBjvjxeF6mxSvxfV5aMzxRMgzy3DfIf14iHwXmluptCDMLCyUtafB5wshvkEJ:1voL5z:1uY7LD19v3cXpcLe-KdtjA-R1LefMAw90uUqDnXO2hg','2026-02-07 12:37:59.617295'),('8pb2qacorm24qp9ir96zp7m9c7vrd53a','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vR0UF:Xnv3rZXvOu-N8jyIuvIFypscXLzuqzmyOgx0YTZclqY','2025-12-18 03:58:35.738689'),('8rkmj5qk10ies7yj7skvykgl8bkif4s8','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Ii8ifQ:1w4y3i:KqzFC3CqiEhtw1WRf_G9_hdSDA-m6LawIEQ8j_iLCcE','2026-03-25 09:28:22.733929'),('8ytuf8rzav7e5qc3uqm6xgoafpems7ux','.eJwdzc0KgkAUBeB3ubhLKA1FhBZJLfrBokWUG5n0qpM6yr2jUdG7N3V258Dhe4PkVAy6QqVlJjTmEGoa0AbCAgkJQpiCDQMjKdGiqSJvpTJTL5gfHZkD9Lc6L9yUK-F6vuXM_rEcpYJLeS2XTjBqziJ1chORWfM969U2jjZVOyZJ7h_r2aSaHLSz9HZxVLzW9-ep0ecLIS8Mw0OP9OMhdG1oulKqlDAzcCqNHQSfLyHFQQ0:1vnyNt:TjX4b9F3l_rQ_lKXCl1cAfcsdL5SNKMQU-G_R6II5QE','2026-02-06 12:22:57.101602'),('93ltbc6xida43cudhcag21ov56cexomz','.eJwdzUsLgkAUBeD_cnGXkA8UEVoktehBRYsoNzLpVSd1kntHo6L_3tTZnQOH7w2SMzHoGpWWudBYQKxpQBsISyQkiGEKNgyMpESHpoqik8pMvWB-3MkcoL82RellXAsvCC3X-cdylYrO1aWau9GoOU_U0UtFbvlb1ov1LlnV3ZimRXhonEk92Wt3Hmx2Sfla3p7HVp_OhDwzDA890o-H2LOhvVdSZYS5gTNpbN_5fAEhpkEA:1vbYrm:LxRfChXEkSlV1gI62-yLH6MhnRi-fhgMVvx2CBW-lkA','2026-01-03 06:42:30.652094'),('93ryayx0d2g8zukt5k17cmrupsxxenyh','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxLCJpc19hdXRoZW50aWNhdGVkIjp0cnVlfQ:1vNlwv:xN0HOi2XmPOwS2h6KF739X8t4P8qztWnGwmwk5MY3jU','2025-12-09 05:50:49.646324'),('99phsf413gwzs9papzoio1inpcv0izmw','e30:1vxjbv:YYQ5vY85X1DyVMzDDWFavP7mYbnOQimP8_VT8tIPgEs','2026-03-05 10:37:47.399005'),('9bgp8dpfh0a1oqznx80wrjep480fnwza','.eJwdzc1OwzAQBOB3sXJrRGyjhshSD43gwI8K6gGVXCI33sSmjRPtbooA8e4Ydm6r0XzfIlBrF_YQOXSWwQnDuEAuEHpAQGGEZ55NUSh9cyVTlKmklIWz5I-TRVeIXCwEGO0IqW3dGGJ6zZboY8K0J-bjyfW6JW_1usyU_L9MxVgdhrdhq6oLU1fHvW5sl10_Ed8-7Op7P16axpUvJ7nyq2dW2_Xjru6_7t4_92d-PSDQJjG0zIB_vDA6F-dpCLFF6BLchmSX6ucXzTZJ6g:1vl1pc:0zZtjanNUBmomdCfGIAt3WSKivNUR3Li-KEl2TytMK4','2026-01-29 09:27:24.263569'),('9j3ujtdl5e3rka9pfnft6rdy09j6ohji','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1vky7m:mbS1GEfyKm3I9yI--O6gtqDjaTZxXjma6AV2DyLK3Eg','2026-01-29 05:29:54.926890'),('9oyu5x7a4sqvk7kygvqmw8mj5kdn8m3n','.eJwdzc1OwzAQBOB3sXJrRGxXKZElDo3gwI8K6gGVXCI33sSmjRPtbooA8e4Ydm6r0XzfIlBrF_YQOXSWwQnDuEAuEHpAQGGEZ55NUSh9fSVTlKmklIWz5I-TRVeIXCwEGO0IqW3dGGJ6zZboY8K0J-bjyfW6JW91ucmU_L9MxVgdhrdhq6oLU1fHvW5sl62fiG8fdvW9Hy9N4zYvJ7nyq2dW2_JxV_dfd--f-zO_HhDoJjG0zIB_vDA6F-dpCLFF6BLchmSrdfnzCxcOShw:1wKdar:H-hvZoTwkbzlzic13DG2hOIkocGEgB2eoP6eEg2Gg6k','2026-05-07 14:51:21.611804'),('9qc4unh5akndgppedsktmqphcty3y631','.eJwdzcFOwzAQBNB_WeXWiNhGLZElDo3gUEAF9YBKLpFJNrHbxLW8myBA_DuGndtqNO8bHDVmZoueXWsYO9AcZ8whYo8RI2iwzEEXhVQ3VyJF6lIIUYxuwWAGLCCHmTB6M2Eqm25yPr2CIfq4xDQH4f3c9aoha9R6k0nxf5n0vjwOb8NWlgtTW_mDqk2bXT8R3z3sq52dlrruNi9nsbKrZ5bb9eO-6r_uT5-HkV-PEek2MTQHjH88aJXDeBmcbyK2CW5csqVUP7_IS0m8:1vxipH:SjwkiTbMF7oSAXiTA7X8lvWrrPhnSFEx5eVXJL0Ce1M','2026-03-05 09:47:31.908698'),('a13q7zw3mftqa799wfltw2ozlm9zf6oh','.eJwdzc0KgkAUBeB3ubhLyDGKElooteiHChdRbmTSq07pKPeORUXv3tTZnQOH7w2KU9mbCrVRmTSYQ2CoRxcICyQkCGAILvSMpGWDtsq8UdpOnWR-tGQP0F1ueeGnXEl_PHGE948jtJ6eynMZiundcBbp2E9k5oy2bBbrXbSqmnuS5JPDzRtUg70R4Xizi4rX8vqMa3M8EfLcMtx3SD8eAt-Fui2VTgkzC6fK2mL2-QIhskEH:1vV51D:3XmW7jdjvCHgC6TmwqMZlsVTEqbXbqE4ImDeCFU0DYg','2025-12-16 09:37:27.916623'),('a33fncgsg6aiwrigelhiuuict0f1vlst','.eJyrViotTi3KS8xNVbJSSkzJzcxT0lEqLi1ILQKJK1kZAXmpOanJJakp8cUZmWkl8ZkpQJWGSkjiZYk5ZanxJZUFqRBJI6VaADqbHjI:1vGbvY:GKkwLbtHdA66CHqWm5Gqesg52aeAAkFWOlEofckLK90','2025-11-19 11:43:48.122270'),('accquwm1otihro01ublzkl1vs0lbyba2','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.163682'),('adddq52iwjr1spw9eb7hb90b5mjhs22m','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vQ12G:ghWOZYZlZxc0o1IkIQEnQ9ca1z20Hx9zyGupYdubZvg','2025-12-15 10:21:36.855748'),('an28roruuxvdvm9hhwwiva68mwi2e51q','e30:1vky7h:1OVy00l2iFEGbCTMF1hVntT763Mpf_XWiG7wuIenEfc','2026-01-29 05:29:49.581854'),('arqcltr84zywj4zjst6vc758lwsgh866','e30:1veAAO:dZ1od7YsmQJrltzzHKRBCIK_6YNkJQQvGTnwDsuzbCM','2026-01-10 10:56:28.670648'),('au3oz9oq4kk85eplyb6y7l5hpcwn14eg','.eJwdzc0KgkAUBeB3ubhTyFGKEFooteiHChdhbmTSq07lJPeORUXv3tTZnQOH7w2KCzmYFrVRpTRYQWRoQA8IayQkiGAEHgyMpGWHtsqqU9pOvWR-3MgeoD9dqjoouJXBeOII_x9HaD3NmmMTi-ndcJnoNMhl6YQbNvPVNlm23T3Pq8n-4rutuzMiHq-3Sf1anJ_p1RwyQp5Zhoce6cdDFHhwvTVKF4SlhQtlbeGHny9ih0Ex:1vtm6v:D8RcmQQmZkM2i63PfES5-Mo85b5Iai9Ar5yFsSOue2M','2026-02-22 12:29:25.332212'),('ay2r0bdbko0sjkiu3mm42wqzmk8fl2z0','.eJyrVsrJT88vLYnPTS0uTkxPVbJS8gELKBSXJicDxdJKc5R0lEqLU4vyEnNB0okpuZl5QKHi0oLUIpC4kpVRLQCu_hmU:1vI08P:L3JBkxtR75uHjZBBlT5yQcpPHc1Y5m-R1QkBthXjnh4','2025-11-23 07:46:49.913708'),('ayechnqkgw6s1d4r9mt534ds92z44k6q','.eJwdzc0KgkAUBeB3ubhLqDEyEVootegHixZRbmTSq07lJPeORkXv3tTZnQOH7w2KM9mZGrVRuTRYQGioQxcISyQkCGEILnSMpGWDtsqiUdpOrWR-3MkeoD1fi9LLuJbexHfE6B9HaB0cq1MViaA3nMd676Uyd8YbNvNVEi_rpk_Twt9dR4N6sDUimqyTuHwtLs_9zRyOhDyzDHct0o-H0HPhdq-UzghzC2fK2kJMP19ikkE2:1vy78U:pbGF8WcEXsUsJBpnTnvwtwqOJiX0hYhE29jCzQh2CLs','2026-03-06 11:44:58.324334'),('b5cjdosn40qjbcfuzy5a6ksyzcs187bm','e30:1viqrR:uYYJEu-YFn43KcOcwyIPqxkAoqdws0cqE7ZN3fRnsYE','2026-01-23 09:20:17.954813'),('b79of3ki9f7rq581jo7fur4x4c3fvf3t','.eJwdyTsOgCAQhOGrmKlpaDmDdyAEVyThYdjdynh3wW7-bx6UnrqKr8QcEsFh_2FjjXHaqQUGyjRaqOte005ivWmsgLMGmX1QuahJjkHogJOh9H58iyKC:1vNpNJ:xv-HbhsJMUfCt-uSn0Zz-Pzl7f3NDfMYPGOTajd-Cvg','2025-12-09 09:30:17.759959'),('b9lr2j3m41vp708r394uh1fjufmhddne','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.968801'),('baowg1j4yzx5rghvqnvdigrr2x9n2hb8','.eJwdzc0KgkAUBeB3ubhLKEeUEFokteiHihZRbmTSq07qKPeORUXv3tTZnQOH7w2KUzmYCrVRmTSYQ2RoQBcICyQkiGAMLgyMpGWLtsq8VdpOvWR-dGQP0F_rvBApV1IEoeNN_nE8rafn8lLOvendcBbro0hk5vhbNov1Ll5V7T1J8vBQT0bVaG-8ebDZxcVreXseG3M6E_LMMjz0SD8eIuFC05VKp4SZhVNlbV98viGqQQI:1vc0F2:a2oZQ44rph-NSAyMPRXDNPIFcFBvOPGlmEZGnRn8K3I','2026-01-04 11:56:20.633879'),('bauyeeybs1i2ty5fhct6me71tf8qz67y','.eJwdzc0KgkAUBeB3ubhLKI1KhBZKLfrBwkWUG5n0qpM6yb2jUdG7N3V258Dhe4PkVPS6QqVlJjTm4Gvq0QbCAgkJfBiDDT0jKdGiqSJvpTJTJ5gfdzIH6K51XrgpV8KdzS1n8o_lKOWdy0sZON6gOQtV7CYis6Z71qttFG6qdkiSfH6sJ6NqdNBOMNtFYfFa355xo09nQl4ahvsO6ceD79rQ3EupUsLMwKk09nTx-QIhtEEH:1veBiX:s822uSjzNg_jyFqRDoxKzJrO5JBYU_wdW_r87mDVCh4','2026-01-10 12:35:49.725270'),('bbzsjiyfghiwgv0qvsv230f7bvywik7k','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxLCJpc19hdXRoZW50aWNhdGVkIjp0cnVlfQ:1vNV2E:aZKMlZgGNlk-04DArXSvkNpYDwkjHljfwMpKYtbCb5g','2025-12-08 11:47:10.215063'),('bdrmxg55t8kmh9vlazp5wl9d7sp6eunu','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1ve6Ag:kBmbCBIc091n2hUvs4QU7S4nMecq088Vu5pkH6TzkYQ','2026-01-10 06:40:30.639423'),('bhpmg9plkmvs1ggs6oex8j9j32yjhte8','eyJyZWZlcmVyIjoiLyIsImlzX2F1dGhlbnRpY2F0ZWQiOnRydWUsInVzZXJuYW1lIjoiYWRtaW4iLCJzdXBlcnVzZXIiOjJ9:1vmlYb:beIkP8mGLvIPNEwlF9oIrE7XFRsxQyIba6r5uvjxcJ0','2026-02-16 04:29:01.859352'),('bk4ok03n6ysc9ycl4hppb7vhlq5cqe7c','.eJwdzc0KgkAUBeB3ubhLKCcSE1ootegHixZRbmTSq07lJPeORkXv3tTZnQOH7w2KM9mZGrVRuTRYQGioQxcISyQkCGEILnSMpGWDtsqiUdpOrWR-3MkeoD1fi1JkXEsx8R1v9I_jaR0cq1MVeUFvOI_1XqQyd8YbNvNVEi_rpk_Twt9dR4N6sDVeNFkncflaXJ77mzkcCXlmGe5apB8PoXDhdq-UzghzC2fK2lPx-QIhvEEI:1voKxV:I-mXi7RlnBHBAkvxGX6HBp9h-YGC7spjaBELX0k8UJo','2026-02-07 12:29:13.582152'),('bqdjdlkyc18ams2erfkfyirf2ipglk4z','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.609943'),('brcjuklfvk75uc0ndzvf7mwlug3i9nhs','.eJwdzr0OgjAYheF7adhgoBgIIXGA6OBP0DAYZGkqFFqBQvq1GDXeu9Uzvstz3sgAU5KODCWINqOQyEMzBXhMqrFpvvVNGxDgNAgjB_v_OVjKuOyuXYrjRUOdySKoaO2sjqA3-zzb8XGpqiY6977L3ZPGaXjIs_a1vT-LQV9KxWBtGTAzUz8eJYGHBBBqNGdSi5pqZnGtDPPQMHVCEsVqe4gIm7Effb6QQD0s:1vwG6Y:Uy6VyP80U9f_H8LTDJEO5f14yTaByQApCHjBs6_Yxco','2026-03-01 08:55:18.082226'),('bx26ip6cpblxsbi5mz1j9osmxds5amiu','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1va7mO:zjgk2qxOG8Y36aVM0KvZQl2HN51jQE5Si1_QGqVnjNc','2025-12-30 07:35:00.814293'),('c0ivkb12ux0f7wvwsb0him543797pgna','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1vlfti:mGFVB6r_IAYMDMfcBwogm8ypHMzBwwfn0Q7iG1gQaAI','2026-01-31 04:14:18.774981'),('c7i7tvzm6zjc2uu27ss8vxc9783av463','.eJwdzV9LwzAUBfDvEvq2YpNIZwkMWdEH_zBlDzL7EmJ628S1acm9nUzxuxt3z9uFc34_zKM2CzkI5K0haJmiuEDOInQQITLFHNGsikLImyueIlTFOS_s2Q6g7TTOAxAUt0iG_BRwI1jOFoQYzAipbdrRh_SaDeLXFNM-mz-ObSc1OiPLdSb45TIRQnXo3_utqE6Etg572RibXT8j3T3u6gc3npqmXb8e-cqtXkhsy6dd3X3ff573A70dIuAmMbjMEP95pmTOhqn3QUewCdY-2UKWv3-b9FBd:1w0B2u:1J0r8VAoqVyGd1dpdW9ry5zy8y_NZ_15pSpP-nYYGZA','2026-03-12 04:19:44.533950'),('c82xogd7ieh34zuzouliijekd6wgw33j','.eJwdzUsLgkAUBeD_cnGXUDPRA6GFUoseVLSIciOTXnVKR7l3LCr6702d3Tlw-N6gOVGdLdFYnSqLGQSWOvSBMEdCggD64EPHSEbV6KrKam3c1CrmR0PuAO3lluUy4VLJ0dgTg388Ycz0VJyLUEzvltPIHGSsUm-4YTtfbaNlWd_jOBvvb4Ne2dtZEY7W2yh_La7PQ2WPJ0KeOYa7FunHQyB9qJpCm4QwdXCinS3k5PMFYpVBNw:1w4Xdm:wyRs5D8n1A3FDkLA7DyTrtDWu9UaMIjUaW_K2bwLqXg','2026-03-24 05:15:50.119405'),('can8dp4562v8oulgujpo12lpsjhkl1fw','.eJwdzc1OwzAQBOB3WeXWiNiuWiJLHBrBgR8V1AMquURuvIlNGydab4poxbtj2LmtRvNdwcfGzOwwsG8NowXNNGMOhB0SEmhwzJMuCqlub0SK1KUQorAmusNoyBaQwxyRghkwtY0dfEivycT4NVLag-lwtJ1qojNqtc6k-L9MhlDu-49-I8szx7YKO1WbNlu-RL5_2laPbjjXtV2_HcXCLV5ZblbP26q7PHx-7078vieMd4mJ84T0x4NWOZzG3oeGsE1w45Mtl_LnFxcGShg:1w5NXr:QZO8KCjwTCLXTO10uMifBHyRHpiUVpA1Ub6rj3Hl13c','2026-03-26 12:41:11.634925'),('cfj5odbzlqb70ehoegm18iecjahie4dv','e30:1vV4z5:wRA1zjGwyvd9nsE_JzEtDuREwfyy3v-xygAUVDppk6k','2025-12-16 09:35:15.754909'),('cm31dtyd9f21uk4ljbabd49u6n4nkt1m','e30:1viqrR:uYYJEu-YFn43KcOcwyIPqxkAoqdws0cqE7ZN3fRnsYE','2026-01-23 09:20:17.959079'),('cra7euwmxdy2bvhrx38mby5akrnn544v','.eJxNi0EKgCAUBe_y1m5q6WXkYy_6UCL6FSK6e0abljPDXNAapNnGZBrFuMBbaXRolSXJQXjIcmiCQ22Z5fXw8yDujGMIddPVgo4TE36-y94Z7Mz84oz7AcHVJzo:1vJUui:eU7tYNRu5PtpHlsp43WQoCBdXgZiDK-udjKFz0SlOIQ','2025-11-27 10:50:52.642815'),('crpwddvmf0yuyy8gv57926aymo1540rx','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.044505'),('cuolrdzhvhtu984pwi3t9x7jqoedwuqy','e30:1w4YnU:tWuYZQgtPVu8ONnrlV6dJtizer_jK1pETMmG4LIhk3s','2026-03-24 06:29:56.850237'),('dpfovgq6esu34r061g3c6736zk01puze','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.358122'),('duaia2nw2bd9h9vw16lqr6jzi1n2uqhk','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9saXZlcGFnZS8ifQ:1vxjbr:tHaCpM1Aa-1KU_U3iHqYFDG7CLiUcwWfdKd1XKq04Xw','2026-03-05 10:37:43.989233'),('e2xeby7w1qbub0pjo5ufj6dccvesjbsk','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.532075'),('eq4iiz05zk9ez9jhjsbtr9m0uo0y2q0l','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1va7mU:mx4Rk98Gngv8kag5M1aXjfeZRE-o9xBV3aaBYv9YtVQ','2025-12-30 07:35:06.043071'),('ewz75mwoyigt0yj7c28p6bm73w3dv4dh','.eJwdzc0KgkAUBeB3ubhLKCeUEFootegHixZhbmTSq07lKPeORUXv3tTZnQOH7w2KczmYBrVRhTRYQmhoQBcIKyQkCGEMLgyMpGWLtsqyVdpOvWR-dGQP0J-vZSVybqTwA8eb_ON4Ws_S-lRH3uxuuIj1QWSycKZbNot1Eq-a9p5lZbC_TkbNaGe8yN8kcfVaXp6HmzmmhDy3DA890o-HULhw62qlc8LCwrmythCfLyGnQQE:1vVis0:0eorxVnwOvTvXOCjDq09DJhxJQlSwhKu-0yrfihMdTc','2025-12-18 04:10:36.996783'),('f5ry3jyi6dvq0824wp0c7es6dxnt6ego','.eJwdzc0KgkAUBeB3ubhLKCcSEVooteiHihZhbmTSq07mKPeORUXv3tTZnQOH7w2KMzmYGrVRuTRYQGhoQBcISyQkCGEMLgyMpGWLtsqiVdpOvWR-dGQP0F-aohQZ11LMfMeb_ON4WgdJda4iL7gbzmN9FKnMnemWzWK9i1d1e0_Twj80k1E92hsvmm12cflaXp_HmzklhDy3DA890o-HULhw6yqlM8Lcwpmytgg-XyGzQQc:1vaoye:V0JkXhUUPx4oEvrbGiSZHYD8U79qvcPiCFPBd-uwZOU','2026-01-01 05:42:32.037252'),('fakwiu0yze38jw3yo819pt200gyzx1gg','.eJwdzc0KgkAUBeB3ubhLSCeKEFooteiHChdhbmTSq07mJPeORkXv3tTZnQOH7w2KM9mbGrVRuTRYQGCoRxcISyQkCGAMLvSMpGWLtsqiVdpOnWR-3MkeoLs0RSkyrqWYzhzf-8fxtZ4n1bkK_flgOI90LFKZO5Mdm-VmH63rdkjTYnZsvFE9Ohg_nG73UflaXZ_xzZwSQl5YhvsO6cdDIFy43SulM8LcwpmytvA-XyGjQP8:1vV52D:zqqAOTQyf1G0Tw5X4642YgGpZqCeBD8ym9SeQPM6FYQ','2025-12-16 09:38:29.291796'),('fc0c2lwhh299p1wfwpayuzw7s3hbf9a0','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vPuvF:Nx-ywHd3SyUf3KspdhwwlF_1DixH_uIEypSUESN2vXw','2025-12-15 03:49:57.812536'),('fd7xsx49cg27t80fx2q272x6sk2qqswz','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.369727'),('fhrb6x5844t5icx8k48xnnrrl4et49lu','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vQIKX:qIu3hDLkte8ENpYwe-8XJ37h4j527nheMgWJJWNW-R8','2025-12-16 04:49:37.668380'),('fqm6taib7qzw9ykkdgf5tq8t1nydlllh','.eJwdzc1OwzAQBOB3WeXWiNhGKZGlHhrBgR8V1AMquURuvIlNGydab4oA8e4Ydm6r0Xzf4GNrFnYY2HeG0YJmWjAHwh4JCTQ45lkXhVQ3VyJF6koIUVgT3XEyZAvIYYlIwYyY2saOPqTXbGL8mCjtwXw82V610RlVrjMp_i-TIVSH4W3YyurCsavDXjWmy66fIt8-7Op7N16axq5fTmLlVs8st-Xjru6_7t4_92d-PRDGTWLiMiP98aBVDudp8KEl7BLc-mSX1c8vzUFJ8A:1vjcGM:LeZPn3iQhOEzgdWhFf9RbE_uhbvoHwOJZkToi_oDEXI','2026-01-25 11:57:10.029134'),('fspk6bow1z167qvwzz2jhpyiswwu3t3k','.eJwdjdsKgkAURf_l4KNgGmoJPURiJRGWUdSLTHpMzRtnZrAL_XtT-2nvBZv1hpInTIoCW1GmTGAGniCJOhDmSEjggQE6SI7UsgbV_FVToZ5xPnSkDtBf71luJbxglu1o5ugfLejrahetn-Em706sKQLmTnypVZf0lh1f9tTYx-fD0hj2cfg8DRRNXVrE23EtVg87dFq_ms-Uhsse6ecEz_x8ASEGOac:1vQ0of:NBFNL52UBOvRbXMUQI-xQM0ePzSPOhkQbOX28xFYTQk','2025-12-15 10:07:33.363790'),('fu4zjf587kappdv0eay5itjcf5ziewu8','.eJwdzc1OwzAQBOB3WeXWiNhGKZGlHhrBgR8V1AMquURuvIlNGyfybooA8e4Ydm6r0Xzf4Kk1CzsM7DvDaEFzXDCHiD1GjKDBMc-6KKS6uRIpUldCiMIacsfJRFtADgthDGbE1DZ29CG9ZkP0McW0B_PxZHvVkjOqXGdS_F8mQ6gOw9uwldWFqavDXjWmy66fiG8fdvW9Gy9NY9cvJ7Fyq2eW2_JxV_dfd--f-zO_HiLSJjG0zBj_eNAqh_M0-NBG7BLc-mSX4ucXzTFJ6A:1viXRa:Fya79li9_SiYPZak3nPraU6i3MdQJWvMNm7ddQixX8I','2026-01-22 12:36:18.798959'),('fw20f7it1cgyeontx6v7d1r70qjmknrf','.eJwdzc0KgkAUBeB3ubhLqDEMEVoktegHCxdRbmTSq07pJPeORkXv3tTZnQOH7w2KM9mbGrVRuTRYQGioRxcISyQkCGEMLvSMpGWLtsqiVdpOnWR-3MkeoLvcitLLuJaeP3PE5B9HaB2cqnO1EMFgOI904qUyd6Y7NstNHK3rdkjTYna4TUb1aG_Ewt_GUflaXZ9JY44nQp5bhvsO6cdD6LnQ3CulM8Lcwpmy9lR8viGoQQE:1vbvGy:Bq8mF8Aj4iCdlvZWN88zEQPZBVgcD6PxnjH9sGtY9dw','2026-01-04 06:38:00.998754'),('g0zciylwut0fmf3upzilv1yqe9e4r3l1','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.236272'),('g82peoc25zkcseaqomkw92muekrybafy','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1vlmwl:FcNkuzbDOR5n1nwQEfZ-rUmpokbmy_Z0G7DZyJn8NZg','2026-01-31 11:45:55.338186'),('gq7p2nk7e6jv2v5giy153aw8ctycwr60','.eJwdzcFOwzAQBNB_WeXWiHiNWiJLHBrBoYAK6gGVXCKTbGK3iWvZmyBA_DuGndtqNO8bbGz0zIYc21YzdaA4zJRDoJ4CBVBgmL0qCpQ3VyIFVSmEKEa7kNcDFZDDHCk4PVEq626yLr28jvHjEtIc-Pdz18smGi3XmwzF_2XoXHkc3oYtlgvHtnIHWes2u36KfPewr3ZmWuq627ycxcqsnhm368d91X_dnz4PI78eA8XbxMTZU_jjQckcxstgXROoTXBjk42IP7_ISUm7:1vxLnX:BLYwSluFzpRhjbqbkDa5O6AgNBQ9RUeTvhJIaOdOYJo','2026-03-04 09:12:11.117765'),('gulxqcpb0shyemmr0qr86b7589m98ban','e30:1vxKI3:9dNgMdHkNPNfLm8RR9FptjYmClf9n_1TI6HBsJGq_EU','2026-03-04 07:35:35.474597'),('h7w9etny7o7echnz8n96rdo5oi8igoj1','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Ii8ifQ:1vvtwY:1sYfTa5xNtpy4bDRmowqJEs-bGHZK49TmelHtWlcD3U','2026-02-28 09:15:30.658054'),('hdd6cg4bsfrq01kes52e5bvd5yb3yo4f','.eJwdjU1vwjAQRP_LKjcQcZyERJa4oVI-1CpSAXFCBi9KmtqE9UZAq_53DDO30dO8P2j8Xvdco-PmqBkNKKYeh0B4QkICBTVzp-I4kcVIhCaqFELERvv6cNZkYhhC75GcthhobWzjwtRp769nCn_QHVpzkntfa5mPo0S8EhW3hchmy3dXpi1n63Zb2vwyj5q3bGe_f9rZVF6ryyDh_HdVDtIq-5wu7c19bAumr809rYrjJGh83yE99aDk_wPGxkF4:1vRP0M:2ROrUBDojETfzObJPHV9ZYQ2MBM7yxjaf5KdqX5PMko','2025-12-19 06:09:22.308456'),('hepxzcr0uxqiq8nktem9r2n352h8rgx8','.eJwdjs1OwzAQhN9llVsjYhu1RJZ6aAQHflRQD6jkEplkE5s2brS7KQLEu2M6cxuN5psfCNy4WTxGCa0T7MAKzZgDYY-EBBa8yGSLQpubK5WsbamUKo6nIcQCcpgZKboRU9N1Y4gpmhzz54nSFkzvh643DXtnlqtMq4syHWO5H96GjS7Pwm0Vd6Z2bXb9xHL7sK3u_Xiu6271clALv3gWvVk-bqv---7ja3eU1z0hrxOG5wnpHw_W5HA51BC2CdyExNbK_P4BxtlIhw:1vtJNi:wt-ghoKXxhrBPhiif51oSnGgBtB8NtHeosSuJqtVxmk','2026-02-21 05:48:50.772797'),('hfpj20l5f3siprluqvjvls8pordt6dot','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaGVsbF9tYXRlcmlhbC8ifQ:1vkyCB:tz3WjR6ZMIOYlEgX7PHStXoWa8Uz5-lS7Jm3BJxQ8Ts','2026-01-29 05:34:27.224635'),('hfyx4jfsqt1w27k3rimjg3ski09o1zxi','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.574838'),('hq9skn769pxs6ee6c4gm7xigj047qp5u','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.011340'),('hrzqck6ogfnjy1p0mi9yf37matzye7hm','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.026824'),('htgu5ir6e6quoiunn9qsp6q5gl0mvcwz','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vRUzd:sS3LntlpeE2Er7s0HHLCdN2e4QFsY6Gzph-CA5PIOcY','2025-12-19 12:33:01.544374'),('hvuv94h75aq194ejh8sq4chcjt0h6aoa','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.047139'),('hwe5cno16soy2lhvok01ulkhnerovqzm','.eJwdjU1PwzAQRP_LKrdWxDZqiSxxaAQHPlRQD6jkUm3jTR1K3Gh3UwSI_45h5jZ6mvcNvexw0khJ-xaVAnjliebA1BETg4eoOvqytO7qwuRaXxljyoAS9yfkUMIcJiFOOFCmMQx9ytOIIh8nzn8w7o-hczuJ6BbLwpr_FDalant4PaxsdVZp67RxDbbF5aPozf26vovDuWnC8vloZnH2pHa1eFjX3dft2-fmXV-2THKdNTKNxH968O7nFwTUQrY:1vSuOp:d0IDeup-6u2yuDoccc-Gl2e3u03wJ6r8_OWuJUNHzfg','2025-12-10 09:52:51.209622'),('i02mci2k0lzelnjjcqc3zi343ea7xyne','e30:1vxKI3:9dNgMdHkNPNfLm8RR9FptjYmClf9n_1TI6HBsJGq_EU','2026-03-04 07:35:35.452325'),('i2fhrschgurpe8jk3h7pvfhennnhlllz','.eJwdzcFOwzAQBNB_sXJrRGyjlshSD43gUEAF9YBKLpEbb2K3jRPtbooA8e8Ydm6r0bxvEaixM3uIHFrL4IRhnCEXCB0goDDCM0-mKJS-u5EpypRSysJZ8sfRoitELmYCjHaA1LZuCDG9Jkv0MWLaE9Px7DrdkLd6ucqU_L9MxVge-vd-o8orU1vFva5tm90-E98_7qqtH6517VavZ7nwixdWm-XTruq-Hk6f-wu_HRBonRiaJ8A_Xhidi8vYh9ggtAluQrKVKn9-ARcOSh0:1vyQgg:U9XnDG0Hvh6CoP_EFzb9xf07N4EQjne3VwTJi7Ip_X8','2026-03-07 08:37:34.094326'),('i2fwq3t32040pws9gllgsx512kcrtblu','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.315691'),('i3gq5tmr6676zhtuowus039fy5lc2rrl','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Ii8ifQ:1vzTBR:UqdkPkf0zdWh5AdfrCGncaXUFkoHMcDBBRRqLq91pwM','2026-03-10 05:29:37.593923'),('i6dk6cz2r4qh817ph58komva0jvv54g3','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1vvttw:sfyscu8NdS-Isc8zJ7TlJ2H8tgFQ1TAM-Tn9S_ufbdM','2026-02-28 09:12:48.203671'),('i71jiws6vxeyjxh6ao19wjvw6hxxskbu','.eJwdjUsLgkAURv_LxV1CzoQiQgulFj2wcBHmRia9PjInmTtjVPTfs87uO_Bx3tBSLoxuUOq2EBpLCLQyaIPCChUqCGAONhhCJUWP0xRl38pJDYLocVfTAYZLV1Y8p0Zw17OY88diUvppfa5D5o-aikgmPBOFtdiTXm3jaNP0Y5aV3rFzZs3soFno7uKoeq2vz-SmT6lCWk4ZMgOqXx4C_vkCFC050A:1vSxDU:1IsMjGS-UorNXwkH5KAPCTPDF1rTAn_q1ggjEJlMu4w','2025-12-10 12:53:20.681651'),('ixzwzfvp5x86pf2alywi1rg6ydlhoawh','e30:1vV4z5:wRA1zjGwyvd9nsE_JzEtDuREwfyy3v-xygAUVDppk6k','2025-12-16 09:35:15.767421'),('j29mi2mmfakce2bmq1flw3myk625fwai','.eJwdzc0KgkAUBeB3ubhLKBVFhBZJLfrBokWUG5n0qpM6yr1jUdG7N3V258Dhe4PkTIy6RqVlLjQWEGka0QbCEgkJIpiCDSMjKdGhqaLopDLTIJgfPZkDDNemKN2Ma-H6geXM_rEcpcJzdakWTnjXnMfq6KYit7wd6-Umidd1d0_TIjg0s0k92Wtn4W-TuHytbs9jq09nQp4bhscB6cdD5NrQ9pVUGWFu4EwaO_Q-XyG7QQg:1vnZOJ:8uLK7qD5c4I0WgzzCg18h8nftXI38uKFwJMt5PElp8g','2026-02-05 09:41:43.535562'),('j3eys99dyihhza4ugqwk8dkv0sq4a633','.eJwdzc0KgkAUBeB3ubhLyJkwQmiR1KIfKlqEuZFJrzqlk9w7FhW9e1Nndw4cvjdozlRvazRW58piAZGlHn0gLJGQIIIh-NAzklEtuqqKVhs3dYr5cSN3gO58LUqZca1kOPZE8I8njJkk1amaicndch6bg0xV7o02bOerbbys23uaFuP9NRjUg50Vs3C9jcvX4vI8NPaYEPLUMdx3SD8eIulDc6u0yQhzB2fa2WIkP19ijkEz:1wKADB:y41tbVW52IlKtQB3PjdaVfc-bI2ey4Fpqx9H1fbYfVw','2026-05-06 07:28:57.265623'),('jc1rpqnx93njhwah7jho6ouh7vfehtn9','.eJxNi0EKgCAUBe_y1m5q6WXkYy_6UCL6FSK6e0abljPDXNAapNnGZBrFuMBbaXRolSXJQXjIcmiCQ22Z5fXw8yDujGMIddPVgo4TE36-y94Z7Mz84oz7AcHVJzo:1vJ6Xg:eRpXJyeI2GwOPR3YzClBA9k-x1BboUYEjYnz4Wqn0SM','2025-11-26 08:49:28.051322'),('jp6fjrjrf7v0nrbs82yx8ryyuvbs34wi','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.124091'),('jzlwnxb83bxdesgu2ov7yrm8nfa89s4t','.eJwdjUGvwUAUhf_LTXdEZ0bQTPIWGhZ48cRC6Ebmtbem6Gjm3hLEfzecszv5cr4nVLQ3LVt0XOWGsQDNvsUueCzRowcNlrnRcSzVqCdCpU6EEDF0oSX0ztQYGFPUlQtTY4huFx9eoPk_FaXakzVqMIyk-CaSziXbw-4wlsmVKU_dWmUmj_q_xJP5Mp3Z-pplxXB1Eh3b-WM5HiyWafmYHu_rM2-2HuknaKht0H_0oNXrDSW2Pt8:1vSYy4:JBe8X4wd0Lok56dTL74xt-9UCwe79vpnXdIDVAOXumc','2025-12-22 10:59:48.490215'),('k6vw983ja4n2nzn0uucycwcdds6f192y','.eJwdzc1OwzAQBOB3WeXWiNhGbSNLPTSCAz8qqAdUcolMsolNE9fyboIA8e4Ydm6r0Xzf4KgxM1v07FrD2IHmOGMOEXuMGEGDZQ66KKTaXokUqUshRDG6BYMZEHKYCaM3E6au6Sbn0ysYoo9LTGsQ3s5drxqyRq03mRT_l0nvy9PwOuxluTC1lT-q2rTZ9SPxzf2hurPTUtfd5vksVnb1xHK_fjhU_dft--dx5JdTRNolhuaA8Y8HrXIYL4PzTcQ2wY1LthTbn1-VKUmR:1vwHCf:TTBZj1kRdY9z_1BOLBbXf5teheedyDVoJqsQuEzZwFA','2026-03-01 10:05:41.022622'),('kbkxk1h8l1qs28g0o4uyrnh72llsnotv','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1ve6B2:waz-AvMesc8pinSCj4VmOTX-HGnj5xp5f39IQahMQpM','2026-01-10 06:40:52.048214'),('kfphponszs1dzrgk356fc9sieed0u6uf','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vQm3F:L84dJjJrbjYOkLwr2qaA0QqU5cgOMY3-KLYkkHFNlrg','2025-12-17 12:33:45.415952'),('kgm1jhzr96zocry018iwhirxgfby0u1g','.eJwdjU1rAjEYhP_Lyx4X86GuJeBB0NZDW6jtRS8h6qsJZj98k6xrS_97Y2cuw8DM8wMuaJOixSa6g4l4BBUpYQmEJyQkUGBj7BRjQs5GPFuoJ845Cxa913WekDOeQQkpIDWmxjx5RJGrzoRwaymfQre_HE9SB2vktCoE_1fR3t4uw307rj7ts2vX1-n7B05SYYeXDe3kcmBDWAS2Gvez74btxVZW6ez7nezXr7VbyK_rap4xIXVIDyYoUYJvz67RhIcM1i6zxeT3D6yYTBI:1vTcTE:UhH5zhFK-SvVMd4nY3DIiOpUs8bCCNLUJo8uVG0O77A','2025-12-12 08:56:20.679739'),('khuznct6afcomaki9rczrg10hozgc1qf','e30:1voL3t:OfJEHeqjbrD18k95h4f29Uedf3qWqrV52MWe5Edo74A','2026-02-07 12:35:49.539215'),('ksxbp05ml90jt0a0cvbcvmeggldtxggt','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.969636'),('kybmj2jzbsv77actyxv5937pp399mk7d','.eJwdzc0KgkAUBeB3ubhLqJkoRGiR1KIfKlpEuZFJrzqpk9w7GhW9e1Nndw4cvjdoTlRnSzRWp8piBqGlDn0gzJGQIIQh-NAxklENuqqyRhs3tYr5cSd3gPZaZblMuFRyMvXE6B9PGBOci0sxF0FvOY3MUcYq9cZbtov1LlqVTR_H2fRQjQblYG_FfLLZRflreXsea3s6E_LMMdy1SD8eQulDfS-0SQhTByfa2VJ8viGlQQA:1vVTxS:_JMtMIc2aBElLPR7vbwYisFQ2nrIUbsuLiHVCiN-MHs','2025-12-17 12:15:14.113569'),('l2qmp26s28nu0lm7ip7rdfvkh5zh9493','.eJwdzc0KgkAUBeB3ubhLyDGMEFooteiHChdhbmTSq07mJPeORUXv3tTZnQOH7w2KczmYBrVRhTRYQmhoQBcIKyQkCGEMLgyMpGWHtsqyU9pOvWR-3MgeoD-3ZeXn3Eg_mDrC-8cRWs_S-lRHYnY3XMQ68TNZOJMtm8V6F6-a7p5l5fTQeqNmtDciCja7uHotL8_kao4pIc8tw0OP9OMh9F243mqlc8LCwrmydiA-XyGuQQM:1viq4K:XVWvZN3gKhCVADecbwAmGPnE4c6-L3_-zbu0R27qlSY','2026-01-23 08:29:32.887158'),('l2y36hqhst3jao38riy6x58b6v9l43cx','.eJwdzc0KgkAUBeB3ubhLqDESEVooteiHihZhbmTSq07mKPeORUXv3tTZnQOH7w2KMzmYGrVRuTRYQGhoQBcISyQkCGEMLgyMpGWLtsqiVdpOvWR-dGQP0F-aovQyrqU38x0x-ccRWgdJda4iEdwN57E-eqnMnemWzWK9i1d1e0_Twj80k1E92hsRzTa7uHwtr8_jzZwSQp5bhoce6cdD6Llw6yqlM8Lcwpmytgg-XyGwQQY:1vUJZG:nuWYUM85GUn85m0YN7B59Q7ElhpUGd2xF6-otabcDCU','2025-12-14 06:57:26.466817'),('lgc4ar3ueu40e2rs7ytb0w943dq49qgf','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vRjGN:xpGlQ-e-9ySPvSd3JXk6_3tK6j7wOE95RjFJCeRJWjY','2025-12-20 03:47:15.088694'),('lgg715pt7pz9f15762le1v31xcdf2jtf','.eJyrViotTi3KS8xNVbICMw2VdJSKSwtSi0AcJStDIC81JzW5JDUlvjgjM60kPjMFqBKsCiZelphTlhpfUlmQCpE0UqoFADQEHhg:1vIQPy:hRmCZupS7321NMc0puKqQqKxob6dk3x9iqsDlg0aoAA','2025-11-24 11:50:42.018546'),('lhuvragi7gfzok6ku6oqxo6bs6wl28b0','.eJw1i0EKgCAURO8yaze19DIiNqFgIvoVIrp7ZrSbNzPvQqjGNvFMEpwVbtBSGhVaZUn2IPSMCxRqyywvQC-DGOmGYKoPu5gwTMzX33cbO42cmd-44n4Auz4nIA:1vIoYY:OqRLgrEe4BWU5o-tQ1kUlqWbhrR1zdgh4TNGMjABuec','2025-11-25 13:37:10.073251'),('lonm3uq29qonay6p7jxa8wgs5c4gc46n','.eJwdjUsLgkAURv_LxV1CzoQiQgulFj2wcBHmRia9PjInmTtjVPTfs87uO_Bx3tBSLoxuUOq2EBpLCLQyaIPCChUqCGAONhhCJUWP0xRl38pJDYLocVfTAYZLV1Y8p0Zw17OY88diUvppfa5D5o-aikgmPBOFtdiTXm3jaNP0Y5aV3rFzZs3soFno7uKoeq2vz-SmT6lCWk4ZMgOqXx4C_vkCFC050A:1vSuYp:V2sFrEcywjbMUYOnK1BJzTMCdG1nHl_-iN9IY63Mfz4','2025-12-10 10:03:11.803439'),('lpd0f67o8vxet9os9s9ds197klqj03nx','.eJwdzc0KgkAUBeB3ubhLKBVFhBZJLfrBokWUG5n0qpM6yr1jUdG7N3V258Dhe4PkTIy6RqVlLjQWEGka0QbCEgkJIpiCDSMjKdGhqaLopDLTIJgfPZkDDNemKN2Ma-H6geXM_rEcpcJzdakWTnjXnMfq6KYit7wd6-Umidd1d0_TIjg0s0k92Wtn4W-TuHytbs9jq09nQp4bhscB6cdD5NrQ9pVUGWFu4Ewa2ws_XyG2QQg:1veQJw:Mkx8BAGWMFd2IFv5tYfhqu_BR8wwYPrkJAE71K6PzKc','2026-01-11 04:11:24.704958'),('lq71fqckk0aakbf72nha96xgvammbqca','e30:1vxjbo:ydq6t29tipiM8xo3Kr10sMu7CNVh4cyW-arGO5dqOU8','2026-03-05 10:37:40.512840'),('ltj6409djzeq2klv97g32rnw6wbb4cw9','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZX0:1vJUup:LkacOrpq2MvkQ4e6jzXklfuqBYNMom4b0pg8r9-sZx0','2025-11-27 10:50:59.557450'),('lujiynrydg0tb8p28o4y23b3l3oijkub','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxfQ:1vNUqK:VGIzxpUL5YhxvPS6i1uQNZSz8BahjnzGeNJjCYIguww','2025-12-08 11:34:52.018393'),('lwntzfhmdnujiu9bdu1n33tf4c3uaq7u','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.008073'),('m0pupnal1vsemre6ed85cuw6n0as48qp','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1ve6Ay:5AUNL51KLIlfEctmybFk6VhkXZ9v_4ZM0DX_ph6ZXqY','2026-01-10 06:40:48.589034'),('m1f3oi9r0rco71oq6rp9kt5iq8tup63v','.eJxNyssJgDAQhOFWZM9e9Jga7CGEZIyBPMTNCiL2bhQEj_P9c1IsvkjVCczGgxRNL3Qs1jabJVJPwtiySU82LoXciGXF9jipsS1E2AqneQlz1cG150A_303coeux4ovXDem4K9c:1vIfhK:rWN4vGK9TxDhfVNfvcXUVbqPnkm_jbvKhk_x9Ma0KCA','2025-11-25 04:09:38.847008'),('m5bwhrdjubo7va44vl1bc0rkqr5egn71','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.107340'),('m9lhxd7805jhyv8dt4wurtcvrd9k8k3t','e30:1w4YnU:tWuYZQgtPVu8ONnrlV6dJtizer_jK1pETMmG4LIhk3s','2026-03-24 06:29:56.851750'),('mhusi2hgxu3vi4msbmze6ylsi420dkx5','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.535500'),('mls8q5jcgms5kqer1mqq5jhusg73f8jb','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.161331'),('mqalpavt6whcde64i3bynccgm9lkc964','.eJwdzc0KgkAUBeB3ubhLKBWjhBZKLfqhokWUm2HSq07qJPeORUXv3tTZnQOH7w2KhexNhdqoTBrMITLUowuEBRISRDAEF3pG0rJFW2XeKm2nTjI_bmQP0F3qvPAFV9IPx443-sfxtJ6cynMZe5O74SzRBz-VmRNs2MxX22RZtfc0zcf7ejSoBjvjxeF6mxSvxfV5aMzxRMgzy3DfIf14iHwXmluptCDMLCyUtYPp5wshuEEJ:1vfH6G:yiOoXWHjHSKrAYm8a2Kz8j1FXrlTC5o8bOIyQCtmW0c','2026-01-13 12:32:48.757170'),('mvvs0ntut11zxony8h4uqyzvkbggu9ka','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.083471'),('n5wuidpl5momylwbl93c11o9h0fhql83','e30:1vV51z:Be53vmjyLaGsDuAybg0FGDmB3tzu36Ke_isppBL1LaM','2025-12-16 09:38:15.796041'),('najv1u4a9k0yc6sb89zri5wf74uuo01x','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwic3VwZXJ1c2VyIjoyfQ:1vOYdz:AQH1MnfMZcYBuWdwqyRQsjoc9MXDpqcA73XL3saLIrs','2025-12-11 09:50:31.132804'),('nre4xdkj6rawjx2013d9fpkdqvn5j5wg','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.200011'),('o5czr94kuy21atrtxdsmeaoirz8qnxhg','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.338745'),('oeugg8a27dor1wx606i0zb6ojl3nsa54','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1ve6Ag:0o5Jm8guRLxeTUUDMPCodJtpeZean5dUjAw0sjgrCTY','2026-01-10 06:40:30.654580'),('ogavywx51o6m54wfbwaie4ofnsqxjaa4','.eJwdzr0OgjAYheF7adhgoBAIIXGQ6OBP0DAYZGkqFFqBQvq1GDXeu9Uzvstz3sgAU5KODKWINqOQyEMzBXhMqrFpvvVNGxDgNIhiB_v_OVjKpOyu3Roni4Y6k0VQ0doJj6A3-zzb8XGpqiY-977L3ZPG6-iQZ-1re38Wg76UisHKMmBmpn48SgMPCSDUaM6kFjXVzOJaGeahYeqEJIrV9hARNmMcfr6QPT0q:1vxjrw:kpV-uo97jFDf-hREbgEW-kJq1Yamr-tEUMVsgU3-pmA','2026-03-05 10:54:20.746172'),('oj9r7vrtuvacnh8yjto7akw47uaj9mfs','e30:1vxjbn:OjVn_z4G8AeW30LxPBJAl0QPYzNVugqbWpAYTCrSvgc','2026-03-05 10:37:39.899752'),('ok9oomd0qy4hvnrfxter9aecv23vii0u','.eJwdzc0KgkAUBeB3ubhLyDGSEFoktegHCxdRbmTSq07mKPeORUXv3tTZnQOH7w2KMzmYGrVRuTRYQGhoQBcISyQkCGEMLgyMpGWLtsqiVdpOvWR-dGQP0F-aovQzrqU_DRzh_eMIrWen6lwtxOxuOI904qcydyY7NstNHK3r9p6mRXBovFE92huxmG7jqHytrs_kZo4nQp5bhoce6cdD6Ltw6yqlM8LcwpmythDB5wtikEE1:1vy6jD:9andrGP3tU_SJVKr_VjOfCCqQiIok3vvunEEMP5X9rI','2026-03-06 11:18:51.153494'),('okm2o5yhjnpxe92in7i9na1vmql5e7al','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.972789'),('pfq9idj8aogqgsyoiip0haxutnevc0rt','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.311642'),('pgyiys4nix9os2my1d5xi1b16j3ejhum','e30:1vfGYz:EnRF5Cq2E39GsvkwRCaMOxodg4Bei1Au8lhYta20iFY','2026-01-13 11:58:25.720049'),('pytt6k0p1sp7lknbv9uak9lk0s7g5a9b','e30:1vky7j:QQCms7wLvR2xdcKsbtF97-ZnkiKji_aG29v4toO_Biw','2026-01-29 05:29:51.024875'),('q8xsu6ok2rmrgm86ckp4upxuxtchbhsi','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.431994'),('q9byf8td8m56yio4mfnv24cauc9bd3mn','.eJw1i0EKgCAURO8yaze19DIiNqFgIvoVIrp7JrWbNzPvQqjGNvFMEpwVbtBSGhVaZUn2IPSMCxRqyywvQC-DGOmGYKoPu5gwTMzX33cbO42cmd-44n4A4lEnUQ:1vKFcH:1DN2-k1TXNuOr8fPsebdPSGBwK3kAOGMWASTkHOaJkI','2025-11-29 12:42:57.674463'),('qhqb4j4sgu2fd0oukpab1cljbjldmy93','e30:1vxKI3:9dNgMdHkNPNfLm8RR9FptjYmClf9n_1TI6HBsJGq_EU','2026-03-04 07:35:35.489610'),('qrirk794t7akdo2etw3vdzhjdz55m1ei','.eJwdjU1vwjAQRP_LKjcQcZyERJa4oVI-1CpSAXFCBi9KmtqE9UZAq_53DDO30dO8P2j8Xvdco-PmqBkNKKYeh0B4QkICBTVzp-I4kcVIhCaqFELERvv6cNZkYhhC75GcthhobWzjwtRp769nCn_QHVpzkntfa5mPo0S8EhW3hchmy3dXpi1n63Zb2vwyj5q3bGe_f9rZVF6ryyDh_HdVDtIq-5wu7c19bAumr809rYrjJGh83yE99aDk_wPGxkF4:1vPHox:HoZfV4yVKVPrJRc14kF3EA2FVBOI25rU0DJ2k86XcYg','2025-12-13 10:04:51.827021'),('qrlzdoec6eenn9lmu8sd8to8ciwykcbz','.eJwdzc0KgkAUBeB3ubhLKA3DhBZJLfqhokWUm2HSq07pKPeORkXv3tTZnQOH7w2KhexMidqoVBrMIDLUoQuEORISRDAEFzpG0rJGW2VWK22nVjI_GrIHaK_3LPcFl9IPJo43-sfxtA7PxaWYe2FvOI310U9k6oy3bBbrXbwq6z5JssnhPhqUg73x5sFmF-ev5e15rMzpTMgzy3DXIv14iHwXqqZQWhCmFhbK2tPg8wUhwkEL:1voZsP:lOd0u20iJJVvtvqYaVsbmG9OSLJP30DiTjTHjgF-208','2026-02-08 04:24:57.300964'),('r1plnm9c7hqb6pcss5ps2vmkteed3ru6','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.468034'),('r35ogxq77hbqv6o2nh6miozydy7y0ixz','.eJwdzr0OgjAYheF7adhggBoIIXGA6OBP0DAYZGlqKVCBQvq1GDXeu9Uzvstz3sgAV5KOHCWI1qOQyEMzBXhMqrZpvvV1gwl0FIeRE_j_OYGUcdle2zSIFw0skwWuKHNWR9CbfZ7tunGpqjo6977buScdpOEhz5rX9v4sBn0pFYe1ZcDMXP14lGAPCSDU6I5LLRjV3OJaGe6hYWqFJIoze4gIm3H0-QJTajz9:1vaYXI:VgrZ8ZOvlNS3vUtTT4atfcnHDbXi_ldKLBamxA0VYq8','2025-12-31 12:09:12.840911'),('r43wqf9p3ejpf93pt6hrhsbnwdnu2g3y','.eJwdzUsLgkAUBeD_cnGXkA-UEFoktehBRYswNzLpVSd1lHvHoqL_3tTZnQOH7w2SMzHqGpWWudBYQKRpRBsISyQkiGAKNoyMpESHpoqik8pMg2B-9GQOMFybovQyroUXhJbr_GO5Ss2S6lIt3Nldcx6rk5eK3PJ3rJebfbyuu3uaFuGxcSb15KDdRbDdx-VrdXueWn1OCHluGB4HpB8PkWdD21dSZYS5gTNpbN__fAEhrEED:1vcNhG:ZWko7WOuNwoQxa0ZHWVkLL0YbL7JS1K_4_Y06QZkQH8','2026-01-05 12:59:02.906803'),('r9moub5sgwm47pb4dy6dtpq41ngfvmh0','.eJwdzUsLgkAUBeD_cnGnkNoDEVoktehBhYswNzLpVad0lHvHoqL_3tTZnQOH7w2SMzHoGpWWudBYQKhpQAcISyQkCGEEDgyMpESLpoqilcpMvWB-dGQO0F9uRelnXAt_OrM89x_LUypIqnO18IK75jxSsZ-K3BrvWC83-2hdt_c0LWbHm2vX9kF7i-l2H5Wv1fUZN_qUEPLcMDz0SD8eQt-BpqukyghzA2fS2BP38wUhqUEB:1vhniG:W64TMj8-uMoROBcuM-mydG6gyulQmg0XzSh1gypwID0','2026-01-20 11:46:28.246780'),('rd6x0m5yks59anomqnngjuig4eqvkovj','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwic3VwZXJ1c2VyIjoyfQ:1vy6nO:Dznigv9TYrSJCKuggiDKLgpNzXUkePstpWzkgLGUiEs','2026-03-19 11:23:10.836004'),('rg4ia8gsqcgzzy3yl9vlbo3adwj085yf','eyJpc19hdXRoZW50aWNhdGVkIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwic3VwZXJ1c2VyIjoyfQ:1vOBon:P5J_9m6EENpFpliDhlSta2sG8ossnaBUgRwQ3fWOdR0','2025-12-10 09:28:09.990735'),('ro2584idlit2qmzgxjuuw8f8u56yn1oy','.eJwdzc0KgkAUBeB3ubhLKA3DhBZKLfqhokWUG5n0qpM6yr2jUdG7N3V258Dhe4PkRPS6RKVlKjRmEGjq0QbCHAkJAhiDDT0jKdGgqSJrpDJTJ5gfLZkDdLcqy92ES-F6M8uZ_GM5SvmX4lqEjj9oTiN1cmORWtMd6-VmH63LZojjbHasJqNydNBO6G33Uf5a3Z-nWp8vhLwwDPcd0o-HwLWhbgupEsLUwIk09nz--QIhykEP:1vpLjg:BK3-KWRz0Odffm9bgdQihSiN7bdxiSvkzZsYPYpG-hk','2026-02-10 07:31:08.721925'),('rrpfe7e1zfexen4yry1ndtsk586oi3la','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.921993'),('rtjztg8h5ej9parynid65hl7bpgdh21g','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.203120'),('rtyhvc0pvwcptec7vkgpa07jjo6mxlx4','.eJwdzc1OwzAQBOB3WeXWSHFctYoscWgEB35UUA-o5BIZZxO7dZzIuwkCxLtj2OPsaL5vcNTqhS0GdkYzdqA4LphDxB4jRlBgmWdVFH4y2tuJWFVCiGLVfsXWeE1UQA4LYQx6xNTX3ehCiub0-phiWoT5_dr1siWr5W6fleL_sjKE6jy8DYeyWplMHU6y0SbbPhHfPhzrezuuTdPtX65iYzfPXB52j8e6_7q7fJ48v54j0k1iaJkx_vGgZA5-GlxoI5oEty7Zlfz5BQf2TOw:1vnB4o:gTbvOFTnJbkeba2ghYPgHFhnksSnpYP2MX62h5zF0KE','2026-02-04 07:43:58.075625'),('rwjkj5vmktjfle8fjpll2lsebip8enx8','e30:1vjYkR:A1tqE6HhEqsED4d0RaB65GYSO39Jk8Fqtl6mx78XVr8','2026-01-25 08:11:59.896420'),('s40b05itolw5eftmdrn3c3lkvsqjvhbj','.eJwdzc0KgkAUBeB3ubhLyDGMEFooteiHChdhbmTSq07mJPeORUXv3tTZnQOH7w2KczmYBrVRhTRYQmhoQBcIKyQkCGEMLgyMpGWHtsqyU9pOvWR-3MgeoD-3ZeXn3Eg_mDrC-8cRWs_S-lRHYnY3XMQ68TNZOJMtm8V6F6-a7p5l5fTQeqNmtDciCja7uHotL8_kao4pIc8tw0OP9OMh9F243mqlc8LCwrmytgg-XyGqQQM:1vTfgM:jAw3KYkxPaAlambfR8nS8OH1JBKp6b4U1mtvPXWQ67M','2025-12-12 12:22:06.087574'),('s7gtr6cocu0z1iudvovhpdz342yqmhmi','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1vjAF8:seUPim5xIyhpWgK0qAvntJS2rM4IsJ9wVH37gBiyY3g','2026-01-24 06:02:02.275895'),('s7hz4iab19p4rvdct15d6ga1glc1777f','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxLCJpc19hdXRoZW50aWNhdGVkIjp0cnVlfQ:1vNoPU:DO3lnTx_2d4UB3Xc4w-d_Wnz5G0NIx5vqvoSyLPraH4','2025-12-09 08:28:28.544469'),('sc4rj18hp5lf1y3aoy0mk2vg1lhk7jdf','.eJyrViotTi3KS8xNVbJSKkstKcpU0lEqLi1ILQKJK1kZAnmpOanJJakp8cUZmWkl8ZkpQJWGSkjiZYk5ZanxJZUFqRBJC6VaAEPqHlg:1vEQpR:3GFVOoZzfuh8qo9PavHP6A7ix3WHwGSVaVFFR-fRbDE','2025-11-13 11:28:29.711087'),('sefqhynl0c141uohn31l58dxdmgwmngg','.eJwdzUsLgkAUBeD_cnGXkA-UEFoktehBRYswNzLpVSd1lHvHoqL_3tTZnQOH7w2SMzHqGpWWudBYQKRpRBsISyQkiGAKNoyMpESHpoqik8pMg2B-9GQOMFybovQyroUXhJbr_GO5Ss2S6lIt3Nldcx6rk5eK3PJ3rJebfbyuu3uaFuGxcSb15KDdRbDdx-VrdXueWn1OCHluGB4HpB8PkWdD21dSZYS5gTNpbD_4fAEhsEEF:1vdjqw:kfRjOX528iCmk-3Mvm97KlLt85675X1wm62GY3jntzE','2026-01-09 06:50:38.779537'),('sgjhlk9q9tsdi6gk2yc2xtcspl8hubwj','.eJwdzc1OwzAQBOB3sXJrRGyXlsgSh0b0wI8K6gGVXCI33sSmjRPtbooA8e4Ydm6r0XzfIlBjZ_YQObSWwQnDOEMuEDpAQGGEZ55MUSh9cyVTlCmllIWz5I-jRVeIXMwEGO0AqW3dEGJ6TZboY8S0J6bjyXW6IW_1ap0p-X-ZirE89G_9RpUXpraKe13bNls-Ed897Kp7P1zq2q1fTnLhF8-sNqvHXdV9bd8_92d-PSDQbWJongD_eGF0Ls5jH2KD0Ca4CclW-vrnFxcJSho:1vztfS:drzM5JU2GIeabFHgfctByEZfCZClboiT49LvLLqHNAc','2026-03-11 09:46:22.882263'),('sm3lxnp90mfqlz8sckwr1ew2gkxyp86x','.eJyrViotTi3KS8xNVbICMw2VdJSKSwtSi0AcJStDIC81JzW5JDUlvjgjM60kPjMFqBKsCiZelphTlhpfUlmQCpE0UqoFADQEHhg:1vGy8a:5-aslV26uq6mLio199zQcYmKyj1LGIJ_rDM7XFN0CrI','2025-11-20 11:26:44.030810'),('t19igsfuehhq8xoby4w6rgg3kqx95g54','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1vky7i:n2xqarNqKof1hiRyw0hT-HAaKjSPz7FRfX9CFzffgMA','2026-01-29 05:29:50.808119'),('t1bih09ln79azapx3mm5hl6i9rtf9pbo','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.213470'),('t3uc4mx9tczcw9343cgbg5uzdpemipox','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxfQ:1vGyXU:AbPOd7ORjGQfUq944p_AlS94cq0IWNWCnIECT-ItaiY','2025-11-20 11:52:28.794465'),('tah0drac141kq63owpd21y7mjjbgux1g','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.431994'),('thh4k29ntnciviv59a8uau8p89girjyg','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.532075'),('tsyjynsj5duwf0kus8emurdvo5i5n031','.eJwdzUsLgkAUBeD_cnGnkGMPQmih1KIHFS7C3MikV53KSe4di4r-e1Nndw4cvjcozmVvGtRGFdJgCaGhHj0grJCQIIQBeNAzkpYt2irLVmk7dZL5cSN7gO50Kasg50YG44kj_H8cofU0rY91JKZ3w0WskyCThTPcsJmvtvGyae9ZVk72F99t3J0R0Xi9javX4vxMruaQEvLMMtx3SD8ewsCD661WOicsLJwrawsx-nwBYoxBMw:1vy4aD:2XRTe8Cd0aLRd5EZOL5j0hsyHC64XWSNWbSVnupsePE','2026-03-06 09:01:25.852425'),('u0r9t2mn5sx79c7vgoh2ayng2uyol3kf','.eJwdzc0KgkAUBeB3ubhLyLGUEFoktegHixZRbmTSq07lJPeORkXv3tTZnQOH7w2KM9mZGrVRuTRYQGSoQxcISyQkiGAILnSMpGWDtsqiUdpOrWR-3MkeoD1fi9LPuJZ-EDrC-8cRWk-O1amaiUlvOI_13k9l7ow2bOarJF7WTZ-mRbi7eoN6sDViFqyTuHwtLs_9zRyOhDy1DHct0o-HyHfhdq-UzghzC2fK2sIbf75iiUEy:1vv6EP:Hwb50BYXS53-R6zBwK_VLoCcmiponk-v6uOX-BXsJVA','2026-02-26 04:10:37.252843'),('u5w2l893e0y7enorjhjks7t97u4vyo2q','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.046514'),('u8bhi62qsikzhaxzswh8ya4o9ci5buzn','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1vztZW:IDKE3Gf5E6qodOhfEX6s5zit_02ggyLEX-lgJNGIrFg','2026-03-11 09:40:14.849445'),('u8vyaqa3isw4vy7sizewnho7sz9y15y8','.eJwdzc1OwzAQBOB3WeXWiNhGLcESh0Zw4EcF9YBKLpGbbGLTxo12N0WAeHcMO7fVaL5vCNy4WTxGCa0T7MAKzZgDYY-EBBa8yGSLQpurC5WibamUKtyeuIAcZkaKbsRUdN0YYnpNjvnjRGkKpv2h603D3pnlKtPq_zIdY7kb3oa1Ls_CbRW3pnZtdvnEcvuwqe79eK7rbvVyUAu_eBa9Xj5uqv7r7v1ze5TXHSHfJIbnCemPB2tyOJ6GEBvCNsFNSLZW1z-_az1IHQ:1vxHmI:M5HusfpKKMeM_exDzfPcHrEEgCHAv4U3vsRAOKq6D9U','2026-03-04 04:54:38.843936'),('ug1ft8rnr1vvt5d1x51bis6ewg3tpr34','e30:1vxjbo:ydq6t29tipiM8xo3Kr10sMu7CNVh4cyW-arGO5dqOU8','2026-03-05 10:37:40.553152'),('ukp86194c6fgdyk2k7yqwsj10y1fws0x','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.145198'),('upsjceo5jcuz7vmcybw5fbu5m1iu8i9l','.eJwdzc0KgkAUBeB3ubhLSI1ChBZKLfqhwkWYG5n0qpM6yb2jUdG7N3V258Dhe4PkTAy6RqVlLjQWEGga0AbCEgkJApiCDQMjKdGhqaLopDJTL5gfdzIH6K9NUXoZ18KbLyzX-cdylfKT6lKFrj9qziMVe6nIrdme9Wp7iDZ1N6ZpsTg1zqSeHLUbzneHqHytb8-41eeEkJeG4aFH-vEQeDa090qqjDA3cCaNbbDPF2KBQS4:1vpOb5:DaibqjuhVPgpT_hDA2XFq410SVnzfV4bbmeAZMRMSQw','2026-02-10 10:34:27.389648'),('uqt4t6tmeprdzcwv4wtiv520nvl0tv8b','.eJwdzUsLgkAUBeD_cnGXUBq9hBZJLXpg0SLKjUx61Umd5N4Zo6L_3tTZnQOH7w2SE2F0iUrLVGjMINBk0AXCHAkJAuiDC4aRlGjQVpE1UtmpFcyPO9kDtNcqy_2ES-GPxo43-MfxlJqei0ux8Kad5jRURz8WqTPcsV5uonBdNl0cZ-NDNeiVvb32FqNtFOav1e15rPXpTMhzy7BpkX48BL4L9b2QKiFMLZxIa88mny8hxkEN:1vpKY4:_5eetUCwL3332dd-pVYXOOY_wkEWfwDRNkdZ19Na5qg','2026-02-10 06:15:04.613475'),('uspsa0x1lx8rr2ydau9ux45d1n6dwshq','.eJwdzc1qwzAQBOB3Eb7F1JJCUiMIJSY59Ie05FBSX4Qqry01tmy065S09N2rdue2MPN9M4_azOQgkLeGoGGK4gw5i9BChMgUc0STKgohb294ilAl57ywV9uDtuMw9UBQ3CEZ8mPAjWA5mxFiMAOktmkGH9JrMoifY0z7bHo_N63U6IxcrTPB_y8TIZSn7q3bivJCaKtwlLWx2fIJafdwqO7dcKnrZv1y5gu3eCaxXT0eqvZr_3E99vR6ioCbxOA8QfzjmZI568fOBx3BJlj7ZAu5_PkFm_BQWw:1vztTf:Q7IQ5c_-5kP0R25yho9AbS-vZkxgv_q6al2HwGsbSzY','2026-03-11 09:34:11.860794'),('uwzpipxc7zno2s8xrfo46qz9ap3zc5uc','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.124091'),('v71z23bf04wo0hzewfkxddxkmf8btvmg','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9zaW5nbGVfcGFnZS8ifQ:1va7mn:bJusJPpGa1wJGQVevZbBE7pVBqlR9lcRyyf7ccnpFLs','2025-12-30 07:35:25.483984'),('v9lbj0wot1ugk3q2daplolfpthxb7rzu','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1vaV6Q:bFBX6dbpOEqqw-cd6Se6fbIw02SZK0KeFnesT1Nt9oE','2025-12-31 08:29:14.655442'),('vbzrt2oqnb8j3fi9s6lhhbhuo29ibwv3','.eJwdjU1PwzAQRP_LKrdWxDZqiSxxaAQHPlRQD6jkUm3jTR1K3Gh3UwSI_45h5jZ6mvcNvexw0khJ-xaVAnjliebA1BETg4eoOvqytO7qwuRaXxljyoAS9yfkUMIcJiFOOFCmMQx9ytOIIh8nzn8w7o-hczuJ6BbLwpr_FDalant4PaxsdVZp67RxDbbF5aPozf26vovDuWnC8vloZnH2pHa1eFjX3dft2-fmXV-2THKdNTKNxH968O7nFwTUQrY:1vSwSR:jFbNO9a-kALa2cZNpBgw7TMSoBoj_wV-wicR54b3lTw','2025-12-23 12:04:43.064085'),('vfavxp7ap69lmpze8fbk9xacb0i9khzv','.eJwdzUsLgkAUBeD_cnGXkA-UEFoktehBRYswNzLpVSd1lHvHoqL_3tTZnQOH7w2SMzHqGpWWudBYQKRpRBsISyQkiGAKNoyMpESHpoqik8pMg2B-9GQOMFybovQyroUXhJbr_GO5Ss2S6lIt3Nldcx6rk5eK3PJ3rJebfbyuu3uaFuGxcSb15KDdRbDdx-VrdXueWn1OCHluGB4HpB8PkWdD21dSZYS5gTNp7MD_fAEhskEF:1vjA0l:Udcw8D9VTtVEDm5NWyNDf3_m7ADGm5-qhlZ7-xkJWeY','2026-01-24 05:47:11.708258'),('vhuerbivkw1d2zwv772jf4rjv1tey3wj','.eJwdjdsKgkAURf_l4JtCXsYUoTfJyiiELvQkkx7Rppl0ZkQr-ves9bYXbNYbGpXTXtcodFNQjSVEWvZogcQKJUqIYAYW9AqloBynSUveiEm1VKnhIacDtFdWVm6uaur6c8Ox_xjBuLFJkq5E6DFNjuwccr9bG82SXPjtzpLYHbLOdLT_2oaml5F9nPJR7M6BlofT08uCYjFlVN-i_OUhcj9f1h84kg:1vPFE7:2puw7psJ9MyvmzH3lshrdKsBhrvwU4hNXCow2XRbX_8','2025-12-13 07:18:39.798905'),('vr3xnjbudh9g28i71hjbpviuhzx96qwz','.eJwdzc0KgkAUBeB3ubhLyDGKElooteiHChdRbmTSq07pKPeORUXv3tTZnQOH7w2KU9mbCrVRmTSYQ2CoRxcICyQkCGAILvSMpGWDtsq8UdpOnWR-tGQP0F1ueeGnXEl_PHGE948jtJ6eynMZiundcBbp2E9k5oy2bBbrXbSqmnuS5JPDzRtUg70R4Xizi4rX8vqMa3M8EfLcMtx3SD8eAt-Fui2VTgkzC6fK2kLMPl9ilkE4:1vyNHw:evYtj3QG5xkiaY4_CT8ap2DOS3PXJbqFowHnD4jQ4kg','2026-03-07 04:59:48.671119'),('vudeac6ozvzks2yso235ujzoc17e7ppc','.eJwdjdsKgkAURf_l4KNgGmoJPURiJRGWUdSLTHpMzRtnZrAL_XtT-2nvBZv1hpInTIoCW1GmTGAGniCJOhDmSEjggQE6SI7UsgbV_FVToZ5xPnSkDtBf71luJbxglu1o5ugfLejrahetn-Em706sKQLmTnypVZf0lh1f9tTYx-fD0hj2cfg8DRRNXVrE23EtVg87dFq_ms-Uhsse6ecEz_x8ASEGOac:1vQ0nJ:jQsx44zJwkbimR4caS9h5iIcg7xdAxLbTlsat7b8XwA','2025-12-15 10:06:09.930879'),('vzpwz68rop1tzofbsgktvttfm91wh0mv','.eJyrVsrJT88vLYnPTS0uTkxPVbJS8gELKBSXJicDxdJKc5R0lEqLU4vyEnNB0iCmIVCouLQgtQjEUbIyrAUArckZeg:1vF7c8:hu06NzQrtZnkBy7jkeb7MGtzDkvQo2Ml-PO4OarXit0','2025-11-15 09:09:36.151221'),('w4302lzpb6n88og56di2a3bnid9suzy3','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxLCJpc19hdXRoZW50aWNhdGVkIjp0cnVlfQ:1vNk2o:F7OepWdHe1ISd5TKzWo7K64K0FxKUOZse5m5yfFMtEw','2025-12-09 03:48:46.069405'),('w5w9rov6fjf4lwok5s9fon4z13ly2ort','.eJwdzc0KgkAUBeB3ubhLSA1DhBZJLfrBwkWUG5n0qpM6yb2jUdG7N3V258Dhe4PkTAy6RqVlLjQWEGoa0AbCEgkJQpiCDQMjKdGhqaLopDJTL5gfdzIH6K9NUXoZ18Lz55br_GO5SgXn6lIt3WDUnEcq8VKRW7M969U2jjZ1N6ZpMT82zqSeHLS79HdxVL7Wt2fS6tOZkBeG4aFH-vEQeja090qqjDA3cCaNHfifLyG_QQo:1vnqlV:GqDqsvmfLk5b25zhF-loiuDLUXbQHLsnXVXgEGu5jzg','2026-02-06 04:14:49.175879'),('wkh1ihb5hxxqg1s6uobxah1cq6vq6whg','eyJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwicmVmZXJlciI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQvIn0:1vyk3Y:C1G0Gbh0VeJuWD6czsB4ZINWxFlwSaf0D8jLCXXXwxQ','2026-03-08 05:18:28.012236'),('wmdvui6dsr2huoe4c6ac4s92abnzxtc9','.eJxNyjEKgDAQRNGryNY2duIZvEMIcdRANCG7GxDx7kZtLOf9OSnEJaqYDcx2AQ00vtCwOldt1kAtKSPvdntygWRfiTUhP05DVxcCnGAyvPpZjJ_qs6OfFxsKjBwJX-zpugHzCiv-:1vF2CY:lC_hked-o5na5Kqhs5ybwoNtGQ7ZzGT4-vBXKdAtJ4M','2025-11-15 03:22:50.035247'),('wtf3yq3exucmwu13gorgdwwn4mvufzit','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.248917'),('x4lc2795diosa0dnohjhd95kxzw4qpz3','.eJwdzc0KgkAUBeB3ubhLqJkoRGiR1KIfKlpEuZFJrzqpk9w7GhW9e1Nndw4cvjdoTlRnSzRWp8piBqGlDn0gzJGQIIQh-NAxklENuqqyRhs3tYr5cSd3gPZaZblMuFRyMvXE6B9PGBOci0sxF0FvOY3MUcYq9cZbtov1LlqVTR_H2fRQjQblYG_FfLLZRflreXsea3s6E_LMMdy1SD8eQulDfS-0SQhTByfa2UJ-viGkQQA:1vTJZO:lZsIi29HQc-ZzCL2qVMI5VjeN0rnsf9_CoHEOT6_5x0','2025-12-11 12:45:26.137543'),('xa3kydr28qbi3n5rj777nwecd253zsp5','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.340776'),('xcwdiyoeukcuw9anbwl7kpa653a8ywik','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.435652'),('xe1p16999q3n525l63c473zaomg1d2vz','e30:1vvtF8:zY-dJxodH9DTUj3nASL9PlhdlVvfyCD7q-76JjYtGBg','2026-02-28 08:30:38.292839'),('xeu6bvae410nqof45obj2sixrmkg76h7','eyJsb2dvdXRfbWVzc2FnZSI6IkxvZ291dCBzdWNjZXNzZnVsIn0:1vFugh:Gr4v2C3kUzl8tvde1yGQruz9yYKZ8_FUVlBaPL2lhRE','2025-11-17 13:33:35.454184'),('xmwt5ppcx6f36r4yh841g9ot1n1g1onf','.eJwdzc1OwzAQBOB3WeXWiNhGbSNLHBrRAz8qqAdUconceBO7bZzIuykCxLtj2LmtRvN9g6fGzOwwsG8NowXNccYcInYYMYIGxzzpopBqfSNSpC6FEIU15I6jibaAHGbCGMyAqW3s4EN6TYboY4xpD6bj2XaqIWfUcpVJ8X-ZDKE89O_9RpZXprYKe1WbNrt9Jr5_3FUPbrjWtV29nsXCLV5YbpZPu6r72p4-9xd-O0Sku8TQPGH840GrHC5j70MTsU1w45Mt1z-_zTNJ6w:1vU0Ct:aXHUclxWskXDO7vky_-FG5wKNiH02f0BjuXdB7qOkh4','2025-12-13 10:17:03.894105'),('xxq7n9z3a6do6hsvhsu58i093s9w5ads','.eJyrVipOzUlNLklNiS_OyEwric9MUbJSMlTSQYiXJeaUpcaXVBakQiQtgJKlxalFeYm5qUBuWWpJUSZIfWlBahFIXMnKsBYASv8eWA:1vEgpY:lr_VkSpH9ZtwM2BfMR05mf9DWJng-LyrtWNbYV0BmUQ','2025-11-14 04:33:40.366733'),('y53436ged8x2hxxehe7y7wl3szqe5wsm','.eJwdzcFOwzAQBNB_WeXWiNhGLZElDo3gUEAF9YBKLpFJNrHbxLW8myBA_DuGndtqNO8bHDVmZoueXWsYO9AcZ8whYo8RI2iwzEEXhVQ3VyJF6lIIUYxuwWAGLCCHmTB6M2Eqm25yPr2CIfq4xDQH4f3c9aoha9R6k0nxf5n0vjwOb8NWlgtTW_mDqk2bXT8R3z3sq52dlrruNi9nsbKrZ5bb9eO-6r_uT5-HkV-PEek2MTQHjH88aJXDeBmcbyK2CW5csqUUP7_IR0m6:1vxKCR:UkRX-F9w-7AMx_5eonLqiWtAJcIBajNT8ifT_BCsnPc','2026-03-04 07:29:47.927977'),('y5x4zqp43eckqqur21nyjcka69qyus7a','e30:1w4YnU:tWuYZQgtPVu8ONnrlV6dJtizer_jK1pETMmG4LIhk3s','2026-03-24 06:29:56.858698'),('y8cvuft95q5vrbf5j43uxah6w59p25eq','.eJwdzc1OwzAQBOB3WeXWiNguLZElDo3gwI8K6gGVXCI33sSmjRPtOkWAeHdMd26r0Xw_4Lkxc3QYom9NRAs60ow5EHZISKDBxTjpopDq5kqkSF0KIQpr2B1GQ7aAHGZGCmbA1DZ28CG9JsP8OVLag-lwtJ1q2Bm1WmdSXC6TIZT7_r3fyPIcua3CTtWmzZbPHO8et9WDG851bdevR7Fwi5coN6unbdV933987U7xbU_It4nheUL650GrHE5j70ND2Ca48cmWy-vfPxcMShs:1wKF41:QDkOtzKzybmqZ_wVhEcQ7CumJMmmd4KR4FLa01z1r3M','2026-05-06 12:39:49.704538'),('ybvpc6zz5s4ecldwv2bk9spkw6vxftmi','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.525155'),('ydw2rirdvmpra1scxptddfe2l5a60874','.eJwdjctuwjAURP_lKjsQcZykiSyxQzyrVpHaIlaRIRfFBJtg3zxK1X-vy8xudDTnB5QrZUc1GlInSViBINvhFCye0aIFATVRK8Iw4tmM-UYiZ4yFvbz26NQDQ5hC59AaqdHTstLK-KmVzg036_-gPTbVmZeuljx9CSL2TJCNW5asdmuTxw0ln80-1-l9E6hlctCXa7Na8KG4TyJKH6_5JC6S98VOj-Ztn5H9-PqOi-w09xrXtWj_9SD47x_ibkGp:1vSU9x:m8iqbNit4TKX3-Xp0fRLkyBl8Cj0_RlT8Jm9KtMl2-I','2025-12-22 05:51:45.926217'),('yib7340tc1hiruwgspk8paqrx3vscekp','eyJ1c2VybmFtZSI6InVzZXIxIiwic3VwZXJ1c2VyIjoxfQ:1vFm1n:58h8IzBlpMJxiBGypQfw_HLV85vl-DejnJ-fsIozWw8','2025-11-17 04:18:47.288950'),('ylhfo4wr7tfdhkgqsoh5g6knxxp6561p','.eJwdzc1OwzAQBOB3WeXWiNiuGiJLHBrBgR8V1AMquURuvIlNGydab4oA8e4Ydm6r0Xzf4GNrFnYY2HeG0YJmWjAHwh4JCTQ45lkXhVTXVyJF6koIUVgT3XEyZAvIYYlIwYyY2saOPqTXbGL8mCjtwXw82V610Rm1KTMp_i-TIVSH4W3YyurCsavDXjWmy9ZPkW8fdvW9Gy9NY8uXk1i51TPL7eZxV_dfd--f-zO_HgjjTWLiMiP98aBVDudp8KEl7BLc-mSvy59fzTdJ7A:1ve9hO:phPZy9SvPySnwu6QmpbuduYs9VRqRP_OOy2hRN1DmVc','2026-01-10 10:26:30.999464'),('yupj0mjmk8108iglh98qdkmn7o7w2mfd','.eJwdjdsKgkAURf_l4KNgGmoJPURiJRGWUdSLTHpMzRtnZrAL_XtT-2nvBZv1hpInTIoCW1GmTGAGniCJOhDmSEjggQE6SI7UsgbV_FVToZ5xPnSkDtBf71luJbxglu1o5ugfLejrahetn-Em706sKQLmTnypVZf0lh1f9tTYx-fD0hj2cfg8DRRNXVrE23EtVg87dFq_ms-Uhsse6ecEz_x8ASEGOac:1vQ0tW:tRnhrESGxF5CLbGse54hgdcQMr99p8mE7Nmre_CIODs','2025-12-15 10:12:34.230702'),('yxqhts7qgujked602i4vt3kk4z24voyn','e30:1vvtF7:tlkz4qVrDLn6xqGJCi2_QIv914ISdmoD5j0pnzWQiT4','2026-02-28 08:30:37.969636'),('yypkgvfqz670c3l4lcawo2ijua6kg26n','e30:1vvtwW:0407VOR7oNxLhzk_XV50fersVv9Zz7RH-ZCVGmsqlLo','2026-02-28 09:15:28.111542'),('z1mj71mshyrxg6dfiu14kfa33rdsvqda','.eJwdjVFPwjAUhf_LzR6JbWfGoIkPBIK6GIPMQPSFXOidZcLW3LaZaPzvFs95OTk5Od8PHP0OY7DUheMBAxnQgSONgKkhJgYNNgSnhVB5eSOTlZ5IKYVBb_c9shEwguiJOzxTWl-jSpVD74ee0x-4_adp8p23mBfjTMl_ZUt3al9Wj5fqqem3eLZLLCeLmLXvhw-z-S6mYl2_vd6LYV1Xl-3Aq2nJ8_r59hQevopq3C3a2V3C-OiIr0zQ6vcPEa1CjQ:1vQ0mO:GRPEQ0uzGfg414M4iN9MeyRbXIxrR5d9u4IRRCAVxrU','2025-12-15 10:05:12.581115'),('z899tge7m7sc23l8huuw5qoqcb6y4wko','e30:1vkfY7:Ti2sJviJ5e28bDcPFZ5zygEWEoc0CCq9uaRSEBeOfkk','2026-01-28 09:39:51.917857'),('zgx0da1zjoya3vh9acwnwx016n657kcp','e30:1vvtwY:5USB42gxci0paMdydLJAW5qq9EcEjo6xm1uAOiPY32Q','2026-02-28 09:15:30.769418'),('zii02ajpjvp4z1hdxlx2cdzfcykbg8xh','.eJwdzc0KgkAUBeB3ubhLKCcSE1ootegHixZRbmTSq07lJPeORkXv3tTZnQOH7w2KM9mZGrVRuTRYQGioQxcISyQkCGEILnSMpGWDtsqiUdpOrWR-3MkeoD1fi1JkXEsx8R1v9I_jaR0cq1MVeUFvOI_1XqQyd8YbNvNVEi_rpk_Twt9dR4N6sDVeNFkncflaXJ77mzkcCXlmGe5apB8PoXDhdq-UzghzC2fK2mL6-QIhtUEI:1vbDCq:jpanp9CIcnV1TKWhHdKjW_Iu7QVnrUIGLwFy-1tAR9A','2026-01-02 07:34:48.535799'),('zxxia1395th8100u2jxyl9oj4bzzl9v4','.eJxNyssJgDAQhOFWZM9e9Jga7CGEZIyBPMTNCiL2bhQEj_P9c1IsvkjVCczGgxRNL3Qs1jabJVJPwtiySU82LoXciGXF9jipsS1E2AqneQlz1cG150A_303coeux4ovXDem4K9c:1vGGPe:6Y1fkhYccyBfQGDinkYWXa_Hp2Uydy5OEEK5ko3s6wc','2025-11-18 12:45:26.960388');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_type` varchar(20) NOT NULL,
  `code` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `superuser` tinyint(1) NOT NULL DEFAULT '0',
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'admin','1','user1','pbkdf2_sha256$1000000$1nn8XgYgA18vtscBnR2Zac$3LstDJNBIhmvZZd6Pk0+h+Ot1A5KNBfzEjyRltVXres=','user1@gmail.com','7402080605',NULL,1,'active'),(55,'Approver','2','USER2','pbkdf2_sha256$1000000$FpljQPIyJLfoWamhFa78Du$jZcgdVz59/RSYTG/wRSJyWwrP97rCSN3ltHx5J6nDjA=','','',NULL,0,NULL),(56,'approver','3','USER3 e','pbkdf2_sha256$1000000$FpljQPIyJLfoWamhFa78Du$jZcgdVz59/RSYTG/wRSJyWwrP97rCSN3ltHx5J6nDjA=','pandikumar652001@gmail.com','',NULL,0,'active'),(57,'superadmin','0','admin','pbkdf2_sha256$1000000$1nn8XgYgA18vtscBnR2Zac$3LstDJNBIhmvZZd6Pk0+h+Ot1A5KNBfzEjyRltVXres=','info@gmail.com','63',NULL,2,'active'),(58,'tester','4','vickky','pbkdf2_sha256$1000000$JtlFNV02ZCmgqDuLkpUpnJ$Gn5ic/7dp6DgY5/jyDfP0S2VsbgIFa6ohTXGAvdsRqE=','pandikumarteslead@gmail.com','',NULL,0,'active'),(59,'Approver','5','user7','pbkdf2_sha256$1000000$HQMuAyKM3ZtFRpBgcIjJtW$XpDMamaoj3p15ewcCg9zH5RjWemCfP9OJiOAxxqlQtI=','','',NULL,0,'active'),(60,'approver','1209','Resit','pbkdf2_sha256$1000000$6AYFLipNCGFcU0ElwWs1mM$P9NelKya2ZICYRJ0Wk8wCFjUEUJqzuLPaDmbEnAr09M=','','',NULL,0,NULL);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_login_logout_status`
--

DROP TABLE IF EXISTS `employee_login_logout_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_login_logout_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_code` varchar(200) DEFAULT NULL,
  `employe_name` varchar(100) DEFAULT NULL,
  `Employee_type` varchar(100) DEFAULT NULL,
  `Last_login` datetime DEFAULT NULL,
  `Last_logout` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_login_logout_status`
--

LOCK TABLES `employee_login_logout_status` WRITE;
/*!40000 ALTER TABLE `employee_login_logout_status` DISABLE KEYS */;
INSERT INTO `employee_login_logout_status` VALUES (1,'1','Dharani','Approver','2025-10-15 12:34:32','2025-10-15 12:34:44'),(2,'101','Logesh','User','2025-10-15 12:34:49','2025-10-15 12:34:57'),(3,'1','Dharani','Approver','2025-10-15 12:35:05','2025-10-15 12:35:26'),(4,'101','Logesh','User','2025-10-15 12:35:30','2025-10-15 12:35:33'),(5,'1','Dharani','Approver','2025-10-15 12:35:39','2025-10-15 12:36:29'),(6,'101','Logesh','User','2025-10-15 12:36:34','2025-10-15 12:36:37'),(7,'1','Dharani','Approver','2025-10-15 12:36:41',NULL),(8,'101','Logesh','User','2025-10-24 10:20:49',NULL),(9,'0','admin','superadmin','2025-12-09 17:07:09','2025-12-09 17:07:00'),(10,'2','USER2','Approver','2025-12-09 17:15:55','2025-12-09 17:16:05'),(11,'0','admin','superadmin','2025-12-09 17:16:16',NULL),(12,'0','admin','superadmin','2025-12-10 09:31:47',NULL),(13,'0','admin','superadmin','2025-12-11 09:20:01','2025-12-11 14:03:09'),(14,'1','user1','admin','2025-12-11 14:03:16',NULL),(15,'0','admin','superadmin','2025-12-11 14:26:58',NULL),(16,'0','admin','superadmin','2025-12-12 09:27:57','2025-12-12 13:01:28'),(17,'0','admin','superadmin','2025-12-12 13:01:40',NULL),(18,'0','admin','superadmin','2025-12-13 09:17:42',NULL),(19,'0','admin','superadmin','2025-12-15 15:05:04',NULL),(20,'0','admin','superadmin','2025-12-15 15:08:10',NULL),(21,'0','admin','superadmin','2025-12-16 09:50:01',NULL),(22,'0','admin','superadmin','2025-12-17 09:24:04',NULL),(23,'0','admin','superadmin','2025-12-18 15:21:49',NULL),(24,'0','admin','superadmin','2025-12-28 18:32:55','2025-12-29 13:04:41'),(25,'0','admin','superadmin','2025-12-29 13:34:31','2025-12-30 13:59:04'),(26,'0','admin','superadmin','2025-12-30 13:59:53',NULL),(27,'0','admin','superadmin','2025-12-30 17:50:10','2025-12-31 17:28:59'),(28,'0','admin','superadmin','2025-12-31 06:54:33',NULL),(29,'0','admin','superadmin','2026-01-01 09:00:59',NULL),(30,'0','admin','superadmin','2026-01-01 13:59:00',NULL),(31,'0','admin','superadmin','2026-01-02 12:20:11',NULL),(32,'0','admin','superadmin','2026-01-03 12:20:28',NULL),(33,'0','admin','superadmin','2026-01-04 18:23:44',NULL),(34,'0','admin','superadmin','2026-01-05 09:14:17','2026-01-07 18:06:46'),(35,'0','admin','superadmin','2026-01-08 09:31:55',NULL),(36,'0','admin','superadmin','2026-01-09 12:13:11',NULL),(37,'0','admin','superadmin','2026-01-09 16:26:41',NULL),(38,'0','admin','superadmin','2026-01-10 09:40:38',NULL),(39,'0','admin','superadmin','2026-01-12 09:27:22',NULL),(40,'0','admin','superadmin','2026-01-19 09:56:02',NULL),(41,'0','admin','superadmin','2026-01-19 17:16:55',NULL),(42,'0','admin','superadmin','2026-01-20 09:16:53',NULL),(43,'0','admin','superadmin','2026-01-21 09:33:24','2026-01-21 16:56:09'),(44,'1','user1','admin','2026-01-21 16:56:22','2026-01-21 17:15:46'),(45,'0','admin','superadmin','2026-01-21 17:15:54','2026-01-21 17:15:59'),(46,'0','admin','superadmin','2026-01-21 17:17:56','2026-01-21 17:19:05'),(47,'4','vickky','tester','2026-01-21 17:19:21','2026-01-21 17:24:00'),(48,'0','admin','superadmin','2026-01-21 17:24:07','2026-01-21 17:24:17'),(49,'4','vickky','tester','2026-01-21 17:24:23','2026-01-21 17:34:35'),(50,'0','admin','superadmin','2026-01-21 17:34:43',NULL),(51,'0','admin','superadmin','2026-01-22 09:46:51',NULL),(52,'0','admin','superadmin','2026-01-22 14:50:29',NULL),(53,'0','admin','superadmin','2026-01-23 09:47:36',NULL),(54,'0','admin','superadmin','2026-01-23 11:32:09','2026-01-23 15:53:42'),(55,'0','admin','superadmin','2026-01-23 15:53:52','2026-01-23 16:28:24'),(56,'0','admin','superadmin','2026-01-23 16:28:44',NULL),(57,'0','admin','superadmin','2026-01-23 16:44:31','2026-01-24 09:13:29'),(58,'0','admin','superadmin','2026-01-24 09:13:37',NULL),(59,'0','admin','superadmin','2026-01-27 15:10:03',NULL),(60,'0','admin','superadmin','2026-01-28 11:00:04','2026-01-28 11:04:27'),(61,'0','admin','superadmin','2026-01-28 14:49:09',NULL),(62,'0','admin','superadmin','2026-01-28 15:05:44','2026-01-28 17:19:01'),(63,'0','admin','superadmin','2026-01-28 17:19:19','2026-01-28 17:32:44'),(64,'0','admin','superadmin','2026-01-28 17:32:52','2026-01-28 17:42:47'),(65,'0','admin','superadmin','2026-01-28 17:42:55','2026-01-28 18:02:16'),(66,'0','admin','superadmin','2026-01-28 18:02:23','2026-01-28 20:29:51'),(67,'0','admin','superadmin','2026-01-28 20:29:59','2026-01-29 14:32:32'),(68,'1','user1','admin','2026-01-29 14:32:40','2026-01-29 20:04:13'),(69,'0','admin','superadmin','2026-01-29 20:04:28','2026-01-30 09:29:18'),(70,'0','admin','superadmin','2026-01-30 09:29:27','2026-01-30 14:50:32'),(71,'0','admin','superadmin','2026-01-30 14:50:54','2026-01-30 15:32:22'),(72,'0','admin','superadmin','2026-01-30 15:32:30','2026-01-30 16:37:41'),(73,'0','admin','superadmin','2026-01-30 16:37:59','2026-01-30 16:41:20'),(74,'0','admin','superadmin','2026-01-30 16:41:33','2026-01-30 17:15:55'),(75,'0','admin','superadmin','2026-01-30 17:16:04','2026-01-30 17:38:48'),(76,'0','admin','superadmin','2026-01-30 17:38:56','2026-01-30 20:34:04'),(77,'0','admin','superadmin','2026-01-30 20:34:20','2026-01-30 20:52:17'),(78,'0','admin','superadmin','2026-01-30 20:52:27','2026-01-31 09:28:22'),(79,'0','admin','superadmin','2026-01-31 09:28:30',NULL),(80,'0','admin','superadmin','2026-02-03 12:01:03','2026-02-03 12:01:09'),(81,'1','user1','admin','2026-02-03 12:02:42','2026-02-03 12:32:44'),(82,'0','admin','superadmin','2026-02-03 12:32:56',NULL),(83,'0','admin','superadmin','2026-02-04 12:02:55',NULL),(84,'0','admin','superadmin','2026-02-04 16:05:29',NULL),(85,'0','admin','superadmin','2026-02-05 09:43:25',NULL),(86,'0','admin','superadmin','2026-02-05 10:18:38','2026-02-05 13:30:47'),(87,'0','admin','superadmin','2026-02-05 13:30:58',NULL),(88,'0','admin','superadmin','2026-02-05 17:23:44',NULL),(89,'0','admin','superadmin','2026-02-06 09:27:11','2026-02-06 12:59:09'),(90,'1','user1','admin','2026-02-06 13:02:59','2026-02-06 13:47:19'),(91,'0','admin','superadmin','2026-02-06 13:47:28',NULL),(92,'0','admin','superadmin','2026-02-06 17:27:12',NULL),(93,'0','admin','superadmin','2026-02-06 18:05:41',NULL),(94,'0','admin','superadmin','2026-02-06 18:10:35',NULL),(95,'0','admin','superadmin','2026-02-07 09:35:20',NULL),(96,'0','admin','superadmin','2026-02-07 10:23:01',NULL),(97,'0','admin','superadmin','2026-02-09 09:44:29',NULL),(98,'0','admin','superadmin','2026-02-09 11:48:17','2026-02-09 11:51:54'),(99,'0','admin','superadmin','2026-02-09 11:52:15',NULL),(100,'0','admin','superadmin','2026-02-09 15:44:06',NULL),(101,'0','admin','superadmin','2026-02-13 10:16:36',NULL),(102,'0','admin','superadmin','2026-02-20 11:17:24',NULL),(103,'0','admin','superadmin','2026-02-21 10:04:46',NULL),(104,'0','admin','superadmin','2026-02-23 09:19:27',NULL),(105,'0','admin','superadmin','2026-02-27 14:01:11','2026-02-27 14:42:40'),(106,'0','admin','superadmin','2026-02-27 14:46:21',NULL),(107,'0','admin','superadmin','2026-02-28 14:54:24',NULL),(108,'0','admin','superadmin','2026-03-02 09:40:02','2026-03-03 10:02:11'),(109,'0','admin','superadmin','2026-03-03 10:02:20',NULL),(110,'0','admin','superadmin','2026-03-03 11:41:02',NULL),(111,'0','admin','superadmin','2026-03-03 13:35:17',NULL),(112,'0','admin','superadmin','2026-03-03 14:58:14',NULL),(113,'0','admin','superadmin','2026-03-04 16:08:05',NULL),(114,'0','admin','superadmin','2026-03-05 14:26:07',NULL),(115,'0','admin','superadmin','2026-03-05 15:51:26','2026-03-05 16:20:01'),(116,'0','admin','superadmin','2026-03-05 16:27:33',NULL),(117,'0','admin','superadmin','2026-03-05 16:56:58',NULL),(118,'0','admin','superadmin','2026-03-05 17:18:17',NULL),(119,'0','admin','superadmin','2026-03-05 17:29:48',NULL),(120,'0','admin','superadmin','2026-03-07 10:13:10',NULL),(121,'0','admin','superadmin','2026-03-07 10:48:35',NULL),(122,'0','admin','superadmin','2026-03-09 09:21:18','2026-03-09 11:49:36'),(123,'0','admin','superadmin','2026-03-09 12:25:27',NULL),(124,'0','admin','superadmin','2026-03-10 15:13:36',NULL),(125,'0','admin','superadmin','2026-03-10 16:32:37',NULL),(126,'0','admin','superadmin','2026-03-13 10:00:15',NULL),(127,'0','admin','superadmin','2026-03-23 09:49:27',NULL),(128,'0','admin','superadmin','2026-03-23 11:55:38',NULL),(129,'0','admin','superadmin','2026-03-23 12:07:55',NULL),(130,'0','admin','superadmin','2026-03-23 14:30:32','2026-03-25 12:40:55'),(131,'0','admin','superadmin','2026-03-25 12:42:04',NULL),(132,'0','admin','superadmin','2026-05-05 11:12:42',NULL),(133,'0','admin','superadmin','2026-05-05 16:46:41','2026-05-05 17:21:44'),(134,'0','admin','superadmin','2026-05-05 17:24:09',NULL),(135,'0','admin','superadmin','2026-05-06 14:21:57',NULL);
/*!40000 ALTER TABLE `employee_login_logout_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form_item_details`
--

DROP TABLE IF EXISTS `form_item_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form_item_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `column_name` varchar(255) NOT NULL,
  `row_details` json NOT NULL,
  `status` varchar(50) DEFAULT 'Enabled',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_item_details`
--

LOCK TABLES `form_item_details` WRITE;
/*!40000 ALTER TABLE `form_item_details` DISABLE KEYS */;
INSERT INTO `form_item_details` VALUES (1,'Connector R','{\"0\": {\"data_type\": \"INT\", \"field_name\": \"Heat No\", \"is_mandatory\": true}, \"1\": {\"data_type\": \"VARCHAR\", \"field_name\": \"MPI/DP No\", \"is_mandatory\": true}, \"2\": {\"data_type\": \"VARCHAR\", \"field_name\": \"RT No\", \"is_mandatory\": true}}','Enabled'),(9,'Connector L','{\"0\": {\"data_type\": \"INT\", \"field_name\": \"Heat No\", \"is_mandatory\": true}, \"1\": {\"data_type\": \"VARCHAR\", \"field_name\": \"MPI/DP No\", \"is_mandatory\": true}, \"2\": {\"data_type\": \"VARCHAR\", \"field_name\": \"RT No\", \"is_mandatory\": true}}','Enabled'),(10,'Body','{\"0\": {\"data_type\": \"INT\", \"field_name\": \"Heat No\", \"is_mandatory\": true}, \"1\": {\"data_type\": \"VARCHAR\", \"field_name\": \"MPI/DP No\", \"is_mandatory\": true}, \"2\": {\"data_type\": \"VARCHAR\", \"field_name\": \"RT No\", \"is_mandatory\": true}}','Enabled');
/*!40000 ALTER TABLE `form_item_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form_valve_details`
--

DROP TABLE IF EXISTS `form_valve_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form_valve_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `column_name` varchar(255) NOT NULL,
  `data_type` varchar(100) NOT NULL,
  `is_mandatory` tinyint(1) DEFAULT '0',
  `is_top_header` tinyint(1) DEFAULT '0',
  `status` varchar(50) NOT NULL DEFAULT 'Enabled',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_valve_details`
--

LOCK TABLES `form_valve_details` WRITE;
/*!40000 ALTER TABLE `form_valve_details` DISABLE KEYS */;
INSERT INTO `form_valve_details` VALUES (1,'Valve Serial No','VARCHAR',1,1,'Enabled'),(3,'Sale Order No','VARCHAR',1,0,'Enabled'),(4,'Valve Tag No','VARCHAR',1,0,'Enabled'),(5,'Sale Item No','VARCHAR',0,0,'Enabled'),(6,'Cat No','VARCHAR',0,0,'Disabled'),(7,'Gad No','VARCHAR',0,0,'Enabled'),(8,'Applicability','DROP DOWN',0,0,'Enabled'),(9,'Witnessed By','DROP DOWN',0,0,'Enabled'),(10,'Tested By','DROP DOWN',0,0,'Enabled'),(11,'Stem Orientkk','DROP DOWN',1,0,'Disabled'),(12,'Shift','DROP DOWN',0,1,'Enabled'),(13,'Date','DATE',0,1,'Enabled'),(14,'End Details','VARCHAR',0,0,'Enabled');
/*!40000 ALTER TABLE `form_valve_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gauge_color_mapping`
--

DROP TABLE IF EXISTS `gauge_color_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gauge_color_mapping` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `GAUGE_COLOR_ID` int NOT NULL,
  `RANGE1_VALUE` decimal(10,2) DEFAULT NULL,
  `RANGE1_COLOR` varchar(20) DEFAULT NULL,
  `RANGE2_VALUE` decimal(10,2) DEFAULT NULL,
  `RANGE2_COLOR` varchar(20) DEFAULT NULL,
  `RANGE3_VALUE` decimal(10,2) DEFAULT NULL,
  `RANGE3_COLOR` varchar(20) DEFAULT NULL,
  `CREATED_AT` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gauge_color_mapping`
--

LOCK TABLES `gauge_color_mapping` WRITE;
/*!40000 ALTER TABLE `gauge_color_mapping` DISABLE KEYS */;
/*!40000 ALTER TABLE `gauge_color_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gauge_details`
--

DROP TABLE IF EXISTS `gauge_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gauge_details` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `GD_ID` int NOT NULL,
  `GD_SERIAL_NUMBER` varchar(255) NOT NULL,
  `GD_STATION_ID` varchar(50) DEFAULT NULL,
  `GD_MEDIUM` varchar(255) NOT NULL,
  `GD_PRESSURE_RANGE_PSI` varchar(45) DEFAULT NULL,
  `GD_PRESSURE_RANGE_BAR` varchar(45) DEFAULT NULL,
  `GD_PRESSURE_RANGE_KG/CM2` varchar(45) DEFAULT NULL,
  `GD_DONE_DATE` date DEFAULT NULL,
  `GD_DUE_DATE` date DEFAULT NULL,
  `GD_STATUS` int DEFAULT '1',
  `GD_DUE_ALARM` tinyint DEFAULT '0',
  `GD_CREATED_DATE` datetime DEFAULT CURRENT_TIMESTAMP,
  `GD_UPDATED_DATE` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`GD_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gauge_details`
--

LOCK TABLES `gauge_details` WRITE;
/*!40000 ALTER TABLE `gauge_details` DISABLE KEYS */;
INSERT INTO `gauge_details` VALUES (22,1,'GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13',1,0,'2025-12-16 10:54:44','2026-03-24 06:02:18'),(24,2,'GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:08:04','2026-03-24 06:02:18'),(25,3,'GSN-003','2','Hydro','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:12:50','2026-03-24 06:02:18'),(26,4,'GSN-004','2','Hydro','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:12:50','2026-03-24 06:02:18'),(27,5,'GSN-005','3','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:12:50','2026-03-24 06:02:18'),(28,6,'GSN-006','3','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:12:50','2026-03-24 06:02:18'),(29,7,'GSN-007','4','Hydro','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:12:50','2026-03-24 06:02:18'),(30,8,'GSN-008','4','Hydro','0-2000','0-200','0-200','2026-03-20','2026-03-30',1,0,'2026-03-10 11:12:50','2026-03-24 06:02:18');
/*!40000 ALTER TABLE `gauge_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gauge_details_test_log`
--

DROP TABLE IF EXISTS `gauge_details_test_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gauge_details_test_log` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SERIAL_NUMBER` varchar(100) NOT NULL,
  `PRESSURE_UNIT` varchar(20) NOT NULL,
  `GD_SERIAL_NUMBER` varchar(100) NOT NULL,
  `GD_STATION_ID` varchar(100) DEFAULT NULL,
  `GD_MEDIUM` varchar(50) DEFAULT NULL,
  `GD_PRESSURE_RANGE_PSI` varchar(50) DEFAULT NULL,
  `GD_PRESSURE_RANGE_BAR` varchar(50) DEFAULT NULL,
  `GD_PRESSURE_RANGE_KG_CM2` varchar(50) DEFAULT NULL,
  `GD_DONE_DATE` date DEFAULT NULL,
  `GD_DUE_DATE` date DEFAULT NULL,
  `CREATED_DATE` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gauge_details_test_log`
--

LOCK TABLES `gauge_details_test_log` WRITE;
/*!40000 ALTER TABLE `gauge_details_test_log` DISABLE KEYS */;
INSERT INTO `gauge_details_test_log` VALUES (94,'123456','PSI','GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13','2026-05-06 14:49:47'),(95,'123456','PSI','GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30','2026-05-06 14:49:47'),(96,'147852','PSI','GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13','2026-05-06 16:45:29'),(97,'147852','PSI','GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30','2026-05-06 16:45:29'),(98,'147852','PSI','GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13','2026-05-06 16:53:29'),(99,'147852','PSI','GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30','2026-05-06 16:53:29'),(100,'147852','PSI','GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13','2026-05-06 17:13:47'),(101,'147852','PSI','GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30','2026-05-06 17:13:47'),(102,'147852','PSI','GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13','2026-05-06 17:20:05'),(103,'147852','PSI','GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30','2026-05-06 17:20:05'),(104,'222222','PSI','GSN-001','1','Air','0-2000','0-200','0-200','2025-12-09','2026-05-13','2026-05-06 19:03:56'),(105,'222222','PSI','GSN-002','1','Air','0-2000','0-200','0-200','2026-03-20','2026-03-30','2026-05-06 19:03:56');
/*!40000 ALTER TABLE `gauge_details_test_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gauge_log_details`
--

DROP TABLE IF EXISTS `gauge_log_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gauge_log_details` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `INSTRUMENT_ID` int NOT NULL,
  `INSTRUMENT_SER_NO` varchar(255) NOT NULL,
  `RANGE` varchar(255) NOT NULL,
  `INSTRUMENT_TYPE` varchar(255) NOT NULL,
  `CAL_DUE_DATE` date NOT NULL,
  `CAL_DONE_DATE` date NOT NULL,
  `STATION_ID` int NOT NULL,
  `CREATED_DATE` timestamp NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=513 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gauge_log_details`
--

LOCK TABLES `gauge_log_details` WRITE;
/*!40000 ALTER TABLE `gauge_log_details` DISABLE KEYS */;
INSERT INTO `gauge_log_details` VALUES (1,1,'TL-25001','0-1000','HYDRO','2025-11-01','2025-10-31',1,'2025-11-01 04:04:07'),(2,1,'TL-25001','0-1000','HYDRO','2025-11-01','2025-10-31',1,'2025-11-01 04:04:39'),(3,2,'TL-25002','0-6','AIR','2025-11-01','2025-10-31',2,'2025-11-01 04:04:39'),(4,1,'TL-25001','0-1000','HYDRO','2025-11-01','2025-10-31',1,'2025-11-02 22:58:18'),(5,2,'TL-25002','0-6','AIR','2025-11-01','2025-10-31',2,'2025-11-02 22:58:18'),(6,3,'','0-250','','2025-11-06','2025-11-03',0,'2025-11-02 22:58:18'),(7,3,'TL-25003','0-250','','2025-11-06','2025-11-03',0,'2025-11-02 22:58:50'),(8,1,'TL-25001','0-1000','HYDRO','2025-11-01','2025-10-31',1,'2025-11-02 22:58:50'),(9,2,'TL-25002','0-6','AIR','2025-11-01','2025-10-31',2,'2025-11-02 22:58:50'),(10,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:06:21'),(11,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',2,'2025-11-02 23:06:21'),(12,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:13:39'),(13,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',2,'2025-11-02 23:13:39'),(14,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:13:48'),(15,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',2,'2025-11-02 23:13:48'),(16,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:16:39'),(17,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',2,'2025-11-02 23:16:39'),(18,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:20:32'),(19,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',2,'2025-11-02 23:20:32'),(20,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:20:42'),(21,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',2,'2025-11-02 23:20:42'),(22,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:39:19'),(23,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:39:19'),(24,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:39:37'),(25,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:39:37'),(26,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:39:37'),(27,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:40:01'),(28,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:40:01'),(29,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:40:01'),(30,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:40:01'),(31,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:40:20'),(32,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:40:20'),(33,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:40:20'),(34,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:40:20'),(35,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:40:20'),(36,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:40:35'),(37,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:40:35'),(38,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:40:35'),(39,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:40:35'),(40,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:40:35'),(41,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:40:35'),(42,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:41:00'),(43,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:41:00'),(44,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:41:00'),(45,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:41:00'),(46,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:41:00'),(47,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:41:00'),(48,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:41:00'),(49,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:41:24'),(50,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:41:24'),(51,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:41:24'),(52,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:41:24'),(53,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:41:24'),(54,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:41:24'),(55,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:41:24'),(56,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:41:24'),(57,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:41:44'),(58,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:41:44'),(59,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:41:44'),(60,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:41:44'),(61,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:41:44'),(62,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:41:44'),(63,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:41:44'),(64,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:41:44'),(65,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:41:44'),(66,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:42:33'),(67,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:42:33'),(68,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:42:33'),(69,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:42:33'),(70,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:42:33'),(71,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:42:33'),(72,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:42:33'),(73,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:42:33'),(74,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:42:33'),(75,10,'8','1-100','AIR','2025-11-28','2025-11-17',1,'2025-11-02 23:42:33'),(76,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:43:14'),(77,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:43:14'),(78,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:43:14'),(79,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:43:14'),(80,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:43:14'),(81,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:43:14'),(82,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:43:14'),(83,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:43:14'),(84,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:43:14'),(85,10,'8','1-100','AIR','2025-11-28','2025-11-17',1,'2025-11-02 23:43:14'),(86,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',2,'2025-11-02 23:43:14'),(87,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:43:46'),(88,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:43:46'),(89,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:43:46'),(90,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:43:46'),(91,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:43:46'),(92,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:43:46'),(93,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:43:46'),(94,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:43:46'),(95,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:43:46'),(96,10,'8','1-100','AIR','2025-11-28','2025-11-17',1,'2025-11-02 23:43:46'),(97,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',0,'2025-11-02 23:43:46'),(98,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',0,'2025-11-02 23:55:50'),(99,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:55:50'),(100,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:55:50'),(101,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:55:50'),(102,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:55:50'),(103,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:55:50'),(104,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:55:50'),(105,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:55:50'),(106,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:55:50'),(107,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:55:50'),(108,12,'8','100-250','HYDRO','2025-11-27','2025-11-03',1,'2025-11-02 23:55:50'),(109,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-02 23:57:48'),(110,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:57:48'),(111,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:57:48'),(112,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:57:48'),(113,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:57:48'),(114,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:57:48'),(115,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:57:48'),(116,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:57:48'),(117,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:57:48'),(118,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:57:48'),(119,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:58:31'),(120,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:58:31'),(121,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:31'),(122,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:58:31'),(123,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:58:31'),(124,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:31'),(125,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:58:31'),(126,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:58:31'),(127,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:58:31'),(128,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-02 23:58:31'),(129,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:31'),(130,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:58:43'),(131,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:58:43'),(132,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:43'),(133,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:58:43'),(134,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:58:43'),(135,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:43'),(136,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:58:43'),(137,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:58:43'),(138,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:58:43'),(139,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',2,'2025-11-02 23:58:43'),(140,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:43'),(141,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:58:51'),(142,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:58:51'),(143,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:51'),(144,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:58:51'),(145,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:58:51'),(146,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:51'),(147,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:58:51'),(148,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:58:51'),(149,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:58:51'),(150,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:58:51'),(151,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-02 23:58:51'),(152,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:59:03'),(153,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:59:03'),(154,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:03'),(155,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:59:03'),(156,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:59:03'),(157,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:03'),(158,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:59:03'),(159,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:59:03'),(160,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:59:03'),(161,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-02 23:59:03'),(162,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:03'),(163,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:59:36'),(164,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:59:36'),(165,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:36'),(166,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:59:36'),(167,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:59:36'),(168,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:36'),(169,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:59:36'),(170,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:59:36'),(171,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:59:36'),(172,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-02 23:59:36'),(173,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:36'),(174,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-02 23:59:40'),(175,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-02 23:59:40'),(176,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:40'),(177,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-02 23:59:40'),(178,5,'3','0-1000','AIR','2025-11-14','2025-11-03',1,'2025-11-02 23:59:40'),(179,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-02 23:59:40'),(180,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-02 23:59:40'),(181,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-02 23:59:40'),(182,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-02 23:59:40'),(183,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-02 23:59:40'),(184,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',2,'2025-11-02 23:59:40'),(185,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-03 00:00:01'),(186,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-03 00:00:01'),(187,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:00:01'),(188,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-03 00:00:01'),(189,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 00:00:01'),(190,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:00:01'),(191,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 00:00:01'),(192,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 00:00:01'),(193,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 00:00:01'),(194,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 00:00:01'),(195,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:00:01'),(196,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-03 00:00:06'),(197,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-03 00:00:06'),(198,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:00:06'),(199,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-03 00:00:06'),(200,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:00:06'),(201,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 00:00:06'),(202,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 00:00:06'),(203,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 00:00:06'),(204,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 00:00:06'),(205,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:00:06'),(206,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 00:00:06'),(207,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-03 00:04:50'),(208,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-03 00:04:50'),(209,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-03 00:04:50'),(210,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:04:50'),(211,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 00:04:50'),(212,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 00:04:50'),(213,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 00:04:50'),(214,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 00:04:50'),(215,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 00:04:50'),(216,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:04:50'),(217,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 00:04:50'),(218,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-03 01:51:29'),(219,2,'TL-25002','0-6','AIR','2025-11-05','2025-10-31',1,'2025-11-03 01:51:29'),(220,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-03 01:51:29'),(221,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:51:29'),(222,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:51:29'),(223,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:51:29'),(224,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:51:29'),(225,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:51:29'),(226,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:51:29'),(227,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:51:29'),(228,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:51:29'),(229,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-03 01:53:24'),(230,2,'TL-25002','','AIR','2025-11-05','2025-10-31',1,'2025-11-03 01:53:24'),(231,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-03 01:53:24'),(232,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:53:24'),(233,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:53:24'),(234,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:53:24'),(235,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:53:24'),(236,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:53:24'),(237,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:53:24'),(238,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:53:24'),(239,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:53:24'),(240,1,'TL-25001','0-1000','HYDRO','2025-11-06','2025-10-31',1,'2025-11-03 01:54:01'),(241,2,'TL-25002','0-100','AIR','2025-11-05','2025-10-31',1,'2025-11-03 01:54:01'),(242,4,'2','0-1000','HYDRO','2025-11-19','2025-11-04',1,'2025-11-03 01:54:01'),(243,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:54:01'),(244,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:54:01'),(245,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:54:01'),(246,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:54:01'),(247,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:54:01'),(248,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:54:01'),(249,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:54:01'),(250,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:54:01'),(251,1,'TL-25001','0-1000','HYDRO','2025-11-07','2025-10-31',1,'2025-11-03 01:56:08'),(252,2,'TL-25002','0-100','AIR','2025-11-08','2025-10-31',1,'2025-11-03 01:56:08'),(253,4,'2','0-1000','HYDRO','2025-12-02','2025-10-27',1,'2025-11-03 01:56:08'),(254,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:56:08'),(255,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:56:08'),(256,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:56:08'),(257,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:56:08'),(258,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:56:08'),(259,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:56:08'),(260,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:56:08'),(261,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:56:08'),(262,1,'TL-25001','0-1000','HYDRO','2025-11-07','2025-10-31',1,'2025-11-03 01:56:48'),(263,2,'TL-25002','0-100','AIR','2025-11-08','2025-10-31',1,'2025-11-03 01:56:48'),(264,4,'2','0-1000','HYDRO','2025-11-05','2025-10-27',1,'2025-11-03 01:56:48'),(265,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:56:48'),(266,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:56:48'),(267,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:56:48'),(268,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:56:48'),(269,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:56:48'),(270,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:56:48'),(271,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:56:48'),(272,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:56:48'),(273,1,'TL-25001','0-1000','HYDRO','2025-11-07','2025-10-31',1,'2025-11-03 01:57:12'),(274,2,'TL-25002','0-100','AIR','2025-11-08','2025-10-31',1,'2025-11-03 01:57:12'),(275,4,'2','0-1000','HYDRO','2025-11-03','2025-10-27',1,'2025-11-03 01:57:12'),(276,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:57:12'),(277,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:57:12'),(278,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:57:12'),(279,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:57:12'),(280,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:57:12'),(281,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:57:12'),(282,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:57:12'),(283,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:57:12'),(284,1,'TL-25001','0-1000','HYDRO','2025-11-07','2025-10-31',1,'2025-11-03 01:59:59'),(285,2,'TL-25002','0-100','AIR','2025-11-08','2025-10-31',1,'2025-11-03 01:59:59'),(286,4,'2','0-1000','HYDRO','2025-11-03','2025-10-27',1,'2025-11-03 01:59:59'),(287,6,'4','0-250','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:59:59'),(288,7,'5','0-1000','HYDRO','2025-11-29','2025-11-10',1,'2025-11-03 01:59:59'),(289,9,'7','0-250','AIR','2025-11-20','2025-11-03',1,'2025-11-03 01:59:59'),(290,11,'1234','0-250','HYDRO','2025-11-20','2025-11-03',1,'2025-11-03 01:59:59'),(291,5,'3','0-1000','AIR','2025-11-14','2025-11-03',2,'2025-11-03 01:59:59'),(292,3,'1','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:59:59'),(293,8,'6','0-250','HYDRO','2025-11-21','2025-11-03',1,'2025-11-03 01:59:59'),(294,12,'8','0-1000','HYDRO','2025-11-28','2025-11-03',1,'2025-11-03 01:59:59'),(295,4,'2','0-1000','','2025-11-13','2025-10-27',1,'2025-11-03 02:02:41'),(296,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 02:02:41'),(297,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 02:02:41'),(298,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 02:02:41'),(299,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 02:02:41'),(300,5,'3','0-1000','','2025-11-14','2025-11-03',2,'2025-11-03 02:02:41'),(301,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 02:02:41'),(302,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 02:02:41'),(303,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 02:02:41'),(304,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 02:02:41'),(305,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 02:02:41'),(306,4,'2','','','2025-11-13','2025-10-27',1,'2025-11-03 02:41:06'),(307,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 02:41:06'),(308,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 02:41:06'),(309,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 02:41:06'),(310,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 02:41:06'),(311,5,'3','0-1000','','2025-11-14','2025-11-03',2,'2025-11-03 02:41:06'),(312,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 02:41:06'),(313,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 02:41:06'),(314,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 02:41:06'),(315,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 02:41:06'),(316,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 02:41:06'),(317,4,'2','0-100','','2025-11-13','2025-10-27',1,'2025-11-03 02:47:01'),(318,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 02:47:01'),(319,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 02:47:01'),(320,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 02:47:01'),(321,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 02:47:01'),(322,5,'3','0-1000','','2025-11-14','2025-11-03',2,'2025-11-03 02:47:01'),(323,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 02:47:01'),(324,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 02:47:01'),(325,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 02:47:01'),(326,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 02:47:01'),(327,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 02:47:01'),(328,4,'2','0-100','','2025-11-13','2025-10-27',1,'2025-11-03 06:59:10'),(329,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 06:59:10'),(330,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 06:59:10'),(331,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 06:59:10'),(332,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 06:59:10'),(333,5,'3','0-1000','','2025-11-14','2025-11-03',2,'2025-11-03 06:59:10'),(334,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 06:59:10'),(335,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 06:59:10'),(336,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 06:59:10'),(337,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 06:59:10'),(338,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 06:59:10'),(339,4,'2','0-100','','2025-11-13','2025-10-27',1,'2025-11-03 07:00:18'),(340,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 07:00:18'),(341,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 07:00:18'),(342,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:00:18'),(343,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:00:18'),(344,5,'3','0-1000','','2025-11-14','2025-11-03',2,'2025-11-03 07:00:18'),(345,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 07:00:18'),(346,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 07:00:18'),(347,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:00:18'),(348,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 07:00:18'),(349,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:00:18'),(350,4,'2','0-100','','2025-11-03','2025-10-27',1,'2025-11-03 07:01:45'),(351,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 07:01:45'),(352,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 07:01:45'),(353,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:01:45'),(354,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:01:45'),(355,5,'3','0-1000','','2025-11-14','2025-11-03',2,'2025-11-03 07:01:45'),(356,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 07:01:45'),(357,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 07:01:45'),(358,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:01:45'),(359,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 07:01:45'),(360,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:01:45'),(361,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 07:02:23'),(362,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:02:23'),(363,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:02:23'),(364,5,'3','0-1000','','2025-11-14','2025-11-03',1,'2025-11-03 07:02:23'),(365,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 07:02:23'),(366,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 07:02:23'),(367,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:02:23'),(368,4,'2','0-100','','2025-11-03','2025-10-27',1,'2025-11-03 07:02:23'),(369,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 07:02:23'),(370,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 07:02:23'),(371,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:02:23'),(372,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 07:02:44'),(373,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 07:02:44'),(374,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:02:44'),(375,4,'2','0-100','','2025-11-03','2025-10-27',1,'2025-11-03 07:02:44'),(376,5,'3','0-1000','','2025-11-14','2025-11-03',1,'2025-11-03 07:02:44'),(377,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 07:02:44'),(378,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 07:02:44'),(379,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:02:44'),(380,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:02:44'),(381,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 07:02:44'),(382,12,'8','0-1000','','2025-11-28','2025-11-03',2,'2025-11-03 07:02:44'),(383,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 07:03:09'),(384,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 07:03:09'),(385,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:03:09'),(386,4,'2','0-100','','2025-11-03','2025-10-27',1,'2025-11-03 07:03:09'),(387,5,'3','0-1000','','2025-11-14','2025-11-03',1,'2025-11-03 07:03:09'),(388,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 07:03:09'),(389,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 07:03:09'),(390,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 07:03:09'),(391,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:03:09'),(392,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:03:09'),(393,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:03:09'),(394,1,'TL-25001','0-1000','','2025-11-07','2025-10-31',1,'2025-11-03 07:04:31'),(395,2,'TL-25002','0-100','','2025-11-08','2025-10-31',1,'2025-11-03 07:04:31'),(396,3,'1','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:04:31'),(397,4,'2','0-100','','2025-11-28','2025-10-27',1,'2025-11-03 07:04:31'),(398,5,'3','0-1000','','2025-11-14','2025-11-03',1,'2025-11-03 07:04:31'),(399,6,'4','0-250','','2025-11-28','2025-11-03',1,'2025-11-03 07:04:31'),(400,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-03 07:04:31'),(401,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-03 07:04:31'),(402,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:04:31'),(403,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-03 07:04:31'),(404,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-03 07:04:31'),(405,1,'TL-25001','0-1000','HYDRO_shell','2025-11-07','2025-10-31',1,'2025-11-04 06:23:13'),(406,2,'TL-25002','0-100','HYDRO_shell','2025-11-08','2025-10-31',1,'2025-11-04 06:23:13'),(407,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-04 06:23:13'),(408,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-04 06:23:13'),(409,5,'3','0-1000','HYDRO_shell','2025-11-14','2025-11-03',2,'2025-11-04 06:23:13'),(410,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-04 06:23:13'),(411,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-04 06:23:13'),(412,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-04 06:23:13'),(413,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-04 06:23:13'),(414,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-04 06:23:13'),(415,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-04 06:23:13'),(416,1,'TL-25001','0-1000','HYDRO_shell','2025-11-11','2025-10-31',1,'2025-11-08 01:02:54'),(417,2,'TL-25002','0-100','HYDRO_shell','2025-11-12','2025-10-31',1,'2025-11-08 01:02:54'),(418,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-08 01:02:54'),(419,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-08 01:02:54'),(420,5,'3','0-1000','HYDRO_shell','2025-11-14','2025-11-03',2,'2025-11-08 01:02:54'),(421,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-08 01:02:54'),(422,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-08 01:02:54'),(423,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-08 01:02:54'),(424,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-08 01:02:54'),(425,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-08 01:02:54'),(426,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-08 01:02:54'),(427,1,'TL-25001','0-1000','HYDRO_shell','2025-11-11','2025-10-31',1,'2025-11-10 04:35:16'),(428,2,'TL-25002','0-100','HYDRO_shell','2025-11-12','2025-10-31',1,'2025-11-10 04:35:16'),(429,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-10 04:35:16'),(430,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-10 04:35:16'),(431,5,'3','0-1000','HYDRO_shell','2025-11-14','2025-11-03',2,'2025-11-10 04:35:16'),(432,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-10 04:35:16'),(433,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-10 04:35:16'),(434,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-10 04:35:16'),(435,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-10 04:35:16'),(436,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-10 04:35:16'),(437,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-10 04:35:16'),(438,1,'TL-25001','0-1000','HYDRO_shell','2025-11-12','2025-10-31',0,'2025-11-10 04:55:02'),(439,2,'TL-25002','0-100','HYDRO_shell','2025-11-12','2025-10-31',1,'2025-11-10 04:55:02'),(440,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-10 04:55:02'),(441,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-10 04:55:02'),(442,5,'3','0-1000','HYDRO_shell','2025-11-14','2025-11-03',2,'2025-11-10 04:55:02'),(443,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-10 04:55:02'),(444,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-10 04:55:02'),(445,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-10 04:55:02'),(446,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-10 04:55:02'),(447,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-10 04:55:02'),(448,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-10 04:55:02'),(449,1,'TL-25001','0-1000','HYDRO_shell','2025-11-27','2025-10-31',0,'2025-11-11 22:38:35'),(450,2,'TL-25002','0-100','HYDRO_shell','2025-11-25','2025-10-31',1,'2025-11-11 22:38:35'),(451,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-11 22:38:35'),(452,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-11 22:38:35'),(453,5,'3','0-1000','HYDRO_shell','2025-11-14','2025-11-03',2,'2025-11-11 22:38:35'),(454,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-11 22:38:35'),(455,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-11 22:38:35'),(456,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-11 22:38:35'),(457,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-11 22:38:35'),(458,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-11 22:38:35'),(459,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-11 22:38:35'),(460,1,'TL-25001','0-1000','HYDRO_shell','2025-11-27','2025-10-31',0,'2025-11-13 22:22:23'),(461,2,'TL-25002','0-100','HYDRO_shell','2025-11-25','2025-10-31',1,'2025-11-13 22:22:23'),(462,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-13 22:22:23'),(463,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-13 22:22:23'),(464,5,'3','0-1000','HYDRO_shell','2025-11-15','2025-11-03',2,'2025-11-13 22:22:23'),(465,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-13 22:22:23'),(466,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-13 22:22:23'),(467,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-13 22:22:23'),(468,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-13 22:22:23'),(469,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-13 22:22:23'),(470,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-13 22:22:23'),(471,1,'TL-25001','0-1000','HYDRO_shell','2025-11-27','2025-10-31',0,'2025-11-14 22:12:18'),(472,2,'TL-25002','0-100','HYDRO_shell','2025-11-25','2025-10-31',1,'2025-11-14 22:12:18'),(473,3,'1','0-1000','HYDRO_shell','2025-11-28','2025-11-03',1,'2025-11-14 22:12:18'),(474,4,'2','0-100','HYDRO_shell','2025-11-28','2025-10-27',2,'2025-11-14 22:12:18'),(475,5,'3','0-1000','HYDRO_shell','2025-11-18','2025-11-03',2,'2025-11-14 22:12:18'),(476,7,'5','0-1000','','2025-11-29','2025-11-10',1,'2025-11-14 22:12:18'),(477,8,'6','0-250','','2025-11-21','2025-11-03',1,'2025-11-14 22:12:18'),(478,9,'7','0-250','','2025-11-20','2025-11-03',1,'2025-11-14 22:12:18'),(479,11,'1234','0-250','','2025-11-20','2025-11-03',1,'2025-11-14 22:12:18'),(480,12,'8','0-1000','','2025-11-28','2025-11-03',1,'2025-11-14 22:12:18'),(481,6,'4','0-250','HYDRO_shell','2025-11-28','2025-11-03',2,'2025-11-14 22:12:18'),(482,1,'1','0-1000','HYDRO','2025-11-19','2025-11-13',1,'2025-11-15 01:27:41'),(483,2,'2','0-150','AIR','2025-11-17','2025-11-11',1,'2025-11-15 01:27:41'),(484,1,'1','0-1000','HYDRO','2025-11-19','2025-11-13',1,'2025-11-15 01:28:26'),(485,2,'2','0-150','AIR','2025-11-17','2025-11-11',1,'2025-11-15 01:28:26'),(486,3,'3','0-1000','GAS','2025-11-18','2025-11-11',2,'2025-11-15 01:28:26'),(487,1,'1','0-1000','HYDRO','2025-11-19','2025-11-13',1,'2025-11-15 01:30:09'),(488,2,'2','0-150','AIR','2025-11-17','2025-11-11',1,'2025-11-15 01:30:09'),(489,3,'3','0-1000','GAS','2025-11-18','2025-11-11',2,'2025-11-15 01:30:09'),(490,4,'4','0-150','GAS','2025-11-24','2025-11-10',2,'2025-11-15 01:30:09'),(491,1,'1','0-1000','HYDRO','2025-11-19','2025-11-13',1,'2025-11-17 02:19:27'),(492,2,'2','0-150','AIR','2025-11-20','2025-11-11',1,'2025-11-17 02:19:27'),(493,4,'4','0-150','GAS','2025-11-24','2025-11-10',2,'2025-11-17 02:19:27'),(494,3,'3','0-1000','GAS','2025-11-18','2025-11-11',2,'2025-11-17 02:19:27'),(495,1,'1','0-1000','HYDRO','2025-11-25','2025-11-13',1,'2025-11-18 22:11:25'),(496,2,'2','0-150','AIR','2025-11-20','2025-11-11',1,'2025-11-18 22:11:25'),(497,4,'4','0-150','GAS','2025-11-24','2025-11-10',2,'2025-11-18 22:11:25'),(498,3,'3','0-1000','GAS','2025-11-21','2025-11-11',2,'2025-11-18 22:11:25'),(499,1,'1','0-1000','AIR','2025-11-27','2025-11-13',1,'2025-11-26 04:45:01'),(500,2,'2','0-150','AIR','2025-11-29','2025-11-11',1,'2025-11-26 04:45:01'),(501,4,'4','0-150','GAS','2025-11-29','2025-11-10',2,'2025-11-26 04:45:01'),(502,3,'3','0-1000','GAS','2025-11-29','2025-11-11',2,'2025-11-26 04:45:01'),(503,1,'1','0-1000','AIR','2025-11-27','2025-11-13',1,'2025-11-26 04:45:05'),(504,2,'2','0-150','AIR','2025-11-29','2025-11-11',1,'2025-11-26 04:45:05'),(505,4,'4','0-150','GAS','2025-11-29','2025-11-10',2,'2025-11-26 04:45:05'),(506,3,'3','0-1000','GAS','2025-11-29','2025-11-11',2,'2025-11-26 04:45:05'),(507,1,'1','0-1000','AIR','2025-11-29','2025-11-13',1,'2025-11-27 05:36:55'),(508,2,'2','0-150','AIR','2025-11-29','2025-11-11',1,'2025-11-27 05:36:55'),(509,4,'4','0-150','GAS','2025-11-29','2025-11-10',2,'2025-11-27 05:36:55'),(510,3,'3','0-1000','GAS','2025-11-29','2025-11-11',2,'2025-11-27 05:36:55'),(511,1,'1','0-100','AIR','2025-12-31','2025-12-09',1,'2025-12-16 05:24:44'),(512,1,'1','0-100','AIR','2026-02-28','2025-12-09',1,'2026-01-29 04:18:47');
/*!40000 ALTER TABLE `gauge_log_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gauge_mapping`
--

DROP TABLE IF EXISTS `gauge_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gauge_mapping` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `GAUGE_ID` int NOT NULL,
  `COL1_NAME` varchar(100) DEFAULT NULL,
  `COL1_E_D` varchar(10) DEFAULT NULL,
  `COL2_NAME` varchar(100) DEFAULT NULL,
  `COL2_E_D` varchar(10) DEFAULT NULL,
  `COL3_NAME` varchar(100) DEFAULT NULL,
  `COL3_E_D` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gauge_mapping`
--

LOCK TABLES `gauge_mapping` WRITE;
/*!40000 ALTER TABLE `gauge_mapping` DISABLE KEYS */;
/*!40000 ALTER TABLE `gauge_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hmi_abrs_address`
--

DROP TABLE IF EXISTS `hmi_abrs_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hmi_abrs_address` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `HMI_IP` varchar(50) DEFAULT NULL,
  `ABRS_HOST_ADDR` varchar(50) DEFAULT NULL,
  `ABRS_PORT` int DEFAULT NULL,
  `ABRS_DATABASE` varchar(50) DEFAULT NULL,
  `ABRS_USERNAME` varchar(50) DEFAULT NULL,
  `ABRS_PASSWORD` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hmi_abrs_address`
--

LOCK TABLES `hmi_abrs_address` WRITE;
/*!40000 ALTER TABLE `hmi_abrs_address` DISABLE KEYS */;
INSERT INTO `hmi_abrs_address` VALUES (1,'127.0.0.1','localhost',1433,'ABRSSample','E','2');
/*!40000 ALTER TABLE `hmi_abrs_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instrument_categories`
--

DROP TABLE IF EXISTS `instrument_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instrument_categories` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `INSTRUMENT_ID` int NOT NULL,
  `INSTRUMENT_SERIAL_NUMBER` varchar(45) NOT NULL,
  `INSTRUMENT_TYPE` varchar(255) NOT NULL,
  `INSTRUMENT_DONE_DATE` varchar(45) NOT NULL,
  `INSTRUMENT_DUE_DATE` varchar(45) NOT NULL,
  `INSTRUMENT_DUE_ALARM` varchar(45) NOT NULL,
  `INSTRUMENT_STATUS` varchar(45) NOT NULL DEFAULT 'ACTIVE',
  `CREATED_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`INSTRUMENT_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instrument_categories`
--

LOCK TABLES `instrument_categories` WRITE;
/*!40000 ALTER TABLE `instrument_categories` DISABLE KEYS */;
INSERT INTO `instrument_categories` VALUES (15,1,'1','Torque Wrench 11','2232-02-22','3223-02-23','0','ENABLE','2026-02-07 05:01:00','2026-03-25 05:59:42'),(16,2,'2','Torque Wrench 2','2026-02-03','2026-02-23','1','ENABLE','2026-02-07 05:01:00','2026-03-25 05:59:42'),(17,3,'3','VERNIER CALIPER','2026-03-18','2026-03-11','1','DISABLE','2026-03-23 04:56:49','2026-03-25 05:59:42'),(18,4,'4','LUX METER','2026-03-10','2026-04-01','1','DISABLE','2026-03-23 05:11:40','2026-05-05 05:42:44'),(19,5,'5','STOP WATCH','2026-03-24','2026-03-25','1','ENABLE','2026-03-23 05:11:56','2026-05-05 05:42:44'),(20,6,'6','THERMOMETER','2026-03-26','2026-04-09','1','ENABLE','2026-03-23 05:12:17','2026-05-05 05:42:44');
/*!40000 ALTER TABLE `instrument_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instrument_test_log`
--

DROP TABLE IF EXISTS `instrument_test_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instrument_test_log` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SERIAL_NUMBER` varchar(100) NOT NULL,
  `INSTRUMENT_SERIAL_NUMBER` varchar(100) DEFAULT NULL,
  `INSTRUMENT_TYPE` varchar(100) DEFAULT NULL,
  `INSTRUMENT_DONE_DATE` varchar(100) DEFAULT NULL,
  `INSTRUMENT_DUE_DATE` varchar(100) DEFAULT NULL,
  `CREATED_DATE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=225 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instrument_test_log`
--

LOCK TABLES `instrument_test_log` WRITE;
/*!40000 ALTER TABLE `instrument_test_log` DISABLE KEYS */;
INSERT INTO `instrument_test_log` VALUES (201,'123456','1','Torque Wrench 11','2232-02-22','3223-02-23','2026-05-06 14:49:47'),(202,'123456','2','Torque Wrench 2','2026-02-03','2026-02-23','2026-05-06 14:49:47'),(203,'123456','5','STOP WATCH','2026-03-24','2026-03-25','2026-05-06 14:49:47'),(204,'123456','6','THERMOMETER','2026-03-26','2026-04-09','2026-05-06 14:49:47'),(205,'147852','1','Torque Wrench 11','2232-02-22','3223-02-23','2026-05-06 16:45:29'),(206,'147852','2','Torque Wrench 2','2026-02-03','2026-02-23','2026-05-06 16:45:29'),(207,'147852','5','STOP WATCH','2026-03-24','2026-03-25','2026-05-06 16:45:29'),(208,'147852','6','THERMOMETER','2026-03-26','2026-04-09','2026-05-06 16:45:29'),(209,'147852','1','Torque Wrench 11','2232-02-22','3223-02-23','2026-05-06 16:53:29'),(210,'147852','2','Torque Wrench 2','2026-02-03','2026-02-23','2026-05-06 16:53:29'),(211,'147852','5','STOP WATCH','2026-03-24','2026-03-25','2026-05-06 16:53:29'),(212,'147852','6','THERMOMETER','2026-03-26','2026-04-09','2026-05-06 16:53:29'),(213,'147852','1','Torque Wrench 11','2232-02-22','3223-02-23','2026-05-06 17:13:47'),(214,'147852','2','Torque Wrench 2','2026-02-03','2026-02-23','2026-05-06 17:13:47'),(215,'147852','5','STOP WATCH','2026-03-24','2026-03-25','2026-05-06 17:13:47'),(216,'147852','6','THERMOMETER','2026-03-26','2026-04-09','2026-05-06 17:13:47'),(217,'147852','1','Torque Wrench 11','2232-02-22','3223-02-23','2026-05-06 17:20:05'),(218,'147852','2','Torque Wrench 2','2026-02-03','2026-02-23','2026-05-06 17:20:05'),(219,'147852','5','STOP WATCH','2026-03-24','2026-03-25','2026-05-06 17:20:05'),(220,'147852','6','THERMOMETER','2026-03-26','2026-04-09','2026-05-06 17:20:05'),(221,'222222','1','Torque Wrench 11','2232-02-22','3223-02-23','2026-05-06 19:03:56'),(222,'222222','2','Torque Wrench 2','2026-02-03','2026-02-23','2026-05-06 19:03:56'),(223,'222222','5','STOP WATCH','2026-03-24','2026-03-25','2026-05-06 19:03:56'),(224,'222222','6','THERMOMETER','2026-03-26','2026-04-09','2026-05-06 19:03:56');
/*!40000 ALTER TABLE `instrument_test_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_actuator`
--

DROP TABLE IF EXISTS `master_actuator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_actuator` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SER_NO` varchar(255) DEFAULT NULL,
  `CC_COL1_NAME` varchar(50) DEFAULT NULL,
  `CC_COL1_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL2_NAME` varchar(50) DEFAULT NULL,
  `CC_COL2_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL3_NAME` varchar(50) DEFAULT NULL,
  `CC_COL3_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL4_NAME` varchar(50) DEFAULT NULL,
  `CC_COL4_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL5_NAME` varchar(50) DEFAULT NULL,
  `CC_COL5_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL6_NAME` varchar(50) DEFAULT NULL,
  `CC_COL6_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL7_NAME` varchar(50) DEFAULT NULL,
  `CC_COL7_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL8_NAME` varchar(50) DEFAULT NULL,
  `CC_COL8_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL9_NAME` varchar(50) DEFAULT NULL,
  `CC_COL9_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL10_NAME` varchar(50) DEFAULT NULL,
  `CC_COL10_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL11_NAME` varchar(50) DEFAULT NULL,
  `CC_COL11_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL12_NAME` varchar(50) DEFAULT NULL,
  `CC_COL12_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL13_NAME` varchar(50) DEFAULT NULL,
  `CC_COL13_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL14_NAME` varchar(50) DEFAULT NULL,
  `CC_COL14_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL15_NAME` varchar(50) DEFAULT NULL,
  `CC_COL15_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL16_NAME` varchar(50) DEFAULT NULL,
  `CC_COL16_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL17_NAME` varchar(50) DEFAULT NULL,
  `CC_COL17_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL18_NAME` varchar(50) DEFAULT NULL,
  `CC_COL18_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL19_NAME` varchar(50) DEFAULT NULL,
  `CC_COL19_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL20_NAME` varchar(50) DEFAULT NULL,
  `CC_COL20_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL21_NAME` varchar(50) DEFAULT NULL,
  `CC_COL21_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL22_NAME` varchar(50) DEFAULT NULL,
  `CC_COL22_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL23_NAME` varchar(50) DEFAULT NULL,
  `CC_COL23_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL24_NAME` varchar(50) DEFAULT NULL,
  `CC_COL24_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL25_NAME` varchar(50) DEFAULT NULL,
  `CC_COL25_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL26_NAME` varchar(50) DEFAULT NULL,
  `CC_COL26_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL27_NAME` varchar(50) DEFAULT NULL,
  `CC_COL27_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL28_NAME` varchar(50) DEFAULT NULL,
  `CC_COL28_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL29_NAME` varchar(50) DEFAULT NULL,
  `CC_COL29_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL30_NAME` varchar(50) DEFAULT NULL,
  `CC_COL30_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL31_NAME` varchar(50) DEFAULT NULL,
  `CC_COL31_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL32_NAME` varchar(50) DEFAULT NULL,
  `CC_COL32_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL33_NAME` varchar(50) DEFAULT NULL,
  `CC_COL33_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL34_NAME` varchar(50) DEFAULT NULL,
  `CC_COL34_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL35_NAME` varchar(50) DEFAULT NULL,
  `CC_COL35_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL36_NAME` varchar(50) DEFAULT NULL,
  `CC_COL36_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL37_NAME` varchar(50) DEFAULT NULL,
  `CC_COL37_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL38_NAME` varchar(50) DEFAULT NULL,
  `CC_COL38_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL39_NAME` varchar(50) DEFAULT NULL,
  `CC_COL39_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL40_NAME` varchar(50) DEFAULT NULL,
  `CC_COL40_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL41_NAME` varchar(50) DEFAULT NULL,
  `CC_COL41_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL42_NAME` varchar(50) DEFAULT NULL,
  `CC_COL42_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL43_NAME` varchar(50) DEFAULT NULL,
  `CC_COL43_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL44_NAME` varchar(50) DEFAULT NULL,
  `CC_COL44_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL45_NAME` varchar(50) DEFAULT NULL,
  `CC_COL45_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL46_NAME` varchar(50) DEFAULT NULL,
  `CC_COL46_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL47_NAME` varchar(50) DEFAULT NULL,
  `CC_COL47_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL48_NAME` varchar(50) DEFAULT NULL,
  `CC_COL48_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL49_NAME` varchar(50) DEFAULT NULL,
  `CC_COL49_VALUE` varchar(100) DEFAULT NULL,
  `CC_COL50_NAME` varchar(50) DEFAULT NULL,
  `CC_COL50_VALUE` varchar(100) DEFAULT NULL,
  `SHIFT` varchar(50) DEFAULT NULL,
  `CYCLE_COMPLETE` int DEFAULT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT NULL,
  `REMARKS` mediumtext,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_actuator`
--

LOCK TABLES `master_actuator` WRITE;
/*!40000 ALTER TABLE `master_actuator` DISABLE KEYS */;
INSERT INTO `master_actuator` VALUES (1,'49','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','5','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','55','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','5','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','55','Water Draining After Testing','5','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','55','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 06:36:47','55'),(2,'49','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','5','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','55','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','5','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','55','Water Draining After Testing','5','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','55','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 06:36:54','55'),(3,'99','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','66','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','6','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','66','Actuator Timing (s) Open→Close','6','Actuator Torque Setting (%) Close→Open','6','Actuator Torque Setting (%) Open→Close','66','Torque Test (Nm) BTO at LH','66','Torque Test (Nm) BTO at RH','6','Run Torque @ Atmospheric (Nm)','6','Tightness of Gear Unit Position Stopper','6','Measured Power (V)','6','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','6','Water Draining After Testing','6','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','6','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 06:42:16','6'),(4,'99','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','66','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','6','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','66','Actuator Timing (s) Open→Close','6','Actuator Torque Setting (%) Close→Open','6','Actuator Torque Setting (%) Open→Close','66','Torque Test (Nm) BTO at LH','66','Torque Test (Nm) BTO at RH','6','Run Torque @ Atmospheric (Nm)','6','Tightness of Gear Unit Position Stopper','6','Measured Power (V)','6','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','6','Water Draining After Testing','6','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','6','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 06:42:20','6'),(5,'4543543','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','ghf','Body to Ball: Measured Resistance (Ω)','gfd','Body to Stem/Shaft: Measured Power (V)','gdfg','Body to Stem/Shaft: Measured Resistance (Ω)','gfdg','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','gdfg','Abnormal Sound During Operation','gdf','Water Draining After Testing','fdgfd','Result of Drying','gdfgdf','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','gfdg','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 07:42:48','gfdg'),(6,'7686789','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','ghf','Body to Ball: Measured Resistance (Ω)','gfd','Body to Stem/Shaft: Measured Power (V)','gdfg','Body to Stem/Shaft: Measured Resistance (Ω)','gfdg','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','gdfg','Abnormal Sound During Operation','gdf','Water Draining After Testing','fdgfd','Result of Drying','gdfgdf','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 07:43:09',''),(7,'97869789','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','ghf','Body to Ball: Measured Resistance (Ω)','gfd','Body to Stem/Shaft: Measured Power (V)','gdfg','Body to Stem/Shaft: Measured Resistance (Ω)','gfdg','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','gdfg','Abnormal Sound During Operation','gdf','Water Draining After Testing','fdgfd','Result of Drying','gdfgdf','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','rwer','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 07:43:19','rwer'),(8,'09776','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','reter','Body to Ball: Measured Resistance (Ω)','gfd','Body to Stem/Shaft: Measured Power (V)','gdfg','Body to Stem/Shaft: Measured Resistance (Ω)','gfdg','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','gdfg','Abnormal Sound During Operation','gdf','Water Draining After Testing','fdgfd','Result of Drying','gdfgdf','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','trt','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 07:43:42','trt'),(9,'7898','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','2','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','2','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','22','Actuator Timing (s) Open→Close','2','Actuator Torque Setting (%) Close→Open','4543','Actuator Torque Setting (%) Open→Close','22','Torque Test (Nm) BTO at LH','2','Torque Test (Nm) BTO at RH','2','Run Torque @ Atmospheric (Nm)','2','Tightness of Gear Unit Position Stopper','22','Measured Power (V)','2','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','2','Water Draining After Testing','2','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','2','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-03 07:54:52','2'),(10,'ppo01','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','11','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 04:46:16','1'),(11,'1232','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','11','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 05:21:41','1'),(12,'564','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 05:21:50','1'),(13,'198','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 05:21:58','1'),(14,'PK-001','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','11','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 05:55:14','1'),(15,'PK-002','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 05:55:23','1'),(16,'8','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','11','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','11','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','11','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','333','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 22:41:03','333'),(17,'999','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','99','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','99','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','9','Actuator Timing (s) Open→Close','99','Actuator Torque Setting (%) Close→Open','9','Actuator Torque Setting (%) Open→Close','99','Torque Test (Nm) BTO at LH','99','Torque Test (Nm) BTO at RH','9','Run Torque @ Atmospheric (Nm)','9','Tightness of Gear Unit Position Stopper','99','Measured Power (V)','9','Water Drying Technique (QM-7B)','Vacuum','Abnormal Sound During Operation','9','Water Draining After Testing','9','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','99','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 22:41:17','99'),(18,'522','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','66','Body to Ball: Measured Resistance (Ω)','6','Body to Stem/Shaft: Measured Power (V)','66','Body to Stem/Shaft: Measured Resistance (Ω)','6','Actuator Timing (s) Close→Open','66','Actuator Timing (s) Open→Close','6','Actuator Torque Setting (%) Close→Open','66','Actuator Torque Setting (%) Open→Close','66','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','6','Tightness of Gear Unit Position Stopper','6','Measured Power (V)','','Water Drying Technique (QM-7B)','66','Abnormal Sound During Operation','6','Water Draining After Testing','66','Result of Drying','6','Actuator Sizing Pressure (psig)','6','Torque @ Rated Pressure (Nm) BTO (DBB)','6','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','6','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','6','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','6','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','6','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 22:55:26','6'),(19,'6333','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','88','Body to Ball: Measured Resistance (Ω)','88','Body to Stem/Shaft: Measured Power (V)','8','Body to Stem/Shaft: Measured Resistance (Ω)','88','Actuator Timing (s) Close→Open','8','Actuator Timing (s) Open→Close','8','Actuator Torque Setting (%) Close→Open','88','Actuator Torque Setting (%) Open→Close','8','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','88','Tightness of Gear Unit Position Stopper','8','Measured Power (V)','','Water Drying Technique (QM-7B)','88','Abnormal Sound During Operation','8','Water Draining After Testing','8','Result of Drying','88','Actuator Sizing Pressure (psig)','88','Torque @ Rated Pressure (Nm) BTO (DBB)','8','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','8','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','8','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','8','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','8','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-04 22:55:43','8'),(20,'MMO','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 00:18:09','1'),(21,'879','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 01:32:47','1'),(22,'978','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 01:32:57','1'),(23,'567','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 01:33:04','1'),(24,'765','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 01:33:13','1'),(25,'POO1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 02:35:12','1'),(26,'POO2','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 02:35:22','1'),(27,'DBC-001','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','11','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 02:47:29','1'),(28,'MIP-005','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 02:55:13','1'),(29,'LOL-01','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 03:04:01','1'),(30,'VICKY','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 03:32:40','1'),(31,'KP-001','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 03:39:35','1'),(32,'KP-003','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 04:12:37','1'),(33,'90','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 05:00:58','1'),(34,'1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 05:55:41','1'),(35,'2','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 05:55:50','1'),(36,'3','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 05:56:00','1'),(37,'4','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 05:56:09','1'),(38,'1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 06:02:44','1'),(39,'2','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 06:02:54','1'),(40,'3','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 06:03:03','1'),(41,'4','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 06:03:12','1'),(42,'2024','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 22:36:29','1'),(43,'101','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 22:43:36','1'),(44,'101','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 22:44:52','1'),(45,'102','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 22:53:36','1'),(46,'103','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 22:56:24','1'),(47,'104','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-06 22:58:25','1'),(48,'102','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 01:49:04','1'),(49,'106','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 01:56:43','1'),(50,'109','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 02:35:54','1'),(51,'1996','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 02:46:23','1'),(52,'9898','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 03:29:36','1'),(53,'9898','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 03:39:07','1'),(54,'9898','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 03:56:55','1'),(55,'80','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:10:43','1'),(56,'81','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:12:48','1'),(57,'82','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:15:54','1'),(58,'85','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:19:24','1'),(59,'89','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:24:18','1'),(60,'90','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:32:57','1'),(61,'92','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:49:04','1'),(62,'100','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:51:18','1'),(63,'101','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:54:31','1'),(64,'102','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 04:56:18','1'),(65,'105','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:00:08','1'),(66,'106','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:06:57','1'),(67,'200','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:11:18','1'),(68,'201','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:12:56','1'),(69,'202','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:15:09','1'),(70,'205','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:17:07','1'),(71,'300','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:22:52','1'),(72,'301','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:28:13','1'),(73,'PANDI-01','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-07 05:59:54','1'),(74,'NOTE-001','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 00:28:47','1'),(75,'NOTE-002','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','11','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 00:31:38','1'),(76,'NOTE-003','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 00:35:09','1'),(77,'NOTE-004','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','11','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 00:35:28','1'),(78,'8008','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 01:17:01','1'),(79,'8002','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 01:49:51','1'),(80,'8002','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 01:56:31','1'),(81,'101','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:05:35','1'),(82,'102','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:05:48','1'),(83,'103','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:11:49','1'),(84,'104','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:12:00','1'),(85,'105','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Fail','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','Fail','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:17:51','1'),(86,'106','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:18:13','1'),(87,'107','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:20:59','1'),(88,'108','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:21:09','1'),(89,'109','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:25:43','1'),(90,'110','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:25:55','1'),(91,'1986','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:29:50','1'),(92,'1984','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:30:01','1'),(93,'2028','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:30:14','1'),(94,'2029','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:30:25','1'),(95,'DHARANI','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:36:39','1'),(96,'DHARANI1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:36:50','1'),(97,'ILAN','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:38:56','1'),(98,'ILANMD','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','','Water Drying Technique (QM-7B)','1','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','1','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','1','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','1','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:39:14','1'),(99,'KISHORe','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:50:04','1'),(100,'kishore1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Vacuum','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 03:50:19','1'),(101,'WIRE','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','vicky','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','vicky','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','vicky','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','vicky','Water Draining After Testing','vicky','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','vicky','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 04:15:44','vicky'),(102,'WIRE','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','vicky','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','vicky','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','dharani','Actuator Timing (s) Open→Close','dharani','Actuator Torque Setting (%) Close→Open','dharani','Actuator Torque Setting (%) Open→Close','dharani','Torque Test (Nm) BTO at LH','dharani','Torque Test (Nm) BTO at RH','dharani','Run Torque @ Atmospheric (Nm)','dharani','Tightness of Gear Unit Position Stopper','dharani','Measured Power (V)','vicky','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','vicky','Water Draining After Testing','vicky','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','vicky','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 04:17:19','vicky'),(103,'BOTTLE','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 04:20:36','1'),(104,'MOBILE','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 04:30:28','1'),(105,'7MT','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-08 06:00:38','1'),(106,'1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 01:52:41','1'),(107,'2','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 01:52:50','1'),(108,'3','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 01:53:02','1'),(109,'4','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 01:53:13','1'),(110,'1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 02:47:23','1'),(111,'None','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','6','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','rw','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','rew','Torque Test (Nm) BTO at RH','rew','Run Torque @ Atmospheric (Nm)','rewr','Tightness of Gear Unit Position Stopper','rew','Measured Power (V)','rew','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','rew','Water Draining After Testing','rew','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','rew','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 04:02:49','rew'),(112,'2001','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','65','Body to Stem/Shaft: Measured Resistance (Ω)','5','Actuator Timing (s) Close→Open','5','Actuator Timing (s) Open→Close','55','Actuator Torque Setting (%) Close→Open','5','Actuator Torque Setting (%) Open→Close','5','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','5','Tightness of Gear Unit Position Stopper','5','Measured Power (V)','','Water Drying Technique (QM-7B)','5','Abnormal Sound During Operation','5','Water Draining After Testing','55','Result of Drying','5','Actuator Sizing Pressure (psig)','5','Torque @ Rated Pressure (Nm) BTO (DBB)','5','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','5','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','5','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','5','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','5','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 05:52:47','5'),(113,'2002','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','453','Body to Stem/Shaft: Measured Power (V)','65','Body to Stem/Shaft: Measured Resistance (Ω)','5','Actuator Timing (s) Close→Open','5','Actuator Timing (s) Open→Close','55','Actuator Torque Setting (%) Close→Open','5','Actuator Torque Setting (%) Open→Close','5','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','5','Tightness of Gear Unit Position Stopper','5','Measured Power (V)','','Water Drying Technique (QM-7B)','5','Abnormal Sound During Operation','5','Water Draining After Testing','55','Result of Drying','5','Actuator Sizing Pressure (psig)','5','Torque @ Rated Pressure (Nm) BTO (DBB)','5','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','5','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','5','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','5','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','43534','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 05:53:19','43534'),(114,'2003','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','wrwe','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','erer','Body to Stem/Shaft: Measured Resistance (Ω)','rere','Actuator Timing (s) Close→Open','ere','Actuator Timing (s) Open→Close','rer','Actuator Torque Setting (%) Close→Open','ere','Actuator Torque Setting (%) Open→Close','er','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','ere','Tightness of Gear Unit Position Stopper','er','Measured Power (V)','','Water Drying Technique (QM-7B)','re','Abnormal Sound During Operation','77','Water Draining After Testing','66','Result of Drying','5','Actuator Sizing Pressure (psig)','ere','Torque @ Rated Pressure (Nm) BTO (DBB)','5','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','5','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','5','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','5','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','err','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 05:54:06','err'),(115,'2003','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','wrwe','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','erer','Body to Stem/Shaft: Measured Resistance (Ω)','rere','Actuator Timing (s) Close→Open','ere','Actuator Timing (s) Open→Close','rer','Actuator Torque Setting (%) Close→Open','ere','Actuator Torque Setting (%) Open→Close','er','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','ere','Tightness of Gear Unit Position Stopper','er','Measured Power (V)','','Water Drying Technique (QM-7B)','re','Abnormal Sound During Operation','77','Water Draining After Testing','66','Result of Drying','5','Actuator Sizing Pressure (psig)','ere','Torque @ Rated Pressure (Nm) BTO (DBB)','5','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','5','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','5','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','5','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','err','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 05:54:32','err'),(116,'2003','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','wrwe','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','erer','Body to Stem/Shaft: Measured Resistance (Ω)','rere','Actuator Timing (s) Close→Open','ere','Actuator Timing (s) Open→Close','rer','Actuator Torque Setting (%) Close→Open','ere','Actuator Torque Setting (%) Open→Close','er','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','ere','Tightness of Gear Unit Position Stopper','er','Measured Power (V)','','Water Drying Technique (QM-7B)','re','Abnormal Sound During Operation','77','Water Draining After Testing','66','Result of Drying','5','Actuator Sizing Pressure (psig)','ere','Torque @ Rated Pressure (Nm) BTO (DBB)','5','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','5','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Pass','Torque @ Rated Pressure (Nm) BTO Connector (R)','5','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','Pass','Torque @ Rated Pressure (Nm) BTC','5','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','err','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 05:54:55','err'),(117,'101','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1111','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','5','Torque Test (Nm) BTO at RH','4','Run Torque @ Atmospheric (Nm)','5','Tightness of Gear Unit Position Stopper','4','Measured Power (V)','4','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','4','Water Draining After Testing','4','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 06:39:36','1'),(118,'102','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1111','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','5','Torque Test (Nm) BTO at RH','4','Run Torque @ Atmospheric (Nm)','5','Tightness of Gear Unit Position Stopper','4','Measured Power (V)','4','Water Drying Technique (QM-7B)','Comp. Air','Abnormal Sound During Operation','4','Water Draining After Testing','4','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 06:39:55',''),(119,'103','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','','Actuator Timing (s) Open→Close','','Actuator Torque Setting (%) Close→Open','','Actuator Torque Setting (%) Open→Close','','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','4','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','4','Water Draining After Testing','4','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','15','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 06:40:08','15'),(120,'104','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1111','Actuator Torque Setting (%) Open→Close','11','Torque Test (Nm) BTO at LH','5','Torque Test (Nm) BTO at RH','4','Run Torque @ Atmospheric (Nm)','5','Tightness of Gear Unit Position Stopper','4','Measured Power (V)','4','Water Drying Technique (QM-7B)','Vacuum','Abnormal Sound During Operation','4','Water Draining After Testing','4','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','5','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 06:40:29','5'),(121,'123','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','1','Torque Test (Nm) BTO at RH','1','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','1','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 07:02:41','1'),(122,'101','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','2','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','22','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','2','Actuator Timing (s) Open→Close','2','Actuator Torque Setting (%) Close→Open','222','Actuator Torque Setting (%) Open→Close','2','Torque Test (Nm) BTO at LH','2','Torque Test (Nm) BTO at RH','2','Run Torque @ Atmospheric (Nm)','22','Tightness of Gear Unit Position Stopper','2','Measured Power (V)','2','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','2','Water Draining After Testing','2','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','2','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 07:04:26','2'),(123,'123','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','2','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','2','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','2','Actuator Timing (s) Open→Close','2','Actuator Torque Setting (%) Close→Open','222','Actuator Torque Setting (%) Open→Close','2','Torque Test (Nm) BTO at LH','2','Torque Test (Nm) BTO at RH','2','Run Torque @ Atmospheric (Nm)','2','Tightness of Gear Unit Position Stopper','2','Measured Power (V)','22','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','2','Water Draining After Testing','2','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','2','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-10 07:06:23','2'),(124,'1','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-11 04:56:00','1'),(125,'2','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','1','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-11 04:56:10','1'),(126,'12r','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','2','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','2','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','2','Actuator Timing (s) Open→Close','2','Actuator Torque Setting (%) Close→Open','2','Actuator Torque Setting (%) Open→Close','2','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','2','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','2','Water Draining After Testing','2','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','2','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-15 02:50:24','2'),(127,'12s','Valve Type Name','Floating Ball Valve','Body to Ball: Measured Power (V)','2','Body to Ball: Measured Resistance (Ω)','','Body to Stem/Shaft: Measured Power (V)','2','Body to Stem/Shaft: Measured Resistance (Ω)','','Actuator Timing (s) Close→Open','2','Actuator Timing (s) Open→Close','2','Actuator Torque Setting (%) Close→Open','2','Actuator Torque Setting (%) Open→Close','2','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','','Tightness of Gear Unit Position Stopper','','Measured Power (V)','2','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','2','Water Draining After Testing','2','Result of Drying','','Actuator Sizing Pressure (psig)','','Torque @ Rated Pressure (Nm) BTO (DBB)','','Torque @ Rated Pressure (Nm) BTO (DBB) Result','','Torque @ Rated Pressure (Nm) BTO Connector (L)','','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','','Torque @ Rated Pressure (Nm) BTO Connector (R)','','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','','Torque @ Rated Pressure (Nm) BTC Result','','Remarks','2','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-15 02:50:47','2'),(128,'12132','Valve Type Name','TMBV','Body to Ball: Measured Power (V)','1','Body to Ball: Measured Resistance (Ω)','1','Body to Stem/Shaft: Measured Power (V)','1','Body to Stem/Shaft: Measured Resistance (Ω)','1','Actuator Timing (s) Close→Open','1','Actuator Timing (s) Open→Close','1','Actuator Torque Setting (%) Close→Open','1','Actuator Torque Setting (%) Open→Close','1','Torque Test (Nm) BTO at LH','','Torque Test (Nm) BTO at RH','','Run Torque @ Atmospheric (Nm)','1','Tightness of Gear Unit Position Stopper','11','Measured Power (V)','','Water Drying Technique (QM-7B)','','Abnormal Sound During Operation','1','Water Draining After Testing','1','Result of Drying','1','Actuator Sizing Pressure (psig)','1','Torque @ Rated Pressure (Nm) BTO (DBB)','1','Torque @ Rated Pressure (Nm) BTO (DBB) Result','Pass','Torque @ Rated Pressure (Nm) BTO Connector (L)','2','Torque @ Rated Pressure (Nm) BTO Connector (L) Res','Fail','Torque @ Rated Pressure (Nm) BTO Connector (R)','2','Torque @ Rated Pressure (Nm) BTO Connector (R) Res','','Torque @ Rated Pressure (Nm) BTC','111111','Torque @ Rated Pressure (Nm) BTC Result','Pass','Remarks','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Shift_1',1,'2025-11-15 05:19:29','1');
/*!40000 ALTER TABLE `master_actuator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_degree_data`
--

DROP TABLE IF EXISTS `master_degree_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_degree_data` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SIZE_ID` int NOT NULL,
  `TYPE_ID` int DEFAULT NULL,
  `OPEN_DEGREE` int NOT NULL,
  `CLOSE_DEGREE` int NOT NULL,
  `LOADING_AND_UNLOADING_DEGREE` int NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_degree_data`
--

LOCK TABLES `master_degree_data` WRITE;
/*!40000 ALTER TABLE `master_degree_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `master_degree_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_duration_data`
--

DROP TABLE IF EXISTS `master_duration_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_duration_data` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SIZE_ID` int NOT NULL,
  `STANDARD` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `COL1_DUR` int DEFAULT NULL,
  `COL2_DUR` int DEFAULT NULL,
  `COL3_DUR` int DEFAULT NULL,
  `COL4_DUR` int DEFAULT NULL,
  `COL5_DUR` int DEFAULT NULL,
  `COL6_DUR` int DEFAULT NULL,
  `COL7_DUR` int DEFAULT NULL,
  `COL8_DUR` int DEFAULT NULL,
  `COL9_DUR` int DEFAULT NULL,
  `COL10_DUR` int DEFAULT NULL,
  `COL11_DUR` int DEFAULT NULL,
  `COL12_DUR` int DEFAULT NULL,
  `COL13_DUR` int DEFAULT NULL,
  `COL14_DUR` int DEFAULT NULL,
  `COL15_DUR` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `size_standard_unique` (`VALVE_SIZE_ID`,`STANDARD`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_duration_data`
--

LOCK TABLES `master_duration_data` WRITE;
/*!40000 ALTER TABLE `master_duration_data` DISABLE KEYS */;
INSERT INTO `master_duration_data` VALUES (44,120,'1',9,89,80,78,64,9,NULL,8,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `master_duration_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_pressure_data`
--

DROP TABLE IF EXISTS `master_pressure_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_pressure_data` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `SHELL_MATERIAL_ID` int NOT NULL,
  `VALVE_CLASS_ID` int DEFAULT NULL,
  `COL1_PRE` float DEFAULT NULL,
  `COL2_PRE` float DEFAULT NULL,
  `COL3_PRE` float DEFAULT NULL,
  `COL4_PRE` float DEFAULT NULL,
  `COL5_PRE` float DEFAULT NULL,
  `COL6_PRE` float DEFAULT NULL,
  `COL7_PRE` float DEFAULT NULL,
  `COL8_PRE` float DEFAULT NULL,
  `COL9_PRE` float DEFAULT NULL,
  `COL10_PRE` float DEFAULT NULL,
  `COL11_PRE` float DEFAULT NULL,
  `COL12_PRE` float DEFAULT NULL,
  `COL13_PRE` float DEFAULT NULL,
  `COL14_PRE` float DEFAULT NULL,
  `COL15_PRE` float DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_pressure_data`
--

LOCK TABLES `master_pressure_data` WRITE;
/*!40000 ALTER TABLE `master_pressure_data` DISABLE KEYS */;
INSERT INTO `master_pressure_data` VALUES (15,1,1,100,200,300,400,250,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(16,2,2,300,300,300,300,300,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(17,3,2,300,300,300,300,300,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,3,1,150,150,150,150,150,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,3,4,900,900,900,900,900,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,1,2,100,200,300,400,250,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `master_pressure_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_temp_data`
--

DROP TABLE IF EXISTS `master_temp_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_temp_data` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SER_NO` varchar(100) DEFAULT NULL,
  `PRESSURE_UNIT` varchar(50) DEFAULT NULL,
  `STANDARD_NAME` varchar(100) DEFAULT NULL,
  `SIZE_NAME` varchar(100) DEFAULT NULL,
  `CLASS_NAME` varchar(100) DEFAULT NULL,
  `TYPE_NAME` varchar(100) DEFAULT NULL,
  `SHELL_MATERIAL_NAME` varchar(100) DEFAULT NULL,
  `SYNC_NON_SYNC_STATUS` varchar(25) DEFAULT NULL,
  `STATION_STATUS` varchar(20) DEFAULT NULL,
  `CYCLE_COMPLETE` varchar(20) DEFAULT NULL,
  `COL1_NAME` varchar(50) DEFAULT NULL,
  `COL1_VALUE` varchar(100) DEFAULT NULL,
  `COL2_NAME` varchar(50) DEFAULT NULL,
  `COL2_VALUE` varchar(100) DEFAULT NULL,
  `COL3_NAME` varchar(50) DEFAULT NULL,
  `COL3_VALUE` varchar(100) DEFAULT NULL,
  `COL4_NAME` varchar(50) DEFAULT NULL,
  `COL4_VALUE` varchar(100) DEFAULT NULL,
  `COL5_NAME` varchar(50) DEFAULT NULL,
  `COL5_VALUE` varchar(100) DEFAULT NULL,
  `COL6_NAME` varchar(50) DEFAULT NULL,
  `COL6_VALUE` varchar(100) DEFAULT NULL,
  `COL7_NAME` varchar(50) DEFAULT NULL,
  `COL7_VALUE` varchar(100) DEFAULT NULL,
  `COL8_NAME` varchar(50) DEFAULT NULL,
  `COL8_VALUE` varchar(100) DEFAULT NULL,
  `COL9_NAME` varchar(50) DEFAULT NULL,
  `COL9_VALUE` varchar(100) DEFAULT NULL,
  `COL10_NAME` varchar(50) DEFAULT NULL,
  `COL10_VALUE` varchar(100) DEFAULT NULL,
  `COL11_NAME` varchar(50) DEFAULT NULL,
  `COL11_VALUE` varchar(100) DEFAULT NULL,
  `COL12_NAME` varchar(50) DEFAULT NULL,
  `COL12_VALUE` varchar(100) DEFAULT NULL,
  `COL13_NAME` varchar(50) DEFAULT NULL,
  `COL13_VALUE` varchar(100) DEFAULT NULL,
  `COL14_NAME` varchar(50) DEFAULT NULL,
  `COL14_VALUE` varchar(100) DEFAULT NULL,
  `COL15_NAME` varchar(50) DEFAULT NULL,
  `COL15_VALUE` varchar(100) DEFAULT NULL,
  `COL16_NAME` varchar(50) DEFAULT NULL,
  `COL16_VALUE` varchar(100) DEFAULT NULL,
  `COL17_NAME` varchar(50) DEFAULT NULL,
  `COL17_VALUE` varchar(100) DEFAULT NULL,
  `COL18_NAME` varchar(50) DEFAULT NULL,
  `COL18_VALUE` varchar(100) DEFAULT NULL,
  `COL19_NAME` varchar(50) DEFAULT NULL,
  `COL19_VALUE` varchar(100) DEFAULT NULL,
  `COL20_NAME` varchar(50) DEFAULT NULL,
  `COL20_VALUE` varchar(100) DEFAULT NULL,
  `COL21_NAME` varchar(50) DEFAULT NULL,
  `COL21_VALUE` varchar(100) DEFAULT NULL,
  `COL22_NAME` varchar(50) DEFAULT NULL,
  `COL22_VALUE` varchar(100) DEFAULT NULL,
  `COL23_NAME` varchar(50) DEFAULT NULL,
  `COL23_VALUE` varchar(100) DEFAULT NULL,
  `COL24_NAME` varchar(50) DEFAULT NULL,
  `COL24_VALUE` varchar(100) DEFAULT NULL,
  `COL25_NAME` varchar(50) DEFAULT NULL,
  `COL25_VALUE` varchar(100) DEFAULT NULL,
  `COL26_NAME` varchar(50) DEFAULT NULL,
  `COL26_VALUE` varchar(100) DEFAULT NULL,
  `COL27_NAME` varchar(50) DEFAULT NULL,
  `COL27_VALUE` varchar(100) DEFAULT NULL,
  `COL28_NAME` varchar(50) DEFAULT NULL,
  `COL28_VALUE` varchar(100) DEFAULT NULL,
  `COL29_NAME` varchar(50) DEFAULT NULL,
  `COL29_VALUE` varchar(100) DEFAULT NULL,
  `COL30_NAME` varchar(50) DEFAULT NULL,
  `COL30_VALUE` varchar(100) DEFAULT NULL,
  `COL31_NAME` varchar(50) DEFAULT NULL,
  `COL31_VALUE` varchar(100) DEFAULT NULL,
  `COL32_NAME` varchar(50) DEFAULT NULL,
  `COL32_VALUE` varchar(100) DEFAULT NULL,
  `COL33_NAME` varchar(50) DEFAULT NULL,
  `COL33_VALUE` varchar(100) DEFAULT NULL,
  `COL34_NAME` varchar(50) DEFAULT NULL,
  `COL34_VALUE` varchar(100) DEFAULT NULL,
  `COL35_NAME` varchar(50) DEFAULT NULL,
  `COL35_VALUE` varchar(100) DEFAULT NULL,
  `COL36_NAME` varchar(50) DEFAULT NULL,
  `COL36_VALUE` varchar(100) DEFAULT NULL,
  `COL37_NAME` varchar(50) DEFAULT NULL,
  `COL37_VALUE` varchar(100) DEFAULT NULL,
  `COL38_NAME` varchar(50) DEFAULT NULL,
  `COL38_VALUE` varchar(100) DEFAULT NULL,
  `COL39_NAME` varchar(50) DEFAULT NULL,
  `COL39_VALUE` varchar(100) DEFAULT NULL,
  `COL40_NAME` varchar(50) DEFAULT NULL,
  `COL40_VALUE` varchar(100) DEFAULT NULL,
  `COL41_NAME` varchar(50) DEFAULT NULL,
  `COL41_VALUE` varchar(100) DEFAULT NULL,
  `COL42_NAME` varchar(50) DEFAULT NULL,
  `COL42_VALUE` varchar(100) DEFAULT NULL,
  `COL43_NAME` varchar(50) DEFAULT NULL,
  `COL43_VALUE` varchar(100) DEFAULT NULL,
  `COL44_NAME` varchar(50) DEFAULT NULL,
  `COL44_VALUE` varchar(100) DEFAULT NULL,
  `COL45_NAME` varchar(50) DEFAULT NULL,
  `COL45_VALUE` varchar(100) DEFAULT NULL,
  `COL46_NAME` varchar(50) DEFAULT NULL,
  `COL46_VALUE` varchar(100) DEFAULT NULL,
  `COL47_NAME` varchar(50) DEFAULT NULL,
  `COL47_VALUE` varchar(100) DEFAULT NULL,
  `COL48_NAME` varchar(50) DEFAULT NULL,
  `COL48_VALUE` varchar(100) DEFAULT NULL,
  `COL49_NAME` varchar(50) DEFAULT NULL,
  `COL49_VALUE` varchar(100) DEFAULT NULL,
  `COL50_NAME` varchar(50) DEFAULT NULL,
  `COL50_VALUE` varchar(100) DEFAULT NULL,
  `DURATION_TYPE` varchar(50) DEFAULT NULL,
  `COL51_NAME` varchar(50) DEFAULT NULL,
  `COL51_VALUE` varchar(100) DEFAULT NULL,
  `COL52_NAME` varchar(50) DEFAULT NULL,
  `COL52_VALUE` varchar(100) DEFAULT NULL,
  `COL53_NAME` varchar(50) DEFAULT NULL,
  `COL53_VALUE` varchar(100) DEFAULT NULL,
  `COL54_NAME` varchar(50) DEFAULT NULL,
  `COL54_VALUE` varchar(100) DEFAULT NULL,
  `COL55_NAME` varchar(50) DEFAULT NULL,
  `COL55_VALUE` varchar(100) DEFAULT NULL,
  `COL56_NAME` varchar(50) DEFAULT NULL,
  `COL56_VALUE` varchar(100) DEFAULT NULL,
  `COL57_NAME` varchar(50) DEFAULT NULL,
  `COL57_VALUE` varchar(100) DEFAULT NULL,
  `COL58_NAME` varchar(50) DEFAULT NULL,
  `COL58_VALUE` varchar(100) DEFAULT NULL,
  `COL59_NAME` varchar(50) DEFAULT NULL,
  `COL59_VALUE` varchar(100) DEFAULT NULL,
  `COL60_NAME` varchar(50) DEFAULT NULL,
  `COL60_VALUE` varchar(100) DEFAULT NULL,
  `COL61_NAME` varchar(50) DEFAULT NULL,
  `COL61_VALUE` varchar(100) DEFAULT NULL,
  `COL62_NAME` varchar(50) DEFAULT NULL,
  `COL62_VALUE` varchar(100) DEFAULT NULL,
  `COL63_NAME` varchar(50) DEFAULT NULL,
  `COL63_VALUE` varchar(100) DEFAULT NULL,
  `COL64_NAME` varchar(50) DEFAULT NULL,
  `COL64_VALUE` varchar(100) DEFAULT NULL,
  `COL65_NAME` varchar(50) DEFAULT NULL,
  `COL65_VALUE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_temp_data`
--

LOCK TABLES `master_temp_data` WRITE;
/*!40000 ALTER TABLE `master_temp_data` DISABLE KEYS */;
INSERT INTO `master_temp_data` VALUES (1,'222222','PSI','STND1','One Twenty\"','#150','Globe','Shell material','Sync','Disabled','Yes','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',NULL,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''),(2,'104','PSI','STND1','2\"','#150','Gate','Shell material','Sync','Disabled','No','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','IOGP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `master_temp_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newapp_employee`
--

DROP TABLE IF EXISTS `newapp_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newapp_employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_type` varchar(20) NOT NULL,
  `code` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `superuser` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newapp_employee`
--

LOCK TABLES `newapp_employee` WRITE;
/*!40000 ALTER TABLE `newapp_employee` DISABLE KEYS */;
INSERT INTO `newapp_employee` VALUES (1,'admin','1','user1','pbkdf2_sha256$1000000$FpljQPIyJLfoWamhFa78Du$jZcgdVz59/RSYTG/wRSJyWwrP97rCSN3ltHx5J6nDjA=','user1@gmail.com','7402080605',NULL,1),(55,'Approver','2','USER2','pbkdf2_sha256$1000000$FpljQPIyJLfoWamhFa78Du$jZcgdVz59/RSYTG/wRSJyWwrP97rCSN3ltHx5J6nDjA=','','',NULL,0),(56,'Tester','4','USER3','vetri','pandikumar652001@gmail.com','',NULL,0),(57,'superadmin','0','admin','pbkdf2_sha256$1000000$7xJ04GKHn83kt4UkW8m5qI$iF4YmjlkGD2wQq+1t5zL8+3Q4ODKmxnNW7trTVy3Q7c=','info@gmail.com','63',NULL,2),(59,'Tester','5','afaf','pbkdf2_sha256$1000000$P0Kt3cNvmZg5zhbCkv3vaN$2JzT3fW0H4UN7wmqUcKgwjn+eZpS4vXKwMFG5dtgii0=','fsef@gmail.com','7409638521','Screenshot (1).png',0);
/*!40000 ALTER TABLE `newapp_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newapp_menuitem`
--

DROP TABLE IF EXISTS `newapp_menuitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newapp_menuitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `section` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newapp_menuitem`
--

LOCK TABLES `newapp_menuitem` WRITE;
/*!40000 ALTER TABLE `newapp_menuitem` DISABLE KEYS */;
INSERT INTO `newapp_menuitem` VALUES (1,'Standard','master'),(2,'Valve Size','master'),(3,'Valve Class','master'),(4,'Valve Type','master'),(5,'Shell Material','master'),(6,'Employee','master'),(7,'Alarm','master'),(8,'Gauge Details','master'),(13,'Configuration','settings'),(14,'Graph','report'),(15,'VTR','report'),(18,'Instrument Type','master'),(19,'Pdf','report'),(20,'Employee','users'),(21,'Access Control','users'),(22,'Accounting User Accounting','users'),(23,'ABRS Serial Fetch','ABRS'),(24,'Test Result','ABRS'),(25,'Category','master');
/*!40000 ALTER TABLE `newapp_menuitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newapp_usermenupermission`
--

DROP TABLE IF EXISTS `newapp_usermenupermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newapp_usermenupermission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_item_id` bigint NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `newapp_usermenupermi_menu_item_id_0d1a752b_fk_newapp_me` (`menu_item_id`),
  KEY `newapp_usermenupermi_employee_id_c84f1888_fk_newapp_em` (`employee_id`),
  CONSTRAINT `newapp_usermenupermi_employee_id_c84f1888_fk_newapp_em` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`) ON DELETE CASCADE,
  CONSTRAINT `newapp_usermenupermi_menu_item_id_0d1a752b_fk_newapp_me` FOREIGN KEY (`menu_item_id`) REFERENCES `newapp_menuitem` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newapp_usermenupermission`
--

LOCK TABLES `newapp_usermenupermission` WRITE;
/*!40000 ALTER TABLE `newapp_usermenupermission` DISABLE KEYS */;
INSERT INTO `newapp_usermenupermission` VALUES (3,1,55),(4,2,55),(5,14,55),(6,1,56);
/*!40000 ALTER TABLE `newapp_usermenupermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pressure_analysis`
--

DROP TABLE IF EXISTS `pressure_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pressure_analysis` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SER_NO` varchar(100) DEFAULT NULL,
  `TEST_ID` int DEFAULT NULL,
  `TEST_NAME` varchar(255) DEFAULT NULL,
  `COUNT_ID` int DEFAULT NULL,
  `SET_PRESSURE` decimal(18,3) DEFAULT NULL,
  `ACTUAL_PRESSURE` decimal(18,3) DEFAULT NULL,
  `PRESSURE_UNIT` varchar(50) DEFAULT NULL,
  `SET_TIME` int DEFAULT NULL,
  `ACTUAL_TIME` int DEFAULT NULL,
  `SET_TIME_UNIT` varchar(50) DEFAULT NULL,
  `CLAMPING_PRESSURE` decimal(18,3) DEFAULT NULL,
  `ACTUAL_OPEN_TORQUE` float DEFAULT NULL,
  `ACTUAL_CLOSE_TORQUE` float DEFAULT NULL,
  `START_PRESSURE` decimal(18,3) DEFAULT NULL,
  `RESULT_PRESSURE` decimal(18,3) DEFAULT NULL,
  `LEAK_PRESSURE` decimal(18,3) DEFAULT NULL,
  `STANDARD_NAME` varchar(255) DEFAULT NULL,
  `VALVESIZE_NAME` varchar(100) DEFAULT NULL,
  `VALVETYPE_NAME` varchar(100) DEFAULT NULL,
  `VALVECLASS_NAME` varchar(100) DEFAULT NULL,
  `SHELLMATERIAL_NAME` varchar(100) DEFAULT NULL,
  `START` datetime DEFAULT NULL,
  `END` datetime DEFAULT NULL,
  `CYCLE_START` datetime DEFAULT NULL,
  `CYCLE_END` datetime DEFAULT NULL,
  `VALVE_STATUS` varchar(50) DEFAULT NULL,
  `STATUS` int DEFAULT '0',
  `STATION_STATUS` varchar(50) DEFAULT NULL,
  `DATE_TIME` datetime DEFAULT NULL,
  `TESTED_BY` varchar(100) DEFAULT NULL,
  `APPROVED_BY` varchar(100) DEFAULT NULL,
  `COL1_NAME` varchar(50) DEFAULT NULL,
  `COL1_VALUE` varchar(100) DEFAULT NULL,
  `COL2_NAME` varchar(50) DEFAULT NULL,
  `COL2_VALUE` varchar(100) DEFAULT NULL,
  `COL3_NAME` varchar(50) DEFAULT NULL,
  `COL3_VALUE` varchar(100) DEFAULT NULL,
  `COL4_NAME` varchar(50) DEFAULT NULL,
  `COL4_VALUE` varchar(100) DEFAULT NULL,
  `COL5_NAME` varchar(50) DEFAULT NULL,
  `COL5_VALUE` varchar(100) DEFAULT NULL,
  `COL6_NAME` varchar(50) DEFAULT NULL,
  `COL6_VALUE` varchar(100) DEFAULT NULL,
  `COL7_NAME` varchar(50) DEFAULT NULL,
  `COL7_VALUE` varchar(100) DEFAULT NULL,
  `COL8_NAME` varchar(50) DEFAULT NULL,
  `COL8_VALUE` varchar(100) DEFAULT NULL,
  `COL9_NAME` varchar(50) DEFAULT NULL,
  `COL9_VALUE` varchar(100) DEFAULT NULL,
  `COL10_NAME` varchar(50) DEFAULT NULL,
  `COL10_VALUE` varchar(100) DEFAULT NULL,
  `COL11_NAME` varchar(50) DEFAULT NULL,
  `COL11_VALUE` varchar(100) DEFAULT NULL,
  `COL12_NAME` varchar(50) DEFAULT NULL,
  `COL12_VALUE` varchar(100) DEFAULT NULL,
  `COL13_NAME` varchar(50) DEFAULT NULL,
  `COL13_VALUE` varchar(100) DEFAULT NULL,
  `COL14_NAME` varchar(50) DEFAULT NULL,
  `COL14_VALUE` varchar(100) DEFAULT NULL,
  `COL15_NAME` varchar(50) DEFAULT NULL,
  `COL15_VALUE` varchar(100) DEFAULT NULL,
  `COL16_NAME` varchar(50) DEFAULT NULL,
  `COL16_VALUE` varchar(100) DEFAULT NULL,
  `COL17_NAME` varchar(50) DEFAULT NULL,
  `COL17_VALUE` varchar(100) DEFAULT NULL,
  `COL18_NAME` varchar(50) DEFAULT NULL,
  `COL18_VALUE` varchar(100) DEFAULT NULL,
  `COL19_NAME` varchar(50) DEFAULT NULL,
  `COL19_VALUE` varchar(100) DEFAULT NULL,
  `COL20_NAME` varchar(50) DEFAULT NULL,
  `COL20_VALUE` varchar(100) DEFAULT NULL,
  `COL21_NAME` varchar(50) DEFAULT NULL,
  `COL21_VALUE` varchar(100) DEFAULT NULL,
  `COL22_NAME` varchar(50) DEFAULT NULL,
  `COL22_VALUE` varchar(100) DEFAULT NULL,
  `COL23_NAME` varchar(50) DEFAULT NULL,
  `COL23_VALUE` varchar(100) DEFAULT NULL,
  `COL24_NAME` varchar(50) DEFAULT NULL,
  `COL24_VALUE` varchar(100) DEFAULT NULL,
  `COL25_NAME` varchar(50) DEFAULT NULL,
  `COL25_VALUE` varchar(100) DEFAULT NULL,
  `COL26_NAME` varchar(50) DEFAULT NULL,
  `COL26_VALUE` varchar(100) DEFAULT NULL,
  `COL27_NAME` varchar(50) DEFAULT NULL,
  `COL27_VALUE` varchar(100) DEFAULT NULL,
  `COL28_NAME` varchar(50) DEFAULT NULL,
  `COL28_VALUE` varchar(100) DEFAULT NULL,
  `COL29_NAME` varchar(50) DEFAULT NULL,
  `COL29_VALUE` varchar(100) DEFAULT NULL,
  `COL30_NAME` varchar(50) DEFAULT NULL,
  `COL30_VALUE` varchar(100) DEFAULT NULL,
  `COL31_NAME` varchar(50) DEFAULT NULL,
  `COL31_VALUE` varchar(100) DEFAULT NULL,
  `COL32_NAME` varchar(50) DEFAULT NULL,
  `COL32_VALUE` varchar(100) DEFAULT NULL,
  `COL33_NAME` varchar(50) DEFAULT NULL,
  `COL33_VALUE` varchar(100) DEFAULT NULL,
  `COL34_NAME` varchar(50) DEFAULT NULL,
  `COL34_VALUE` varchar(100) DEFAULT NULL,
  `COL35_NAME` varchar(50) DEFAULT NULL,
  `COL35_VALUE` varchar(100) DEFAULT NULL,
  `COL36_NAME` varchar(50) DEFAULT NULL,
  `COL36_VALUE` varchar(100) DEFAULT NULL,
  `COL37_NAME` varchar(50) DEFAULT NULL,
  `COL37_VALUE` varchar(100) DEFAULT NULL,
  `COL38_NAME` varchar(50) DEFAULT NULL,
  `COL38_VALUE` varchar(100) DEFAULT NULL,
  `COL39_NAME` varchar(50) DEFAULT NULL,
  `COL39_VALUE` varchar(100) DEFAULT NULL,
  `COL40_NAME` varchar(50) DEFAULT NULL,
  `COL40_VALUE` varchar(100) DEFAULT NULL,
  `COL41_NAME` varchar(50) DEFAULT NULL,
  `COL41_VALUE` varchar(100) DEFAULT NULL,
  `COL42_NAME` varchar(50) DEFAULT NULL,
  `COL42_VALUE` varchar(100) DEFAULT NULL,
  `COL43_NAME` varchar(50) DEFAULT NULL,
  `COL43_VALUE` varchar(100) DEFAULT NULL,
  `COL44_NAME` varchar(50) DEFAULT NULL,
  `COL44_VALUE` varchar(100) DEFAULT NULL,
  `COL45_NAME` varchar(50) DEFAULT NULL,
  `COL45_VALUE` varchar(100) DEFAULT NULL,
  `COL46_NAME` varchar(50) DEFAULT NULL,
  `COL46_VALUE` varchar(100) DEFAULT NULL,
  `COL47_NAME` varchar(50) DEFAULT NULL,
  `COL47_VALUE` varchar(100) DEFAULT NULL,
  `COL48_NAME` varchar(50) DEFAULT NULL,
  `COL48_VALUE` varchar(100) DEFAULT NULL,
  `COL49_NAME` varchar(50) DEFAULT NULL,
  `COL49_VALUE` varchar(100) DEFAULT NULL,
  `COL50_NAME` varchar(50) DEFAULT NULL,
  `COL50_VALUE` varchar(100) DEFAULT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT NULL,
  `CYCLE_COMPLETE` varchar(45) DEFAULT NULL,
  `CYCLE_COMPLETED_DATE` datetime DEFAULT NULL,
  `DURATION_TYPE` varchar(50) DEFAULT NULL,
  `COL51_NAME` varchar(50) DEFAULT NULL,
  `COL51_VALUE` varchar(100) DEFAULT NULL,
  `COL52_NAME` varchar(50) DEFAULT NULL,
  `COL52_VALUE` varchar(100) DEFAULT NULL,
  `COL53_NAME` varchar(50) DEFAULT NULL,
  `COL53_VALUE` varchar(100) DEFAULT NULL,
  `COL54_NAME` varchar(50) DEFAULT NULL,
  `COL54_VALUE` varchar(100) DEFAULT NULL,
  `COL55_NAME` varchar(50) DEFAULT NULL,
  `COL55_VALUE` varchar(100) DEFAULT NULL,
  `COL56_NAME` varchar(50) DEFAULT NULL,
  `COL56_VALUE` varchar(100) DEFAULT NULL,
  `COL57_NAME` varchar(50) DEFAULT NULL,
  `COL57_VALUE` varchar(100) DEFAULT NULL,
  `COL58_NAME` varchar(50) DEFAULT NULL,
  `COL58_VALUE` varchar(100) DEFAULT NULL,
  `COL59_NAME` varchar(50) DEFAULT NULL,
  `COL59_VALUE` varchar(100) DEFAULT NULL,
  `COL60_NAME` varchar(50) DEFAULT NULL,
  `COL60_VALUE` varchar(100) DEFAULT NULL,
  `COL61_NAME` varchar(50) DEFAULT NULL,
  `COL61_VALUE` varchar(100) DEFAULT NULL,
  `COL62_NAME` varchar(50) DEFAULT NULL,
  `COL62_VALUE` varchar(100) DEFAULT NULL,
  `COL63_NAME` varchar(50) DEFAULT NULL,
  `COL63_VALUE` varchar(100) DEFAULT NULL,
  `COL64_NAME` varchar(50) DEFAULT NULL,
  `COL64_VALUE` varchar(100) DEFAULT NULL,
  `COL65_NAME` varchar(50) DEFAULT NULL,
  `COL65_VALUE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `uniq_test` (`VALVE_SER_NO`,`COUNT_ID`,`TEST_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pressure_analysis`
--

LOCK TABLES `pressure_analysis` WRITE;
/*!40000 ALTER TABLE `pressure_analysis` DISABLE KEYS */;
INSERT INTO `pressure_analysis` VALUES (10,'123456',1,'PRIMARY SHELL',1,1450.000,NULL,'PSI',9,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'STND1','One Twenty\"','Globe','#150','Shell material',NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,'USER 3','vicky','Shift','Shift 3','Date','2026-05-06','Sale Order No','1','Valve Tag No','2','Sale Item No','3','Gad No','4','Applicability','ARAMCO','Witnessed By','USER2','BODY_HEAT_NO','11','BODY_MPI_DP_NO','12','BODY_RT_NO','13','CONNECTOR_L_HEAT_NO','14','CONNECTOR_L_MPI_DP_NO','15','CONNECTOR_L_RT_NO','16','CONNECTOR_R_HEAT_NO','17','CONNECTOR_R_MPI_DP_NO','18','CONNECTOR_R_RT_NO','19','Tested By','vickky','End Details','Test ','body_to_ball_power','110','body_to_ball_resistance','111','body_to_stem_power','112','body_to_stem_resistance','113','actuator_timing_close_open','114','actuator_timing_open_close','115','torque_setting_close_open','116','torque_setting_open_close','117','actuator_sizing_pressure','118','run_torque_set','119','run_torque_result','120','gear_unit_stopper_torque','121','drying_technique_compressed_air','True','drying_technique_vacuum','False','abnormal_sound_result','122','water_draining_result','123','drying_result','124','gear_unit_details','125','actuator_details','126','antistatic_test_result','127','water_temperature_result','128','seat_test_stabilization_time','129','drain_plug_torque','130','vent_plug_torque','131','stem_position','Vertical','remarks','Form 2 Remark','seat_test_vent_set_pressure','134','seat_test_drain_set_pressure','135','seat_test_vent_actual_pressure','136','seat_test_drain_actual_pressure','137','seat_test_vent_duration_min','138',NULL,'Yes',NULL,NULL,'seat_test_drain_duration_min','139','torque_bto_dbb_required','140','torque_bto_dbb_actual','141','torque_bto_connector_l_required','142','torque_bto_connector_l_actual','143','torque_bto_connector_r_required','144','torque_bto_connector_r_actual','145','torque_btc_required','146','torque_btc_actual','147','','','','','','','','','','','',''),(11,'147852',1,'PRIMARY SHELL',1,1450.000,NULL,'PSI',9,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'STND1','One Twenty\"','Globe','#150','Shell material',NULL,NULL,NULL,NULL,'PASS',0,NULL,NULL,NULL,NULL,'Shift','Shift 2','Date','2026-05-06','Sale Order No','101','Valve Tag No','102','Sale Item No','103','Gad No','104','Applicability','ARAMCO','Witnessed By','USER2','BODY_HEAT_NO','2001','BODY_MPI_DP_NO','2002','BODY_RT_NO','2003','CONNECTOR_L_HEAT_NO','2004','CONNECTOR_L_MPI_DP_NO','2005','CONNECTOR_L_RT_NO','2006','CONNECTOR_R_HEAT_NO','2007','CONNECTOR_R_MPI_DP_NO','2008','CONNECTOR_R_RT_NO','2009','Tested By','vickky','End Details','Test ','body_to_ball_power','110','body_to_ball_resistance','111','body_to_stem_power','112','body_to_stem_resistance','113','actuator_timing_close_open','114','actuator_timing_open_close','115','torque_setting_close_open','116','torque_setting_open_close','117','actuator_sizing_pressure','118','run_torque_set','119','run_torque_result','120','gear_unit_stopper_torque','121','drying_technique_compressed_air','False','drying_technique_vacuum','True','abnormal_sound_result','122','water_draining_result','123','drying_result','124','gear_unit_details','125','actuator_details','126','antistatic_test_result','127','water_temperature_result','128','seat_test_stabilization_time','129','drain_plug_torque','130','vent_plug_torque','131','stem_position','Vertical','remarks','Form 2 Remarks','seat_test_vent_set_pressure','134','seat_test_drain_set_pressure','135','seat_test_vent_actual_pressure','136','seat_test_drain_actual_pressure','137','seat_test_vent_duration_min','138',NULL,'Yes',NULL,NULL,'seat_test_drain_duration_min','139','torque_bto_dbb_required','140','torque_bto_dbb_actual','141','torque_bto_connector_l_required','142','torque_bto_connector_l_actual','143','torque_bto_connector_r_required','144','torque_bto_connector_r_actual','145','torque_btc_required','146','torque_btc_actual','147','','','','','','','','','','','',''),(12,'222222',2,'Hydro seat A',1,1450.000,NULL,'PSI',9,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'STND1','One Twenty\"','Globe','#150','Shell material',NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,'Shift','Shift 1','Date','2026-05-06','Sale Order No','1','Valve Tag No','2','Sale Item No','3','Gad No','4','Applicability','ARAMCO','Witnessed By','USER2','BODY_HEAT_NO','11','BODY_MPI_DP_NO','12','BODY_RT_NO','13','CONNECTOR_L_HEAT_NO','14','CONNECTOR_L_MPI_DP_NO','15','CONNECTOR_L_RT_NO','16','CONNECTOR_R_HEAT_NO','17','CONNECTOR_R_MPI_DP_NO','18','CONNECTOR_R_RT_NO','19','Tested By','vickky','End Details','Test ','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',NULL,'Yes',NULL,NULL,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
/*!40000 ALTER TABLE `pressure_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pressure_gauge_analysis`
--

DROP TABLE IF EXISTS `pressure_gauge_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pressure_gauge_analysis` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SER_NO` varchar(255) DEFAULT NULL,
  `INSTRUMENT_SER_NO` varchar(255) DEFAULT NULL,
  `RANGE` varchar(255) DEFAULT NULL,
  `INSTRUMENT_TYPE` varchar(255) DEFAULT NULL,
  `CAL_DUE_DATE` date DEFAULT NULL,
  `CAL_DONE_DATE` date DEFAULT NULL,
  `STATION_ID` int DEFAULT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1636 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pressure_gauge_analysis`
--

LOCK TABLES `pressure_gauge_analysis` WRITE;
/*!40000 ALTER TABLE `pressure_gauge_analysis` DISABLE KEYS */;
INSERT INTO `pressure_gauge_analysis` VALUES (1458,'87654321','GSN-005','0-2000','Air','2026-03-30','2026-03-20',2,'2026-03-10 11:41:20'),(1459,'87654321','GSN-006','0-2000','Air','2026-03-30','2026-03-20',2,'2026-03-10 11:41:20'),(1460,'87654321','GSN-007','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-10 11:41:20'),(1461,'87654321','GSN-008','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-10 11:41:21'),(1462,'5432100','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-10 12:11:30'),(1463,'5432100','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-10 12:11:30'),(1464,'5432100','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:11:30'),(1465,'5432100','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:11:30'),(1466,'65432111','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-10 12:15:44'),(1467,'65432111','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-10 12:15:45'),(1468,'65432111','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:15:45'),(1469,'65432111','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:15:45'),(1470,'654321','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-10 12:25:10'),(1471,'654321','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-10 12:25:10'),(1472,'654321','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:25:10'),(1473,'654321','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:25:10'),(1474,'11223344','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-10 12:31:27'),(1475,'11223344','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-10 12:31:27'),(1476,'11223344','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:31:27'),(1477,'11223344','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:31:27'),(1478,'1234444','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-10 12:35:02'),(1479,'1234444','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-10 12:35:02'),(1480,'1234444','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:35:02'),(1481,'1234444','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-10 12:35:02'),(1482,'654321','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-11 03:51:18'),(1483,'654321','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-11 03:51:19'),(1484,'654321','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 03:51:19'),(1485,'654321','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 03:51:19'),(1486,'65432111','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-11 03:59:16'),(1487,'65432111','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-11 03:59:16'),(1488,'65432111','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 03:59:16'),(1489,'65432111','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 03:59:16'),(1490,'12345677','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-11 04:03:48'),(1491,'12345677','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-11 04:03:48'),(1492,'12345677','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 04:03:48'),(1493,'12345677','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 04:03:48'),(1494,'5554441','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-11 04:13:49'),(1495,'5554441','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-11 04:13:49'),(1496,'5554441','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 04:13:49'),(1497,'5554441','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 04:13:49'),(1498,'8765432','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-11 04:19:25'),(1499,'8765432','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-11 04:19:25'),(1500,'8765432','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 04:19:25'),(1501,'8765432','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-11 04:19:25'),(1502,'331312','GSN-005','0-2000','Air','2026-03-30','2026-03-20',2,'2026-03-11 04:19:44'),(1503,'331312','GSN-006','0-2000','Air','2026-03-30','2026-03-20',2,'2026-03-11 04:19:44'),(1504,'331312','GSN-007','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-11 04:19:44'),(1505,'331312','GSN-008','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-11 04:19:44'),(1506,'123','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-13 04:42:19'),(1507,'123','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-13 04:42:19'),(1508,'123','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-13 04:42:19'),(1509,'123','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-13 04:42:19'),(1510,'123','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-23 04:20:38'),(1511,'123','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-23 04:20:38'),(1512,'123','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-23 04:20:38'),(1513,'123','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-23 04:20:38'),(1514,'1122553','GSN-005','0-2000','Air','2026-03-30','2026-03-20',2,'2026-03-23 04:21:19'),(1515,'1122553','GSN-006','0-2000','Air','2026-03-30','2026-03-20',2,'2026-03-23 04:21:19'),(1516,'1122553','GSN-007','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-23 04:21:19'),(1517,'1122553','GSN-008','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-23 04:21:19'),(1518,'1122333','GSN-001','0-2000','Air','2026-03-11','2025-12-09',1,'2026-03-23 04:23:03'),(1519,'1122333','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-23 04:23:03'),(1520,'1122333','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-23 04:23:03'),(1521,'1122333','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-23 04:23:03'),(1544,'1234','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-23 12:39:54'),(1545,'1234','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-23 12:39:54'),(1546,'1234','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-24 04:11:12'),(1547,'1234','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-24 04:11:12'),(1548,'1234','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-24 04:13:28'),(1549,'1234','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-24 04:13:28'),(1550,'1234','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-24 05:52:58'),(1551,'1234','GSN-002','0-2000','Hydro','2026-03-30','2026-03-20',1,'2026-03-24 05:52:58'),(1552,'1234','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-24 06:06:23'),(1553,'1234','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-24 06:06:23'),(1554,'112255','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-24 11:46:30'),(1555,'112255','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-24 11:46:30'),(1556,'112233','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 04:50:16'),(1557,'112233','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 04:50:16'),(1558,'12222','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 04:56:43'),(1559,'12222','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 04:56:44'),(1560,'1','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 06:28:07'),(1561,'1','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 06:28:07'),(1562,'554422','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 09:26:00'),(1563,'554422','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 09:26:00'),(1564,'14','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 10:48:26'),(1565,'14','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 10:48:26'),(1566,'43312','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 10:57:01'),(1567,'43312','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 10:57:01'),(1568,'11111','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 10:57:52'),(1569,'11111','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 10:57:52'),(1570,'12331','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 11:15:15'),(1571,'12331','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 11:15:15'),(1572,'112233','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 11:30:06'),(1573,'112233','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 11:30:06'),(1574,'111221','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 11:47:56'),(1575,'111221','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 11:47:56'),(1576,'2222','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-25 11:48:01'),(1577,'2222','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-25 11:48:01'),(1578,'33333','GSN-005','0-2000','Air','2026-03-30','2026-03-20',3,'2026-03-25 11:54:05'),(1579,'33333','GSN-006','0-2000','Air','2026-03-30','2026-03-20',3,'2026-03-25 11:54:05'),(1580,'4444','GSN-007','0-2000','Hydro','2026-03-30','2026-03-20',4,'2026-03-25 11:54:39'),(1581,'4444','GSN-008','0-2000','Hydro','2026-03-30','2026-03-20',4,'2026-03-25 11:54:39'),(1582,'11111','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-03-25 12:33:24'),(1583,'11111','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-03-25 12:33:24'),(1584,'431312','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-25 12:33:32'),(1585,'431312','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-03-25 12:33:32'),(1586,'33345','GSN-005','0-2000','Air','2026-03-30','2026-03-20',3,'2026-03-25 12:33:47'),(1587,'33345','GSN-006','0-2000','Air','2026-03-30','2026-03-20',3,'2026-03-25 12:33:47'),(1588,'444122','GSN-007','0-2000','Hydro','2026-03-30','2026-03-20',4,'2026-03-25 12:33:55'),(1589,'444122','GSN-008','0-2000','Hydro','2026-03-30','2026-03-20',4,'2026-03-25 12:33:55'),(1590,'102','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:19:37'),(1591,'102','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:19:37'),(1592,'103','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:20:38'),(1593,'103','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:20:38'),(1594,'102','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:20:42'),(1595,'102','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:20:42'),(1596,'102','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:20:53'),(1597,'102','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:20:53'),(1598,'103','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:21:06'),(1599,'103','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:21:06'),(1600,'101','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:22:05'),(1601,'101','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:22:05'),(1602,'102','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:22:20'),(1603,'102','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:22:20'),(1604,'101','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:27:26'),(1605,'101','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:27:26'),(1606,'102','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:27:33'),(1607,'102','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:27:33'),(1608,'101','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:47:42'),(1609,'101','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:47:42'),(1610,'102','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:47:47'),(1611,'102','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 06:47:47'),(1612,'101','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 06:58:04'),(1613,'101','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 06:58:04'),(1614,'103','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 07:00:22'),(1615,'103','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 07:00:22'),(1616,'104','GSN-003','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 07:00:28'),(1617,'104','GSN-004','0-2000','Hydro','2026-03-30','2026-03-20',2,'2026-05-05 07:00:28'),(1618,'99','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-05 12:15:45'),(1619,'99','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-05 12:15:45'),(1620,'112233`','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 08:53:56'),(1621,'112233`','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 08:53:56'),(1622,'112233`','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 08:55:46'),(1623,'112233`','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 08:55:46'),(1624,'123456','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 09:19:47'),(1625,'123456','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 09:19:47'),(1626,'147852','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 11:15:29'),(1627,'147852','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 11:15:29'),(1628,'147852','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 11:23:29'),(1629,'147852','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 11:23:29'),(1630,'147852','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 11:43:47'),(1631,'147852','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 11:43:47'),(1632,'147852','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 11:50:05'),(1633,'147852','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 11:50:05'),(1634,'222222','GSN-001','0-2000','Air','2026-05-13','2025-12-09',1,'2026-05-06 13:33:56'),(1635,'222222','GSN-002','0-2000','Air','2026-03-30','2026-03-20',1,'2026-05-06 13:33:56');
/*!40000 ALTER TABLE `pressure_gauge_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serial_tbl`
--

DROP TABLE IF EXISTS `serial_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serial_tbl` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Serial_No` varchar(25) DEFAULT NULL,
  `Count_No` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Serial_No` (`Serial_No`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serial_tbl`
--

LOCK TABLES `serial_tbl` WRITE;
/*!40000 ALTER TABLE `serial_tbl` DISABLE KEYS */;
INSERT INTO `serial_tbl` VALUES (1,'101',2),(2,'102',1),(3,'112233`',1),(4,'123456',1),(5,'147852',1),(6,'222222',1);
/*!40000 ALTER TABLE `serial_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shell_material`
--

DROP TABLE IF EXISTS `shell_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shell_material` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `SHELL_MATERIAL_ID` int NOT NULL,
  `SHELL_MATERIAL_NAME` varchar(255) NOT NULL,
  `SHELL_MATERIAL_DESCRIPTION` varchar(255) DEFAULT NULL,
  `SHELL_MATERIAL_STATUS` varchar(45) NOT NULL,
  `CREATE_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`SHELL_MATERIAL_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shell_material`
--

LOCK TABLES `shell_material` WRITE;
/*!40000 ALTER TABLE `shell_material` DISABLE KEYS */;
INSERT INTO `shell_material` VALUES (1,1,'Shell material','added shell material','Enabled','2026-03-04 06:42:23','2026-03-04 06:42:23'),(2,2,'2 Shell','Shell material','Disabled','2026-03-25 06:04:09','2026-03-25 06:05:39'),(3,3,'Shell Material 3','Add the 3 Shell Material','Enabled','2026-03-25 06:05:31','2026-03-25 06:05:31');
/*!40000 ALTER TABLE `shell_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift`
--

DROP TABLE IF EXISTS `shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shift` (
  `ID` bigint NOT NULL AUTO_INCREMENT,
  `SHIFT_NAME` varchar(50) NOT NULL,
  `IS_ACTIVE` tinyint(1) DEFAULT '1',
  `CREATED_AT` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `TYPE_ID` bigint DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift`
--

LOCK TABLES `shift` WRITE;
/*!40000 ALTER TABLE `shift` DISABLE KEYS */;
INSERT INTO `shift` VALUES (1,'Shift_1',1,'2025-11-11 09:05:22','2025-11-11 09:05:22',3),(2,'Shift_1',1,'2025-11-11 09:05:32','2025-11-11 09:05:32',3),(3,'Shift_1',1,'2025-11-11 09:05:46','2025-11-11 09:05:46',3),(4,'Shift_1',1,'2025-11-11 09:11:28','2025-11-11 09:11:28',3),(5,'Shift_1',1,'2025-11-11 09:51:37','2025-11-11 09:51:37',3),(6,'Shift_1',1,'2025-11-11 10:22:14','2025-11-11 10:22:14',3),(7,'Shift_1',1,'2025-11-11 11:33:37','2025-11-11 11:33:37',3),(8,'Shift_1',1,'2025-11-11 11:44:17','2025-11-11 11:44:17',3),(9,'Shift_1',1,'2025-11-11 11:47:42','2025-11-11 11:47:42',3),(10,'Shift_1',1,'2025-11-11 11:53:06','2025-11-11 11:53:06',3),(11,'Shift_1',1,'2025-11-11 11:53:06','2025-11-11 11:53:06',3),(12,'Shift_1',1,'2025-11-11 11:58:32','2025-11-11 11:58:32',3),(13,'Shift_1',1,'2025-11-11 12:10:26','2025-11-11 12:10:26',3),(14,'Shift_1',1,'2025-11-11 12:18:02','2025-11-11 12:18:02',3),(15,'Shift_1',1,'2025-11-11 12:36:20','2025-11-11 12:36:20',3),(16,'Shift_1',1,'2025-11-11 12:51:50','2025-11-11 12:51:50',3),(17,'Shift_1',1,'2025-11-11 12:57:40','2025-11-11 12:57:40',3),(18,'Shift_1',1,'2025-11-11 13:04:12','2025-11-11 13:04:12',3),(19,'Shift_1',1,'2025-11-11 13:14:25','2025-11-11 13:14:25',3),(20,'Shift_1',1,'2025-11-11 13:19:18','2025-11-11 13:19:18',3),(21,'Shift_1',1,'2025-11-12 06:14:56','2025-11-12 06:14:56',3),(22,'Shift_1',1,'2025-11-12 06:17:45','2025-11-12 06:17:45',3),(23,'Shift_1',1,'2025-11-12 06:43:40','2025-11-12 06:43:40',3),(24,'Shift_1',1,'2025-11-12 07:11:08','2025-11-12 07:11:08',3);
/*!40000 ALTER TABLE `shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `standard`
--

DROP TABLE IF EXISTS `standard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `standard` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `STANDARD_ID` int NOT NULL,
  `STANDARD_NAME` varchar(255) NOT NULL,
  `STANDARD_DESC` varchar(255) NOT NULL,
  `STANDARD_STATUS` varchar(45) NOT NULL,
  `CREATED_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`STANDARD_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `standard`
--

LOCK TABLES `standard` WRITE;
/*!40000 ALTER TABLE `standard` DISABLE KEYS */;
INSERT INTO `standard` VALUES (29,1,'STND1','Standard added','Enabled','2026-02-07 10:23:22','2026-02-27 14:09:37'),(30,2,'STND2','STND2 added','Disabled','2026-03-25 11:30:28','2026-03-25 11:31:35'),(31,3,'STND3','STND3 added','Disabled','2026-03-25 11:31:13','2026-03-25 11:40:15'),(32,4,'STND4','STND4 added','Enabled','2026-03-25 11:31:29','2026-03-25 11:31:29');
/*!40000 ALTER TABLE `standard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_pressure_analysis`
--

DROP TABLE IF EXISTS `temp_pressure_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_pressure_analysis` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SER_NO` varchar(100) DEFAULT NULL,
  `TEST_ID` int DEFAULT NULL,
  `TEST_NAME` varchar(255) DEFAULT NULL,
  `COUNT_ID` int DEFAULT NULL,
  `SET_PRESSURE` decimal(18,3) DEFAULT NULL,
  `ACTUAL_PRESSURE` decimal(18,3) DEFAULT NULL,
  `PRESSURE_UNIT` varchar(50) DEFAULT NULL,
  `SET_TIME` int DEFAULT NULL,
  `ACTUAL_TIME` int DEFAULT NULL,
  `SET_TIME_UNIT` varchar(50) DEFAULT NULL,
  `CLAMPING_PRESSURE` decimal(18,3) DEFAULT NULL,
  `ACTUAL_OPEN_TORQUE` float DEFAULT NULL,
  `ACTUAL_CLOSE_TORQUE` float DEFAULT NULL,
  `START_PRESSURE` decimal(18,3) DEFAULT NULL,
  `RESULT_PRESSURE` decimal(18,3) DEFAULT NULL,
  `LEAK_PRESSURE` decimal(18,3) DEFAULT NULL,
  `STANDARD_NAME` varchar(255) DEFAULT NULL,
  `VALVESIZE_NAME` varchar(100) DEFAULT NULL,
  `VALVETYPE_NAME` varchar(100) DEFAULT NULL,
  `VALVECLASS_NAME` varchar(100) DEFAULT NULL,
  `SHELLMATERIAL_NAME` varchar(100) DEFAULT NULL,
  `START` datetime DEFAULT NULL,
  `END` datetime DEFAULT NULL,
  `CYCLE_START` datetime DEFAULT NULL,
  `CYCLE_END` datetime DEFAULT NULL,
  `VALVE_STATUS` varchar(50) DEFAULT NULL,
  `STATUS` int DEFAULT '0',
  `STATION_STATUS` varchar(50) DEFAULT NULL,
  `DATE_TIME` datetime DEFAULT NULL,
  `TESTED_BY` varchar(100) DEFAULT NULL,
  `APPROVED_BY` varchar(100) DEFAULT NULL,
  `COL1_NAME` varchar(50) DEFAULT NULL,
  `COL1_VALUE` varchar(100) DEFAULT NULL,
  `COL2_NAME` varchar(50) DEFAULT NULL,
  `COL2_VALUE` varchar(100) DEFAULT NULL,
  `COL3_NAME` varchar(50) DEFAULT NULL,
  `COL3_VALUE` varchar(100) DEFAULT NULL,
  `COL4_NAME` varchar(50) DEFAULT NULL,
  `COL4_VALUE` varchar(100) DEFAULT NULL,
  `COL5_NAME` varchar(50) DEFAULT NULL,
  `COL5_VALUE` varchar(100) DEFAULT NULL,
  `COL6_NAME` varchar(50) DEFAULT NULL,
  `COL6_VALUE` varchar(100) DEFAULT NULL,
  `COL7_NAME` varchar(50) DEFAULT NULL,
  `COL7_VALUE` varchar(100) DEFAULT NULL,
  `COL8_NAME` varchar(50) DEFAULT NULL,
  `COL8_VALUE` varchar(100) DEFAULT NULL,
  `COL9_NAME` varchar(50) DEFAULT NULL,
  `COL9_VALUE` varchar(100) DEFAULT NULL,
  `COL10_NAME` varchar(50) DEFAULT NULL,
  `COL10_VALUE` varchar(100) DEFAULT NULL,
  `COL11_NAME` varchar(50) DEFAULT NULL,
  `COL11_VALUE` varchar(100) DEFAULT NULL,
  `COL12_NAME` varchar(50) DEFAULT NULL,
  `COL12_VALUE` varchar(100) DEFAULT NULL,
  `COL13_NAME` varchar(50) DEFAULT NULL,
  `COL13_VALUE` varchar(100) DEFAULT NULL,
  `COL14_NAME` varchar(50) DEFAULT NULL,
  `COL14_VALUE` varchar(100) DEFAULT NULL,
  `COL15_NAME` varchar(50) DEFAULT NULL,
  `COL15_VALUE` varchar(100) DEFAULT NULL,
  `COL16_NAME` varchar(50) DEFAULT NULL,
  `COL16_VALUE` varchar(100) DEFAULT NULL,
  `COL17_NAME` varchar(50) DEFAULT NULL,
  `COL17_VALUE` varchar(100) DEFAULT NULL,
  `COL18_NAME` varchar(50) DEFAULT NULL,
  `COL18_VALUE` varchar(100) DEFAULT NULL,
  `COL19_NAME` varchar(50) DEFAULT NULL,
  `COL19_VALUE` varchar(100) DEFAULT NULL,
  `COL20_NAME` varchar(50) DEFAULT NULL,
  `COL20_VALUE` varchar(100) DEFAULT NULL,
  `COL21_NAME` varchar(50) DEFAULT NULL,
  `COL21_VALUE` varchar(100) DEFAULT NULL,
  `COL22_NAME` varchar(50) DEFAULT NULL,
  `COL22_VALUE` varchar(100) DEFAULT NULL,
  `COL23_NAME` varchar(50) DEFAULT NULL,
  `COL23_VALUE` varchar(100) DEFAULT NULL,
  `COL24_NAME` varchar(50) DEFAULT NULL,
  `COL24_VALUE` varchar(100) DEFAULT NULL,
  `COL25_NAME` varchar(50) DEFAULT NULL,
  `COL25_VALUE` varchar(100) DEFAULT NULL,
  `COL26_NAME` varchar(50) DEFAULT NULL,
  `COL26_VALUE` varchar(100) DEFAULT NULL,
  `COL27_NAME` varchar(50) DEFAULT NULL,
  `COL27_VALUE` varchar(100) DEFAULT NULL,
  `COL28_NAME` varchar(50) DEFAULT NULL,
  `COL28_VALUE` varchar(100) DEFAULT NULL,
  `COL29_NAME` varchar(50) DEFAULT NULL,
  `COL29_VALUE` varchar(100) DEFAULT NULL,
  `COL30_NAME` varchar(50) DEFAULT NULL,
  `COL30_VALUE` varchar(100) DEFAULT NULL,
  `COL31_NAME` varchar(50) DEFAULT NULL,
  `COL31_VALUE` varchar(100) DEFAULT NULL,
  `COL32_NAME` varchar(50) DEFAULT NULL,
  `COL32_VALUE` varchar(100) DEFAULT NULL,
  `COL33_NAME` varchar(50) DEFAULT NULL,
  `COL33_VALUE` varchar(100) DEFAULT NULL,
  `COL34_NAME` varchar(50) DEFAULT NULL,
  `COL34_VALUE` varchar(100) DEFAULT NULL,
  `COL35_NAME` varchar(50) DEFAULT NULL,
  `COL35_VALUE` varchar(100) DEFAULT NULL,
  `COL36_NAME` varchar(50) DEFAULT NULL,
  `COL36_VALUE` varchar(100) DEFAULT NULL,
  `COL37_NAME` varchar(50) DEFAULT NULL,
  `COL37_VALUE` varchar(100) DEFAULT NULL,
  `COL38_NAME` varchar(50) DEFAULT NULL,
  `COL38_VALUE` varchar(100) DEFAULT NULL,
  `COL39_NAME` varchar(50) DEFAULT NULL,
  `COL39_VALUE` varchar(100) DEFAULT NULL,
  `COL40_NAME` varchar(50) DEFAULT NULL,
  `COL40_VALUE` varchar(100) DEFAULT NULL,
  `COL41_NAME` varchar(50) DEFAULT NULL,
  `COL41_VALUE` varchar(100) DEFAULT NULL,
  `COL42_NAME` varchar(50) DEFAULT NULL,
  `COL42_VALUE` varchar(100) DEFAULT NULL,
  `COL43_NAME` varchar(50) DEFAULT NULL,
  `COL43_VALUE` varchar(100) DEFAULT NULL,
  `COL44_NAME` varchar(50) DEFAULT NULL,
  `COL44_VALUE` varchar(100) DEFAULT NULL,
  `COL45_NAME` varchar(50) DEFAULT NULL,
  `COL45_VALUE` varchar(100) DEFAULT NULL,
  `COL46_NAME` varchar(50) DEFAULT NULL,
  `COL46_VALUE` varchar(100) DEFAULT NULL,
  `COL47_NAME` varchar(50) DEFAULT NULL,
  `COL47_VALUE` varchar(100) DEFAULT NULL,
  `COL48_NAME` varchar(50) DEFAULT NULL,
  `COL48_VALUE` varchar(100) DEFAULT NULL,
  `COL49_NAME` varchar(50) DEFAULT NULL,
  `COL49_VALUE` varchar(100) DEFAULT NULL,
  `COL50_NAME` varchar(50) DEFAULT NULL,
  `COL50_VALUE` varchar(100) DEFAULT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT NULL,
  `CYCLE_COMPLETE` varchar(45) DEFAULT NULL,
  `DURATION_TYPE` varchar(50) DEFAULT NULL,
  `COL51_NAME` varchar(50) DEFAULT NULL,
  `COL51_VALUE` varchar(100) DEFAULT NULL,
  `COL52_NAME` varchar(50) DEFAULT NULL,
  `COL52_VALUE` varchar(100) DEFAULT NULL,
  `COL53_NAME` varchar(50) DEFAULT NULL,
  `COL53_VALUE` varchar(100) DEFAULT NULL,
  `COL54_NAME` varchar(50) DEFAULT NULL,
  `COL54_VALUE` varchar(100) DEFAULT NULL,
  `COL55_NAME` varchar(50) DEFAULT NULL,
  `COL55_VALUE` varchar(100) DEFAULT NULL,
  `COL56_NAME` varchar(50) DEFAULT NULL,
  `COL56_VALUE` varchar(100) DEFAULT NULL,
  `COL57_NAME` varchar(50) DEFAULT NULL,
  `COL57_VALUE` varchar(100) DEFAULT NULL,
  `COL58_NAME` varchar(50) DEFAULT NULL,
  `COL58_VALUE` varchar(100) DEFAULT NULL,
  `COL59_NAME` varchar(50) DEFAULT NULL,
  `COL59_VALUE` varchar(100) DEFAULT NULL,
  `COL60_NAME` varchar(50) DEFAULT NULL,
  `COL60_VALUE` varchar(100) DEFAULT NULL,
  `COL61_NAME` varchar(50) DEFAULT NULL,
  `COL61_VALUE` varchar(100) DEFAULT NULL,
  `COL62_NAME` varchar(50) DEFAULT NULL,
  `COL62_VALUE` varchar(100) DEFAULT NULL,
  `COL63_NAME` varchar(50) DEFAULT NULL,
  `COL63_VALUE` varchar(100) DEFAULT NULL,
  `COL64_NAME` varchar(50) DEFAULT NULL,
  `COL64_VALUE` varchar(100) DEFAULT NULL,
  `COL65_NAME` varchar(50) DEFAULT NULL,
  `COL65_VALUE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `uniq_test` (`VALVE_SER_NO`,`COUNT_ID`,`TEST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_pressure_analysis`
--

LOCK TABLES `temp_pressure_analysis` WRITE;
/*!40000 ALTER TABLE `temp_pressure_analysis` DISABLE KEYS */;
/*!40000 ALTER TABLE `temp_pressure_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_testing_data`
--

DROP TABLE IF EXISTS `temp_testing_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_testing_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `VALVE_SERIAL_NO` varchar(45) DEFAULT NULL,
  `TEST_ID` int NOT NULL,
  `TEST_NAME` varchar(255) NOT NULL,
  `TEST_MEDIUM` varchar(255) NOT NULL,
  `TEST_CATEGORY` varchar(255) NOT NULL,
  `COL_PRE` varchar(255) NOT NULL,
  `COL_DUR` varchar(255) NOT NULL,
  `TESTING_PR_UNIT` varchar(255) NOT NULL,
  `TESTING_PR_BAR` double(18,2) NOT NULL,
  `TESTING_PR_PSI` double(18,2) NOT NULL,
  `TESTING_PR_KGCM2` double(18,2) NOT NULL,
  `TESTING_DUR_UNIT` varchar(255) NOT NULL,
  `TESTING_DUR_SEC` int NOT NULL,
  `TESTING_DUR_MIN` int NOT NULL,
  `CREATED_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_testing_data`
--

LOCK TABLES `temp_testing_data` WRITE;
/*!40000 ALTER TABLE `temp_testing_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `temp_testing_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_type`
--

DROP TABLE IF EXISTS `test_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_type` (
  `id` int NOT NULL,
  `TEST_TYPE_ID` int NOT NULL,
  `TEST_TYPE_NAME` varchar(255) DEFAULT NULL,
  `TEST_CATEGORY_ID` varchar(255) DEFAULT NULL,
  `TEST_STATUS` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`TEST_TYPE_ID`),
  UNIQUE KEY `test_id_UNIQUE` (`TEST_TYPE_ID`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `test_name_UNIQUE` (`TEST_TYPE_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_type`
--

LOCK TABLES `test_type` WRITE;
/*!40000 ALTER TABLE `test_type` DISABLE KEYS */;
INSERT INTO `test_type` VALUES (1,1,'PRIMARY SHELL','1','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(2,2,'SECONDARY SHELL','1','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(3,3,'BACK SEAT','5','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(4,4,'HYDRO SEAT L','4','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(5,5,'HYDRO SEAT T','4','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(6,6,'AIR SEAT L','3','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(7,7,'AIR SEAT T','3','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(8,8,'LOW PRESSURE','4','ENABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(9,9,'SPARE 4',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(10,10,'SPARE 5',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(11,11,'SPARE 6',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(12,12,'SPARE 7',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(13,13,'SPARE 8',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(14,14,'SPARE 9',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(15,15,'SPARE 10',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(16,16,'SPARE 11',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(17,17,'SPARE 12',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(18,18,'SPARE 13',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(19,19,'SPARE 14',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(20,20,'SPARE 15',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(21,21,'SPARE 16',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(22,22,'SPARE 17',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(23,23,'SPARE 18',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(24,24,'SPARE 19',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33'),(25,25,'SPARE 20',NULL,'DISABLE','2025-10-25 07:08:22','2026-03-23 05:10:33');
/*!40000 ALTER TABLE `test_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valve_type`
--

DROP TABLE IF EXISTS `valve_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valve_type` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_TYPE_ID` int NOT NULL,
  `VALVE_TYPE_NAME` varchar(255) NOT NULL,
  `VALVE_TYPE_DESCRIPTION` varchar(255) DEFAULT NULL,
  `VALVE_TYPE_STATUS` varchar(45) NOT NULL,
  `CREATED_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`VALVE_TYPE_ID`),
  UNIQUE KEY `TYPE_ID` (`VALVE_TYPE_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valve_type`
--

LOCK TABLES `valve_type` WRITE;
/*!40000 ALTER TABLE `valve_type` DISABLE KEYS */;
INSERT INTO `valve_type` VALUES (82,1,'TMBV','TMBV added','Disabled','2026-02-06 12:56:56','2026-03-25 11:28:27'),(84,2,'Gate','','Enabled','2026-03-23 10:31:58','2026-03-25 11:40:51'),(85,3,'Globe','','Enabled','2026-03-24 12:24:25','2026-03-24 12:24:25'),(86,4,'Check','','Enabled','2026-03-24 13:10:43','2026-03-24 13:10:43');
/*!40000 ALTER TABLE `valve_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valveclass`
--

DROP TABLE IF EXISTS `valveclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valveclass` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_CLASS_ID` int NOT NULL,
  `VALVE_CLASS_NAME` varchar(255) NOT NULL,
  `VALVE_CLASS_DESCRIPTION` varchar(255) DEFAULT NULL,
  `VALVE_CLASS_STATUS` varchar(45) NOT NULL,
  `CREATE_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`VALVE_CLASS_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valveclass`
--

LOCK TABLES `valveclass` WRITE;
/*!40000 ALTER TABLE `valveclass` DISABLE KEYS */;
INSERT INTO `valveclass` VALUES (20,1,'#150','#150 class added','Enabled','2026-02-06 07:25:02','2026-02-07 05:03:16'),(21,2,'#300','#300class added','Enabled','2026-03-25 05:55:39','2026-03-25 05:55:39'),(22,3,'#600','#600 class added','Disabled','2026-03-25 05:57:51','2026-03-25 05:58:15'),(23,4,'#900','#900 class added','Disabled','2026-03-25 05:58:08','2026-03-25 06:11:47');
/*!40000 ALTER TABLE `valveclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valvesize`
--

DROP TABLE IF EXISTS `valvesize`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valvesize` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_SIZE_ID` int NOT NULL,
  `VALVE_SIZE_NAME` varchar(255) NOT NULL,
  `VALVE_SIZE_DESCRIPTION` varchar(255) NOT NULL,
  `PART_NO` varchar(100) NOT NULL,
  `PART_NAME` varchar(255) NOT NULL,
  `VALVE_SIZE_STATUS` varchar(45) NOT NULL,
  `CREATED_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`VALVE_SIZE_ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valvesize`
--

LOCK TABLES `valvesize` WRITE;
/*!40000 ALTER TABLE `valvesize` DISABLE KEYS */;
INSERT INTO `valvesize` VALUES (13,120,'One Twenty\"','Desv','PArtnO','Partname','Enabled','2026-05-05 11:44:59','2026-05-05 11:44:59');
/*!40000 ALTER TABLE `valvesize` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valvetype_testtype`
--

DROP TABLE IF EXISTS `valvetype_testtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valvetype_testtype` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VALVE_TYPE_ID` int NOT NULL,
  `TEST_TYPE_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `unique_type_test` (`VALVE_TYPE_ID`,`TEST_TYPE_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valvetype_testtype`
--

LOCK TABLES `valvetype_testtype` WRITE;
/*!40000 ALTER TABLE `valvetype_testtype` DISABLE KEYS */;
INSERT INTO `valvetype_testtype` VALUES (108,1,1),(109,1,2),(110,1,3),(111,1,4),(112,1,5),(113,1,6),(114,1,7),(115,1,8),(116,2,1),(117,2,2),(118,2,3),(92,3,1),(93,3,2),(94,3,3),(95,3,4),(96,3,5),(97,3,6),(98,3,7),(99,3,8),(100,4,1),(101,4,2),(102,4,3),(103,4,4),(104,4,5),(105,4,6),(106,4,7),(107,4,8);
/*!40000 ALTER TABLE `valvetype_testtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'landt60mt-2station'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-07  9:59:52
