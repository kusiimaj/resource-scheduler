import eventlet
eventlet.monkey_patch()  # ✅ Patch before any imports

from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_socketio import SocketIO
from flask_socketio import emit
import random
import threading
import time
import sqlite3



app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Scheduler API is running!"})

simulation_running = False  # ✅ Define it globally

socketio = SocketIO(app, cors_allowed_origins="*",async_mode="eventlet")
@socketio.on("connect")
def handle_connect():
    print("✅ WebSocket Client Connected")
    emit("server_message", {"message": "Connected to WebSocket Server!"})

@socketio.on("disconnect")
def handle_disconnect():
    print("🔴 WebSocket Client Disconnected")



@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Retrieve all logged events."""
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    conn.close()
    return jsonify({"logs": [{"id": log[0], "event": log[1], "timestamp": log[2]} for log in logs]})
def log_event(event):
    """
    Log an event into the database.
    """
    
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (event) VALUES (?)', (event,))
    conn.commit()
    conn.close()

def init_db():
    """
    Initialize the database with necessary tables.
    """
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

    #  Log that the database has been initialized
    log_event("Database initialized")

algorithm = "round_robin"  # ✅ Default scheduling algorithm


def notify_clients():
    """Send real-time updates to frontend using WebSockets."""
    socketio.emit("customer_update", {"customers": customer_queue})
    socketio.emit("agent_update", {"agents": agents})
    socketio.emit("metrics_update", {
        "average_wait_time": calculate_average_wait_time(),
        "queue_length": len(customer_queue),
        "agent_utilization": [a["utilization"] for a in agents]
    })
    print("✅ WebSocket Sent: All Updates")



@app.route("/api/algorithm/<string:algorithm_type>", methods=["PUT"])
def change_algorithm(algorithm_type):
    global algorithm
    if algorithm_type in ["round_robin", "priority", "shortest_job"]:
        algorithm = algorithm_type
        # ✅ Log algorithm change
        log_event(f"Scheduling algorithm changed to {algorithm_type}")

        return jsonify({"message": f"Algorithm changed to {algorithm_type}!"})
    return jsonify({"error": "Invalid algorithm type!"}), 400

###  System Status Route ###
@app.route("/api/status", methods=["GET"])
def get_status():
    """Returns system status and performance metrics."""
    return jsonify({
        
        "simulation_running": simulation_running,
        
        "metrics": {
            "average_wait_time": calculate_average_wait_time(),
            "agent_utilization": [a["utilization"] for a in agents],
            "queue_length": len(customer_queue)
        }
    })

###  Agent Management Routes ###
@app.route("/api/agents", methods=["GET"])
def get_agents():
    """Returns a list of all agents."""
    return jsonify(agents)

@app.route("/api/agents", methods=["POST"])
def add_agent():
    """Dynamically adds a new agent."""
    new_agent = {"id": len(agents) + 1, "name": f"Agent {len(agents) + 1}", "available": True, "tasks_handled": 0, "utilization": 0}
    agents.append(new_agent)
    # ✅ Log agent addition
    log_event(f"Agent {new_agent['id']} added")
    return jsonify({"message": "Agent added successfully!", "agents": agents})

@app.route("/api/agents/<int:agent_id>", methods=["DELETE"])
def remove_agent(agent_id):
    """Removes an agent by ID."""
    global agents
    agents = [agent for agent in agents if agent["id"] != agent_id]
    # ✅ Log agent removal
    log_event(f"Agent {agent_id} removed")
    return jsonify({"message": f"Agent {agent_id} removed!", "agents": agents})

### ✅ Simulation Control Routes ###
@app.route("/api/simulation/start", methods=["POST"])
def start_simulation():
    """Starts the simulation with WebSockets enabled."""
    global simulation_running
    simulation_running = True
    # ✅ Log simulation start
    log_event("Simulation started")

    

    threading.Thread(target=auto_assign_customers, daemon=True).start()
    notify_clients()
    return jsonify({"message": "Simulation started!"})


@app.route("/api/simulation/pause", methods=["POST"])
def pause_simulation():
    """Pauses the simulation."""
    global simulation_running
    simulation_running = False
    # ✅ Log simulation pause
    log_event("Simulation paused")

    return jsonify({"message": "Simulation paused!"})

@app.route("/api/simulation/reset", methods=["POST"])
def reset_simulation():
    """Resets the simulation and clears the queue."""
    global customer_queue, simulation_running
    customer_queue = []
    for agent in agents:
        agent["available"] = True
        agent["tasks_handled"] = 0
        agent["utilization"] = 0
    simulation_running = False
    # ✅ Log simulation reset
    log_event("Simulation reset")

    # ✅ Notify all clients that the simulation has been reset
    notify_clients()

    return jsonify({"message": "Simulation reset!"})


# Global storage
customer_queue = []
agents = [
    {"id": 1, "name": "Agent 1", "available": True, "tasks_handled": 0, "utilization": 0},
    {"id": 2, "name": "Agent 2", "available": True, "tasks_handled": 0, "utilization": 0},
    {"id": 3, "name": "Agent 3", "available": True, "tasks_handled": 0, "utilization": 0}
]
completed_customers = []  # Track completed tasks

def add_customer():
    """Simulates customer arrival with random priority and service time."""
    new_customer = {
        "id": len(customer_queue) + 1,
        "priority": random.choice(["VIP", "Corporate", "Normal"]),
        "service_time": random.randint(3, 10)  # Random service time between 3-10 seconds
    }
    customer_queue.append(new_customer)

    # ✅ Emit WebSocket Event: Customer Queue Update
    socketio.emit("customer_update", {"customers": customer_queue})
    print("✅ WebSocket Sent: Customer Update")

    # ✅ Assign the customer to an agent immediately if available
    assign_customers_to_agents(algorithm)

    # ✅ Notify all clients
    notify_clients()

    # ✅ Log the event
    log_event(f"New customer added: {new_customer}")




def assign_customers_to_agents(algorithm="round_robin"):
    """Assigns customers to agents based on the selected algorithm."""
    if not customer_queue:
        print("⚠️ No customers in queue to assign!")
        return

    if algorithm == "round_robin":
        round_robin_scheduling()
    elif algorithm == "priority":
        priority_scheduling()
    elif algorithm == "shortest_job":
        shortest_job_scheduling()

def round_robin_scheduling():
    """Assigns customers in a round-robin manner, ensuring fair workload distribution."""
    for agent in agents:
        if agent["available"] and customer_queue:
            assign_task_to_agent(agent)

def priority_scheduling():
    """Processes VIP first, then Corporate, then Normal customers."""
    priority_order = {"VIP": 1, "Corporate": 2, "Normal": 3}
    customer_queue.sort(key=lambda c: priority_order[c["priority"]])
    round_robin_scheduling()

def shortest_job_scheduling():
    """Processes customers with shortest service time first."""
    customer_queue.sort(key=lambda c: c["service_time"])
    round_robin_scheduling()

def assign_task_to_agent(agent):
    """Assigns a customer task to an available agent and schedules completion."""
    if customer_queue:
        assigned_customer = customer_queue.pop(0)
        agent["available"] = False
        agent["tasks_handled"] += 1
        service_time = assigned_customer["service_time"]

        # ✅ Emit WebSocket Event: Agent Assigned Task
        socketio.emit("agent_update", {"agents": agents})
        print("✅ WebSocket Sent: Agent Update")

        # ✅ Emit WebSocket Event: Metrics Updated
        socketio.emit("metrics_update", {
            "average_wait_time": calculate_average_wait_time(),
            "queue_length": len(customer_queue),
            "agent_utilization": [a["utilization"] for a in agents]
        })
        print("📊 WebSocket Sent: Metrics Update")

        # ✅ Log agent assignment
        log_event(f"Customer {assigned_customer['id']} assigned to {agent['name']}")

        # ✅ Notify all connected clients about updated state
        notify_clients()

        # ✅ Schedule agent availability reset
        threading.Timer(service_time, mark_agent_available, [agent["id"]]).start()


def mark_agent_available(agent_id):
    """Marks an agent as available after completing a task and updates utilization."""
    for agent in agents:
        if agent["id"] == agent_id:
            agent["available"] = True
            agent["utilization"] = round((agent["tasks_handled"] / max(1, len(completed_customers))) * 100, 2)
            
            # ✅ Emit WebSocket Event: Agent Availability Update
            socketio.emit("agent_update", {"agents": agents})
            print("✅ WebSocket Sent: Agent Update")

            # ✅ Immediately assign the next customer if available
            assign_customers_to_agents(algorithm)

            # ✅ Notify all clients after the agent becomes available
            notify_clients() 

            # ✅ Log the agent's availability
            log_event(f"Agent {agent['id']} is now available")



@app.route("/schedule", methods=["GET"])
def get_schedule():
    """Returns current customer queue and agent status, updating every 5 seconds."""
    algorithm = request.args.get("algorithm", "round_robin")
    assign_customers_to_agents(algorithm)
    return jsonify({
        "customers": customer_queue,
        "agents": agents,
        "metrics": {
            "average_wait_time": calculate_average_wait_time(),
            "agent_utilization": [a["utilization"] for a in agents]
        }
    })
@app.route("/api/customers", methods=["GET"])
def get_customers():
    """Returns the list of customers currently in the queue."""
    return jsonify({"customers": customer_queue})

@app.route("/add_customer", methods=["POST"])
def add_new_customer():
    """Adds a new customer (triggered by frontend) and notifies the frontend."""
    add_customer()
    notify_clients()
    log_event("New customer added")  # ✅ Log this event
    socketio.emit("customer_update", {"event": "customer_update", "data": customer_queue})
    return jsonify({"message": "Customer added successfully!", "customers": customer_queue})

def calculate_average_wait_time():
    """Calculates the average wait time for completed customers."""
    if not completed_customers:
        return 0
    total_wait_time = sum(c["service_time"] for c in completed_customers)
    return round(total_wait_time / len(completed_customers), 2)
def auto_assign_customers():
    """Automatically assigns customers based on selected scheduling algorithm."""
    while simulation_running:
        assign_customers_to_agents(algorithm)
        time.sleep(5)  # Assign every 5 seconds



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
