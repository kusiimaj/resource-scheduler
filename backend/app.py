from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets for real-time updates

# Global storage
customer_queue = []
agents = [
    {"id": 1, "name": "Agent 1", "available": True, "tasks_handled": 0, "utilization": 0, "current_customer": None},
    {"id": 2, "name": "Agent 2", "available": True, "tasks_handled": 0, "utilization": 0, "current_customer": None},
    {"id": 3, "name": "Agent 3", "available": True, "tasks_handled": 0, "utilization": 0, "current_customer": None}
]
completed_customers = []
algorithm = "round_robin"  # Default scheduling algorithm
simulation_running = False

def add_customer():
    """Simulates customer arrival with priority and service time."""
    new_customer = {
        "id": len(customer_queue) + 1,
        "priority": random.choice(["VIP", "Corporate", "Normal"]),
        "service_time": random.randint(3, 10)
    }
    customer_queue.append(new_customer)
    socketio.emit("customer_update", customer_queue)  # Real-time update

def assign_customers():
    """Assigns customers dynamically based on the selected scheduling algorithm."""
    if not customer_queue or not simulation_running:
        return

    if algorithm == "round_robin":
        round_robin_scheduling()
    elif algorithm == "priority":
        priority_scheduling()
    elif algorithm == "shortest_job":
        shortest_job_scheduling()

def round_robin_scheduling():
    """Assigns customers in a cyclic order."""
    for agent in agents:
        if agent["available"] and customer_queue:
            assign_task(agent)

def priority_scheduling():
    """Prioritizes customers based on type."""
    priority_order = {"VIP": 1, "Corporate": 2, "Normal": 3}
    customer_queue.sort(key=lambda c: priority_order[c["priority"]])
    round_robin_scheduling()

def shortest_job_scheduling():
    """Assigns shortest service time customers first."""
    customer_queue.sort(key=lambda c: c["service_time"])
    round_robin_scheduling()

def assign_task(agent):
    """Assigns a customer task to an available agent."""
    if customer_queue:
        assigned_customer = customer_queue.pop(0)
        agent["available"] = False
        agent["tasks_handled"] += 1
        agent["current_customer"] = assigned_customer
        socketio.emit("agent_update", agents)  # Real-time update

        threading.Timer(assigned_customer["service_time"], mark_agent_available, [agent["id"]]).start()

def mark_agent_available(agent_id):
    """Marks an agent as available after task completion."""
    for agent in agents:
        if agent["id"] == agent_id:
            agent["available"] = True
            agent["current_customer"] = None
            agent["utilization"] = round((agent["tasks_handled"] / max(1, len(completed_customers))) * 100, 2)
            socketio.emit("agent_update", agents)

def calculate_metrics():
    """Computes average wait time and agent utilization."""
    avg_wait_time = sum(c["service_time"] for c in completed_customers) / max(1, len(completed_customers))
    agent_utilization = [agent["utilization"] for agent in agents]
    return {
        "average_wait_time": round(avg_wait_time, 2),
        "agent_utilization": agent_utilization,
        "queue_length": len(customer_queue)
    }

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({"simulation_running": simulation_running, "metrics": calculate_metrics()})

@app.route("/api/agents", methods=["GET"])
def get_agents():
    return jsonify(agents)

@app.route("/api/agents", methods=["POST"])
def add_agent():
    new_agent = {"id": len(agents) + 1, "name": f"Agent {len(agents) + 1}", "available": True, "tasks_handled": 0, "utilization": 0, "current_customer": None}
    agents.append(new_agent)
    return jsonify({"message": "Agent added successfully!", "agents": agents})

@app.route("/api/agents/<int:agent_id>", methods=["DELETE"])
def remove_agent(agent_id):
    global agents
    agents = [agent for agent in agents if agent["id"] != agent_id]
    return jsonify({"message": f"Agent {agent_id} removed!", "agents": agents})

@app.route("/api/customers", methods=["GET"])
def get_customers():
    return jsonify(customer_queue)

@app.route("/api/simulation/start", methods=["POST"])
def start_simulation():
    global simulation_running
    simulation_running = True
    return jsonify({"message": "Simulation started!"})

@app.route("/api/simulation/pause", methods=["POST"])
def pause_simulation():
    global simulation_running
    simulation_running = False
    return jsonify({"message": "Simulation paused!"})

@app.route("/api/simulation/reset", methods=["POST"])
def reset_simulation():
    global customer_queue, agents, simulation_running
    customer_queue = []
    for agent in agents:
        agent["available"] = True
        agent["tasks_handled"] = 0
        agent["utilization"] = 0
        agent["current_customer"] = None
    simulation_running = False
    return jsonify({"message": "Simulation reset!"})

@app.route("/api/algorithm/<string:algorithm_type>", methods=["PUT"])
def change_algorithm(algorithm_type):
    global algorithm
    if algorithm_type in ["round_robin", "priority", "shortest_job"]:
        algorithm = algorithm_type
        return jsonify({"message": f"Algorithm changed to {algorithm_type}!"})
    return jsonify({"error": "Invalid algorithm type!"}), 400

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
