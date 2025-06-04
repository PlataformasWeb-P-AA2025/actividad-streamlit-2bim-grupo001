from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv

# se importa la clase(s) del 
# archivo genera_tablas
from clases import Usuario, Publicacion, Reaccion

# se importa información del archivo configuracion
from config import cadena_base_datos
# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# Cargar datos de Usuario
with open('DATA/usuarios_red_x.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        usuario = Usuario(nombre_usuario=row['usuario'])
        session.add(usuario)

# Cargar datos de Publicaciones
with open('DATA/usuarios_publicaciones.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='|')
    for row in reader:
        usuario = session.query(Usuario).filter_by(nombre_usuario=row['usuario']).first()
        if usuario:
            publicacion = Publicacion(
                contenido=row['publicacion'],
                usuario=usuario
            )
            session.add(publicacion)


# Cargar datos de Reacciones
with open('DATA/usuario_publicacion_emocion.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='|')
    for row in reader:
        usuario = session.query(Usuario).filter_by(nombre_usuario=row['Usuario']).first()
        publicacion = session.query(Publicacion).filter_by(contenido=row['comentario']).first()
        if usuario and publicacion:
            reaccion = Reaccion(
                usuario=usuario,
                publicacion=publicacion,
                tipo_reaccion=row['tipo emocion']
            )
            session.add(reaccion)

# Confirmar los cambios en la base de datos
session.commit()