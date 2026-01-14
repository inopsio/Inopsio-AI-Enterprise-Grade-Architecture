# 🚀 Start Here: Inopsio AI Enterprise Architecture

> **Your SaaS boilerplate.** Clone this repo and build any SaaS product on top of it.

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites

- **Node.js 20+** (for frontend)
- **Python 3.12+** (for backend)
- **PostgreSQL 15+** (any version 15, 16, 17, 18+ works)
- **Git** (version control)

---

### Step 1: Clone & Setup Environment

```bash
# Clone the repository
git clone <your-repo-url> my-saas
cd my-saas

# Copy environment templates
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
```

---

### Step 2: Configure Environment Variables

#### Frontend (`frontend/.env`)

```env
NEXT_PUBLIC_APP_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

#### Backend (`backend/.env`)

```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/inopsio_db"
SECRET_KEY="change-this-to-a-secure-random-string"
CORS_ORIGINS=["http://localhost:3000"]
```

> ⚠️ **Important:** Create your PostgreSQL database first:
>
> ```bash
> createdb inopsio_db
> ```

---

### Step 3: Install & Run Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
prisma generate

# Run database migrations
prisma db push

# Start the server
fastapi dev app/main.py
```

✅ **Backend running at:** http://localhost:8000  
📖 **API Docs at:** http://localhost:8000/docs

---

### Step 4: Install & Run Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ **Frontend running at:** http://localhost:3000

---

## 📁 Project Structure

```
my-saas/
├── frontend/          # Next.js 16 + React 19 + TypeScript
│   ├── src/
│   │   ├── app/       # Pages and routes
│   │   ├── components/# Reusable UI components
│   │   ├── lib/       # API client, auth, utilities
│   │   ├── types/     # TypeScript type definitions
│   │   └── middleware.ts  # Route protection
│   └── package.json
│
├── backend/           # FastAPI + Prisma + Python 3.12
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Config, security
│   │   ├── crud/      # Database operations
│   │   ├── schemas/   # Pydantic models
│   │   └── main.py    # App entry point
│   ├── prisma/
│   │   └── schema.prisma  # Database schema
│   └── requirements.txt
│
└── docs/              # Documentation
```

---

## 🔌 Frontend ↔ Backend Connection

The integration layer is ready:

| File                              | Purpose                                   |
| --------------------------------- | ----------------------------------------- |
| `frontend/src/lib/api.ts`         | HTTP client with JWT auth                 |
| `frontend/src/lib/auth.ts`        | Login, logout, token management           |
| `frontend/src/middleware.ts`      | Protects `/dashboard` and `/admin` routes |
| `frontend/src/types/api-types.ts` | TypeScript mirrors of Pydantic models     |

---

## 🏗️ Building Your SaaS

### Add a New Feature

1. **Backend:** Create `backend/app/api/v1/endpoints/your-feature.py`
2. **Backend:** Add Pydantic schema in `backend/app/schemas/your-feature.py`
3. **Frontend:** Add TypeScript types in `frontend/src/types/api-types.ts`
4. **Frontend:** Create page in `frontend/src/app/[locale]/(platform)/your-feature/page.tsx`

### Add a Database Model

1. Edit `backend/prisma/schema.prisma`
2. Run `prisma db push` (development) or `prisma migrate dev` (production)
3. Run `prisma generate` to update the client

---

## 🛠️ Tech Stack

| Layer              | Technology   | Version |
| ------------------ | ------------ | ------- |
| Frontend Framework | Next.js      | 16.1    |
| UI Library         | React        | 19.2    |
| Styling            | Tailwind CSS | 4.x     |
| Backend Framework  | FastAPI      | 0.115+  |
| Database ORM       | Prisma       | 0.15+   |
| Database           | PostgreSQL   | 15+     |
| Auth               | JWT + bcrypt | —       |

---

## 📚 More Documentation

| Document                                                    | Description                    |
| ----------------------------------------------------------- | ------------------------------ |
| [Architecture Decision](architecture/why-prisma-fastapi.md) | Why we chose Prisma + FastAPI  |
| [Backend Standards](backend/standards.md)                   | Coding conventions for backend |

---

## ❓ Common Issues

### "Cannot find module 'next/server'"

Run `npm install` in the frontend directory.

### "Database connection failed"

Make sure PostgreSQL is running and `DATABASE_URL` is correct.

### "CORS error in browser"

Verify `CORS_ORIGINS` in backend `.env` includes your frontend URL.

---

**Ready to build!** 🎉
