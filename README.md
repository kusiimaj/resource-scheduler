# **Resource Scheduler - Backend & Frontend**

## Introduction
The Resource Scheduler is a web-based system designed to efficiently manage service queues using various scheduling algorithms. It ensures optimized task allocation and real-time updates using WebSockets.

## **Features**
- Real-time updates using WebSockets
- Multiple Scheduling Algorithms
- Round Robin Scheduling (Equal task distribution)
- Priority Scheduling (VIP/Corporate clients get priority)
- Shortest Job Next (Minimizing waiting time)
- REST API powered by Flask
- WebSocket Notifications for real-time user updates
- Dockerized Deployment (Both Backend & Frontend)
- Fully Responsive UI built with React & TailwindCSS
- Automated Tests to ensure reliability

## Tech Stack
### Backend
- Python (Flask)
- Flask-SocketIO for real-time WebSockets
- SQLite (Lightweight database for queue storage)
- Docker for containerization
### Frontend
- React (Component-based UI)
-TailwindCSS (Modern UI framework)
- Axios (For API communication)
- Socket.io-client (WebSocket connections)
  
## Deployment
- Docker Hub (Containerized backend & frontend)
- Render (Free cloud hosting for services)
  
## Installation & Setup
### Clone the Repository
- git clone https://github.com/kusiimaj/resource-scheduler.git
- cd resource-scheduler

## Setup Backend
  
### Using Docker
cd backend
docker build -t resource-scheduler-backend .
docker run -p 5000:5000 resource-scheduler-backend

### Without Docker
-cd backend
-python -m venv venv
-source venv/Scripts/activate  # For Windows (Use `source venv/bin/activate` on Mac/Linux)
-pip install -r requirements.txt
-python app.py

## Setup Frontend
### Using Docker
-cd frontend
-docker build -t resource-scheduler-frontend .
-docker run -p 3000:3000 resource-scheduler-frontend
### Without Docker
-cd frontend
-npm install
-npm start
## API Endpoints
Method	Endpoint	Description
- GET	/api/customers	Get current queue of customers
- GET	/api/agents	Get list of available agents
- POST	/api/add_customer	Add a new customer to the queue
- POST	/api/simulation/start	Start the scheduling simulation
- POST	/api/simulation/pause	Pause the simulation
- POST	/api/simulation/reset	Reset the simulation
## WebSocket Events
Event	-- Description
- customer_update	Sent when a new customer is added
- agent_update	Sent when agent availability changes
- metrics_update	Sent when system metrics are updated
## Automated Testing
This project includes automated tests to validate API functionality.

### Run Tests
- cd backend
- pytest tests/
Note: Ensure the backend is running before executing tests.

## Docker Deployment
### Build and Push Backend Image
- docker tag resource-scheduler-backend kusiimaj/resource-scheduler-backend:latest
- docker push kusiimaj/resource-scheduler-backend:latest
  
### Build and Push Frontend Image

- docker tag resource-scheduler-frontend kusiimaj/resource-scheduler-frontend:latest
- docker push kusiimaj/resource-scheduler-frontend:latest

### Deploy Using Docker Compose
- docker-compose up --build
- Hosted Application
Live Demo: Click Here https://resource-scheduler-e597.onrender.com/

### Contributors
- kusiimaj - Backend Developer
- ndikunoj - API Integration
- nambielinor - Frontend Developer
- hnam6 - Docker & Deployment
### Future Enhancements
- Implement user authentication
- Add an admin dashboard for monitoring queues
- Optimize scheduling algorithms with machine learning
- Introduce mobile support for agent management
  
## License
This project is open-source and available under the MIT License.

![image](https://github.com/user-attachments/assets/511fac60-315f-452e-ac74-ff672d67ccc8)
