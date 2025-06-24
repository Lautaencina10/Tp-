from gestionar_obras import GestionarObra
from modelo_orm import sqlite_db
import os

def menu():
    print("\n--- Menú Principal ---")
    print("1. Conectar base de datos")
    print("2. Leer y cargar datos desde CSV")
    print("3. Crear nueva obra")
    print("4. Ver indicadores")
    print("5. Exportar a CSV")
    print("6. Salir")
    return input("Seleccione una opción: ")

def main():
    csv_path = "observatorio-de-obras-urbanas.csv"

    while True:
        opcion = menu()
        
        if opcion == "1":
            print("→ Conectando a la base de datos...")
            GestionarObra.conectar_db()
            GestionarObra.mapear_orm()

        elif opcion == "2":
            print("→ Procesando CSV y cargando datos a la base...")
            if not os.path.exists(csv_path):
                print(" El archivo CSV no se encuentra en la carpeta.")
            else:
                GestionarObra.extraer_datos(csv_path)
                GestionarObra.limpiar_datos()
                GestionarObra.cargar_datos()

        elif opcion == "3":
            print("→ Crear nueva obra")
            GestionarObra.nueva_obra()

        elif opcion == "4":
            print("→ Indicadores básicos")
            GestionarObra.obtener_indicadores()

        elif opcion == "5":
            print("→ Exportando datos seleccionados a obras_exportadas.csv")
            GestionarObra.exportar_csv()

        elif opcion == "6":
            print("→ Saliendo del sistema...")
            break

        else:
            print(" Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
