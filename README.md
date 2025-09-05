# UniAdmit University Admission Management System

## Project Overview

UniAdmit is a comprehensive web-based university admission management system designed to streamline the application process for both students and administrative staff. The system provides an end-to-end solution for application submission, review, and management.

### Key Features

- **User Authentication**: Secure registration and login for students and administrators
- **Multi-step Application Process**: Intuitive form with progress tracking
- **Document Management**: Upload, store, and retrieve application documents
- **Application Tracking**: Real-time status updates for applicants
- **Admin Dashboard**: Comprehensive tools for application review and management
- **Admission Letter Generation**: Automatic PDF generation for approved applications

## Installation Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 14 or higher
- MySQL 8.0 or higher
- Git

### Quick Start Guide

For those who want to get the application running quickly:

```bash
# Clone the repository
git clone https://github.com/SiddhanthMuragundi/UniAdmit.git
cd UniAdmit

# Set up backend
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# The application will automatically create the database when run.py is executed
# However, you must ensure MySQL is running and your credentials in app/config.py are correct
# You can optionally create the database manually with:
# mysql -u root -p
# CREATE DATABASE student_admission_db;
# exit;

# Run the application (this will create the database and tables)
python run.py  # Start in a new terminal window

# Set up frontend (in a separate terminal)
cd frontend-vue
npm install
npm run dev
```

Then open your browser to http://localhost:5173

### MySQL Setup

1. Install MySQL (if not already installed):
   - Download from [MySQL official website](https://dev.mysql.com/downloads/mysql/)
   - During installation, set a root password you'll remember

2. Configure MySQL credentials:
   - Update the database connection details in `backend/app/config.py`:
     ```python
     DB_HOST = 'localhost'
     DB_USER = 'root'
     DB_PASSWORD = 'your-mysql-password'
     DB_NAME = 'student_admission_db'
     ```

3. Important Note: The application will attempt to create the database automatically when run.py is executed. Manual database creation is only needed if this automatic process fails.

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/SiddhanthMuragundi/UniAdmit.git
   cd UniAdmit
   ```

2. Set up a Python virtual environment:
   ```
   cd backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Key dependencies include:
   - Flask
   - Flask-SQLAlchemy
   - Flask-Security-Too
   - Flask-Cors
   - PyMySQL
   - ReportLab
   - python-dotenv
   
   If you encounter any issues with the requirements.txt file, you can install the core dependencies manually:
   ```
   pip install flask flask-sqlalchemy flask-security-too flask-cors pymysql reportlab python-dotenv
   ```

4. Configure the database:
   - Update the database connection details in `app/config.py` if needed:
     ```python
     DB_HOST = 'localhost'
     DB_USER = 'root'
     DB_PASSWORD = 'your-mysql-password'
     DB_NAME = 'student_admission_db'
     ```

5. **Database setup**:
   - The application will automatically create the database when run.py is executed
   - You don't need to manually create the database unless the automatic creation fails
   - If needed, you can manually create the database:
     ```
     mysql -u root -p
     ```
     ```sql
     CREATE DATABASE student_admission_db;
     exit;
     ```

6. Start the backend server:
   ```
   python run.py
   ```
   The backend API will be available at http://localhost:5000

7. **Only if needed**: If you encounter issues with file uploads, run the migration script to update column sizes:
   ```
   python migrate_db.py
   ```
   Note: migrate_db.py should only be run AFTER the database and tables are created.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd ../frontend-vue
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```
   
   Key dependencies include:
   - Vue.js 3
   - Vue Router
   - Axios
   - Bootstrap 5
   - Vite
   
   If you encounter any issues with npm install, you can install the core dependencies manually:
   ```
   npm install vue@3 vue-router axios bootstrap@5 vite
   ```

3. Start the development server:
   ```
   npm run dev
   ```
   The frontend application will be available at http://localhost:5173

### Initial Admin Setup

After starting the backend server, the initial admin user will be automatically created with these credentials:
- Email: admin@email.com
- Password: adminpassword

If you need to manually create an admin user:
```
cd backend
python -c "from app import create_app; from app.models import db, User, Role; from flask_security.utils import hash_password; import uuid; app = create_app(); with app.app_context(): admin_role = Role.query.filter_by(name='admin').first() or Role(name='admin', description='Administrator'); db.session.add(admin_role); db.session.commit(); admin = User(name='Admin User', email='admin@email.com', phone='9876543210', password=hash_password('adminpassword'), fs_uniquifier=str(uuid.uuid4()), address='Admin Address', country='Country', state='State', district='District', pincode='123456', active=True); admin.roles.append(admin_role); db.session.add(admin); db.session.commit(); print('Admin user created successfully')"
```

## Usage Instructions

### For Students

1. **Registration and Login**:
   - Navigate to the homepage and click "Register"
   - Fill in your details and submit the registration form
   - Login with your email and password

2. **Submitting an Application**:
   - From the dashboard, click "Apply Now"
   - Complete the multi-step application form:
     - Step 1: Basic Information (course, previous qualification)
     - Step 2: Academic Details (10th/12th grade marks)
     - Step 3: Document Upload (degree certificate, ID proof)
     - Step 4: Review and Submit
   - You can save your application as a draft at any step
   - After submission, you can track your application status from the dashboard

3. **Tracking Application Status**:
   - Log in to your account
   - View current application status on the dashboard
   - Check for any updates or additional requirements
   - Download offer letter (if application is approved)

### For Administrators

1. **Login**:
   - Use admin credentials to log in (email: admin@email.com, password: adminpassword)
   - You will be directed to the admin dashboard

2. **Reviewing Applications**:
   - From the admin dashboard, click "Review Applications"
   - Browse the list of pending applications
   - Click on an application to view details
   - Review all information and attached documents
   - Add review comments
   - Approve or reject the application

3. **User Management**:
   - From the admin dashboard, navigate to "User Management"
   - View all registered users
   - Activate/deactivate accounts
   - Assign or modify roles

4. **System Configuration**:
   - Update application deadlines
   - Configure system-wide announcements
   - Adjust document upload limits

## Testing

The project follows Test-Driven Development (TDD) principles with comprehensive test documentation. While actual tests are not implemented in this repository, the testing approach is documented in detail:

- **TDD Implementation Plan**: `TDD_Implementation_Plan.md`
- **Functional Requirements Mapping**: `TDD_Functional_Requirements_Mapping.md`
- **FRD Updates for TDD**: `FRD_Updates_for_TDD.md`

These documents outline how tests would be structured and implemented for both backend and frontend components.

## Technology Stack

### Backend

- **Framework**: Flask (Python)
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Authentication**: Flask-Security with JWT tokens
- **PDF Generation**: ReportLab
- **File Handling**: Built-in binary storage

### Frontend

- **Framework**: Vue.js 3
- **Router**: Vue Router
- **UI Components**: Bootstrap 5
- **HTTP Client**: Axios

## Assumptions and Design Decisions

1. **User Roles**: The system assumes two primary user roles: students and administrators. Additional roles could be added in future versions.

2. **Document Storage**: Documents are stored directly in the database as binary data for simplicity. In a production environment, a dedicated file storage service might be more appropriate.

3. **Application States**: Applications follow a simple workflow: draft → pending → approved/rejected. More complex workflows could be implemented based on institutional requirements.

4. **Single Active Application**: Students can have only one active application at a time. This simplifies tracking and prevents duplicate submissions.

5. **PDF Generation**: Admission letters are generated as PDFs using ReportLab. The design assumes a standard format for all letters.

6. **Email Notifications**: The system is designed with hooks for email notifications, but actual email sending is commented out in the code. In a production environment, a proper email service would be integrated.

7. **Academic Details**: The system collects basic academic information (10th/12th grades, previous qualification). Institutions may need to customize these fields based on their specific requirements.

8. **Security Considerations**: The implementation uses JWT tokens for authentication and includes basic security measures. A production deployment would require additional security hardening.

## Documentation

For more detailed information, refer to the following documents:

- **Functional Requirements Document**: `FRD_UniAdmit_System.md`
- **Updated FRD with TDD Integration**: `Updated_FRD_UniAdmit_System.md`
- **TDD Implementation Plan**: `TDD_Implementation_Plan.md`

## Troubleshooting

### Common Installation Issues

3. **Database Creation**:
   - The application will automatically attempt to create the database when run.py is executed
   - You don't need to manually create the database unless the automatic creation fails
   - The migrate_db.py script is only needed if you need to update the database schema (for example, after changing models)

4. **When to Run migrate_db.py**:
   - The migrate_db.py script should be run in these cases:
     - After changing database models (modifying app/models.py)
     - If you need to update column types (e.g., increasing size limits)
     - If the application fails with database schema errors
   - **Important**: This script modifies the schema but doesn't create the database or tables

5. **MySQL Connection Issues**:
   - Ensure MySQL service is running
   - Verify your MySQL credentials in `app/config.py`
   - Test connection with: `mysql -u root -p -h localhost`
   - If automatic database creation fails, create it manually: `CREATE DATABASE student_admission_db;`

2. **Python Dependency Issues**:
   - Try updating pip: `pip install --upgrade pip`
   - Install dependencies one by one if batch installation fails
   - Check Python version compatibility (3.10+ recommended)

3. **Node.js/npm Issues**:
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules folder and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version (14+ recommended)

4. **Backend Server Issues**:
   - Check if port 5000 is already in use
   - Look for error messages in the terminal
   - Verify database connection settings

5. **Frontend Development Server Issues**:
   - Check if port 5173 is already in use
   - Verify Vue dependencies are installed correctly
   - Check for JavaScript errors in browser console

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Siddhanth Muragundi**

---

© 2025 UniAdmit University Admission System
