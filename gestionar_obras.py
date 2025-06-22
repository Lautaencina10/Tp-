from peewee import fn
import pandas as pd
from modelo_orm import Obra, sqlite_db as db

class GestionarObra:

    df = None

    @staticmethod
    def conectar_db():
        print("→ Conectando a la base de datos...")
        try:
            db.connect()
        except Exception as e:
            print(f"Error al conectar a la DB: {e}")

    @staticmethod
    def mapear_orm():
        print("→ Creando tablas si no existen...")
        try:
            db.create_tables([Obra])
        except Exception as e:
            print(f"Error al crear tablas: {e}")

    @staticmethod
    def extraer_datos():
        print("→ Leyendo datos desde el CSV...")
        try:
            GestionarObra.df = pd.read_csv("observatorio-de-obras-urbanas.csv", encoding='latin1', sep=';')
        except Exception as e:
            print(f"Error al leer el CSV: {e}")

    @staticmethod
    def limpiar_columna_numerica(col):
        return (
            col.astype(str)
               .str.replace(",", ".", regex=False)
               .str.replace("%", "", regex=False)
               .str.extract(r"(\d+\.?\d*)")[0]
               .astype(float)
               .fillna(0.0)
        )

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
                try:
                    Obra.create(
                        Nombre_obra=row["nombre"],
                        Etapa=row["etapa"],
                        Descripcion=row.get("descripcion", ""),
                        Monto_contrato=row["monto_contrato"],
                        Porcentaje_avance=row["porcentaje_avance"],
                        Fecha_inicio=pd.to_datetime(row["fecha_inicio"], dayfirst=True, errors='coerce'),
                        Fecha_fin=pd.to_datetime(row["fecha_fin_inicial"], dayfirst=True, errors='coerce'),
                        Plazo=int(row["plazo_meses"]) if pd.notna(row["plazo_meses"]) else None,
                        Direccion=row.get("direccion", ""),
                        Compromiso=row.get("compromiso", ""),
                        Destacada=row.get("destacada", ""),
                        ba_elige=row.get("ba_elige", ""),
                        año_licitacion=str(row.get("licitacion_anio", "")),
                        Nro_contratacion=str(row.get("nro_contratacion", "")),
                        Cuit_contratista=str(row.get("cuit_contratista", "")),
                        Mano_de_obra=int(row["mano_obra"]) if pd.notna(row["mano_obra"]) else None
                    )
                except Exception as e:
                    print(f"Error en fila {row['nombre']}: {e}")

            print("→ Datos cargados con éxito.")
        except Exception as e:
            print(f"Error durante la carga de datos: {e}")

    @staticmethod
    def obtener_indicadores():
        print("→ Indicadores básicos:")
        try:
            promedio_avance = Obra.select(fn.AVG(Obra.Porcentaje_avance)).scalar()
            total_monto = Obra.select(fn.SUM(Obra.Monto_contrato)).scalar()

            if promedio_avance is not None:
                print(f"   - Promedio avance: {promedio_avance:.2f}%")
            else:
                print("   - Promedio avance: No disponible")

            if total_monto is not None:
                print(f"   - Monto total invertido: ${total_monto:,.2f}")
            else:
                print("   - Monto total invertido: No disponible")
        except Exception as e:
            print(f"Error al calcular indicadores: {e}")

    @staticmethod
    def obras_por_comuna(numero):
        print(f"→ Obras en la comuna {numero}:")
        try:
            obras = Obra.select().where(Obra.Comuna == numero)
            if obras:
                for obra in obras:
                    print(f"   - {obra.Nombre_obra} | Avance: {obra.Porcentaje_avance}%")
            else:
                print("   No se encontraron obras.")
        except Exception as e:
            print(f"Error al obtener obras por comuna: {e}")

    @staticmethod
    def exportar_a_csv(nombre_archivo):
        print(f"→ Exportando datos a {nombre_archivo}...")
        try:
            data = [{
                "nombre": o.Nombre_obra,
                "avance": o.Porcentaje_avance,
                "monto": o.Monto_contrato,
                "direccion": o.Direccion
            } for o in Obra.select()]

            export_df = pd.DataFrame(data)
            export_df.to_csv(nombre_archivo, index=False, encoding="utf-8")
            print("→ Exportación completada.")
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
