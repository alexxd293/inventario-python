import json
import os

DIRECTORIO = os.path.dirname(__file__)
RUTA_ARCHIVO = os.path.join(DIRECTORIO, 'productos.json')

class Producto:
    def __init__(self, Nombre, Precio, Cantidad, ID):
        self.nombre = Nombre
        self.precio = Precio
        self.cantidad = Cantidad
        self.id = ID
    
    def __repr__(self):
        return f"Producto: {self.nombre}, Precio: {self.precio}, ID: {self.id}, Cantidad: {self.cantidad}"
    
    def to_dict(self):
        return {"Nombre": self.nombre, "Precio": self.precio, "Cantidad": self.cantidad, "ID": self.id}

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar(self, Nombre, Precio, Cantidad, ID):
        self.productos[ID] = Producto(Nombre, Precio, Cantidad, ID)

    def __repr__(self):
        return str(self.productos)
    
    def abrir_json(self):
        try:
            with open(RUTA_ARCHIVO, 'r') as file:
                data = json.load(file)
                for id, dato in data.items():
                    self.agregar(dato['Nombre'],dato['Precio'],dato['Cantidad'],dato['ID'])
        except FileNotFoundError:
            print("Archivo no encontrado")


    def guardar_json(self):
        diccionario_final = {}
        for id_project, obj_prod in self.productos.items():
            diccionario_final[id_project] = obj_prod.to_dict()
        

        with open(RUTA_ARCHIVO,'w') as file:
            json.dump(diccionario_final, file)
    
    def eliminar(self, ID):
        del self.productos[ID]

    
    def mostrar_inventario(self):
        if not self.productos:
            print("El inventario esta vacio")
            return

        print("\n--- LISTA DE PRODUCTOS ---")
        for prod in self.productos.values():
            print(f"ID: {prod.id} | Nombre: {prod.nombre} | Precio: S/.{prod.precio:.2f} | Stock: {prod.cantidad}")
        print("--------------------------\n")


inventario = Inventario()
inventario.abrir_json()

while True:
    try:
        opcion = int(input("Elija una opcion:"
                        "\n1: Agregar producto"
                        "\n2: Ver inventario"
                        "\n3: Eliminar Producto"
                        "\n4: Salir"
                        '\n'))
    except ValueError:
        print("Ingrese un numero del 1-4")
        continue
    
    if opcion == 1:

        id_valido = False
        while True:
            nombreproducto = input("Nombre: ").strip().capitalize()
            if not nombreproducto.replace(" ", "").isalpha():
                print("Error: El nombre solo debe contener letras.")
                
            elif len(nombreproducto) < 2:
                print("Error: El nombre es muy corto o está vacío.")

            else:
                break

        while True:
            try:
                precioproducto = float(input("Precio: "))
                break
            except ValueError:
                print("Ingrese solo numeros")
    
        while True:
            try:
                cantidadproducto = int(input("Cantidad: "))
                break
            except ValueError:
                print("Ingrese solo numeros")

        while not id_valido:
            idproducto = input("id: ").strip()
            if not idproducto.isdigit():
                print("El id solo debe contener numeros")
                continue
            elif len(idproducto) != 6:
                print("El id debe contener 6 numeros")
                continue
            elif idproducto in inventario.productos:
                producto_actual = inventario.productos[idproducto].nombre
                print(f"Error: El ID '{idproducto}' ya pertenece al producto: {producto_actual}")
                decision = input("¿Deseas intentar con otro ID? (s/n): ").lower()
                if decision != 's':
                    break 
            else:
                id_valido = True


        if id_valido:
            inventario.agregar(nombreproducto, precioproducto, cantidadproducto, idproducto)
            inventario.guardar_json()
            print("Producto guardado correctamente.")
        else:
            print("Operación cancelada: No se agregó el producto.")
    elif opcion == 2:
        inventario.mostrar_inventario()
    elif opcion == 3:
        producto_eliminar = input("ingrese id: ")
        if producto_eliminar in inventario.productos:
            inventario.eliminar(producto_eliminar)
            inventario.guardar_json()
            print(f"Producto eliminado con exito")
            
        else: 
            print("Producto no encontrado")
    elif opcion == 4:
        inventario.guardar_json()
        break
    else:
        print(f"\nLa opción '{opcion}' no es válida. Por favor, elige del 1 al 4.")