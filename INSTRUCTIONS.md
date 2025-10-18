# Furnace Robot Simulation — Instructions

## Requirements

- Python 3.10 (recommended)
- pip
- [virtualenv](https://virtualenv.pypa.io/en/latest/) for isolated environments

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/AlejandroMoc/Sim_FurnaceRobot
cd App_FurnaceRobot
```

### 2. Create and Activate a Virtual Environment

#### On Linux/macOS:

```sh
python3.10 -m venv venv
source venv/bin/activate
```

#### On Windows:

```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install Mesa and other required packages:

```sh
pip install -r requirements.txt
```

### 4. Running the Simulation

Start the simulation server with:

```sh
python main.py
```

This will launch a local web server. Open your browser and go to that specific port:

```
http://localhost:8526
```

You will see the interactive simulation interface.
