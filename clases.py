from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


# se importa información del archivo configuracion
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(500), nullable=False)

    publicaciones = relationship("Publicacion", back_populates="usuario")
    reacciones = relationship("Reaccion", back_populates="usuario")

    def __repr__(self):
        return f"Usuario: nombre={self.nombre_usuario}"

class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    contenido = Column(String(500), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="publicaciones")
    reacciones = relationship("Reaccion", back_populates="publicacion")

    def __repr__(self):
        return f"Publicacion: {self.contenido}"

class Reaccion(Base):
    __tablename__ = 'reaccion'
    id = Column(Integer, primary_key=True)
    publicacion_id = Column(Integer, ForeignKey("publicacion.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    tipo_reaccion = Column(String(100), nullable=False)

    publicacion = relationship("Publicacion", back_populates="reacciones")
    usuario = relationship("Usuario", back_populates="reacciones")

    def __repr__(self):
        return f"Usuario: {self.usuario.nombre_usuario}\nPublicacion: {self.publicacion.contenido}\nTipo_reaccion: {self.tipo_reaccion}"

Base.metadata.create_all(engine)
