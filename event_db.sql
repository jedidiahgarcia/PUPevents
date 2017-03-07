-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 07, 2017 at 06:08 AM
-- Server version: 10.1.13-MariaDB
-- PHP Version: 5.6.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `event_db`
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
  `guestName` varchar(30) NOT NULL,
  `contactNumber` int(15) NOT NULL,
  `email` varchar(30) NOT NULL,
  `eventId` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `organizer`
--

CREATE TABLE `organizer` (
  `organizerId` int(10) NOT NULL,
  `organizerName` varchar(30) NOT NULL,
  `designation` varchar(20) NOT NULL,
  `contactNumber` int(15) NOT NULL,
  `email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  ADD KEY `eventId` (`eventId`);

--
-- Indexes for table `organizer`
--
ALTER TABLE `organizer`
  ADD PRIMARY KEY (`organizerId`);

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
