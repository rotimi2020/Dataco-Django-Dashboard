# Deploying DataCo on PythonAnywhere

This guide is for the DataCo Django dashboard in this repository. It uses the current project settings and the included `import_dataco` management command.

## Before you start

- Push the project to GitHub first.
- Create/sign in to the PythonAnywhere account you want to use for DataCo.
- A separate Gmail address used to register the PythonAnywhere account does **not** need to be added to this Django project. The app currently has no email-sending configuration.
- Use the exact website domain shown on your PythonAnywhere **Web** tab. Depending on the PythonAnywhere system, it may end in `.pythonanywhere.com` or `.eu.pythonanywhere.com`.

### Free-account limits to keep in mind

PythonAnywhere currently lists these limits for free accounts: 512 MiB disk space, one web app, one web worker, two consoles, 100 CPU seconds for console/scheduled-task work, and a one-month web-app expiry. The web app itself is not charged against the 100 CPU-second console allowance. Free accounts also have restricted outbound internet access, but GitHub is supported for Git operations.

The project includes roughly 85 MB of CSV data files, before the Python environment and the SQLite database are created. The free storage limit may be tight after installation and data import. Check the storage usage shown in your account. Avoid keeping duplicate ZIP files, database backups, or pip caches on the server. If the final app and database do not fit, the account will need more storage; do not delete source files the dashboard uses just to force it to fit.

New free accounts created after the 2026 plan changes may not include a PythonAnywhere-hosted MySQL database. This project is configured for SQLite, so a MySQL database is not required for this deployment.

## 1. Create the PythonAnywhere web app

1. Sign in to PythonAnywhere.
2. Open the **Web** tab and choose **Add a new web app**.
3. Select **Manual configuration** (do not use the Django quick-start option).
4. Choose Python **3.12** if it is offered. Django 6.1.3 supports Python 3.12 and later supported versions; PythonAnywhere's current system image lists Python 3.12 and 3.13.
5. Finish creating the web app. Keep the Web tab open so you can copy the exact domain shown there.

## 2. Clone the GitHub repository

Open a **Bash console** from the PythonAnywhere **Consoles** tab. This is a Linux console on the hosting service; it is separate from Windows CMD on your computer.

For a public GitHub repository, run:

```bash
cd ~
git clone https://github.com/YOUR-GITHUB-USERNAME/Dataco-Django-Dashboard.git
cd Dataco-Django-Dashboard
```

Replace `YOUR-GITHUB-USERNAME` with the actual GitHub username. If the repository is private, use GitHub's supported token/credential method; do not put a password or token in this guide or in a committed file.

Confirm that `manage.py` is in the current directory:

```bash
pwd
ls
```

## 3. Create the Python virtual environment and install packages

Create a virtual environment using Python 3.12:

```bash
mkvirtualenv --python=/usr/bin/python3.12 dataco-venv
```

The command normally activates the environment. Install the project dependencies without retaining a pip download cache:

```bash
pip install --no-cache-dir -r requirements.txt
```

If `mkvirtualenv` reports that Python 3.12 is unavailable, check the Python versions offered by the account's system image and use Python 3.13 if available. The selected version must match the Python version selected for the web app.

## 4. Create the production `.env` file

Generate a new secret key inside the activated virtual environment:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output. In the PythonAnywhere **Files** tab, open the project folder and create a file named `.env` in the same folder as `manage.py`. Add the following, replacing the placeholders:

```dotenv
DJANGO_SECRET_KEY=PASTE_THE_NEW_SECRET_KEY_HERE
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=YOUR-EXACT-WEB-APP-DOMAIN
DJANGO_CSRF_TRUSTED_ORIGINS=https://YOUR-EXACT-WEB-APP-DOMAIN
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_HSTS_SECONDS=0
```

For example, if the Web tab shows `mydataco.eu.pythonanywhere.com`, use that exact host in both host settings and include `https://` only in the CSRF trusted origin.

Do not add quotes around the values. Do not commit this `.env` file to GitHub. The project's `settings.py` loads `.env` automatically from the folder containing `manage.py`.

## 5. Create the database and import the data

Return to the Bash console and make sure you are in the project folder and the `dataco-venv` environment is active. Run:

```bash
python manage.py check
python manage.py migrate
python manage.py import_dataco
```

The import command reads `data/processed/DataCo_SupplyChain.csv` and imports the 180,519 source records into SQLite. It may take a while on a free account. Let it finish; do not start a second import while the first one is running.

If you need staff-only record management, create an administrator account:

```bash
python manage.py createsuperuser
```

## 6. Collect static files

Run:

```bash
python manage.py collectstatic --noinput
```

This creates the `staticfiles/` directory. It is generated on the server and is intentionally not committed to GitHub.

## 7. Configure the PythonAnywhere web app

Open the **Web** tab.

### Code and virtual environment

Set the source-code/project directory to:

```text
/home/YOUR-PYTHONANYWHERE-USERNAME/Dataco-Django-Dashboard
```

Set the working directory to the same project directory if the Web tab provides that field.

In the **Virtualenv** section, enter:

```text
/home/YOUR-PYTHONANYWHERE-USERNAME/.virtualenvs/dataco-venv
```

Replace `YOUR-PYTHONANYWHERE-USERNAME` with the username shown in your PythonAnywhere account. Do not use your Gmail address here.

### WSGI file

In the Web tab, click the link to edit the WSGI configuration file. Replace its contents with the code below, changing the username in `project_home`:

```python
import os
import sys

project_home = "/home/YOUR-PYTHONANYWHERE-USERNAME/Dataco-Django-Dashboard"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

A copy of this example is also included at `deployment/pythonanywhere_wsgi.py.example`.

### Static files mapping

In the **Static files** section, add this mapping:

| URL | Directory |
|---|---|
| `/static/` | `/home/YOUR-PYTHONANYWHERE-USERNAME/Dataco-Django-Dashboard/staticfiles` |

Replace the username in the directory path. The project currently has no separate uploaded-media workflow, so no media mapping is required.

## 8. Reload and test the live site

1. Return to the Web tab.
2. Click **Reload** for the DataCo web app.
3. Open the HTTPS website address shown on the Web tab.
4. Test the dashboard pages:
   - `/`
   - `/logistics/`
   - `/supply-chain/`
   - `/delivery-risk/`
   - `/order-forecast/`
   - `/data-records/`
5. If you created a superuser, test `/admin/` and confirm that staff-only record actions require staff login.

If the site shows an error, open the **Error log** link on the Web tab. The traceback there is the best starting point for fixing a deployment problem.

## 9. Updating the live app after a GitHub change

After you push a code change from your computer, open a PythonAnywhere Bash console and run:

```bash
cd ~/Dataco-Django-Dashboard
git pull origin main
workon dataco-venv
python manage.py migrate
python manage.py collectstatic --noinput
```

Then open the Web tab and click **Reload**. If the change does not involve models or static files, the migration and collectstatic commands may not need to be repeated, but reloading the web app is required to publish code changes.

## Troubleshooting notes

- **DisallowedHost:** check `DJANGO_ALLOWED_HOSTS` against the exact domain displayed on the Web tab, then reload.
- **CSRF verification failed:** check that `DJANGO_CSRF_TRUSTED_ORIGINS` contains the exact HTTPS origin, including any `.eu` subdomain, then reload.
- **Static files missing:** rerun `collectstatic --noinput` and verify the `/static/` mapping points to the `staticfiles` directory.
- **ModuleNotFoundError:** check that the Web tab uses `/home/USERNAME/.virtualenvs/dataco-venv` and that dependencies were installed inside that environment.
- **Disk quota exceeded:** inspect storage usage. Remove only disposable caches or duplicate files; do not remove the source CSV or forecast files because the application reads them.
- **Free account expiry:** PythonAnywhere free web apps have a one-month expiry. Follow the renewal/extension prompt on the account when it appears.

## Security reminders

- Never commit `.env`, `db.sqlite3`, passwords, secret keys, or GitHub tokens.
- Use a different, newly generated Django secret key for production.
- Keep `DJANGO_DEBUG=False` on the live site.
- Keep `DJANGO_HSTS_SECONDS=0` until HTTPS has been confirmed working. The site uses HTTPS and secure cookies when `DEBUG=False`.
