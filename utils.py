import colorama as c
import acciones as a
import main


def validar_opcion_num(text_str:str,min_opcion:int=1, max_opcion:int=4)-> int:
    '''Valida una opcion numerica ingresada por el usuario.
    text_str:es un texto que se muestra en pantalla.
    min_opcion:valor minimo que puede ingresar el usuario.
    max_opcion:idem pero maximo.
    Returns:int con la opcion valida ingresada por el ususario.
    Raises:Puede haber errores al ingresar los parametros de la funcion.'''
    contador_intentos = 0
    while True:   
        try:
            opcion=input(text_str)
            if opcion.isdigit() and (min_opcion <= int(opcion) <= max_opcion):
                return int(opcion)
                break
            else:
                print(c.Fore.RED + f"Opción inválida. Por favor, ingrese un número entre {min_opcion} y {max_opcion}." + c.Style.RESET_ALL)
                contador_intentos += 1
                muchos_intentos(contador_intentos)
        except ValueError:
            print(c.Fore.RED + f"Opción inválida. Por favor, ingrese un número entre {min_opcion} y {max_opcion}." + c.Style.RESET_ALL)
            contador_intentos += 1
            muchos_intentos(contador_intentos)

def muchos_intentos(contador_intentos:int,max_intentos:int=6):
    '''Si son muchos intentos de ingresar una opcion numerica,se sale del programa.
    contador_intentos:es un numero entero que se le pasa para compararlo con max_intentos,si son iguales,se sale del programa.
    max_intentos:es el numero maximo de intentos.
    Returns:None.
    Raises:puede generar errores al ingresar mal los parametros de la funcion'''
    if contador_intentos >= max_intentos:
        print(c.Fore.RED + "Se han agotado los intentos. Saliendo del programa..." + c.Style.RESET_ALL)
        exit()

def precio_float()->float:
    '''Valida el precio ingresado por el usuario.
    Returns:float(precio) verificado por la funcion.
    Variables:None.
    Raises:puede ser ValueError.No es un error pero deberia poner la funcion muchos_intentos().
    '''
    while True:
        try:
            precio=float(input("Ingrese el precio del producto:$"))
            if not precio:
                print("El precio no puede estar vacio")
                continue
            return precio
        except ValueError as e:
            print(f"Error de precio {e}")
            print("por favor intentelo de nuevo")

def menu_act_menu(producto)->None:
    '''Pequeña parte del codigo que se repite(
        "Pulse 1 para actualizar producto,2 para eliminar producto o 0 para volver al menu principal: ")
        producto:es una lista de tuplas con producto/s.
        Returns:None.
        Raises:puede generar error si no se ingresa una lista de tupla/tuplas.'''
    opcion=validar_opcion_num("Pulse 1 para actualizar producto,2 para eliminar producto o 0 para volver al menu principal: ",0,2)
    match opcion:
        case 1:
            a.modificar_productos(producto)
        case 2:
            a.eliminar_productos(producto)
        case 0:
            main.bucle_main()
            
def volver_al_menu(palabras:str=None)->None:
    '''Pequeña funcion para volver al menu principal.
    palabras:es un texto que se muestra en pantalla,por defecto es None,si es None se ejecuta el else,sino el if.
    Returns:None.
    Raises:puede generar ValueError si el parametro no es una string,no se puede sumar con el texto en el if.
    '''
    if palabras:
        volver_al_menu=input(palabras+"Preciones una tecla para volver al menu principal.")
    else:
        volver_al_menu=input("Preciones una tecla para volver al menu principal.")
    main.bucle_main()
    
def crear_config_notificaciones()->None:
    '''Crea  un txt de las configuraciones de las notificaciones si no existe,primer intento con la opcion "x".
    Returns:None.
    Raises:Puede generar error al crear el archivo,pero no estoy seguro.'''
    try:
        open("config_notificaciones.txt", "x").close()
    except FileExistsError:
        pass
        
        