# Flask Intelligent Chatbot with DB Integration 🤖💬

A professional, real-time chat application built with **Flask**, featuring a robust **LangChain AI SQL Agent** that can safely interact with an underlying database. This project follows current best practices for Flask architecture, including the **Application Factory** pattern, and implements secure, role-based database access for the AI.

---

## 🌟 Key Features

- **Real-time Communication**: Powered by `Flask-SocketIO` for seamless, instant messaging.
- **Intelligent SQL Agent**: Leverages `LangChain` and `HuggingFace (Qwen2.5-72B)` to translate natural language into safe SQL queries.
- **Role-Based Data Access**: The AI agent only "sees" and queries tables authorized for the current user's role.
- **Professional Architecture**: Uses the Application Factory pattern to eliminate circular imports and ensure scalability.
- **Secure Authentication**: Integrated with `Flask-Login` for user session management and protected routes.
- **Database Migrations**: Managed with `Alembic` and `Flask-Migrate` for production-grade schema evolution.
- **Modern UI**: A responsive and dynamic frontend (Vue.js based) for an optimal user experience.

---

## 🏗️ Technical Architecture

This project implements a clean **Separation of Concerns** to avoid common pitfalls like circular dependencies.

### Project Structure
```bash
├── app/
│   ├── __init__.py          # Application Factory (creates Flask app)
│   ├── extensions.py        # Centralized Extension initialization (SocketIO, DB, Login)
│   ├── core/                # Core logic, auth callbacks, and configuration
│   ├── routes/              # Blueprint-based routing (AI, Auth, etc.)
│   ├── models/              # SQLAlchemy database models
│   ├── templates/           # HTML templates
│   └── static/              # CSS/JS assets
└── main.py                  # Entry point of the application
```

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Real-time**: WebSockets (Flask-SocketIO)
- **AI/LLM**: LangChain, HuggingFace Inference API
- **Migrations**: Alembic
- **Frontend**: HTML5, Vanilla CSS, JS (Vue.js)

---

## 🤖 AI Agent Implementation

The AI agent is designed with **Security First** in mind:
1. **Dynamic Schema Inspection**: On every initialization, the agent inspects the database.
2. **Access Control**: It filters available tables based on the `current_user.has_access_to_tables` property.
3. **Strict System Prompt**: Prevents the LLM from revealing technical details like table names or raw SQL queries to the end user.
4. **Response Formatting**: Uses a structured template for metrics, revenues, and counts to ensure consistency.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A HuggingFace API Token (for the AI features)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/flask-chat-bot-with-DB.git
   cd flask-chat-bot-with-DB
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   HUGGINGFACEHUB_API_TOKEN=your_token_here
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///my_database.db
   ```

5. **Initialize the Database**:
   ```bash
   flask db upgrade
   ```

6. **Run the Application**:
   ```bash
   python src/main.py
   ```

---

## 🗄️ Database Management

We use **Alembic** via `Flask-Migrate` to manage database changes.

- **Create a migration**: `flask db migrate -m "Description of changes"`
- **Apply migrations**: `flask db upgrade`
- **Rollback**: `flask db downgrade`

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author
**Mohamed Taha Essa**
- GitHub: [@Mohamed-Taha-Essa](https://github.com/Mohamed-Taha-Essa)
