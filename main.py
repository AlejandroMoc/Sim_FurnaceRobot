from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from src.models import Robot, FurnaceBlock, WallBlock, CoalBlock, Zone

gridsize = 25

def agent_portrayal(agent):

    # Define shapes for agents
    incinerator_a_shape= {"Shape": "src/img/horno.png", "Layer": 2}
    incinerator_b_shape= {"Shape": "src/img/hornoencendido.png", "Layer": 2}
    robot_a_shape = {"Shape": "src/img/steve.png", "Layer": 3}
    robot_b_shape = {"Shape": "src/img/herobrine.png", "Layer": 3}
    trash_shape = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Color": "#FFFFFF", "Layer": 0}
    wall_shape = {"Shape": "src/img/piedra.png", "Layer": 1}
    coal_shape = {"Shape": "src/img/coal.png", "Layer": 1}

    if type(agent)==WallBlock:
        return(wall_shape)

    elif type(agent)==FurnaceBlock:
        if agent.state == agent.STATE_OFF:
            return(incinerator_a_shape)
        elif agent.state == agent.STATE_ON:
            return(incinerator_b_shape)

    elif type(agent) == Robot:
        if agent.state == agent.STATE_IDLE:
            return(robot_a_shape)
        elif agent.state == agent.STATE_CARRYING:
            return(robot_b_shape)
        elif agent.state == agent.STATE_RETURNING:
            return(robot_a_shape)

    elif type(agent)==CoalBlock:
        if agent.state == agent.STATE_ON_GROUND:
            return(coal_shape)
        else:
            return(trash_shape)

def run_simulation():
    cell_pixel_size = 20
    grid = CanvasGrid(agent_portrayal, gridsize, gridsize, gridsize * cell_pixel_size, gridsize * cell_pixel_size)

    chart = ChartModule([{"Label": "Percentage of clean cells", "Color": "Black"}], data_collector_name='datacollector')

    server = ModularServer(Zone, [grid, chart], "Collector Robots", {
        "density": Slider("CoalBlock density", 0.1, 0.01, 0.1, 0.01, "CoalBlock density."),
        "sizeofmatrix": Slider("Simulation size", gridsize, 21, gridsize, 1, "Matrix size."),
        "maxsteps": Slider("Maximum steps", 4000, 0, 5000, 1, "Maximum number of steps."),
        "width": 50, "height": 50,
    })

    server.port = 8527
    server.launch()

if __name__ == "__main__":
    run_simulation()