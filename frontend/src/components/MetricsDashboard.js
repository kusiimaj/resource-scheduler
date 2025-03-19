import React, { useState, useEffect } from "react";
import axios from "axios";
import socket from "../socket"; // Import WebSocket connection

const MetricsDashboard = () => {
  const [metrics, setMetrics] = useState({
    average_wait_time: 0,
    queue_length: 0,
    agent_utilization: [],
  });

  // Fetch initial metrics data from the backend
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/status")
      .then(response => {
        setMetrics(response.data.metrics);
      })
      .catch(error => console.error("Error fetching metrics:", error));

    // WebSocket listener for real-time updates
    socket.on("metrics_update", (data) => {
      setMetrics(data);
    });

    return () => {
      socket.off("metrics_update");
    };
  }, []);

  return (
    <div className="p-4 bg-gray-100 shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">📊 System Metrics</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-3 bg-white rounded shadow">
          ⏳ <strong>Average Wait Time:</strong> {metrics.average_wait_time} sec
        </div>
        <div className="p-3 bg-white rounded shadow">
          🔄 <strong>Queue Length:</strong> {metrics.queue_length}
        </div>
        <div className="p-3 bg-white rounded shadow col-span-2">
          🏆 <strong>Agent Utilization:</strong>
          <ul className="list-disc ml-4">
            {metrics.agent_utilization.length > 0 ? (
              metrics.agent_utilization.map((utilization, index) => (
                <li key={index}>Agent {index + 1}: {utilization}%</li>
              ))
            ) : (
              <p>No data available</p>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MetricsDashboard;
