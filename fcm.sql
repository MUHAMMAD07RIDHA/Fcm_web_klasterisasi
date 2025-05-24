-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 22, 2024 at 02:08 PM
-- Server version: 8.0.30
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fcm`
--

-- --------------------------------------------------------

--
-- Table structure for table `data_penyakit`
--

CREATE TABLE `data_penyakit` (
  `id` int NOT NULL,
  `puskesmas_kecamatan` varchar(255) NOT NULL,
  `sasaran_balita_eppgbm` int DEFAULT NULL,
  `balita_entry_2023` int DEFAULT NULL,
  `persentase` int DEFAULT NULL,
  `stunting` int DEFAULT NULL,
  `wasting` int DEFAULT NULL,
  `underweight` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_penyakit`
--

INSERT INTO `data_penyakit` (`id`, `puskesmas_kecamatan`, `sasaran_balita_eppgbm`, `balita_entry_2023`, `persentase`, `stunting`, `wasting`, `underweight`) VALUES
(1, 'SAWANG', 18744, 16357, 87, 1035, 361, 2195),
(2, 'NISAM', 20328, 18254, 90, 1128, 1143, 1417),
(3, 'BANDA BARO', 8606, 7353, 85, 368, 59, 741),
(4, 'KUTA MAKMUR', 28992, 20563, 71, 2773, 1529, 3160),
(5, 'SIMPANG KRAMAT', 10263, 10047, 98, 822, 478, 779),
(6, 'SYAMTALIRA BAYU', 22812, 22400, 98, 239, 265, 601),
(7, 'GEUREUDONG PASE', 7255, 6543, 90, 717, 401, 684),
(8, 'MEURAH MULIA', 19848, 13569, 68, 1938, 1241, 1768),
(9, 'MATANGKULI', 14160, 12226, 86, 424, 296, 1398),
(10, 'PAYA BAKONG', 17076, 14743, 86, 790, 624, 753),
(11, 'PIRAK TIMU', 10149, 7613, 75, 2222, 641, 2061),
(12, 'COT GIREK', 17802, 16664, 94, 315, 213, 366),
(13, 'TANAH JAMBO AYE', 18218, 16778, 92, 794, 533, 657),
(14, 'LHOK BEURINGEN', 9168, 5155, 56, 505, 475, 657),
(15, 'LANGKAHAN', 10980, 9287, 85, 614, 260, 485),
(16, 'SIMPANG TIGA', 4680, 3764, 80, 497, 257, 496),
(17, 'SEUNUDON', 17976, 17049, 95, 140, 651, 899),
(18, 'BLANG GEULUMPANG', 6514, 6260, 96, 354, 138, 322),
(19, 'BAKTIYA', 29424, 24567, 83, 628, 488, 300),
(20, 'BAKTIYA BARAT', 17352, 15156, 87, 618, 665, 1171),
(21, 'LHOKSUKON', 16949, 14913, 88, 1628, 438, 967),
(22, 'BUKET HAGU', 17529, 12973, 74, 877, 1160, 1367),
(23, 'TANAH LUAS', 28102, 23035, 82, 590, 353, 457),
(24, 'NIBONG', 9634, 8677, 90, 340, 381, 329),
(25, 'SAMUDERA', 19956, 17681, 89, 262, 1085, 1259),
(26, 'SYAMTALIRA ARON', 19332, 17881, 92, 1513, 460, 1555),
(27, 'TANAH PASIR', 11195, 10528, 94, 550, 567, 858),
(28, 'LAPANG', 9761, 7657, 78, 828, 390, 861),
(29, 'MUARA BATU', 24852, 24236, 98, 475, 469, 610),
(30, 'DEWANTARA', 32868, 30376, 92, 1567, 1124, 1733),
(31, 'BABAH BULOH', 12744, 11089, 87, 828, 963, 1576),
(32, 'NISAM ANTARA', 11339, 10682, 94, 661, 1102, 1023);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'Admin', 'scrypt:32768:8:1$MqLgzWxNyZ1W7sXH$b6073a4362b6db8a0f3f9abb56bced12e321377ad756dc111f55e54d2f0ce8555214f5d0e0fb52895e2fa91639ec777694071227191b0144c64a834f174fa3b1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `data_penyakit`
--
ALTER TABLE `data_penyakit`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `data_penyakit`
--
ALTER TABLE `data_penyakit`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
