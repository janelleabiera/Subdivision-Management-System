-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: subdivisiondb
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `_block`
--

DROP TABLE IF EXISTS `_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `_block` (
  `block_id` int NOT NULL AUTO_INCREMENT,
  `number_of_units` int DEFAULT NULL,
  `block_total_area` decimal(10,0) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`block_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_block`
--

LOCK TABLES `_block` WRITE;
/*!40000 ALTER TABLE `_block` DISABLE KEYS */;
INSERT INTO `_block` VALUES (12,10,50,'1 First St.'),(13,6,89,'2 Second St.'),(14,7,78,'Random st.'),(15,3,231,'Hello st.');
/*!40000 ALTER TABLE `_block` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bills`
--

DROP TABLE IF EXISTS `bills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bills` (
  `bill_id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int DEFAULT NULL,
  `bill_category` varchar(255) DEFAULT NULL,
  `bill_amount` float DEFAULT NULL,
  `billing_date` date DEFAULT NULL,
  `bill_status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`bill_id`),
  KEY `unit_id` (`unit_id`),
  CONSTRAINT `bills_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`unit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bills`
--

LOCK TABLES `bills` WRITE;
/*!40000 ALTER TABLE `bills` DISABLE KEYS */;
INSERT INTO `bills` VALUES (30,20,'Rent',6000,'2024-06-17',0),(32,19,'Renovation',9000,'2024-06-18',0),(33,19,'Rent',8000,'2024-06-18',0),(35,21,'Renovation',3002,'2024-06-18',0),(37,20,'Repairs',1000,'2024-06-18',0),(38,21,'Repairs',3333,'2024-06-18',1),(39,20,'Renovation',9000,'2024-06-18',1),(40,21,'Restoration',38888,'2024-06-18',1),(41,21,'Cleaning',2000,'2024-06-18',0);
/*!40000 ALTER TABLE `bills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `occupants`
--

DROP TABLE IF EXISTS `occupants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `occupants` (
  `occupant_id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int DEFAULT NULL,
  `occupant_name` varchar(255) DEFAULT NULL,
  `occupant_age` int DEFAULT NULL,
  `occupant_sex` varchar(255) DEFAULT NULL,
  `occupant_phone_number` bigint DEFAULT NULL,
  `move_in_date` date DEFAULT NULL,
  PRIMARY KEY (`occupant_id`),
  KEY `unit_id` (`unit_id`),
  CONSTRAINT `occupants_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`unit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `occupants`
--

LOCK TABLES `occupants` WRITE;
/*!40000 ALTER TABLE `occupants` DISABLE KEYS */;
INSERT INTO `occupants` VALUES (31,19,'Santa Claus',89,'Male',932813642,'2024-06-17'),(38,20,'Name N. Name',90,'Female',932032,'2022-01-14'),(39,20,'User U. User',18,'Female',90909092,'2022-01-14'),(40,20,'Hello H. Ello',36,'Female',232934999,'2022-01-14'),(41,21,'Username U. Sername',73,'Female',9999999999,'2022-08-23'),(42,21,'Myna M. Eis',30,'Female',98323421421,'2024-06-18'),(46,23,'H',3,'Female',2398,'2020-12-02'),(48,23,'Labrador',22,'Male',938182,'2024-06-18'),(49,23,'Hello',21,'Female',9388850830,'2024-06-18'),(56,20,'Ele C. Tricfan',23,'Male',9555434567,'2024-06-18'),(58,23,'Tao T. Ao',19,'Male',97231727,'2020-12-02');
/*!40000 ALTER TABLE `occupants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `bill_id` int DEFAULT NULL,
  `payment_amount` float DEFAULT NULL,
  `payment_method` varchar(255) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `bills` (`bill_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit`
--

DROP TABLE IF EXISTS `unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unit` (
  `unit_id` int NOT NULL AUTO_INCREMENT,
  `block_id` int DEFAULT NULL,
  `occupancy_status` tinyint(1) DEFAULT NULL,
  `number_of_floors` int DEFAULT NULL,
  `unit_total_area` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`unit_id`),
  KEY `block_id` (`block_id`),
  CONSTRAINT `block_id` FOREIGN KEY (`block_id`) REFERENCES `_block` (`block_id`),
  CONSTRAINT `unit_ibfk_1` FOREIGN KEY (`block_id`) REFERENCES `_block` (`block_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit`
--

LOCK TABLES `unit` WRITE;
/*!40000 ALTER TABLE `unit` DISABLE KEYS */;
INSERT INTO `unit` VALUES (19,12,1,5,59),(20,13,1,4,832),(21,14,1,7,467),(22,14,1,9,2313),(23,15,1,2,321);
/*!40000 ALTER TABLE `unit` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-18 20:23:54
