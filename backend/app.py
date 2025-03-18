from flask import Flask, jsonify, request
import random
import threading
import time

app = Flask(__name__)

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

def assign_customers_to_agents(algorithm="round_robin"):
    """Assigns customers to agents based on the selected algorithm."""
    if not customer_queue:
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
        completed_customers.append(assigned_customer)

        # Simulate task completion
        threading.Timer(service_time, mark_agent_available, [agent["id"]]).start()

def mark_agent_available(agent_id):
    """Marks an agent as available after completing a task and updates utilization."""
    for agent in agents:
        if agent["id"] == agent_id:
            agent["available"] = True
            agent["utilization"] = round((agent["tasks_handled"] / max(1, len(completed_customers))) * 100, 2)

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

@app.route("/add_customer", methods=["POST"])
def add_new_customer():
    """Adds a new customer (triggered by frontend)."""
    add_customer()
    return jsonify({"message": "Customer added successfully!", "customers": customer_queue})

def calculate_average_wait_time():
    """Calculates the average wait time for completed customers."""
    if not completed_customers:
        return 0
    total_wait_time = sum(c["service_time"] for c in completed_customers)
    return round(total_wait_time / len(completed_customers), 2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
