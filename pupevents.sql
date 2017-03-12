-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 12, 2017 at 03:07 PM
-- Server version: 5.6.26-log
-- PHP Version: 7.0.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pupevents`
--

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `eventId` int(10) NOT NULL,
  `eventName` varchar(30) NOT NULL,
  `dateTime` datetime(6) NOT NULL,
  `venueId` int(10) NOT NULL,
  `organzerId` int(10) NOT NULL,
  `guestId` int(10) NOT NULL,
  `eventDesc` varchar(40) NOT NULL,
  `status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `guest`
--

CREATE TABLE `guest` (
  `guestId` int(10) NOT NULL,
  `userId` varchar(15) NOT NULL,
  `eventId` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `organizer`
--

CREATE TABLE `organizer` (
  `organizerId` int(11) NOT NULL,
  `userId` varchar(20) NOT NULL,
  `eventId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` varchar(15) NOT NULL COMMENT 'Student of Employee Number',
  `firstName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) DEFAULT NULL,
  `contactNumber` varchar(45) DEFAULT NULL,
  `designation` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `firstName`, `lastName`, `contactNumber`, `designation`, `email`, `password`) VALUES
('2014-05666-MN-0', 'Redentor', 'Periabras', '09093291283', 'student', 'redperiabras@gmail.com', '6eeb9d2bdd07689712c90334d568775b9f1cb1f9bcb9c1ea86ce8acfb7ab8e83');

-- --------------------------------------------------------

--
-- Table structure for table `venue`
--

CREATE TABLE `venue` (
  `venueId` int(10) NOT NULL,
  `venueInfoId` int(10) NOT NULL,
  `eventId` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `venueinfo`
--

CREATE TABLE `venueinfo` (
  `venueInfoId` int(10) NOT NULL,
  `venueName` varchar(30) NOT NULL,
  `cost` double NOT NULL,
  `equipment` varchar(20) NOT NULL,
  `venueDesc` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`eventId`),
  ADD KEY `venueId` (`venueId`),
  ADD KEY `organzerId` (`organzerId`),
  ADD KEY `guestId` (`guestId`);

--
-- Indexes for table `guest`
--
ALTER TABLE `guest`
  ADD PRIMARY KEY (`guestId`),
  ADD KEY `eventId` (`eventId`),
  ADD KEY `userId_idx` (`userId`),
  ADD KEY `userId` (`userId`);

--
-- Indexes for table `organizer`
--
ALTER TABLE `organizer`
  ADD PRIMARY KEY (`organizerId`),
  ADD KEY `user_idx` (`userId`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `venue`
--
ALTER TABLE `venue`
  ADD PRIMARY KEY (`venueId`),
  ADD UNIQUE KEY `venueInfoId` (`venueInfoId`),
  ADD KEY `eventId` (`eventId`),
  ADD KEY `eventId_2` (`eventId`);

--
-- Indexes for table `venueinfo`
--
ALTER TABLE `venueinfo`
  ADD PRIMARY KEY (`venueInfoId`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`venueId`) REFERENCES `venue` (`venueId`),
  ADD CONSTRAINT `event_ibfk_2` FOREIGN KEY (`organzerId`) REFERENCES `organizer` (`organizerId`),
  ADD CONSTRAINT `event_ibfk_3` FOREIGN KEY (`guestId`) REFERENCES `guest` (`guestId`);

--
-- Constraints for table `guest`
--
ALTER TABLE `guest`
  ADD CONSTRAINT `guest_ibfk_1` FOREIGN KEY (`eventId`) REFERENCES `event` (`eventId`);

--
-- Constraints for table `venue`
--
ALTER TABLE `venue`
  ADD CONSTRAINT `venue_ibfk_1` FOREIGN KEY (`eventId`) REFERENCES `event` (`eventId`),
  ADD CONSTRAINT `venue_ibfk_2` FOREIGN KEY (`venueInfoId`) REFERENCES `venueinfo` (`venueInfoId`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
