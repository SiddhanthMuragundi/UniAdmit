import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from flask_security.utils import hash_password
from datetime import datetime, timezone
import uuid
import mysql.connector
from mysql.connector import Error

from app.config import Config
from app.models import db, User, Role

# Initialize user datastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def create_database_if_not_exists():
    """Create MySQL database if it doesn't exist using environment variables"""
    try:
        # Get database credentials from config (which loads from .env)
        db_host = Config.DB_HOST
        db_user = Config.DB_USER
        db_password = Config.DB_PASSWORD
        db_name = Config.DB_NAME
        
        print(f"Checking database connection to {db_host}...")
        
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if db_name not in databases:
                # Create database if it doesn't exist
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created successfully!")
            else:
                print(f"Database '{db_name}' already exists")
            
            cursor.close()
            connection.close()
            
        return True
        
    except Error as e:
        print(f"Database setup failed: {e}")
        return False
    except Exception as e:
        print(f"Database error: {e}")
        return False

def create_default_admin(user_datastore):
    """Create default admin user if it doesn't exist"""
    from flask import current_app
    
    admin_email = current_app.config['ADMIN_EMAIL']
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        # Create admin role
        admin_role = user_datastore.find_or_create_role(
            name="admin",
            description="Administrator"
        )
        
        # Create admin user using config values
        admin_user = user_datastore.create_user(
            name=current_app.config['ADMIN_NAME'],
            email=current_app.config['ADMIN_EMAIL'],
            phone=current_app.config['ADMIN_PHONE'],
            password=hash_password(current_app.config['ADMIN_PASSWORD']),
            fs_uniquifier=str(uuid.uuid4()),
            address=current_app.config['ADMIN_ADDRESS'],           
            country=current_app.config['ADMIN_COUNTRY'],
            state=current_app.config['ADMIN_STATE'],
            district=current_app.config['ADMIN_DISTRICT'],
            pincode=current_app.config['ADMIN_PINCODE'],
            active=True,
            date_created=datetime.now(timezone.utc),
            confirmed_at=datetime.now(timezone.utc),
        )
        
        user_datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()
        print("Admin user created")
    # Admin already exists - no message needed

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    print("Starting UniAdmit System...")
    
    # Add request size limit error handler
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'error': 'File too large',
            'message': 'The uploaded file exceeds the maximum size limit of 16MB'
        }), 413

    # Step 1: Create database if it doesn't exist
    if not create_database_if_not_exists():
        print("Warning: Database setup failed")

    # Step 2: Initialize extensions
    db.init_app(app)
    security = Security(app, user_datastore)
    
    # Configure CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Authentication-Token", "Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Step 3: Create tables and default admin
    with app.app_context():
        try:
            db.create_all()
            create_default_admin(user_datastore)
        except Exception as e:
            print(f"Database setup failed: {e}")

    # Step 4: Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.application import application_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(application_bp, url_prefix='/api/application')

    # Health check route
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Student Admission System API is running'}, 200

    @app.route('/')
    def index():
        return {
            'message': 'UniAdmit API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'auth': '/api/auth',
                'application': '/api/application',
                'health': '/health'
            }
        }, 200

    print("UniAdmit API ready at http://localhost:5000")
    
    return app
