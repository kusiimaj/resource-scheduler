import React, { useState, useEffect } from "react";
import axios from "axios";
import socket from "../socket"; // Import WebSocket connection

const AgentList = () => {
  const [agents, setAgents] = useState([]);

  // Fetch initial agent data from the backend
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/agents")
      .then(response => {
        setAgents(response.data);
      })
      .catch(error => console.error("Error fetching agents:", error));

    // WebSocket listener for agent updates
    socket.on("agent_update", (data) => {
      setAgents(data.agents);
    });

    return () => {
      socket.off("agent_update");
    };
  }, []);

  return (
    <div className="p-4 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">👨‍💼 Active Agents</h2>
      <ul>
        {agents.length > 0 ? (
          agents.map((agent) => (
            <li key={agent.id} className="border p-2 mb-2 rounded">
              🆔 {agent.id} | {agent.name} | {agent.available ? "✅ Available" : "⏳ Busy"}
            </li>
          ))
        ) : (
          <p>No active agents</p>
        )}
      </ul>
    </div>
  );
};

export default AgentList;
