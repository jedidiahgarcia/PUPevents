-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 16, 2017 at 05:57 AM
-- Server version: 5.6.26-log
-- PHP Version: 7.0.4
-- Host: 127.0.0.1
-- Generation Time: Mar 16, 2017 at 05:13 AM
-- Server version: 10.1.13-MariaDB
-- PHP Version: 5.6.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pupevents`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `getAllEvents` ()  BEGIN
	Select eventId, eventName, eventDate, startTime, endTime from event;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `getNextThree` ()  BEGIN
	Select a.eventName,
		a.eventDate,
        a.startTime,
        a.endTime,
        c.venueName
        from event a, venue b, venueinfo c
        where
        a.eventDate > NOW() AND
		a.startTime > NOW() AND
        a.venueId = b.venueId AND
        b.venueInfoId = c.venueInfoId
        LIMIT 3;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `eventId` int(10) NOT NULL,
  `eventName` varchar(30) NOT NULL,
  `eventDesc` varchar(100) NOT NULL,
  `eventDate` date NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  `venueId` int(10) NOT NULL,
  `organizerId` int(10) NOT NULL,
  `peopleAlloc` int(11) NOT NULL,
  `status` varchar(15) NOT NULL DEFAULT 'reserved'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`eventId`, `eventName`, `eventDesc`, `eventDate`, `startTime`, `endTime`, `venueId`, `organizerId`, `peopleAlloc`, `status`) VALUES
(4, 'PUP Operation Tuli', 'Abutin ang pangarap na minsang naunahan ng takot HAHAHA', '2017-03-17', '15:00:00', '16:00:00', 2, 1, 50, 'reserved'),
(5, 'PUP Graduation', 'k', '2017-03-17', '14:30:00', '16:00:00', 2, 2, 6500, 'published');

-- --------------------------------------------------------

--
-- Table structure for table `guest`
--

CREATE TABLE `guest` (
  `guestId` int(10) NOT NULL,
  `userId` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guest`
--

INSERT INTO `guest` (`guestId`, `userId`) VALUES
(2, 'xcxcxc');

-- --------------------------------------------------------

--
-- Table structure for table `organizer`
--

CREATE TABLE `organizer` (
  `organizerId` int(11) NOT NULL,
  `userId` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `organizer`
--

INSERT INTO `organizer` (`organizerId`, `userId`) VALUES
(1, '2014-05666-MN-0'),
(2, '2014-05666-MN-0');

-- --------------------------------------------------------

--
-- Table structure for table `samp`
--

CREATE TABLE `samp` (
  `id` int(5) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `samp`
--

INSERT INTO `samp` (`id`, `name`) VALUES
(9, 'reserve');

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
('2014-01559-MN-0', 'Jay Leonarth', 'Gecarane', '09224750210', 'student', 'jayleonarth_gecarane@yahoo.com', 'd3cada00b2f6eafc5ec4f6c2cb81091ab7eef31d92345f73b48dc381a239af29'),
('2014-05666-MN-0', 'Redentor', 'Periabras', '09093291283', 'student', 'redperiabras@gmail.com', '6eeb9d2bdd07689712c90334d568775b9f1cb1f9bcb9c1ea86ce8acfb7ab8e83');

-- --------------------------------------------------------

--
-- Table structure for table `venue`
--

CREATE TABLE `venue` (
  `venueId` int(10) NOT NULL,
  `venueInfoId` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `venue`
--

INSERT INTO `venue` (`venueId`, `venueInfoId`) VALUES
(2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `venueinfo`
--

CREATE TABLE `venueinfo` (
  `venueInfoId` int(10) NOT NULL,
  `venueName` varchar(30) NOT NULL,
  `capacity` int(11) NOT NULL DEFAULT '0',
  `cost` double NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `venueinfo`
--

INSERT INTO `venueinfo` (`venueInfoId`, `venueName`, `capacity`, `cost`) VALUES
(1, 'Bulwagang Balagtas', 50, 500),
(2, 'PUP Gymnasium', 400, 200),
(3, 'Ninoy Aquino Hall', 200, 100),
(4, 'Freedom Park', 200, 50),
(5, 'PUP Theater', 500, 200);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`eventId`),
  ADD KEY `venueId` (`venueId`),
  ADD KEY `organzerId` (`organizerId`);

--
-- Indexes for table `guest`
--
ALTER TABLE `guest`
  ADD PRIMARY KEY (`guestId`),
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
  ADD UNIQUE KEY `venueInfoId` (`venueInfoId`);

--
-- Indexes for table `venueinfo`
--
ALTER TABLE `venueinfo`
  ADD PRIMARY KEY (`venueInfoId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `eventId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `organizer`
--
ALTER TABLE `organizer`
  MODIFY `organizerId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `venue`
--
ALTER TABLE `venue`
  MODIFY `venueId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `venueinfo`
--
ALTER TABLE `venueinfo`
  MODIFY `venueInfoId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_2` FOREIGN KEY (`organizerId`) REFERENCES `organizer` (`organizerId`),
  ADD CONSTRAINT `event_ibfk_3` FOREIGN KEY (`venueId`) REFERENCES `venue` (`venueId`);

--
-- Constraints for table `venue`
--
ALTER TABLE `venue`
  ADD CONSTRAINT `venue_ibfk_2` FOREIGN KEY (`venueInfoId`) REFERENCES `venueinfo` (`venueInfoId`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
