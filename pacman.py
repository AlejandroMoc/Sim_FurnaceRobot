from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class Ghost(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
         
    def step(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False)
        for i in next_moves:
            if type(next_moves[i]) != WallBlock:
                next_movez = next_movez.append(next_moves[i])
        print(next_moves)
        next_move = self.random.choice(next_movez)
        self.model.grid.move_agent(self, next_move)

class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class Maze(Model):
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(17, 14, torus=False)

        ghost = Ghost(self, (8, 6))
        self.grid.place_agent(ghost, ghost.pos)
        self.schedule.add(ghost)

        matrix = [
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
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

        """for _,x,y in self.grid.coord_iter():
            print(matrix[y])
            print(matrix[x])
            if matrix[y][x] == 0:
                print(f"block at ({x},{y})")
                wallblock.pos = matrix[y][x]"""
            

        for cell in self.grid.coord_iter():
            x, y = cell[1]  
            if matrix[y][x] == 0:
                wallblock = WallBlock(self, (y,x))
                #print(f"block at ({x}, {y})")
                self.grid.place_agent(wallblock, cell[1])
                self.schedule.add(wallblock)

    def step(self):
        self.schedule.step()

def agent_portrayal(agent):
    if type(agent) == Ghost:
        return {"Shape": "C:/Users/GhulRasal/Desktop/ModelAgente/PacMan/ghost.png", "Layer": 0}
    elif type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Blue", "Layer": 0}

grid = CanvasGrid(agent_portrayal, 17, 14, 450, 450)

server = ModularServer(Maze, [grid], "PacMan", {})
server.port = 8522
server.launch()