import { io } from "socket.io-client";

// Backend WebSocket server URL
const SOCKET_SERVER_URL = "http://127.0.0.1:5000";

// Initialize WebSocket connection
const socket = io(SOCKET_SERVER_URL, {
  transports: ["websocket"], // Ensure WebSocket transport is used
});

// Event listeners for connection status
socket.on("connect", () => {
  console.log("✅ Connected to WebSocket Server");
});

socket.on("disconnect", () => {
  console.log("🔴 Disconnected from WebSocket Server");
});

// Handle incoming customer updates
socket.on("customer_update", (data) => {
  console.log("📡 Customer Update Received:", data);
});

// Handle incoming agent updates
socket.on("agent_update", (data) => {
  console.log("👨‍💼 Agent Status Update:", data);
});

// Handle incoming metrics updates
socket.on("metrics_update", (data) => {
  console.log("📊 Metrics Updated:", data);
});

export default socket;
