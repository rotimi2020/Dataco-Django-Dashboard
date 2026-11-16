# DataCo Supply Chain Analytics Dashboard

A web-based analytics dashboard built with Django to explore supply chain operations, delivery performance, logistics, and order trends using the DataCo dataset.

The project brings together data analysis and web development to make supply chain information easier to explore, understand, and manage.

## Overview

The dashboard provides an interactive way to examine supply chain performance and work with individual order records.

It covers:

- Supply chain and order performance
- Delivery risk analysis
- Logistics and shipping information
- Order forecasting
- Individual order record management

The application uses the DataCo supply chain dataset, containing approximately 180,519 records.

## Technology Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Data processing:** Python and CSV
- **Frontend:** HTML, CSS, JavaScript and Django templates
- **Analytics:** Supply chain analysis and forecasting outputs

## Project Structure

```text
Dataco_Django_Dashboard/
│
├── config/                 # Django project configuration
├── dashboard/              # Application logic, models and views
├── templates/               # Dashboard templates
├── static/                  # Static assets
├── data/
│   ├── processed/           # Processed supply chain data
│   └── forecasts/           # Forecasting and prediction outputs
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

### Requirements

- Python 3.12 or a compatible version
- pip
- Git (if cloning the repository)

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Dataco-Django-Dashboard.git
```

Move into the project directory:

```bash
cd Dataco-Django-Dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Configuration

Copy `.env.example` to `.env` and configure the Django environment variables.

Generate a new secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add the generated value to `.env` as `DJANGO_SECRET_KEY`.

Keep your `.env` file private.

### Database Setup

Run the migrations:

```bash
python manage.py migrate
```

Import the DataCo dataset:

```bash
python manage.py import_dataco
```

### Run the Application

Start the local development server:

```bash
python manage.py runserver
```

Open the dashboard at:

http://127.0.0.1:8000/

To create an administrator account:

```bash
python manage.py createsuperuser
```

Dashboard pages are publicly accessible. Staff permissions are required for adding, editing, and deleting records.

## Dataset

The project includes the DataCo supply chain CSV dataset with approximately 180,519 records.

Main dataset:

`data/processed/DataCo_SupplyChain.csv`

The dataset is approximately 78.7 MB.

## Deployment

The application is prepared for deployment using PythonAnywhere. Production configuration requires environment variables, database setup, static-file configuration, and the Django WSGI application.

Production secrets and database files should not be committed to the repository.

## Author

**Rotimi Omosewo**

GitHub: https://github.com/rotimi2020

Portfolio: https://rotimi2020.github.io
