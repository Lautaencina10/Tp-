import pandas as pd
import numpy as np
import os
from abc import ABC, abstractmethod
from modelo_orm import *
from peewee import SqliteDatabase, IntegrityError

class GestionarObra(ABC):
    db = None
    df = None
    archivo_csv = "observatorio-de-obras-urbanas.csv"

    @classmethod
    def conectar_db(cls):
        cls.db = SqliteDatabase("obras_urbanas.db")
        cls.db.connect()
        cls.db.bind([Etapa, TipoObra, AreaResponsable, Barrio, TipoContratacion, Empresa, Financiamiento, Obra])

    @classmethod
    def mapear_orm(cls):
        cls.db.create_tables([Etapa, TipoObra, AreaResponsable, Barrio, TipoContratacion, Empresa, Financiamiento, Obra])

    @classmethod
    def extraer_datos(cls):
        print("→ Leyendo datos desde el CSV...")
        try:
            cls.df = pd.read_csv(cls.archivo_csv)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {cls.archivo_csv}")
            return

    @classmethod
    def limpiar_datos(cls):
        print("→ Limpiando y cargando datos...")
        df = cls.df.copy()

        df.columns = df.columns.str.lower().str.strip()

        df["monto_contrato"] = pd.to_numeric(df["monto_contrato"], errors="coerce")
        df["porcentaje_avance"] = pd.to_numeric(df["porcentaje_avance"], errors="coerce")
        df["plazo_meses"] = pd.to_numeric(df["plazo_meses"], errors="coerce")
        df["mano_obra"] = pd.to_numeric(df["mano_obra"], errors="coerce")
        df["beneficiarios"] = pd.to_numeric(df["beneficiarios"], errors="coerce")

        df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], dayfirst=True, errors="coerce")
        df["fecha_fin_inicial"] = pd.to_datetime(df["fecha_fin_inicial"], dayfirst=True, errors="coerce")

        df = df.dropna(subset=["nombre", "direccion"])

        df["etapa"] = df["etapa"].fillna("Proyecto")
        df["tipo"] = df["tipo"].fillna("Sin especificar")
        df["area_responsable"] = df["area_responsable"].fillna("Desconocida")
        df["barrio"] = df["barrio"].fillna("Sin barrio")
        df["comuna"] = df["comuna"].fillna("0").astype(str)

        cls.df = df
    @classmethod
    def cargar_datos(cls):
        print("→ Cargando datos en la base de datos...")
        df = cls.df.copy()

        for _, row in df.iterrows():
            try:
                tipo_obra, _ = TipoObra.get_or_create(nombre=row["tipo"].strip())
                etapa, _ = Etapa.get_or_create(nombre=row["etapa"].strip())
                barrio, _ = Barrio.get_or_create(nombre=row["barrio"].strip())
                area, _ = AreaResponsable.get_or_create(nombre=row["area_responsable"].strip())
                contratacion, _ = TipoContratacion.get_or_create(nombre=row.get("contratacion_tipo", "Desconocida").strip())
                empresa, _ = Empresa.get_or_create(
                    nombre=row.get("licitacion_oferta_empresa", "Sin empresa").strip(),
                    cuit=row.get("cuit_contratista", "0").strip()
                )
                financiamiento, _ = FuenteFinanciamiento.get_or_create(
                    nombre=row.get("financiamiento", "Sin fuente").strip()
                )

                Obra.create(
                    nombre=row["nombre"].strip(),
                    etapa=etapa,
                    tipo_obra=tipo_obra,
                    area_responsable=area,
                    descripcion=row.get("descripcion", "").strip(),
                    monto_contrato=row.get("monto_contrato", 0) or 0,
                    comuna=row.get("comuna", "0").strip(),
                    barrio=barrio,
                    direccion=row["direccion"].strip(),
                    lat=row.get("lat", 0),
                    lng=row.get("lng", 0),
                    fecha_inicio=row.get("fecha_inicio"),
                    fecha_fin_inicial=row.get("fecha_fin_inicial"),
                    plazo_meses=row.get("plazo_meses", 0) or 0,
                    porcentaje_avance=row.get("porcentaje_avance", 0) or 0,
                    imagen_1=row.get("imagen_1", ""),
                    imagen_2=row.get("imagen_2", ""),
                    imagen_3=row.get("imagen_3", ""),
                    imagen_4=row.get("imagen_4", ""),
                    licitacion_anio=row.get("licitacion_anio", "0"),
                    contratacion_tipo=contratacion,
                    nro_contratacion=row.get("nro_contratacion", ""),
                    empresa=empresa,
                    expediente_numero=row.get("expediente-numero", ""),
                    beneficiarios=row.get("beneficiarios", 0) or 0,
                    mano_obra=row.get("mano_obra", 0) or 0,
                    compromiso=row.get("compromiso", ""),
                    destacada=row.get("destacada", ""),
                    ba_elige=row.get("ba_elige", ""),
                    link_interno=row.get("link_interno", ""),
                    pliego_descarga=row.get("pliego_descarga", ""),
                    estudio_ambiental_descarga=row.get("estudio_ambiental_descarga", ""),
                    fuente_financiamiento=financiamiento
                )
            except Exception as e:
                print(f"  Error cargando fila: {e}")

    @classmethod
    def nueva_obra(cls):
        try:
            print("→ Creando nueva obra...")

            nombre = input("Nombre de la obra: ")
            descripcion = input("Descripción: ")
            direccion = input("Dirección: ")

            tipo_nombre = input("Tipo de obra (exacto): ")
            tipo = TipoObra.get_or_none(nombre=tipo_nombre)
            if not tipo:
                print(f"Tipo de obra '{tipo_nombre}' no encontrado.")
                return

            etapa_nombre = "Proyecto"
            etapa, _ = Etapa.get_or_create(nombre=etapa_nombre)

            area_nombre = input("Área responsable (exacto): ")
            area = AreaResponsable.get_or_none(nombre=area_nombre)
            if not area:
                print(f"Área '{area_nombre}' no encontrada.")
                return

            barrio_nombre = input("Barrio (exacto): ")
            barrio = Barrio.get_or_none(nombre=barrio_nombre)
            if not barrio:
                print(f"Barrio '{barrio_nombre}' no encontrado.")
                return

            comuna = input("Comuna (ej. 5): ")

            obra = Obra.create(
                nombre=nombre,
                etapa=etapa,
                tipo_obra=tipo,
                area_responsable=area,
                descripcion=descripcion,
                monto_contrato=0,
                comuna=comuna,
                barrio=barrio,
                direccion=direccion,
                porcentaje_avance=0,
            )

            print(f" Obra '{obra.nombre}' creada con estado inicial 'Proyecto'")
            return obra

        except Exception as e:
            print(f" Error al crear obra: {e}")
               


        
