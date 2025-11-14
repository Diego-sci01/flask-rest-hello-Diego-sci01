from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()


#    Explicacion de mi perspectiva basandome en Star Wars

# Los usuarios pueden tener uno o varios planetas favoritos,
# y muchos planetas pueden ser favoritos de varios usuarios. 
# En cada planeta puede haber uno o varios personajes, 
# y cada personaje puede estar en uno o varios planetas (pueden viajar en naves). 
# Ademas, los usuarios pueden tener uno o varios personajes favoritos, 
# y un mismo personaje puede ser favorito de muchos usuarios. :) 🛸


planeta_favorito = db.Table(
    'planeta_favorito',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('planeta_id', db.Integer, db.ForeignKey('planetas.id'), primary_key=True)
)

personaje_favorito= db.Table ('personaje_favorito', 
  db.Column ('usuario_id', db.Integer, db.ForeignKey('usuarios.id'),primary_key=True),
  db.Column ('personaje_id', db.Integer, db.ForeignKey('personajes.id'), primary_key=True))

planeta_personaje= db.Table ('planeta_personaje', 
  db.Column ('planeta_id', db.Integer, db.ForeignKey('planetas.id'),primary_key=True),
  db.Column ('personaje_id', db.Integer, db.ForeignKey('personajes.id'), primary_key=True))

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_suscripcion: Mapped[datetime] = mapped_column(DateTime)

    favorito_planeta: Mapped[List['Planeta']] = relationship(
     'Planeta', secondary=planeta_favorito, back_populates='favorito_usuario')
    
    favorito_personaje: Mapped[List['Personaje']] = relationship ('Personaje', secondary=personaje_favorito, back_populates="favorito_usuario")

class Planeta(db.Model):
    __tablename__ = 'planetas'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    clima: Mapped[str] = mapped_column(String(30), nullable=False)
    terreno: Mapped[str] = mapped_column(String(120), nullable=False)
    poblacion: Mapped[int] = mapped_column(Integer, nullable=False)

    favorito_usuario: Mapped[List["Usuarios"]] = relationship(
        'Usuarios', secondary=planeta_favorito, back_populates='favorito_planeta')
    
    personaje_planeta: Mapped[List["Personaje"]] = relationship(
        'Personaje', secondary=planeta_personaje, back_populates='planeta_personaje')

class Personaje(db.Model):
    __tablename__ = 'personajes'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    genero: Mapped[str] = mapped_column(String(50), nullable=False)
    ano_nacimiento: Mapped[str] = mapped_column(String(25), nullable=False)
    especie: Mapped[str] = mapped_column(String(25), nullable=False)

    favorito_usuario: Mapped[List["Usuarios"]] = relationship('Usuarios', secondary=personaje_favorito, back_populates="favorito_personaje")
    planeta_personaje: Mapped[List["Planeta"]] = relationship('Planeta', secondary=planeta_personaje, back_populates='personaje_planeta')