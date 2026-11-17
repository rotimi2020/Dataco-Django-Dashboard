# DataCo Supply Chain Analytics Dashboard

An interactive supply chain analytics web application built with **Python and Django**. It turns the DataCo supply chain dataset into practical views of order performance, logistics, delivery risk, forecasting, and individual order records.

<p align="center">
  <a href="https://rotimi0000.pythonanywhere.com/"><strong>🌐 Open the Live Dashboard</strong></a>
  &nbsp;·&nbsp;
  <a href="https://rotimi2020.github.io/"><strong>Portfolio</strong></a>
</p>

## Live Demo

**Application:** https://rotimi0000.pythonanywhere.com/

The live application is hosted on PythonAnywhere. Visitors can explore the dashboard pages. Adding, editing, and deleting records are restricted to authorised staff users.

> The hosted demo may occasionally be unavailable during maintenance or hosting-service interruptions.

## Project Overview

The application works with approximately **180,519 DataCo supply chain records** and provides an interactive way to explore operational performance.

It brings together data analysis, visual reporting, forecasting outputs, and database-backed record management in one Django application.

## Dashboard Features

| Section | What it provides |
|---|---|
| **Executive Overview** | High-level view of supply chain and order performance |
| **Logistics** | Shipping and logistics analysis |
| **Supply Chain** | Exploration of supply chain performance and order information |
| **Delivery Risk** | Delivery-risk prediction results and model-performance metrics |
| **Order Forecast** | Forecasting outputs and order trend analysis |
| **Data Records** | Paginated access to individual records, with staff-only add, edit, and delete actions |

## Technology Stack

- **Language:** Python
- **Web framework:** Django
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript, Django templates
- **Data input and processing:** CSV and Python
- **Deployment:** PythonAnywhere
- **Version control:** Git and GitHub

## Dataset

The application uses the DataCo supply chain dataset, containing approximately **180,519 records**.

Main source file:

`data/processed/DataCo_SupplyChain.csv`

Forecasting and delivery-risk output files are stored under:

`data/forecasts/`

## Project Structure

```text
Dataco-Django-Dashboard/
├── config/                 # Django project configuration
├── dashboard/              # Models, views and application logic
├── templates/               # Dashboard templates
├── static/                  # Static assets
├── data/
│   ├── processed/           # Main processed supply chain dataset
│   └── forecasts/           # Forecasting and prediction outputs
├── deployment/              # Deployment examples
├── manage.py
├── requirements.txt
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rotimi2020/Dataco-Django-Dashboard.git
cd Dataco-Django-Dashboard
```

### 2. Create and activate a virtual environment

**Windows:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root, alongside `manage.py`. Set the required Django environment variables using `.env.example` as a guide.

Generate a new secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set the generated value as `DJANGO_SECRET_KEY` in your private `.env` file. Keep `.env` out of Git.

### 5. Create the database and import the dataset

```bash
python manage.py migrate
python manage.py import_dataco
```

The import command reads `data/processed/DataCo_SupplyChain.csv`. Make sure the dataset file is present before running the command.

### 6. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Deployment

The application is deployed on **PythonAnywhere**:

https://rotimi0000.pythonanywhere.com/

For deployment configuration and step-by-step hosting instructions, see [PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md).

## Security Notes

- Do not commit `.env`, production secret keys, passwords, or private database files.
- Keep `DJANGO_DEBUG=False` in production.
- Record-management actions are intended for authorised staff users.

## Author

**Rotimi Omosewo**

- **Portfolio:** https://rotimi2020.github.io/
- **GitHub:** https://github.com/rotimi2020
- **Project repository:** https://github.com/rotimi2020/Dataco-Django-Dashboard
- **Live dashboard:** https://rotimi0000.pythonanywhere.com/
