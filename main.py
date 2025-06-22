from gestionar_obras import GestionarObra

def main():
    GestionarObra.conectar_db()
    GestionarObra.mapear_orm()
    GestionarObra.extraer_datos()
    GestionarObra.cargar_datos()
    GestionarObra.obtener_indicadores()
    GestionarObra.obras_por_comuna(5)  # Cambiá el número si querés otra comuna
    GestionarObra.exportar_a_csv("obras_exportadas.csv")

if __name__ == "__main__":
    main()

