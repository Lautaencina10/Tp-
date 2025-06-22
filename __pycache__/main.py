from gestionar_obras import GestionarObra

def main():
    GestionarObra.conectar_db()
    GestionarObra.mapear_orm()
    GestionarObra.extraer_datos()
    GestionarObra.cargar_datos()
    GestionarObra.exportar_a_csv("obras_exportadas.csv")

if __name__ == "__main__":
    main()
