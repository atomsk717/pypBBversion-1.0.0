# PyPBB v0.1.0

A simple, clean, phpBB-style discussion forum built with Django, designed to work without JavaScript.

**Status:** Early development release. Core features are functional, but the project is not production-hardened.

## Features

- Categories containing forums
- Forums containing topics and posts
- Public and restricted forums. Restricted forums require users to log in.
- Default categories and forums created automatically by a database migration
- User registration and login with CAPTCHA
- Moderator tools to lock and unlock topics, delete posts, and delete topics
- Confirmation pages, POST requests, and CSRF protection for moderation actions
- Role separation:
  - **Moderator:** A user in the group named exactly `Moderator`, with Staff status and Superuser status unchecked. Can moderate content without accessing Django Admin.
  - **Forum Admin:** A user with Staff status and Superuser status enabled. Has full Django Admin access and moderation privileges.
- Role badges and colored usernames in posts and the header
- Homepage status indicators:
  - Blue: Open to everyone
  - Green: Login required
- Dark theme, empty states, and success and error messages
- Zero JavaScript. The interface is designed to work with JavaScript disabled.

## Not Yet Implemented

- True staff-only forums. The current restricted-forum setting only requires users to log in.
- A custom Admin Control Panel (ACP), planned for a future iteration
- Search
- Private messages
- File attachments
- Email notifications

## Requirements

- Python 3.10 or newer
- Django 5.2.x
- pip

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/atomsk717/pypBBversion-1.0.0.git
cd pypBBversion-1.0.0
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents activation because of its execution policy, you can use Command Prompt instead:

```bat
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

On a fresh database, the migrations create the default categories and forums.

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your account.

### 6. Start the development server

```bash
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

**Important:** `runserver` is intended for local development, not public production deployment.

## Creating a Moderator

1. Log in to Django Admin at http://127.0.0.1:8000/admin/.
2. Open **Groups** and select **Add group**.
3. Set the group name to exactly `Moderator`.
4. Leave the permissions selection empty and save the group.
5. Open **Users** and select the account you want to make a moderator.
6. Add the user to the `Moderator` group.
7. Leave **Staff status** unchecked.
8. Leave **Superuser status** unchecked.
9. Save the user.

The moderator can lock and unlock topics and delete posts and topics. The moderator cannot access Django Admin.

## Creating a Forum Admin

1. Log in to Django Admin.
2. Open **Users** and select the account.
3. Enable **Staff status**.
4. Enable **Superuser status**.
5. Save the user.

This configuration grants full Django Admin access and moderation privileges.

**Security note:** Superuser accounts have extensive administrative privileges. Grant them only to trusted users.

A user with Staff status enabled but without Superuser status or the required model permissions may be able to open Django Admin but will not necessarily have permission to view or edit application data.

## Project Structure

```text
pypBBversion-1.0.0/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── forum/
│   ├── migrations/
│   ├── static/
│   │   └── forum/
│   │       └── css/
│   ├── templates/
│   │   └── forum/
│   ├── templatetags/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── .gitignore
├── manage.py
├── readme.md
└── requirements.txt
```

## Security and Deployment Notes

PyPBB v0.1.0 is an early learning project. It has not been hardened or independently audited for production use.

Before deploying it publicly:

- Replace the development `SECRET_KEY` with a strong secret supplied through an environment variable.
- Set `DEBUG = False`.
- Configure `ALLOWED_HOSTS` for your deployment.
- Use HTTPS and secure cookie settings.
- Review database, static-file, and media-file configuration.
- Review access controls, CAPTCHA implementation, and all user-submitted content handling.
- Run Django's deployment checks and follow the official deployment checklist.
- Use a production-ready web server and deployment configuration.

Never commit real credentials, production secrets, or a database containing private user information.

The `.gitignore` file excludes the local SQLite database, virtual environments, Python cache files, and other generated or private files.

## License

No open-source license has been selected yet.

Until a license is added, assume that the project is not offered under an explicit open-source license. If you intend to allow others to reuse, modify, or distribute PyPBB, choose and add an appropriate license.

## Acknowledgements

PyPBB is inspired by the traditional phpBB-style discussion forum experience and is built with Python and Django.

