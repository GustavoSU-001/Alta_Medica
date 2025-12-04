# Walkthrough: ETL Alta Medica Implementation

## Resumen del Proyecto

Se ha completado el análisis y documentación para implementar un proceso ETL que migra datos desde la base de datos MySQL `alta_medica` hacia el Data Warehouse SQL Server `dwh_alta_medica`, siguiendo el patrón establecido por PolanMed.

---

## Documentos Creados

### 1. [implementation_plan.md](file:///C:/Users/Eliwasauki/.gemini/antigravity/brain/4273a8d6-17f3-482c-b118-296b1f17ff89/implementation_plan.md)
Plan de implementación completo con:
- Descripción general del proyecto
- Estructura de las tres transformaciones KTR
- Plan de verificación
- Puntos importantes para revisión del usuario

### 2. [analisis_etl.md](file:///C:/Users/Eliwasauki/.gemini/antigravity/brain/4273a8d6-17f3-482c-b118-296b1f17ff89/analisis_etl.md)
Análisis técnico detallado con:
- Comparación entre PolanMed y Alta Medica
- Mapeo completo de tablas origen → staging → dimensiones → fact
- Queries SQL con transformaciones complejas
- Diagramas de flujo de datos
- Recomendaciones de implementación

### 3. [guia_configuracion_ktr.md](file:///C:/Users/Eliwasauki/.gemini/antigravity/brain/4273a8d6-17f3-482c-b118-296b1f17ff89/guia_configuracion_ktr.md)
**Guía práctica paso a paso** para configurar los KTR en Pentaho Spoon:
- Configuración de conexiones a bases de datos
- Todos los SQL queries necesarios
- Configuración de cada step (Table Input, Sort, Calculator, Database Lookup, Table Output)
- Orden de ejecución
- Queries de validación

---

## Arquitectura ETL

```
┌─────────────────────────────────────────────────────────────┐
│                    MySQL: alta_medica                       │
│  (5,000 pacientes, 200 especialistas, 18,000 altas)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ STG_Alta_Medica.ktr
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           SQL Server: dwh_alta_medica.STG                   │
│  (tb_paciente, tb_especialista, tb_alta_medica)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ DWH_Alta_Medica.ktr
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           SQL Server: dwh_alta_medica.DWH                   │
│  (6 dimensiones: paciente, especialista, tiempo,            │
│   tipo_alta, condicion, hospitalizacion)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ FACT_Alta_Medica.ktr
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           SQL Server: dwh_alta_medica.DWH                   │
│              (fact_alta_medica)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Próximos Pasos

### 1. Preparar el Entorno

#### Verificar SQL Server
```powershell
# Verificar que existe la base de datos
sqlcmd -S localhost\SQLEXPRESS -U sa -P [password] -Q "SELECT name FROM sys.databases WHERE name = 'dwh_alta_medica'"
```

Si no existe, ejecutar `script3.sql` para crear el DWH.

#### Verificar MySQL
```powershell
# Verificar conteo de datos
mysql -h localhost -u root -p alta_medica -e "SELECT 'paciente' as tabla, COUNT(*) as registros FROM paciente UNION ALL SELECT 'especialista', COUNT(*) FROM especialista UNION ALL SELECT 'alta_medica', COUNT(*) FROM alta_medica;"
```

Resultado esperado:
- paciente: ~5,000
- especialista: ~200
- alta_medica: ~18,000

---

### 2. Configurar Pentaho Spoon

#### Abrir los archivos KTR
Los archivos ya están abiertos en tu Pentaho Spoon:
- `STG_Alta_Medica.ktr`
- `DWH_Alta_Medica.ktr`
- `FACT_Alta_Medica.ktr`

#### Configurar Conexiones

**Para cada archivo KTR:**

1. **Crear conexión MySQL:**
   - Clic derecho en "Database connections" → New
   - Nombre: `MySQLConexion`
   - Connection Type: MySQL
   - Host: `localhost`
   - Port: `3306`
   - Database: `alta_medica`
   - Username: `root`
   - Password: [tu contraseña]
   - Test Connection

2. **Crear conexión SQL Server:**
   - Clic derecho en "Database connections" → New
   - Nombre: `SQLServerConexion`
   - Connection Type: MS SQL Server
   - Host: `localhost`
   - Port: `1433`
   - Instance: `SQLEXPRESS`
   - Database: `dwh_alta_medica`
   - Username: `sa`
   - Password: [tu contraseña]
   - Test Connection

---

### 3. Configurar STG_Alta_Medica.ktr

Usar la [guia_configuracion_ktr.md](file:///C:/Users/Eliwasauki/.gemini/antigravity/brain/4273a8d6-17f3-482c-b118-296b1f17ff89/guia_configuracion_ktr.md) sección "1. STG_Alta_Medica.ktr" para:

1. **Agregar Step "Extract Paciente"** (Table Input)
   - Copiar SQL query de la guía
   - Conectar a MySQLConexion

2. **Agregar Step "Sort Paciente"** (Sort rows)
   - Ordenar por `run_paciente`

3. **Agregar Step "Output Paciente"** (Table Output)
   - Conectar a SQLServerConexion
   - Schema: `STG`
   - Table: `tb_paciente`
   - Truncate: Yes

4. **Repetir para Especialista** (Steps 4-6 en la guía)

5. **Configurar Extract Alta Medica** (Step 7-10 en la guía)
   - Query complejo con múltiples JOINs
   - Agregar Calculator para `dias_desde_emision_hasta_alta`
   - Select Values para limpiar campos
   - Output a `STG.tb_alta_medica`

**Conectar los steps con "hops" (flechas)**

---

### 4. Configurar DWH_Alta_Medica.ktr

Usar la sección "2. DWH_Alta_Medica.ktr" de la guía para configurar 6 flujos paralelos (uno por dimensión):

**Para cada dimensión:**
1. Table Input (SELECT DISTINCT desde staging)
2. Calculator (para campos calculados como nombre_completo, edad)
3. Database Lookup (verificar si ya existe)
4. Filter Rows (solo registros nuevos)
5. Table Output (insertar en dimensión)

**Dimensiones a configurar:**
- dim_paciente
- dim_especialista
- dim_tiempo (incluye JavaScript para nombres en español)
- dim_tipo_alta
- dim_condicion
- dim_hospitalizacion

---

### 5. Configurar FACT_Alta_Medica.ktr

Usar la sección "3. FACT_Alta_Medica.ktr" de la guía:

1. **Table Input** desde `STG.tb_alta_medica`

2. **6 Database Lookups** (uno por dimensión):
   - Lookup `id_dim_paciente` usando `run_paciente`
   - Lookup `id_dim_especialista` usando `run_especialista`
   - Lookup `id_dim_tiempo` usando `fecha_alta`
   - Lookup `id_dim_tipo_alta` usando 4 campos
   - Lookup `id_dim_condicion` usando 5 campos
   - Lookup `id_dim_hospitalizacion` usando 3 campos

3. **Calculator** para `dias_desde_emision_hasta_alta`

4. **Select Values** para seleccionar solo campos necesarios

5. **Table Output** a `DWH.fact_alta_medica`

---

### 6. Ejecutar las Transformaciones

**Orden de ejecución:**

1. **STG_Alta_Medica.ktr**
   - Click en botón "Run" (F9)
   - Verificar que todos los steps terminan en verde
   - Revisar "Metrics" tab para conteo de registros

2. **DWH_Alta_Medica.ktr**
   - Click en botón "Run"
   - Verificar que las 6 dimensiones se cargan correctamente

3. **FACT_Alta_Medica.ktr**
   - Click en botón "Run"
   - Verificar que la tabla de hechos se carga

---

### 7. Validar Resultados

Ejecutar las queries de validación de la guía:

```sql
-- Conteo de registros
SELECT 'STG Paciente' as tabla, COUNT(*) as registros FROM STG.tb_paciente
UNION ALL
SELECT 'STG Especialista', COUNT(*) FROM STG.tb_especialista
UNION ALL
SELECT 'STG Alta Medica', COUNT(*) FROM STG.tb_alta_medica
UNION ALL
SELECT 'DIM Paciente', COUNT(*) FROM DWH.dim_paciente
UNION ALL
SELECT 'DIM Especialista', COUNT(*) FROM DWH.dim_especialista
UNION ALL
SELECT 'DIM Tiempo', COUNT(*) FROM DWH.dim_tiempo
UNION ALL
SELECT 'DIM Tipo Alta', COUNT(*) FROM DWH.dim_tipo_alta
UNION ALL
SELECT 'DIM Condicion', COUNT(*) FROM DWH.dim_condicion
UNION ALL
SELECT 'DIM Hospitalizacion', COUNT(*) FROM DWH.dim_hospitalizacion
UNION ALL
SELECT 'FACT Alta Medica', COUNT(*) FROM DWH.fact_alta_medica;
```

**Resultados esperados:**
- STG Paciente: ~5,000
- STG Especialista: ~200
- STG Alta Medica: ~18,000
- DIM Paciente: ~5,000
- DIM Especialista: ~200
- DIM Tiempo: ~50-100 (fechas únicas)
- DIM Tipo Alta: ~10-20 (combinaciones únicas)
- DIM Condicion: ~20-30 (combinaciones únicas)
- DIM Hospitalizacion: ~10-15 (combinaciones únicas)
- FACT Alta Medica: ~18,000

---

## Troubleshooting

### Error: "Connection failed"
- Verificar que MySQL y SQL Server están corriendo
- Verificar credenciales (usuario/contraseña)
- Verificar puertos (3306 para MySQL, 1433 para SQL Server)

### Error: "Table not found"
- Verificar que `script3.sql` fue ejecutado en SQL Server
- Verificar que los schemas `STG` y `DWH` existen

### Error: "Lookup returned no results"
- Verificar que las dimensiones se cargaron antes de la fact table
- Verificar que los campos de lookup coinciden exactamente

### Registros con NULL en foreign keys
- Revisar los Database Lookup steps
- Configurar "Default value" para manejar casos no encontrados

---

## Recursos Adicionales

- **PolanMed KTR files:** Usar como referencia visual en Pentaho Spoon
  - `STGPolanMed.ktr`
  - `DWHPolanMed.ktr`
  - `FACTPolanMed.ktr`

- **Gustavo.py:** Referencia para entender la estructura de datos generados

- **script3.sql:** Esquema completo del Data Warehouse

---

## Conclusión

La documentación proporcionada incluye:
✅ Plan de implementación completo  
✅ Análisis técnico detallado con mapeos  
✅ Guía paso a paso para configuración en Pentaho  
✅ Todas las queries SQL necesarias  
✅ Queries de validación  
✅ Troubleshooting común  

**Siguiente acción:** Seguir la [guia_configuracion_ktr.md](file:///C:/Users/Eliwasauki/.gemini/antigravity/brain/4273a8d6-17f3-482c-b118-296b1f17ff89/guia_configuracion_ktr.md) para configurar los KTR files en Pentaho Spoon.
