DROP DATABASE IF EXISTS `statfive`;
CREATE SCHEMA `statfive`;

use `statfive`;

-- MySQL dump 10.13  Distrib 8.0.21, for osx10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: statfive
-- ------------------------------------------------------
-- Server version	8.0.17

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
-- Table structure for table `match_played`
--

DROP TABLE IF EXISTS `match_played`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match_played` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `duration` varchar(255) NOT NULL,
  `ground` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match_played`
--

LOCK TABLES `match_played` WRITE;
/*!40000 ALTER TABLE `match_played` DISABLE KEYS */;
INSERT INTO `match_played` VALUES (1,'match1','12',12,'uwiew');
/*!40000 ALTER TABLE `match_played` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stats`
--

DROP TABLE IF EXISTS `stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `kilometre` int(11) DEFAULT NULL,
  `passe` int(11) DEFAULT NULL,
  `but` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `userstat` (`user_id`),
  CONSTRAINT `userstat` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stats`
--

LOCK TABLES `stats` WRITE;
/*!40000 ALTER TABLE `stats` DISABLE KEYS */;
INSERT INTO `stats` VALUES (1,1,10,30,10),(2,2,40,10,15),(3,1,30,10,10);
/*!40000 ALTER TABLE `stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES (1,'team1'),(2,'team2'),(3,'team3'),(4,'jaouadred'),(5,'jaouadblue');
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_has_match_played`
--

DROP TABLE IF EXISTS `team_has_match_played`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_has_match_played` (
  `match_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `goals` int(3) NOT NULL,
  `possesion` float NOT NULL,
  `color` varchar(10) NOT NULL,
  `ended` tinyint(1) NOT NULL,
  KEY `matchid` (`match_id`),
  KEY `teamid` (`team_id`),
  CONSTRAINT `matchid` FOREIGN KEY (`match_id`) REFERENCES `match_played` (`id`),
  CONSTRAINT `teamid` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_has_match_played`
--

LOCK TABLES `team_has_match_played` WRITE;
/*!40000 ALTER TABLE `team_has_match_played` DISABLE KEYS */;
INSERT INTO `team_has_match_played` VALUES (1,4,1,50,'red',1),(1,5,2,50,'blue',1);
/*!40000 ALTER TABLE `team_has_match_played` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_stats`
--

DROP TABLE IF EXISTS `team_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_stats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `but` int(11) NOT NULL,
  `passe` int(11) NOT NULL,
  `km` float NOT NULL,
  `possesion` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teamstats` (`team_id`),
  CONSTRAINT `teamstats` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_stats`
--

LOCK TABLES `team_stats` WRITE;
/*!40000 ALTER TABLE `team_stats` DISABLE KEYS */;
INSERT INTO `team_stats` VALUES (1,4,10,50,40,50),(2,5,25,50,40,50);
/*!40000 ALTER TABLE `team_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_has_team`
--

DROP TABLE IF EXISTS `user_has_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_has_team` (
  `team_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  KEY `team` (`team_id`),
  KEY `user` (`user_id`),
  CONSTRAINT `team` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`),
  CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_has_team`
--

LOCK TABLES `user_has_team` WRITE;
/*!40000 ALTER TABLE `user_has_team` DISABLE KEYS */;
INSERT INTO `user_has_team` VALUES (4,1),(5,2);
/*!40000 ALTER TABLE `user_has_team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` tinyint(1) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `firstname` varchar(45) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

ALTER TABLE `users`
ADD COLUMN `code` VARCHAR(45) NULL AFTER `image`,
ADD COLUMN `verification` TINYINT(1) NULL AFTER `code`;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,0,'jaouad@gmail.com','elhormi','jaouad','pbkdf2:sha256:260000$L1AmSnPjCtNX7pm0$3dca7aaf82a577f3fcb7ee8cf1f2eadd45f30814102003d4f35d66e82fdf64f1',NULL, 'aaaa', 1),(2,0,'jaouad@jaouad.com','jaouad','jaouad','pbkdf2:sha256:260000$INCFtMQOPWdPQ5MO$db08b9642113a37274145c8556942b086ee8737dbd1b10477d056f0bf8603107',NULL, 'aaaa', 1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-09  9:27:38


# use statfive;
#
# CREATE TABLE `match_played` (
#   `id` int(11) NOT NULL,
#   `name` varchar(255) NOT NULL,
#   `duration` varchar(255) NOT NULL,
#   `ground` int(11) NOT NULL,
#   `path` varchar(255) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `stats` (
#   `id` int(11) NOT NULL,
#   `user_id` int(11) DEFAULT NULL,
#   `kilometre` int(11) DEFAULT NULL,
#   `passe` int(11) DEFAULT NULL,
#   `but` int(11) DEFAULT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `team` (
#   `id` int(11) NOT NULL,
#   `name` varchar(45) DEFAULT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `team_has_match_played` (
#   `match_id` int(11) NOT NULL,
#   `team_id` int(11) NOT NULL,
#   `goals` int(3) NOT NULL,
#   `possesion` float NOT NULL,
#   `color` varchar(10) NOT NULL,
#   `ended` tinyint(1) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `team_stats` (
#   `id` int(11) NOT NULL,
#   `team_id` int(11) NOT NULL,
#   `but` int(11) NOT NULL,
#   `passe` int(11) NOT NULL,
#   `km` float NOT NULL,
#   `possesion` float NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `users` (
#   `id` int(11) NOT NULL,
#   `role` tinyint(1) NOT NULL,
#   `mail` varchar(255) DEFAULT NULL,
#   `name` varchar(45) DEFAULT NULL,
#   `firstname` varchar(45) DEFAULT NULL,
#   `password` varchar(200) DEFAULT NULL,
#   `image` varchar(45) DEFAULT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `user_has_team` (
#   `team_id` int(11) NOT NULL,
#   `user_id` int(11) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
# --
# -- Index pour la table `match_played`
# --
# ALTER TABLE `match_played`
#   ADD PRIMARY KEY (`id`);
#
# --
# -- Index pour la table `stats`
# --
# ALTER TABLE `stats`
#   ADD PRIMARY KEY (`id`),
#   ADD KEY `userstat` (`user_id`);
#
# --
# -- Index pour la table `team`
# --
# ALTER TABLE `team`
#   ADD PRIMARY KEY (`id`);
#
# --
# -- Index pour la table `team_has_match_played`
# --
# ALTER TABLE `team_has_match_played`
#   ADD KEY `matchid` (`match_id`),
#   ADD KEY `teamid` (`team_id`);
#
# --
# -- Index pour la table `team_stats`
# --
# ALTER TABLE `team_stats`
#   ADD PRIMARY KEY (`id`),
#   ADD KEY `teamstats` (`team_id`);
#
# --
# -- Index pour la table `users`
# --
# ALTER TABLE `users`
#   ADD PRIMARY KEY (`id`);
#
# --
# -- Index pour la table `user_has_team`
# --
# ALTER TABLE `user_has_team`
#   ADD KEY `team` (`team_id`),
#   ADD KEY `user` (`user_id`);
#
# --
# -- AUTO_INCREMENT pour les tables déchargées
# --
#
# --
# -- AUTO_INCREMENT pour la table `match_played`
# --
# ALTER TABLE `match_played`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
#
# --
# -- AUTO_INCREMENT pour la table `stats`
# --
# ALTER TABLE `stats`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
#
# --
# -- AUTO_INCREMENT pour la table `team`
# --
# ALTER TABLE `team`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
#
# --
# -- AUTO_INCREMENT pour la table `team_stats`
# --
# ALTER TABLE `team_stats`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
#
# --
# -- AUTO_INCREMENT pour la table `users`
# --
# ALTER TABLE `users`
#   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
#
# --
# -- Contraintes pour les tables déchargées
# --
#
# --
# -- Contraintes pour la table `stats`
# --
# ALTER TABLE `stats`
#   ADD CONSTRAINT `userstat` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
#
# --
# -- Contraintes pour la table `team_has_match_played`
# --
# ALTER TABLE `team_has_match_played`
#   ADD CONSTRAINT `matchid` FOREIGN KEY (`match_id`) REFERENCES `match_played` (`id`),
#   ADD CONSTRAINT `teamid` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);
#
# --
# -- Contraintes pour la table `team_stats`
# --
# ALTER TABLE `team_stats`
#   ADD CONSTRAINT `teamstats` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);
#
# --
# -- Contraintes pour la table `user_has_team`
# --
# ALTER TABLE `user_has_team`
#   ADD CONSTRAINT `team` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`),
#   ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
# COMMIT;
