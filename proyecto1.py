from re import A
from tkinter.tix import PopupMenu
import numpy as np
import copy 
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import sys, os

import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)
    
clave_path=resource_path("serviceAccountKey.json")

cred = credentials.Certificate(clave_path)
firebase_admin.initialize_app(cred)

db=firestore.client()
                               
#Perfiles
perfiles=["Oficinista", "Editor Video", "Gamer_Bajo", "Gamer_Medio", "Gamer_Alto", "Render", "Programador","Musico","EditorVideo","Streaming"]
cpu_escogida="VACIO"
mb_escogida="VACIO"
gpu_escogida="VACIO"
ram_escogida="VACIO"
st_escogido="VACIO"
psu_escogida="VACIO"
usuario_reglas=[]
usuario_contenido=[]
perfilPrimario=""
perfilSecundario=""
reglas_cpu_ig=False
reglas_cpu_fan=True

ram = ["2 GB-2500 MHz","4 GB-2500 MHz","8 GB-2500 MHz","16 GB-2500 MHz","32 GB-2500 MHz","64 GB-2500 MHz","128 GB-2500 MHz",
"2 GB-3600 MHz","4 GB-3600 MHz","8 GB-3600 MHz","16 GB-3600 MHz","32 GB-3600 MHz","64 GB-3600 MHz","128 GB-3600 MHz"]

st = ["1 HDD-250 GB", "1 HDD-500 GB", "1 HDD-1 TB", "1 HDD-2 TB", "1 SSD-250 GB", "1 SSD-500 GB", "1 SSD-1 TB", "1 SSD-2 TB",
"1 SSD M.2-250 GB", "1 SSD M.2-500 GB", "1 SSD M.2-1 TB", "1 SSD M.2-2 TB"]

root = Tk()
root.geometry("1000x500")
root.title("Proyecto Sistema Recomendador")

perfil_label=Label(root, text="2. Introducir Perfiles: (Mayor prioridad perfil de arriba)")
perfil_label.place(x=100,y=150)
perfil1 = StringVar(root)
perfil2 = StringVar(root)
choices = {"Gamer","Oficinista", "Render","Programador","Musico","EditorVideo","Streaming"}
perfil1.set("Vacio")
perfil2.set("Vacio")
popmenu = OptionMenu(root,perfil1,*choices)
popmenu2 = OptionMenu(root,perfil2,*choices)
popmenu.place(x=100,y=200)
popmenu2.place(x=100,y=250)

altura_escogida = StringVar(root)
choices_altura = {"35 - 42 cm","43 - 53 cm"}
altura_escogida.set("Vacio")
popmenu_altura = OptionMenu(root,altura_escogida,*choices_altura)
popmenu_altura.place(x=100,y=370)
altura_label=Label(root, text="3. Introducir Altura aproximada que su gabinete puede tener: ")
altura_label.place(x=100,y=320)
altura_gabinete=""

presu_label=Label(root, text="1. Introducir Presupuesto: ")
presu_label.place(x=100,y=50)
presu_entry = Entry(root)
presu_entry.place(x=100,y=100)

presupuesto = 0

my_tabla = ttk.Treeview(root)
my_tabla['columns'] = ("Tipo", "Nombre", "Puntaje")
#formato Columna
my_tabla.column("#0", width=0, stretch=NO)
my_tabla.column("Tipo", anchor=W, width=100)
my_tabla.column("Nombre", anchor=W, width=200)
my_tabla.column("Puntaje", anchor=CENTER, width=100)

#Headers
my_tabla.heading("#0", text="")
my_tabla.heading("Tipo", text="Tipo", anchor=W)
my_tabla.heading("Nombre", text="Nombre", anchor=W)
my_tabla.heading("Puntaje", text="Puntaje", anchor=CENTER)

#Poner info
for i in range(2):
    my_tabla.insert(parent='', index='end', iid=i, text="", values=("","",""))


def seleccionar_parte():
    global cpu_escogida
    global mb_escogida
    global gpu_escogida
    global ram_escogida
    global st_escogido
    global my_tabla

    seleccion = my_tabla.focus()
    valores = my_tabla.item(seleccion,"values")
    print(valores)

    if(valores[0]=="CPU"):
        cpu_escogida=valores[1]
        print(cpu_escogida)
        establecer_mb()
    elif(valores[0]=="TM"):
        mb_escogida=valores[1]
        print(mb_escogida)
        establecer_gpu()
    elif(valores[0]=="GPU"):
        gpu_escogida=valores[1]
        print(gpu_escogida)
        establecer_ram()
    elif(valores[0]=="RAM"):
        ram_escogida=valores[1]
        print(ram_escogida)
        establecer_st()
    elif(valores[0]=="Almacenamiento"):
        st_escogido=valores[1]
        print(st_escogido)
        establecer_ps()
    else:
        print("Por favor escoger una parte")


def crear_tabla(nombre_tabla, lista_productos, lista_puntajes, parte):

    top = Toplevel()
    top.title(nombre_tabla)
    top.geometry("500x500")
    my_tabla = ttk.Treeview(top)
    my_tabla['columns'] = ("Nombre", "Puntaje")
    #formato Columna
    my_tabla.column("#0", width=0, stretch=NO)
    my_tabla.column("Nombre", anchor=W, width=230)
    my_tabla.column("Puntaje", anchor=CENTER, width=100)
    #Headers
    my_tabla.heading("#0", text="")
    my_tabla.heading("Nombre", text="Nombre", anchor=W)
    my_tabla.heading("Puntaje", text="Puntaje", anchor=CENTER)
    #Poner info
    for i in range(len(lista_productos)):
        my_tabla.insert(parent='', index='end', iid=i, text="", values=(lista_productos[i], lista_puntajes[i]))

    my_tabla.place(x=0,y=0)

    eleccion_entry = Entry(top)
    eleccion_entry.place(x=50,y=250)

    buttonsele = Button(top,text="Escoger Parte", command=seleccionar_parte(eleccion_entry.get(),parte))
    buttonsele.place(x=300,y=250)

    
def diferenciar_Gamer(reglas):
    perfil_gamer_modificado=''
    if(reglas[0]==1):
        perfil_gamer_modificado="Gamer_Bajo"
    elif(reglas[1]==1):
        perfil_gamer_modificado="Gamer_Medio"
    elif(reglas[2]==1):
       perfil_gamer_modificado="Gamer_Alto"
    
    return perfil_gamer_modificado


def agregar_reglas_presupuesto(lista_reglas):
    if(presupuesto >= 2500000 and presupuesto <= 4000000):
        bajo = [1,0,0]
        for i in range(len(bajo)):
            lista_reglas.append(bajo[i])
    elif(presupuesto >= 4000001 and presupuesto <= 6500000):
        medio = [0,1,0]
        for i in range(len(medio)):
            lista_reglas.append(medio[i])
    elif(presupuesto >= 6500001):
        alto = [0,0,1]
        for i in range(len(alto)):
            lista_reglas.append(alto[i])

    
def filtrar_productos(reglas_producto,reglas_usuario, condicion):
    filtro = True
    if(condicion==0): #no importa si es 0 o 1, debe ser igual
        if(reglas_producto == reglas_usuario):
            filtro = True
        else:
            filtro= False
    
    if(condicion==1): #las 2 condiciones deben ser 0
        if(reglas_producto == 0 and reglas_usuario == 0):
            filtro = True
        else:
            filtro= False
    
    if(condicion==2): #las 2 condiciones deben ser 1
        if(reglas_producto == 1 and reglas_usuario == 1):
            filtro = True
        else:
            filtro= False

    return filtro


def establecer_lista_final():

    mensajeFinal=""
    per1 = False
    per2 = False
    global reglas_cpu_ig
    global parte_label

    archivo = open('Lista de Recomendaciones.txt','w')

    if(perfilPrimario in perfiles):
        per1 = True
    if(perfilSecundario in perfiles):
        per2=True
    #Para poner perfil(es)
    if(per1 and not per2):
        mensajeFinal="Para el perfil: " + str(perfilPrimario) + "\n"
    elif(per1 and per2):
        mensajeFinal="Para los perfiles: " + str(perfilPrimario) + " y " + str(perfilSecundario) + "\n"
    
    #Presupuesto
    mensajeFinal = mensajeFinal + "Con presupuesto de: " + str(presupuesto) + " el sistema recomendó: \n"
    #CPU
    mensajeFinal = mensajeFinal + "CPU: " + cpu_escogida + "\n"
    if(reglas_cpu_fan==False):
        mensajeFinal = mensajeFinal + "El CPU recomendado no trae ventilador incluido, hay que adquirirlo por aparte" + "\n"

    #MB
    mensajeFinal  = mensajeFinal + "Tarjeta Madre: " + mb_escogida + "\n"
    #GPU
    mensajeFinal  = mensajeFinal + "Tarjeta Grafica: " + gpu_escogida + "\n"
    if(reglas_cpu_ig):
        mensajeFinal = mensajeFinal + "Tu CPU tiene graficos integrados, si necesitas ahorrar puede NO comprar la GPU recomendada " + "\n"

    #RAM
    mensajeFinal  = mensajeFinal + "RAM: " + ram_escogida + "\n"
    #Storage
    mensajeFinal  = mensajeFinal + "Almacenamiento: " + st_escogido + "\n"
    #PSU
    mensajeFinal  = mensajeFinal + "Fuente Alimentacion: " + psu_escogida + "\n"
    #Gabinete
    if(altura_gabinete=="matx"):
        mensajeFinal  = mensajeFinal + "Gabinete: Mini-Tower "  "\n"
    else:
        mensajeFinal  = mensajeFinal + "Gabinete: Mid-Tower "  "\n"

    archivo.write(mensajeFinal)
    archivo.close()

    print("Terminado")


def establecer_ps():
    global psu_escogida

    all_info_gpu_elegida = db.collection("GPU").where("nombre","==",gpu_escogida).get()
    for i in all_info_gpu_elegida:
        info_gpu_elegida = i.to_dict()
        tdp_gpu_elegida = info_gpu_elegida["TDP"]
    
    tdp_gpu_elegida=int(tdp_gpu_elegida)
    psu_escogida = tdp_gpu_elegida + 500

    psu_escogida="PSU de " + str(psu_escogida) + " W como minimo"

    parte_label.config(text="PROCESO TERMINADO, revisar archivo de texto con la lista final")
    print(psu_escogida)

    buttonsele.config(state=DISABLED)

    establecer_lista_final()


def establecer_st():

    global st
    global parte_label

    usuario_contenido_st=[]
    reglas_mb_st=[]
    lista_st=[]
    lista_st=copy.deepcopy(st)

    all_info_mb_elegida = db.collection("MB").where("nombre","==",mb_escogida).get()
    for i in all_info_mb_elegida:
        info_mb_elegida = i.to_dict()
        reglas_mb_st = info_mb_elegida["contenido"]

    print(reglas_mb_st)

    #Sacar contenido usuario gpu
    #contenido_usuario
    if(perfilPrimario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilPrimario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_st_"+ perfilPrimario.lower()
            perfil_contenido = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido)

    if(perfilSecundario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilSecundario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_st_"+ perfilSecundario.lower()
            perfil_contenido2 = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido2)
    
    if(perfilPrimario in perfiles and not(perfilSecundario in perfiles)):
        for i in range(len(perfil_contenido)):
            usuario_contenido_st.append(perfil_contenido[i])  #+0.5 es para dar mas importacia el perfil 1
        print("Vector de contenido Usuario Almacenamiento")
        print(usuario_contenido_st)
    elif(perfilSecundario in perfiles and not(perfilPrimario in perfiles)):
        for i in range(len(perfil_contenido2)):
            usuario_contenido_st.append(perfil_contenido2[i])
        print("Vector de contenido UsuarioAlmacenamiento")
        print(usuario_contenido_st)
    else:
        for i in range(len(perfil_contenido)):
            if(float(perfil_contenido[i])<float(perfil_contenido2[i])):
               usuario_contenido_st.append((float(perfil_contenido[i])+float(perfil_contenido2[i]-(perfil_contenido[i]/2)))/2)  #para el mayor valor de p2 no suba tanto esa necesidad
            elif(float(perfil_contenido[i])>float(perfil_contenido2[i])):
                usuario_contenido_st.append((float(perfil_contenido[i])+float(perfil_contenido2[i]+(perfil_contenido[i]/2)))/2)  #para el menor valor de p2 no baje tanto esa necesidad
            else:
                usuario_contenido_st.append((float(perfil_contenido[i])+float(perfil_contenido2[i]))/2)

        print("Vector de contenido Usuario  Almacenamiento")
        print(usuario_contenido_st)

    
    if(reglas_mb_st[10]==0 and reglas_mb_st[11]==0): #si no tiene slots M.2
        print("se quitaron M.2")
        usuario_contenido_st.pop(-1)
        usuario_contenido_st.pop(-1)
        usuario_contenido_st.pop(-1)
        usuario_contenido_st.pop(-1)
        lista_st.pop(-1)
        lista_st.pop(-1)
        lista_st.pop(-1)
        lista_st.pop(-1)
    
    #print(usuario_contenido_ram)
    #print(lista_ram)
 
    lista_st_con_puntajes=[]
    top_st=[0,0,0,0,0]  #tres espacios para que exista un top 3
    
    #juntar nombre cpu con puntaje para poder hacer ranking
    for i in range(len(lista_st)):
        lista_st_con_puntajes.append(lista_st[i])
        lista_st_con_puntajes.append(usuario_contenido_st[i])

    usuario_contenido_st.sort(reverse=True)
    
    for i in range(len(top_st)):
        for j in range(len(lista_st_con_puntajes)):
            if(usuario_contenido_st[i]==lista_st_con_puntajes[j] and lista_st_con_puntajes[j-1] not in top_st):
                top_st[i]=lista_st_con_puntajes[j-1]
    
    parte_label.config(text="Lista de Almacenamiento Recomendadas (Se puede adquirir mas de uno):")
   
    #Poner info
    for row in my_tabla.get_children():
        my_tabla.delete(row)
    for i in range(len(top_st)):
        my_tabla.insert(parent='', index='end', iid=i, text="", values=("Almacenamiento",top_st[i], usuario_contenido_st[i]))

    print(top_st)
    print(usuario_contenido_st)


def establecer_ram():

    global ram
    global parte_label

    usuario_contenido_ram=[]
    reglas_mb_max_ram=[]
    lista_ram=[]
    lista_ram=copy.deepcopy(ram)

    all_info_mb_elegida = db.collection("MB").where("nombre","==",mb_escogida).get()
    for i in all_info_mb_elegida:
        info_mb_elegida = i.to_dict()
        reglas_mb_max_ram = info_mb_elegida["contenido"]

    print(reglas_mb_max_ram)

    #Sacar contenido usuario gpu
    #contenido_usuario
    if(perfilPrimario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilPrimario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_ram_"+ perfilPrimario.lower()
            perfil_contenido = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido)

    if(perfilSecundario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilSecundario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_ram_"+ perfilSecundario.lower()
            perfil_contenido2 = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido2)
    
    if(perfilPrimario in perfiles and not(perfilSecundario in perfiles)):
        for i in range(len(perfil_contenido)):
            usuario_contenido_ram.append(perfil_contenido[i])  #+0.5 es para dar mas importacia el perfil 1
        print("Vector de contenido Usuario RAM")
        print(usuario_contenido_ram)
    elif(perfilSecundario in perfiles and not(perfilPrimario in perfiles)):
        for i in range(len(perfil_contenido2)):
            usuario_contenido_ram.append(perfil_contenido2[i])
        print("Vector de contenido Usuario RAM")
        print(usuario_contenido_ram)
    else:
        for i in range(len(perfil_contenido)):
            if(float(perfil_contenido[i])<float(perfil_contenido2[i])):
               usuario_contenido_ram.append((float(perfil_contenido[i])+float(perfil_contenido2[i]-(perfil_contenido[i]/2)))/2)  #para el mayor valor de p2 no suba tanto esa necesidad
            elif(float(perfil_contenido[i])>float(perfil_contenido2[i])):
                usuario_contenido_ram.append((float(perfil_contenido[i])+float(perfil_contenido2[i]+(perfil_contenido[i]/2)))/2)  #para el menor valor de p2 no baje tanto esa necesidad
            else:
                usuario_contenido_ram.append((float(perfil_contenido[i])+float(perfil_contenido2[i]))/2)

        print("Vector de contenido Usuario MB")
        print(usuario_contenido_ram)

    
    if(reglas_mb_max_ram[4]==0): #si no tiene capacidad de 128GB
        usuario_contenido_ram.pop(6)
        usuario_contenido_ram.pop(-1)
        lista_ram.pop(6)
        lista_ram.pop(-1)
    
    #print(usuario_contenido_ram)
    #print(lista_ram)
 
    lista_ram_con_puntajes=[]
    top_ram=[0,0,0,0,0]  #tres espacios para que exista un top 3
    
    #juntar nombre cpu con puntaje para poder hacer ranking
    for i in range(len(lista_ram)):
        lista_ram_con_puntajes.append(lista_ram[i])
        lista_ram_con_puntajes.append(usuario_contenido_ram[i])

   
    usuario_contenido_ram.sort(reverse=True)
    
    for i in range(len(top_ram)):
        for j in range(len(lista_ram_con_puntajes)):
            if(usuario_contenido_ram[i]==lista_ram_con_puntajes[j] and lista_ram_con_puntajes[j-1] not in top_ram):
                top_ram[i]=lista_ram_con_puntajes[j-1]
    
    parte_label.config(text="Lista de RAM Recomendadas:")
   
    #Poner info
    for row in my_tabla.get_children():
        my_tabla.delete(row)
    for i in range(len(top_ram)):
        my_tabla.insert(parent='', index='end', iid=i, text="", values=("RAM",top_ram[i], usuario_contenido_ram[i]))

   
    print(top_ram)
    print(usuario_contenido_ram)
    

def establecer_gpu():
    
    global parte_label
    usuario_contenido_gpu=[]

    #Sacar contenido usuario gpu
    #contenido_usuario
    if(perfilPrimario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilPrimario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_gpu_"+ perfilPrimario.lower()
            perfil_contenido = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido)

    if(perfilSecundario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilSecundario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_gpu_"+ perfilSecundario.lower()
            perfil_contenido2 = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido2)
    
    if(perfilPrimario in perfiles and not(perfilSecundario in perfiles)):
        for i in range(len(perfil_contenido)):
            usuario_contenido_gpu.append(perfil_contenido[i])  #+0.5 es para dar mas importacia el perfil 1
        agregar_reglas_presupuesto(usuario_contenido_gpu) #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario MB")
        print(usuario_contenido_gpu)
    elif(perfilSecundario in perfiles and not(perfilPrimario in perfiles)):
        for i in range(len(perfil_contenido2)):
            usuario_contenido_gpu.append(perfil_contenido2[i])
        agregar_reglas_presupuesto(usuario_contenido_gpu)  #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario MB")
        print(usuario_contenido_gpu)
    else:
        for i in range(len(perfil_contenido)):
            if(float(perfil_contenido[i])<float(perfil_contenido2[i])):
               usuario_contenido_gpu.append((float(perfil_contenido[i])+float(perfil_contenido2[i]-(perfil_contenido[i]/2)))/2)  #para el mayor valor de p2 no suba tanto esa necesidad
            elif(float(perfil_contenido[i])>float(perfil_contenido2[i])):
                usuario_contenido_gpu.append((float(perfil_contenido[i])+float(perfil_contenido2[i]+(perfil_contenido[i]/2)))/2)  #para el menor valor de p2 no baje tanto esa necesidad
            else:
                usuario_contenido_gpu.append((float(perfil_contenido[i])+float(perfil_contenido2[i]))/2)


        agregar_reglas_presupuesto(usuario_contenido_gpu)  #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario MB")
        print(usuario_contenido_gpu)

    
    
    all_gpu = db.collection("GPU").get()
    lista_gpu=[]
    lista_contenidos_gpu=[]
    lista_gpu_con_puntajes=[]
    top_gpu=[0,0,0,0,0]  #tres espacios para que exista un top 3
    

    for gpu in all_gpu:
        #print(cpu.to_dict())
        gpu_dicc = gpu.to_dict()
        #separar reglas y contenido
        nombre_gpu = gpu_dicc["nombre"]
        contenido_gpu = gpu_dicc["contenido"]
        #print(reglas_comp_mb_cpu)

        #filtro1 - compatibilidad con CPU elegida  
        
        filtro1 = True
        if(altura_gabinete == "matx" and contenido_gpu[10]==1): #gabinete pequeño y posible MB es ATX
            filtro1 = False

        if(filtro1):
            lista_gpu.append(nombre_gpu)
            lista_contenidos_gpu.append(contenido_gpu)
        
    print(lista_gpu)
    print(lista_contenidos_gpu)    

    #----------------------FILTRADO BASADO EN CONTENIDO - Producto Punto estre vectores-------------------------------------------
    ranking_gpu=[]
    for i in range(len(lista_contenidos_gpu)):
        sumatoria=0
        for j in range(len(usuario_contenido_gpu)):
            sumatoria = sumatoria + (lista_contenidos_gpu[i][j] * usuario_contenido_gpu[j])
        ranking_gpu.append(sumatoria)


    #juntar nombre cpu con puntaje para poder hacer ranking
    for i in range(len(lista_gpu)):
        lista_gpu_con_puntajes.append(lista_gpu[i])
        lista_gpu_con_puntajes.append(ranking_gpu[i])

    #----------------------FILTRADO BASADO EN CONTENIDO - Hacer Ranking -----------------------------------------------------
    #hacer sort de rankings de MAYOR A MENOR
    ranking_gpu.sort(reverse=True) 

    for i in range(len(top_gpu)):
        for j in range(len(lista_gpu_con_puntajes)):
            if(lista_gpu_con_puntajes[j]==ranking_gpu[i] and (lista_gpu_con_puntajes[j-1] not in top_gpu)):
                top_gpu[i]=lista_gpu_con_puntajes[j-1]  #encontro puntaje top 3 y guarda en ese orden los nombres de top 3 

    parte_label.config(text="Lista de GPUs Recomendadas:")
   
    #----------------------FILTRADO BASADO EN CONTENIDO - Poner en tabla ordenada las recomendaciones -----------------------------------------------------
    #Poner info
    for row in my_tabla.get_children():
        my_tabla.delete(row)
    for i in range(len(top_gpu)):
        my_tabla.insert(parent='', index='end', iid=i, text="", values=("GPU",top_gpu[i], ranking_gpu[i]))

   
    print(top_gpu)
    print(ranking_gpu)


def establecer_mb():

    global parte_label
    global reglas_cpu_ig
    global reglas_cpu_fan

    reglas_cpu_for_mb=[]
    usuario_contenido_mb=[]

    all_info_cpu_elegida = db.collection("CPU").where("nombre","==",cpu_escogida).get()
    for i in all_info_cpu_elegida:
        info_cpu_elegida = i.to_dict()
        reglas_cpu_for_mb = info_cpu_elegida["reglas_mb"]
        reglas_cpu = info_cpu_elegida["reglas"]
        
    #Saber si hay Graficos integrados
    if(reglas_cpu[3]==1):
        reglas_cpu_ig=True
    #Saber si tiene Fan incluido
    if(reglas_cpu[2]==0):
        reglas_cpu_fan=False

    #Sacar contenido usuario mb
    #contenido_usuario
    if(perfilPrimario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilPrimario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_mb_"+ perfilPrimario.lower()
            perfil_contenido = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido)

    if(perfilSecundario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilSecundario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_mb_"+ perfilSecundario.lower()
            perfil_contenido2 = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido2)
    
    if(perfilPrimario in perfiles and not(perfilSecundario in perfiles)):
        for i in range(len(perfil_contenido)):
            usuario_contenido_mb.append(perfil_contenido[i])  #+0.5 es para dar mas importacia el perfil 1
        agregar_reglas_presupuesto(usuario_contenido_mb) #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario MB")
        print(usuario_contenido_mb)
    elif(perfilSecundario in perfiles and not(perfilPrimario in perfiles)):
        for i in range(len(perfil_contenido2)):
            usuario_contenido_mb.append(perfil_contenido2[i])
        agregar_reglas_presupuesto(usuario_contenido_mb)  #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario MB")
        print(usuario_contenido_mb)
    else:
        for i in range(len(perfil_contenido)):
            if(float(perfil_contenido[i])<float(perfil_contenido2[i])):
               usuario_contenido_mb.append((float(perfil_contenido[i])+float(perfil_contenido2[i]-(perfil_contenido[i]/2)))/2)  #para el mayor valor de p2 no suba tanto esa necesidad
            elif(float(perfil_contenido[i])>float(perfil_contenido2[i])):
                usuario_contenido_mb.append((float(perfil_contenido[i])+float(perfil_contenido2[i]+(perfil_contenido[i]/2)))/2)  #para el menor valor de p2 no baje tanto esa necesidad
            else:
                usuario_contenido_mb.append((float(perfil_contenido[i])+float(perfil_contenido2[i]))/2)


        agregar_reglas_presupuesto(usuario_contenido_mb)  #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario MB")
        print(usuario_contenido_mb)

    
    
    all_mb = db.collection("MB").get()
    lista_mb=[]
    lista_contenidos_mb=[]
    lista_mb_con_puntajes=[]
    top_mb=[]  #tres espacios para que exista un top 3
    

    for mb in all_mb:
        #print(cpu.to_dict())
        mb_dicc = mb.to_dict()
        #separar reglas y contenido
        reglas_comp_mb_cpu = mb_dicc["reglas_comp_cpu"]
        nombre_mb = mb_dicc["nombre"]
        contenido_mb = mb_dicc["contenido"]
        #print(reglas_comp_mb_cpu)

        filtro2 = True
        #filtro1 - compatibilidad con CPU elegida  
        for j in range(8):
            filtro1 = filtrar_productos(reglas_cpu_for_mb[j],reglas_comp_mb_cpu[j],2) 
            #filtro2 - comprobar tamaño MB
            if(altura_gabinete == "matx" and contenido_mb[21]==1): #gabinete pequeño y posible MB es ATX
                filtro2 = False

            if(filtro1):
                if(filtro2):
                    lista_mb.append(nombre_mb)
                    lista_contenidos_mb.append(contenido_mb)
        
    print(lista_mb)
    print(lista_contenidos_mb)    

    #----------------------FILTRADO BASADO EN CONTENIDO - Producto Punto estre vectores-------------------------------------------
    ranking_mb=[]
    for i in range(len(lista_contenidos_mb)):
        sumatoria=0
        for j in range(len(usuario_contenido_mb)):
            sumatoria = sumatoria + (lista_contenidos_mb[i][j] * usuario_contenido_mb[j])
        ranking_mb.append(sumatoria)


    #juntar nombre cpu con puntaje para poder hacer ranking
    for i in range(len(lista_mb)):
        lista_mb_con_puntajes.append(lista_mb[i])
        lista_mb_con_puntajes.append(ranking_mb[i])

    #----------------------FILTRADO BASADO EN CONTENIDO - Hacer Ranking -----------------------------------------------------
    #hacer sort de rankings de MAYOR A MENOR
    ranking_mb.sort(reverse=True) 

    for i in range(len(ranking_mb)): #la idea es que sea 3 (tamaño de top_mb)
        for j in range(len(lista_mb_con_puntajes)):
            if(lista_mb_con_puntajes[j]==ranking_mb[i] and (lista_mb_con_puntajes[j-1] not in top_mb)):
                top_mb.append(lista_mb_con_puntajes[j-1])   #encontro puntaje top 3 y guarda en ese orden los nombres de top 3 

    parte_label.config(text="Lista de Tarjetas Madre Recomendadas:")
    
    #----------------------FILTRADO BASADO EN CONTENIDO - Poner en tabla ordenada las recomendaciones -----------------------------------------------------
    #Poner info
    for row in my_tabla.get_children():
        my_tabla.delete(row)
    for i in range(len(top_mb)):
        my_tabla.insert(parent='', index='end', iid=i, text="", values=("TM",top_mb[i], ranking_mb[i]))

   
    print(top_mb)
    print(ranking_mb)
        

def establecer_cpu(p1,p2):

    global my_tabla
    global perfilPrimario
    global perfilSecundario

    #cpu 
    
    #por ahora las unicas reglas de usuario sera el presupuesto, las reglas solo se usaran para comprobar compatibilidad entre partes
    agregar_reglas_presupuesto(usuario_reglas) 
    print("Vector de reglas de Usuario: ")
    print(usuario_reglas)

    if(p1=='Gamer'):
        p1=diferenciar_Gamer(usuario_reglas)
    elif(p2=='Gamer'):
        p2=diferenciar_Gamer(usuario_reglas)
    
    perfilPrimario = p1
    perfilSecundario = p2

    #contenido_usuario
    if(perfilPrimario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilPrimario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_"+ perfilPrimario.lower()
            perfil_contenido = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido)

    if(perfilSecundario in perfiles):
        all_perfiles = db.collection("perfiles").where("nombre","==",perfilSecundario).get()
        for perfil in all_perfiles:
            perfil_dicc = perfil.to_dict()
            query_perfil_contendio="contenido_"+ perfilSecundario.lower()
            perfil_contenido2 = perfil_dicc [query_perfil_contendio]
            #print("Vector de contenido Usuario")
            #print(perfil_contenido2)
    
    if(perfilPrimario in perfiles and not(perfilSecundario in perfiles)):
        for i in range(len(perfil_contenido)):
            usuario_contenido.append(perfil_contenido[i])  #+0.5 es para dar mas importacia el perfil 1
        agregar_reglas_presupuesto(usuario_contenido) #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario CPU")
        print(usuario_contenido)
    elif(perfilSecundario in perfiles and not(perfilPrimario in perfiles)):
        for i in range(len(perfil_contenido2)):
            usuario_contenido.append(perfil_contenido2[i])
        agregar_reglas_presupuesto(usuario_contenido)  #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario CPU")
        print(usuario_contenido)
    else:
        for i in range(len(perfil_contenido)):
            if(float(perfil_contenido[i])<float(perfil_contenido2[i])):
                usuario_contenido.append((float(perfil_contenido[i])+float(perfil_contenido2[i]-(perfil_contenido[i]/2)))/2)  #para el mayor valor de p2 no suba tanto esa necesidad
            elif(float(perfil_contenido[i])>float(perfil_contenido2[i])):
                usuario_contenido.append((float(perfil_contenido[i])+float(perfil_contenido2[i]+(perfil_contenido[i]/2)))/2)  #para el menor valor de p2 no baje tanto esa necesidad
            else:
                usuario_contenido.append((float(perfil_contenido[i])+float(perfil_contenido2[i]))/2)


        agregar_reglas_presupuesto(usuario_contenido)  #agregar presupuesto a lista de contenido de usuario, para qu tambien de puntaje basado en su "gama"
        print("Vector de contenido Usuario CPU")
        print(usuario_contenido)


    #contenido_cpu (Metodo Filtrado)
    all_cpu = db.collection("CPU").get()
    lista_cpu=[]
    lista_contenidos_cpu=[]
    lista_cpu_con_puntajes=[]
    top_cpu=[0,0,0,0,0]  #tres espacios para que exista un top 3
    

    for cpu in all_cpu:
        #print(cpu.to_dict())
        cpu_dicc = cpu.to_dict()
        #separar reglas y contenido
        cpu_reglas = cpu_dicc["reglas"]
        cpu_nombre = cpu_dicc["nombre"]
        cpu_contenido = cpu_dicc["contenido"]

        lista_cpu.append(cpu_nombre)
        lista_contenidos_cpu.append(cpu_contenido)

        
    #----------------------FILTRADO BASADO EN CONTENIDO - Producto Punto estre vectores-------------------------------------------
    ranking_cpu=[]
    for i in range(len(lista_contenidos_cpu)):
        sumatoria=0
        for j in range(len(lista_contenidos_cpu[i])):
            sumatoria = sumatoria + (lista_contenidos_cpu[i][j] * usuario_contenido[j])
        ranking_cpu.append(sumatoria)


    #juntar nombre cpu con puntaje para poder hacer ranking
    for i in range(len(lista_cpu)):
        lista_cpu_con_puntajes.append(lista_cpu[i])
        lista_cpu_con_puntajes.append(ranking_cpu[i])

    #----------------------FILTRADO BASADO EN CONTENIDO - Hacer Ranking -----------------------------------------------------
    #hacer sort de rankings de MAYOR A MENOR
    ranking_cpu.sort(reverse=True) 

    for i in range(len(top_cpu)):
        for j in range(len(lista_cpu_con_puntajes)):
            if(lista_cpu_con_puntajes[j]==ranking_cpu[i] and (lista_cpu_con_puntajes[j-1] not in top_cpu)):
                top_cpu[i]=lista_cpu_con_puntajes[j-1]   #encontro puntaje top 3 y guarda en ese orden los nombres de top 3 

    parte_label.config(text="Lista de CPUs:")
    
    #----------------------FILTRADO BASADO EN CONTENIDO - Poner en tabla ordenada las recomendaciones -----------------------------------------------------
    #Poner info
    for row in my_tabla.get_children():
        my_tabla.delete(row)
    for i in range(len(top_cpu)):
        my_tabla.insert(parent='', index='end', iid=i, text="", values=("CPU",top_cpu[i], ranking_cpu[i]))

    my_tabla.place(x=500,y=100)
    buttonsele.config(state=ACTIVE) 


   
    print(top_cpu)
    print(ranking_cpu)

 
def introducir_presupuesto():
    global presupuesto 
    presupuesto = int(presu_entry.get())
    if(presupuesto<2500000):
        presu_label.config(text="Presupuesto muy bajo, se recomienda que sea mayor a 2.5 Milliones")
    else:
        button.config(state=DISABLED)
        button2.config(state=ACTIVE)
        presu_label.config(text="Presupuesto valido")
        presu_entry.config(state=DISABLED)
        
def establecer_gabinete():
    global altura_gabinete

    if(altura_escogida.get()=="Vacio"):
        altura_label.config(text="3. Escoga un rango de altura porfavor")
    else:
        if(altura_escogida.get()=="35 - 42 cm"):
            altura_gabinete="matx"
            print(altura_gabinete)
        elif(altura_escogida.get()=="43 - 53 cm"):
            altura_gabinete="atx"
            print(altura_gabinete)

        button3.config(state=DISABLED)
        establecer_cpu(perfil1.get(),perfil2.get())
        


def introducir_perfiles():
    if(perfil1.get()=="Vacio" and perfil2.get()=="Vacio"):
        perfil_label.config(text="2. Introduzca al menos un perfil")
    else:
        button2.config(state=DISABLED)
        button3.config(state=ACTIVE)

        
parte_label=Label(root, text="")
parte_label.place(x=500,y=50)

#crear_tabla("Lista CPU",top_cpu,ranking_cpu,"cpu")
buttonsele = Button(root, text="Escoger Parte", command=seleccionar_parte, state=DISABLED)
buttonsele.place(x=500,y=350)
    
button = Button(root,text="Introducir", command=introducir_presupuesto)
button.place(x=350,y=100)

button2 = Button(root,text="Escoger", command=introducir_perfiles, state=DISABLED)
button2.place(x=350,y=250)

button3 = Button(root,text="Continuar", command=establecer_gabinete, state=DISABLED)
button3.place(x=250,y=370)

root.mainloop()




