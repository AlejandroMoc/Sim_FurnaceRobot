import math
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

gridsize = 25
robotCentral = [0,0]

def dist_between_points(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

class Robot(Agent):

    STATE_IDLE = 0
    STATE_CARRYING = 1
    STATE_RETURNING = 2

    def __init__(self, model, pos, inc, grid, id):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.iniPos = pos
        self.inc = inc
        self.last = pos
        self.grid = grid
        self.count = 0

        self.state = self.STATE_IDLE  # Initial state is IDLE
        self.id = id  # Unique robot ID
        self.basura = False
        self.direccion = [1, 1]  # Direction for movement in IDLE

        self.vueltas = 0  # Number of loops completed (for central robot)
        self.regreso = False  # Indicates if central robot is returning

        self.basuraPos = None  # Last coal block position found

        self.steps = 0  # Step counter for each robot

    def step(self):
        # Central robot's grid boundaries
        small_grid_1 = gridsize - gridsize // 2 + gridsize // 7
        small_grid_2 = gridsize // 2 - gridsize // 7
        global robotCentral

        x, y = self.pos

        if self.state == self.STATE_IDLE:

            # Bottom-left robot
            if self.id == 0:
                if x + 1 == small_grid_2 and y >= small_grid_2 and self.direccion[0] == 1:
                    if y == gridsize // 2 - 1:
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1, 1]
                elif x < gridsize // 2 and self.direccion[0] == 1:
                    next_move = (x + 1, y)
                elif x == gridsize // 2 and self.direccion[0] == 1:
                    if y == gridsize // 2 - 1:
                        return
                    elif y + 1 == small_grid_2:
                        next_move = (x - 1, y)
                        self.direccion = [-1, 1]
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1, 1]
                elif x > 1 and self.direccion[0] == -1:
                    next_move = (x - 1, y)
                elif x == 1 and self.direccion[0] == -1:
                    if y == gridsize // 2 - 1:
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [1, 1]

                self.model.grid.move_agent(self, next_move)
                self.count += 1
                self.steps += 1

            # Top-left robot
            elif self.id == 1:
                if x + 1 == small_grid_2 and y <= small_grid_1 and self.direccion[0] == 1:
                    if y == gridsize // 2:
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1, 1]
                elif x < gridsize // 2 - 1 and self.direccion[0] == 1:
                    next_move = (x + 1, y)
                elif x == gridsize // 2 - 1 and self.direccion[0] == 1:
                    if y == gridsize // 2:
                        return
                    elif y == small_grid_1:
                        next_move = (x - 1, y)
                        self.direccion = [-1, 1]
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1, 1]
                elif x > 1 and self.direccion[0] == -1:
                    next_move = (x - 1, y)
                elif x == 1 and self.direccion[0] == -1:
                    if y == gridsize // 2:
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [1, 1]

                self.model.grid.move_agent(self, next_move)
                self.count += 1
                self.steps += 1

            # Bottom-right robot
            elif self.id == 2:
                if x == small_grid_1 and y >= small_grid_2 and self.direccion[0] == 1:
                    if y == gridsize // 2:
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1, 1]
                elif x > gridsize // 2 + 1 and self.direccion[0] == 1:
                    next_move = (x - 1, y)
                elif x == gridsize // 2 + 1 and self.direccion[0] == 1:
                    if y == gridsize // 2:
                        return
                    elif y + 1 == small_grid_2:
                        next_move = (x - 1, y)
                        self.direccion = [-1, 1]
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1, 1]
                elif x < gridsize - 2 and self.direccion[0] == -1:
                    next_move = (x + 1, y)
                elif x == gridsize - 2 and self.direccion[0] == -1:
                    if y == gridsize // 2:
                        return
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [1, 1]

                self.model.grid.move_agent(self, next_move)
                self.count += 1
                self.steps += 1

            # Top-right robot
            elif self.id == 3:
                if x == small_grid_1 and y <= small_grid_1 and self.direccion[0] == 1:
                    if y == gridsize // 2 + 1:
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1, 1]
                elif x > gridsize // 2 and self.direccion[0] == 1:
                    next_move = (x - 1, y)
                elif x == gridsize // 2 and self.direccion[0] == 1:
                    if y == gridsize // 2 + 1:
                        return
                    elif y == small_grid_1:
                        next_move = (x - 1, y)
                        self.direccion = [-1, 1]
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [-1, 1]
                elif x < gridsize - 2 and self.direccion[0] == -1:
                    next_move = (x + 1, y)
                elif x == gridsize - 2 and self.direccion[0] == -1:
                    if y == gridsize // 2 + 1:
                        return
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [1, 1]

                self.model.grid.move_agent(self, next_move)
                self.count += 1
                self.steps += 1

            # Central robot
            elif self.id == 4:
                if x < small_grid_1 - (self.vueltas + 1) and self.direccion[0] == 1 and self.direccion[1] == 1:
                    next_move = (x + 1, y)
                elif x == small_grid_1 - (self.vueltas + 1) and self.direccion[1] == 1:
                    if y == small_grid_1 - (self.vueltas + 1):
                        self.direccion = [-1, -1]
                        next_move = (x - 1, y)
                    else:
                        next_move = (x, y + 1)
                        self.direccion = [-1, 1]
                elif x > small_grid_2 + self.vueltas and self.direccion[0] == -1:
                    next_move = (x - 1, y)
                elif x == small_grid_2 + self.vueltas and self.direccion[1] == -1:
                    if y == small_grid_2 + self.vueltas:
                        # Count number of loops for central robot
                        if self.vueltas == gridsize // 7 - 1:
                            self.vueltas -= 1
                            self.regreso = True
                        elif not self.regreso:
                            self.vueltas += 1
                        else:
                            self.vueltas -= 1
                            if self.vueltas == 0:
                                self.regreso = False
                        self.direccion = [1, 1]
                        next_move = (x, y)
                    else:
                        next_move = (x, y - 1)
                        self.direccion = [1, -1]

                self.model.grid.move_agent(self, next_move)
                self.count += 1
                robotCentral = next_move
                self.steps += 1

        elif self.state == self.STATE_CARRYING:
            # Robot is carrying coal block to the incinerator
            if self.inc.getState() == 1:
                next_move = (x, y)
            else:
                incinerator_node = self.inc.getPos()
                best_move = None
                best_distance = float('inf')
                possible_moves = [
                    (self.pos[0] + 1, self.pos[1]),
                    (self.pos[0] + 1, self.pos[1] + 1),
                    (self.pos[0], self.pos[1] + 1),
                    (self.pos[0] - 1, self.pos[1] + 1),
                    (self.pos[0] - 1, self.pos[1]),
                    (self.pos[0] - 1, self.pos[1] - 1),
                    (self.pos[0], self.pos[1] - 1),
                    (self.pos[0] + 1, self.pos[1] - 1)
                ]
                for move in possible_moves:
                    distance = dist_between_points(move, incinerator_node)
                    if distance < best_distance and move != robotCentral:
                        best_distance = distance
                        best_move = move
                next_move = best_move
                self.last = self.pos
                self.model.grid.move_agent(self, next_move)
                if next_move == incinerator_node:
                    self.state = self.STATE_RETURNING
                    self.inc.setState(1)
                self.count += 1
                self.steps += 1

        elif self.state == self.STATE_RETURNING:
            # Robot returns to the last coal block position
            best_move = None
            best_distance = float('inf')
            possible_moves = [
                (self.pos[0] + 1, self.pos[1]),
                (self.pos[0] + 1, self.pos[1] + 1),
                (self.pos[0], self.pos[1] + 1),
                (self.pos[0] - 1, self.pos[1] + 1),
                (self.pos[0] - 1, self.pos[1]),
                (self.pos[0] - 1, self.pos[1] - 1),
                (self.pos[0], self.pos[1] - 1),
                (self.pos[0] + 1, self.pos[1] - 1)
            ]
            for move in possible_moves:
                distance = dist_between_points(move, self.basuraPos)
                if distance < best_distance and (move != robotCentral or self.id == 4):
                    best_distance = distance
                    best_move = move
            next_move = best_move
            self.last = self.pos
            self.model.grid.move_agent(self, next_move)
            if next_move == self.basuraPos:
                self.state = self.STATE_IDLE
            self.count += 1
            self.steps += 1

    def getPos(self):
        return self.pos

    def getSteps(self):
        return self.steps

    def setBasura(self, pos):
        self.basuraPos = pos

    def setState(self, estado):
        if estado == 0:
            self.state = self.STATE_IDLE
        elif estado == 1:
            self.state = self.STATE_CARRYING
        else:
            self.state = self.STATE_RETURNING

    def getState(self):
        return self.state

class FurnaceBlock(Agent):

    STATE_OFF = 0
    STATE_ON = 1

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.state = self.STATE_OFF
        self.timer = 0

    def step(self):
        if self.state == self.STATE_ON:
            self.timer += 1

            if self.timer == 5:
                self.state = self.STATE_OFF
                self.timer = 0

    def setState(self, state):
        if state == 0:
            self.state = self.STATE_OFF
        elif state == 1:
            self.state = self.STATE_ON

    def getState(self):
        return self.state

    def getPos(self):
        return self.pos

class Floor(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class CoalBlock(Agent):
    STATE_COLLECTED = 0
    STATE_ON_GROUND = 1

    def __init__(self, model: Model, pos, robots):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.robots = robots
        self.state = self.STATE_ON_GROUND

    def step(self):
        for robot in self.robots:
            if self.pos == robot.getPos() and self.state == self.STATE_ON_GROUND and robot.getState() == 0:
                robot.setBasura(self.pos)
                self.state = self.STATE_COLLECTED
                robot.setState(1)

    def getPos(self):
        return self.pos

class Zone(Model):

    def __init__(self, height=50, width=50, density=0.6, sizeofmatrix=gridsize, maxsteps=100):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.sizeofmatrix = sizeofmatrix
        self.maxsteps = maxsteps
        self.recorridoTerminado = False

        # Update global gridsize if changed via slider
        global gridsize
        gridsize = sizeofmatrix

        # Initial positions

        # FurnaceBlock is placed at the center
        incineratorposition = (sizeofmatrix // 2, sizeofmatrix // 2)

        robot_positions = [
            (1, 1),
            (1, self.sizeofmatrix - 2),
            (self.sizeofmatrix - 2, 1),
            (self.sizeofmatrix - 2, self.sizeofmatrix - 2),
            (self.sizeofmatrix // 2 - self.sizeofmatrix // 7, self.sizeofmatrix // 2 - self.sizeofmatrix // 7)
        ]

        self.grid = MultiGrid(self.sizeofmatrix, self.sizeofmatrix, torus=False)

        # Build the matrix for the environment
        self.matrix = []
        j = 0
        for i in range(self.sizeofmatrix):
            if i == 0 and j == 0:
                self.matrix.append([0] * self.sizeofmatrix)
            elif i == self.sizeofmatrix - 1 and j == self.sizeofmatrix - 1:
                self.matrix.append([0] * self.sizeofmatrix)
            else:
                self.matrix.append([1] * (self.sizeofmatrix - 2))
                self.matrix[i].insert(0, 0)
                self.matrix[i].insert(self.sizeofmatrix, 0)
            j += 1

        # Place Floor and WallBlock agents based on the matrix
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.matrix[y][x] == 1:
                    block = Floor(self, (x, y))
                    self.grid.place_agent(block, block.pos)
                if self.matrix[y][x] == 0:
                    block2 = WallBlock(self, (x, y))
                    self.grid.place_agent(block2, block2.pos)

        # Place the FurnaceBlock at the center
        incinerator = FurnaceBlock(self, incineratorposition)
        self.grid.place_agent(incinerator, incinerator.pos)
        self.schedule.add(incinerator)

        # Spawn Robots at their initial positions
        robot1 = Robot(self, robot_positions[0], incinerator, self.matrix, 0)
        robot2 = Robot(self, robot_positions[1], incinerator, self.matrix, 1)
        robot3 = Robot(self, robot_positions[2], incinerator, self.matrix, 2)
        robot4 = Robot(self, robot_positions[3], incinerator, self.matrix, 3)
        robot5 = Robot(self, robot_positions[4], incinerator, self.matrix, 4)
        self.robot_list = [robot1, robot2, robot3, robot4, robot5]

        # Randomly place CoalBlock agents on Floor cells based on density
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.random.random() < density:
                    if self.matrix[y][x] == 1:
                        basura = CoalBlock(self, (x, y), self.robot_list)
                        self.grid.place_agent(basura, (x, y))
                        self.schedule.add(basura)

        # Place and schedule robots
        for robot in self.robot_list:
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)

        # DataCollector to track percentage of clean cells
        self.datacollector = DataCollector({
            "Clean cells percentage": lambda m: self.count_type(m, CoalBlock.STATE_ON_GROUND, self.sizeofmatrix)
        })

    @staticmethod
    def count_type(model, state, sizeofmatrix):
        count = 0
        total_cells = sizeofmatrix * sizeofmatrix
        for agent in model.schedule.agents:
            if hasattr(agent, 'state') and agent.state == state:
                count += 1
        clean_cells = total_cells - count
        clean_percentage = (clean_cells / total_cells) * 100
        if clean_percentage == 100:
            model.recorridoTerminado = True
        return clean_percentage

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # Stop if max steps reached or all cells are clean
        if self.schedule.steps == self.maxsteps or self.recorridoTerminado:
            print("Execution time:", self.schedule.steps)
            self.running = False

