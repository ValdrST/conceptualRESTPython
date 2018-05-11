-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-05-2018 a las 20:46:40
-- Versión del servidor: 10.1.30-MariaDB
-- Versión de PHP: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pruebasy`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bajas_temporales`
--

CREATE TABLE `bajas_temporales` (
  `idBAJAS_TEMPORALES` int(11) NOT NULL,
  `CUENTA` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cred_sem_carr_pln`
--

CREATE TABLE `cred_sem_carr_pln` (
  `idCRED_SEM_CARR_PLN` int(11) NOT NULL,
  `CUENTA` varchar(45) DEFAULT NULL,
  `ASEM01` varchar(45) DEFAULT NULL,
  `ASEM02` varchar(45) DEFAULT NULL,
  `ASEM03` varchar(45) DEFAULT NULL,
  `ASEM04` varchar(45) DEFAULT NULL,
  `ASEM05` varchar(45) DEFAULT NULL,
  `ASEM06` varchar(45) DEFAULT NULL,
  `ASEM07` varchar(45) DEFAULT NULL,
  `ASEM08` varchar(45) DEFAULT NULL,
  `ASEM09` varchar(45) DEFAULT NULL,
  `ASEM10` varchar(45) DEFAULT NULL,
  `CARRERA` varchar(45) DEFAULT NULL,
  `PLN` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cred_sem_carr_pln`
--

INSERT INTO `cred_sem_carr_pln` (`idCRED_SEM_CARR_PLN`, `CUENTA`, `ASEM01`, `ASEM02`, `ASEM03`, `ASEM04`, `ASEM05`, `ASEM06`, `ASEM07`, `ASEM08`, `ASEM09`, `ASEM10`, `CARRERA`, `PLN`) VALUES
(1, '314144799', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200', '110', '2016');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dir_alumnos_dgae`
--

CREATE TABLE `dir_alumnos_dgae` (
  `CUENTA` varchar(45) NOT NULL,
  `CARRERA` varchar(45) DEFAULT NULL,
  `PLAN_DGAE` varchar(45) DEFAULT NULL,
  `REGISTRO` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `dir_alumnos_dgae`
--

INSERT INTO `dir_alumnos_dgae` (`CUENTA`, `CARRERA`, `PLAN_DGAE`, `REGISTRO`) VALUES
('314144799', '110', '1412', '6');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudia_seriacion`
--

CREATE TABLE `estudia_seriacion` (
  `idESTUDIA_SERIACION` int(11) NOT NULL,
  `CUENTA` varchar(45) DEFAULT NULL,
  `CARRERA` varchar(45) DEFAULT NULL,
  `PLN_DGAE` varchar(45) DEFAULT NULL,
  `PLN` varchar(45) DEFAULT NULL,
  `REGISTRO` varchar(45) DEFAULT NULL,
  `AVANCE` varchar(45) DEFAULT NULL,
  `PROMEDIO` varchar(45) DEFAULT NULL,
  `CREDITOS_CUBIERTOS` varchar(45) DEFAULT NULL,
  `ULTIMO_CURSADO` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `estudia_seriacion`
--

INSERT INTO `estudia_seriacion` (`idESTUDIA_SERIACION`, `CUENTA`, `CARRERA`, `PLN_DGAE`, `PLN`, `REGISTRO`, `AVANCE`, `PROMEDIO`, `CREDITOS_CUBIERTOS`, `ULTIMO_CURSADO`) VALUES
(1, '314144799', '110', '1412', '2016', '7', '70', '7.8', '200', '6');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `periodo`
--

CREATE TABLE `periodo` (
  `idPERIODO` int(11) NOT NULL,
  `ANIO` varchar(45) DEFAULT NULL,
  `SEMESTRE` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `periodo`
--

INSERT INTO `periodo` (`idPERIODO`, `ANIO`, `SEMESTRE`) VALUES
(1, '2018', '2');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bajas_temporales`
--
ALTER TABLE `bajas_temporales`
  ADD PRIMARY KEY (`idBAJAS_TEMPORALES`),
  ADD KEY `FK_BAJAS_CUENTA_idx` (`CUENTA`);

--
-- Indices de la tabla `cred_sem_carr_pln`
--
ALTER TABLE `cred_sem_carr_pln`
  ADD PRIMARY KEY (`idCRED_SEM_CARR_PLN`),
  ADD KEY `FK_CRED_ALUM_idx` (`CUENTA`);

--
-- Indices de la tabla `dir_alumnos_dgae`
--
ALTER TABLE `dir_alumnos_dgae`
  ADD PRIMARY KEY (`CUENTA`);

--
-- Indices de la tabla `estudia_seriacion`
--
ALTER TABLE `estudia_seriacion`
  ADD PRIMARY KEY (`idESTUDIA_SERIACION`),
  ADD KEY `FK_ESTUDIA_DIR_idx` (`CUENTA`);

--
-- Indices de la tabla `periodo`
--
ALTER TABLE `periodo`
  ADD PRIMARY KEY (`idPERIODO`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bajas_temporales`
--
ALTER TABLE `bajas_temporales`
  MODIFY `idBAJAS_TEMPORALES` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cred_sem_carr_pln`
--
ALTER TABLE `cred_sem_carr_pln`
  MODIFY `idCRED_SEM_CARR_PLN` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `estudia_seriacion`
--
ALTER TABLE `estudia_seriacion`
  MODIFY `idESTUDIA_SERIACION` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `periodo`
--
ALTER TABLE `periodo`
  MODIFY `idPERIODO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `bajas_temporales`
--
ALTER TABLE `bajas_temporales`
  ADD CONSTRAINT `FK_BAJAS_CUENTA` FOREIGN KEY (`CUENTA`) REFERENCES `dir_alumnos_dgae` (`CUENTA`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `cred_sem_carr_pln`
--
ALTER TABLE `cred_sem_carr_pln`
  ADD CONSTRAINT `FK_CRED_ALUM` FOREIGN KEY (`CUENTA`) REFERENCES `dir_alumnos_dgae` (`CUENTA`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `estudia_seriacion`
--
ALTER TABLE `estudia_seriacion`
  ADD CONSTRAINT `FK_ESTUDIA_DIR` FOREIGN KEY (`CUENTA`) REFERENCES `dir_alumnos_dgae` (`CUENTA`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
