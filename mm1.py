import numpy as np
import matplotlib.pyplot as plt

class Simulacion():
   reloj = 0.0
   estado_servidor = 0 #0-disponible 1-ocupado
   proximo_evento = ""
   tiempo_servidor_acumulado = 0.0
   demora_acumulada_clientes_en_cola = 0.0
   area_clientes_en_cola_q = 0.0
   tiempo_ultimo_evento_reloj = 0.0
   cantidad_clientes_en_cola = 0
   completaron_demora_en_cola = 0
   tiempo_arribo = 7.0
   tiempo_servicio = 9.0
   eventos = []
   cola = []
   tasa_arribo_respecto_tasa_servicio = [tiempo_servicio*0.25, tiempo_servicio*0.5,tiempo_servicio*0.75]
   nombre_tasa_arribo_respecto_tasa_servicio = ['25%','50%','75%']

   #Listas para graficas
   lista_utilizacion_servidor = []
   lista_area_clientes_en_cola_q = []
   lista_demora_cola = []

   #Listas para promedios
   promedio_lista_utilizacion_servidor = []
   promedio_lista_area_clientes_en_cola_q = []
   promedio_lista_demora_cola = []

   promedio_numpy_lista_utilizacion_servidor = []
   promedio_numpy_lista_area_clientes_en_cola_q = []
   promedio_numpy_lista_demora_cola = []

   def initialization_routine(self):
       self.reloj = 0.0
       self.estado_servidor = 0 #0-disponible 1-ocupado
       self.proximo_evento = ""
       self.reloj = 0.0
       self.tiempo_servidor_acumulado = 0.0
       self.demora_acumulada_clientes_en_cola = 0.0
       self.area_clientes_en_cola_q = 0.0
       self.tiempo_ultimo_evento_reloj = 0.0
       self.cantidad_clientes_en_cola = 0
       self.completaron_demora_en_cola = 0
       self.eventos = []
       self.cola = []
       self.eventos.append(np.random.exponential(1/self.tiempo_arribo))
       self.eventos.append(99999999) #Para que el prox sea un arribo

       #Listas para graficas
       self.lista_utilizacion_servidor.clear()
       self.lista_area_clientes_en_cola_q.clear()
       self.lista_demora_cola.clear()
       #Promedios
       self.promedio_lista_utilizacion_servidor.clear()
       self.promedio_lista_area_clientes_en_cola_q.clear()
       self.promedio_lista_demora_cola.clear()

       self.promedio_numpy_lista_utilizacion_servidor = None
       self.promedio_numpy_lista_area_clientes_en_cola_q = None
       self.promedio_numpy_lista_demora_cola = None

   def timing(self):
       self.tiempo_ultimo_evento_reloj = self.reloj
       if self.eventos[0] <= self.eventos[1]:
           self.reloj = self.eventos[0]
           self.proximo_evento = "Arribo"
       else:
           self.reloj = self.eventos[1]
           self.proximo_evento = "Partida"

   def arrive(self):
       self.eventos[0] = self.reloj + np.random.exponential(1/self.tiempo_arribo)
       if self.estado_servidor == 0:
           self.estado_servidor = 1 #Lo cambio a ocupado
           self.eventos[1] = self.reloj + np.random.exponential(1/self.tiempo_servicio)
           self.tiempo_servidor_acumulado += (self.eventos[1] - self.reloj)
           self.lista_utilizacion_servidor.append(self.tiempo_servidor_acumulado/self.reloj)
           self.completaron_demora_en_cola += 1
       else:
           self.area_clientes_en_cola_q += self.cantidad_clientes_en_cola * (self.reloj - self.tiempo_ultimo_evento_reloj)
           self.lista_area_clientes_en_cola_q.append(self.area_clientes_en_cola_q/self.reloj)
           self.cantidad_clientes_en_cola += 1
           self.cola.append(self.reloj)

   def departure(self):
       if self.cantidad_clientes_en_cola > 0:
           self.eventos[1] = self.reloj + np.random.exponential(1/self.tiempo_servicio)
           self.demora_acumulada_clientes_en_cola += self.reloj - self.cola[0]
           self.completaron_demora_en_cola += 1
           self.lista_demora_cola.append(self.demora_acumulada_clientes_en_cola/self.completaron_demora_en_cola)
           self.tiempo_servidor_acumulado += self.eventos[1] - self.reloj
           self.lista_utilizacion_servidor.append(self.tiempo_servidor_acumulado/self.reloj)
           self.area_clientes_en_cola_q += (self.cantidad_clientes_en_cola * (self.reloj - self.tiempo_ultimo_evento_reloj))
           self.lista_area_clientes_en_cola_q.append(self.area_clientes_en_cola_q/self.reloj)
           self.cantidad_clientes_en_cola -= 1
           self.cola.pop(0)
       else:
           self.estado_servidor = 0
           self.eventos[1] = 99999999

   def reports(self):
       #self.reports()
       print("-"*60)
       print("Cantidad promedio de clientes en cola: ", np.mean(np.mean(self.promedio_numpy_lista_area_clientes_en_cola_q, axis=1), axis=0))
       print("-"*60)
       print("Utilizacion promedio del servidor: ", np.mean(np.mean(self.promedio_numpy_lista_utilizacion_servidor,axis=1), axis=0))
       print("-"*60)
       print("Demora promedio de cliente: ", np.mean(np.mean(self.promedio_numpy_lista_demora_cola,axis=1),axis=0))

       #VALORES TEORICOS ESPERADOS
       print("-"*60)
       teorico_promedio_clientes_cola = (self.tiempo_arribo**2)/(self.tiempo_servicio*(self.tiempo_servicio-self.tiempo_arribo))
       print("Valor teorico cantidad clientes en cola: ",round(teorico_promedio_clientes_cola,4))
       print("-"*60)
       teorico_utilizacion_servidor = self.tiempo_arribo/self.tiempo_servicio
       print("Valor teorico Utilizacion del servidor: ",round(teorico_utilizacion_servidor,4))
       print("-"*60)
       teorico_demora_prom_cliente = self.tiempo_arribo/(self.tiempo_servicio*(self.tiempo_servicio-self.tiempo_arribo))
       print("Valor teorico demora clientes en cola: ",round(teorico_demora_prom_cliente,4))

       """
       print("-"*60) 
       lq = (self.tiempo_arribo**2)/(self.tiempo_servicio*(self.tiempo_servicio-self.tiempo_arribo))
       ls = lq + (self.tiempo_arribo/self.tiempo_servicio)
       print("Promedio clientes en el sistema: ", round(ls,4))
       print("-"*60)
       wq = lq / Simulacion.tiempo_arribo
       ws = wq + (1/Simulacion.tiempo_servicio)
       #print("Tiempo promedio clientes en el sistema", round(ws,4))
       print("-"*60)
       p0 = 1 - (self.tiempo_arribo/self.tiempo_servicio)
       pn = ((self.tiempo_arribo/self.tiempo_servicio)**5)*p0
       print("Probabilidad de que haya 5 clientes en el sistema", round(pn,4))
       print("-"*60)
       """

   def main(self):
       cantidad_experimentos = 10
       cont_tasa = 0

       for tasa in self.tasa_arribo_respecto_tasa_servicio:
           self.initialization_routine()
           self.tiempo_arribo = tasa #Vario la tasa de arribos con respecto a la de servicios
           print('*'*60)
           print(' TASA: ',self.nombre_tasa_arribo_respecto_tasa_servicio[cont_tasa])
           print('*'*60)
           cont_tasa+=1

           for i in range(cantidad_experimentos):
               while self.completaron_demora_en_cola < 201:
                   self.timing()
                   if self.proximo_evento == "Arribo":
                       self.arrive()
                   else:
                       self.departure()
               self.promedio_lista_utilizacion_servidor.append(self.lista_utilizacion_servidor) #En algunas simulaciones el servidor arroja un resultado mayor al 100%
                                                                                                #No encontramos el erorr
               self.promedio_lista_area_clientes_en_cola_q.append(self.lista_area_clientes_en_cola_q)
               self.promedio_lista_demora_cola.append(self.lista_demora_cola)


           #Los convierto a numpy para hacer el promedio de las 10 corridas
           self.promedio_numpy_lista_utilizacion_servidor = np.array(self.promedio_lista_utilizacion_servidor)
           self.promedio_numpy_lista_area_clientes_en_cola_q = np.array(self.promedio_lista_area_clientes_en_cola_q)
           self.promedio_numpy_lista_demora_cola = np.array(self.promedio_lista_demora_cola)
           self.reports()
           #GRAFICAS
           self.grafico_clientes_en_cola_area_q()
           self.grafico_utilizacion_servidor()
           self.grafico_demora_clientes_en_cola()

   def grafico_utilizacion_servidor(self):
       plt.title('Utilización promedio del servidor')
       utilizacion_promedio_servidor = (np.mean(np.mean(self.promedio_numpy_lista_utilizacion_servidor, axis = 1), axis=0))
       plt.plot(np.mean(self.promedio_numpy_lista_utilizacion_servidor, axis=0),color='skyblue')
       plt.axhline(utilizacion_promedio_servidor, linestyle='dashed', color='black')
       legend1 = 'Utilización servidor entre eventos'
       legend2 = 'Promedio: '+ str(round(utilizacion_promedio_servidor,4))
       plt.legend((legend1,legend2), loc="lower right")
       plt.show()

   def grafico_clientes_en_cola_area_q(self):
       plt.title('Promedio clientes en cola')
       promedio_clientes_en_cola = np.mean(np.mean(self.promedio_numpy_lista_area_clientes_en_cola_q, axis=1), axis=0)
       plt.plot(np.mean(self.promedio_numpy_lista_area_clientes_en_cola_q, axis=0),color='skyblue')
       plt.axhline(promedio_clientes_en_cola, linestyle='dashed', color='black')
       legend1 = 'Clientes en cola entre eventos'
       legend2 = 'Promedio: '+ str(round(promedio_clientes_en_cola,4))
       plt.legend((legend1,legend2), loc="lower right")
       plt.show()

   def grafico_demora_clientes_en_cola(self):
       plt.title('Demora promedio clientes en cola')
       demora_promedio_cola = np.mean(np.mean(self.promedio_numpy_lista_demora_cola,axis=1),axis=0)
       plt.plot(np.mean(self.promedio_numpy_lista_demora_cola, axis=0),color='skyblue')
       plt.axhline(demora_promedio_cola, linestyle='dashed', color='black')
       legend1 = 'Demora clientes en cola entre eventos'
       legend2 = 'Promedio: '+ str(round(demora_promedio_cola,4))
       plt.legend((legend1,legend2), loc="lower right")
       plt.show()

sim = Simulacion()
sim.main()

