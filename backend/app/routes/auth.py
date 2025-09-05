from flask import Blueprint, request, jsonify, current_app
from flask_security import auth_token_required, current_user, logout_user, roles_required
from flask_security.utils import hash_password, verify_password
from app.models import db, User, Role
import uuid
from datetime import datetime, timezone
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password', 'address', 'country', 'state', 'district', 'pincode']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate phone format
        if not validate_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number format (10 digits required)'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == data['email']) | (User.phone == data['phone'])
        ).first()
        
        if existing_user:
            if existing_user.email == data['email']:
                return jsonify({'error': 'Email already registered'}), 400
            if existing_user.phone == data['phone']:
                return jsonify({'error': 'Phone number already registered'}), 400
        
        # Create student role if it doesn't exist
        student_role = Role.query.filter_by(name='student').first()
        if not student_role:
            student_role = Role(name='student', description='Student')
            db.session.add(student_role)
            db.session.commit()
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=hash_password(data['password']),
            fs_uniquifier=str(uuid.uuid4()),
            address=data['address'],
            country=data['country'],
            state=data['state'],
            district=data['district'],
            pincode=data['pincode'],
            active=True,
            confirmed_at=datetime.now(timezone.utc),
            date_created=datetime.now(timezone.utc)
        )
        
        # Add student role to user
        new_user.roles.append(student_role)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Student registered successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
                'phone': new_user.phone,
                'roles': [role.name for role in new_user.roles]
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return authentication token"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(data['password'], user.password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if user is active
        if not user.active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Generate authentication token
        token = user.get_auth_token()
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'roles': [role.name for role in user.roles]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@auth_token_required
def logout():
    """Logout current user"""
    try:
        # Get current user info before logout
        user_email = current_user.email
        
        # Logout user (this invalidates the token)
        logout_user()
        
        return jsonify({
            'message': f'User {user_email} logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Logout failed', 'details': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@auth_token_required
def get_profile():
    """Get current user profile"""
    try:
        return jsonify({
            'user': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email,
                'phone': current_user.phone,
                'address': current_user.address,
                'country': current_user.country,
                'state': current_user.state,
                'district': current_user.district,
                'pincode': current_user.pincode,
                'roles': [role.name for role in current_user.roles],
                'date_created': current_user.date_created.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get profile', 'details': str(e)}), 500

@auth_bp.route('/profile/edit', methods=['PUT'])
@auth_token_required
def edit_profile():
    """Edit user profile with restrictions on important fields"""
    try:
        data = request.get_json()
        
        # Define fields that cannot be edited (important fields)
        protected_fields = ['email', 'phone']
        
        # Check if user is trying to edit protected fields
        for field in protected_fields:
            if field in data:
                return jsonify({'error': f'Field "{field}" cannot be edited. Contact admin for changes.'}), 400
        
        # Define editable fields
        editable_fields = ['name', 'address', 'country', 'state', 'district', 'pincode']
        
        # Update only allowed fields
        updated_fields = []
        for field in editable_fields:
            if field in data and data[field] is not None:
                # Validate data if necessary
                if field == 'name' and len(data[field].strip()) == 0:
                    return jsonify({'error': 'Name cannot be empty'}), 400
                
                if field == 'address' and len(data[field].strip()) == 0:
                    return jsonify({'error': 'Address cannot be empty'}), 400
                
                if field == 'pincode' and not data[field].isdigit():
                    return jsonify({'error': 'Pincode must contain only numbers'}), 400
                
                # Update the field
                setattr(current_user, field, data[field])
                updated_fields.append(field)
        
        if not updated_fields:
            return jsonify({'error': 'No valid fields provided for update'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'updated_fields': updated_fields,
            'user': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email,
                'phone': current_user.phone,
                'address': current_user.address,
                'country': current_user.country,
                'state': current_user.state,
                'district': current_user.district,
                'pincode': current_user.pincode,
                'roles': [role.name for role in current_user.roles]
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Profile update failed', 'details': str(e)}), 500

@auth_bp.route('/profile/restrictions', methods=['GET'])
@auth_token_required
def get_profile_restrictions():
    """Get information about which fields can and cannot be edited"""
    return jsonify({
        'protected_fields': {
            'email': 'Contact admin to change email address',
            'phone': 'Contact admin to change phone number'
        },
        'editable_fields': {
            'name': 'Your full name',
            'address': 'Your current address',
            'country': 'Your country',
            'state': 'Your state/province',
            'district': 'Your district/city',
            'pincode': 'Your postal/zip code'
        },
        'note': 'Protected fields require admin approval for changes due to security reasons'
    }), 200

# Admin-only endpoints
@auth_bp.route('/admin/users', methods=['GET'])
@auth_token_required
def get_all_users():
    """Get all users with pagination (admin only)"""
    try:
        # Check if user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        role_filter = request.args.get('role')
        search = request.args.get('search')
        
        # Build query
        query = User.query
        
        if role_filter:
            query = query.join(User.roles).filter(Role.name == role_filter)
        
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                (User.name.ilike(search_term)) |
                (User.email.ilike(search_term)) |
                (User.phone.ilike(search_term))
            )
        
        # Order by creation date (newest first)
        query = query.order_by(User.date_created.desc())
        
        # Paginate
        users = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        users_list = []
        for user in users.items:
            users_list.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'country': user.country,
                'state': user.state,
                'district': user.district,
                'pincode': user.pincode,
                'roles': [role.name for role in user.roles],
                'date_created': user.date_created.isoformat(),
                'is_active': user.active
            })
        
        return jsonify({
            'users': users_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages,
                'has_next': users.has_next,
                'has_prev': users.has_prev
            },
            'filters': {
                'role': role_filter,
                'search': search
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve users', 'details': str(e)}), 500

@auth_bp.route('/admin/user/<int:user_id>/profile', methods=['PUT'])
@auth_token_required
def admin_edit_user_profile(user_id):
    """Edit any user's profile (admin only) - can edit protected fields"""
    try:
        # Check if user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Admin can edit all fields including protected ones
        editable_fields = [
            'name', 'email', 'phone', 'address', 'country', 
            'state', 'district', 'pincode'
        ]
        
        updated_fields = []
        for field in editable_fields:
            if field in data and data[field] is not None:
                # Validate data
                if field == 'name' and len(data[field].strip()) == 0:
                    return jsonify({'error': 'Name cannot be empty'}), 400
                
                if field == 'email':
                    # Check if email is already taken by another user
                    existing_user = User.query.filter(
                        User.email == data[field], 
                        User.id != user_id
                    ).first()
                    if existing_user:
                        return jsonify({'error': 'Email already exists'}), 400
                
                if field == 'phone':
                    # Check if phone is already taken by another user
                    existing_user = User.query.filter(
                        User.phone == data[field], 
                        User.id != user_id
                    ).first()
                    if existing_user:
                        return jsonify({'error': 'Phone number already exists'}), 400
                
                if field == 'pincode' and not data[field].isdigit():
                    return jsonify({'error': 'Pincode must contain only numbers'}), 400
                
                # Update the field
                setattr(user, field, data[field])
                updated_fields.append(field)
        
        if not updated_fields:
            return jsonify({'error': 'No valid fields provided for update'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'User profile updated successfully by admin',
            'updated_fields': updated_fields,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'country': user.country,
                'state': user.state,
                'district': user.district,
                'pincode': user.pincode,
                'roles': [role.name for role in user.roles]
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Profile update failed', 'details': str(e)}), 500

@auth_bp.route('/admin/user/<int:user_id>/toggle-status', methods=['POST'])
@auth_token_required
def toggle_user_status(user_id):
    """Activate or deactivate a user (admin only)"""
    try:
        # Check if user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent admin from deactivating themselves
        if user.id == current_user.id:
            return jsonify({'error': 'Cannot deactivate your own account'}), 400
        
        # Toggle status
        user.active = not user.active
        db.session.commit()
        
        status = 'activated' if user.active else 'deactivated'
        
        return jsonify({
            'message': f'User {status} successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'is_active': user.active
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Status update failed', 'details': str(e)}), 500

@auth_bp.route('/admin/stats', methods=['GET'])
@auth_token_required
def get_user_stats():
    """Get user statistics (admin only)"""
    try:
        # Check if user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        # Get user counts
        total_users = User.query.count()
        active_users = User.query.filter_by(active=True).count()
        inactive_users = User.query.filter_by(active=False).count()
        
        # Get role-wise counts
        from sqlalchemy import func
        role_stats = db.session.query(
            Role.name,
            func.count(User.id).label('count')
        ).join(User.roles).group_by(Role.name).all()
        
        role_breakdown = [{'role': role, 'count': count} for role, count in role_stats]
        
        # Get recent registrations (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        recent_registrations = User.query.filter(
            User.date_created >= thirty_days_ago
        ).count()
        
        # Get newest users
        newest_users = User.query.order_by(
            User.date_created.desc()
        ).limit(5).all()
        
        newest_users_list = []
        for user in newest_users:
            newest_users_list.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'roles': [role.name for role in user.roles],
                'date_created': user.date_created.isoformat()
            })
        
        return jsonify({
            'summary': {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'recent_registrations': recent_registrations
            },
            'role_breakdown': role_breakdown,
            'newest_users': newest_users_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user statistics', 'details': str(e)}), 500

@auth_bp.route('/admin/user/<int:user_id>/reset-password', methods=['POST'])
@auth_token_required
def admin_reset_password(user_id):
    """Reset a user's password (admin only)"""
    try:
        # Check if user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        new_password = data.get('new_password')
        
        if not new_password or len(new_password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Hash the new password
        user.password = hash_password(new_password)
        db.session.commit()
        
        return jsonify({
            'message': 'Password reset successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Password reset failed', 'details': str(e)}), 500

@auth_bp.route('/admin/dashboard', methods=['GET'])
@auth_token_required
def admin_dashboard():
    """Get comprehensive admin dashboard data"""
    try:
        # Check if user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        from app.models import Application
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # User statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(active=True).count()
        students_count = User.query.join(User.roles).filter(Role.name == 'student').count()
        admins_count = User.query.join(User.roles).filter(Role.name == 'admin').count()
        
        # Application statistics
        total_applications = Application.query.count()
        pending_applications = Application.query.filter_by(status='pending').count()
        approved_applications = Application.query.filter_by(status='approved').count()
        rejected_applications = Application.query.filter_by(status='rejected').count()
        draft_applications = Application.query.filter_by(status='draft').count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_users = User.query.filter(User.date_created >= week_ago).count()
        recent_applications = Application.query.filter(Application.date_created >= week_ago).count()
        
        # Top courses
        top_courses = db.session.query(
            Application.course_applied,
            func.count(Application.id).label('count')
        ).group_by(Application.course_applied).order_by(
            func.count(Application.id).desc()
        ).limit(5).all()
        
        top_courses_list = [{'course': course, 'applications': count} for course, count in top_courses]
        
        # Recent applications needing review
        pending_review = Application.query.filter_by(status='pending').order_by(
            Application.date_created.desc()
        ).limit(5).all()
        
        pending_list = []
        for app in pending_review:
            pending_list.append({
                'id': app.id,
                'student_name': app.student.name,
                'course_applied': app.course_applied,
                'date_created': app.date_created.isoformat(),
                'days_pending': (datetime.now(timezone.utc) - app.date_created).days
            })
        
        # Monthly trends (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        monthly_applications = db.session.query(
            func.date_format(Application.date_created, '%Y-%m').label('month'),
            func.count(Application.id).label('count')
        ).filter(
            Application.date_created >= six_months_ago
        ).group_by(
            func.date_format(Application.date_created, '%Y-%m')
        ).order_by('month').all()
        
        monthly_users = db.session.query(
            func.date_format(User.date_created, '%Y-%m').label('month'),
            func.count(User.id).label('count')
        ).filter(
            User.date_created >= six_months_ago
        ).group_by(
            func.date_format(User.date_created, '%Y-%m')
        ).order_by('month').all()
        
        return jsonify({
            'user_stats': {
                'total_users': total_users,
                'active_users': active_users,
                'students_count': students_count,
                'admins_count': admins_count,
                'recent_registrations': recent_users
            },
            'application_stats': {
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'approved_applications': approved_applications,
                'rejected_applications': rejected_applications,
                'draft_applications': draft_applications,
                'recent_submissions': recent_applications,
                'approval_rate': round((approved_applications / max(total_applications - draft_applications, 1)) * 100, 2) if total_applications > 0 else 0
            },
            'top_courses': top_courses_list,
            'pending_review': pending_list,
            'trends': {
                'monthly_applications': [{'month': month, 'count': count} for month, count in monthly_applications],
                'monthly_users': [{'month': month, 'count': count} for month, count in monthly_users]
            },
            'system_health': {
                'total_admins': admins_count,
                'active_users_percentage': round((active_users / max(total_users, 1)) * 100, 2),
                'pending_review_count': pending_applications
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to load dashboard data', 'details': str(e)}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@auth_token_required
def verify_token():
    """Verify if token is valid"""
    try:
        return jsonify({
            'valid': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'roles': [role.name for role in current_user.roles]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Token verification failed', 'details': str(e)}), 500

@auth_bp.route('/create-admin', methods=['POST'])
@auth_token_required
def create_admin():
    """Create a new admin user (only accessible by existing admins)"""
    try:
        # Check if current user is admin
        user_roles = [role.name for role in current_user.roles]
        if 'admin' not in user_roles:
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password', 'address', 'country', 'state', 'district', 'pincode']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate phone format
        if not validate_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number format (10 digits required)'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == data['email']) | (User.phone == data['phone'])
        ).first()
        
        if existing_user:
            if existing_user.email == data['email']:
                return jsonify({'error': 'Email already registered'}), 400
            if existing_user.phone == data['phone']:
                return jsonify({'error': 'Phone number already registered'}), 400
        
        # Create admin role if it doesn't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
            db.session.commit()
        
        # Create new admin user
        new_admin = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=hash_password(data['password']),
            fs_uniquifier=str(uuid.uuid4()),
            address=data['address'],
            country=data['country'],
            state=data['state'],
            district=data['district'],
            pincode=data['pincode'],
            active=True,
            confirmed_at=datetime.now(timezone.utc),
            date_created=datetime.now(timezone.utc)
        )
        
        # Add admin role to user
        new_admin.roles.append(admin_role)
        
        db.session.add(new_admin)
        db.session.commit()
        
        return jsonify({
            'message': 'Admin user created successfully',
            'admin': {
                'id': new_admin.id,
                'name': new_admin.name,
                'email': new_admin.email,
                'phone': new_admin.phone,
                'roles': [role.name for role in new_admin.roles]
            },
            'created_by': {
                'id': current_user.id,
                'email': current_user.email
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Admin creation failed', 'details': str(e)}), 500
