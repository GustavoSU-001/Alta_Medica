# Guía de Configuración KTR - Alta Medica ETL

## Configuración de Conexiones

### Conexión MySQL (MySQLConexion)
```
Nombre: MySQLConexion
Tipo: MySQL
Host: localhost
Puerto: 3306
Base de datos: alta_medica
Usuario: root
Contraseña: [tu contraseña]
```

### Conexión SQL Server (SQLServerConexion)
```
Nombre: SQLServerConexion
Tipo: MS SQL Server
Host: localhost
Puerto: 1433
Instancia: SQLEXPRESS
Base de datos: dwh_alta_medica
Usuario: sa
Contraseña: [tu contraseña]
```

---

## 1. STG_Alta_Medica.ktr

### Step 1: Extract Paciente
**Tipo:** Table Input  
**Conexión:** MySQLConexion  
**SQL:**
```sql
SELECT 
    p.run as run_paciente,
    p.nombres,
    p.apellidos,
    IFNULL(p.fecha_nac, '1900-01-01') as fecha_nacimiento,
    g.nombre_genero as genero,
    p.grupo_sang as grupo_sanguineo,
    es.nombre_estado_salud as estado_salud,
    p.fono as telefono,
    p.email as correo,
    p.direccion
FROM paciente p
LEFT JOIN genero g ON p.id_genero = g.id_genero
LEFT JOIN estado_salud es ON p.id_estado_salud = es.id_estado_salud
ORDER BY p.run
```

### Step 2: Sort Paciente
**Tipo:** Sort rows  
**Campos a ordenar:** run_paciente (Ascending)

### Step 3: Output Paciente
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** STG  
**Tabla:** tb_paciente  
**Commit size:** 1000  
**Truncate table:** Yes

---

### Step 4: Extract Especialista
**Tipo:** Table Input  
**Conexión:** MySQLConexion  
**SQL:**
```sql
SELECT 
    e.run_especialista,
    e.nombres,
    e.apellidos,
    a.nombre_area as especialidad,
    a.nombre_area as area_medica,
    ee.nombre_estado as estado,
    e.fono as telefono,
    e.email as correo
FROM especialista e
INNER JOIN area a ON e.id_area = a.id_area
INNER JOIN estado_especialista ee ON e.id_estado_espec = ee.id_estado_espec
ORDER BY e.run_especialista
```

### Step 5: Sort Especialista
**Tipo:** Sort rows  
**Campos a ordenar:** run_especialista (Ascending)

### Step 6: Output Especialista
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** STG  
**Tabla:** tb_especialista  
**Commit size:** 1000  
**Truncate table:** Yes

---

### Step 7: Extract Alta Medica (COMPLEJO)
**Tipo:** Table Input  
**Conexión:** MySQLConexion  
**SQL:**
```sql
SELECT 
    -- Claves de negocio
    am.run_paciente,
    am.run_especialista,
    
    -- Información del alta
    am.numero_certificado,
    am.codigo_unico_nacional,
    am.tipo_formulario,
    IFNULL(cca.nombre_calificacion, 'Sin Calificación') as calificacion,
    IFNULL(cma.descripcion_motivo, 'Sin Motivo') as motivo_alta,
    CASE 
        WHEN cma.descripcion_motivo LIKE '%mejor%' THEN 'Recuperación'
        WHEN cma.descripcion_motivo LIKE '%fallec%' THEN 'Fallecimiento'
        WHEN cma.descripcion_motivo LIKE '%traslad%' THEN 'Traslado'
        WHEN cma.descripcion_motivo LIKE '%volunt%' THEN 'Alta Voluntaria'
        ELSE 'Otro'
    END as categoria_motivo,
    
    -- Condiciones del paciente
    am.es_menor_edad,
    am.persona_mayor as es_persona_mayor,
    am.discapacidad as tiene_discapacidad,
    am.dependencia_parcial_total as tiene_dependencia,
    am.presume_invalidez,
    CONCAT_WS(', ',
        CASE WHEN am.es_menor_edad = 1 THEN 'Menor de edad' END,
        CASE WHEN am.persona_mayor = 1 THEN 'Persona mayor' END,
        CASE WHEN am.discapacidad = 1 THEN 'Con discapacidad' END,
        CASE WHEN am.dependencia_parcial_total = 1 THEN 'Con dependencia' END,
        CASE WHEN am.presume_invalidez = 1 THEN 'Presume invalidez' END,
        'Normal'
    ) as descripcion_condicion,
    
    -- Información de hospitalización
    IFNULL(tc.nombre_tipo_camilla, 'Sin hospitalización') as tipo_camilla,
    IFNULL(eh.nombre_estado, 'N/A') as estado_hospitalizacion,
    CASE 
        WHEN h.motivo LIKE '%emerg%' THEN 'Emergencia'
        WHEN h.motivo LIKE '%program%' THEN 'Programada'
        WHEN h.motivo LIKE '%urgent%' THEN 'Urgencia'
        ELSE 'Otro'
    END as categoria_motivo_hosp,
    
    -- Métricas
    IFNULL(DATEDIFF(h.fecha_real_alta, h.fecha_ingreso), 0) as dias_hospitalizacion,
    YEAR(am.fecha_alta) - YEAR(p.fecha_nac) - 
        (DATE_FORMAT(am.fecha_alta, '%m%d') < DATE_FORMAT(p.fecha_nac, '%m%d')) as edad_paciente_al_alta,
    
    -- Indicadores
    CASE WHEN am.id_hospitalizacion IS NOT NULL THEN 1 ELSE 0 END as tiene_hospitalizacion,
    CASE WHEN am.resp_legal_rut IS NOT NULL AND am.resp_legal_rut != '' THEN 1 ELSE 0 END as tiene_responsable_legal,
    CASE WHEN am.empleador_rut IS NOT NULL AND am.empleador_rut != '' THEN 1 ELSE 0 END as tiene_empleador,
    CASE WHEN am.codigo_unico_nacional IS NOT NULL AND am.codigo_unico_nacional != '' THEN 1 ELSE 0 END as tiene_codigo_unico,
    CASE WHEN am.fecha_diat_diep IS NOT NULL THEN 1 ELSE 0 END as tiene_diat_diep,
    
    -- Fechas
    am.fecha_emision_certificado as fecha_emision,
    am.fecha_alta,
    am.fecha_diat_diep

FROM alta_medica am
INNER JOIN paciente p ON am.run_paciente = p.run
INNER JOIN especialista e ON am.run_especialista = e.run_especialista
LEFT JOIN hospitalizacion h ON am.id_hospitalizacion = h.id_hospitalizacion
LEFT JOIN camilla c ON h.id_camilla = c.id_camilla
LEFT JOIN tipo_camilla tc ON c.id_tipo_camilla = tc.id_tipo_camilla
LEFT JOIN estado_hospitalizacion eh ON h.id_estado_hospitalizacion = eh.id_estado_hosp
LEFT JOIN catalogo_calificacion_alta cca ON am.id_calificacion = cca.id_calificacion
LEFT JOIN catalogo_motivo_alta cma ON am.id_motivo_alta = cma.id_motivo_alta
ORDER BY am.id_alta_medica
```

### Step 8: Calculator - Dias desde emision
**Tipo:** Calculator  
**Cálculo:** dias_desde_emision_hasta_alta = fecha_alta - fecha_emision (resultado en días)

### Step 9: Select Values
**Tipo:** Select & Alter  
**Seleccionar todos los campos necesarios para STG.tb_alta_medica**

### Step 10: Output Alta Medica
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** STG  
**Tabla:** tb_alta_medica  
**Commit size:** 1000  
**Truncate table:** Yes

---

## 2. DWH_Alta_Medica.ktr

### Dimension: Paciente

#### Step 1: Input from Staging
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT DISTINCT
    run_paciente,
    nombres,
    apellidos,
    fecha_nacimiento,
    genero,
    grupo_sanguineo,
    estado_salud,
    telefono,
    correo,
    direccion
FROM STG.tb_paciente
WHERE run_paciente NOT IN (SELECT run_paciente FROM DWH.dim_paciente)
```

#### Step 2: Calculator - Nombre Completo y Edad
**Tipo:** Calculator  
**Cálculos:**
- nombre_completo = nombres + " " + apellidos
- edad = DateDiff(CurrentDate, fecha_nacimiento) / 365

#### Step 3: Output Dimension
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** dim_paciente  
**Commit size:** 1000  
**Truncate table:** No

---

### Dimension: Especialista

#### Step 1: Input from Staging
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT DISTINCT
    run_especialista,
    nombres,
    apellidos,
    especialidad,
    area_medica,
    estado,
    telefono,
    correo
FROM STG.tb_especialista
WHERE run_especialista NOT IN (SELECT run_especialista FROM DWH.dim_especialista)
```

#### Step 2: Calculator - Nombre Completo
**Tipo:** Calculator  
**Cálculo:** nombre_completo = nombres + " " + apellidos

#### Step 3: Output Dimension
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** dim_especialista  
**Commit size:** 1000  
**Truncate table:** No

---

### Dimension: Tiempo

#### Step 1: Generate Dates
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT DISTINCT fecha_alta as fecha FROM STG.tb_alta_medica
UNION
SELECT DISTINCT fecha_emision FROM STG.tb_alta_medica
UNION
SELECT DISTINCT fecha_diat_diep FROM STG.tb_alta_medica WHERE fecha_diat_diep IS NOT NULL
```

#### Step 2: Filter Existing
**Tipo:** Database Lookup  
**Lookup:** Verificar si la fecha ya existe en dim_tiempo  
**Acción:** Filtrar solo fechas nuevas

#### Step 3: Calculator - Componentes de Fecha
**Tipo:** Calculator  
**Cálculos:**
- anio = Year(fecha)
- mes = Month(fecha)
- dia = Day(fecha)
- dia_semana = DayOfWeek(fecha)
- trimestre = CEIL(mes / 3)
- semestre = CEIL(mes / 6)
- es_fin_semana = (dia_semana = 1 OR dia_semana = 7) ? 1 : 0

#### Step 4: JavaScript - Nombres en Español
**Tipo:** Modified Java Script Value  
**Script:**
```javascript
var meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
var dias = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];

nombre_mes = meses[mes - 1];
nombre_dia = dias[dia_semana - 1];
es_festivo = 0; // Por defecto
```

#### Step 5: Output Dimension
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** dim_tiempo  
**Commit size:** 1000  
**Truncate table:** No

---

### Dimension: Tipo Alta

#### Step 1: Input Distinct Values
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT DISTINCT 
    tipo_formulario,
    calificacion,
    motivo_alta,
    categoria_motivo
FROM STG.tb_alta_medica
```

#### Step 2: Filter Existing
**Tipo:** Database Lookup  
**Lookup:** Verificar si la combinación ya existe  
**Acción:** Filtrar solo combinaciones nuevas

#### Step 3: Output Dimension
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** dim_tipo_alta  
**Commit size:** 1000  
**Truncate table:** No

---

### Dimension: Condición

#### Step 1: Input Distinct Values
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT DISTINCT 
    es_menor_edad,
    es_persona_mayor,
    tiene_discapacidad,
    tiene_dependencia,
    presume_invalidez,
    descripcion_condicion
FROM STG.tb_alta_medica
```

#### Step 2: Filter Existing
**Tipo:** Database Lookup  
**Lookup:** Verificar si la combinación ya existe  
**Acción:** Filtrar solo combinaciones nuevas

#### Step 3: Output Dimension
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** dim_condicion  
**Commit size:** 1000  
**Truncate table:** No

---

### Dimension: Hospitalización

#### Step 1: Input Distinct Values
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT DISTINCT 
    tipo_camilla,
    estado_hospitalizacion,
    categoria_motivo_hosp as categoria_motivo
FROM STG.tb_alta_medica
WHERE tiene_hospitalizacion = 1
```

#### Step 2: Filter Existing
**Tipo:** Database Lookup  
**Lookup:** Verificar si la combinación ya existe  
**Acción:** Filtrar solo combinaciones nuevas

#### Step 3: Output Dimension
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** dim_hospitalizacion  
**Commit size:** 1000  
**Truncate table:** No

---

## 3. FACT_Alta_Medica.ktr

### Step 1: Input from Staging
**Tipo:** Table Input  
**Conexión:** SQLServerConexion  
**SQL:**
```sql
SELECT 
    run_paciente,
    run_especialista,
    tipo_formulario,
    calificacion,
    motivo_alta,
    categoria_motivo,
    es_menor_edad,
    es_persona_mayor,
    tiene_discapacidad,
    tiene_dependencia,
    presume_invalidez,
    tipo_camilla,
    estado_hospitalizacion,
    categoria_motivo_hosp,
    dias_hospitalizacion,
    edad_paciente_al_alta,
    tiene_hospitalizacion,
    tiene_responsable_legal,
    tiene_empleador,
    tiene_codigo_unico,
    tiene_diat_diep,
    numero_certificado,
    codigo_unico_nacional,
    fecha_emision,
    fecha_alta,
    fecha_diat_diep
FROM STG.tb_alta_medica
```

### Step 2: Lookup id_dim_paciente
**Tipo:** Database Lookup  
**Conexión:** SQLServerConexion  
**Tabla:** DWH.dim_paciente  
**Lookup field:** run_paciente = run_paciente  
**Return field:** id_dim_paciente

### Step 3: Lookup id_dim_especialista
**Tipo:** Database Lookup  
**Conexión:** SQLServerConexion  
**Tabla:** DWH.dim_especialista  
**Lookup field:** run_especialista = run_especialista  
**Return field:** id_dim_especialista

### Step 4: Lookup id_dim_tiempo
**Tipo:** Database Lookup  
**Conexión:** SQLServerConexion  
**Tabla:** DWH.dim_tiempo  
**Lookup field:** fecha = fecha_alta  
**Return field:** id_dim_tiempo

### Step 5: Lookup id_dim_tipo_alta
**Tipo:** Database Lookup  
**Conexión:** SQLServerConexion  
**Tabla:** DWH.dim_tipo_alta  
**Lookup fields:**
- tipo_formulario = tipo_formulario
- calificacion = calificacion
- motivo_alta = motivo_alta
- categoria_motivo = categoria_motivo  
**Return field:** id_dim_tipo_alta

### Step 6: Lookup id_dim_condicion
**Tipo:** Database Lookup  
**Conexión:** SQLServerConexion  
**Tabla:** DWH.dim_condicion  
**Lookup fields:**
- es_menor_edad = es_menor_edad
- es_persona_mayor = es_persona_mayor
- tiene_discapacidad = tiene_discapacidad
- tiene_dependencia = tiene_dependencia
- presume_invalidez = presume_invalidez  
**Return field:** id_dim_condicion

### Step 7: Lookup id_dim_hospitalizacion
**Tipo:** Database Lookup  
**Conexión:** SQLServerConexion  
**Tabla:** DWH.dim_hospitalizacion  
**Lookup fields:**
- tipo_camilla = tipo_camilla
- estado_hospitalizacion = estado_hospitalizacion
- categoria_motivo = categoria_motivo_hosp  
**Return field:** id_dim_hospitalizacion  
**Nota:** Este lookup puede retornar NULL si no hay hospitalización

### Step 8: Calculator - Dias desde emision
**Tipo:** Calculator  
**Cálculo:** dias_desde_emision_hasta_alta = DateDiff(fecha_alta, fecha_emision)

### Step 9: Select Values
**Tipo:** Select & Alter  
**Seleccionar solo los campos necesarios para la fact table:**
- id_dim_paciente
- id_dim_especialista
- id_dim_tiempo
- id_dim_tipo_alta
- id_dim_condicion
- id_dim_hospitalizacion
- dias_hospitalizacion
- edad_paciente_al_alta
- dias_desde_emision_hasta_alta
- tiene_hospitalizacion
- tiene_responsable_legal
- tiene_empleador
- tiene_codigo_unico
- tiene_diat_diep
- numero_certificado
- codigo_unico_nacional
- fecha_emision
- fecha_alta
- fecha_diat_diep

### Step 10: Output Fact Table
**Tipo:** Table Output  
**Conexión:** SQLServerConexion  
**Esquema:** DWH  
**Tabla:** fact_alta_medica  
**Commit size:** 1000  
**Truncate table:** No

---

## Orden de Ejecución

1. **Primero:** Ejecutar `STG_Alta_Medica.ktr` para poblar las tablas de staging
2. **Segundo:** Ejecutar `DWH_Alta_Medica.ktr` para poblar las dimensiones
3. **Tercero:** Ejecutar `FACT_Alta_Medica.ktr` para poblar la tabla de hechos

## Notas Importantes

- **Truncate:** Solo las tablas de staging se truncan en cada ejecución
- **Dimensiones:** Se cargan en modo incremental (solo registros nuevos)
- **Fact Table:** Se carga en modo incremental
- **Commit Size:** 1000 registros por lote para optimizar rendimiento
- **Manejo de NULLs:** Usar IFNULL/COALESCE en las queries MySQL
- **Lookups:** Configurar "Default value" para manejar lookups fallidos

## Validación Post-Ejecución

```sql
-- Verificar conteo de registros
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

-- Verificar integridad referencial
SELECT COUNT(*) as registros_huerfanos_paciente
FROM DWH.fact_alta_medica f
WHERE NOT EXISTS (SELECT 1 FROM DWH.dim_paciente p WHERE p.id_dim_paciente = f.id_dim_paciente);

SELECT COUNT(*) as registros_huerfanos_especialista
FROM DWH.fact_alta_medica f
WHERE NOT EXISTS (SELECT 1 FROM DWH.dim_especialista e WHERE e.id_dim_especialista = f.id_dim_especialista);
```
