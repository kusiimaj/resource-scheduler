import React, { useState, useEffect } from "react";
import axios from "axios";
import io from "socket.io-client";
import CustomerQueue from "./CustomerQueue";
import AgentList from "./AgentList";
import MetricsDashboard from "./MetricsDashboard";
import SimulationControls from "./SimulationControls";

const socket = io("http://127.0.0.1:5000", {
  transports: ["websocket", "polling"],
});


const Dashboard = () => {
  const [customers, setCustomers] = useState([]);
  const [agents, setAgents] = useState([]);
  const [metrics, setMetrics] = useState({
    average_wait_time: 0,
    queue_length: 0,
    agent_utilization: [],
  });

  // ✅ Fetch initial data and set up WebSocket listeners
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch customer queue
        const customerResponse = await axios.get("http://127.0.0.1:5000/api/customers");
        setCustomers(customerResponse.data.customers || []);
  
        // Fetch agent list
        const agentResponse = await axios.get("http://127.0.0.1:5000/api/agents");
        setAgents(agentResponse.data || []);
  
        // Fetch system metrics
        const metricsResponse = await axios.get("http://127.0.0.1:5000/api/status");
        setMetrics(metricsResponse.data.metrics || {});
      } catch (error) {
        console.error("❌ Error fetching data:", error);
      }
    };
  
    fetchData();
  
    // WebSocket event listeners
    socket.on("customer_update", (data) => {
      setCustomers(data.customers || []);
    });
  
    socket.on("agent_update", (data) => {
      setAgents(data.agents || []);
    });
  
    socket.on("metrics_update", (data) => {
      setMetrics(data || {});
    });
  
    return () => {
      socket.off("customer_update");
      socket.off("agent_update");
      socket.off("metrics_update");
    };
  }, []);
  

  // ✅ Simulation control functions
  const startSimulation = () => {
    axios.post("http://127.0.0.1:5000/api/simulation/start");
  };

  const pauseSimulation = () => {
    axios.post("http://127.0.0.1:5000/api/simulation/pause");
  };

  const resetSimulation = () => {
    axios.post("http://127.0.0.1:5000/api/simulation/reset");
  };

  return (
    <div className="min-h-screen bg-gray-200 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">📊 Resource Scheduler Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Customer Queue */}
        <div className="md:col-span-1">
          <CustomerQueue customers={customers} />
        </div>

        {/* Metrics Dashboard */}
        <div className="md:col-span-1">
          <MetricsDashboard metrics={metrics} />
        </div>

        {/* Agent List */}
        <div className="md:col-span-1">
          <AgentList agents={agents} />
        </div>
      </div>

      {/* Simulation Controls */}
      <div className="mt-6">
        <SimulationControls
          startSimulation={startSimulation}
          pauseSimulation={pauseSimulation}
          resetSimulation={resetSimulation}
        />
      </div>
    </div>
  );
};

export default Dashboard;
