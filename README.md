# Sensor Fault Detection
PROBLEM STATEMENT: The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air...

# Solution Proposed
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

# Running a GitHub Source Code Analysis
This project is a web-based code analysis assistant that lets users submit a GitHub repository URL, automatically clones the repo, processes the Python source files using LangChain, and creates embeddings with OpenAI GPT to enable intelligent code-related Q&A. It uses ChromaDB as the vector store and provides a conversational interface powered by a memory-enabled OpenAI chat model.

#### How to Run?

### Step 1-: Clone the Repository
```
git clone https://github.com/midofemi/sensor-fault-detection.git
```

### Steps 2-: Create a Virtual Environment
```
conda create -p venv python==3.7 -y
```

### Step 3-: Activate Conda environment
```
conda activate venv/
```

### Step 4-: Install requirements
```
pip install -r requirements.txt
```

### Step 5-: Start the Application
```
python main.py
```

### Visit http://localhost:8080 to interact with your PDF chatbot.


