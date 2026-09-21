import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad
random.seed(42)
np.random.seed(42)

# ==========================================
# 1. PESTAÑA AULAS (150 ESPACIOS)
# ==========================================
edificios = [f"Edificio {letra}" for letra in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]
tipos_espacio = ['Aula Estándar', 'Cómputo', 'Auditorio', 'Salón Magno', 'Taller / Lab']

equipamientos = {
    'Aula Estándar': ['Videobeam, Aire Acondicionado', 'Smart TV, Aire Acondicionado'],
    'Cómputo': ['PC, Videobeam, Aire Acondicionado'],
    'Auditorio': ['Audio Pro, Videobeam, Streaming'],
    'Salón Magno': ['Smart TV, Videobeam, Audio Pro'],
    'Taller / Lab': ['Equipamiento Especializado, Videobeam']
}

aulas = []
for i in range(1, 151):
    id_aula = f"AULA-{i:03d}"
    edificio = random.choice(edificios)
    tipo = random.choice(tipos_espacio)
    
    if tipo == 'Auditorio':
        capacidad = random.choice([100, 120, 150, 200])
    elif tipo == 'Cómputo':
        capacidad = random.choice([25, 30, 35, 40])
    elif tipo == 'Salón Magno':
        capacidad = random.choice([50, 60, 80])
    else:
        capacidad = random.choice([30, 35, 40, 45, 50])
        
    equip = random.choice(equipamientos[tipo])
    estado = 'Activo' if random.random() > 0.05 else 'Mantenimiento'
    
    aulas.append({
        'ID_Aula': id_aula,
        'Edificio': edificio,
        'Tipo_Espacio': tipo,
        'Capacidad': capacidad,
        'Equipamiento': equip,
        'Estado': estado
    })

df_aulas = pd.DataFrame(aulas)

# ==========================================
# 2. PESTAÑA PROGRAMACIÓN ACADÉMICA (~1,200 CURSOS)
# ==========================================
programas = [
    'Psicología', 'Ing. Sistemas', 'Ing. Industrial', 'Derecho', 'Administración', 
    'Economía', 'Mercadeo', 'Medicina', 'Diseño de Medios', 'Biología', 
    'Química Farmacéutica', 'Contaduría', 'Licenciatura en Educación', 
    'Ciencia de Datos', 'Posgrados Analytics', 'Posgrados Gerencia',
    'Ing. Bioquímica', 'Diseño Industrial', 'Ing. Telemática', 'Antropología',
    'Filosofía', 'Sociología', 'Música', 'Finanzas', 'Mercadeo Internacional'
]

dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
bloques_horarios = [
    ('07:00', '09:00'), ('08:00', '10:00'), ('08:00', '11:00'), 
    ('10:00', '12:00'), ('11:00', '13:00'), ('14:00', '16:00'), 
    ('14:00', '17:00'), ('16:00', '18:00'), ('18:00', '21:00')
]

aulas_activas = df_aulas[df_aulas['Estado'] == 'Activo']['ID_Aula'].tolist()

programacion = []
for i in range(1, 1201):
    id_curso = f"CURS-{i:04d}"
    programa = random.choice(programas)
    materia = f"Asignatura {random.randint(101, 499)}"
    dia = random.choice(dias_semana)
    h_inicio, h_fin = random.choice(bloques_horarios)
    aula_id = random.choice(aulas_activas)
    
    # Obtener capacidad del salón asignado
    cap_aula = df_aulas[df_aulas['ID_Aula'] == aula_id]['Capacidad'].values[0]
    
    # Simular inscritos (algunos con sobrecupo leve o subutilización para generar alertas)
    factor_ocupacion = random.uniform(0.4, 1.1)
    inscritos = int(cap_aula * factor_ocupacion)
    
    programacion.append({
        'ID_Curso': id_curso,
        'Programa': programa,
        'Materia': materia,
        'Dia': dia,
        'Hora_Inicio': h_inicio,
        'Hora_Fin': h_fin,
        'Inscritos': inscritos,
        'ID_Aula': aula_id
    })

df_programacion = pd.DataFrame(programacion)

# ==========================================
# 3. PESTAÑA RESERVAS Y EVENTOS (~300 SOLICITUDES)
# ==========================================
solicitantes = [
    'Bienestar Universitario', 'Posgrados', 'Gestión Humana', 
    'Educación Continua', 'Decanatura Ingeniería', 'Decanatura C. Humanas',
    'Grupo Estudiantil ComPsi', 'Consultorio Jurídico', 'Relaciones Internacionales'
]

tipos_evento = [
    'Taller / Capacitación', 'Conferencia / Panel', 'Asamblea / Reunión',
    'Examen Extraordinario', 'Networking / Evento Institucional', 'Hackathon'
]

estados_reserva = ['Aprobado', 'Aprobado', 'Aprobado', 'Pendiente', 'Rechazado']

fecha_inicio = datetime(2026, 8, 1)
reservas = []

for i in range(1, 301):
    id_reserva = f"RES-{i:03d}"
    solicitante = random.choice(solicitantes)
    evento = random.choice(tipos_evento)
    
    # Generar fecha aleatoria dentro del semestre 2026-2
    dias_aleatorios = random.randint(0, 110)
    fecha_evento = (fecha_inicio + timedelta(days=dias_aleatorios)).strftime('%Y-%m-%d')
    
    h_inicio, h_fin = random.choice(bloques_horarios)
    aula_id = random.choice(aulas_activas)
    asistentes = random.randint(15, 120)
    estado = random.choice(estados_reserva)
    
    reservas.append({
        'ID_Reserva': id_reserva,
        'Solicitante': solicitante,
        'Tipo_Evento': evento,
        'Fecha': fecha_evento,
        'Hora_Inicio': h_inicio,
        'Hora_Fin': h_fin,
        'Asistentes': asistentes,
        'ID_Aula': aula_id,
        'Estado': estado
    })

df_reservas = pd.DataFrame(reservas)

# ==========================================
# 4. EXPORTAR A EXCEL Y CSV
# ==========================================
nombre_archivo_excel = 'data/raw/Base_Datos_Programacion_Academica.xlsx'

with pd.ExcelWriter(nombre_archivo_excel, engine='openpyxl') as writer:
    df_aulas.to_excel(writer, sheet_name='Aulas', index=False)
    df_programacion.to_excel(writer, sheet_name='Programacion_Academica', index=False)
    df_reservas.to_excel(writer, sheet_name='Reservas_Eventos', index=False)

print("✅ Base de datos simulada generada exitosamente en data/raw/Base_Datos_Programacion_Academica.xlsx")