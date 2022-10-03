-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : mariadb
-- Généré le : dim. 02 oct. 2022 à 17:08
-- Version du serveur : 10.5.9-MariaDB-1:10.5.9+maria~focal
-- Version de PHP : 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `statfive`
--
CREATE DATABASE IF NOT EXISTS `statfive` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `statfive`;

-- --------------------------------------------------------

--
-- Structure de la table `complex`
--

DROP TABLE IF EXISTS `complex`;
CREATE TABLE `complex` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `complex`
--

INSERT INTO `complex` (`id`, `name`, `phone`, `address`) VALUES
(2, 'Complexe sofiane', '0618540065', '1 rue de toulouse');

-- --------------------------------------------------------

--
-- Structure de la table `match_played`
--

DROP TABLE IF EXISTS `match_played`;
CREATE TABLE `match_played` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `duration` varchar(255) NOT NULL,
  `ground` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `finish` tinyint(2) NOT NULL DEFAULT 0,
  `complex_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `match_played`
--

INSERT INTO `match_played` (`id`, `name`, `duration`, `ground`, `path`, `finish`, `complex_id`) VALUES
(1, '167685_video.mp4', '10:00', 1, '/app/video/167685_video.mp4', 1, 2),
(10, '126654_video.mp4', '10:00', 1, '/app/video/126654_video.mp4', 1, 2),
(11, '712330_video.mp4', '10:00', 1, '/app/video/712330_video.mp4', 1, 2),
(12, '002871_video.mp4', '10:00', 1, '/app/video/002871_video.mp4', 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `pending`
--

DROP TABLE IF EXISTS `pending`;
CREATE TABLE `pending` (
  `id` int(11) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `expired` tinyint(2) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `stats`
--

DROP TABLE IF EXISTS `stats`;
CREATE TABLE `stats` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `kilometre` int(11) DEFAULT NULL,
  `passe` int(11) DEFAULT NULL,
  `but` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `team`
--

DROP TABLE IF EXISTS `team`;
CREATE TABLE `team` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `team`
--

INSERT INTO `team` (`id`, `name`) VALUES
(6, 'Lions'),
(8, 'Indestructibles');

-- --------------------------------------------------------

--
-- Structure de la table `team_has_match_played`
--

DROP TABLE IF EXISTS `team_has_match_played`;
CREATE TABLE `team_has_match_played` (
  `match_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `goals` int(3) NOT NULL,
  `possesion` float NOT NULL,
  `color` varchar(10) NOT NULL,
  `ended` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `team_has_match_played`
--

INSERT INTO `team_has_match_played` (`match_id`, `team_id`, `goals`, `possesion`, `color`, `ended`) VALUES
(1, 6, 1, 12.0805, '0', 1),
(1, 8, 0, 87.9195, '1', 1),
(10, 8, 3, 70, '0', 1),
(10, 6, 2, 30, '1', 1),
(11, 6, 3, 70, '0', 1),
(11, 8, 2, 30, '1', 1),
(12, 8, 1, 12.0805, '0', 1),
(12, 6, 0, 87.9195, '1', 1);

-- --------------------------------------------------------

--
-- Structure de la table `team_stats`
--

DROP TABLE IF EXISTS `team_stats`;
CREATE TABLE `team_stats` (
  `id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `but` int(11) NOT NULL,
  `passe` int(11) NOT NULL,
  `km` float NOT NULL,
  `possesion` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `role` tinyint(1) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `firstname` varchar(45) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `verification` tinyint(1) DEFAULT NULL,
  `post` varchar(45) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `complex_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `role`, `mail`, `name`, `firstname`, `password`, `image`, `code`, `verification`, `post`, `description`, `complex_id`) VALUES
(3, 2, 'mokhta_s@etna-alternance.net', 'Mokhtari', 'Sofiane', 'pbkdf2:sha256:260000$Y4ylYZFrbRXZF16W$a12c5d5b0ad0c9f999ae4095a28248fdda3eb69e5455211d31f47f7680a6dfb2', NULL, '036304', 1, 'Attaquant', 'ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING ERLING', NULL),
(4, 2, 'courta_f@etna-alternance.net', 'Courtaux', 'Franck', 'pbkdf2:sha256:260000$jHxZmtbqP0vq7FZW$e6b19dc463559212b960f490d6702730c16f58f7509c38ea9f7e41a0e3531850', NULL, '882155', 1, NULL, NULL, NULL),
(5, 2, 'elhormij@gmail.com', 'El hormi', 'Jaouad', 'pbkdf2:sha256:260000$MReOmBI3mnlBKHmA$9ce6ec851469aa89a09676474adb6f5231027ee025e1a5b18b76ff415a95a5c1', NULL, '972173', 1, NULL, NULL, NULL),
(6, 0, 'courta_f2@etna-alternance.net', 'De Jesus Velez Pereira Real', 'Francisco', 'pbkdf2:sha256:260000$kMtNFAdUcROGYcoi$90d642098ae854491d6ad5fae4ea6ee5430beda85463d4236cfcabd654634765', NULL, '072777', 1, NULL, NULL, 2),
(7, 0, 'courta_f3@etna-alternance.net', 'Ouzzaouit', 'Muath', 'pbkdf2:sha256:260000$impdZlYJoZl4BLIk$85fdf032fa5fea5ae5106d032b2d2bf647a3a2965bbf5310d5f2b1a55a6041c9', NULL, '372259', 1, NULL, NULL, NULL),
(8, 0, 'courta_f4@etna-alternance.net', 'Boulin', ' Benjamin', 'pbkdf2:sha256:260000$WI8FnqaxN1RW4utr$f69bb606b8e642fa30c20363b4afe436d9682e5468ff9446abc8fba31dfc7de1', NULL, '106570', 1, NULL, NULL, NULL),
(9, 0, 'mokhta_s1@etna-alternance.net', 'Vy', 'Terence', 'pbkdf2:sha256:260000$GhdONN2x8GVn30jQ$f88f311e5642f281d5d6f17bfd384afdcb955f5e7c11841a5719ef244dfeafcc', NULL, '052562', 0, NULL, NULL, NULL),
(10, 0, 'mokhta_s1@etna-alternance.net', 'Djennah', 'Youcef', 'pbkdf2:sha256:260000$cJO4ancCZrMaCEgN$c5770c5c668060f32d3062ffc28c7b0831fce7b070bdea50c35f912805c959e9', NULL, '236657', 0, NULL, NULL, NULL),
(11, 2, 'kernin_b@etna-alternance.net', 'Kernin', 'Brandon', 'pbkdf2:sha256:260000$AGzcWlEoVaRtwpZS$e027be3cfdf5142e416e529610efc56916df83036813ea07ead082f1cd1b4f97', NULL, '157169', 1, 'Défenseur', 'Grand défenseur ', NULL),
(12, 2, 'acalhabi@gmail.com', 'Habi', 'Açal', 'pbkdf2:sha256:260000$EURGxi89Z1ApjmRk$68fa87ccb9658833202f7e80d5871977252d28d8afa09d05a05e7b32ab7d10bf', NULL, '716721', 1, NULL, NULL, NULL),
(13, 0, 'kerninbrandon@gmail.com', 'Fevrier', 'Matteo', 'pbkdf2:sha256:260000$FKyI9hzc4elhu4Nm$383e258272f988e6a7b663daf8134d444b74a81888a9f4b48c2ff99508de8fe3', NULL, '236324', 1, NULL, NULL, NULL),
(14, 0, 'aqwwqab@gmail.com', 'Berwick', 'Flavien', 'pbkdf2:sha256:260000$8WxqW6lRy9MfkIWa$d90646fae9c399f464b8a1949ed6fd8f8f6a7505a81bba4a99adc05eceda8189', NULL, '389083', 0, NULL, NULL, NULL),
(15, 0, 'brandon777290@gmail.com', 'Clain', 'Matthieu', 'pbkdf2:sha256:260000$QoUdStHvkhFfKMKw$7c2eea0eb7d88cfa0b74eafe91fd6d0466805bacc38f2f9bd63bed55d944badb', NULL, '619161', 0, NULL, NULL, NULL),
(16, 0, 'kernin_b1@etna-alternance.net', 'Migliardi', 'Enzo', 'pbkdf2:sha256:260000$9nnp9soq60BYAOPB$ae59314586ff109aaa8c782ac3e44c46baef6c2fde1be98523dea9f76cb14d61', NULL, '441560', 0, NULL, NULL, NULL),
(17, 0, 'kernin_b2@etna-alternance.net', 'Vanhove', 'Jeremy', 'pbkdf2:sha256:260000$sesN3pfxt5CSv1hS$2890d0cb11cfede95dc82c2f6049980bcf751ffdd07a6e0fea6880e4e0f67df7', NULL, '537798', 0, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `user_has_team`
--

DROP TABLE IF EXISTS `user_has_team`;
CREATE TABLE `user_has_team` (
  `team_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `user_has_team`
--

INSERT INTO `user_has_team` (`team_id`, `user_id`) VALUES
(6, 3),
(6, 4),
(6, 5),
(6, 6),
(6, 7),
(8, 5),
(8, 7),
(8, 3),
(8, 8),
(8, 4);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `complex`
--
ALTER TABLE `complex`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `match_played`
--
ALTER TABLE `match_played`
  ADD PRIMARY KEY (`id`),
  ADD KEY `match_complex_idx` (`complex_id`);

--
-- Index pour la table `pending`
--
ALTER TABLE `pending`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userpending_idx` (`user_id`);

--
-- Index pour la table `stats`
--
ALTER TABLE `stats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userstat` (`user_id`);

--
-- Index pour la table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `team_has_match_played`
--
ALTER TABLE `team_has_match_played`
  ADD KEY `matchid` (`match_id`),
  ADD KEY `teamid` (`team_id`);

--
-- Index pour la table `team_stats`
--
ALTER TABLE `team_stats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teamstats` (`team_id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `users_complex_idx` (`complex_id`);

--
-- Index pour la table `user_has_team`
--
ALTER TABLE `user_has_team`
  ADD KEY `team` (`team_id`),
  ADD KEY `user` (`user_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `complex`
--
ALTER TABLE `complex`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `match_played`
--
ALTER TABLE `match_played`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `pending`
--
ALTER TABLE `pending`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `stats`
--
ALTER TABLE `stats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `team`
--
ALTER TABLE `team`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `team_stats`
--
ALTER TABLE `team_stats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `match_played`
--
ALTER TABLE `match_played`
  ADD CONSTRAINT `match_complex` FOREIGN KEY (`complex_id`) REFERENCES `complex` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `pending`
--
ALTER TABLE `pending`
  ADD CONSTRAINT `userpending` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `stats`
--
ALTER TABLE `stats`
  ADD CONSTRAINT `userstat` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `team_has_match_played`
--
ALTER TABLE `team_has_match_played`
  ADD CONSTRAINT `matchid` FOREIGN KEY (`match_id`) REFERENCES `match_played` (`id`),
  ADD CONSTRAINT `teamid` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);

--
-- Contraintes pour la table `team_stats`
--
ALTER TABLE `team_stats`
  ADD CONSTRAINT `teamstats` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);

--
-- Contraintes pour la table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_complex` FOREIGN KEY (`complex_id`) REFERENCES `complex` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `user_has_team`
--
ALTER TABLE `user_has_team`
  ADD CONSTRAINT `team` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
