# ARIN7102-MedAI_platform

## 🧠 Project Overview

**ARIN7102-MedAI_platform** is a web-based interactive chatbot for medication sales. Users can ask drug-related questions through the web interface, and the system retrieves relevant information from the database to provide intelligent sales suggestions.

---

## 🚀 Main Features

- 💬 Interactive medication sales chatbot
- 🔍 Retrieves relevant Q&A from a MySQL database
- 🧠 Integrates with an AI model to understand and respond to user queries
- 🖥️ Frontend-backend separated architecture

---

## 🛠 Tech Stack

- **Frontend**: Vue 3
- **Backend**: Flask
- **Database**: MySQL

---

## 📁 Database Schema

### `conversation` Table

| Field        | Type     | Null | Key | Extra          |
| ------------ | -------- | ---- | --- | -------------- |
| id           | int      | NO   | PRI | auto_increment |
| created_at   | datetime | YES  |     |                |
| last_updated | datetime | YES  |     |                |

### `message` Table

| Field           | Type | Null | Key | Extra          |
| --------------- | ---- | ---- | --- | -------------- |
| id              | int  | NO   | PRI | auto_increment |
| conversation_id | int  | NO   | MUL |                |
| question        | text | NO   |     |                |
| answer          | text | NO   |     |                |

---

## 🧪 How to Run the Project Locally

### 1. Database Setup

- Create a database named `aiask`
- Create the following two tables using the schema above: `conversation` and `message`

### 2. Backend Setup

- Navigate to the backend folder:
  ```bash
  cd backend
  ```

- Install required Python packages:
  ```bash
  pip install flask flask-cors flask-sqlalchemy openai
  ```

- Run the backend server:
  ```bash
  python app.py
  ```

### 3. Frontend Setup

- Navigate to the frontend project folder:
  ```bash
  cd user-center-frontend-vue-master
  ```

- Install dependencies and run:
  ```bash
  npm install
  npm run serve
  ```

---

## 📷 Demo Screenshots
![MedAI Chat Interface](./assets/chat.png)

---