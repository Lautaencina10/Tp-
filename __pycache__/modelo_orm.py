from peewee import *

sqlite_db = SqliteDatabase("obras_urbanas.db")

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class Obra(BaseModel):
    nombre = CharField()
    direccion = CharField()
    monto = FloatField()
    avance = FloatField()
    comuna = IntegerField(null=True)
    barrio = CharField(null=True)
    fecha_inicio = DateField(null=True)
    fecha_fin = DateField(null=True)
    tipo = CharField(null=True)
    descripcion = TextField(null=True)
