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
        sqlite_db.create_tables([Obra])

    @staticmethod
    def extraer_datos():
        print("→ Leyendo datos desde el CSV...")
        try:
            GestionarObra.df = pd.read_csv("observatorio-de-obras-urbanas.csv")
        except Exception as e:
            print("Error al leer CSV:", e)

    @staticmethod
    def limpiar_columna_numerica(columna):
        return pd.to_numeric(columna.astype(str).str.replace(",", "."), errors="coerce")

    @staticmethod
    def cargar_datos():
        print("→ Limpiando y cargando datos...")
        if GestionarObra.df is None:
            print("No se cargaron datos.")
            return

        df = GestionarObra.df.copy()

        try:
            df["monto_contrato"] = GestionarObra.limpiar_columna_numerica(df["monto_contrato"])
            df["porcentaje_avance"] = GestionarObra.limpiar_columna_numerica(df["porcentaje_avance"])

            for _, row in df.iterrows():
                Obra.create(
                    nombre=row.get("nombre", ""),
                    direccion=row.get("direccion", ""),
                    monto_contrato=float(row["monto_contrato"]) if pd.notna(row["monto_contrato"]) else 0.0,
                    porcentaje_avance=float(row["porcentaje_avance"]) if pd.notna(row["porcentaje_avance"]) else 0.0,
                )
            print("→ Datos cargados con éxito.")
        except Exception as e:
            print("Error durante la carga de datos:", e)

    @staticmethod
    def exportar_a_csv(nombre_archivo):
        print(f"→ Exportando datos a {nombre_archivo}...")
        try:
            obras = Obra.select()
            data = [{
                "nombre": o.nombre,
                "avance": o.porcentaje_avance,
                "monto": o.monto_contrato,
                "direccion": o.direccion
            } for o in obras]
            df_export = pd.DataFrame(data)
            df_export.to_csv(nombre_archivo, index=False)
            print("→ Exportación completada.")
        except Exception as e:
            print("Error al exportar:", e)
