# 🏦 BankAssist AI – Intelligent Banking Assistant

An AI-powered banking assistant designed to simplify banking interactions using Generative AI, Large Language Models (LLMs), and intelligent tool calling.

BankAssist AI helps users get banking information, calculate loan EMIs, check loan eligibility, and access customer account information through a conversational interface.

## 🚀 Project Overview

BankAssist AI is built using Python, Streamlit, FastAPI, LangChain, LiteLLM Proxy, and Groq.

The application follows a modular architecture that separates the frontend, backend, and LLM provider integration.

It uses LiteLLM Proxy to manage model access and routing, while FastAPI handles backend requests and Streamlit provides the user interface.

## ✨ Key Features

- **AI Banking Assistant:** Ask banking-related questions using natural language.
- **Loan Interest Rates:** Retrieve home loan and personal loan interest rates.
- **EMI Calculator:** Calculate monthly loan installments based on principal, interest rate, and tenure.
- **Loan Eligibility:** Check loan eligibility using customer financial details.
- **Customer Account Information:** Retrieve sample customer account details.
- **LLM Tool Calling:** Connect the language model with banking functions.
- **Model Routing:** Use LiteLLM Proxy to route requests to configured models.
- **Fallback Model:** Configure a backup model when the primary model fails.
- **REST API:** Handle application requests through FastAPI.
- **Interactive UI:** Provide a conversational interface using Streamlit.
- **Docker Deployment:** Run the application services using Docker Compose.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend user interface |
| FastAPI | Backend REST API |
| LangChain | LLM integration and tool calling |
| LiteLLM Proxy | LLM routing and model management |
| Groq | LLM inference provider |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

## 🏗️ System Architecture

```text
             User
               |
               v
      Streamlit Frontend
         Port 8501
               |
               v
       FastAPI Backend
         Port 8001
               |
               v
       LangChain Integration
               |
               v
         LiteLLM Proxy
          Port 4000
               |
          +----+----+
          |         |
          v         v
       Primary    Backup
        Model      Model
          |         |
          +----+----+
               |
               v
          Groq Provider
               |
               v
        AI-generated Response
               |
               v
         Streamlit UI
```

## 📂 Project Structure

```text
BankAssist-AI/
│
├── assets/
│   └── northwind_logo.png
│
├── src/
│   └── s21_practice/
│       └── __init__.py
│
├── client_app.py
├── client_app_backup.py
├── api_gateway.py
├── bankassist_Ic.py
├── banking_services.py
├── router.py
│
├── config.yaml
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .dockerignore
├── .gitignore
│
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following tools:

- Python 3.12 or higher
- Docker Desktop
- Git
- Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/Sai-juttu-1/BankAssist-AI.git
```

```bash
cd BankAssist-AI
```

### 2. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
API_KEY=your_groq_api_key
LITELLM_MASTER_KEY=your_litellm_master_key
```

Keep your actual API keys private. Never upload `.env` to GitHub.

### 3. Run with Docker Compose

Build and start all services:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

### 4. Access the Application

| Service | URL |
|---|---|
| Streamlit Frontend | http://localhost:8501 |
| FastAPI Backend | http://localhost:8001 |
| FastAPI Swagger Docs | http://localhost:8001/docs |
| LiteLLM Proxy | http://localhost:4000 |

### 5. Stop the Application

```bash
docker compose down
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check backend health |
| POST | `/chat` | Send a banking question |
| POST | `/chat/stream` | Receive a streaming response |
| GET | `/sessions/{session_id}` | Retrieve session information |

## 💡 Example Banking Questions

Try asking BankAssist AI:

1. What is the interest rate for a home loan?
2. Calculate EMI for a loan of ₹10,00,000.
3. Am I eligible for a personal loan?
4. What are the available banking services?
5. Show customer account information.

## 🔐 Security Considerations

- Store API keys and credentials in environment variables.
- Never commit `.env` files to GitHub.
- Use LiteLLM Proxy for centralized LLM access.
- Validate incoming API requests.
- Use sample customer information for demonstration purposes.

**Note:** This is an educational demonstration project. It does not connect to a real banking core system or perform actual financial transactions. Customer records and banking data are sample data.

## 🔮 Future Enhancements

- Retrieval-Augmented Generation (RAG) for banking documents.
- Conversation memory and improved session management.
- Advanced authentication and authorization.
- More banking tools and services.
- Automated LLM evaluation and monitoring.
- Production deployment with enhanced security.

## 👨‍💻 Author

**Sai Kumar Juttu**

GitHub: [Sai-juttu-1](https://github.com/Sai-juttu-1)

Project Repository: [BankAssist-AI](https://github.com/Sai-juttu-1/BankAssist-AI)

---

⭐ If you find this project useful, consider giving it a star!
