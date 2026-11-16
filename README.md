# DataCo Supply Chain Analytics Dashboard

A Django dashboard for exploring DataCo supply-chain performance, delivery risk, logistics, order forecasts, and individual order records.

## Project structure

- `config/` — Django project configuration.
- `dashboard/` — dashboard views, models, forms, URLs, migrations, and CSV import command.
- `templates/dashboard/` — dashboard and record-management templates.
- `static/` — project static assets (currently empty; Django static collection is configured).
- `data/processed/` — processed DataCo source data and analysis extracts.
- `data/forecasts/` — delivery-risk predictions and order-forecast outputs.

The project includes the source CSV (180,519 records). The local SQLite database and Windows virtual environment are deliberately excluded. The database is created from migrations and populated from the included CSV.

## Runtime

- Python 3.12.7 or another Python 3.12+ version supported by the host.
- Django 6.1.3 (the version used to generate the included migration).
- Other dependencies are listed in `requirements.txt`.

## Run locally on Windows

Open Command Prompt in the folder containing `manage.py`.

1. Create a virtual environment:

   ```bat
   py -3.12 -m venv .venv
   ```

2. Activate it:

   ```bat
   .venv\Scripts\activate
   ```

3. Install the project dependencies:

   ```bat
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env`.
5. Generate a new Django secret key:

   ```bat
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. Put the generated key in `.env` as `DJANGO_SECRET_KEY`. Keep `.env` private; it is excluded by `.gitignore`.
7. Create the database tables:

   ```bat
   python manage.py migrate
   ```

8. Import the DataCo records:

   ```bat
   python manage.py import_dataco
   ```

9. Start the development server:

   ```bat
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/`.

To create a staff account for record management:

```bat
python manage.py createsuperuser
```

The dashboard pages are public. Adding, editing, and deleting records require a staff account.

## Push this project to GitHub

Create an empty repository on GitHub. Extract this ZIP, open a terminal in the extracted `Dataco_Django_Dashboard` folder (the folder containing `manage.py`), then run:

```bash
git init
git add .
git status
git commit -m "Prepare DataCo dashboard for deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your actual GitHub repository URL. Review `git status` before committing. Do not add `.env`, `db.sqlite3`, or a virtual environment.

**Large dataset note:** `data/processed/DataCo_SupplyChain.csv` is approximately 78.7 MB. It is below GitHub's 100 MB per-file hard limit, but GitHub will warn about files above 50 MB. Use Git from your computer to push the repository; do not use the GitHub browser's file uploader for this project.

## PythonAnywhere (after GitHub)

After the GitHub push is complete, clone the repository into PythonAnywhere. Create a virtual environment using a Python version supported by your account, install `requirements.txt`, configure the WSGI file, set production environment variables, run migrations, import the CSV, run `collectstatic`, and configure the `/static/` mapping in the PythonAnywhere web app.

For the live site, configure these variables outside GitHub:

- `DJANGO_SECRET_KEY` — a new, private production key.
- `DJANGO_DEBUG=False`.
- `DJANGO_ALLOWED_HOSTS=YOUR-USERNAME.pythonanywhere.com`.
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://YOUR-USERNAME.pythonanywhere.com`.
- `DJANGO_SECURE_SSL_REDIRECT=True`.

Do not commit production secrets or the production SQLite database to GitHub.
