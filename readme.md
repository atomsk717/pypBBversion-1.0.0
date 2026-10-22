# PyPBB v0.1.0

Initial development release of a simple, clean, phpBB-style discussion forum built with Django.

**Status:** Early working prototype. Core features are functional. Not production-hardened.

## Features

- Categories containing forums
- Forums containing topics and posts
- Public and restricted forums (restricted = login required)
- Default categories and forums created automatically on first migration
- User registration and login with CAPTCHA
- Moderator tools: lock/unlock topics, delete posts and topics (confirmation pages + POST + CSRF)
- Role separation:
  - **Moderator** — group named exactly `Moderator`, Staff status unchecked → can moderate, no admin access
  - **Forum Admin** — Staff status + Superuser status → full Django Admin access
- Role badges and colored usernames visible on posts and in the header
- Status dots on the home page (blue = open to everyone, green = registered users only) with a legend
- Dark theme, empty states, success and error messages
- Zero JavaScript (works with JavaScript disabled)

## Not yet implemented

- True staff-only forums (the current restricted flag only checks whether the user is logged in)
- Custom Admin Control Panel (planned for a later iteration)
- Search, private messages, file attachments, email notifications

## Requirements

- Python 3.10 or newer
- Django 5.2.x

## Installation

1. Clone the repository and enter the project folder.

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
Install dependencies:Bashpip install -r requirements.txt
Apply migrations (this also creates the default categories and forums):Bashpython manage.py migrate
Create the first superuser:Bashpython manage.py createsuperuser
Run the development server:Bashpython manage.py runserver
Open http://127.0.0.1:8000/ in your browser.Creating a Moderator
Log in to the admin site at http://127.0.0.1:8000/admin/
Go to Groups → Add group
Name the group exactly Moderator
Leave the permissions box empty and save
Go to Users, open the user you want to make a moderator, and add them to the Moderator group
Leave Staff status unchecked
Leave Superuser status unchecked
Save
That user can lock/unlock topics and delete posts/topics, but cannot access the admin site.Creating a Forum Admin
Go to Users and open the user
Check Staff status
Check Superuser status
Save
That user has full access to the Django Admin and can also moderate.Note: Checking only Staff status (without Superuser status or explicit permissions) allows the user to open the admin site but shows “You don’t have permission to view or edit anything.”Project structure
forum/ — models, views, templates, static files, and template tags for the forum
accounts/ — registration, login (with CAPTCHA), and logout
config/ — project settings and root URL configuration
Notes
The SECRET_KEY in config/settings.py is the default development key. Do not use it in production.
This is an early learning project. Review Django’s deployment checklist before any public deployment.
db.sqlite3, virtual environments, and Python cache files are excluded via .gitignore.
LicenseAdd your preferred open-source license here.textSave the file. After that you can run the git commands from the previous message to upload the project.
