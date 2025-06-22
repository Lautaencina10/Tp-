import pandas as pd
from modelo_orm import Obra, sqlite_db

class GestionarObra:
    df = None

    @staticmethod
    def conectar_db():
        print("→ Conectando a la base de datos...")
        sqlite_db.connect()

    @staticmethod
    def mapear_orm():
        print("→ Creando tablas si no existen...")
        sqlite_db.create_tables([Obra], safe=True)

    @staticmethod
    def extraer_datos():
        print("→ Leyendo datos desde el CSV...")
        try:
            GestionarObra.df = pd.read_csv("observatorio-de-obras-urbanas.csv", encoding='latin1', sep=';')
        except Exception as e:
            print(f"Error al leer el CSV: {e}")

    @staticmethod
    def cargar_datos():
        print("→ Limpiando y cargando datos...")
        if GestionarObra.df is None:
            print("No se cargaron datos.")
            return

        df = GestionarObra.df.copy()

        try:
            df["monto_contrato"] = pd.to_numeric(df["monto_contrato"], errors="coerce").fillna(0)
            df["porcentaje_avance"] = pd.to_numeric(df["porcentaje_avance"], errors="coerce").fillna(0)
            df["comuna"] = pd.to_numeric(df["comuna"], errors="coerce").fillna(0).astype(int)

            for _, row in df.iterrows():
                Obra.create(
                    nombre=row["nombre"],
                    direccion=row["direccion"],
                    monto=float(row["monto_contrato"]),
                    avance=float(row["porcentaje_avance"]),
                    comuna=int(row["comuna"]),
                    barrio=row.get("barrio"),
                    fecha_inicio=pd.to_datetime(row.get("fecha_inicio"), errors="coerce"),
                    fecha_fin=pd.to_datetime(row.get("fecha_fin_inicial"), errors="coerce"),
                    tipo=row.get("tipo"),
                    descripcion=row.get("descripcion")
                )
            print("→ Datos cargados con éxito.")
        except Exception as e:
            print(f"Error durante la carga de datos: {e}")

    @staticmethod
    def exportar_a_csv(nombre_archivo):
        print(f"→ Exportando datos a {nombre_archivo}...")
        try:
            obras = Obra.select()
            datos = [{
                "nombre": o.nombre,
                "avance": o.avance,
                "monto": o.monto,
                "direccion": o.direccion,
                "comuna": o.comuna,
                "barrio": o.barrio,
                "fecha_inicio": o.fecha_inicio,
                "fecha_fin": o.fecha_fin,
                "tipo": o.tipo,
                "descripcion": o.descripcion
            } for o in obras]
            pd.DataFrame(datos).to_csv(nombre_archivo, index=False)
            print("→ Exportación completada.")
        except Exception as e:
            print(f"Error al exportar: {e}")
