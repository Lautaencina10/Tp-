from peewee import *
from datetime import datetime

sqlite_db = SqliteDatabase("obras_urbanas.db")

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class Etapa(BaseModel):
    nombre = CharField(unique=True)

class TipoObra(BaseModel):
    nombre = CharField(unique=True)

class AreaResponsable(BaseModel):
    nombre = CharField(unique=True)

class Empresa(BaseModel):
    nombre = CharField(unique=True)

class TipoContratacion(BaseModel):
    nombre = CharField(unique=True)

class FuenteFinanciamiento(BaseModel):
    nombre = CharField(unique=True)

class Obra(BaseModel):
    nombre = CharField()
    direccion = CharField()
    monto = FloatField()
    avance = FloatField(default=0)
    comuna = IntegerField(null=True)
    barrio = CharField(null=True)
    fecha_inicio = DateField(null=True)
    fecha_fin = DateField(null=True)
    tipo = ForeignKeyField(TipoObra, backref='obras', null=True)
    descripcion = TextField(null=True)
    etapa = ForeignKeyField(Etapa, backref='obras', null=True)
    area_responsable = ForeignKeyField(AreaResponsable, backref='obras', null=True)
    contratacion_tipo = ForeignKeyField(TipoContratacion, backref='obras', null=True)
    nro_contratacion = CharField(null=True)
    empresa = ForeignKeyField(Empresa, backref='obras', null=True)
    expediente_numero = CharField(null=True)
    fuente_financiamiento = ForeignKeyField(FuenteFinanciamiento, backref='obras', null=True)
    mano_obra = IntegerField(null=True)
    plazo_meses = IntegerField(null=True)

    def nuevo_proyecto(self):
        etapa, _ = Etapa.get_or_create(nombre="Proyecto")
        self.etapa = etapa
        self.save()

    def iniciar_contratacion(self, tipo_contratacion_nombre, nro_contratacion):
        try:
            tipo = TipoContratacion.get(TipoContratacion.nombre == tipo_contratacion_nombre)
            self.contratacion_tipo = tipo
            self.nro_contratacion = nro_contratacion
            etapa, _ = Etapa.get_or_create(nombre="Licitación")
            self.etapa = etapa
            self.save()
        except TipoContratacion.DoesNotExist:
            print(f"Tipo de contratación '{tipo_contratacion_nombre}' no encontrado.")

    def adjudicar_obra(self, empresa_nombre, expediente_numero):
        try:
            empresa = Empresa.get(Empresa.nombre == empresa_nombre)
            self.empresa = empresa
            self.expediente_numero = expediente_numero
            etapa, _ = Etapa.get_or_create(nombre="Adjudicada")
            self.etapa = etapa
            self.save()
        except Empresa.DoesNotExist:
            print(f"Empresa '{empresa_nombre}' no encontrada.")

    def iniciar_obra(self, destacada: bool, fecha_inicio, fecha_fin, fuente_financiamiento_nombre, mano_obra):
        try:
            self.fecha_inicio = fecha_inicio
            self.fecha_fin = fecha_fin
            self.mano_obra = mano_obra
            self.avance = 0
            fuente = FuenteFinanciamiento.get(FuenteFinanciamiento.nombre == fuente_financiamiento_nombre)
            self.fuente_financiamiento = fuente
            etapa, _ = Etapa.get_or_create(nombre="En ejecución")
            self.etapa = etapa
            self.save()
        except FuenteFinanciamiento.DoesNotExist:
            print(f"Fuente de financiamiento '{fuente_financiamiento_nombre}' no encontrada.")

    def actualizar_porcentaje_avance(self, nuevo_avance):
        self.avance = nuevo_avance
        self.save()

    def incrementar_plazo(self, meses_extra):
        if self.plazo_meses:
            self.plazo_meses += meses_extra
        else:
            self.plazo_meses = meses_extra
        self.save()

    def incrementar_mano_obra(self, adicionales):
        if self.mano_obra:
            self.mano_obra += adicionales
        else:
            self.mano_obra = adicionales
        self.save()

    def finalizar_obra(self):
        self.avance = 100
        etapa, _ = Etapa.get_or_create(nombre="Finalizada")
        self.etapa = etapa
        self.save()

    def rescindir_obra(self):
        etapa, _ = Etapa.get_or_create(nombre="Rescindida")
        self.etapa = etapa
        self.save()
