# Ticket Management System (Django)

A simple **Ticket Management System** built with Django and Django REST Framework.  
Supports dynamic **role-based permissions**, hierarchical menus, ticket status & priority, and notifications.

---

## Features

- **Authentication & Authorization**

  - JWT-based login (username & password)
  - Dynamic roles: Admin, Manager, Agent, Customer
  - Role-based permissions control CRUD access on Tickets, Status, Priority, and Menus

- **Role-Based Dynamic Permissions**

  - Roles and permissions configurable from the database
  - Users inherit permissions from assigned role
  - Admin users have full access by default

- **Ticket Management**

  - Create, view, edit, delete tickets
  - Assign tickets to agents (supports reassignment)
  - Dynamic ticket status & priority management

- **Menu System**

  - 3-level hierarchical menu for ticket classification
  - Admin/Supervisor can manage menus
  - Users see only assigned menus when creating tickets

- **Notification System**
  - Logs notifications on ticket creation, update, assignment, and reassignment
  - Implemented using Django signals and in-app `NotificationLog`

---

## Tech Stack

- Python 3.13.1
- Django 5.2.5
- Django REST Framework
- PostgreSQL (or your preferred DB)
- JWT Authentication (`djangorestframework-simplejwt`)

---

## Models

- **User** – Custom user model with username password login and role
- **Role** – Defines user roles and associated permissions
- **Ticket** – Stores ticket details, assigned user, status, priority
- **TicketStatus** – Dynamic status with weight
- **TicketPriority** – Dynamic priority with weight
- **MenuLevel1/2/3** – Hierarchical menu structure
- **NotificationLog** – Stores logs for ticket notifications

---

## Folder Structure

```
├── 📁 .git/ 🚫 (auto-hidden)
├── 📁 .venv/ 🚫 (auto-hidden)
├── 📁 .vscode/ 🚫 (auto-hidden)
├── 📁 apps/
│   ├── 📁 notifications/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   ├── 📁 migrations/
│   │   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   │   ├── 🐍 0001_initial.py
│   │   │   ├── 🐍 0002_alter_notificationlog_action.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 apps.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 tests.py
│   │   └── 🐍 views.py
│   ├── 📁 tickets/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   ├── 📁 api/
│   │   │   └── 📁 v1/
│   │   │       ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   │       ├── 📁 routes/
│   │   │       │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   │       │   └── 🐍 routers.py
│   │   │       ├── 📁 serializers/
│   │   │       │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   │       │   └── 🐍 serializers.py
│   │   │       ├── 📁 viewsets/
│   │   │       │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   │       │   └── 🐍 viewsets.py
│   │   │       ├── 🐍 __init__.py
│   │   │       └── 🐍 signals.py
│   │   ├── 📁 management/
│   │   │   └── 📁 commands/
│   │   │       └── 🐍 seed_demo_data.py
│   │   ├── 📁 migrations/
│   │   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   │   ├── 🐍 0001_initial.py
│   │   │   ├── 🐍 0002_initial.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 apps.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 tests.py
│   │   └── 🐍 views.py
│   └── 📁 users/
│       ├── 📁 __pycache__/ 🚫 (auto-hidden)
│       ├── 📁 api/
│       │   └── 📁 v1/
│       │       ├── 📁 routes/
│       │       │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│       │       │   ├── 🐍 routers.py
│       │       │   └── 🐍 urls.py
│       │       ├── 📁 serializers/
│       │       │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│       │       │   └── 🐍 serializers.py
│       │       └── 📁 views/
│       │           ├── 📁 __pycache__/ 🚫 (auto-hidden)
│       │           ├── 🐍 views.py
│       │           └── 🐍 viewsets.py
│       ├── 📁 management/
│       │   └── 📁 commands/
│       │       ├── 📁 __pycache__/ 🚫 (auto-hidden)
│       │       └── 🐍 seed_roles_with_permissions.py
│       ├── 📁 migrations/
│       │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│       │   ├── 🐍 0001_initial.py
│       │   └── 🐍 __init__.py
│       ├── 🐍 __init__.py
│       ├── 🐍 admin.py
│       ├── 🐍 apps.py
│       ├── 🐍 models.py
│       ├── 🐍 tests.py
│       └── 🐍 views.py
├── 📁 ticket_mgmt_sys/
│   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   ├── 🐍 __init__.py
│   ├── 🐍 asgi.py
│   ├── 🐍 settings.py
│   ├── 🐍 urls.py
│   └── 🐍 wsgi.py
├── 📁 utils/
│   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   ├── 🐍 constants.py
│   ├── 🐍 models.py
│   ├── 🐍 pagination.py
│   ├── 🐍 permissions.py
│   ├── 🐍 services.py
│   └── 🐍 threads.py
├── 🔒 .env 🚫 (auto-hidden)
├── 📄 .env.example 🚫 (auto-hidden)
├── 🚫 .gitignore
├── 📖 README.md
├── 🐍 manage.py
├── ⚙️ pre-commit-config.yaml
└── 📄 requirements.txt
```

---

## Seed Data

Seed initial roles, permissions, and demo users using:

```bash
python manage.py seed_roles_with_permissions
```

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/SaugatMgr/Ticket-Management-System.git
cd Ticket-Management-System
```

2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt

```

4. Run migrations

```bash
python manage.py migrate
```

5. Seed initial roles, permissions, and demo users

```bash
python manage.py seed_roles_with_permissions
```

6. Seed demo data

```bash
python manage.py seed
```

7. Run the development server

```bash
python manage.py runserver

```
