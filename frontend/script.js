document.getElementById("fetchSchedule").addEventListener("click", fetchSchedule);

document.getElementById("addCustomer").addEventListener("click", function () {
    fetch("http://127.0.0.1:5000/add_customer", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            console.log("Customer Added:", data);
            fetchSchedule();
        })
        .catch(error => console.error("Error adding customer:", error));
});

function fetchSchedule() {
    let algorithm = document.getElementById("algorithm").value; // Get selected algorithm
    fetch(`http://127.0.0.1:5000/schedule?algorithm=${algorithm}`)
        .then(response => response.json())
        .then(data => {
            updateCustomerQueue(data.customers);
            updateAgentAssignments(data.agents);
        })
        .catch(error => console.error("Error fetching schedule:", error));
}

function updateCustomerQueue(customers) {
    let queueList = document.getElementById("customerQueue");
    queueList.innerHTML = "";
    customers.forEach(customer => {
        let li = document.createElement("li");
        li.innerText = `Customer ${customer.id} (Priority: ${customer.priority})`;
        queueList.appendChild(li);
    });
}

function updateAgentAssignments(agents) {
    let agentList = document.getElementById("agentAssignments");
    agentList.innerHTML = "";
    agents.forEach(agent => {
        let li = document.createElement("li");
        li.innerText = `${agent.name} - ${agent.available ? "Available" : "Serving Customer " + agent.current_customer.id}`;
        agentList.appendChild(li);
    });
}
