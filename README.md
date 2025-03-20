#Resource Scheduler

##Overview

The Resource Scheduler is a real-time task scheduling application that optimizes customer service delivery by managing agent workloads using various scheduling algorithms. The application provides a dynamic environment to simulate and analyze different scheduling strategies.

##Live Deployment

The application is deployed on Render: https://rebrand.ly/resource-scheduler-hosted

Backend API: Deployed Backend URL

Frontend UI: Deployed Frontend URL

##Features

Customer Management

Dynamic customer generation with configurable arrival rates

Customer classification (VIP, Corporate, Normal)

Unique customer tracking and wait time monitoring

Customizable service requirements

Agent Management

Automatic assignment of three agents on simulation start

Ability to add or remove agents during the simulation

Real-time agent status monitoring

Workload distribution visualization

Performance metrics tracking

Scheduling Algorithms

Round Robin: Distributes tasks evenly among agents

Priority-based: Prioritizes VIP and Corporate customers

Shortest Job Next: Assigns customers with shortest service time first

Simulation Control

Start/Pause functionality

Reset/Stop capabilities

Real-time system state updates via WebSockets

System Architecture

The application follows the Model-View-Controller (MVC) architecture:

Models: Define customer, agent, and queue data structures

Views: React-based frontend for UI rendering

Controllers: Flask API handlers for business logic

Key Components

Flask Web Server (Python backend)

PostgreSQL Database (Deployed version)

WebSockets for real-time updates

Background Task Scheduler (Event-driven simulation)

Dockerized Deployment for scalable execution

API Reference

RESTful Endpoints

GET /api/status - Retrieves system status and metrics

GET /api/agents - Lists all agents

POST /api/agents - Adds a new agent

DELETE /api/agents/{id} - Removes an agent

GET /api/customers - Lists all customers in queue

POST /api/simulation/start - Starts the simulation

POST /api/simulation/pause - Pauses the simulation

POST /api/simulation/reset - Resets the simulation

PUT /api/algorithm/{algorithm_type} - Changes the scheduling algorithm

WebSocket Events

agent_update - Real-time agent status changes

customer_update - Customer queue changes

metrics_update - Performance metrics updates

Performance Metrics

The system tracks:

Average Wait Time: Time customers spend in the queue

Agent Utilization: Time agents spend actively serving vs idle

Queue Length: Number of customers waiting for service

Task Fairness: Ensures tasks are evenly distributed among agents

Customers Served: Number of customers processed within target time

User Interface

UI Components

Dashboard: Centralized control panel for managing simulation

Agent Panel: Displays agent workload and availability

Queue Monitor: Real-time visualization of waiting customers

Performance Metrics: Live charts and statistics

Installation & Running Locally

Prerequisites

Docker installed

Git installed

Node.js & npm installed

Running via Docker Compose

Clone the repository:

git clone https://github.com/kusiimaj/resource-scheduler.git
cd resource-scheduler

Start the backend & frontend services:

docker-compose up --build

Access the application:

Backend API: http://localhost:5000

Frontend UI: http://localhost:3000

Running Without Docker

Start Backend:

cd backend
python app.py

Start Frontend:

cd frontend
npm start

Deployment

The system is deployed using Render:

Backend and frontend are containerized using Docker

Automated CI/CD pipeline through GitHub

Contributors

Backend Development: [ndikunoj]

Frontend Development: [nambielinor]

Docker & Deployment: [hnam6]

Project Lead: [Kusiimaj]

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

Flask for backend development

React.js & Tailwind CSS for frontend UI

Docker & Render for deployment
![image](https://github.com/user-attachments/assets/cc6d5a36-07aa-460e-a9b8-5bfa7d300119)
![image](https://github.com/user-attachments/assets/19614a77-17a2-4a7f-995f-366834134617)
