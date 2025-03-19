import React, { useState, useEffect } from "react";
import axios from "axios";

const CustomerQueue = () => {
  const [customers, setCustomers] = useState([]); // ✅ Initialize as an empty array
  const [loading, setLoading] = useState(true);

  // ✅ Fetch customers from backend
  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/customers");
      setCustomers(response.data.customers || []); // ✅ Fallback to empty array
      setLoading(false);
    } catch (error) {
      console.error("❌ Error fetching customers:", error);
      setLoading(false);
    }
  };

  // ✅ Function to start the simulation
  const startSimulation = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/api/simulation/start");
      console.log("✅ Simulation started!");
    } catch (error) {
      console.error("❌ Error starting simulation:", error);
    }
  };

  // ✅ Function to pause the simulation
  const pauseSimulation = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/api/simulation/pause");
      console.log("⏸ Simulation paused!");
    } catch (error) {
      console.error("❌ Error pausing simulation:", error);
    }
  };

  // ✅ Function to reset the simulation
  const resetSimulation = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/api/simulation/reset");
      console.log("🔄 Simulation reset!");
      fetchCustomers(); // ✅ Refresh customer queue after reset
    } catch (error) {
      console.error("❌ Error resetting simulation:", error);
    }
  };

  // ✅ Function to add a new customer
  const addCustomer = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/add_customer");
      console.log("✅ Customer added successfully!");
      fetchCustomers(); // ✅ Refresh customer queue after adding
    } catch (error) {
      console.error("❌ Error adding customer:", error);
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      

      {/* ✅ Simulation Control Buttons */}
      <div className="mt-4 space-x-2">
        <button onClick={startSimulation} className="bg-green-500 text-white px-4 py-2 rounded">
          ▶ Start Simulation
        </button>
        <button onClick={pauseSimulation} className="bg-yellow-500 text-white px-4 py-2 rounded">
          ⏸ Pause Simulation
        </button>
        <button onClick={resetSimulation} className="bg-red-500 text-white px-4 py-2 rounded">
          🔄 Reset Simulation
        </button>
        <button onClick={addCustomer} className="bg-blue-500 text-white px-4 py-2 rounded">
          ➕ Add Customer
        </button>
      </div>
    </div>
  );
};

export default CustomerQueue;
