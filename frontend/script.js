let customerQueue = [];
let agents = [
    { id: 1, name: "Agent 1", available: true },
    { id: 2, name: "Agent 2", available: true },
    { id: 3, name: "Agent 3", available: true }
];

document.getElementById("startSimulation").addEventListener("click", function () {
    setInterval(addCustomer, 3000); // Customers arrive every 3 seconds
    setInterval(assignCustomersToAgents, 5000); // Assign customers every 5 seconds
});

function addCustomer() {
    let newCustomer = { id: customerQueue.length + 1, priority: Math.floor(Math.random() * 3) + 1 };
    customerQueue.push(newCustomer);
    updateUI();
}

function assignCustomersToAgents() {
    if (customerQueue.length === 0) return;

    let algorithm = document.getElementById("algorithm").value;

    if (algorithm === "round_robin") {
        roundRobinScheduling();
    } else if (algorithm === "priority") {
        priorityScheduling();
    } else if (algorithm === "shortest_job") {
        shortestJobScheduling();
    }

    updateUI();
}

function roundRobinScheduling() {
    let availableAgent = agents.find(agent => agent.available);
    if (availableAgent && customerQueue.length > 0) {
        availableAgent.available = false;
        let assignedCustomer = customerQueue.shift();
        setTimeout(() => {
            availableAgent.available = true;
            updateUI();
        }, 5000); // Simulate task completion in 5 seconds
    }
}

function priorityScheduling() {
    customerQueue.sort((a, b) => a.priority - b.priority);
    roundRobinScheduling();
}

function shortestJobScheduling() {
    customerQueue.sort((a, b) => a.id - b.id);
    roundRobinScheduling();
}

function updateUI() {
    let customerList = document.getElementById("customerQueue");
    customerList.innerHTML = "";
    customerQueue.forEach(customer => {
        let li = document.createElement("li");
        li.innerText = `Customer ${customer.id} (Priority: ${customer.priority})`;
        customerList.appendChild(li);
    });

    let agentList = document.getElementById("agentStatus");
    agentList.innerHTML = "";
    agents.forEach(agent => {
        let li = document.createElement("li");
        li.innerText = `${agent.name} - ${agent.available ? "Available" : "Busy"}`;
        agentList.appendChild(li);
    });
}
