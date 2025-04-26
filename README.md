
**Bookstore Management System**

Project Overview
A full-stack Django application for managing a bookstore, featuring user authentication, book catalog, shopping cart, checkout, order confirmation, and an admin panel for managing books, categories, and orders.

**Features:**

User Authentication (Register, Login, Logout)

Book Catalog with Categories

Shopping Cart with Session Management

Checkout and Order Confirmation

Custom Admin Panel for Book, Category, and Order Management


**Tech Stack**

Backend: Django 4.2.7

Database: MySQL with PyMySQL

Frontend: Bootstrap 5

Containerization: Docker & Docker Compose

CI/CD: Jenkins

**Setup & Run Instructions**
Prerequisites:
Docker & Docker Compose

Git

**Installation:**
Clone the repository:

git clone <repository-url>
cd bookstore_project

Build Docker Containers:

docker-compose build

docker-compose up -d

Access the app at http://localhost:8000.

**Docker Usage**

Start: docker-compose up

Stop: docker-compose down

Django Commands: docker-compose run --rm web python manage.py <command>

Jenkins CI/CD
Set up Jenkins to automatically build, test, and deploy the application using the repository’s pipeline configuration.

**Troubleshooting:**
Ensure the MySQL container is running if you face database connection issues.

Use docker-compose logs to troubleshoot Docker container issues.

**Screeshots**
<img width="1440" alt="Screenshot 2025-04-26 at 9 03 49 AM" src="https://github.com/user-attachments/assets/972c7ca7-a226-4b1a-a5ed-c27906c755a4" />
<img width="1440" alt="Screenshot 2025-04-26 at 9 04 02 AM" src="https://github.com/user-attachments/assets/6900f5fa-7dd2-4d01-9f40-a19d10a296a1" />
<img width="1440" alt="Screenshot 2025-04-26 at 9 04 12 AM" src="https://github.com/user-attachments/assets/f107c6eb-abec-4fdb-8a68-62c625eba251" />
<img width="1440" alt="Screenshot 2025-04-26 at 9 04 29 AM" src="https://github.com/user-attachments/assets/686562ce-97e6-4c51-ac77-ee5a6525ca07" />
<img width="1440" alt="Screenshot 2025-04-26 at 9 05 05 AM" src="https://github.com/user-attachments/assets/41ace395-a963-49f4-af43-b18578bfc781" />
<img width="1440" alt="Screenshot 2025-04-26 at 9 05 29 AM" src="https://github.com/user-attachments/assets/83e34f9a-8fa5-498a-9cde-e92598c81bdc" />





