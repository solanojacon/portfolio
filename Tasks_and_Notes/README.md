# :briefcase: Tasks & Notes

[![tests](https://github.com/solanojacon/portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/solanojacon/portfolio/actions/workflows/tests.yml)

A multi-user web app for managing task lists and notes, built with Django.

Each user registers, logs in and keeps their own **task lists** (tasks with due dates, stars and subtasks) and **note lists**. A user can only ever see and change their own data.

![Task list](images/tasks.png)

<br>

## :sparkles: Features

- **Accounts:** registration, login, logout and password change.
- **Tasks:**
  - organized in color-coded lists;
  - due date, star, completion and details;
  - any number of subtasks, edited on the same page as the task;
  - overdue tasks highlighted, open tasks shown first by due date.
- **Notes:** organized in color-coded lists, with a star and free text.
- **Filtering:** click a list to see only its tasks or notes.
- **Admin:** Django admin for staff users.
- **Responsive:** works on phones, where secondary columns are hidden.

| Editing a task and its subtasks | Notes |
|---|---|
| ![Task form](images/task_form.png) | ![Notes](images/notes.png) |

<br>

## :lock: Security

- **Data isolation:**
  - Every query is filtered by the logged-in user, so another user's task, note or list returns *404 Not Found*.
  - The owner of a new object is always the logged-in user, never a value sent by the browser.
  - Forms only offer the user's own lists, and any other list id is rejected.
- **Safe deletion:** deleting asks for confirmation and only happens on a POST request with a CSRF token.
- **No secrets in the code:** all secrets and environment-specific settings come from environment variables.
- **Production settings:** without `DJANGO_DEBUG=true`, the app refuses to start without a secret key, redirects to HTTPS, sends HSTS headers and uses secure cookies.
- **Tests:** the test suite covers these rules.

<br>

## :hammer_and_wrench: Stack

- **Backend:** Python 3.10+, Django 5.2 LTS, with class-based views and shared ownership mixins.
- **Frontend:** server-rendered templates with Bootstrap 5 (django-bootstrap5), and a few lines of plain JavaScript to add subtask rows.
- **Database:** SQLite locally, PostgreSQL in production (psycopg 3), configured through `DATABASE_URL`.
- **Serving:** WhiteNoise for static files and Gunicorn as the application server, ready for AWS Elastic Beanstalk.

<br>

## :rocket: Running locally

```bash
cd Tasks_and_Notes
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # local settings: debug on, SQLite
python manage.py migrate
python manage.py createsuperuser   # optional, for the admin
python manage.py runserver
```

Then open http://127.0.0.1:8000 and register a user.

**Tests:**

```bash
python manage.py test
```

<br>

## :cloud: Deploying

The app runs on any host that provides Python and environment variables. Set:

| Variable | Value |
|---|---|
| `DJANGO_SECRET_KEY` | A long random string (see `.env.example`) |
| `DJANGO_ALLOWED_HOSTS` | The site's domain, e.g. `tasks.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | The site's origin, e.g. `https://tasks.example.com` |
| `DATABASE_URL` | e.g. `postgres://user:password@host:5432/dbname` |

On **AWS Elastic Beanstalk**:

- Set these variables as environment properties.
- `.ebextensions/django.config` points to the WSGI application and runs `migrate` and `collectstatic` on each deployment.

On other hosts, run the same two commands and start the app with:

```bash
gunicorn config.wsgi
```

<br>

## :file_folder: Project structure

```
Tasks_and_Notes/
├── config/       settings, URLs, WSGI/ASGI entry points
├── core/         registration, password change, ownership mixins, shared form helpers
├── tasks/        task lists, tasks and subtasks: models, forms, views, templates, tests
├── notes/        note lists and notes: models, forms, views, templates, tests
├── templates/    base layout, shared form and delete pages, login and registration
└── static/       stylesheet and images
```

<br>

[← Back to portfolio](../README.md)
