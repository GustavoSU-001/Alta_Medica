# Implementation Plan: ETL Alta Medica

## Overview

Create three Pentaho Data Integration (Kettle) transformation files to migrate data from the `alta_medica` MySQL database to the `dwh_alta_medica` SQL Server data warehouse, following the established pattern from PolanMed.

## Background

The PolanMed project provides a reference implementation with three KTR files:
- **STGPolanMed.ktr**: Extracts data from MySQL (`bd_polanmed`) and loads into SQL Server staging area (`dwh_polanmed.STG`)
- **DWHPolanMed.ktr**: Transforms staging data into dimension tables (`dwh_polanmed.DWH`)
- **FACTPolanMed.ktr**: Loads the fact table by joining dimensions with staging data

The Alta Medica project requires the same pattern but with a different schema:
- **Source**: MySQL database `alta_medica_2025` with 18 tables
- **Target**: SQL Server database `dwh_alta_medica` with star schema (6 dimensions + 1 fact table)

---

## Proposed Changes

### [NEW] [STG_Alta_Medica.ktr](file:///c:/Users/Eliwasauki/OneDrive/Escritorio/Guias/Inacap/Semestre8/Machine%20Learning/Evaluacion3/Alta_Medica/STG_Alta_Medica.ktr)

Create a new staging transformation that extracts data from MySQL and loads it into SQL Server staging tables.

**Database Connections:**
- **MySQLConexion**: localhost:3306, database `alta_medica_2025`, user `root`
- **SQLServerConexion**: localhost:1433\\SQLEXPRESS, database `dwh_alta_medica`, user `sa`

**Transformation Steps:**

1. **Extract Paciente** (Table Input → Sort → Table Output)
   - Source: MySQL query joining `paciente`, `genero`, `grupo_sanguineo`, `estado_salud`
   - Transformation: Sort by `run`
   - Target: `STG.tb_paciente`
   - Fields: run_paciente, nombres, apellidos, fecha_nacimiento, genero, grupo_sanguineo, estado_salud, telefono, correo, direccion

2. **Extract Especialista** (Table Input → Sort → Table Output)
   - Source: MySQL query joining `especialista`, `area`, `estado_especialista`
   - Transformation: Sort by `run_especialista`
   - Target: `STG.tb_especialista`
   - Fields: run_especialista, nombres, apellidos, especialidad (from area), area_medica, estado, telefono, correo

3. **Extract Alta Medica** (Table Input → Select Values → Calculator → Table Output)
   - Source: MySQL query joining `alta_medica`, `paciente`, `especialista`, `hospitalizacion`, `catalogo_calificacion_alta`, `catalogo_motivo_alta`, `camilla`, `tipo_camilla`, `estado_hospitalizacion`
   - Transformations:
     - Calculate `edad_paciente_al_alta` from fecha_nacimiento and fecha_alta
     - Calculate `dias_hospitalizacion` from hospitalizacion dates
     - Calculate `dias_desde_emision_hasta_alta` from fecha_emision_certificado and fecha_alta
     - Set boolean indicators (tiene_hospitalizacion, tiene_responsable_legal, tiene_empleador, tiene_codigo_unico, tiene_diat_diep)
     - Build `descripcion_condicion` from boolean flags
   - Target: `STG.tb_alta_medica`

---

### [NEW] [DWH_Alta_Medica.ktr](file:///c:/Users/Eliwasauki/OneDrive/Escritorio/Guias/Inacap/Semestre8/Machine%20Learning/Evaluacion3/Alta_Medica/DWH_Alta_Medica.ktr)

Create dimension loading transformation that populates dimension tables from staging data.

**Transformation Steps:**

1. **Load dim_paciente** (Table Input → Calculator → Table Output)
   - Source: `STG.tb_paciente`
   - Transformations:
     - Calculate `edad` from fecha_nacimiento
     - Concatenate `nombre_completo` from nombres + apellidos
   - Target: `DWH.dim_paciente`
   - Truncate: No (append mode)

2. **Load dim_especialista** (Table Input → Calculator → Table Output)
   - Source: `STG.tb_especialista`
   - Transformations:
     - Concatenate `nombre_completo` from nombres + apellidos
   - Target: `DWH.dim_especialista`
   - Truncate: No (append mode)

3. **Load dim_tiempo** (Table Input → Calculator → Table Output)
   - Source: `STG.tb_alta_medica` (SELECT DISTINCT fecha_alta, fecha_emision, fecha_diat_diep)
   - Transformations:
     - Extract year, month, day, quarter, semester
     - Calculate day of week, weekend flag
     - Generate month and day names (Spanish)
   - Target: `DWH.dim_tiempo`
   - Truncate: No (append mode with DISTINCT check)

4. **Load dim_tipo_alta** (Table Input → Table Output)
   - Source: `STG.tb_tipo_alta` (SELECT DISTINCT tipo_formulario, calificacion, motivo_alta, categoria_motivo)
   - Target: `DWH.dim_tipo_alta`
   - Truncate: No (append mode with DISTINCT check)

5. **Load dim_condicion** (Table Input → Table Output)
   - Source: `STG.tb_condicion` (SELECT DISTINCT es_menor_edad, es_persona_mayor, tiene_discapacidad, tiene_dependencia, presume_invalidez, descripcion_condicion)
   - Target: `DWH.dim_condicion`
   - Truncate: No (append mode with DISTINCT check)

6. **Load dim_hospitalizacion** (Table Input → Table Output)
   - Source: `STG.tb_hospitalizacion` (SELECT DISTINCT tipo_camilla, estado_hospitalizacion, categoria_motivo)
   - Target: `DWH.dim_hospitalizacion`
   - Truncate: No (append mode with DISTINCT check)

---

### [NEW] [FACT_Alta_Medica.ktr](file:///c:/Users/Eliwasauki/OneDrive/Escritorio/Guias/Inacap/Semestre8/Machine%20Learning/Evaluacion3/Alta_Medica/FACT_Alta_Medica.ktr)

Create fact table loading transformation that joins staging data with dimensions.

**Transformation Steps:**

1. **Load fact_alta_medica** (Table Input → Database Lookup × 6 → Table Output)
   - Source: `STG.tb_alta_medica`
   - Lookups (to get dimension surrogate keys):
     - Lookup `id_dim_paciente` from `DWH.dim_paciente` WHERE run_paciente = ?
     - Lookup `id_dim_especialista` from `DWH.dim_especialista` WHERE run_especialista = ?
     - Lookup `id_dim_tiempo` from `DWH.dim_tiempo` WHERE fecha = fecha_alta
     - Lookup `id_dim_tipo_alta` from `DWH.dim_tipo_alta` WHERE tipo_formulario = ? AND calificacion = ? AND motivo_alta = ?
     - Lookup `id_dim_condicion` from `DWH.dim_condicion` WHERE all condition flags match
     - Lookup `id_dim_hospitalizacion` from `DWH.dim_hospitalizacion` WHERE tipo_camilla = ? AND estado_hospitalizacion = ?
   - Target: `DWH.fact_alta_medica`
   - Truncate: No (append mode)

---

## Verification Plan

### Automated Tests

Since this is an ETL project using Pentaho Data Integration, there are no traditional unit tests. Verification will be done through:

1. **Connection Testing**
   ```powershell
   # Test MySQL connection
   mysql -h localhost -u root -p alta_medica_2025 -e "SELECT COUNT(*) FROM paciente;"
   
   # Test SQL Server connection
   sqlcmd -S localhost\SQLEXPRESS -U sa -P [password] -d dwh_alta_medica -Q "SELECT COUNT(*) FROM STG.tb_paciente;"
   ```

2. **Data Validation Queries**
   ```sql
   -- Verify staging row counts match source
   SELECT 'MySQL Paciente' as source, COUNT(*) FROM alta_medica_2025.paciente
   UNION ALL
   SELECT 'STG Paciente', COUNT(*) FROM dwh_alta_medica.STG.tb_paciente;
   
   -- Verify dimension loading
   SELECT 'dim_paciente', COUNT(*) FROM DWH.dim_paciente
   UNION ALL
   SELECT 'dim_especialista', COUNT(*) FROM DWH.dim_especialista
   UNION ALL
   SELECT 'dim_tiempo', COUNT(*) FROM DWH.dim_tiempo
   UNION ALL
   SELECT 'dim_tipo_alta', COUNT(*) FROM DWH.dim_tipo_alta
   UNION ALL
   SELECT 'dim_condicion', COUNT(*) FROM DWH.dim_condicion
   UNION ALL
   SELECT 'dim_hospitalizacion', COUNT(*) FROM DWH.dim_hospitalizacion;
   
   -- Verify fact table
   SELECT COUNT(*) as total_facts FROM DWH.fact_alta_medica;
   
   -- Verify no orphaned records (all foreign keys valid)
   SELECT COUNT(*) FROM DWH.fact_alta_medica f
   WHERE NOT EXISTS (SELECT 1 FROM DWH.dim_paciente p WHERE p.id_dim_paciente = f.id_dim_paciente);
   ```

### Manual Verification

1. **Run STG_Alta_Medica.ktr in Spoon (Pentaho)**
   - Open Pentaho Data Integration (Spoon)
   - File → Open → Select `STG_Alta_Medica.ktr`
   - Click "Run" button (F9)
   - Verify no errors in execution log
   - Check "Metrics" tab for row counts
   - Expected: All steps show green checkmarks

2. **Run DWH_Alta_Medica.ktr in Spoon**
   - Open `DWH_Alta_Medica.ktr`
   - Click "Run" button
   - Verify all dimension tables populated
   - Check for duplicate records in dimensions

3. **Run FACT_Alta_Medica.ktr in Spoon**
   - Open `FACT_Alta_Medica.ktr`
   - Click "Run" button
   - Verify fact table populated
   - Check that all dimension lookups succeeded (no nulls in FK columns)

4. **Visual Data Quality Check**
   - Query sample records from fact table with dimension joins
   - Verify calculated metrics are reasonable (edad, dias_hospitalizacion)
   - Check that dates are in correct format
   - Verify boolean flags are set correctly

---

## User Review Required

> [!IMPORTANT]
> **Database Credentials**: The implementation assumes default credentials (root for MySQL, sa for SQL Server). Please confirm or provide the correct credentials for both databases.

> [!WARNING]
> **Data Volume**: The plan assumes the alta_medica database has been populated with data. If the database is empty, the ETL will run but produce no output. Please confirm data exists in the source database.

> [!IMPORTANT]
> **SQL Server File Paths**: The script3.sql creates the database with specific file paths (`C:\dwh_alta_medica\...`). Please confirm these directories exist or modify the paths as needed.
