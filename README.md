# Brudite-SES
# Student Evaluation System - sebackend

Welcome to the Student Evaluation System - a Django project designed to manage student evaluations with custom user roles.

## About

The Student Evaluation System is a Django-based web application that streamlines student evaluation management. It features custom user authentication and role management for enhanced security and tailored access.

## Getting Started

### Prerequisites

- Python 3.x
- Virtual environment tool (e.g., `venv` or `virtualenv`)

### Installation

Clone repository:
 onterminal--
   git clone https://github.com/Brudite-Pvt-Ltd/Brudite-SES

Create and activate virtual environment:
    python -m venv venv
   venv\Scripts\activate

Install dependencies:
    pip install -r requirements.txt

Run Django development server:
    python manage.py runserver
    Access at http://127.0.0.1:8000/
        #for admin admin/
Custom User and Role
Utilizes custom user models and roles for:

Extended user info and authentication.
Role-based access control and tailored permissions.

## New Feature: CSV Upload and Email Notifications

We've recently added a new feature to our project that allows users to upload CSV files, compare the data with our database, and send email notifications to users found in both datasets. Here's an overview of how it works:

### `forms.py`

We've added a new file `forms.py` that defines a form for uploading CSV files. Users can use this form to select and submit a CSV file.

### CSV Upload View

We've created a new view, `upload_csv`, which handles the CSV file upload process. When a user submits a CSV file using the form, this view does the following:

1. Parses the uploaded CSV file.
2. Fetches relevant data from our database.
3. Compares the CSV data with the database data to identify common users.

### Email Notifications

If common users are found in both the CSV and the database, our project will send email notifications to these users. These notifications can be customized to include specific details or messages.

## Usage

To take advantage of this new feature, follow these steps:

1. Run the project locally or on your server.
2. Access the CSV upload feature through the appropriate URL (e.g., `/upload-csv/`).
3. Use the provided form to select and upload a CSV file.
4. The project will process the data, compare it with the database, and send email notifications to common users.

## Dependencies

Make sure you have the following dependencies installed to use this feature:

- [pandas , smptlib ,MIMEText ,MIMEMultipart]

## Contributing

If you'd like to contribute to this project or have suggestions for improvements, please follow our [contribution guidelines](CONTRIBUTING.md).



author :  https://github.com/Brudite-Pvt-Ltd/Brudite-SES
