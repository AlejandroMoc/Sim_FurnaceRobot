# Importación de librerías
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import math

#posiciones iniciales de los agentes
pacmanposition=(8, 7)
ghostposition1=(10,12)


#Funcion distancia
def distancia_entre_puntos(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Clase fantasma
class Ghost(Agent):
    def __init__(self, model, pos, pac):
        super().__init__(model.next_id(), model)
        self.pos = pos
        #Agregado
        self.radio = 1.0
        self.pac = pac
        self.last = pos

    def step(self):
        
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

        mejor_movimiento = None
        mejor_distancia = float('inf')  # Inicializar con un valor muy grande
        pacmannode = self.pac.getPos()

        for movim in posiblemovs:
            distancia = distancia_entre_puntos(movim, pacmannode)
            if distancia < mejor_distancia and movim != self.last:
                mejor_distancia = distancia
                mejor_movimiento = movim

        next_move = mejor_movimiento
        self.last = self.pos 
        self.model.grid.move_agent(self, next_move)
        
class Pacman(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.radio = 1

    def step(self):
        #Descomentar para que el pacman se mueva aleatoriamente
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
    #Retorna posicion actual
    def getPos(self):
        return self.pos
        

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
        self.grid = MultiGrid(17, 14, torus=False)

        #Matriz del laberinto
        self.matrix = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
            [0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,1,0],
            [0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0],
            [0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0],
            [0,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0],
            [0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0],
            [0,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,0],
            [0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0],
            [0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0],
            [0,1,0,1,0,1,0,1,1,1,0,0,0,1,0,1,0],
            [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        
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
                         #Spawnear Pacman en el centro
        pacman = Pacman(self, pacmanposition)
        self.grid.place_agent(pacman, pacman.pos)
        self.schedule.add(pacman)

        #Spawnear Ghost
        ghost = Ghost(self, ghostposition1, pacman)
        self.grid.place_agent(ghost, ghost.pos)
        self.schedule.add(ghost)

    def step(self):
        self.schedule.step()

def agent_portrayal(agent):
    
    #Definir presets
    wallblocka = {"Shape": "rect", "w": 1.1, "h":1.1, "Filled": "true", "Color": "#1543e6", "Layer": 1}
    pacmana={"Shape": "circle", "r": 1, "Filled": "true", "Color": "Orange", "Layer": 0}
    ghosta = {"Shape": "ghost.png", "Layer": 1}
    pisoa = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#e0ecff", "Layer": 0}

        
    if type(agent)==Piso:
        return(pisoa)
    elif type(agent)==WallBlock:
        return(wallblocka)
    elif type(agent)==Pacman:
        return(pacmana)
    elif type(agent)==Ghost:
        return(ghosta)
    else:
        print('Error')

grid = CanvasGrid(agent_portrayal, 17, 14, 450, 450)

#Conectar con el puerto para poder visualizar
server = ModularServer(Maze, [grid], "PacMan", {})

#El port original es 8522
server.port = 8525
server.launch()