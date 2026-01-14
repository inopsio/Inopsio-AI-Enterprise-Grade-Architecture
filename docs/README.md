# Project Documentation

Welcome to the **InopsioHQ** project documentation. This folder contains all knowledge, standards, and guides for the project.

> **Note:** This is a **Universal SaaS Starter Kit** designed to be a reusable foundation for building multiple SaaS products. The architecture is intentionally abstracted to support both local-first (VPS) and cloud-first (Supabase) deployments.

---

## 📚 Documentation Index

### **Architecture**
- [Why Prisma + FastAPI in One Backend?](./architecture/why-prisma-fastapi.md)
  - Explains the architectural decision
  - Benefits of the stack
  - Provider independence

### **Backend**
- [Setup Guide](./backend/setup-guide.md)
  - Installation instructions
  - Environment configuration
  - Development workflow
- [Coding Standards](./backend/standards.md)
  - Coding conventions
  - Security standards
  - Best practices

### **Frontend**
- (Coming soon)

---

## 🚀 Quick Start

### **Backend Setup**

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and API keys
   ```

3. **Initialize Prisma:**
   ```bash
   prisma generate
   prisma migrate dev
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

See [Backend Setup Guide](./backend/setup-guide.md) for detailed instructions.

---

## 📖 Key Concepts

### **Why Prisma + FastAPI?**

This project uses **FastAPI** (Python web framework) with **Prisma** (ORM) for:

- **Provider Independence** - Switch between Supabase and local PostgreSQL
- **Type Safety** - Auto-generated Python types from database schema
- **Developer Experience** - Prisma Studio, migrations, autocomplete
- **Modern Stack** - Fast, async-first, production-ready

See [Why Prisma + FastAPI](./architecture/why-prisma-fastapi.md) for full explanation.

---

## 🏗️ Project Structure

```
domain-investor/
├── backend/          # FastAPI + Prisma backend
├── frontend/         # Next.js 16 frontend
├── docs/            # This documentation
└── docker-compose.yml
```

---

## 🎯 Project Phases

### **Phase 1: Architecture & Hydration (Current)**

The project is currently in the **Architecture Phase**. The folder structure, documentation, and standards are **finalized**. We are now "hydrating" the empty files with implementation code.

**What's Complete:**
- ✅ Frontend structure (Next.js 16 with i18n)
- ✅ Backend structure (FastAPI + Prisma)
- ✅ Documentation and standards
- ✅ Security patterns defined
- ✅ Multi-tenancy architecture planned

**What's Next:**
- 🔄 Database schema (`prisma/schema.prisma`)
- 🔄 Core implementation files
- 🔄 API endpoints
- 🔄 Frontend components

**Why Empty Files?**
The empty files are **intentional architectural slots**. They represent:
- **Reserved space** for enterprise features (observability, multi-tenancy, security)
- **Consistent patterns** across multiple SaaS products built from this kit
- **Scalability commitments** (Request-ID tracking, org scoping, etc.)

This approach ensures that when you build 5 different SaaS products, they all follow the same patterns, making maintenance and scaling predictable.

---

## 💡 Documentation Value

| Documentation Area | Real-World Value for Your Kit |
| --- | --- |
| **`setup-guide.md`** | Allows a client to move from a **$5 VPS** to **Supabase** in 10 minutes. Zero code changes required. |
| **`standards.md`** | Ensures that if you build 5 different SaaS products, they all use the same security patterns, observability standards, and architectural patterns. |
| **`why-prisma-fastapi.md`** | Justifies the "Abstracted Database" principle—explains why the kit is provider-independent and how it enables rapid deployment flexibility. |

---

## 📝 Contributing

When contributing to this project:

1. **Read the standards** - See [Backend Standards](./backend/standards.md)
2. **Follow conventions** - Use established patterns
3. **Write tests** - Test your changes
4. **Update docs** - Keep documentation current

---

## 🔗 External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prisma Python Documentation](https://www.prisma.io/docs/concepts/overview/what-is-prisma)
- [Supabase Documentation](https://supabase.com/docs)

---

## 📧 Support

For questions or issues, please refer to the relevant documentation section or create an issue in the repository.
