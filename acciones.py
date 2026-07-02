import utils
import colorama as c
import main 
import database_sql as dsql

def registrar_producto()->None:
    '''Registra un producto en la base de datos.
    Returns:None,pero llama a la funcion guardar_productos_sql() que guardara el producto.
    Variables:None.
    Raises:puede generar error al llamar a la funcion guardar_productos_sql().
    '''
    print(c.Fore.BLUE + "\nRegistrar producto" + c.Style.RESET_ALL)
    while True:
        nombre=input("Ingrese el nombre del producto: ").strip()
        if not nombre:
            print("El nombre no puede estar vacio")
        break
    descripcion=input("Ingrese una breve descripcion(opcional): ").strip()
    cantidad=utils.validar_opcion_num("Ingrese la cantidad del producto(1-1000): ",1,1000)
    precio=utils.precio_float()
    categoria=input("Ingrese la categoria del producto(opcional): ")
    dsql.guardar_producto_sql(nombre,descripcion,cantidad,precio,categoria)
    
def mostrar_productos()->None:
    '''Muestra los productos en la base de datos.
    Returns:None,pero llama a la funcion consultar_productos_sql() que trae los productos y muestra los productos.
    Variables:None.
    Raises:puede generar error al llamar a la funcion consultar_productos_sql().'''    
    print(c.Fore.GREEN + "Consultar productos " + c.Style.RESET_ALL)
    print("\n"+c.Fore.BLUE + "Id" +" "*2+"Nombre"+" "*5+"Descripcion"+" "*4+"Cantidad"+" "*3+"Precio"+" "*5+"Categoria"+" "+c.Style.RESET_ALL+"\n")
    inventario=dsql.consultar_productos_sql()
    opcion=utils.validar_opcion_num("Pulse 1 para buscar producto o 0 para volver al menu principal: ",0,1)
    if opcion==1:
        busqueda_del_producto(inventario)
    else:
        main.bucle_main()
        ...

def busqueda_del_producto(inventario)->None:
    '''Busca el producto en la base de datos.
    inventario:lista de tuplas extraido de la base de datos.
    Returns:None
    Raises:puede generar error al llamar a la funcion mostrar_producto() o menu_act_menu()
    tambien puede dar error si no se ingresa una lista de tuplaas.'''
    search=input("Selecciona un producto de la lista(id,producto o categoria)o 0 para ir al menu: ")
    if search == "0":
        main.bucle_main()
    elif search.isdigit() and int(search) > 0 :
        producto=dsql.mostrar_producto(search)
        producto=producto[0]
        utils.menu_act_menu(producto)    
    else:
        lista_resultados=[]
        for items in inventario:
            for item in items:
                if item == search:
                    indice=items[0]
                    producto=dsql.mostrar_producto(indice)
                    #En lista_resultados se guarda los resultados para la funcion(varios_productos(lista_resultados,producto))
                    if producto in lista_resultados:
                        pass
                    else:
                        lista_resultados.append(producto)
        if len(lista_resultados) > 1:
            ultimo_resultado=lista_resultados[-1][0]
            varios_productos(ultimo_resultado)
        else:
            print("No se encontro ningun producto con ese criterio de busqueda,volviendo al menu principal")
            main.bucle_main()
    
    if len(producto) == 1:
        utils.menu_act_menu(producto)
    else:
        varios_productos(producto)    
                
def modificar_productos(producto)->None:
    '''Modifica un producto en la base de datos.
    producto:es una tupla con el producto a modificar.
    Returns:None.
    Raises:puede generar error al no ingresar con una tupla.'''
    categoria=input("Indique la categoria que desea modificar(nombre,descripcion,cantidad,precio,categoria): ")
    entrada=categoria.lower()
    if entrada == "nombre":
        print(f'El nombre actual es "{producto[1]}"')
        new_valor=input("Ingrese el nuevo nombre: ")
        dsql.modificar_producto_sql(new_valor,0,producto[0])
    elif entrada == "descripcion":
        print(f'La descripcion actual es "{producto[2]}"')
        new_valor=input("Ingrese la nueva descripcion: ")
        dsql.modificar_producto_sql(new_valor,1,producto[0])
    elif entrada == "cantidad":
        print(f"La cantidad actual es {producto[3]}")
        new_valor=utils.validar_opcion_num("Ingrese la nueva cantidad",1,1000)
        dsql.modificar_producto_sql(new_valor,2,producto[0])
    elif entrada == "precio":
        print(f'El precio actual es "{producto[4]}"')
        new_valor=input("Ingrese el nuevo precio: ")
        dsql.modificar_producto_sql(new_valor,3,producto[0])
    elif entrada == "categoria":
        print(f'la categoria actual es "{producto[5]}"')
        new_valor=input("Ingrese la nueva categoria: ")
        dsql.modificar_producto_sql(new_valor,4,producto[0])
    else:
        ...
        
    

def eliminar_productos(producto)->None:
    '''Elimina un producto de la base de datos.
    produc:es una tupla con el producto a eliminar.
    Returns:None.
    Raises:puede generar error al no ingresar con una tupla.'''
    opcion_borrar=input(f"Esta seguro que desea eliminar el producto{producto[1]}(si/no)")
    if opcion_borrar.lower() == "si":
        dsql.borrar_producto_sql(producto)
    elif opcion_borrar.lower() == "no":
        print("El producto no se eliminara,volviendo al menu principal")
               


def notificaciones()->None:
    '''Muestra los productos con cantidad menor a la configuracion establecida en el archivo config_notificaciones.txt.
    Returns:None.
    Variables:None.
    Raises:puede generar error al llamar a la funcion notificaciones_sql() o al abrir el archivo config_notificaciones.txt.'''
    while True:
        with open ("config_notificaciones.txt","r") as configuracion:
            config=configuracion.read()
            configurar_notificaciones=False
            if not config:
                configurar_notificaciones=True
            while True:
                if configurar_notificaciones == True:
                    new_valor=utils.validar_opcion_num("""Elije la configuracion de las notificaciones,cuando la cantidad del producto sea menor al valor establecido aparecera en 'Notificaciones': """,1,100000)
                    configuracion=open ("config_notificaciones.txt","w")
                    configuracion.write(str(new_valor))
                    print("Notificaciones se configuro correctamente.")
                    configurar_notificaciones=False
                    configuracion.close()
                    utils.volver_al_menu()
                elif config == "1":
                    print("No hay nada para mostrar.")
                    opcion=utils.validar_opcion_num("Pulse 1 para modificar las notificaciones o 0 para ir al menu principal: ",0,1)
                    if opcion == 0:
                        main.bucle_main()
                    else:
                        configurar_notificaciones=True
                        continue
                    break
                else:    
                    items=dsql.notificaciones_sql(config)
                    if not items:
                        print("No hay nada para mostrar.")
                        opcion=utils.validar_opcion_num("Pulse 1 para modificar las notificaciones o 0 para ir al menu principal: ",0,1)
                        if opcion == 0:
                            main.bucle_main()
                        else:
                            configurar_notificaciones=True
                            continue
                    print("Estos productos estan por debajo del valor establecido.")
                    
                    numeros=0
                    for x in items:
                        numeros+=1
                    if len(items) == 1:
                        print(items[0])
                        opcion=utils.validar_opcion_num("Pulse 1 para modificar las notificaciones o 0 para ir al menu principal: ",0,1)
                        if opcion == 0:
                            main.bucle_main()
                        else:
                            configurar_notificaciones=True
                            continue
                    elif len(items) > 1:
                        for item in items:
                            print(item[0],item[1],item[2],item[3],item[4],item[5])
                        opcion=utils.validar_opcion_num("Pulse 1 para modificar las notificaciones o 0 para ir al menu principal: ",0,1)    
                        if opcion == 0:
                            main.bucle_main()
                        else:
                            configurar_notificaciones=True
                            continue
                    
    

def salir()->None:
    '''Sale del programa.
    Returns:None.
    Variables:None.
    Raises:ninguno que sepa.'''
    opcion_salir=utils.validar_opcion_num("¿Estas seguro que deseas salir?\nPulse 0 para salir o 1 para volver al menu: ",0,1)
    if opcion_salir == 0:
        print("Saliendo del programa")
        exit()
    else:
        main.bucle_main()
        

def match_acciones(opcion)->None:
    '''Recibe la opcion del menu principal y va a la funcion correspondiente.
    opcion:es un int que se le pasa de la funcion bucle_main() que sirve para seleccionar la accion a realizar.
    Retuens:None.
    Raises:puede generar error si no se ingresa un int.'''
    match opcion:
        case 1:
            registrar_producto()
        case 2:
            mostrar_productos()        
        case 3:
            notificaciones()
        case 4:
            salir()
        case _:
            print("opcion invalida")
              
def varios_productos(producto)->None:
    '''Esta funcion sirve si en tu busqueda salieron varios productos.
    producto:es una lista de tuplas con los productos encontrados.
    Returns:None.
    Raises:puede generar error si no se ingresa una lista de tuplas.'''
    indice_producto=utils.validar_opcion_num("Encontramos varios productos con tu criterio de busqueda,selecciona su id o 0 para ir al menu principal:",0,(producto[0]))
    if indice_producto == 0:
        main.bucle_main()
    dsql.mostrar_producto(indice_producto)
    utils.menu_act_menu(producto)
    
