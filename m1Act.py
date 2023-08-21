# Importación de librerías
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import math
import heapq

#Posiciones iniciales de los objetos
gridsize = 81

#Posición del incinerador (en medio de todo)
incineratorposition=(gridsize//2,gridsize//2)
ghostposition1=(1,2)


#Funcion distancia
def distancia_entre_puntos(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

#Agregados para A*
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

# Clase fantasma
class Robot(Agent):
    def __init__(self, model, pos, pac, grid):
        super().__init__(model.next_id(), model)
        self.pos = pos
        #Agregado
        self.radio = 1.0
        self.pac = pac
        self.last = pos
        self.grid = grid
        self.count = 0
        
    def step(self):
        pacmannode = self.pac.getPos()
        path = astar(self.grid, ghostposition1,incineratorposition)
        if self.count < len(path):
            next_move = path[self.count]
            print(next_move)
            self.model.grid.move_agent(self, next_move)          
            self.count += 1

class Incinerator(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.radio = 1

    def step(self):
        """ 
        #Obtener todos los movimientos posibles
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False)
        
        #Separar movimientos posibles
        posiblemovs=[]
        for movim in next_moves:
            x, y = movim
            if self.model.matrix[y][x] == 0:
                continue
            else:
                posiblemovs.append(movim)
        
        #Elegir pos aleatoria de movs posibles y hacer mov
        next_move = self.random.choice(posiblemovs)
        #enemigo.update(enemyNode.x,plataformaActual,enemyNode.z);
        self.model.grid.move_agent(self, next_move)
        """
        return None
        #Agregado
    def getPos(self):
        return self.pos
        
    def buscaColision(self, fantasma):
        dx = self.pos[0] - fantasma.self.pos[0]
        dy = self.pos[1] - fantasma.self.pos[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        return distancia < self.radio + fantasma.self.radio

#Clase de piso (blanco)
class Piso(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

#Clase de bloque de muro (azul)
class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

#Clase de modelo (laberinto)
class Maze(Model):
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(gridsize ,gridsize , torus=False)
        self.matrix = []

        #Dibujado de la matriz gridsize x gridsize
        i = 0
        j = 0
        
        for i in range(gridsize): 
            if i == 0 and j == 0:
                self.matrix.append([0]*gridsize)
            elif i == gridsize-1 and j == gridsize-1:
                self.matrix.append([0]*gridsize)
            else:
                #matrix.append([0])
                self.matrix.append([1] *(gridsize-2))
                #matrix.append([0])
                self.matrix[i].insert(0, 0)
                self.matrix[i].insert(gridsize, 0)
            j += 1
        
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

        #Spawnear Robot
        robot = Robot(self, ghostposition1, incinerator, self.matrix)
        self.grid.place_agent(robot, robot.pos)
        self.schedule.add(robot)

    def step(self):
        self.schedule.step()

def agent_portrayal(agent):
    
    #Definir presets
    wallblocka = {"Shape": "rect", "w": 1.1, "h":1.1, "Filled": "true", "Color": "#1543e6", "Layer": 1}
    #incineratora={"Shape": "circle", "r": 1, "Filled": "true", "Color": "Orange", "Layer": 0}
    incineratora= {"Shape": "horno.png", "Layer": 1}
    robota = {"Shape": "robot.png", "Layer": 1}
    pisoa = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#e0ecff", "Layer": 0}

    #Regresar preset
    if type(agent)==Piso:
        return(pisoa)
    elif type(agent)==WallBlock:
        return(wallblocka)
    elif type(agent)==Incinerator:
        return(incineratora)
    elif type(agent)==Robot:
        return(robota)
    else:
        print('Error')

grid = CanvasGrid(agent_portrayal, gridsize, gridsize, gridsize *7, gridsize *7)

#Conectar con el puerto para poder visualizar
server = ModularServer(Maze, [grid], "Robots Recolectores", {})

#El port original es 8522
server.port = 8525
server.launch()