
from datetime import datetime, timedelta
import faker
from Conexion import Conexion
import random

class Creacion_bd_alta_medica:
    def __init__(self):
        self.faker = faker.Faker('es_CL')
        self.limpiar_tablas()
        self.definir_datos_estaticos()
        
    def limpiar_tablas(self):
        print("Limpiando tablas...")
        db = Conexion()
        # Orden de eliminación importante por claves foráneas
        tablas = [
            "examen", "registro_medico", "alta_medica", "hospitalizacion", 
            "alergia_paciente", "camilla", "paciente", "especialista",
            "area", "estado_especialista", "genero", "grupo_sanguineo",
            "estado_salud", "tipo_alergia", "tipo_camilla", "tipo_examen",
            "estado_en_consulta", "estado_hospitalizacion", 
            "catalogo_motivo_alta", "catalogo_calificacion_alta"
        ]
        for tabla in tablas:
            try:
                db.cursor.execute(f"DELETE FROM {tabla}")
                db.conn.commit()
                db.cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")
                db.conn.commit()
            except Exception as e:
                print(f"Error limpiando tabla {tabla}: {e}")
        if db.conn:
            db.conn.close()
        print("Tablas limpiadas correctamente.")

    def definir_datos_estaticos(self):
        self.areas = ["Cardiología", "Neurología", "Pediatría", "Urgencias", "Traumatología", "Medicina General", "Oncología", "Ginecología"]
        # Pesos para áreas más demandadas (Urgencias, Medicina General, Traumatología)
        self.areas_pesos = [15, 10, 12, 25, 18, 20, 8, 12]  # Total: 120
        
        self.estados_especialista = ["Activo", "Inactivo", "Vacaciones", "Licencia"]
        self.estados_especialista_pesos = [80, 5, 10, 5]  # 80% activos
        
        self.generos = ["Masculino", "Femenino"]
        self.grupos_sanguineos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.grupos_pesos = [35, 8, 25, 7, 5, 2, 15, 3]  # O+ y A+ más comunes
        
        self.estados_salud = ["Sano", "En Tratamiento", "Crónico", "Grave", "Recuperación"]
        self.tipos_alergia = [
            ("Polen", "Alergia estacional común"), 
            ("Penicilina", "Reacción a antibióticos"), 
            ("Maní", "Alergia alimentaria severa"), 
            ("Látex", "Alergia de contacto"),
            ("Polvo", "Alergia ambiental"),
            ("Mariscos", "Alergia alimentaria")
        ]
        self.tipos_camilla = ["Estándar", "Quirúrgica", "UCI", "Pediatrica", "Ginecológica"]
        self.tipos_camilla_pesos = [50, 20, 10, 12, 8]  # Más camillas estándar
        
        self.tipos_examen = ["Sangre", "Orina", "Rayos X", "Resonancia", "Scanner", "Biopsia"]
        self.tipos_examen_pesos = [40, 30, 15, 5, 7, 3]  # Sangre y orina más comunes
        
        self.estados_consulta = ["Agendada", "En Espera", "En Atención", "Finalizada", "Cancelada"]
        self.estados_consulta_pesos = [15, 10, 5, 65, 5]  # Mayoría finalizadas
        
        self.estados_hospitalizacion = ["Ingresado", "En Observación", "UCI", "UTI", "Pre-Alta", "Alta"]
        self.estados_hosp_pesos = [20, 25, 8, 7, 10, 30]  # Tendencia hacia alta
        
        self.motivos_alta = ["Mejoría", "Traslado", "Fallecimiento", "Alta Voluntaria", "Fuga"]
        self.motivos_alta_pesos = [70, 15, 5, 8, 2]  # Mayoría por mejoría
        
        self.calificaciones_alta = [
            ("Tipo A", "Alta Médica Definitiva"),
            ("Tipo B", "Alta Médica Temporal"),
            ("Tipo C", "Alta por Traslado"),
            ("Tipo D", "Alta Disciplinaria")
        ]

    def cargar_catalogos(self):
        print("Cargando catálogos...")
        db = Conexion()
        
        # Area
        db.cursor.executemany("INSERT INTO area (nombre_area) VALUES (%s)", [(x,) for x in self.areas])
        
        # Estado Especialista
        db.cursor.executemany("INSERT INTO estado_especialista (nombre_estado) VALUES (%s)", [(x,) for x in self.estados_especialista])
        
        # Genero
        db.cursor.executemany("INSERT INTO genero (nombre_genero) VALUES (%s)", [(x,) for x in self.generos])
        
        # Grupo Sanguineo
        db.cursor.executemany("INSERT INTO grupo_sanguineo (nombre_grupo) VALUES (%s)", [(x,) for x in self.grupos_sanguineos])
        
        # Estado Salud
        db.cursor.executemany("INSERT INTO estado_salud (nombre_estado_salud) VALUES (%s)", [(x,) for x in self.estados_salud])
        
        # Tipo Alergia
        db.cursor.executemany("INSERT INTO tipo_alergia (nombre_alergia, descripcion) VALUES (%s, %s)", self.tipos_alergia)
        
        # Tipo Camilla
        db.cursor.executemany("INSERT INTO tipo_camilla (nombre_tipo_camilla) VALUES (%s)", [(x,) for x in self.tipos_camilla])
        
        # Tipo Examen
        db.cursor.executemany("INSERT INTO tipo_examen (tipo_examen) VALUES (%s)", [(x,) for x in self.tipos_examen])
        
        # Estado En Consulta
        db.cursor.executemany("INSERT INTO estado_en_consulta (nombre_estado_consulta) VALUES (%s)", [(x,) for x in self.estados_consulta])
        
        # Estado Hospitalizacion
        db.cursor.executemany("INSERT INTO estado_hospitalizacion (nombre_estado) VALUES (%s)", [(x,) for x in self.estados_hospitalizacion])
        
        # Catalogo Motivo Alta
        db.cursor.executemany("INSERT INTO catalogo_motivo_alta (descripcion_motivo) VALUES (%s)", [(x,) for x in self.motivos_alta])
        
        # Catalogo Calificacion Alta
        db.cursor.executemany("INSERT INTO catalogo_calificacion_alta (tipo_formulario, nombre_calificacion) VALUES (%s, %s)", self.calificaciones_alta)
        
        db.conn.commit()
        db.conn.close()
        print("Catálogos cargados correctamente.")

    def cargar_especialistas(self, cantidad=50):
        print("Cargando especialistas...")
        db = Conexion()
        
        db.cursor.execute("SELECT id_area FROM area")
        areas = [x['id_area'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_estado_espec FROM estado_especialista")
        estados = [x['id_estado_espec'] for x in db.cursor.fetchall()]
        
        datos = []
        ruts_usados = set()
        batch_size = 1000
        
        for i in range(cantidad):
            while True:
                rut = self.faker.rut()
                if rut not in ruts_usados:
                    ruts_usados.add(rut)
                    break
            
            # Distribución ponderada de áreas (más especialistas en áreas demandadas)
            id_area = random.choices(areas, weights=self.areas_pesos[:len(areas)], k=1)[0]
            # Distribución ponderada de estados (80% activos)
            id_estado = random.choices(estados, weights=self.estados_especialista_pesos[:len(estados)], k=1)[0]
            
            sexo = random.choice(['M', 'F'])
            if sexo == 'M':
                nombres = f"{self.faker.first_name_male()} {self.faker.first_name_male()}"
            else:
                nombres = f"{self.faker.first_name_female()} {self.faker.first_name_female()}"
            apellidos = f"{self.faker.last_name()} {self.faker.last_name()}"
            fono = self.faker.phone_number()
            direccion = self.faker.address()
            email = self.faker.email()
            
            datos.append((rut, id_area, id_estado, nombres, apellidos, fono, direccion, email))
            
            # Insertar en lotes
            if (i + 1) % batch_size == 0 or (i + 1) == cantidad:
                db.cursor.executemany("""
                    INSERT INTO especialista (run_especialista, id_area, id_estado_espec, nombres, apellidos, fono, direccion, email) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, datos)
                db.conn.commit()
                print(f"  Insertados {i + 1}/{cantidad} especialistas...")
                datos = []
        
        db.conn.close()
        print("Especialistas cargados correctamente.")

    def cargar_pacientes(self, cantidad=200):
        print("Cargando pacientes...")
        db = Conexion()
        
        db.cursor.execute("SELECT id_genero FROM genero")
        generos = [x['id_genero'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT nombre_grupo FROM grupo_sanguineo")
        grupos = [x['nombre_grupo'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_estado_salud FROM estado_salud")
        estados = [x['id_estado_salud'] for x in db.cursor.fetchall()]
        
        datos = []
        ruts_usados = set()
        batch_size = 1000
        
        for i in range(cantidad):
            while True:
                rut = self.faker.rut()
                if rut not in ruts_usados:
                    ruts_usados.add(rut)
                    break
            
            nombres = self.faker.first_name() + " " + self.faker.first_name()
            apellidos = self.faker.last_name() + " " + self.faker.last_name()
            
            # Distribución de edades con tendencia: más pacientes entre 20-60 años
            edad_grupo = random.choices([0, 1, 2, 3], weights=[15, 50, 25, 10], k=1)[0]
            if edad_grupo == 0:  # Niños y adolescentes
                fecha_nac = self.faker.date_of_birth(minimum_age=0, maximum_age=18)
            elif edad_grupo == 1:  # Adultos jóvenes y mediana edad
                fecha_nac = self.faker.date_of_birth(minimum_age=19, maximum_age=50)
            elif edad_grupo == 2:  # Adultos mayores
                fecha_nac = self.faker.date_of_birth(minimum_age=51, maximum_age=70)
            else:  # Ancianos
                fecha_nac = self.faker.date_of_birth(minimum_age=71, maximum_age=95)
            
            # Calcular edad para determinar estado de salud
            edad = (datetime.now().date() - fecha_nac).days // 365
            
            id_genero = random.choice(generos)
            # Distribución ponderada de grupos sanguíneos
            grupo_sang = random.choices(grupos, weights=self.grupos_pesos[:len(grupos)], k=1)[0]
            
            # Estado de salud correlacionado con edad (mayores más propensos a condiciones crónicas)
            if edad < 18:
                estado_pesos = [70, 20, 5, 2, 3]  # Niños mayormente sanos
            elif edad < 50:
                estado_pesos = [50, 30, 10, 5, 5]  # Adultos jóvenes
            elif edad < 70:
                estado_pesos = [20, 35, 25, 10, 10]  # Adultos mayores
            else:
                estado_pesos = [10, 30, 40, 15, 5]  # Ancianos con más condiciones crónicas
            
            id_estado = random.choices(estados, weights=estado_pesos[:len(estados)], k=1)[0]
            
            fono = self.faker.phone_number()
            fono_alt = self.faker.phone_number()
            direccion = self.faker.address()
            email = self.faker.email()
            
            datos.append((rut, nombres, apellidos, fecha_nac, id_genero, grupo_sang, id_estado, fono, fono_alt, direccion, email))
            
            # Insertar en lotes
            if (i + 1) % batch_size == 0 or (i + 1) == cantidad:
                db.cursor.executemany("""
                    INSERT INTO paciente (run, nombres, apellidos, fecha_nac, id_genero, grupo_sang, id_estado_salud, fono, fono_alt, direccion, email) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, datos)
                db.conn.commit()
                print(f"  Insertados {i + 1}/{cantidad} pacientes...")
                datos = []
        
        db.conn.close()
        print("Pacientes cargados correctamente.")

    def cargar_camillas(self, cantidad=50):
        print("Cargando camillas...")
        db = Conexion()
        
        db.cursor.execute("SELECT id_tipo_camilla FROM tipo_camilla")
        tipos = [x['id_tipo_camilla'] for x in db.cursor.fetchall()]
        
        datos = []
        for i in range(cantidad):
            # Distribución ponderada de tipos de camilla
            id_tipo = random.choices(tipos, weights=self.tipos_camilla_pesos[:len(tipos)], k=1)[0]
            nombre = f"Camilla-{i+1:03d}"
            datos.append((id_tipo, nombre))
            
        db.cursor.executemany("INSERT INTO camilla (id_tipo_camilla, nombre_camilla) VALUES (%s, %s)", datos)
        db.conn.commit()
        db.conn.close()
        print("Camillas cargadas correctamente.")

    def cargar_alergias_pacientes(self, cantidad=100):
        print("Cargando alergias de pacientes...")
        db = Conexion()
        
        db.cursor.execute("SELECT run FROM paciente")
        pacientes = [x['run'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_tipo_alergia FROM tipo_alergia")
        alergias = [x['id_tipo_alergia'] for x in db.cursor.fetchall()]
        
        datos = []
        asignados = set()
        batch_size = 1000
        
        for i in range(cantidad):
            while True:
                paciente = random.choice(pacientes)
                alergia = random.choice(alergias)
                if (paciente, alergia) not in asignados:
                    asignados.add((paciente, alergia))
                    break
            
            severidad = random.choice(["Leve", "Moderada", "Severa", "Mortal"])
            fecha = self.faker.date_this_decade()
            observaciones = self.faker.sentence()
            
            datos.append((paciente, alergia, severidad, fecha, observaciones))
            
            # Insertar en lotes
            if (i + 1) % batch_size == 0 or (i + 1) == cantidad:
                db.cursor.executemany("""
                    INSERT INTO alergia_paciente (run_paciente, id_tipo_alergia, severidad, fecha_deteccion, observaciones) 
                    VALUES (%s, %s, %s, %s, %s)
                """, datos)
                db.conn.commit()
                print(f"  Insertadas {i + 1}/{cantidad} alergias...")
                datos = []
        
        db.conn.close()
        print("Alergias de pacientes cargadas correctamente.")

    def cargar_hospitalizaciones(self, cantidad=100):
        print("Cargando hospitalizaciones...")
        db = Conexion()
        
        db.cursor.execute("SELECT run, fecha_nac FROM paciente")
        pacientes = db.cursor.fetchall()
        
        db.cursor.execute("SELECT run_especialista FROM especialista")
        especialistas = [x['run_especialista'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_camilla FROM camilla")
        camillas = [x['id_camilla'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_estado_hosp FROM estado_hospitalizacion")
        estados = [x['id_estado_hosp'] for x in db.cursor.fetchall()]
        
        datos = []
        batch_size = 1000
        
        for i in range(cantidad):
            # Pacientes mayores tienen más probabilidad de hospitalización
            paciente_data = random.choice(pacientes)
            paciente = paciente_data['run']
            edad = (datetime.now().date() - paciente_data['fecha_nac']).days // 365
            
            especialista = random.choice(especialistas)
            camilla = random.choice(camillas)
            
            # Distribución ponderada de estados
            estado = random.choices(estados, weights=self.estados_hosp_pesos[:len(estados)], k=1)[0]
            
            motivo = self.faker.text(max_nb_chars=100)
            observaciones = self.faker.text(max_nb_chars=100)
            
            # Tendencia estacional: más hospitalizaciones en invierno (junio-agosto)
            mes = random.choices(
                range(1, 13),
                weights=[8, 8, 9, 10, 11, 15, 14, 12, 10, 9, 8, 6],  # Pico en junio-julio
                k=1
            )[0]
            
            año = random.choices([2023, 2024, 2025], weights=[20, 40, 40], k=1)[0]  # Más recientes
            fecha_ingreso = self.faker.date_time_between(
                start_date=datetime(año, mes, 1),
                end_date=datetime(año, mes, 28) if mes == 2 else datetime(año, mes, 30 if mes in [4,6,9,11] else 31)
            )
            
            # Duración de hospitalización correlacionada con edad
            if edad < 18:
                dias_estadia = random.randint(1, 7)
            elif edad < 50:
                dias_estadia = random.randint(2, 15)
            elif edad < 70:
                dias_estadia = random.randint(3, 25)
            else:
                dias_estadia = random.randint(5, 40)
            
            fecha_estimada = fecha_ingreso + timedelta(days=dias_estadia)
            
            # 72% de probabilidad de alta (más realista)
            fecha_real = None
            if random.random() > 0.28:
                fecha_real = fecha_estimada + timedelta(days=random.randint(-3, 7))
            
            datos.append((paciente, especialista, camilla, estado, motivo, observaciones, fecha_ingreso, fecha_estimada, fecha_real))
            
            # Insertar en lotes
            if (i + 1) % batch_size == 0 or (i + 1) == cantidad:
                db.cursor.executemany("""
                    INSERT INTO hospitalizacion (run_paciente, run_especialista, id_camilla, id_estado_hospitalizacion, motivo, observaciones, fecha_ingreso, fecha_estimada_alta, fecha_real_alta) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, datos)
                db.conn.commit()
                print(f"  Insertadas {i + 1}/{cantidad} hospitalizaciones...")
                datos = []
        
        db.conn.close()
        print("Hospitalizaciones cargadas correctamente.")

    def cargar_registros_medicos(self, cantidad=300):
        print("Cargando registros médicos...")
        db = Conexion()
        
        db.cursor.execute("SELECT run, fecha_nac FROM paciente")
        pacientes = db.cursor.fetchall()
        
        db.cursor.execute("SELECT run_especialista FROM especialista")
        especialistas = [x['run_especialista'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_estado_consulta FROM estado_en_consulta")
        estados = [x['id_estado_consulta'] for x in db.cursor.fetchall()]
        
        datos = []
        batch_size = 1000
        
        for i in range(cantidad):
            paciente_data = random.choice(pacientes)
            paciente = paciente_data['run']
            edad = (datetime.now().date() - paciente_data['fecha_nac']).days // 365
            
            especialista = random.choice(especialistas)
            
            # Tendencia temporal: crecimiento de consultas en últimos años
            año = random.choices([2022, 2023, 2024, 2025], weights=[10, 20, 35, 35], k=1)[0]
            # Tendencia estacional: más consultas en otoño-invierno
            mes = random.choices(
                range(1, 13),
                weights=[9, 9, 10, 11, 12, 14, 13, 11, 10, 9, 8, 4],  # Pico mayo-julio
                k=1
            )[0]
            
            fecha = self.faker.date_time_between(
                start_date=datetime(año, mes, 1),
                end_date=datetime(año, mes, 28) if mes == 2 else datetime(año, mes, 30 if mes in [4,6,9,11] else 31)
            )
            
            # Distribución ponderada de estados
            id_estado = random.choices(estados, weights=self.estados_consulta_pesos[:len(estados)], k=1)[0]
            
            motivo = self.faker.sentence()
            diagnostico = self.faker.text(max_nb_chars=200)
            resultado = self.faker.text(max_nb_chars=100)
            notas = self.faker.text(max_nb_chars=100)
            
            # Peso y altura correlacionados con edad
            if edad < 12:
                peso = round(random.uniform(15.0, 50.0), 2)
                altura = round(random.uniform(0.80, 1.50), 2)
            elif edad < 18:
                peso = round(random.uniform(40.0, 80.0), 2)
                altura = round(random.uniform(1.40, 1.85), 2)
            else:
                peso = round(random.uniform(50.0, 110.0), 2)
                altura = round(random.uniform(1.50, 1.95), 2)
            
            # Signos vitales con variación realista
            pa_sistolica = random.randint(90, 160) if edad > 50 else random.randint(100, 140)
            pa_diastolica = random.randint(60, 100) if edad > 50 else random.randint(60, 90)
            fc = random.randint(50, 110)
            signos = f"PA: {pa_sistolica}/{pa_diastolica}, FC: {fc}"
            
            datos.append((paciente, especialista, fecha, id_estado, motivo, diagnostico, resultado, notas, peso, altura, signos))
            
            # Insertar en lotes
            if (i + 1) % batch_size == 0 or (i + 1) == cantidad:
                db.cursor.executemany("""
                    INSERT INTO registro_medico (run_paciente, run_especialista, fecha_hora_atencion, id_estado_en_consulta, motivo_consulta, diagnostico, resultado_consulta, notas, peso, altura, signos_vitales) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, datos)
                db.conn.commit()
                print(f"  Insertados {i + 1}/{cantidad} registros médicos...")
                datos = []
        
        db.conn.close()
        print("Registros médicos cargados correctamente.")

    def cargar_examenes(self, cantidad=200):
        print("Cargando exámenes...")
        db = Conexion()
        
        db.cursor.execute("SELECT id_registro_med, fecha_hora_atencion FROM registro_medico")
        registros = db.cursor.fetchall()
        
        db.cursor.execute("SELECT id_tipo_examen FROM tipo_examen")
        tipos = [x['id_tipo_examen'] for x in db.cursor.fetchall()]
        
        datos = []
        batch_size = 1000
        
        for i in range(cantidad):
            registro_data = random.choice(registros)
            id_registro = registro_data['id_registro_med']
            fecha_consulta = registro_data['fecha_hora_atencion']
            
            # Distribución ponderada de tipos de examen (sangre y orina más comunes)
            id_tipo = random.choices(tipos, weights=self.tipos_examen_pesos[:len(tipos)], k=1)[0]
            
            nombre = f"Examen {self.faker.word()}"
            detalle = self.faker.sentence()
            resultado = self.faker.text(max_nb_chars=100)
            
            # Fecha de examen cercana a la fecha de consulta (0-7 días después)
            fecha = fecha_consulta + timedelta(days=random.randint(0, 7))
            
            datos.append((id_registro, id_tipo, nombre, detalle, resultado, fecha))
            
            # Insertar en lotes
            if (i + 1) % batch_size == 0 or (i + 1) == cantidad:
                db.cursor.executemany("""
                    INSERT INTO examen (id_registro_med, id_tipo_examen, nombre_examen, detalle, resultado, fecha_examen) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, datos)
                db.conn.commit()
                print(f"  Insertados {i + 1}/{cantidad} exámenes...")
                datos = []
        
        db.conn.close()
        print("Exámenes cargados correctamente.")

    def cargar_altas_medicas(self, cantidad=50):
        print("Cargando altas médicas...")
        db = Conexion()
        
        # Obtener hospitalizaciones que tienen fecha real de alta (ya fueron dados de alta)
        db.cursor.execute("""
            SELECT h.id_hospitalizacion, h.run_paciente, h.run_especialista, h.fecha_real_alta, p.fecha_nac
            FROM hospitalizacion h
            JOIN paciente p ON h.run_paciente = p.run
            WHERE h.fecha_real_alta IS NOT NULL
        """)
        hospitalizaciones = db.cursor.fetchall()
        
        db.cursor.execute("SELECT id_calificacion FROM catalogo_calificacion_alta")
        calificaciones = [x['id_calificacion'] for x in db.cursor.fetchall()]
        
        db.cursor.execute("SELECT id_motivo_alta FROM catalogo_motivo_alta")
        motivos = [x['id_motivo_alta'] for x in db.cursor.fetchall()]
        
        datos = []
        batch_size = 1000
        # Usar las hospitalizaciones disponibles, si hay menos que la cantidad solicitada, usar todas
        to_process = hospitalizaciones[:cantidad] if len(hospitalizaciones) > cantidad else hospitalizaciones
        
        for idx, hosp in enumerate(to_process):
            run_paciente = hosp['run_paciente']
            run_especialista = hosp['run_especialista']
            id_hosp = hosp['id_hospitalizacion']
            fecha_alta = hosp['fecha_real_alta']
            edad = (datetime.now().date() - hosp['fecha_nac']).days // 365
            
            tipo_form = random.choices(["Form A", "Form B"], weights=[70, 30], k=1)[0]
            num_cert = self.faker.uuid4()
            fecha_emision = fecha_alta
            cod_unico = self.faker.ean13()
            id_calif = random.choice(calificaciones)
            detalle_calif = self.faker.sentence()
            fecha_diat = self.faker.date_this_year()
            
            # Condiciones correlacionadas con edad
            es_menor = 1 if edad < 18 else 0
            persona_mayor = 1 if edad >= 65 else 0
            
            # Dependencia y discapacidad más común en mayores
            if edad >= 70:
                dep_parcial = random.choices([0, 1], weights=[40, 60], k=1)[0]
                discapacidad = random.choices([0, 1], weights=[50, 50], k=1)[0]
            elif edad >= 50:
                dep_parcial = random.choices([0, 1], weights=[70, 30], k=1)[0]
                discapacidad = random.choices([0, 1], weights=[80, 20], k=1)[0]
            else:
                dep_parcial = random.choices([0, 1], weights=[90, 10], k=1)[0]
                discapacidad = random.choices([0, 1], weights=[95, 5], k=1)[0]
            
            otra_cond = self.faker.sentence() if random.random() > 0.75 else None
            
            resp_nombres = self.faker.name()
            resp_rut = self.faker.rut()
            resp_dir = self.faker.address()
            resp_comuna = self.faker.city()
            resp_fono = self.faker.phone_number()
            
            emp_razon = self.faker.company()
            emp_rut = self.faker.rut()
            emp_dir = self.faker.address()
            emp_comuna = self.faker.city()
            
            # Distribución ponderada de motivos de alta (mayoría por mejoría)
            id_motivo = random.choices(motivos, weights=self.motivos_alta_pesos[:len(motivos)], k=1)[0]
            detalle_motivo = self.faker.sentence()
            
            # Presunción de invalidez más común en mayores con discapacidad
            if discapacidad == 1 and edad >= 50:
                presume_inv = random.choices([0, 1], weights=[30, 70], k=1)[0]
            else:
                presume_inv = random.choices([0, 1], weights=[90, 10], k=1)[0]
            
            firma = self.faker.name()
            
            datos.append((
                run_paciente, run_especialista, id_hosp, tipo_form, num_cert, fecha_emision,
                cod_unico, id_calif, detalle_calif, fecha_diat, es_menor, dep_parcial,
                discapacidad, persona_mayor, otra_cond, resp_nombres, resp_rut, resp_dir,
                resp_comuna, resp_fono, emp_razon, emp_rut, emp_dir, emp_comuna,
                id_motivo, detalle_motivo, presume_inv, fecha_alta, firma
            ))
            
            # Insertar en lotes
            if (idx + 1) % batch_size == 0 or (idx + 1) == len(to_process):
                db.cursor.executemany("""
                    INSERT INTO alta_medica (
                        run_paciente, run_especialista, id_hospitalizacion, tipo_formulario, numero_certificado,
                        fecha_emision_certificado, codigo_unico_nacional, id_calificacion, detalle_calificacion,
                        fecha_diat_diep, es_menor_edad, dependencia_parcial_total, discapacidad, persona_mayor,
                        otra_condicion, resp_legal_nombres, resp_legal_rut, resp_legal_direccion, resp_legal_comuna,
                        resp_legal_fono, empleador_razon_social, empleador_rut, empleador_direccion, empleador_comuna,
                        id_motivo_alta, detalle_motivo, presume_invalidez, fecha_alta, firma_medico
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, datos)
                db.conn.commit()
                print(f"  Insertadas {idx + 1}/{len(to_process)} altas médicas...")
                datos = []
        
        db.conn.close()
        print(f"Altas médicas cargadas correctamente ({len(to_process)} registros).")

# Ejecución
if __name__ == "__main__":
    creador = Creacion_bd_alta_medica()
    creador.cargar_catalogos()
    creador.cargar_especialistas(200)
    creador.cargar_pacientes(5000)
    creador.cargar_camillas(300)
    creador.cargar_alergias_pacientes(8000)
    creador.cargar_hospitalizaciones(25000)
    creador.cargar_registros_medicos(150000)
    creador.cargar_examenes(400000)
    creador.cargar_altas_medicas(18000)
    print("Proceso finalizado con éxito.")
