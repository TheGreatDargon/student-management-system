
# Student Management System

A Flask-based web application for managing student records, featuring a responsive UI built with Tailwind CSS and a React-powered dynamic table. It enables staff to register, log in, and perform complete CRUD operations on student records. Data is securely stored in a SQLite database.

---

## Features

### User Authentication

* Secure registration and login system using bcrypt password hashing.

### Student Management

* Add student details such as name, age, date of birth, gender, address, parent information, and class.
* Edit existing student records.
* Delete students with confirmation.
* Search students by ID.

### Responsive User Interface

* Developed using Tailwind CSS for modern design.
* Fully responsive across mobile and desktop screens.
* Color scheme: Blue (`#1E90FF`, `#4682B4`), Light Gray (`#F5F7FA`), White (`#FFFFFF`).

### Dynamic Student Table

* Implemented using React.
* Real-time updates and sortable columns.

### Flash Messaging

* React-based alerts to indicate success or failure.

### Database

* SQLite database with tables for Student, Class, and Staff.
* Preloaded with sample class entries (10A, 10B, 11A, 12A).

---

## Project Structure

```
project/
├── static/
│   ├── styles.css
│   └── favicon.ico
├── templates/
│   ├── base.html
│   ├── form.html
│   ├── login.html
│   ├── register.html
│   ├── table.html
│   └── update.html
├── app.py
├── students.db
└── README.md
```

---

## Prerequisites

* Python 3.8 or above
* pip package manager
* SQLite (included with Python)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create a Virtual Environment

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy bcrypt
```

### 4. Run the Application

```bash
python app.py
```

Access the application at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Database Initialization

* The database (`students.db`) is automatically created during the first run.
* Default classes are inserted automatically.
* To reset the data, delete `students.db` and restart the application.

---

## Usage Instructions

### Staff Registration

* Navigate to `/register` to create an account.

### Login

* Go to `/login` and enter valid credentials.

### Managing Students

* Home page displays the student table.
* Use "Add Student" to create new entries.
* Edit and delete options are available next to each record.
* Use the search bar to find a student by ID.

### Logout

* Click the "Logout" option in the navigation bar.

---

## Routes Overview

| Route          | Description                    |
| -------------- | ------------------------------ |
| `/`            | Student table (requires login) |
| `/login`       | Staff login page               |
| `/register`    | Staff registration page        |
| `/logout`      | Logout current user            |
| `/add_student` | Add a new student              |
| `/edit/<id>`   | Edit student details           |
| `/delete/<id>` | Delete student record          |
| `/search`      | Search student by ID           |

---

## Technologies Used

* **Backend:** Flask, Flask-SQLAlchemy, bcrypt
* **Frontend:** Tailwind CSS, React with Babel (via CDN)
* **Database:** SQLite

---

## Testing Guidelines

* Validate authentication workflows with valid and invalid data.
* Check CRUD operations thoroughly.
* Test responsive layouts on various screen sizes.
* Confirm proper error handling and messaging.

---

## Troubleshooting

* **Page not found:** Ensure correct login and route access.
* **Database errors:** Remove `students.db` and rerun the app.
* **UI issues:** Confirm React and Babel CDN integration and inspect browser console.

---

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit and push your changes.
4. Open a pull request with a detailed description.

---
