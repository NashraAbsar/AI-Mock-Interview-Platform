# AI Mock Interview Platform

A full-stack mock interview practice application that helps users prepare for technical interviews through topic-based questions, answer evaluation, scores, and feedback.

## Features

- **User Authentication:** Register, log in, and access protected routes using JWT authentication.
- **Interview Setup:** Choose a job role, experience level, and interview topic.
- **Question Practice:** Practice interview questions for Python, SQL, and general interviews.
- **Answer Evaluation:** Submit answers and receive scores with feedback.
- **Interview History:** Review previous interview sessions and submitted answers.
- **User-Friendly Interface:** Responsive frontend with interview setup, practice, and history screens.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL |
| Authentication | JWT |
| Tools | Git, GitHub, GitHub Desktop, VS Code |

## Project Structure

```text
AI-Mock-Interview-Platform/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── security.py
│       ├── evaluator.py
│       └── question_bank.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/NashraAbsar/AI-Mock-Interview-Platform.git
cd AI-Mock-Interview-Platform
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the project's Python dependencies. If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure your PostgreSQL connection and authentication settings.

Example placeholders:

```env
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/YOUR_DATABASE
SECRET_KEY=your_secret_key
```

Never commit your real `.env` file or credentials.

### 5. Run the application

From the project root:

```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```

Open the application at:

- Frontend: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs

## How It Works

1. Register or log in.
2. Select a job role, experience level, and interview topic.
3. Answer the generated practice questions.
4. Submit answers to receive evaluation scores and feedback.
5. Review previous sessions in Interview History.

## Current Evaluation Approach

The current answer evaluator uses rule-based checks, including answer length and relevant keywords, to provide practice scores and feedback. It is a work in progress and does not yet provide full semantic evaluation using an LLM.

## Future Improvements

- More accurate semantic answer evaluation.
- Performance analysis charts and graphs.
- Improved question generation and answer feedback.
- Additional interview topics and question sets.
- Deployment for public access.

## Author

**Nashra Absar**  
B.Tech CSE-AIML Student
