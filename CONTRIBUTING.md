# Contributing to Inopsio AI Enterprise

Thank you for contributing to the Inopsio HQ ecosystem! To maintain our "Enterprise Grade" standards, all contributions must follow these rules.

## 🏗️ Architectural Rules

1. **Strict Multi-Tenancy:** Every database query in the backend MUST use the `CRUDBase` class and include an `organization_id`. Direct database access without tenant filtering is prohibited.
2. **Type Safety:** All frontend code must use **Strict TypeScript**. No `any` types allowed.
3. **UI Consistency:** New components must be placed in `frontend/src/components/ui/` and use the `cn()` utility for styling.
4. **Backend Security:** All new API endpoints must use the dependency injection found in `app.api.deps` to verify user identity.

## 🛠️ Development Workflow

1. **Branching:** Create a feature branch (e.g., `feature/ai-chat-integration`).
2. **Linting:** Run `pnpm lint` in the frontend and ensure your Python code follows PEP8.
3. **Testing:** Ensure all `vitest` (frontend) and `pytest` (backend) suites pass.
4. **Pull Requests:** Provide a clear description of what the change does and how it affects the "Universal" nature of the kit.

## 🤖 For AI Developers

If you are an AI agent contributing to this repo:

- Always check `docs/start-here.md` before generating code.
- Ensure all environment variables are added to `frontend/src/env.ts`.
- Maintain the folder structure: Storefront (`frontend/`) and Warehouse (`backend/`).
