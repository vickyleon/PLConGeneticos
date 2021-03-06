#!/usr/bin/python

import sys
import time
import Tkinter as tk
import tktable as tkt
from numpy import *
import math
import random


perdidoMinimizar=[]
#variables globales, 
"""
Las variables sa_ guardan  el valor por el que se multiplica a cada variable del problema, por
ejemplo, si el problema esta sujeto a:

3X+2y<=5
2x-y<=20

En sa_x se guarda [3,2]; en sa_y se guarda[2,1]

En signo se guarara [<=,<=]

En igual se guardara [5,20]


TODOS ESTOS DATOS SON CADENAS, PARA PASARLOS A ENTERO HACER
int(sa_x[i])
"""
sa_x=[]
sa_y=[]
sa_v=[]
sa_w=[]
igual=[]
signo=["" for x in range(9)]

"""
En la lista "z" se guardan los coeficientes de la funcion objetivo, por ejemplo:
Minimizar 3X+2Y-9W+2V

Se guarda en z=[3,2,-9,2]
TODOS ESTOS DATOS SON CADENAS

"""
z=[]

"""
En la tabla a mostrar al usuario se deben ver los siguientes datos
	-valor respuesta de X
	-valor respuesta de Y
	-valor respuesta de W
	-valor respuesta de V
	-Funcion objetivo evaluada en los valores anteriores

Estos datos coinciden las variables de abajo. 
z_entabla tiene un valor extra ya que es la sumatoria de todos los elementos que la componen

SI z_entabla=[3,2,1,0] su ultimo elemento es 3+2+1+0=6
z_entabla[3,2,1,0,6]


TODOS ESTOS DATOS SON CADENAS

"""
x_entabla=[0,0,0,0]
y_entabla=[0,0,0,0]
w_entabla=[0,0,0,0]
v_entabla=[0,0,0,0]
z_entabla=[0,0,0,0,0]

"""
La variable porcentaje_z esta dada por:
	z_entabla[i]/z_entabla[4], 
Es la probabilidad de que suceda Z (asi viene en sus diapostivas :s)

La variable aleatorios_tabla sirve para almacenar cuatro numeros aleatorios entre 0 y 1

TODOS ESTOS DATOS SON CADENAS
"""
porcentaje_z=[0,0,0,0]
aleatorios_tabla=[0,0,0,0]

"""
z_acumulado es la sumatoria en zigzag, esta dada por:
	z_acumulado[i]=z_acumulado[i-1]+porcentaje_z[i]	
TODOS ESTOS DATOS SON CADENAS

"""
z_acumulado=[0,0,0,0]

"""
Veredicto es una lista DE CADENAS (strings) que guarda el numero de vectores que sobreviven
Por ejemplo, si solo sobreviven los vectores 2 y 3, debera ser algo similar a:

[2,2,3,2] 

Con que una sola vez se encuentre el identificador, quiere decir que el vector sobrevive, por ejemplo

[1,3,2,2] 

Sobreviven 1,3,2 para la sigiente iteracion


Si para este vector, no se cumplio ningun cirterio, se pone "Hijo/Mutacion", por ejemplo

[0,Hijo/MUtacion,2,0]

En este caso sobreviven solo los vectores 0 y 2, siendo asi, se debera generar dos nuevos
vectores, uno para el '0' repetido y otro para el 'Hijo/Mutacion; estos se generaran a partir
de 0 y 2

SON CADENAS
"""

veredicto=[0,0,0,0]

"""
Para el calculo de "mjs" es necesario saber los valores minimos y maximos que podra
tener cada variable, por ejemplo:

3<=X<=9
0<=Y<=10

En este caso en maximos se guarda -----> [9,10]
y en minimos ---------> [0,3]

SON CADENAS
"""
maximos=[]
minimos=[]

"""
Se guarda el numero de bits de precicion y las iteraciones que se van a hacer
ES UNA CADENA
"""
Bits_Precision=[]

"""
Es el numero de veces que va a iterar 
"""
Itera=[]

"""
Aqui es en donde se especifica en NUMERO DE BITS que debe tener la poblacion,

si X requiere 3 bits
Y requiere 9 bits
W necesita 8 bits
V necesota 10 bits

EL valor mjs es:

[3,9,8,10]

ES IMPORTANTE NO MODIFICARLA NUNCA, SON CADENAS, PARA USARLAS COMO ENTEROS, USAR

int(mjs[i])
"""
mjs=[]

"""
Aqui es en donde se guardan las poblaciones de bits. CON CADA ITERACION SE DEBEN
MODIFICAR LOS VALORES, ejemplo:

ITERACION 1 (notese que siempre tienen el mismo tamano, ya que todos cumplen
con el numero de bits especificado por iteracion en mjs)

[0101,0010,0000,1111]

Se obtiene que sobreviven los vectores 0 y 2, por lo que los vectores 1 y 3 se modifican

[0101, 1000, 0000, 1110]

Para editarlos, basta con usar poblacion[i]=UNA CADENA
"""
poblacion=[]

"""
Aqui guardol el resultado a final de las iteraciones
"""

resultado=[]
###################################### NO MOVERLE ########################################
raiz=tk.Tk()
raiz.title("Algoritmos geneticos")
###########################################################################################


"""
	Esta funcion editarla al final, lo unico que tiene que hacer es
	cambiar Z=-Z (el arreglo) y mandar a llamar a Maximizar

	El resultado imprimirlo como -MAXIMIZAR
"""
def Minimizar():
	for i in range(len(z)):
		if(z[i].get()!=''):
			zcadena=str(-1*int(z[i].get()))
			z[i].set(zcadena)
			
	perdidoMinimizar.append(1)
	#ImprimeArreglos()
	Maximizar()



"""
	Solo sirve para ver que lo que estas haciendo va bien
	unicamente imprime los arreglos
"""
def ImprimeArreglos():
	print "EN X: "
	for i in range(len(sa_x)):
		print sa_x[i].get(),
	print ""
	print "EN Y: "
	for i in range(len(sa_y)):
		print sa_y[i].get(),
	print ""
	print "EN V: "
	for i in range(len(sa_v)):
		print sa_v[i].get(),
	print ""
	print "EN W: "
	for i in range(len(sa_w)):
		print sa_w[i].get(),
	print ""
	print "EN SIGNOS: "
	print signo
	print "EN INDEPENDIENTE: "
	for i in range(len(igual)):
		print igual[i].get(),
	print ""
	print "Funcion objetivo"
	for i in range(len(z)):
		print z[i].get(),
	print ""

	print "En minimos"
	for i in range(len(minimos)):
		print minimos[i]
	print ""
	print "En maximos"
	for i in range(len(maximos)):
		print maximos[i]
	print ""
	print "En MJS"
	for i in range(len(mjs)):
		print mjs[i]
	print ""
	print "En Poblacion"
	for i in range(len(poblacion)):
		print poblacion[i]
	print ""
	print "En Tabla x"
	for i in range(len(x_entabla)):
		print x_entabla[i]
	print ""
	print "En Tabla y"
	for i in range(len(y_entabla)):
		print y_entabla[i]
	print ""
	print "En Tabla w"
	for i in range(len(w_entabla)):
		print w_entabla[i]
	print ""
	print "En Tabla v"
	for i in range(len(v_entabla)):
		print v_entabla[i]
	print ""
	print "En Tabla z"
	for i in range(len(z_entabla)):
		print z_entabla[i]
	print ""
	print "Porcentaje en z"
	for i in range(len(porcentaje_z)):
		print porcentaje_z[i]
	print ""
	print "Z acumulativo"
	for i in range(len(z_acumulado)):
		print z_acumulado[i]
	print ""
	print "Aleatorios"
	for i in range(len(aleatorios_tabla)):
		print aleatorios_tabla[i]
	print ""
	print "Nueva poblacion"
	for i in range(len(veredicto)):
		print veredicto[i]
	print ""
	print "Numero de iteraciones"
	for i in range(len(Itera)):
		print Itera[i].get()
	print ""
	print "Numero de bits de precision"
	for i in range(len(Bits_Precision)):
		print Bits_Precision[i].get()
	print ""
	

def Maximizar():
	perdidoMinimizar.append(0)
	############INICIO ALGORITMO################
	#Obtengo los maximos y minimos de cada variable asi como sus mjs
	for i in range(len(z)): #para cada variable en la funcion objetivo
		if z[i].get()!="": # No tomes en cuenta las variables que estan vacias en la funcion objetivo
			minimos.append(Minimo(i)) #obten el minimo de la variable
			maximos.append(Maximo(i)) #obten el maximo de la variable 
			mjs.append(Calcula_mj(minimos[i],maximos[i])) #obtener cuantos bits debe tener la poblacion por culpa de esa variable
	ImprimeArreglos()
	#modificacion Vicky
	# recupera el numero de iteraciones y lo guarda en otra variable 
	for i in range(len(Itera)):
		iteraciones=int(Itera[i].get())
	
	print iteraciones

	for i in range(4): #Creo 4 vectores de poblacion
		"""
		En las siguientes iteraciones, en lugar de crear nuevos vectores y usar append
		se va a hacer

		poblacion[i]=Cruza(Num_de_vector1,Num_de_vector2)

		O en su defecto

		poblacion[i]=Mutacion(Num_de_vector1)
		"""
		poblacion.append(NuevoVector()) ##Creo un nuevo vector que tenga el tamano de todas las mjs
		SeleccionNatural(i) ##Antes de aceptarlo, veo que cumpla con las condiciones (s.a.)

	############################ AQUI INICIARIA LA ITERACION N ################################################
	while True:
		"""
		Ahora que ya tengo vectores que cumplen con las condicions (s.a), empiezo a llenar la tabla
		(ver tus apuntes)

		En este caso empiezo con las variables X,Y,W,V pero con su valor real, el cual se obtiene de_

		min+decimal(CADENA BINARA)*(maximo-minimo)(2**mjs-1)

		"""
		for i in range(4): #Para cada vector
			Variable_enTabla(i) #Obtengo los valores X,Y.W.V que genera dicho vector
			Evalua_Z_enTabla(i) #Evaluo los valores anteriores en la funcion objetivo y tengo Z

		Sumatoria_Z() #Hago la sumatoria en z
		Porcientos() #Saco los porcentajes
		AcumulativoZ() #Hago el zig zag de la tabla 
		Aleatorios() #Genero cuatro numeros aleatorios de 0 a 1
		for i in range(4): #Para cada vector de la poblacion
			SegundaSeleccion(i) #Checo cuales vectores sobreviven para mutaciones y cruzas y cuales no
		
		ImprimeArreglos()
		#time.sleep(10)
		print "*************************************************"
		
		if int(Itera[0].get())>10:
			n=10
		else:
			n=2

		if iteraciones>n:
			for i in range(4):
				if(Sobrevive(i)==0):
					numeroVeredicto1=int(random.uniform(0, 4))
					numeroVeredicto2=int(random.uniform(0, 4))
					if(veredicto[numeroVeredicto1]==veredicto[numeroVeredicto2]):
						numeroVeredicto2=int(random.uniform(0, 4))	
					poblacion[i]=Cruzar(veredicto[numeroVeredicto1],veredicto[numeroVeredicto2])
					SeleccionNatural_ConCruza(i,veredicto[numeroVeredicto1],veredicto[numeroVeredicto2])

		else:
			for i in range(4):
				if(Sobrevive(i)==0):
					poblacion[i]=Mutar(i)
					poblacion[i]=SeleccionNatural_ConMutacion(i)
		

		"""
		Faltaria por agregar las mutaciones y las cruzas
		"""

		iteraciones=iteraciones-1
		print iteraciones
		
		if iteraciones==0 :
			obtieneResultado()
			break;
		#time.sleep(10)
	####################################################AQUI TERMINARIA LA ITERACION ################################3

	




	"""
	Esto es lo que dibuja la tabla (hasta antes de "def SegundaSeleccion")
	"""
	#OBTENER VALOR DE Z PARA LA TABLA

	#Configuraciones basicas
	otra_ventana=tk.Toplevel()
	vent=tk.Frame(otra_ventana)
	raiz.withdraw()
	vent.grid(column=0, row=0,padx=(50,50), pady=(10,10))
	vent.columnconfigure(0,weight=1)
	vent.rowconfigure(0,weight=1)

	stringObjetivo="Z="
	cont=0
	conta=0
	for l in range(len(z)):
		if(z[l].get()!=""):
			conta+=1

	for l in range(len(z)):
		if(z[l].get()!=""):
			if(cont==0):
				stringObjetivo+=z[l].get()+"X"
			if(cont==1):
				stringObjetivo+=z[l].get()+"Y"
			if(cont==2):
				stringObjetivo+=z[l].get()+"W"
			if(cont==3):
				stringObjetivo+=z[l].get()+"V"
			if(cont<conta-1):
				stringObjetivo+="+"
			cont+=1



	Label_FuncionObjetivo=tk.Label(vent,text=stringObjetivo)
	Label_FuncionObjetivo.grid(column=3, row=0)

	Label_FuncionTexto=tk.Label(vent,text="Funcion Objetivo: Z="+str(resultado[0]))
	Label_FuncionTexto.grid(column=0, row=0,columnspan=3)

	Label_XRes=tk.Label(vent,text="X="+str(resultado[1]))
	Label_XRes.grid(column=1, row=1)
	Label_YRes=tk.Label(vent,text="Y="+str (resultado[2]))
	Label_YRes.grid(column=2, row=1)
	Label_WRes=tk.Label(vent,text="W="+str (resultado[3]))
	Label_WRes.grid(column=3, row=1)
	Label_VRes=tk.Label(vent,text="V="+str (resultado[4]))
	Label_VRes.grid(column=4, row=1)


	Boton_salir=tk.Button(vent,text="Salir", command=fin)
	Boton_salir.grid(column=3,row=15)
	
	Tabla=tkt.Table(vent,rows=5,cols=5)
	
	for i in range(5):
         for j in range(10):
         	if (i==0):
         		if(j==0):
         			l=tk.Label(vent,text="X")
         		elif(j==1):
         			l=tk.Label(vent,text="Y")
         		elif(j==2):
         			l=tk.Label(vent,text="W")
         		elif(j==3):
         			l=tk.Label(vent,text="V")
         		elif(j==4):
         			l=tk.Label(vent,text="Z")
         		elif(j==5):
         			l=tk.Label(vent,text="% z")
         		elif(j==6):
         			l=tk.Label(vent,text="% z acumulado")
         		elif(j==7):
         			l=tk.Label(vent,text="Aleatorios")
         		elif(j==8):
         			l=tk.Label(vent,text="Nuevo V")
         		

         	elif(j==0):
         		if perdidoMinimizar[0]==1:
         			l=tk.Label(vent,text=str(float(x_entabla[i-1])/(10)))
         		else:
        			l = tk.Label(vent,text=str(x_entabla[i-1]))

        	elif(j==1):
        		if perdidoMinimizar[0]==1:
        			l=tk.Label(vent,text=str(float(y_entabla[i-1])/(10)))
        		else:
        			l = tk.Label(vent,text=str(y_entabla[i-1]))
        	elif(j==2):
        		if perdidoMinimizar[0]==1:
        			l=tk.Label(vent,text=str(float(w_entabla[i-1])/(10)))
        		else:
        			l = tk.Label(vent,text=str(w_entabla[i-1]))
        	elif(j==3):
        		if perdidoMinimizar[0]==1:
        			l=tk.Label(vent,text=str(float(v_entabla[i-1])/(10)))
        		else:
        			l = tk.Label(vent,text=str(v_entabla[i-1]))
        	elif(j==4):
        		if perdidoMinimizar[0]==1:
        			l=tk.Label(vent,text=str(float(z_entabla[i-1])/(10)))
        		else:
        			l = tk.Label(vent,text=str(z_entabla[i-1]))
        	elif(j==5):
        		l=tk.Label(vent,text=str(porcentaje_z[i-1]))
        	elif(j==6):
        		l = tk.Label(vent,text=str(z_acumulado[i-1]))
        	elif(j==7):
        		l = tk.Label(vent,text=str(aleatorios_tabla[i-1]))
        	elif(j==8):
        		l=tk.Label(vent,text=str(veredicto[i-1]))
        	

        	l.grid(row=i+5, column=j)



	#Tabla.grid(column=1, row=2,columnspan=6)
	otra_ventana.mainloop()
	#vs=tk.Frame(otra_ventana)
"""
Esta funcion verifica que es lo que sucedera en la siguiente iteracion con el vector
en la posicion idVector, Pueden suceder tres cosas

	1.- Se queda el valor del vector actual
	2.- Se cambia por una mutacion o un  hijo

Para esto lo que hace es lo siguiente
	1.-Ordena los porcentajes de Z de menor a mayor
	2.- Checa si el aleatorio que se genero para el vector entra dentro del rango
		de posibles valores
			1.- Si es asi, checa en que rango entra, por lo tanto elije
				el %z mayor inmediato y pone su identificador en la lista
				veredicto. Es decir que si el mayor inmediato del vector actual es el
				2, entonces veredicto[idVector]=2
			2.- Si no hay un mayor inmediato, entonces senala que se debe hacer
				una mutacion o un hijo

"""
def obtieneResultado():
	mayor=-99999
	id=0
	for i in range(len(z_entabla)-1):
		if(float(z_entabla[i])>mayor):
			id=i
			mayor=float(z_entabla[i])

	if perdidoMinimizar[0]==1:
		mayor*=-1
		mayor/=10
		resultado.append(mayor)
		x=float(x_entabla[id]/10)		
		resultado.append(x)
		y=float(y_entabla[id]/10)	
		resultado.append(y)
		w=float(w_entabla[id]/10)	
		resultado.append(w)
		v=float(v_entabla[id]/10)	
		resultado.append(v)
	else:
		resultado.append(mayor)			
		resultado.append(x_entabla[id])
		resultado.append(y_entabla[id])
		resultado.append(w_entabla[id])
		resultado.append(v_entabla[id])

def SegundaSeleccion(idVector):
	acumulador=0
	ordenados=z_acumulado
	ordenados.sort()
	print ordenados[3],
	print "<",
	print aleatorios_tabla[idVector]
	if ordenados[3]<aleatorios_tabla[idVector]:
		veredicto[idVector]="Hijo/Mutacion"
	else:
		#Buscar dentro de que rango esta el aleatorio y guardar el valor del rango
		"""
			Si el mayor inmediato es 0.9 entonces guarda en acumulador 0.9
		"""
		if aleatorios_tabla[idVector]<ordenados[3]:
			acumulador=ordenados[3]
		if aleatorios_tabla[idVector]<ordenados[2]:
			acumulador=ordenados[2]
		if aleatorios_tabla[idVector]<ordenados[1]:
			acumulador=ordenados[1]
		if aleatorios_tabla[idVector]<ordenados[0]:
			acumulador=ordenados[0]
		#ahora que se dentro de que rango esta, busco a que vector corresponde
		#el valor de acumulador
		for i in range(len(z_acumulado)):
			if z_acumulado[i]==acumulador:
				veredicto[idVector]=i


				
		
"""
	Genero 4 numeros aleatorios del 0 al 1
"""


def Aleatorios():
	for i in range(4):
		aleatorios_tabla[i]=random.uniform(0, 1)

"""
	Hace la operacion en sigsag (ver apuntes del cuaderno para calcular %Za cuum)
"""

def AcumulativoZ():
	z_acumulado[0]=porcentaje_z[0]
	for i in range(1,4):
		z_acumulado[i]=z_acumulado[i-1]+porcentaje_z[i]

"""
	Realiza la division del valor de z en el vector entre la sumatoria de valores
	en z

"""

def Porcientos():
	for i in range(4):
		porcentaje_z[i]=float(z_entabla[i])/float(z_entabla[4])


"""
	Suma todos los valores de z y lo guarda en la posicion 4
"""
def Sumatoria_Z():
	acumulador=0
	for i in range(len(z_entabla)-1):
		acumulador+=float(z_entabla[i])
	z_entabla[4]=acumulador

"""
	Usando los coficientes de la funcion objetivo, evalua los valores del vector 
	para obtener el resultado de z
"""	

def Evalua_Z_enTabla(idVector):
	acumulador=0 #el valor de z
	if z[0].get()!="": #verifico si la variable x esta en la funcion objetivo
		#print x_entabla[idVector]
		acumulador+=int(z[0].get())*float(x_entabla[idVector]) #coeficiente*valor en x
	#LO MISMO EN LOS DEMAS CASOS
	if z[1].get()!="":
		#print z[1].get()
		acumulador+=int(z[1].get())*float(y_entabla[idVector])
	if z[2].get()!="":
		#print z[2].get()
		acumulador+=int(z[2].get())*float(w_entabla[idVector])
	if z[3].get()!="":
		#print z[3].get()
		acumulador+=int(z[3].get())*float(v_entabla[idVector])
	z_entabla[idVector]=acumulador

"""
	Esta funcion hace la operacion descrita en tus apuntes como:

	min+decimal(CADENA BINARIA)(algo/algo)

	Segun el vector que se le de, dara los valores reales para
	X Y W V
"""
def Variable_enTabla(idVector):
	##################### DEL VECTOR OBTIENE LAS PARTES X Y W V ##################
	"""
	Si el vector [00110011], esta parte devuelve x=00 y==11 w=00 v=11
	Con base en el tamano que se le otorgo en mjs 
	"""
	strings=[]
	acumulador=0
	for i in range(len(z)):
		if z[i].get()!="":
			#obtener x,y,w,v del vector
			strings.append(poblacion[idVector][acumulador:acumulador+int(mjs[i])])
			acumulador+=int(mjs[i])
	##############################################################################
	# verifico que exista la variable, ya sea x,y,v o w, si existe hago el calculo
	if len(minimos)>0 and len(strings)>0 and len(maximos)>0 and len(mjs)>0:
		x_entabla[idVector]=float(minimos[0])+int(strings[0],2)*((float(maximos[0])-float(minimos[0])))/(2**int(mjs[0])-1)
	if len(minimos)>1 and len(strings)>1 and len(maximos)>1 and len(mjs)>1:
		y_entabla[idVector]=float(minimos[1])+int(strings[1],2)*((float(maximos[1])-float(minimos[1])))/(2**int(mjs[1])-1)
	if len(minimos)>2 and len(strings)>2 and len(maximos)>2 and len(mjs)>2:
		w_entabla[idVector]=float(minimos[2])+int(strings[2],2)*((float(maximos[2])-float(minimos[2])))/(2**int(mjs[2])-1)
	if len(minimos)>3 and len(strings)>3 and len(maximos)>3 and len(mjs)>3:
		v_entabla[idVector]=float(minimos[3])+int(strings[3],2)*((float(maximos[3])-float(minimos[3])))/(2**int(mjs[3])-1)

"""
	Esa funcion evalua un vector para saber si es apto o no,
	si es apto, lo deja en su posicion, si no, manda a llamar a la funcion
	que crea vectores para pedirle uno nuevo
"""

def SeleccionNatural(idVector):
	vivio=0 # numero de condiciones que ha cumplido el vector con id idVector
	while not vivio==len(igual): #mientras que el vector no cumpla todas las condiciones
		vivio=0
		##################### DEL VECTOR OBTIENE LAS PARTES X Y W V ##################
		"""
		Si el vector [00110011], esta parte devuelve x=00 y==11 w=00 v=11
		Con base en el tamano que se le otorgo en mjs 
		"""
		strings=[]
		acumulador=0
		#print poblacion[idVector]
		for i in range(len(z)):
			if z[i].get()!="":
				#obtener x,y,w,v del vector
				strings.append(poblacion[idVector][acumulador:acumulador+int(mjs[i])])
				acumulador+=int(mjs[i])
		################################################################################

		sobrevive=0 #para saber si sobrevive a la i-esima condicion
		valor=0 #lo que vale la ecuacion s.a. 
		for i in range(len(igual)): #por cada condicion
			#evaluo el polinomio
			if len(strings)>0: #si hay cromosomas dentro del vector que pertenecen a x
				# si la variable x si existe
				if sa_x[i].get()!="" and strings[0]!="" and minimos[0]!="" and mjs[0]!="":
					#print  int(sa_x[i].get()),
					#print "*",
					#print  int(strings[0],2)
					#evalua (pero con el valor de min+decimal(CADENA BINARIA)*(algo/algo))
					valor_procedimiento=float(minimos[0])+int(strings[0],2)*((float(maximos[0])-float(minimos[0])))/(2**int(mjs[0])-1)
					#coeficiente*variable ya evaluada
					valor+=int(sa_x[i].get())*valor_procedimiento #se suma al resultado del polinomio
			########## REPETIR CON LOS DEMAS
			if len(strings)>1:
				#print "entre a 1"
				if sa_y[i].get()!="" and strings[1]!="" and minimos[1]!="" and mjs[1]!="":
					#print  int(sa_y[i].get()),
					#print "*",
					#print  int(strings[1],2)
					valor_procedimiento=float(minimos[1])+int(strings[1],2)*((float(maximos[1])-float(minimos[1])))/(2**int(mjs[1])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_y[i].get())*valor_procedimiento
			if len(strings)>2:
				#print "entre a 2"
				if sa_w[i].get()!="" and strings[2]!="" and minimos[2]!="" and mjs[2]!="":
					#print  int(sa_w[i].get()),
					#print "*",
					#print  int(strings[2],2)
					valor_procedimiento=float(minimos[2])+int(strings[2],2)*((float(maximos[2])-float(minimos[2])))/(2**int(mjs[2])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_w[i].get())*valor_procedimiento
			if len(strings)>3:
				#print "entre a 3"
				if sa_v[i].get()!="" and strings[3]!="" and minimos[3]!="" and mjs[3]!="":
					#print  int(sa_v[i].get()),
					#print "*",
					#print  int(strings[3],2)
					valor_procedimiento=float(minimos[3])+int(strings[3],2)*((float(maximos[3])-float(minimos[3])))/(2**int(mjs[3])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_v[i].get())*valor_procedimiento
			#print "VALOR:",
			#print valor
		
			#checo el signo 
			if signo[i]=="<=":
				#print signo[i],
				#print igual[i].get()
				if valor <= int(igual[i].get()):
					sobrevive=1 ##cumple con la condicion
			elif signo[i]==">=":
				#print signo[i],
				#print igual[i].get()
				if valor>=int(igual[i].get()):
					sobrevive=1 #cumple con la conficion
			else:
				#print signo[i],
				#print igual[i].get()
				if valor==int(igual[i].get()):
					sobrevive=1 #cumple con la conficion
			if sobrevive==1:
				#print "sobrevive"
				sobrevive=0 #reinicio para que evalue la siguiente condicion
				vivio+=1 #ya sobrevivio a una de las n condiciones
			else:
				break
				#print "muere!"

		if vivio==len(igual): #si sobrevivio a todas las condiciones, entonces es apto
			return poblacion[idVector]
		else: # matalo y crea otro vector, esto sige dentro del while, asi que repite el proceso
			poblacion[idVector]=NuevoVector()
"""
	Crea un nuevo vector con numeros aleatorios y lo guarda en poblacion
"""	

def NuevoVector():
	aux=0
	vector=[]
	for i in range(len(z)): #por cada variable que exista en la funcion objetivo
		if z[i].get()!="":
			#print "mjs: ",
			#print mjs[i]
		 	aux=random.randrange((2**int(mjs[i]))) ##crea un numero aleatorio que quepa en mjs digitos
			#print "Aux",
			#print bin(aux)[2:]
			if len(bin(aux)[2:])!=int(mjs[i]): #si el numero en binario tiene menos bits de los necesarios, llena la cadena con ceros
				#print "entre"
				ceros=int(mjs[i])-len(bin(aux)[2:])
				for l in range(ceros):
					vector.append("0")
			vector.append(bin(aux)[2:])
	string_vector=''.join(vector) # junta los ceros con el valor
	"""
		Por ejemplo si mjs=[2,3,4,9]
		x genera el numero 1 que en binario es 1 y requiere un cero -->01
		y genera el numero 4 que en binario 100, no requiere ceros --->100
		w genera el numero 3 que en binario es 11, requiere dos ceros-->0011
		w genera el 7 que en binario es 111, requiere seis ceros--->000000111

		Al hacer join la cadena es 01100001100000011 y se regresa como resultado
	"""
	return string_vector
#Nos dice si sobrevive el vector
def Sobrevive(idVector):
	sobrevive=0
	#Muere=0
	#Vive =1 
	for i in range(len(poblacion)):
		if(veredicto[i]==idVector):
			sobrevive=1
	return sobrevive

verectorQueSeVa=[0,0,0,0]

def QuienSeVa():
	for i in range(len(poblacion)):
		verectorQueSeVa[veredicto[i]]=1
		print verectorQueSeVa[i]
	for i in range(4):	
		if verectorQueSeVa[i]==0:
			MejoradoVector=i
			Mutar(i)

#
def Mutar(idVectorMutable):

    ####### AQUI TU CODIGO ######
    #poblacion[idVectorMutable]
    # VectorMutado debe ser algo como: 1000100100101 ya al final
    # pasamos la poblacion que muere a entero 
   print "vamo a mutar"
   tamano=len(poblacion[idVectorMutable])
   
   aleatorio=int(random.uniform(0, tamano))
   string2=[]
   str1=""
   if(int(poblacion[idVectorMutable][aleatorio])==0):
   	print "agarroo un 0"
	string=poblacion[idVectorMutable][:]
	
	for x in range(len(string)):
		if(x==aleatorio):
			string2.append('1')
		else:
			string2.append(string[x])
	str1=''.join(string2)
   else:
	print "agarro un 1"
	string=poblacion[idVectorMutable][:]
	
	for x in range(len(string)):
		if(x==aleatorio):
			string2.append('0')
		else:
			string2.append(string[x])
	str1=''.join(string2)
	
   print str1	
   return str1
def  Cruzar ( idVectorPadre , idVectorMadre ):
	tamano=0
	for i in range(len(mjs)):
		if mjs[i]!="":
			tamano+=mjs[i]

	tamano=int(tamano)
	linea=int(random.uniform(0, tamano))
	VectorCruzado=""
	VectorCruzado=poblacion[idVectorPadre][0:linea]+poblacion[idVectorMadre][linea:tamano]
	VectorCruza=''.join(VectorCruzado)

 	return VectorCruza

#Verfica si es valido el vector que mutamos anteriormente 
def SeleccionNatural_ConMutacion(idVector):
	print "entre a seleccion natural"
	vivio=0 # numero de condiciones que ha cumplido el vector con id idVector
	while not vivio==len(igual): #mientras que el vector no cumpla todas las condiciones
		vivio=0
		##################### DEL VECTOR OBTIENE LAS PARTES X Y W V ##################
		"""
		Si el vector [00110011], esta parte devuelve x=00 y==11 w=00 v=11
		Con base en el tamano que se le otorgo en mjs 
		"""
		strings=[]
		acumulador=0
		#print poblacion[idVector]
		for i in range(len(z)):
			if z[i].get()!="":
				#obtener x,y,w,v del vector
				strings.append(poblacion[idVector][acumulador:acumulador+int(mjs[i])])
				acumulador+=int(mjs[i])
		################################################################################

		sobrevive=0 #para saber si sobrevive a la i-esima condicion
		valor=0 #lo que vale la ecuacion s.a. 
		for i in range(len(igual)): #por cada condicion
			#evaluo el polinomio
			if len(strings)>0: #si hay cromosomas dentro del vector que pertenecen a x
				# si la variable x si existe
				if sa_x[i].get()!="" and strings[0]!="" and minimos[0]!="" and mjs[0]!="":
					#print  int(sa_x[i].get()),
					#print "*",
					#print  int(strings[0],2)
					#evalua (pero con el valor de min+decimal(CADENA BINARIA)*(algo/algo))
					valor_procedimiento=float(minimos[0])+int(strings[0],2)*((float(maximos[0])-float(minimos[0])))/(2**int(mjs[0])-1)
					#coeficiente*variable ya evaluada
					valor+=int(sa_x[i].get())*valor_procedimiento #se suma al resultado del polinomio
			########## REPETIR CON LOS DEMAS
			if len(strings)>1:
				#print "entre a 1"
				if sa_y[i].get()!="" and strings[1]!="" and minimos[1]!="" and mjs[1]!="":
					#print  int(sa_y[i].get()),
					#print "*",
					#print  int(strings[1],2)
					valor_procedimiento=float(minimos[1])+int(strings[1],2)*((float(maximos[1])-float(minimos[1])))/(2**int(mjs[1])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_y[i].get())*valor_procedimiento
			if len(strings)>2:
				#print "entre a 2"
				if sa_w[i].get()!="" and strings[2]!="" and minimos[2]!="" and mjs[2]!="":
					#print  int(sa_w[i].get()),
					#print "*",
					#print  int(strings[2],2)
					valor_procedimiento=float(minimos[2])+int(strings[2],2)*((float(maximos[2])-float(minimos[2])))/(2**int(mjs[2])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_w[i].get())*valor_procedimiento
			if len(strings)>3:
				#print "entre a 3"
				if sa_v[i].get()!="" and strings[3]!="" and minimos[3]!="" and mjs[3]!="":
					#print  int(sa_v[i].get()),
					#print "*",
					#print  int(strings[3],2)
					valor_procedimiento=float(minimos[3])+int(strings[3],2)*((float(maximos[3])-float(minimos[3])))/(2**int(mjs[3])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_v[i].get())*valor_procedimiento
			#print "VALOR:",
			#print valor
		
			#checo el signo 
			if signo[i]=="<=":
				#print signo[i],
				#print igual[i].get()
				if valor <= int(igual[i].get()):
					sobrevive=1 ##cumple con la condicion
			elif signo[i]==">=":
				#print signo[i],
				#print igual[i].get()
				if valor>=int(igual[i].get()):
					sobrevive=1 #cumple con la conficion
			else:
				#print signo[i],
				#print igual[i].get()
				if valor==int(igual[i].get()):
					sobrevive=1 #cumple con la conficion
			if sobrevive==1:
				#print "sobrevive"
				sobrevive=0 #reinicio para que evalue la siguiente condicion
				vivio+=1 #ya sobrevivio a una de las n condiciones
			else:
				break
				#print "muere!"

		if vivio==len(igual): #si sobrevivio a todas las condiciones, entonces es apto
			return poblacion[idVector]
		else: # matalo y crea otro vector, esto sige dentro del while, asi que repite el proceso
			poblacion[idVector]=Mutar(idVector)
"""
	Crea un nuevo vector con numeros aleatorios y lo guarda en poblacion
 """
def SeleccionNatural_ConCruza(idVector,idVectorPadre,idVectorMadre):
	vivio=0 # numero de condiciones que ha cumplido el vector con id idVector
	while not vivio==len(igual): #mientras que el vector no cumpla todas las condiciones
		vivio=0
		##################### DEL VECTOR OBTIENE LAS PARTES X Y W V ##################
		"""
		Si el vector [00110011], esta parte devuelve x=00 y==11 w=00 v=11
		Con base en el tamano que se le otorgo en mjs 
		"""
		strings=[]
		acumulador=0
		#print poblacion[idVector]
		for i in range(len(z)):
			if z[i].get()!="":
				#obtener x,y,w,v del vector
				strings.append(poblacion[idVector][acumulador:acumulador+int(mjs[i])])
				acumulador+=int(mjs[i])
		################################################################################

		sobrevive=0 #para saber si sobrevive a la i-esima condicion
		valor=0 #lo que vale la ecuacion s.a. 
		for i in range(len(igual)): #por cada condicion
			#evaluo el polinomio
			if len(strings)>0: #si hay cromosomas dentro del vector que pertenecen a x
				# si la variable x si existe
				if sa_x[i].get()!="" and strings[0]!="" and minimos[0]!="" and mjs[0]!="":
					#print  int(sa_x[i].get()),
					#print "*",
					#print  int(strings[0],2)
					#evalua (pero con el valor de min+decimal(CADENA BINARIA)*(algo/algo))
					valor_procedimiento=float(minimos[0])+int(strings[0],2)*((float(maximos[0])-float(minimos[0])))/(2**int(mjs[0])-1)
					#coeficiente*variable ya evaluada
					valor+=int(sa_x[i].get())*valor_procedimiento #se suma al resultado del polinomio
			########## REPETIR CON LOS DEMAS
			if len(strings)>1:
				#print "entre a 1"
				if sa_y[i].get()!="" and strings[1]!="" and minimos[1]!="" and mjs[1]!="":
					#print  int(sa_y[i].get()),
					#print "*",
					#print  int(strings[1],2)
					valor_procedimiento=float(minimos[1])+int(strings[1],2)*((float(maximos[1])-float(minimos[1])))/(2**int(mjs[1])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_y[i].get())*valor_procedimiento
			if len(strings)>2:
				#print "entre a 2"
				if sa_w[i].get()!="" and strings[2]!="" and minimos[2]!="" and mjs[2]!="":
					#print  int(sa_w[i].get()),
					#print "*",
					#print  int(strings[2],2)
					valor_procedimiento=float(minimos[2])+int(strings[2],2)*((float(maximos[2])-float(minimos[2])))/(2**int(mjs[2])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_w[i].get())*valor_procedimiento
			if len(strings)>3:
				#print "entre a 3"
				if sa_v[i].get()!="" and strings[3]!="" and minimos[3]!="" and mjs[3]!="":
					#print  int(sa_v[i].get()),
					#print "*",
					#print  int(strings[3],2)
					valor_procedimiento=float(minimos[3])+int(strings[3],2)*((float(maximos[3])-float(minimos[3])))/(2**int(mjs[3])-1)
					#print "valor procedimiento:",
					#print valor_procedimiento
					valor+=int(sa_v[i].get())*valor_procedimiento
			#print "VALOR:",
			#print valor
		
			#checo el signo 
			if signo[i]=="<=":
				#print signo[i],
				#print igual[i].get()
				if valor <= int(igual[i].get()):
					sobrevive=1 ##cumple con la condicion
			elif signo[i]==">=":
				#print signo[i],
				#print igual[i].get()
				if valor>=int(igual[i].get()):
					sobrevive=1 #cumple con la conficion
			else:
				#print signo[i],
				#print igual[i].get()
				if valor==int(igual[i].get()):
					sobrevive=1 #cumple con la conficion
			if sobrevive==1:
				#print "sobrevive"
				sobrevive=0 #reinicio para que evalue la siguiente condicion
				vivio+=1 #ya sobrevivio a una de las n condiciones
			else:
				break
				#print "muere!"

		if vivio==len(igual): #si sobrevivio a todas las condiciones, entonces es apto
			return poblacion[idVector]
		else: # matalo y crea otro vector, esto sige dentro del while, asi que repite el proceso
			 poblacion[idVector]=Cruzar(idVectorPadre,idVectorMadre)
"""
	Crea un nuevo vector con numeros aleatorios y lo guarda en poblacion
"""
################################################ NO MOVERLE DE AQUI PARA ABAJO ######################################

def Calcula_mj(minimo,maximo):
	aux=maximo-minimo
	aux*=10**int(Bits_Precision[0].get())
	auxb=aux
	aux=round(math.log(aux)/math.log(2))

	#verificamos que cumplan las condifciones#
	if 2**(aux-1)<=auxb and (2**aux)-1>=auxb:
		return aux
	else:
		aux+=1
	return aux


def Maximo(idVariable):
	maximo=-99999
	r=0
	if idVariable==0:
		for i in range(len(sa_x)):
			numero=float(sa_x[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r>=maximo:
				maximo=r
	elif idVariable==1:
		for i in range(len(sa_y)):
			numero=float(sa_y[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r>=maximo:
				maximo=r
	elif idVariable==2:
		for i in range(len(sa_w)):
			numero=float(sa_w[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r>=maximo:
				maximo=r
	elif idVariable==3:
		for i in range(len(sa_v)):
			numero=float(sa_v[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r>=maximo:
				maximo=r

	return maximo

def Minimo(idVariable):
	minimo=99999
	r=0
	if idVariable==0:
		for i in range(len(sa_x)):
			numero=float(sa_x[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r<=minimo:
				minimo=r
	elif idVariable==1:
		for i in range(len(sa_y)):
			numero=float(sa_y[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r<=minimo:
				minimo=r
	elif idVariable==2:
		for i in range(len(sa_w)):
			numero=float(sa_w[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r<=minimo:
				minimo=r
	elif idVariable==3:
		for i in range(len(sa_v)):
			numero=float(sa_v[i].get())
			solucion=float(igual[i].get())
			r=solucion/numero
			if r<=minimo:
				minimo=r
	return minimo

def fin():
	raiz.destroy()

def agrega_condicion():
	global tkvar
	global choices
	try:
		contador.set(contador.get()+1)
		numCondiciones=contador.get()

		if numCondiciones<14:
			Label_x=tk.Label(vp,text="X+")
			Label_x.grid(column=6, row=numCondiciones)

			Label_y=tk.Label(vp,text="Y+")
			Label_y.grid(column=8, row=numCondiciones)

			Label_w=tk.Label(vp,text="W+")
			Label_w.grid(column=10, row=numCondiciones)

			Label_v=tk.Label(vp,text="V")
			Label_v.grid(column=12, row=numCondiciones)

			#Textareas
			sax=tk.StringVar()
			sa_x.append(sax)
			Text_x=tk.Entry(vp,width=6,textvariable=sax)
			Text_x.grid(column=5,row=numCondiciones)
			say=tk.StringVar()
			sa_y.append(say)
			Texto_y=tk.Entry(vp,width=6,textvariable=say)
			Texto_y.grid(column=7,row=numCondiciones)
			saw=tk.StringVar()
			sa_w.append(saw)
			Text_w=tk.Entry(vp,width=6,textvariable=saw)
			Text_w.grid(column=9,row=numCondiciones)
			sav=tk.StringVar()
			sa_v.append(sav)
			Text_v=tk.Entry(vp,width=6,textvariable=sav)
			Text_v.grid(column=11,row=numCondiciones)

			##print sa_x[0].get()
			##print sa_x[1].get()
			
			
			tkvar=tk.StringVar(raiz)
			choices={'>=','<=','='}
			tkvar.set('=')
			popupMenu=tk.OptionMenu(vp,tkvar,*choices)
			popupMenu.grid(column=13, row=numCondiciones)
			tkvar.trace('w', change_drop)

			iguals=tk.StringVar()
			igual.append(iguals)
			Text_igual=tk.Entry(vp,width=6,textvariable=iguals)
			Text_igual.grid(column=14,row=numCondiciones)
			#vp.pack()

	except IndexError:
			print "No se permiten mas de 5 condiciones"

def change_drop(*args):
	global tkvar
	global choices
	signo[contador.get()-5]=tkvar.get()


###############################INICIA MAIN##########################

contador=tk.IntVar() #lleva el numero de condiciones que se han usado -4
#ventana principal
vp=tk.Frame(raiz)
#configuraciones base para la ventana principal
vp.grid(column=0, row=0,padx=(50,50), pady=(10,10))
vp.columnconfigure(0,weight=1)
vp.rowconfigure(0,weight=1)


#se anaden los elementos base


#labels
Label_titulo=tk.Label(vp, text="Solucionador de problemas de P.L. mediante algoritmos geneticos")
#Label_titulo.grid(column=3,row=1)
Label_z=tk.Label(vp,text="Z=")
Label_z.grid(column=4, row=2)

Label_x=tk.Label(vp,text="X+")
Label_x.grid(column=6, row=2)

Label_y=tk.Label(vp,text="Y+")
Label_y.grid(column=8, row=2)

Label_w=tk.Label(vp,text="W+")
Label_w.grid(column=10, row=2)

Label_v=tk.Label(vp,text="V")
Label_v.grid(column=12, row=2)




#Textareas
x_main=tk.StringVar()
z.append(x_main)
Text_x=tk.Entry(vp,width=6,textvariable=x_main)
Text_x.grid(column=5,row=2)

y_main=tk.StringVar()
z.append(y_main)
Text_y=tk.Entry(vp,width=6,textvariable=y_main)
Text_y.grid(column=7,row=2)

w_main=tk.StringVar()
z.append(w_main)
Text_w=tk.Entry(vp,width=6,textvariable=w_main)
Text_w.grid(column=9,row=2)

v_main=tk.StringVar()
z.append(v_main)
Text_v=tk.Entry(vp,width=6,textvariable=v_main)
Text_v.grid(column=11,row=2)


#botones
contador.set(4)
boton_Agregar=tk.Button(vp,text="Agregar", command=agrega_condicion)
boton_Agregar.grid(column=1,row=12)

boton_Min=tk.Button(vp,text="Minimizar", command=Minimizar)
boton_Min.grid(column=2, row=12)

boton_Max=tk.Button(vp,text="Maximizar", command=Maximizar)
boton_Max.grid(column=3, row=12)



#texto a lado de Z

Label_Texto=tk.Label(vp,text="Funcion objetivo: ")
Label_Texto.grid(column=1, row=2, columnspan=2)
Label_Texto=tk.Label(vp,text="Calculadora de algoritmos geneticos V1.0")
Label_Texto.grid(column=5, row=1, columnspan=6)

#bits de precision
Label_Bits=tk.Label(vp,text="Numero de bits de precision: ")
Label_Bits.grid(column=1, row=10, columnspan=2)
bits=tk.StringVar()
Bits_Precision.append(bits)
Text_Bits=tk.Entry(vp,width=6,textvariable=bits)
Text_Bits.grid(column=3,row=10)


#numero de iteraciones
#bits de precision
Label_itera=tk.Label(vp,text="Numero de iteraciones: ")
Label_itera.grid(column=1, row=11, columnspan=2)
itera=tk.StringVar()
Itera.append(itera)
Text_itera=tk.Entry(vp,width=6,textvariable=itera)
Text_itera.grid(column=3,row=11)

#poner en la matriz


raiz.mainloop()
