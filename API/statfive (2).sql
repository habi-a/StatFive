-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  mer. 24 juil. 2019 à 17:48
-- Version du serveur :  10.1.40-MariaDB
-- Version de PHP :  7.3.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `statfive`
--

-- --------------------------------------------------------

--
-- Structure de la table `match_played`
--

CREATE TABLE `match_played` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `duration` varchar(255) NOT NULL,
  `ground` int(11) NOT NULL,
  `path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `match_played`
--

INSERT INTO `match_played` (`id`, `name`, `duration`, `ground`, `path`) VALUES
(1, '', '00:00:00', 1, ''),
(2, '', '12:00:00', 2, 'chemin'),
(3, '', '14:25', 0, '/mnt/c/Users/nour/Documents/ProjetLib/Git/StatFive/video/myMatch.mp4'),
(4, 'Match2019-07-24', '10:41', 0, '/mnt/c/Users/nour/Documents/ProjetLib/Git/StatFive/video/myMatch2019-07-24.mp4');

-- --------------------------------------------------------

--
-- Structure de la table `stats`
--

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

CREATE TABLE `team` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `team`
--

INSERT INTO `team` (`id`, `name`) VALUES
(1, 'Paris'),
(2, 'Real');

-- --------------------------------------------------------

--
-- Structure de la table `team_has_match_played`
--

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
(4, 1, 2, 50, 'blue', 1),
(4, 2, 3, 50, 'red', 1);

-- --------------------------------------------------------

--
-- Structure de la table `team_stats`
--

CREATE TABLE `team_stats` (
  `id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `but` int(11) NOT NULL,
  `passe` int(11) NOT NULL,
  `km` float NOT NULL,
  `possesion` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `team_stats`
--

INSERT INTO `team_stats` (`id`, `team_id`, `but`, `passe`, `km`, `possesion`) VALUES
(1, 1, 2, 30, 14.5, 40),
(2, 2, 4, 50, 13, 60);

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `firstname` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `user_has_team`
--

CREATE TABLE `user_has_team` (
  `team_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `match_played`
--
ALTER TABLE `match_played`
  ADD PRIMARY KEY (`id`);

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
  ADD PRIMARY KEY (`id`);

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
-- AUTO_INCREMENT pour la table `match_played`
--
ALTER TABLE `match_played`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `stats`
--
ALTER TABLE `stats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `team`
--
ALTER TABLE `team`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `team_stats`
--
ALTER TABLE `team_stats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

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
-- Contraintes pour la table `user_has_team`
--
ALTER TABLE `user_has_team`
  ADD CONSTRAINT `team` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
