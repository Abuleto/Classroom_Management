import smtplib, socket, sys, getpass, pymysql, os, re

# CONEXIÓN A LA BASE DE DATOS
DB_HOST = 'localhost'
DB_USER = 'root' 
DB_PASS = '' 
DB_NAME = 'aula_python'

conn = pymysql.connect(DB_HOST,DB_USER,DB_PASS,DB_NAME) 
cursor = conn.cursor()

seleccion = 1 #Selección de opciones en el menú.
smtpserver = ""
gmail_user = "" #Guarda el correo electrónico del usuario
conectado = False #Comprueba si está conectado a un servicio de correos o no.

#FUNCIÓN QUE BORRA LA PANTALLA PARA QUE EL MENÚ SEA MÁS LEGIBLE
def limpiarPantalla():
    input("\nPulse INTRO para continuar...") 
    cls = lambda: os.system('cls')  #Limpia consola
    cls()

def menu_inicial():
    salir = False #Permanecerá en el menú hasta que la variable sea true
    print("********** AULA PYTHON **********")
    print("1. Gestión de alumnos.")
    print("2. Enviar correo.")
    print("0. Salir del menú.")
    print("\n\n")

    seleccion = int(input("Seleccione opción: \n"))

    if(seleccion == 1):
        menu_gestion()
    elif(seleccion == 2):
        menu_correo()
    elif(seleccion == 0):
        salir = True
    else: print("Introduzca una opción válida.")

    return salir

def menu_gestion():
    print("********** GESTIÓN DE ALUMNADO **********")
    print("1. Añadir alumnos.")
    print("2. Modificar datos de alumnos.")
    print("3. Eliminar alumnos.")
    print("\n\n")

    seleccion = int(input("Seleccione opción: \n"))

    if(seleccion == 1):
        anadir_alumno()
    elif(seleccion == 2):
        modificar_alumno()
    elif(seleccion == 3):
        eliminar_alumno()

def menu_correo():
    print("********** ENVIAR CORREO **********")
    print("1. Introducir datos del correo.")
    print("2. Enviar correo.")
    print("\n\n")

    seleccion = int(input("Seleccione opción: \n"))

    if(seleccion == 1):
        smtpserver, gmail_user = datos_correo()
    elif(seleccion == 2):
        enviar_correo(smtpserver, gmail_user)
    else: print("Introduzca una opción válida.")

def anadir_alumno():
    
        nombre_tabla = 'alumno'
        print("Datos para "+nombre_tabla+":")
        dni = input("DNI: ")
        while True:
            if re.match("^[0-9]{8,8}[A-Za-z]$", dni):
                break
            else: dni = input("Debe introducir un DNI válido. (8 números y 1 letra al final)\nDNI: ")
        nombre = input("Nombre: ")
        while any(str.isdigit(c) for c in nombre) or len(nombre)>30:
            nombre = input("Recuerde que el nombre no puede contener números ni superar 30 caracteres.\nNombre: ")
        direccion = input("Direccion: ")
        while len(direccion)>30:
            direccion = input("La dirección no puede tener más de 30 caracteres.\nNombre: ")
        while True:
            try:
                edad = int(input("Edad: "))
                if edad > 120 or edad < 3:
                    raise ValueError
                else: break
            except ValueError:
                print("La edad sólo pueden ser números entre 3 y 120")
        while True:
            try:
                telefono = int(input("Teléfono: "))
                if len(str(telefono))!=9:
                    raise ValueError
                else: break
            except ValueError:
                print("El teléfono introducido sólo puede contener números y tener una longitud de 9.")
        correo_electronico = input("Correo Electrónico: ")
        while True:
            if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", correo_electronico):
                break
            else: correo_electronico = input("Debe introducir un correo electrónico válido.\nCorreo Electrónico: ")

        query = "INSERT INTO "+nombre_tabla+"(DNI, NOMBRE, DIRECCION, EDAD, TELEFONO, CORREO_ELECTRONICO) VALUES ( '%s', '%s', '%s', %s, %s, '%s' )" %(dni, nombre, direccion, edad, telefono, correo_electronico)
        cursor.execute(query)
        conn.commit()
        limpiarPantalla()

def modificar_alumno():

        dni = input("DNI: ")
        while True:
            if re.match("^[0-9]{8,8}[A-Za-z]$", dni):
                break
            else: dni = input("Debe introducir un DNI válido. (8 números y 1 letra al final)\nDNI: ")
        resultados = select(dni) #Si hay al menos una coincidencia devolverá True
        if resultados:
            print("Introduzca los nuevos datos:\n")
            nombre = input("Nombre: ")
            while any(str.isdigit(c) for c in nombre) or len(nombre)>30:
                nombre = input("Recuerde que el nombre no puede contener números ni superar 30 caracteres.\nNombre: ")
            direccion = input("Direccion: ")
            while len(direccion)>30:
                direccion = input("La dirección no puede tener más de 30 caracteres.\nNombre: ")
            while True:
                try:
                    edad = int(input("Edad: "))
                    if edad > 120 or edad < 3:
                        raise ValueError
                    else: break
                except ValueError:
                    print("La edad sólo pueden ser números entre 3 y 120")
            while True:
                try:
                    telefono = int(input("Teléfono: "))
                    if len(str(telefono))!=9:
                        raise ValueError
                    else: break
                except ValueError:
                    print("El teléfono introducido sólo puede contener números y tener una longitud de 9.")
            correo_electronico = input("Correo Electrónico: ")
            while True:
                if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", correo_electronico):
                    break
                else: correo_electronico = input("Debe introducir un correo electrónico válido.\nCorreo Electrónico: ")

            query = "UPDATE ALUMNO SET NOMBRE='%s', DIRECCION='%s', EDAD=%s, TELEFONO=%s, CORREO_ELECTRONICO='%s' WHERE DNI='%s'" %(nombre, direccion, edad, telefono, correo_electronico, dni)
            cursor.execute(query)
            conn.commit()
            print("El alumno con DNI: "+dni+" ha sido modificado con éxito.")
        else:
            print("No hay alumnos disponibles para modificar con ese DNI.")

        limpiarPantalla()

def select(dni):
    resultados = False
    query = "SELECT * FROM ALUMNO WHERE DNI='"+dni+"' "
    cursor.execute(query)
    columns = cursor.fetchall()
    for i in columns:
        resultados = True #Si entra en el bucle for significa que hay al menos una coincidencia
        print(i)
    print("\n")
    return resultados

def eliminar_alumno():

    dni = input("DNI: ")
    while True:
        if re.match("^[0-9]{8,8}[A-Za-z]$", dni):
            break
        else: dni = input("Debe introducir un DNI válido. (8 números y 1 letra al final)\nDNI: ")
    resultados = select(dni) #Si hay al menos una coincidencia devolverá True
    if resultados:
        eliminar = input("¿Desea eliminar al alumno? s/n\n")
        if eliminar == 's':
            query = "DELETE FROM ALUMNO WHERE DNI='%s'" %dni
            cursor.execute(query)
            conn.commit()
            print("El alumno con DNI: "+dni+" ha sido eliminado de la Base de Datos.")
    else:
        print("No hay alumnos disponibles para eliminar con ese DNI.")

    limpiarPantalla()


def datos_correo():
    try:
        smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        print("Conexión exitosa con Outlook")
        
        try:
            gmail_user = str(input("Escriba su correo: ")).lower().strip()
            gmail_pwd = getpass.getpass("Escriba su contraseña: ").strip()
            smtpserver.login(gmail_user, gmail_pwd)
            return smtpserver, gmail_user
        except smtplib.SMTPException:
            print("")
            print("Autenticación incorrecta\n")
            smtpserver.close()
            getpass.getpass("Presione ENTER para continuar...")
            sys.exit(1)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException):
        print("Fallo en la conexión con Outlook")
        print("Presione ENTER para continuar...")
        sys.exit(1)
    

def enviar_correo(smtpserver, gmail_user):

    while True:
        to = str(input("Enviar correo a: ")).lower().strip()
        if to != "":
            break
        else:
            print( "Debe especificar el correo del destinatario.")

    sub = str(input("Asunto: ")).strip()
    print(sub)
    bodymsg = str(input("Mensaje: "))
    print("")
    header = "Para: " + to +"\n" + "De: " + gmail_user + "\n" + "Asunto: " + sub + "\n"
    print (header)
    msg = header + "\n" + bodymsg + "\n\n"
    print(msg)

    respuesta = input("¿Desea enviar el correo?")

    if(respuesta == "s" or respuesta == "si" or respuesta == "SI"):
        try:   
            smtpserver.sendmail(gmail_user, to, msg)
        except smtplib.SMTPException:
            print( "El correo no pudo ser enviado" + "\n")
        smtpserver.close()
        getpass.getpass("Presione ENTER para continuar...")
        sys.exit(1)

        print ("El correo se envio correctamente" + "\n")	
        smtpserver.close()
        getpass.getpass("Presione ENTER para continuar")
        sys.exit(1)

while True:

    salir = menu_inicial()
    if salir: break

