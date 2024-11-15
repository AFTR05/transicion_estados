import time                 # Importa el módulo time para simular el tiempo de ejecución de procesos
import random               # Importa el módulo random para generar duraciones aleatorias de los procesos
from queue import Queue     # Importa la clase Queue para manejar la cola de procesos

# Definición de la clase Proceso, que representa cada proceso en el sistema
class Proceso:
    def __init__(self, id, duracion, estado):
        self.id = id                    # Asigna un identificador único al proceso
        self.duracion = duracion        # Define la duración total que el proceso necesita para completarse
        self.tiempo_restante = duracion # Establece el tiempo restante, que se actualizará durante la ejecución
        self.estado = estado            # Establece el estado inicial del proceso

    # Define cómo se mostrará el proceso cuando se imprima
    def __str__(self):
        return f"Proceso {self.id} | Estado: {self.estado} | Tiempo restante: {self.tiempo_restante}s"

# Crear una cola de procesos para gestionar los procesos listos para ejecutarse
cola_procesos = Queue()

# Estados iniciales posibles, excluyendo "Terminado"
# nuevo, listo,  ejecutando, esperando, terminado
estados_iniciales= ["Listo", "Bloqueado", "En ejecución", "Esperando", "Terminado"]

# Generar algunos procesos aleatorios y añadirlos a la cola de procesos
for i in range(10):  # Cambia este número para agregar más procesos si se desea
    duracion = random.randint(2, 10)                 # Asigna una duración aleatoria entre 2 y 5 segundos a cada proceso
    estado_inicial = random.choice(estados_iniciales)  # Asigna un estado inicial aleatorio
    proceso = Proceso(id=i + 1, duracion=duracion, estado=estado_inicial)  # Crea un proceso con un identificador, duración y estado inicial
    cola_procesos.put(proceso)                      # Añade el proceso a la cola

# Muestra la cola inicial de procesos antes de la ejecución
print("Cola de procesos inicial:")
for proceso in list(cola_procesos.queue):
    print(proceso)

# Estructura del planificador
def planificador(cola_procesos, quantum=2, expulsivo=True):
    """
    Función que simula un planificador de procesos.
    :param cola_procesos: Cola de procesos listos para ejecutar
    :param quantum: Tiempo máximo en segundos para procesos expulsivos
    :param expulsivo: Define si el planificador es expulsivo o no
    """
    procesos_bloqueados = Queue()  # Cola auxiliar para procesos bloqueados

    while not cola_procesos.empty() or not procesos_bloqueados.empty():
        if cola_procesos.empty() and not procesos_bloqueados.empty():
            print("\nNo quedan procesos listos. Cambiando procesos bloqueados a 'Listo' para reanudar.")
            # Mueve todos los procesos de bloqueados a listos
            while not procesos_bloqueados.empty():
                proceso = procesos_bloqueados.get()
                proceso.estado = "Listo"
                cola_procesos.put(proceso)

        proceso = cola_procesos.get()

        # Gestión de estados
        if proceso.estado == "Nuevo":
            print(f"{proceso} pasa de 'Nuevo' a 'Listo'.")
            proceso.estado = "Listo"
            cola_procesos.put(proceso)

        elif proceso.estado == "Listo":
            print(f"{proceso} pasa de 'Listo' a 'En ejecución'.")
            proceso.estado = "En ejecución"

        elif proceso.estado == "En ejecución":
            print(f"\nEjecutando {proceso}")
            tiempo_ejecucion = min(proceso.tiempo_restante, quantum)
            proceso.tiempo_restante -= tiempo_ejecucion
            time.sleep(tiempo_ejecucion)
            if proceso.tiempo_restante > 0:
                proceso.estado = random.choice(["Bloqueado", "Esperando", "Listo"])
                print(f"{proceso} no terminó. Cambia a estado '{proceso.estado}'.")
                if proceso.estado == "Bloqueado":
                    procesos_bloqueados.put(proceso)
                else:
                    cola_procesos.put(proceso)
            else:
                proceso.estado = "Terminado"
                print(f"{proceso} ha terminado.")

        elif proceso.estado == "Esperando":
            print(f"{proceso} está esperando. Pasa a 'Listo'.")
            proceso.estado = "Listo"
            cola_procesos.put(proceso)

        elif proceso.estado == "Bloqueado":
            print(f"{proceso} está bloqueado y no puede ejecutarse ahora.")
            procesos_bloqueados.put(proceso)

        elif proceso.estado == "Terminado":
            print(f"{proceso} ya ha terminado. Se elimina del sistema.")

# Ejecuta la simulación de planificación de procesos
print("\nIniciando la simulación del planificador de procesos")
planificador(cola_procesos)