# UniAdmit - University Admission Management System

A modern, full-stack university admission management system built with Vue.js frontend and Flask backend.

## Features

### For Students
- **User Registration & Authentication** - Secure account creation and login
- **Application Management** - Step-by-step application process
- **Document Upload** - Secure upload of certificates and ID proof
- **Application Tracking** - Real-time status updates
- **Profile Management** - Update personal information

### For Administrators
- **Application Review** - Review and manage student applications
- **Status Management** - Approve or reject applications with comments
- **Dashboard Analytics** - Overview of application statistics
- **Student Management** - View student details and applications

## Technology Stack

### Frontend (Vue.js)
- **Vue 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **Bootstrap 5** - UI framework
- **Axios** - HTTP client
- **Vite** - Build tool

### Backend (Flask)
- **Flask** - Python web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Security-Too** - Authentication and authorization
- **Flask-CORS** - Cross-origin resource sharing
- **MySQL** - Database
- **Argon2** - Password hashing

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- MySQL database

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend-vue
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=student_admission_db
   SECRET_KEY=your_secret_key
   ADMIN_EMAIL=admin@email.com
   ADMIN_PASSWORD=adminpassword
   ```

5. Start the Flask server:
   ```bash
   python run.py
   ```

The backend API will be available at `http://localhost:5000`

## Default Admin Credentials

- **Email:** admin@email.com
- **Password:** adminpassword

## Project Structure

```
├── frontend-vue/          # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia stores
│   │   ├── router/        # Vue Router configuration
│   │   └── assets/        # Static assets
│   └── package.json
│
├── backend/               # Flask backend
│   ├── app/
│   │   ├── routes/        # API routes
│   │   ├── models.py      # Database models
│   │   └── config.py      # Configuration
│   ├── requirements.txt
│   └── run.py
```

## Application Flow

1. **Student Registration** - Students create accounts with personal details
2. **Application Submission** - Step-by-step form with academic details and document upload
3. **Admin Review** - Administrators review applications and make decisions
4. **Status Updates** - Students receive real-time updates on their application status

## Key Features

- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Secure Authentication** - Token-based authentication with Flask-Security
- **File Upload** - Secure document upload with validation
- **Real-time Updates** - Dynamic status updates without page refresh
- **Role-based Access** - Different interfaces for students and administrators

## API Endpoints

### Authentication
- `POST /api/auth/register` - Student registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### Applications
- `POST /api/application/submit` - Submit application
- `GET /api/application/my-applications` - Get user applications
- `GET /api/application/all` - Get all applications (admin)
- `PUT /api/application/{id}/status` - Update application status (admin)

## Security Features

- **Password Hashing** - Argon2 password hashing
- **Token Authentication** - Secure token-based authentication
- **CORS Protection** - Proper CORS configuration
- **Input Validation** - Server-side validation for all inputs
- **File Upload Security** - File type and size validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
