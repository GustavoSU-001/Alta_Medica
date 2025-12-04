-- =====================================================
-- DATA WAREHOUSE: DWH_ALTA_MEDICA
-- Esquema Estrella Puro (Pure Star Schema)
-- Optimizado para Pentaho ETL
-- =====================================================

CREATE DATABASE dwh_alta_medica
ON PRIMARY
(NAME='dwh_alta_medica', FILENAME='C:\dwh_alta_medica\mdf\dwh_alta_medica.mdf', 
SIZE=200MB, MAXSIZE=500MB, FILEGROWTH=30MB),
FILEGROUP DIMENSIONS DEFAULT
(NAME='dwh_alta_medica_dimensions', FILENAME='C:\dwh_alta_medica\dimensions\dwh_alta_medica_dimensions.ndf',
SIZE=200MB, MAXSIZE=500MB, FILEGROWTH=30MB),
FILEGROUP FACTS
(NAME='dwh_alta_medica_facts', FILENAME='C:\dwh_alta_medica\facts\dwh_alta_medica_facts.ndf',
SIZE=200MB, MAXSIZE=500MB, FILEGROWTH=30MB),
FILEGROUP STAGING
(NAME='dwh_alta_medica_staging', FILENAME='C:\dwh_alta_medica\staging\dwh_alta_medica_staging.ndf',
SIZE=200MB, MAXSIZE=500MB, FILEGROWTH=30MB)
LOG ON
(NAME='dwh_alta_medica_log', FILENAME='C:\dwh_alta_medica\ldf\dwh_alta_medica_log.ldf',
SIZE=200MB, FILEGROWTH=30MB)
GO

USE dwh_alta_medica
GO

CREATE SCHEMA STG
GO
CREATE SCHEMA DWH
GO

-- =====================================================
-- DIMENSIONES (DIMENSIONS)
-- =====================================================

-- Dimensión: Paciente
CREATE TABLE DWH.dim_paciente(
	id_dim_paciente INT NOT NULL IDENTITY(1,1),
	run_paciente VARCHAR(12) NOT NULL,
	nombre_completo VARCHAR(200) NOT NULL,
	nombres VARCHAR(100) NOT NULL,
	apellidos VARCHAR(100) NOT NULL,
	fecha_nacimiento DATE NOT NULL,
	edad INT NOT NULL,
	genero VARCHAR(50) NOT NULL,
	grupo_sanguineo VARCHAR(5) NOT NULL,
	estado_salud VARCHAR(100) NOT NULL,
	telefono VARCHAR(20) NULL,
	correo VARCHAR(100) NULL,
	direccion VARCHAR(255) NULL,
	CONSTRAINT pk_dim_paciente PRIMARY KEY(id_dim_paciente) ON DIMENSIONS
) ON DIMENSIONS
GO

-- Dimensión: Especialista
CREATE TABLE DWH.dim_especialista(
	id_dim_especialista INT NOT NULL IDENTITY(1,1),
	run_especialista VARCHAR(12) NOT NULL,
	nombre_completo VARCHAR(200) NOT NULL,
	nombres VARCHAR(100) NOT NULL,
	apellidos VARCHAR(100) NOT NULL,
	especialidad VARCHAR(100) NOT NULL,
	area_medica VARCHAR(100) NOT NULL,
	estado VARCHAR(50) NOT NULL,
	telefono VARCHAR(20) NULL,
	correo VARCHAR(100) NULL,
	CONSTRAINT pk_dim_especialista PRIMARY KEY(id_dim_especialista) ON DIMENSIONS
) ON DIMENSIONS
GO

-- Dimensión: Tiempo
CREATE TABLE DWH.dim_tiempo(
	id_dim_tiempo INT NOT NULL IDENTITY(1,1),
	fecha DATE NOT NULL,
	anio INT NOT NULL,
	mes INT NOT NULL,
	dia INT NOT NULL,
	trimestre INT NOT NULL,
	semestre INT NOT NULL,
	nombre_mes VARCHAR(20) NOT NULL,
	nombre_dia VARCHAR(20) NOT NULL,
	dia_semana INT NOT NULL,
	es_fin_semana BIT NOT NULL,
	es_festivo BIT NOT NULL DEFAULT 0,
	CONSTRAINT pk_dim_tiempo PRIMARY KEY(id_dim_tiempo) ON DIMENSIONS,
	CONSTRAINT uk_dim_tiempo_fecha UNIQUE(fecha)
) ON DIMENSIONS
GO

-- Dimensión: Tipo Alta
CREATE TABLE DWH.dim_tipo_alta(
	id_dim_tipo_alta INT NOT NULL IDENTITY(1,1),
	tipo_formulario VARCHAR(50) NOT NULL,
	calificacion VARCHAR(100) NOT NULL,
	motivo_alta VARCHAR(255) NOT NULL,
	categoria_motivo VARCHAR(100) NOT NULL,
	CONSTRAINT pk_dim_tipo_alta PRIMARY KEY(id_dim_tipo_alta) ON DIMENSIONS
) ON DIMENSIONS
GO

-- Dimensión: Condición Paciente
CREATE TABLE DWH.dim_condicion(
	id_dim_condicion INT NOT NULL IDENTITY(1,1),
	es_menor_edad BIT NOT NULL,
	es_persona_mayor BIT NOT NULL,
	tiene_discapacidad BIT NOT NULL,
	tiene_dependencia BIT NOT NULL,
	presume_invalidez BIT NOT NULL,
	descripcion_condicion VARCHAR(255) NOT NULL,
	CONSTRAINT pk_dim_condicion PRIMARY KEY(id_dim_condicion) ON DIMENSIONS
) ON DIMENSIONS
GO

-- Dimensión: Hospitalizacion
CREATE TABLE DWH.dim_hospitalizacion(
	id_dim_hospitalizacion INT NOT NULL IDENTITY(1,1),
	tipo_camilla VARCHAR(100) NOT NULL,
	estado_hospitalizacion VARCHAR(100) NOT NULL,
	categoria_motivo VARCHAR(100) NOT NULL,
	CONSTRAINT pk_dim_hospitalizacion PRIMARY KEY(id_dim_hospitalizacion) ON DIMENSIONS
) ON DIMENSIONS
GO

-- =====================================================
-- TABLA DE HECHOS CENTRAL (CENTRAL FACT TABLE)
-- =====================================================

CREATE TABLE DWH.fact_alta_medica(
	id_fact INT NOT NULL IDENTITY(1,1),
	
	-- Claves foráneas a dimensiones (Foreign Keys to Dimensions)
	id_dim_paciente INT NOT NULL,
	id_dim_especialista INT NOT NULL,
	id_dim_tiempo INT NOT NULL,
	id_dim_tipo_alta INT NOT NULL,
	id_dim_condicion INT NOT NULL,
	id_dim_hospitalizacion INT NULL,
	
	-- Métricas Numéricas (Numeric Metrics)
	dias_hospitalizacion INT NULL,
	edad_paciente_al_alta INT NOT NULL,
	dias_desde_emision_hasta_alta INT NOT NULL,
	
	-- Indicadores Binarios (Binary Indicators)
	tiene_hospitalizacion BIT NOT NULL,
	tiene_responsable_legal BIT NOT NULL,
	tiene_empleador BIT NOT NULL,
	tiene_codigo_unico BIT NOT NULL,
	tiene_diat_diep BIT NOT NULL,
	
	-- Atributos Degenerados (Degenerate Dimensions)
	numero_certificado VARCHAR(50) NOT NULL,
	codigo_unico_nacional VARCHAR(20) NULL,
	
	-- Fechas para análisis (Dates for analysis)
	fecha_emision DATE NOT NULL,
	fecha_alta DATE NOT NULL,
	fecha_diat_diep DATE NULL,
	
	-- Constraints
	CONSTRAINT pk_fact_alta_medica PRIMARY KEY(id_fact) ON FACTS,
	CONSTRAINT fk_fact_paciente FOREIGN KEY(id_dim_paciente) 
		REFERENCES DWH.dim_paciente(id_dim_paciente),
	CONSTRAINT fk_fact_especialista FOREIGN KEY(id_dim_especialista) 
		REFERENCES DWH.dim_especialista(id_dim_especialista),
	CONSTRAINT fk_fact_tiempo FOREIGN KEY(id_dim_tiempo) 
		REFERENCES DWH.dim_tiempo(id_dim_tiempo),
	CONSTRAINT fk_fact_tipo_alta FOREIGN KEY(id_dim_tipo_alta) 
		REFERENCES DWH.dim_tipo_alta(id_dim_tipo_alta),
	CONSTRAINT fk_fact_condicion FOREIGN KEY(id_dim_condicion) 
		REFERENCES DWH.dim_condicion(id_dim_condicion),
	CONSTRAINT fk_fact_hospitalizacion FOREIGN KEY(id_dim_hospitalizacion) 
		REFERENCES DWH.dim_hospitalizacion(id_dim_hospitalizacion)
) ON FACTS
GO

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN DE CONSULTAS
-- =====================================================

-- Índices en Dimensiones
CREATE INDEX idx_paciente_run ON DWH.dim_paciente(run_paciente)
GO
CREATE INDEX idx_paciente_genero ON DWH.dim_paciente(genero)
GO
CREATE INDEX idx_paciente_edad ON DWH.dim_paciente(edad)
GO

CREATE INDEX idx_especialista_run ON DWH.dim_especialista(run_especialista)
GO
CREATE INDEX idx_especialista_especialidad ON DWH.dim_especialista(especialidad)
GO

CREATE INDEX idx_tiempo_anio_mes ON DWH.dim_tiempo(anio, mes)
GO
CREATE INDEX idx_tiempo_trimestre ON DWH.dim_tiempo(trimestre)
GO

CREATE INDEX idx_tipo_alta_formulario ON DWH.dim_tipo_alta(tipo_formulario)
GO
CREATE INDEX idx_tipo_alta_categoria ON DWH.dim_tipo_alta(categoria_motivo)
GO

-- Índices en Tabla de Hechos
CREATE INDEX idx_fact_fechas ON DWH.fact_alta_medica(fecha_emision, fecha_alta)
GO
CREATE INDEX idx_fact_paciente ON DWH.fact_alta_medica(id_dim_paciente)
GO
CREATE INDEX idx_fact_especialista ON DWH.fact_alta_medica(id_dim_especialista)
GO
CREATE INDEX idx_fact_tiempo ON DWH.fact_alta_medica(id_dim_tiempo)
GO
CREATE INDEX idx_fact_certificado ON DWH.fact_alta_medica(numero_certificado)
GO

-- =====================================================
-- VISTAS PARA ANÁLISIS (ANALYTICAL VIEWS)
-- =====================================================

-- Vista: Resumen de Altas por Mes
CREATE VIEW DWH.v_altas_por_mes AS
SELECT 
	t.anio,
	t.mes,
	t.nombre_mes,
	COUNT(*) as total_altas,
	AVG(f.edad_paciente_al_alta) as edad_promedio,
	AVG(CAST(f.dias_hospitalizacion AS FLOAT)) as dias_hosp_promedio,
	SUM(CASE WHEN c.tiene_discapacidad = 1 THEN 1 ELSE 0 END) as total_con_discapacidad,
	SUM(CASE WHEN c.presume_invalidez = 1 THEN 1 ELSE 0 END) as total_presume_invalidez
FROM DWH.fact_alta_medica f
INNER JOIN DWH.dim_tiempo t ON f.id_dim_tiempo = t.id_dim_tiempo
INNER JOIN DWH.dim_condicion c ON f.id_dim_condicion = c.id_dim_condicion
GROUP BY t.anio, t.mes, t.nombre_mes
GO

-- Vista: Altas por Especialista
CREATE VIEW DWH.v_altas_por_especialista AS
SELECT 
	e.nombre_completo,
	e.especialidad,
	e.area_medica,
	COUNT(*) as total_altas,
	AVG(CAST(f.dias_hospitalizacion AS FLOAT)) as dias_hosp_promedio,
	MIN(f.fecha_alta) as primera_alta,
	MAX(f.fecha_alta) as ultima_alta
FROM DWH.fact_alta_medica f
INNER JOIN DWH.dim_especialista e ON f.id_dim_especialista = e.id_dim_especialista
GROUP BY e.nombre_completo, e.especialidad, e.area_medica
GO

-- Vista: Análisis de Condiciones Especiales
CREATE VIEW DWH.v_analisis_condiciones AS
SELECT 
	t.anio,
	t.trimestre,
	c.descripcion_condicion,
	COUNT(*) as total_casos,
	AVG(f.edad_paciente_al_alta) as edad_promedio,
	AVG(CAST(f.dias_hospitalizacion AS FLOAT)) as dias_hosp_promedio
FROM DWH.fact_alta_medica f
INNER JOIN DWH.dim_tiempo t ON f.id_dim_tiempo = t.id_dim_tiempo
INNER JOIN DWH.dim_condicion c ON f.id_dim_condicion = c.id_dim_condicion
GROUP BY t.anio, t.trimestre, c.descripcion_condicion
GO

-- =====================================================
-- TABLAS DE STAGING (STAGING AREA)
-- =====================================================

-- Staging: Paciente
CREATE TABLE STG.tb_paciente (
    run_paciente VARCHAR(12) NOT NULL,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_nacimiento DATE NULL,
    genero VARCHAR(50),
    grupo_sanguineo VARCHAR(5),
    estado_salud VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    direccion VARCHAR(255),
    CONSTRAINT PK_stg_paciente PRIMARY KEY (run_paciente)
) ON STAGING
GO

-- Staging: Especialista
CREATE TABLE STG.tb_especialista (
    run_especialista VARCHAR(12) NOT NULL,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    especialidad VARCHAR(100),
    area_medica VARCHAR(100),
    estado VARCHAR(50),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    CONSTRAINT PK_stg_especialista PRIMARY KEY (run_especialista)
) ON STAGING
GO

-- Staging: Tipo Alta
CREATE TABLE STG.tb_tipo_alta (
    tipo_formulario VARCHAR(50),
    calificacion VARCHAR(100),
    motivo_alta VARCHAR(255),
    categoria_motivo VARCHAR(100)
) ON STAGING
GO

-- Staging: Condición
CREATE TABLE STG.tb_condicion (
    es_menor_edad BIT,
    es_persona_mayor BIT,
    tiene_discapacidad BIT,
    tiene_dependencia BIT,
    presume_invalidez BIT,
    descripcion_condicion VARCHAR(255)
) ON STAGING
GO

-- Staging: Hospitalización
CREATE TABLE STG.tb_hospitalizacion (
    tipo_camilla VARCHAR(100),
    estado_hospitalizacion VARCHAR(100),
    categoria_motivo VARCHAR(100)
) ON STAGING
GO

-- Staging: Alta Médica (Tabla principal de staging)
CREATE TABLE STG.tb_alta_medica (
    -- Claves de negocio
    run_paciente VARCHAR(12),
    run_especialista VARCHAR(12),
    
    -- Información del alta
    numero_certificado VARCHAR(50),
    codigo_unico_nacional VARCHAR(20),
    tipo_formulario VARCHAR(50),
    calificacion VARCHAR(100),
    motivo_alta VARCHAR(255),
    categoria_motivo VARCHAR(100),
    
    -- Condiciones del paciente
    es_menor_edad BIT,
    es_persona_mayor BIT,
    tiene_discapacidad BIT,
    tiene_dependencia BIT,
    presume_invalidez BIT,
    descripcion_condicion VARCHAR(255),
    
    -- Información de hospitalización
    tipo_camilla VARCHAR(100),
    estado_hospitalizacion VARCHAR(100),
    categoria_motivo_hosp VARCHAR(100),
    
    -- Métricas
    dias_hospitalizacion INT,
    edad_paciente_al_alta INT,
    
    -- Indicadores
    tiene_hospitalizacion BIT,
    tiene_responsable_legal BIT,
    tiene_empleador BIT,
    tiene_codigo_unico BIT,
    tiene_diat_diep BIT,
    
    -- Fechas
    fecha_emision DATE,
    fecha_alta DATE,
    fecha_diat_diep DATE
) ON STAGING
GO

-- =====================================================
-- DOCUMENTACIÓN DEL ESQUEMA ESTRELLA
-- =====================================================

/*
ESTRUCTURA DEL ESQUEMA ESTRELLA:

CENTRO (FACT TABLE):
- fact_alta_medica: Tabla central con todas las métricas de altas médicas

DIMENSIONES (6 DIMENSIONS):
1. dim_paciente: Información demográfica del paciente
2. dim_especialista: Datos del médico que emite el alta
3. dim_tiempo: Jerarquía temporal para análisis
4. dim_tipo_alta: Clasificación del tipo de alta médica
5. dim_condicion: Condiciones especiales del paciente
6. dim_hospitalizacion: Detalles de la hospitalización

MÉTRICAS PRINCIPALES:
- Días de hospitalización
- Edad del paciente al alta
- Días desde emisión hasta alta
- Contadores de condiciones especiales

ANÁLISIS POSIBLES:
✓ Tendencias temporales de altas médicas
✓ Desempeño por especialista/especialidad
✓ Análisis de condiciones especiales (discapacidad, invalidez)
✓ Duración de hospitalizaciones
✓ Distribución por edad y género
✓ Análisis de tipos de alta y motivos
✓ Patrones estacionales y temporales

OPTIMIZADO PARA PENTAHO:
- Estructura simple y plana
- Claves surrogadas (IDENTITY)
- Índices optimizados para joins
- Vistas pre-calculadas para reportes comunes
- Sin tablas de staging (se manejan en Pentaho)
*/
