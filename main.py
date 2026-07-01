import colorama as c
import utils
import acciones as a
from database_sql import crear_tabla as ct, mostrar_producto,notificaciones_sql as noti 

def menu(numeros_notificaciones=0)->None:
    '''Muestra el titulo y menu principal del programa.
    numeros_notificaciones:en una variable=int que se le pasa que sirve para mostrar el numero de notificaciones de los productos con menor valor a la configuracion establecida.
    Returns:None.
    Raises:Puede ser ValueError si el parametro no es un int.'''
    print(c.Fore.CYAN + "┌" + "─"*50 + "┐")
    print(c.Fore.CYAN + "│" + c.Fore.BLUE + " "*10+"Sistema de gestión de productos" + " "*9 + c.Fore.CYAN + "│")
    print(c.Fore.CYAN + "└" + "─"*50 + "┘\n")
    print(c.Fore.CYAN + "┌" + "─"*50 + "┐")
    print(c.Fore.CYAN + "│" + c.Fore.BLUE + " "+"1_ Registrar producto" + " "*28+ c.Fore.CYAN + "│")
    print(c.Fore.CYAN + "│" + c.Fore.GREEN + " "+"2_ Consultar productos" + " "*27+ c.Fore.CYAN + "│")
    print(c.Fore.CYAN + "│" + c.Fore.YELLOW + " "+"3_ Notificaciones",c.Fore.LIGHTMAGENTA_EX+f"[{numeros_notificaciones}]" + " "*(29-len(str(numeros_notificaciones)))+ c.Fore.CYAN + "│")
    print(c.Fore.CYAN + "│" + c.Fore.RED + " "+"4_ Salir" + " "*41+ c.Fore.CYAN + "│")
    print(c.Fore.CYAN + "└" + "─"*50 + "┘\n"+c.Style.RESET_ALL)
    
def lista_consulta_producto(inventario)->None:
    '''De "inventario" extrae la consulta sql y la muestra en pantalla
    inventario:es una lista de tuplas que contiene los datos de la consulta sql.
    Returns:None.
    Raises:Puede ser ValueError si el parametro no es una lista de tuplas.'''
    for id,nombre,descripcion,cantidad,precio,categoria in inventario:    
            print(str(id)+" "*(3-len(str(id))),nombre+" "*(10-len(nombre)),descripcion+" "*(14-len(descripcion)),str(cantidad)+" "*(10-len(str(cantidad))),"$",str(precio)+" "*(10-len(str(precio))),categoria)
    

def bucle_main()->int:
    '''Bucle principal del programa,llama al menu,actualiza las notificaciones y llama a la funcion match_acciones.
    Args:None.
    Returns:int que se usa para la funcion menu(numeros_notificaciones)
    Raises:Puede generar error al llamar a las funciones dentro,pero no estoy seguro.)'''
    utils.crear_config_notificaciones()
    numeros_notificaciones=0
    ct()  
    #______cuenta los productos con cantidad menor a 10 y el valor se muestra en notificaciones.
    notifiaciones=noti()

    if notifiaciones == 0:
        pass
    else:
        for x in notifiaciones:
            numeros_notificaciones+=1
    #_______
    menu(numeros_notificaciones)    
    opcion= utils.validar_opcion_num("Ingrese una opción(1-4): ")
    a.match_acciones(opcion)
    return numeros_notificaciones

if __name__=="__main__":
        bucle_main()