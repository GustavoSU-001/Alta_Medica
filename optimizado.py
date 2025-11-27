
from datetime import datetime
import faker
from conexion import Conexion

class Creacion_bd_uni:
    def __init__(self):
        self.faker = faker.Faker('es_CL')
        self.limpiar_tablas()
        
    def limpiar_tablas(self):
        print("Limpiando tablas...")
        db = Conexion()
        tablas = [
            "evaluacion", "curso_alumno", "alumno",
            "titulo_profesor", "profesor_curso", "profesor", "titulo",
            "curso_tipo_clase", "tipo_clase",
            "curso_Sala", "sala", "curso",
            "carrera"
        ]
        for tabla in tablas:
            db.cursor.execute(f"DELETE FROM {tabla}")
            db.conn.commit()
            db.cursor.execute(f"ALTER TABLE {tabla} AUTO_INCREMENT = 1")
            db.conn.commit()
        db.conn.close()
        print("Tablas limpiadas correctamente.")
        
    
    def Cargar_datos(self):
        print("Cargando datos estáticos...")
        self.Especialidades ={
            "Administración": ['Ingeniero Comercial', 'Administrador de Empresas', 'Técnico en Recursos Humanos', 'Ingeniero en Gestión de Operaciones', 
                                'Licenciado en Administración Pública', 'Técnico en Asistencia Ejecutiva', 'Licenciado en Relaciones Internacionales', 
                                'Ingeniero en Gestión de Calidad', 'Técnico en Secretariado', 'Ingeniero en Productividad y Procesos', 'Licenciado en Gestión del Turismo', 
                                'Técnico en Hotelería', 'Licenciado en Ciencias Políticas', 'Ingeniero en Prevención y Control de Pérdidas'
                               ],
            "Artes": ['Licenciado en Artes Visuales', 'Director Audiovisual', 'Técnico en Fotografía Profesional', 'Técnico en Animación Digital', 
                        'Licenciado en Danza', 'Técnico en Desarrollo de Videojuegos', 'Licenciado en Actuación', 'Técnico en Escenografía'
                        ],
            "Ciencias": ['Bioquímico', 'Licenciado en Química', 'Licenciado en Física', 'Licenciado en Matemáticas', 'Licenciado en Biología Marina', 
                        'Licenciado en Astronomía', 'Técnico en Geomática', 'Licenciado en Geografía', 'Licenciado en Geología', 'Licenciado en Matemáticas Puras'
                        ],
            "Comercio": ['Técnico en Comercio Exterior', 'Ingeniero en Comercio Internacional', 'Magíster en Negocios Internacionales'
                        ],  
            "Comunicaciones": ['Periodista', 'Publicista', 'Técnico en Comunicación Audiovisual', 'Periodista Deportivo', 'Licenciado en Relaciones Públicas'
                                ],
            "Contabilidad": ['Contador Auditor', 'Técnico en Contabilidad General', 'Contador General'
                            ],
            "Derecho": ['Abogado', 'Licenciado en Ciencias Jurídicas', 'Abogado en Derecho Tributario', 'Técnico Jurídico'
                        ],
            "Diseño": ['Diseñador Gráfico', 'Diseñador Web', 'Diseñador Industrial', 'Diseñador de Modas', 'Técnico en Ilustración', 'Diseñador de Interiores', 'Diseñador UX/UI'
                        ],
            "Economía": ['Economista'],
            "Educación": ['Profesor de Enseñanza Básica', 'Profesor de Enseñanza Media (Historia)', 'Técnico en Educación Parvularia', 'Profesor de Lenguaje y Comunicación', 
                            'Profesor de Inglés', 'Profesor de Música', 'Profesor de Matemáticas', 'Profesor de Educación Física'
                            ],
            "Finanzas": ['Licenciado en Finanzas', 'Técnico en Prevención de Fraudes', 'Técnico en Gestión Bancaria', 'Licenciado en Seguros y Riesgos', 
                        'Técnico en Tesorería', 'Licenciado en Inversiones', 'Ingeniero en Administración de Riesgos', 'Técnico en Cajas y Servicios Financieros'
                        ],
            "Humanidades": ['Licenciado en Filosofía', 'Licenciado en Historia', 'Licenciado en Literatura', 'Licenciado en Lingüística', 'Licenciado en Arte', 
                            'Técnico en Traducción e Interpretariado', 'Licenciado en Musicología', 'Técnico en Archivística'
                            ],
            "Ingeniería": ['Ingeniero Civil', 'Ingeniero Civil Industrial', 'Ingeniero Civil en Minas', 'Ingeniero Civil Estructural', 'Ingeniero Civil Hidráulico', 
                            'Ingeniero Civil Eléctrico', 'Ingeniero en Mecánica Automotriz', 'Ingeniero Mecánico', 'Ingeniero Electrónico', 'Ingeniero Químico', 
                            'Ingeniero Ambiental', 'Ingeniero Agrónomo', 'Arquitecto', 'Constructor Civil', 'Técnico en Automatización Industrial', 'Técnico en Energías Renovables', 
                            'Técnico en Mantenimiento de Maquinaria', 'Ingeniero en Automatización y Control', 'Ingeniero en Logística y Supply Chain', 
                            'Ingeniero en Metalurgia', 'Ingeniero Geólogo', 'Técnico en Prevención de Riesgos', 'Técnico en Topografía', 'Ingeniero en Geomensura', 
                            'Ingeniero en Calidad y Producción'],
            "Logística": ['Técnico en Gestión Logística', 'Ingeniero en Cadena de Suministro'],
            "Marketing": ['Técnico en Marketing Digital', 'Licenciado en Marketing y Publicidad', 'Técnico en Comercio Electrónico'],
            "Posgrado": ['Magíster en Ciencia de Datos Avanzada', 'Magíster en Ingeniería Estructural', 'Magíster en Ciberseguridad Ofensiva', 
                            'Magíster en Gestión de Proyectos TI', 'Doctorado en Inteligencia Artificial', 'Doctorado en Ingeniería Química', 
                            'Magíster en Ingeniería de Procesos', 'Magíster en Electrónica Industrial', 'Magíster en Big Data', 'Doctorado en Telecomunicaciones', 
                            'Magíster en Administración de Negocios (MBA)', 'Magíster en Marketing Estratégico', 'Magíster en Finanzas Corporativas', 
                            'Doctorado en Economía', 'Magíster en Tributación', 'Magíster en Dirección de RRHH', 'Doctorado en Administración de Empresas', 
                            'Magíster en Auditoría', 'Magíster en Emprendimiento', 'Magíster en Contabilidad Financiera', 'Magíster en Logística Integral', 
                            'Doctorado en Derecho Civil', 'Magíster en Salud Pública', 'Magíster en Bioestadística', 'Magíster en Ciencias Químicas', 
                            'Doctorado en Biología Molecular', 'Magíster en Nutrición Clínica', 'Magíster en Fisiología del Ejercicio', 'Doctorado en Física Aplicada', 
                            'Magíster en Genética', 'Magíster en Ciencias del Deporte', 'Magíster en Epidemiología', 'Doctorado en Ciencias de la Tierra', 
                            'Magíster en Bioingeniería', 'Magíster en Psicología Clínica', 'Magíster en Comunicación Estratégica', 'Magíster en Educación', 
                            'Doctorado en Sociología', 'Magíster en Antropología Social', 'Magíster en Gestión Cultural', 'Doctorado en Filosofía', 
                            'Magíster en Asuntos Públicos', 'Magíster en Historia del Arte', 'Doctorado en Historia Moderna', 'Magíster en Psicología Organizacional', 
                            'Magíster en Diseño y Creatividad', 'Magíster en Producción Audiovisual', 'Doctorado en Teoría del Arte', 'Magíster en Conservación de Arte', 
                            'Magíster en Innovación en Diseño'],
            "Salud": ['Médico Cirujano', 'Enfermera/o', 'Tecnólogo Médico', 'Nutricionista', 'Kinesiólogo', 'Odontólogo', 'Técnico en Enfermería Nivel Superior (TENS)', 
                        'Técnico en Laboratorio Clínico', 'Técnico en Farmacia', 'Químico Farmacéutico', 'Fonoaudiólogo', 'Terapeuta Ocupacional', 
                        'Técnico en Radiología', 'Técnico en Veterinaria', 'Técnico en Control Sanitario', 'Médico Veterinario', 'Técnico Dental', 
                        'Técnico en Instrumentación Quirúrgica'],
            "Sociales": ['Psicólogo', 'Sociólogo', 'Trabajador Social', 'Antropólogo', 'Técnico en Trabajo Comunitario', 'Técnico en Desarrollo Local', 
                        'Licenciado en Ciencias de la Familia', 'Técnico en Asistencia Social'],
            "Tecnología": ['Ingeniero en Informática', 'Ingeniero en Ciencia de Datos', 'Ingeniero en Ciberseguridad', 'Ingeniero en Redes y Telecomunicaciones', 
                            'Ingeniero en Software', 'Técnico en Programación Web', 'Técnico en Diseño UX/UI', 'Técnico en Soporte Informático', 
                            'Técnico en Robótica y Sistemas', 'Técnico en Análisis de Sistemas', 'Ingeniero en Telecomunicaciones Móviles', 'Licenciado en Computación', 
                            'Ingeniero Civil en Computación', 'Técnico en Cloud Computing', 'Técnico en Diseño 3D']
        }
    
        self.Carreras={
            "Ingeniería y Ciencias":['Ingeniería Civil', 'Ingeniería Civil Industrial', 'Ingeniería Civil en Computación', 'Ingeniería Civil Eléctrica', 
                                    'Ingeniería Civil en Minas', 'Ingeniería en Ciberseguridad', 'Ingeniería en Ciencia de Datos', 'Ingeniería en Metalurgia', 
                                    'Ingeniería Civil Química', 'Licenciatura en Matemáticas', 'Licenciatura en Física', 'Geología', 'Astronomía', 
                                    'Ingeniería Mecánica', 'Arquitectura'],
            "Administración y Negocios":['Ingeniería Comercial', 'Contador Auditor', 'Administración Pública', 'Ingeniería en Finanzas', 'Ingeniería en Marketing Digital', 
                                        'Licenciatura en Economía', 'Ingeniería en Logística', 'Comercio Internacional', 'Técnico en Administración de Recursos Humanos', 
                                        'Ingeniería en Gestión de Proyectos'],
            "Salud":['Medicina', 'Odontología', 'Enfermería', 'Kinesiología', 'Nutrición y Dietética', 'Fonoaudiología', 'Tecnología Médica', 'Terapia Ocupacional', 
                    'Química y Farmacia', 'Medicina Veterinaria'],
            "Sociales y Derecho":['Derecho', 'Psicología', 'Sociología', 'Trabajo Social', 'Periodismo', 'Licenciatura en Historia', 'Licenciatura en Filosofía', 
                                    'Ciencia Política', 'Antropología', 'Comunicación Audiovisual'],
            "Educación":['Pedagogía en Educación Básica', 'Pedagogía en Educación Parvularia', 'Pedagogía en Inglés', 'Pedagogía en Historia y Ciencias Sociales', 
                        'Pedagogía en Matemáticas y Física', 'Educación Diferencial', 'Educación Física', 'Pedagogía en Lenguaje y Comunicación'],
            "Artes y Diseño":['Diseño Gráfico', 
                                'Diseño Industrial', 'Licenciatura en Artes Visuales', 'Cine y Televisión', 'Teatro y Actuación', 'Licenciatura en Música', 
                                'Diseño de Ambientes y Espacios'],
            "Técnicas y TIC":['Técnico en Programación y Análisis de Sistemas', 'Técnico en Conectividad y Redes', 'Técnico en Electricidad Industrial', 
                                'Técnico en Energías Renovables', 'Técnico en Prevención de Riesgos', 'Técnico en Instrumentación y Control', 'Técnico en Gastronomía', 
                                'Técnico en Turismo Sustentable', 'Técnico en Mantenimiento Aeronáutico', 'Técnico en Diseño UX/UI']
        }
    
        self.Tipo_Clase=[
            "Cátedra (Teoría)",
            "Taller (Práctica)",
            "Laboratorio",
            "Seminario",
            "Clínica / Terreno",
            "Ayudantía / Tutoría",
            "Evaluación / Prueba",
            "Online Sincrónico",
            "Online Asincrónico",
            "Conferencia / Visita"
        ]
    
        self.salas=[
            {'Tipo': 'Aula Estándar', 'Cantidad' : 400},
            {'Tipo': 'Laboratorio de Computación', 'Cantidad' : 100},
            {'Tipo': 'Taller Especializado', 'Cantidad' : 80},
            {'Tipo': 'Laboratorio de Ciencias', 'Cantidad' : 60},
            {'Tipo': 'Clínica / Box', 'Cantidad' : 50},
            {'Tipo': 'Auditorio / Anfiteatro', 'Cantidad' : 20},
            {'Tipo': 'Sala de Reuniones', 'Cantidad' : 50},
            {'Tipo': 'Estudio / Cabina', 'Cantidad' : 40}
        ]
    
        print("Datos estáticos cargados.")
    
    
    #Cargar primeras tablas
    def cargar_carreras(self):
        print("Cargando carreras...")
        db=Conexion()
        datos_carreras = []
        for facultad, carreras in self.Carreras.items():
            for carrera in carreras:
                sd=datetime(2015,1,1)
                ed=datetime(2025,1,1)
                nombre=carrera
                semestre_total=self.faker.random_int(min=4, max=12)
                fecha_impartida=self.faker.date_time_between(start_date=sd, end_date=ed)
                datos_carreras.append((nombre, semestre_total, fecha_impartida))
        db.cursor.executemany("INSERT INTO carrera (Nombre, Semestre_Total, Fecha_Impartida) VALUES (%s, %s, %s)", datos_carreras)
        db.conn.commit()
        db.conn.close()
        print("Carreras cargadas correctamente.")
    
    def cargar_cursos(self,cant=10):
        print("Cargando cursos...")
        db=Conexion()
        
        query = "SELECT ID_Carrera, Fecha_Impartida FROM carrera"
        db.cursor.execute(query)
        carreras_data = db.cursor.fetchall()
        
        if not carreras_data:
            print("Error: No se encontraron datos de 'carrera'. Asegúrate de cargar la tabla primero.")
            db.conn.close()
            return
        
        
        datos_cursos=[]
        for _ in range(cant):
            carrera_seleccionada = self.faker.random_element(carreras_data)
            
            id_carrera = carrera_seleccionada['ID_Carrera']
            fecha_inicio_carrera = carrera_seleccionada['Fecha_Impartida'] 
            
            año_minimo = fecha_inicio_carrera.year
            
            nombre = self.faker.sentence(nb_words=4).rstrip('.')
            especialidad = self.faker.random_element(self.Especialidades.get(self.faker.random_element(list(self.Especialidades.keys())), []))
            
            año = self.faker.random_int(min=año_minimo, max=2025)
            
            seccion = f"{año}--{especialidad[:3].upper()}--{self.faker.random_int(min=1, max=5)}"
            
            horas_semanales = self.faker.random_int(min=1, max=4)
            
            Hora_Total = horas_semanales * 16
            
            Capacidad_Max = self.faker.random_int(min=20, max=45)
            
            
            semestre = self.faker.random_int(min=1, max=2)
            
            datos_cursos.append((
                id_carrera, nombre, especialidad, seccion, Hora_Total, 
                Capacidad_Max, año, semestre))
            
        db.cursor.executemany(
            "INSERT INTO curso (ID_Carrera, Nombre, Especialidad, Seccion, Hora_Total, Capacidad_Max, Año, Semestre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            datos_cursos
        )
            
        db.conn.commit()
        db.conn.close()
        print("Cursos cargados correctamente.")
                
    
    #Cargar Tablas sin relaciones
    def cargar_salas(self):
        print("Cargando salas...")
        db=Conexion()
        datos_salas = []
        for sala in self.salas:
            tipo = sala['Tipo']
            cantidad = sala['Cantidad']
            for _ in range(cantidad):
                piso = self.faker.random_int(min=1, max=5)
                datos_salas.append((tipo, piso))
        
        db.cursor.executemany("INSERT INTO sala (Tipo, Piso) VALUES (%s, %s)", datos_salas)
        db.conn.commit()
        db.conn.close()
        print("Salas cargadas correctamente.")
    
    
    def cargar_profesores(self,cant):
        print("Cargando profesores...")
        db=Conexion()
        datos_profesores = []
        rut_asignados = set()
        for _ in range(cant):
            while True:
                rut=self.faker.rut(min=2000000, max=25000000)
                if rut not in rut_asignados:
                    rut_asignados.add(rut)
                    break
            
            
            sexo = self.faker.random_element(elements=('Masculino', 'Femenino'))
            if sexo == 'Masculino':
                nombres = f'{self.faker.first_name_male()} {self.faker.first_name_male()}'
            else:
                nombres = f'{self.faker.first_name_female()} {self.faker.first_name_female()}'
            apellido_p = self.faker.last_name()
            apellido_m = self.faker.last_name()
            correo = self.faker.email()
            datos_profesores.append((rut, nombres, apellido_p, apellido_m, sexo ,correo))
        db.cursor.executemany("INSERT INTO profesor (Rut_Profesor, Nombres, Apellido_Paterno, Apellido_Materno, Sexo, Correo) VALUES (%s, %s, %s, %s, %s, %s)", datos_profesores)
        db.conn.commit()
        db.conn.close()
        print("Profesores cargados correctamente.")        
    
    
    def cargar_titulos(self):
        print("Cargando titulos...")
        db=Conexion()
        
        datos_titulos = []
        for area, especialidad in self.Especialidades.items():
            for titulo in especialidad:
                nombre = titulo
                especialidad = area
                datos_titulos.append((nombre, especialidad))
        db.cursor.executemany("INSERT INTO titulo (nombre, especialidad) VALUES (%s, %s)", datos_titulos)
        db.conn.commit()
        db.conn.close()
        print("Titulos cargados correctamente.")
    
    
    def cargar_alumnos(self,cant):
        print("Cargando alumnos...")
        db=Conexion()
        datos_alumnos = []
        rut_asignados = set()
        for _ in range(cant):
            while True: 
                rutFormateado=self.faker.rut(min=1000000,max=25000000)
                if rutFormateado not in rut_asignados:
                    rut_asignados.add(rutFormateado)
                    break
                
            
            sexo = self.faker.random_element(elements=('Masculino', 'Femenino'))
            if sexo == 'Masculino':
                nombres = f'{self.faker.first_name_male()} {self.faker.first_name_male()}'
            else:
                nombres = f'{self.faker.first_name_female()} {self.faker.first_name_female()}'
                
            apellido_p = self.faker.last_name()
            apellido_m = self.faker.last_name()
            correo = self.faker.email()
            telefono = self.faker.phone_number()
            datos_alumnos.append((rutFormateado, nombres, apellido_p, apellido_m, sexo, correo, telefono))
        db.cursor.executemany("INSERT INTO alumno (rut, nombres, apellido_p, apellido_m, sexo, correo, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s)", datos_alumnos)
        db.conn.commit()
        db.conn.close()
        print("Alumnos cargados correctamente.")
    
    
    def cargar_tipos_clase(self):
        print("Cargando tipos_clase...")
        db=Conexion()
        
        datos_tipos_clase = [(tipo,) for tipo in self.Tipo_Clase]
        db.cursor.executemany("INSERT INTO tipo_clase (Nombre) VALUES (%s)", datos_tipos_clase)
        db.conn.commit()
        db.conn.close()
        print("Tipos_clase cargados correctamente.")
    
    
    #Cargar tablas con relaciones
    def cargar_curso_sala(self):
        print("Cargando curso_sala...")
        db=Conexion()
        
        query = db.cursor.execute("SELECT ID_Curso, Año, Semestre FROM curso")
        cursos_obtenidos = db.cursor.fetchall()
        
        datos_curso_sala = []
        for curso in cursos_obtenidos:
            id_curso = curso['ID_Curso']
            año_curso = datetime(year=curso['Año'],month=1 if curso["Semestre"] == 1 else 6,day=1)
            
            
            db.cursor.execute("SELECT Codigo_Sala FROM sala ORDER BY RAND() LIMIT 1")
            sala_seleccionada = db.cursor.fetchone()
            codigo_sala = sala_seleccionada['Codigo_Sala']
            
            datos_curso_sala.append((id_curso, codigo_sala, año_curso))
        db.cursor.executemany("INSERT INTO curso_sala (ID_Curso, Codigo_Sala, Fecha) VALUES (%s, %s, %s)", datos_curso_sala)
        db.conn.commit()
        db.conn.close() 
        print("curso_sala cargado correctamente.")   
    
    
    def cargar_profesor_curso(self):
        print("Cargando profesor_curso...")
        db=Conexion()
        
        query = "SELECT ID_Curso, Año FROM curso"
        db.cursor.execute(query)
        cursos_data = db.cursor.fetchall()
        
        query = "SELECT count(Rut_Profesor) FROM profesor"
        db.cursor.execute(query)
        total_profesores = db.cursor.fetchone()['count(Rut_Profesor)']
        
        
        if not cursos_data:
            print("Error: No se encontraron datos de 'curso'. Asegúrate de cargar la tabla primero.")
            db.conn.close()
            return
        
        datos_profesor_curso = []
        for curso in cursos_data:
            id_curso = curso['ID_Curso']
            año_curso = datetime(year=curso['Año'],month=1,day=1)
            fecha_limite = datetime(year=año_curso.year,month=3,day=15)
            
            cant_asignaciones = self.faker.random_int(min=1, max=3)
            asignados = set()
            for _ in range(cant_asignaciones):
                while True:
                    db.cursor.execute("SELECT Rut_Profesor FROM profesor ORDER BY RAND() LIMIT 1")
                    profesor_seleccionado = db.cursor.fetchone()
                    rut_profesor = profesor_seleccionado['Rut_Profesor']
                    
                    if rut_profesor not in asignados:
                        asignados.add(rut_profesor)
                        break
                
                fecha_asignacion = self.faker.date_between(start_date=año_curso, end_date=fecha_limite)
                datos_profesor_curso.append((rut_profesor, id_curso, fecha_asignacion))
        
        db.cursor.executemany("INSERT INTO profesor_curso (Rut_Profesor, ID_Curso, Fecha_Agregado) VALUES (%s, %s, %s)", datos_profesor_curso)
        db.conn.commit()
        db.conn.close()
        print("profesor_curso cargado correctamente.")
    
    
    def cargar_profesor_titulo(self):
        print("Cargando profesor_titulo...")
        db=Conexion()
        
        query = "SELECT Rut_Profesor FROM profesor"
        db.cursor.execute(query)
        profesores_data = db.cursor.fetchall()
        
        query = "SELECT ID_Titulo FROM titulo"
        db.cursor.execute(query)
        titulos_data = db.cursor.fetchall()
        
        datos_profesor_titulo = []
        for profesor in profesores_data:
            rut_profesor = profesor['Rut_Profesor']
            cant_titulos = self.faker.random_int(min=1, max=4)
            titulos_asignados = set()
            for _ in range(cant_titulos):
                while True:
                    titulo_seleccionado = self.faker.random_element(titulos_data)
                    id_titulo = titulo_seleccionado['ID_Titulo']
                    
                    if id_titulo not in titulos_asignados:
                        titulos_asignados.add(id_titulo)
                        break
                fecha_obtencion = self.faker.date_between(start_date='-10y', end_date='today')
                datos_profesor_titulo.append((id_titulo, rut_profesor, fecha_obtencion))
        db.cursor.executemany("INSERT INTO titulo_profesor (ID_Titulo, Rut_Profesor, Fecha_Agregado) VALUES (%s, %s, %s)", datos_profesor_titulo)
        db.conn.commit()
        db.conn.close()
        print("profesor_titulo cargado correctamente.")
    
    
    def cargar_alumno_curso(self):
        print("Cargando alumno_curso...")
        db=Conexion()
        query = "SELECT ID_Curso, Capacidad_Max, Año FROM curso"
        db.cursor.execute(query)
        cursos_data = db.cursor.fetchall()
        query = "SELECT rut FROM alumno"
        db.cursor.execute(query)
        alumnos_data = db.cursor.fetchall()
        
        datos_alumno_curso = []
        for curso in cursos_data:
            id_curso = curso['ID_Curso']
            capacidad_max = curso['Capacidad_Max']
            fecha_curso = curso['Año']
            año_curso = datetime(year=fecha_curso,month=1,day=1)
            fecha_limite = datetime(year=año_curso.year,month=3,day=15)
            
            cant_inscritos = self.faker.random_int(min=int(capacidad_max*0.8), max=capacidad_max)
            inscritos = set()
            for _ in range(cant_inscritos):
                while True:
                    alumno_seleccionado = self.faker.random_element(alumnos_data)
                    rut_alumno = alumno_seleccionado['rut']
                    
                    if rut_alumno not in inscritos:
                        inscritos.add(rut_alumno)
                        break
                
                fecha_inscripcion = self.faker.date_between(start_date=año_curso, end_date=fecha_limite)
                datos_alumno_curso.append((rut_alumno, id_curso, fecha_inscripcion))
        db.cursor.executemany("INSERT INTO curso_alumno (Rut_Alumno, ID_Curso, Fecha_Agregado) VALUES (%s, %s, %s)", datos_alumno_curso)
        db.conn.commit()
        db.conn.close()
        print("alumno_curso cargado correctamente.")
    
    
    def cargar_evaluaciones(self):
        print("Cargando evaluaciones...")
        db=Conexion()
        
        db.cursor.execute("SELECT ID_Curso_Alumno, ID_Curso FROM curso_alumno")
        curso_alumno_data = db.cursor.fetchall()
        
        datos_evaluaciones = []
        for curso_alumno in curso_alumno_data:
            id_curso_alumno = curso_alumno['ID_Curso_Alumno']
            db.cursor.execute("SELECT Año, Semestre FROM curso WHERE ID_Curso = %s", (curso_alumno['ID_Curso']))
            curso_data = db.cursor.fetchone()
            cant_evaluaciones = self.faker.random_int(min=3, max=5)
            año_curso = datetime(year=curso_data['Año'],month=1 if curso_data["Semestre"] == 1 else 6,day=1)
            fecha_limite = datetime(year=año_curso.year,month=6 if curso_data["Semestre"] == 2 else 12,day=30)
            while True:
                ponderacion = self.faker.random_elements(elements=[10, 15, 20, 25, 30], length=cant_evaluaciones-1)
                total_asignado = sum(ponderacion)
                if total_asignado < 100:
                    ultima_ponderacion = 100 - total_asignado
                    ponderacion.append(ultima_ponderacion)
                    break
            for p in ponderacion:
                fecha_evaluacion = self.faker.date_between(start_date=año_curso, end_date=fecha_limite)
                puntaje = self.faker.random_int(min=40, max=100)
                nota = self.faker.pyfloat(right_digits=1, min_value=1.0, max_value=7.0)
                
                datos_evaluaciones.append((id_curso_alumno, fecha_evaluacion, p, puntaje, nota))
        db.cursor.executemany("INSERT INTO evaluacion (ID_Curso_Alumno, Fecha, Ponderacion, Puntaje, Nota) VALUES (%s, %s, %s, %s, %s)", datos_evaluaciones)
        db.conn.commit()
        db.conn.close()
        print("Evaluaciones cargadas correctamente.")
    
    
    def cargar_curso_tipo_clase(self):
        print("Cargando curso_tipo_clase...")
        db=Conexion()
        
        db.cursor.execute("SELECT ID_Curso, Hora_Total FROM curso")
        cursos_data = db.cursor.fetchall()
        
        db.cursor.execute("SELECT ID_Tipo_Clase FROM tipo_clase")
        tipo_clase_data = db.cursor.fetchall()
        
        tipo = [tc['ID_Tipo_Clase'] for tc in tipo_clase_data]
        
        datos_curso_tipo_clase = []
        for curso in cursos_data:
            id_curso = curso['ID_Curso']
            horas_totales = curso['Hora_Total']
            while True:
                cant_tipo_clase = self.faker.random_int(min=1, max=3)
                tipo_clases_asignados = [self.faker.random_int(min=int(horas_totales*0.3), max=horas_totales) for _ in range(cant_tipo_clase-1)]
                total_asignado = sum(tipo_clases_asignados)
                if total_asignado < horas_totales:
                    ultima_asignacion = horas_totales - total_asignado
                    tipo_clases_asignados.append(ultima_asignacion)
                    break
                
            asignados = self.faker.random_elements(elements=tipo, length=cant_tipo_clase, unique=True)
            for n, horas in enumerate(tipo_clases_asignados):
                tipo_clase = asignados[n]
                datos_curso_tipo_clase.append((id_curso, tipo_clase, horas))
        db.cursor.executemany("INSERT INTO curso_tipo_clase (ID_Curso, ID_Tipo_Clase, Horas) VALUES (%s, %s, %s)", datos_curso_tipo_clase)
        db.conn.commit()
        db.conn.close()
        print("curso_tipo_clase cargado correctamente.")
                
        
Creacion_bd = Creacion_bd_uni()
Creacion_bd.Cargar_datos()
Creacion_bd.cargar_carreras()
Creacion_bd.cargar_salas()
Creacion_bd.cargar_titulos()
Creacion_bd.cargar_tipos_clase()   
Creacion_bd.cargar_profesores(500)
Creacion_bd.cargar_alumnos(30000)
Creacion_bd.cargar_cursos(7000)
Creacion_bd.cargar_curso_sala()
Creacion_bd.cargar_profesor_curso()
Creacion_bd.cargar_profesor_titulo()
Creacion_bd.cargar_alumno_curso()
Creacion_bd.cargar_evaluaciones()
Creacion_bd.cargar_curso_tipo_clase()

    
    
    
    
    










































