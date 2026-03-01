# FoundrIQ – AI Decision Intelligence Platform for Entrepreneurs

> Validate startup ideas, analyze business risks, forecast revenue, and generate AI-powered strategic reports.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🚀 Features

- **Business Idea Analyzer** – Input idea, market, budget, competitors → get validation score, risk level, SWOT
- **Revenue Forecasting** – 12-month projections with break-even analysis
- **Risk Assessment** – Visual gauge with Low/Medium/High classification
- **Strategy Roadmap** – Step-by-step execution plan with timelines
- **AI-Powered Reports** – OpenAI GPT integration with structured JSON output
- **Secure Authentication** – JWT + bcrypt, user sessions
- **Premium UI** – Glassmorphism, dark/light mode, 3D hover effects, animated charts
- **Fully Responsive** – Works on desktop, tablet, and mobile

---

## 📂 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py             # Environment config
│   ├── database.py           # SQLAlchemy async setup
│   ├── auth/
│   │   └── security.py       # JWT + bcrypt auth
│   ├── models/
│   │   ├── user.py           # User model
│   │   ├── project.py        # Business project model
│   │   └── report.py         # AI report model
│   ├── routes/
│   │   ├── auth.py           # Auth endpoints
│   │   ├── projects.py       # Project CRUD
│   │   ├── analysis.py       # AI analysis endpoints
│   │   └── dashboard.py      # Dashboard stats
│   └── services/
│       └── ai_service.py     # OpenAI integration
├── frontend/
│   ├── index.html            # Landing page
│   ├── login.html            # Login page
│   ├── signup.html           # Registration page
│   ├── dashboard.html        # User dashboard
│   ├── analyze.html          # Business idea form
│   ├── css/
│   │   └── style.css         # Complete design system
│   ├── js/
│   │   ├── theme.js          # Dark/light mode
│   │   ├── animations.js     # Scroll reveals, tilt, parallax
│   │   ├── auth.js           # Auth module
│   │   ├── charts.js         # Canvas chart library
│   │   └── dashboard.js      # Dashboard logic
│   └── assets/
├── .env                      # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Setup

### Prerequisites

- Python 3.9+
- pip

### 1. Clone & Navigate

```bash
cd "AI Decision Intelligence Platform for Entrepreneurs"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Edit `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite+aiosqlite:///./foundriq.db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 5. Run the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

### 6. Open in Browser

Navigate to **http://localhost:8000**

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Current user profile |
| GET | `/api/projects` | List user projects |
| POST | `/api/projects` | Create project |
| GET | `/api/projects/:id` | Get project + report |
| PUT | `/api/projects/:id` | Update project |
| DELETE | `/api/projects/:id` | Delete project |
| POST | `/api/analysis/:id` | Run AI analysis |
| GET | `/api/analysis/:id` | Get analysis report |
| POST | `/api/analysis/:id/strategy` | Generate strategy |
| GET | `/api/dashboard` | Dashboard stats |

---

## 🔐 Security & Best Practices

**⚠️ CRITICAL: NEVER COMMIT THESE FILES/DATA TO GITHUB:**
- `.env` files
- `node_modules/` or `venv/`
- Private keys
- API tokens (OpenAI, etc.)
- Database URLs with credentials

**Security Features Included:**
- Passwords hashed with **bcrypt**
- JWT tokens with configurable expiry
- CORS middleware configured securely
- API keys stored in `.env` (which is correctly listed in `.gitignore`)
- A `.env.example` is provided for safe onboarding
- All sensitive routes require authentication

---

## 🌙 Dark / Light Mode

Toggle between dark and light themes. Preference is saved to `localStorage` and persists across sessions.

---

## 🚀 Deployment

### Production Build

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Notes

- Set `SECRET_KEY` to a strong random value in production
- Use PostgreSQL for production: `DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/foundriq`
- Add `asyncpg` to requirements for PostgreSQL support
- Configure proper CORS origins in `main.py`

---

## 📄 License

MIT License – Built with ❤️ by FoundrIQ Team

---

## 📫 Contact

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:moyih50210@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammad-talha-6278463a1)
