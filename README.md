# Booking SaaS

Booking SaaS is a multi-tenant appointment management platform built for service businesses that need both an internal operations dashboard and a public-facing booking flow. The project combines a FastAPI backend, a React frontend, tenant-aware authentication, booking availability logic, and asynchronous reminder scheduling.

This repository showcases a realistic full-stack product architecture rather than an isolated CRUD demo. It includes protected backoffice workflows for staff, a public reservation experience for end customers, database migrations, automated tests, and background job orchestration.

## Product Scope

The platform is designed around a `negocio` as the tenant boundary. Each business can manage its own:

- services
- clients
- employees
- business hours
- appointments
- public booking page

The system also supports:

- tenant-scoped authentication with access token + refresh token flow
- role-based access for `admin` and `empleado`
- public booking by business slug/domain
- appointment conflict prevention
- reminder job scheduling with Celery + Redis
- automated database migrations with Alembic

## Why This Project Matters

This project reflects the kind of engineering problems found in production SaaS systems:

- tenant isolation across API and persistence layers
- role-aware access control for internal operations
- availability calculation based on business hours and existing bookings
- consistency between appointment lifecycle changes and background reminder jobs
- separation of concerns across routers, services, CRUD helpers, schemas, and models

It is intentionally organized as a maintainable backend/frontend codebase rather than a single-file prototype.

## Architecture

### Backend

- FastAPI for the HTTP API
- SQLAlchemy 2.0 for ORM and persistence
- Alembic for schema migrations
- PostgreSQL-oriented design
- Celery + Redis for background reminder scheduling
- SlowAPI for rate limiting
- Pydantic schemas and settings management

### Frontend

- React 18 + TypeScript
- Vite for tooling and bundling
- Axios for API integration
- Tailwind CSS for UI styling
- FullCalendar for agenda visualization
- Vitest and Playwright for frontend testing

## Core Workflows

### 1. Tenant onboarding

The API allows registering a business and bootstrapping its first admin user. From that point on, all protected operations are scoped to that tenant.

### 2. Internal scheduling

Authenticated staff can manage clients, services, employees, business hours, and appointments from the private application. Appointment creation and updates validate tenant ownership and reject overlapping bookings.

### 3. Public reservation flow

Each business exposes a public booking path where end users can:

- browse active services
- consult available time slots
- create a reservation without logging in

This flow is tenant-aware and checks both business hours and existing appointments before confirming a booking.

### 4. Reminder orchestration

When appointments change, reminder jobs are synchronized and scheduled for asynchronous processing. The project includes bootstrap logic to recover pending reminders on application startup.

## Engineering Highlights

- Clear layering: `Routers -> Services -> CRUD -> Models`
- Multi-tenant domain model centered on `negocio`
- Role restrictions for staff access
- Anti-overbooking logic in both private and public flows
- Persistent reminder job tracking to avoid duplicate scheduling
- Backend tests covering appointment and public booking behavior
- Frontend test split by unit, integration, and e2e scopes

## Repository Structure

```text
backend/
  app/
    core/
    crud/
    db/
    dependencies/
    events/
    models/
    routers/
    schemas/
    services/
    tasks/
  alembic/
  tests/

frontend/
  src/
  tests/

docs/
.github/
```

## Current State

This is a working professional prototype with real architectural decisions already implemented. A few pieces are still intentionally lightweight:

- notification delivery is currently simulated through a service abstraction
- the login flow currently requires `negocio_id` explicitly
- the public reservation route is consolidated in the public agenda experience

Those limitations are visible in the codebase and represent natural next steps for product hardening rather than missing fundamentals.

## Running Locally

Backend:

```bash
cd backend
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Testing

Backend:

```bash
pytest backend/tests -q
```

Frontend:

```bash
cd frontend
npm run test:unit
npm run test:integration
npm run test:e2e
```

## Author

Built by Diego Chacón as a portfolio-grade SaaS booking platform focused on practical backend architecture, product workflows, and maintainable full-stack implementation.
