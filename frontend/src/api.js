import axios from "axios";

// Base URL of the backend API
const API_BASE_URL = "http://127.0.0.1:5000";

// Create an Axios instance for API calls
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to add a customer
export const addCustomer = async () => {
  try {
    const response = await api.post("/add_customer");
    return response.data;
  } catch (error) {
    console.error("Error adding customer:", error);
  }
};

// Function to fetch agents
export const getAgents = async () => {
  try {
    const response = await api.get("/api/agents");
    return response.data;
  } catch (error) {
    console.error("Error fetching agents:", error);
  }
};

// Function to start the simulation
export const startSimulation = async () => {
  try {
    const response = await api.post("/api/simulation/start");
    return response.data;
  } catch (error) {
    console.error("Error starting simulation:", error);
  }
};

export default api;
