-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2023 at 05:21 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lms_python`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `adminID` int(8) NOT NULL,
  `user_type` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `middle_initial` varchar(1) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`adminID`, `user_type`, `first_name`, `last_name`, `middle_initial`, `username`, `password`) VALUES
(4, 'Admin', 'Admin', 'Admin', 'A', 'admin', '8b9a763c42080f2f32ad5523a1b03648caf91ac387b6cbf5fef530431dcdc7ec'),
(5, 'Staff', 'Staff', 'Staff', 'S', 'staff', '4ddc032185b17295d06dc09edae4623d45375ebed895e422561db847450328c8'),
(8, 'Staff', 'asd', 'asd', 'a', 'asd', '7423cca07cd0b7278771079eec9fa5b30c80db1e460792badbda03d90de21e25');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `bookID` int(8) NOT NULL,
  `accession_no` varchar(255) NOT NULL,
  `categoryID` int(8) NOT NULL,
  `author` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`bookID`, `accession_no`, `categoryID`, `author`, `title`, `date_created`) VALUES
(111, '123433', 15, 'Dr. Jose Rizal', 'El Filibusterismo', '2023-06-23 08:11:25'),
(112, '111111', 16, 'Lao Tzu', 'Java Programming', '2023-06-23 08:13:49'),
(113, '222222', 16, 'Linmui P.', 'Flutter Development', '2023-06-23 08:14:24'),
(114, '123323', 15, 'Dr. Jose Rizal', 'Noli Mi Tangere', '2023-06-23 08:15:44'),
(115, '432155', 23, 'Hectar Garcia', 'The Mountain is You', '2023-06-23 08:16:29'),
(116, '123466', 15, 'George Orwell', '1984', '2023-06-23 08:26:51'),
(117, '432156', 15, 'Harper Lee', 'To Kill a Mockingbird', '2023-06-23 08:27:11'),
(118, '321222', 16, 'F. Scott Fitzgerald', 'The Great Gatsby', '2023-06-23 08:27:34'),
(119, '123422', 15, 'Jane Austen', 'Pride and Prejudice', '2023-06-23 08:27:54'),
(120, '222332', 16, 'J.D. Salinger', 'The Catcher in the Rye', '2023-06-23 08:28:18'),
(121, '444455', 16, 'C.S. Lewis', 'The Chronicles of Narnia', '2023-06-23 08:28:37'),
(122, '232234', 23, 'Aldous Huxley', 'Brave New World', '2023-06-23 08:28:53'),
(123, '565654', 23, 'Herman Melville', 'Moby-Deck', '2023-06-23 08:29:14');

-- --------------------------------------------------------

--
-- Table structure for table `borrowed_books`
--

CREATE TABLE `borrowed_books` (
  `borrowed_bookID` int(8) NOT NULL,
  `userID` int(8) NOT NULL,
  `bookID` int(8) NOT NULL,
  `date_issued` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `borrowed_books`
--

INSERT INTO `borrowed_books` (`borrowed_bookID`, `userID`, `bookID`, `date_issued`) VALUES
(30, 17, 112, '2023-12-16 10:37:17'),
(31, 17, 113, '2023-12-16 10:38:29'),
(32, 17, 120, '2023-12-16 10:39:15');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `categoryID` int(8) NOT NULL,
  `category_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`categoryID`, `category_name`) VALUES
(15, 'General Education'),
(16, 'BSIT'),
(23, 'Senior High'),
(29, 'Engineeeer');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `reportID` int(8) NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `new_arrival` int(8) NOT NULL,
  `total_fines` int(8) NOT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`reportID`, `from_date`, `to_date`, `new_arrival`, `total_fines`, `date_created`) VALUES
(12, '2023-06-01', '2023-06-30', 13, 0, '2023-06-23 14:51:05');

-- --------------------------------------------------------

--
-- Table structure for table `returned_books`
--

CREATE TABLE `returned_books` (
  `returned_bookID` int(8) NOT NULL,
  `userID` int(8) NOT NULL,
  `bookID` int(8) NOT NULL,
  `book_condition` varchar(255) NOT NULL,
  `remarks` varchar(255) NOT NULL,
  `date_issued` datetime NOT NULL,
  `date_returned` datetime NOT NULL DEFAULT current_timestamp(),
  `fines` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userID` int(8) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `middle_initial` varchar(255) NOT NULL,
  `user_school_id` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userID`, `first_name`, `last_name`, `middle_initial`, `user_school_id`, `username`, `password`) VALUES
(5, 'student', 'student', 's', '2020-2020', 'student', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54'),
(16, 'student', 'student', 's', '1020-03030', 'student@gmail.com', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54'),
(17, 'test', 'test', 't', '2020-03030', 'test@gmail.com', 'b2a1f4fd0a460606b34c8913e2981dac8d2e283d778aba586c416ee2629bfa54');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adminID`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`bookID`),
  ADD KEY `categoryID` (`categoryID`);

--
-- Indexes for table `borrowed_books`
--
ALTER TABLE `borrowed_books`
  ADD PRIMARY KEY (`borrowed_bookID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `bookID` (`bookID`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`categoryID`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`reportID`);

--
-- Indexes for table `returned_books`
--
ALTER TABLE `returned_books`
  ADD PRIMARY KEY (`returned_bookID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `bookID` (`bookID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `adminID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `bookID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=131;

--
-- AUTO_INCREMENT for table `borrowed_books`
--
ALTER TABLE `borrowed_books`
  MODIFY `borrowed_bookID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `categoryID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `reportID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `returned_books`
--
ALTER TABLE `returned_books`
  MODIFY `returned_bookID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
