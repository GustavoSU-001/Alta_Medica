-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-11-2025 a las 16:17:43
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `alta_medica_2025`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alergia_paciente`
--

CREATE TABLE `alergia_paciente` (
  `id_alergia_paciente` int(11) NOT NULL,
  `run_paciente` varchar(12) NOT NULL,
  `id_tipo_alergia` int(11) NOT NULL,
  `severidad` varchar(50) DEFAULT NULL,
  `fecha_deteccion` date DEFAULT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alta_medica`
--

CREATE TABLE `alta_medica` (
  `id_alta_medica` int(11) NOT NULL,
  `run_paciente` varchar(12) NOT NULL,
  `run_especialista` varchar(12) NOT NULL,
  `id_hospitalizacion` int(11) DEFAULT NULL,
  `tipo_formulario` varchar(20) NOT NULL DEFAULT '',
  `numero_certificado` varchar(50) NOT NULL,
  `fecha_emision_certificado` date NOT NULL,
  `codigo_unico_nacional` varchar(20) DEFAULT NULL,
  `id_calificacion` int(11) DEFAULT NULL,
  `detalle_calificacion` text DEFAULT NULL,
  `fecha_diat_diep` date DEFAULT NULL,
  `es_menor_edad` tinyint(1) NOT NULL DEFAULT 0,
  `dependencia_parcial_total` tinyint(1) NOT NULL DEFAULT 0,
  `discapacidad` tinyint(1) NOT NULL DEFAULT 0,
  `persona_mayor` tinyint(1) NOT NULL DEFAULT 0,
  `otra_condicion` text DEFAULT NULL,
  `resp_legal_nombres` varchar(150) DEFAULT NULL,
  `resp_legal_rut` varchar(12) DEFAULT NULL,
  `resp_legal_direccion` varchar(255) DEFAULT NULL,
  `resp_legal_comuna` varchar(100) DEFAULT NULL,
  `resp_legal_fono` varchar(20) DEFAULT NULL,
  `empleador_razon_social` varchar(100) DEFAULT NULL,
  `empleador_rut` varchar(12) DEFAULT NULL,
  `empleador_direccion` varchar(255) DEFAULT NULL,
  `empleador_comuna` varchar(100) DEFAULT NULL,
  `id_motivo_alta` int(11) DEFAULT NULL,
  `detalle_motivo` text DEFAULT NULL,
  `presume_invalidez` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_alta` date NOT NULL,
  `firma_medico` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `area`
--

CREATE TABLE `area` (
  `id_area` int(11) NOT NULL,
  `nombre_area` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `camilla`
--

CREATE TABLE `camilla` (
  `id_camilla` int(11) NOT NULL,
  `id_tipo_camilla` int(11) NOT NULL,
  `nombre_camilla` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalogo_calificacion_alta`
--

CREATE TABLE `catalogo_calificacion_alta` (
  `id_calificacion` int(11) NOT NULL,
  `tipo_formulario` varchar(20) NOT NULL,
  `nombre_calificacion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalogo_motivo_alta`
--

CREATE TABLE `catalogo_motivo_alta` (
  `id_motivo_alta` int(11) NOT NULL,
  `descripcion_motivo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `especialista`
--

CREATE TABLE `especialista` (
  `run_especialista` varchar(12) NOT NULL,
  `id_area` int(11) NOT NULL,
  `id_estado_espec` int(11) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `fono` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_en_consulta`
--

CREATE TABLE `estado_en_consulta` (
  `id_estado_consulta` int(11) NOT NULL,
  `nombre_estado_consulta` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_especialista`
--

CREATE TABLE `estado_especialista` (
  `id_estado_espec` int(11) NOT NULL,
  `nombre_estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_hospitalizacion`
--

CREATE TABLE `estado_hospitalizacion` (
  `id_estado_hosp` int(11) NOT NULL,
  `nombre_estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_salud`
--

CREATE TABLE `estado_salud` (
  `id_estado_salud` int(11) NOT NULL,
  `nombre_estado_salud` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examen`
--

CREATE TABLE `examen` (
  `id_examen` int(11) NOT NULL,
  `id_registro_med` int(11) DEFAULT NULL,
  `id_tipo_examen` int(11) DEFAULT NULL,
  `nombre_examen` varchar(255) DEFAULT NULL,
  `detalle` text DEFAULT NULL,
  `resultado` text DEFAULT NULL,
  `fecha_examen` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero`
--

CREATE TABLE `genero` (
  `id_genero` int(11) NOT NULL,
  `nombre_genero` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupo_sanguineo`
--

CREATE TABLE `grupo_sanguineo` (
  `nombre_grupo` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hospitalizacion`
--

CREATE TABLE `hospitalizacion` (
  `id_hospitalizacion` int(11) NOT NULL,
  `run_paciente` varchar(12) NOT NULL,
  `run_especialista` varchar(12) DEFAULT NULL,
  `id_camilla` int(11) DEFAULT NULL,
  `id_estado_hospitalizacion` int(11) DEFAULT NULL,
  `motivo` text DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `fecha_ingreso` datetime NOT NULL,
  `fecha_estimada_alta` date DEFAULT NULL,
  `fecha_real_alta` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paciente`
--

CREATE TABLE `paciente` (
  `run` varchar(12) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `fecha_nac` date DEFAULT NULL,
  `id_genero` int(11) DEFAULT NULL,
  `grupo_sang` varchar(5) DEFAULT NULL,
  `id_estado_salud` int(11) DEFAULT NULL,
  `fono` varchar(20) DEFAULT NULL,
  `fono_alt` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_medico`
--

CREATE TABLE `registro_medico` (
  `id_registro_med` int(11) NOT NULL,
  `run_paciente` varchar(12) NOT NULL,
  `run_especialista` varchar(12) NOT NULL,
  `fecha_hora_atencion` datetime NOT NULL,
  `id_estado_en_consulta` int(11) DEFAULT NULL,
  `motivo_consulta` text DEFAULT NULL,
  `diagnostico` text DEFAULT NULL,
  `resultado_consulta` text DEFAULT NULL,
  `notas` text DEFAULT NULL,
  `peso` decimal(5,2) DEFAULT NULL,
  `altura` decimal(5,2) DEFAULT NULL,
  `signos_vitales` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_alergia`
--

CREATE TABLE `tipo_alergia` (
  `id_tipo_alergia` int(11) NOT NULL,
  `nombre_alergia` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_camilla`
--

CREATE TABLE `tipo_camilla` (
  `id_tipo_camilla` int(11) NOT NULL,
  `nombre_tipo_camilla` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_examen`
--

CREATE TABLE `tipo_examen` (
  `id_tipo_examen` int(11) NOT NULL,
  `tipo_examen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alergia_paciente`
--
ALTER TABLE `alergia_paciente`
  ADD PRIMARY KEY (`id_alergia_paciente`),
  ADD UNIQUE KEY `unique_alergia_paciente` (`run_paciente`,`id_tipo_alergia`),
  ADD KEY `fk_ap_tipo` (`id_tipo_alergia`);

--
-- Indices de la tabla `alta_medica`
--
ALTER TABLE `alta_medica`
  ADD PRIMARY KEY (`id_alta_medica`),
  ADD KEY `fk_alta_paciente` (`run_paciente`),
  ADD KEY `fk_alta_especialista` (`run_especialista`),
  ADD KEY `fk_alta_hospitalizacion` (`id_hospitalizacion`),
  ADD KEY `fk_alta_calificacion` (`id_calificacion`),
  ADD KEY `fk_alta_motivo` (`id_motivo_alta`);

--
-- Indices de la tabla `area`
--
ALTER TABLE `area`
  ADD PRIMARY KEY (`id_area`);

--
-- Indices de la tabla `camilla`
--
ALTER TABLE `camilla`
  ADD PRIMARY KEY (`id_camilla`),
  ADD KEY `fk_camilla_tipo` (`id_tipo_camilla`);

--
-- Indices de la tabla `catalogo_calificacion_alta`
--
ALTER TABLE `catalogo_calificacion_alta`
  ADD PRIMARY KEY (`id_calificacion`);

--
-- Indices de la tabla `catalogo_motivo_alta`
--
ALTER TABLE `catalogo_motivo_alta`
  ADD PRIMARY KEY (`id_motivo_alta`);

--
-- Indices de la tabla `especialista`
--
ALTER TABLE `especialista`
  ADD PRIMARY KEY (`run_especialista`),
  ADD KEY `fk_esp_area` (`id_area`),
  ADD KEY `fk_esp_estado` (`id_estado_espec`);

--
-- Indices de la tabla `estado_en_consulta`
--
ALTER TABLE `estado_en_consulta`
  ADD PRIMARY KEY (`id_estado_consulta`);

--
-- Indices de la tabla `estado_especialista`
--
ALTER TABLE `estado_especialista`
  ADD PRIMARY KEY (`id_estado_espec`);

--
-- Indices de la tabla `estado_hospitalizacion`
--
ALTER TABLE `estado_hospitalizacion`
  ADD PRIMARY KEY (`id_estado_hosp`);

--
-- Indices de la tabla `estado_salud`
--
ALTER TABLE `estado_salud`
  ADD PRIMARY KEY (`id_estado_salud`);

--
-- Indices de la tabla `examen`
--
ALTER TABLE `examen`
  ADD PRIMARY KEY (`id_examen`),
  ADD KEY `fk_examen_registro` (`id_registro_med`),
  ADD KEY `fk_examen_tipo` (`id_tipo_examen`);

--
-- Indices de la tabla `genero`
--
ALTER TABLE `genero`
  ADD PRIMARY KEY (`id_genero`);

--
-- Indices de la tabla `grupo_sanguineo`
--
ALTER TABLE `grupo_sanguineo`
  ADD PRIMARY KEY (`nombre_grupo`);

--
-- Indices de la tabla `hospitalizacion`
--
ALTER TABLE `hospitalizacion`
  ADD PRIMARY KEY (`id_hospitalizacion`),
  ADD KEY `fk_hosp_paciente` (`run_paciente`),
  ADD KEY `fk_hosp_especialista` (`run_especialista`),
  ADD KEY `fk_hosp_camilla` (`id_camilla`),
  ADD KEY `fk_hosp_estado` (`id_estado_hospitalizacion`);

--
-- Indices de la tabla `paciente`
--
ALTER TABLE `paciente`
  ADD PRIMARY KEY (`run`),
  ADD KEY `fk_paciente_genero` (`id_genero`),
  ADD KEY `fk_paciente_grupo` (`grupo_sang`),
  ADD KEY `fk_paciente_estado` (`id_estado_salud`);

--
-- Indices de la tabla `registro_medico`
--
ALTER TABLE `registro_medico`
  ADD PRIMARY KEY (`id_registro_med`),
  ADD KEY `fk_rm_paciente` (`run_paciente`),
  ADD KEY `fk_rm_especialista` (`run_especialista`),
  ADD KEY `fk_rm_estado` (`id_estado_en_consulta`);

--
-- Indices de la tabla `tipo_alergia`
--
ALTER TABLE `tipo_alergia`
  ADD PRIMARY KEY (`id_tipo_alergia`),
  ADD UNIQUE KEY `nombre_alergia` (`nombre_alergia`);

--
-- Indices de la tabla `tipo_camilla`
--
ALTER TABLE `tipo_camilla`
  ADD PRIMARY KEY (`id_tipo_camilla`);

--
-- Indices de la tabla `tipo_examen`
--
ALTER TABLE `tipo_examen`
  ADD PRIMARY KEY (`id_tipo_examen`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alergia_paciente`
--
ALTER TABLE `alergia_paciente`
  MODIFY `id_alergia_paciente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alta_medica`
--
ALTER TABLE `alta_medica`
  MODIFY `id_alta_medica` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `area`
--
ALTER TABLE `area`
  MODIFY `id_area` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `camilla`
--
ALTER TABLE `camilla`
  MODIFY `id_camilla` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalogo_calificacion_alta`
--
ALTER TABLE `catalogo_calificacion_alta`
  MODIFY `id_calificacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `catalogo_motivo_alta`
--
ALTER TABLE `catalogo_motivo_alta`
  MODIFY `id_motivo_alta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estado_en_consulta`
--
ALTER TABLE `estado_en_consulta`
  MODIFY `id_estado_consulta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estado_especialista`
--
ALTER TABLE `estado_especialista`
  MODIFY `id_estado_espec` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estado_hospitalizacion`
--
ALTER TABLE `estado_hospitalizacion`
  MODIFY `id_estado_hosp` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estado_salud`
--
ALTER TABLE `estado_salud`
  MODIFY `id_estado_salud` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `examen`
--
ALTER TABLE `examen`
  MODIFY `id_examen` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `genero`
--
ALTER TABLE `genero`
  MODIFY `id_genero` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `hospitalizacion`
--
ALTER TABLE `hospitalizacion`
  MODIFY `id_hospitalizacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `registro_medico`
--
ALTER TABLE `registro_medico`
  MODIFY `id_registro_med` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_alergia`
--
ALTER TABLE `tipo_alergia`
  MODIFY `id_tipo_alergia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_camilla`
--
ALTER TABLE `tipo_camilla`
  MODIFY `id_tipo_camilla` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_examen`
--
ALTER TABLE `tipo_examen`
  MODIFY `id_tipo_examen` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alergia_paciente`
--
ALTER TABLE `alergia_paciente`
  ADD CONSTRAINT `fk_ap_paciente` FOREIGN KEY (`run_paciente`) REFERENCES `paciente` (`run`),
  ADD CONSTRAINT `fk_ap_tipo` FOREIGN KEY (`id_tipo_alergia`) REFERENCES `tipo_alergia` (`id_tipo_alergia`);

--
-- Filtros para la tabla `alta_medica`
--
ALTER TABLE `alta_medica`
  ADD CONSTRAINT `fk_alta_calificacion` FOREIGN KEY (`id_calificacion`) REFERENCES `catalogo_calificacion_alta` (`id_calificacion`),
  ADD CONSTRAINT `fk_alta_especialista` FOREIGN KEY (`run_especialista`) REFERENCES `especialista` (`run_especialista`),
  ADD CONSTRAINT `fk_alta_hospitalizacion` FOREIGN KEY (`id_hospitalizacion`) REFERENCES `hospitalizacion` (`id_hospitalizacion`),
  ADD CONSTRAINT `fk_alta_motivo` FOREIGN KEY (`id_motivo_alta`) REFERENCES `catalogo_motivo_alta` (`id_motivo_alta`),
  ADD CONSTRAINT `fk_alta_paciente` FOREIGN KEY (`run_paciente`) REFERENCES `paciente` (`run`);

--
-- Filtros para la tabla `camilla`
--
ALTER TABLE `camilla`
  ADD CONSTRAINT `fk_camilla_tipo` FOREIGN KEY (`id_tipo_camilla`) REFERENCES `tipo_camilla` (`id_tipo_camilla`);

--
-- Filtros para la tabla `especialista`
--
ALTER TABLE `especialista`
  ADD CONSTRAINT `fk_esp_area` FOREIGN KEY (`id_area`) REFERENCES `area` (`id_area`),
  ADD CONSTRAINT `fk_esp_estado` FOREIGN KEY (`id_estado_espec`) REFERENCES `estado_especialista` (`id_estado_espec`);

--
-- Filtros para la tabla `examen`
--
ALTER TABLE `examen`
  ADD CONSTRAINT `fk_examen_registro` FOREIGN KEY (`id_registro_med`) REFERENCES `registro_medico` (`id_registro_med`),
  ADD CONSTRAINT `fk_examen_tipo` FOREIGN KEY (`id_tipo_examen`) REFERENCES `tipo_examen` (`id_tipo_examen`);

--
-- Filtros para la tabla `hospitalizacion`
--
ALTER TABLE `hospitalizacion`
  ADD CONSTRAINT `fk_hosp_camilla` FOREIGN KEY (`id_camilla`) REFERENCES `camilla` (`id_camilla`),
  ADD CONSTRAINT `fk_hosp_especialista` FOREIGN KEY (`run_especialista`) REFERENCES `especialista` (`run_especialista`),
  ADD CONSTRAINT `fk_hosp_estado` FOREIGN KEY (`id_estado_hospitalizacion`) REFERENCES `estado_hospitalizacion` (`id_estado_hosp`),
  ADD CONSTRAINT `fk_hosp_paciente` FOREIGN KEY (`run_paciente`) REFERENCES `paciente` (`run`);

--
-- Filtros para la tabla `paciente`
--
ALTER TABLE `paciente`
  ADD CONSTRAINT `fk_paciente_estado` FOREIGN KEY (`id_estado_salud`) REFERENCES `estado_salud` (`id_estado_salud`),
  ADD CONSTRAINT `fk_paciente_genero` FOREIGN KEY (`id_genero`) REFERENCES `genero` (`id_genero`),
  ADD CONSTRAINT `fk_paciente_grupo` FOREIGN KEY (`grupo_sang`) REFERENCES `grupo_sanguineo` (`nombre_grupo`);

--
-- Filtros para la tabla `registro_medico`
--
ALTER TABLE `registro_medico`
  ADD CONSTRAINT `fk_rm_especialista` FOREIGN KEY (`run_especialista`) REFERENCES `especialista` (`run_especialista`),
  ADD CONSTRAINT `fk_rm_estado` FOREIGN KEY (`id_estado_en_consulta`) REFERENCES `estado_en_consulta` (`id_estado_consulta`),
  ADD CONSTRAINT `fk_rm_paciente` FOREIGN KEY (`run_paciente`) REFERENCES `paciente` (`run`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
