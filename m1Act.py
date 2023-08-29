# Importación de librerías
import math
import heapq
from random import randrange
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

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

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def astar(grid, start, end):
    open_list = []
    closed_set = set()

    start_node = Node(start)
    end_node = Node(end)
    
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        closed_set.add(current_node.position)

        for neighbor in get_neighbors(current_node.position, grid):
            if neighbor in closed_set:
                continue
            
            g_score = current_node.g + 1
            h_score = heuristic(neighbor, end_node.position)
            f_score = g_score + h_score

            if any(neighbor == node.position for node in open_list):
                existing_node = next(node for node in open_list if node.position == neighbor)
                if g_score < existing_node.g:
                    existing_node.g = g_score
                    existing_node.f = f_score
                    existing_node.parent = current_node
            else:
                neighbor_node = Node(neighbor, current_node)
                neighbor_node.g = g_score
                neighbor_node.h = h_score
                neighbor_node.f = f_score
                heapq.heappush(open_list, neighbor_node)

    return None

def get_neighbors(position, grid):
    neighbors = []
    col, row = position  # Swap col and row here
    rows, cols = len(grid), len(grid[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dc, dr in directions:  # Swap dc and dr here
        new_col, new_row = col + dc, row + dr  # Swap new_col and new_row here
        if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] == 1:
            neighbors.append((new_col, new_row))  # Swap new_col and new_row here
    
    return neighbors

def heuristic(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

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
        
    def step(self):
        
        #Si el estado es IDLE, entonces busca basura
        if self.condition == self.IDLE:
            inicerator_node = self.inc.getPos()
            path = astar(self.grid, self.last, inicerator_node)
            if self.count < len(path):
                next_move = path[self.count]
                #print(next_move)
                self.model.grid.move_agent(self, next_move)          
                self.count += 1
                
        #Si el estado es CARGADO, el robot tiene basura y va rumbo al incinerador
        elif self.condition == self.CARGADO:
            inicerator_node = self.inc.getPos()
            path = astar(self.grid, self.last, inicerator_node)
            if self.count < len(path):
                next_move = path[self.count]
                #print(next_move)
                self.model.grid.move_agent(self, next_move)          
                self.count += 1
                
        #Si el estado es REGRESANDO, entonces voy de regreso a la posición inicial
        elif self.condition == self.REGRESANDO:
            path = astar(self.grid, self.last, self.iniPos)
            if self.count < len(path):
                next_move = path[self.count]
                #print(next_move)
                self.model.grid.move_agent(self, next_move)          
                self.count += 1
        
            

class Incinerator(Agent):
    
    FINE = 0
    BURNING = 1
    BURNT_OUT = 2
    
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.radio = 1
        self.condition = self.FINE

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
    
    FINE = 0
    BURNING = 1
    BURNT_OUT = 2
    
    def __init__(self, model: Model):
        super().__init__(model.next_id(), model)
        self.condition = self.FINE
    
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
        self.schedule = RandomActivation(self)
        self.sizeofmatrix = sizeofmatrix
        
        #Posiciones iniciales colocadas en clase Zona debido a error que tenian al modificar el sizeofmatrix
        #Posición del incinerador (en medio de todo)
        incineratorposition=(sizeofmatrix//2,sizeofmatrix//2)
        #Posiciones de cada robot
        # robotpositions=[
        #     (self.sizeofmatrix//self.sizeofmatrix,self.sizeofmatrix//self.sizeofmatrix),
        #     (self.sizeofmatrix//self.sizeofmatrix, self.sizeofmatrix - 1 - self.sizeofmatrix//self.sizeofmatrix),
        #     (self.sizeofmatrix - 1 - self.sizeofmatrix//self.sizeofmatrix, self.sizeofmatrix//self.sizeofmatrix),
        #     (self.sizeofmatrix - 1 - self.sizeofmatrix//self.sizeofmatrix, self.sizeofmatrix - 1 - self.sizeofmatrix//self.sizeofmatrix)
        # ]
        
        robotpositions=[
            (1,1),
            (1, self.sizeofmatrix -2),
            (self.sizeofmatrix -2, 1),
            (self.sizeofmatrix -2, self.sizeofmatrix -2)
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
                if self.random.random() < density:
                    if self.matrix[y][x] == 1:
                        basura = Basura(self)
                        # if x == 25: #Origen cambiado al centro del grid
                        #     basura.condition = Basura.BURNING
                        self.grid.place_agent(basura, (x, y))
                        self.schedule.add(basura)
        
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
        
        #Spawnear Incinerator en el centro      
        incinerator = Incinerator(self, incineratorposition)
        self.grid.place_agent(incinerator, incinerator.pos)
        self.schedule.add(incinerator)

        #Spawnear Robots
        robot1 = Robot(self, robotpositions[0], incinerator, self.matrix, 0)
        robot2 = Robot(self, robotpositions[1], incinerator, self.matrix, 1)
        robot3 = Robot(self, robotpositions[2], incinerator, self.matrix, 2)
        robot4 = Robot(self, robotpositions[3], incinerator, self.matrix, 3)
        robotos=[robot1, robot2, robot3, robot4]
        
        for robot in robotos:
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)
            
        # Contar cuántos árboles ya se recolectaron. Dividir cantidad con respecto a total, dando porcentaje
        #Función lambda es una función anónima que puede pasar como parámetro             
        self.datacollector = DataCollector({"Porcentaje recolectado": lambda m: self.count_type(m, Basura.BURNT_OUT) / len(self.schedule.agents)})

    @staticmethod
    def count_type(model, condition):
        count = 0
        for basura in model.schedule.agents:
            if basura.condition == condition:
                count += 1
        return count
    
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Ejecutar hasta paso específico (opcional)
        # if self.schedule.steps==20:
        #     self.running=False
        
def agent_portrayal(agent):
    
    # if agent.condition == Basura.FINE:
    #     portrayal = {"Shape": "coal.png", "Layer": 1}
    # elif agent.condition == Basura.BURNING:
    #     portrayal = {"Shape": "circle", "Filled": "true", "Color": "Red", "r": 0.75, "Layer": 0}
    # elif agent.condition == Basura.BURNT_OUT:
    #     portrayal = {"Shape": "circle", "Filled": "true", "Color": "Gray", "r": 0.75, "Layer": 0}
    # elif agent.condition == Piso:
    #     portrayal= {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "white", "Layer": 0}
    # elif agent.condition == Incinerator:
    #     portrayal= {"Shape": "horno.png", "Layer": 1}
    # elif agent.condition == Robot:
    #     portrayal= {"Shape": "steve.png", "Layer": 1}
    # elif agent.condition == WallBlock:
    #     portrayal= {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#706d64", "Layer": 1}
    # else:
    #     portrayal = {}
    
    incineratora= {"Shape": "horno.png", "Layer": 2}
    incineratorb= {"Shape": "hornoencendido.png", "Layer": 2}
    robota = {"Shape": "steve.png", "Layer": 3}
    robotb = {"Shape": "herobrine.png", "Layer": 3}
    pisoa = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#a4d6a3", "Layer": 0}
    wallblocka = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#706d64", "Layer": 1}
    #basuraa = {"Shape": "coal.png", "Layer": 1}
    basuraa = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#7b8c89", "Layer": 1}

    #Regresar preset
    # if type(agent)==Piso:
    #     return(pisoa)
    
    
    if type(agent)==WallBlock:
        return(wallblocka)
    
    elif type(agent)==Incinerator:
        #Si el incinerador no tiene carga, regresar horno
        if agent.condition == agent.FINE:
            return(incineratora)
        #Si el incinerador tiene carga, regresar horno encendido
        elif agent.condition == agent.BURNING:
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
        return(basuraa)

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