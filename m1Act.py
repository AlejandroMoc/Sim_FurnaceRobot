# Importación de librerías
import math
import heapq
from random import randrange
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule

#Gridsize Inicial
gridsize = 53

#Funciones para pathfinding
def distancia_entre_puntos(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Clase de robot
class Robot(Agent):
        
    IDLE = 0
    CARGADO = 1
    REGRESANDO = 2 
    
    def __init__(self, model, pos, inc, grid, id):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.iniPos = pos
        #Agregado
        self.radio = 1.0
        self.inc = inc
        self.last = pos
        self.grid = grid
        self.count = 0
        #Condición inicial del robot es IDLE
        self.condition = self.IDLE
        #Agregada id de cada robot
        self.id = id
        self.basura = False
        #direccion para movimiento en IDLE
        self.direccion = [1,1] 
        
        #atributos asignados para que el robot sepa si repite recorrido
        self.vueltas = 0
        self.regreso = False
        
        #Ultima basura encontrada
        self.basuraPos = None
        
    def step(self):
        #Espacio del robot de enmedio
        small_grid_1 = gridsize - gridsize // 2 + gridsize // 7 #hacia la derecha y arriba
        small_grid_2 = gridsize // 2 - gridsize // 7 #hacia la izquierda y abajo
        #Si el estado es IDLE, entonces busca basura
        if self.condition == self.IDLE:
            x,y = self.pos
            #robot abajo izquierda   
            if self.id == 0:              
                #movimientos hacia la derecha y arriba
                if x + 1 == small_grid_2 and y >= small_grid_2 and self.direccion[0] == 1:
                    if (y == gridsize//2 - 1):
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1,1]
                elif x < gridsize//2 and self.direccion[0] == 1:
                    next_move = (x + 1,y)  
                elif x == gridsize//2 and self.direccion[0] == 1:
                    if (y == gridsize//2 - 1):
                        return
                    elif y + 1 == small_grid_2:
                        next_move = (x - 1, y)
                        self.direccion = [-1,1]
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1,1]

                #movimientos hacia la izquierda y arriba
                elif x > 1 and self.direccion[0] == -1:
                    next_move = (x - 1,y)
                elif x == 1 and self.direccion[0] == -1:
                    if (y == gridsize//2 - 1):
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [1,1] 
                
                self.model.grid.move_agent(self, next_move)          
                self.count += 1
                
            #robot izquierda arriba
            elif self.id == 1: 
                #movimientos hacia la derecha y abajo
                if x + 1 == small_grid_2 and y <= small_grid_1 and self.direccion[0] == 1:
                    if (y == gridsize//2):
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1,1]
                elif x < gridsize//2 - 1 and self.direccion[0] == 1:
                    next_move = (x + 1,y)
                elif x == gridsize//2 - 1 and self.direccion[0] == 1:
                    if (y == gridsize//2):
                        return
                    elif y == small_grid_1:
                        next_move = (x - 1, y)
                        self.direccion = [-1,1]
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1,1]
                    
                #movimientos hacia la izquierda y abajo
                elif x > 1 and self.direccion[0] == -1:
                    next_move = (x - 1,y)
                elif x == 1 and self.direccion[0] == -1:
                    if (y == gridsize//2):
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [1,1] 
                
                self.model.grid.move_agent(self, next_move)          
                self.count += 1 
                        
            #robot abajo derecha 
            elif self.id == 2: 
                #movimientos hacia la izquierda y arriba
                if x == small_grid_1 and y >= small_grid_2 and self.direccion[0] == 1:
                    if (y == gridsize//2):
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1,1]
                elif x > gridsize//2 + 1 and self.direccion[0] == 1:
                    next_move = (x - 1,y)
                elif x == gridsize//2 + 1 and self.direccion[0] == 1:
                    if (y == gridsize//2):
                        return
                    elif y + 1 == small_grid_2:
                        next_move = (x - 1, y)
                        self.direccion = [-1,1]
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1,1]
                        
                #movimientos hacia la derecha y arriba
                elif x < gridsize - 2 and self.direccion[0] == -1:
                    next_move = (x + 1,y)
                elif x == gridsize - 2 and self.direccion[0] == -1:
                    if (y == gridsize//2):
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [1,1] 
                
                self.model.grid.move_agent(self, next_move)          
                self.count += 1                

            #robot arriba derecha 
            elif self.id == 3: 
                #movimientos hacia la izquierda y abajo
                if x == small_grid_1 and y <= small_grid_1 and self.direccion[0] == 1:
                    if (y == gridsize//2 + 1):
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1,1]
                elif x > gridsize//2 and self.direccion[0] == 1:
                    next_move = (x - 1,y)
                elif x == gridsize//2 and self.direccion[0] == 1:
                    if (y == gridsize//2 + 1):
                        return
                    elif y == small_grid_1:
                        next_move = (x - 1, y)
                        self.direccion = [-1,1]
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1,1]
                        
                #movimientos hacia la derecha y abajo
                elif x < gridsize - 2 and self.direccion[0] == -1:
                    next_move = (x + 1,y)
                elif x == gridsize - 2 and self.direccion[0] == -1:
                    if (y == gridsize//2 + 1):
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [1,1] 
                
                self.model.grid.move_agent(self, next_move)          
                self.count += 1
        
            #robot en medio
            elif self.id == 4:
                x,y = self.pos           
                #movimientos hacia la derecha y arriba
                if x < small_grid_1 - (self.vueltas + 1) and self.direccion[0] == 1 and self.direccion[1] == 1:
                    next_move = (x + 1,y)
                elif x == small_grid_1 - (self.vueltas + 1) and self.direccion[1] == 1:
                    if (y == small_grid_1 - (self.vueltas + 1)):
                        self.direccion = [-1,-1]
                        next_move = (x - 1, y)
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1,1]
                    
                #movimientos hacia la izquierda y arriba
                elif x > small_grid_2 + self.vueltas and self.direccion[0] == -1:
                    next_move = (x - 1,y)
                elif x == small_grid_2 + self.vueltas and self.direccion[1] == -1:
                    if (y == small_grid_2 + self.vueltas):
                        if self.vueltas == gridsize//7 - 1: #Se cuenta el numero de vueltas del recorrido
                            self.vueltas -= 1               #Se utiliza para saber si ya tiene que hacer el reocrrido en reversa
                            self.regreso = True             #Se encuentra regresando
                        elif not self.regreso:
                            self.vueltas += 1
                        else:
                            self.vueltas -= 1
                            if self.vueltas == 0:
                                self.regreso = False        #No se encuentra regresando
                        self.direccion = [1,1]
                        next_move = (x, y)
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [1, -1]
                
                self.model.grid.move_agent(self, next_move)          
                self.count += 1
                
        #Si el estado es CARGADO, el robot tiene basura y va rumbo al incinerador
        elif self.condition == self.CARGADO:
            inicerator_node = self.inc.getPos()
            mejor_movimiento = None
            mejor_distancia = float('inf')  # Inicializar con un valor muy grande
            posiblemovs = [
                (self.pos[0] + 1, self.pos[1]),
                (self.pos[0] + 1, self.pos[1] + 1),
                (self.pos[0], self.pos[1] + 1),
                (self.pos[0] - 1, self.pos[1] + 1),
                (self.pos[0] - 1, self.pos[1]),
                (self.pos[0] - 1, self.pos[1] - 1),
                (self.pos[0], self.pos[1] - 1),
                (self.pos[0] + 1, self.pos[1] - 1)
            ]
            for movim in posiblemovs:
                distancia = distancia_entre_puntos(movim, inicerator_node)
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_movimiento = movim
            next_move = mejor_movimiento
            self.last = self.pos 
            self.model.grid.move_agent(self, next_move)
            if next_move == inicerator_node:
                self.condition = self.REGRESANDO
                
        #Si el estado es REGRESANDO, entonces voy de regreso a la posición inicial
        #Se podria implementar con un pathfinding pero teniendo como objetivo la posicion donde encontro la basura
        elif self.condition == self.REGRESANDO:
            mejor_movimiento = None
            mejor_distancia = float('inf')  # Inicializar con un valor muy grande
            posiblemovs = [
                (self.pos[0] + 1, self.pos[1]),
                (self.pos[0] + 1, self.pos[1] + 1),
                (self.pos[0], self.pos[1] + 1),
                (self.pos[0] - 1, self.pos[1] + 1),
                (self.pos[0] - 1, self.pos[1]),
                (self.pos[0] - 1, self.pos[1] - 1),
                (self.pos[0], self.pos[1] - 1),
                (self.pos[0] + 1, self.pos[1] - 1)
            ]
            for movim in posiblemovs:
                distancia = distancia_entre_puntos(movim, self.basuraPos)
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_movimiento = movim
            next_move = mejor_movimiento
            self.last = self.pos 
            self.model.grid.move_agent(self, next_move)
            if next_move == self.basuraPos:
                self.condition = self.IDLE
                
    def getPos(self):
        return self.pos
    
    def setBasura(self, pos):
        self.basuraPos = pos
        
    def actualizaEstado(self, estado):
        if estado == 0:
            self.condition = self.IDLE
        elif estado == 1:
            self.condition = self.CARGADO
        else:
            self.condition = self.REGRESANDO   
            
    def muestraEstado(self):
        return self.condition

class Incinerator(Agent):
    
    # FINE = 0
    # BURNING = 1
    # BURNT_OUT = 2
    
    APAGADO = 0
    ENCENDIDO = 1
    
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.radio = 1
        self.condition = self.APAGADO

    #def step(self):
    #    return None

    def getPos(self):
        return self.pos
        
    def buscaColision(self, fantasma):
        dx = self.pos[0] - fantasma.self.pos[0]
        dy = self.pos[1] - fantasma.self.pos[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        return distancia < self.radio + fantasma.self.radio

class Piso(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

#Agentes
class Basura(Agent):
    RECOLECTADA = 0
    TIRADA = 1
    def __init__(self, model: Model, pos, robots):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.robots = robots
        self.condition = self.TIRADA
    def step(self):
        for robot in self.robots:
            if self.pos == robot.getPos() and self.condition == self.TIRADA and robot.muestraEstado() == 0:
                robot.setBasura(self.pos)
                self.condition = self.RECOLECTADA
                robot.actualizaEstado(1)

    # def step(self):
    #     if self.condition == self.BURNING:

    #         #if self.probability_of_spread2 < self.probability_of_spread:
                
    #             #Valor default de la posición del fuego
    #             #fire_neighbors = self.pos
                
    #             #Quemar vecino (no aplica)
    #             # if self.model.grid.out_of_bounds(fire_neighbors): #Se cambio el condicional inicial
    #             #     return() #Se agrega un if para cuando se pase del grid
    #             # elif self.probability_of_spread2<self.probability_of_spread:
    #             #     for neighbor in self.model.grid.iter_neighbors(fire_neighbors, moore=True):                      #CAMBIADO SELF.POS PARA QUE USE fire_neighbors
    #             #         if neighbor.condition == self.FINE:
    #             #             neighbor.condition = self.BURNING
    #             #     self.condition = self.BURNT_OUT                 
            
    #         #ESTO SE TIENE QUE ACTUALIZAR
    #         #Cuando el robot lo recoja, borrar
    #         self.condition = self.BURNT_OUT

class Zona(Model):

    def __init__(self, height=50, width=50, density=0.6, sizeofmatrix=83):
        super().__init__()
        self.schedule = BaseScheduler(self)
        self.sizeofmatrix = sizeofmatrix
        
        #se actualiza gridsize en caso que se cambie de medidas con el slider
        global gridsize
        gridsize = sizeofmatrix
        #Posiciones iniciales
        
        #Posición del incinerador (en medio de todo)
        incineratorposition=(sizeofmatrix//2,sizeofmatrix//2)
        
        robotpositions=[
            (1,1),
            (1, self.sizeofmatrix -2),
            (self.sizeofmatrix -2, 1),
            (self.sizeofmatrix -2, self.sizeofmatrix -2),
            (self.sizeofmatrix // 2 - self.sizeofmatrix // 7, self.sizeofmatrix // 2 - self.sizeofmatrix // 7)
        ]
        
        self.grid = MultiGrid(self.sizeofmatrix, self.sizeofmatrix, torus=False)

        #ESTO SE DEBE CAMBIAR SUPONGO
                
        #Dibujado de la matriz sizeofmatrix x sizeofmatrix
        self.matrix=[]
        i = 0
        j = 0
        
        for i in range(self.sizeofmatrix): 
            if i == 0 and j == 0:
                self.matrix.append([0]*self.sizeofmatrix)
            elif i == self.sizeofmatrix-1 and j == self.sizeofmatrix-1:
                self.matrix.append([0]*self.sizeofmatrix)
            else:
                #matrix.append([0])
                self.matrix.append([1] *(self.sizeofmatrix-2))
                #matrix.append([0])
                self.matrix[i].insert(0, 0)
                self.matrix[i].insert(self.sizeofmatrix, 0)
            j += 1
        
        #print(self.matrix)

        
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                
                #Si la posición tiene 1, es tipo Piso
                if self.matrix[y][x] == 1:
                    block = Piso(self, (x, y))
                    self.grid.place_agent(block, block.pos)
                    
                #Si la posición tiene 0, es tipo Muro
                if self.matrix[y][x] == 0:
                    #print(f"block at ({x}, {y})")
                    block2 = WallBlock(self, (x, y))
                    self.grid.place_agent(block2, block2.pos)
        
        #Spawnear Incinerator en centro     
        incinerator = Incinerator(self, incineratorposition)
        self.grid.place_agent(incinerator, incinerator.pos)
        self.schedule.add(incinerator)

        #Spawnear Robots
        robot1 = Robot(self, robotpositions[0], incinerator, self.matrix, 0)
        robot2 = Robot(self, robotpositions[1], incinerator, self.matrix, 1)
        robot3 = Robot(self, robotpositions[2], incinerator, self.matrix, 2)
        robot4 = Robot(self, robotpositions[3], incinerator, self.matrix, 3)
        robot5 = Robot(self, robotpositions[4], incinerator, self.matrix, 4)
        robotos=[robot1, robot2, robot3, robot4, robot5]
        
        trashPositions = []
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.random.random() < density:
                    if self.matrix[y][x] == 1:
                        trashcoor = []
                        basura = Basura(self,(x,y),robotos)
                        # if x == 25: #Origen cambiado al centro del grid
                        #     basura.condition = Basura.BURNING
                        self.grid.place_agent(basura, (x, y))
                        trashcoor.append(x)
                        trashcoor.append(y)
                        trashPositions.append(trashcoor)
                        self.schedule.add(basura)
                        
        for robot in robotos:
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)
            
        ### Contar cuántos árboles ya se recolectaron. Dividir cantidad con respecto a total, dando porcentaje
        #Función lambda es una función anónima que puede pasar como parámetro             
        self.datacollector = DataCollector({"Porcentaje recolectado": lambda m: self.count_type(m, Basura) / len(self.schedule.agents)})

    @staticmethod
    def count_type(model, condition):
        count = 0
        for basura in model.schedule.agents:
            count += 1
        return count
    
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Ejecutar hasta paso específico (opcional)
        # if self.schedule.steps==20:
        #     self.running=False
        
def agent_portrayal(agent):
    
    incineratora= {"Shape": "/Users/LACG2/OneDrive/Escritorio/Python/Multiagentes/M1_1/E3_M1Actividad/horno.png", "Layer": 2}
    incineratorb= {"Shape": "/Users/LACG2/OneDrive/Escritorio/Python/Multiagentes/M1_1/E3_M1Actividad/hornoencendido.png", "Layer": 2}
    robota = {"Shape": "/Users/LACG2/OneDrive/Escritorio/Python/Multiagentes/M1_1/E3_M1Actividad/steve.png", "Layer": 3}
    robotb = {"Shape": "/Users/LACG2/OneDrive/Escritorio/Python/Multiagentes/M1_1/E3_M1Actividad/herobrine.png", "Layer": 3}
    pisoa = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#a4d6a3", "Layer": 0}
    pisoBasura = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#FFFFFF", "Layer": 0}
    wallblocka = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#706d64", "Layer": 1}
    #basuraa = {"Shape": "coal.png", "Layer": 1}
    basuraa = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#7b8c89", "Layer": 1}
    
    
    if type(agent)==WallBlock:
        return(wallblocka)
    # elif type(agent)==Piso:
    #     return(pisoa)
    elif type(agent)==Incinerator:
        #Si el incinerador no tiene carga, regresar horno
        if agent.condition == agent.APAGADO:
            return(incineratora)
        #Si el incinerador tiene carga, regresar horno encendido
        elif agent.condition == agent.ENCENDIDO:
            return(incineratorb)
        
    elif type(agent) == Robot:
        #El robot está buscando basura
        if agent.condition == agent.IDLE:
            return(robota)
        #Tiene basura y va a dejarla al incinerador
        elif agent.condition == agent.CARGADO:
            return(robotb)
        #Ya dejó basura, va de regreso a su posición inicial
        elif agent.condition == agent.REGRESANDO:
            return(robotb)
        
    elif type(agent)==Basura:
        if agent.condition == agent.TIRADA:
            return(basuraa)
        else:
            return(pisoBasura)

    #return portrayal

grid = CanvasGrid(agent_portrayal, gridsize, gridsize, gridsize *10, gridsize *10)

#Pregunta 1.3
chart = ChartModule([{"Label": "Basura recogida", "Color": "Black"}], data_collector_name = 'datacollector')

server = ModularServer(Zona, [grid, chart], "Robots Recolectores", {
    "density": Slider("Densidad de la basura", 0.1, 0.01, 0.1, 0.01),
    "sizeofmatrix": Slider("Tamaño de la simulación", gridsize, 21, gridsize, 1),
    "width":50, "height":50,
})

server.port = 8526
server.launch()