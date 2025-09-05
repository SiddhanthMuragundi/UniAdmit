from flask import Blueprint, request, jsonify, current_app, send_file
from flask_security import current_user, auth_token_required, roles_required
from werkzeug.utils import secure_filename
from app.models import Application, User, db
from datetime import datetime, timezone, timedelta
import base64
import binascii
import os
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics import renderPDF

application_bp = Blueprint('application', __name__)

@application_bp.route('/save-draft', methods=['POST'])
@auth_token_required
def save_draft():
    """Save application as draft - allows saving with minimal or no data"""
    try:
        data = request.get_json()
        if not data:
            data = {}  # Allow empty data for draft
        
        # Validate numeric fields only if provided and not empty
        if data.get('tenth_percentage') and str(data.get('tenth_percentage')).strip():
            try:
                tenth_pct = float(data.get('tenth_percentage'))
                if not (0 <= tenth_pct <= 100):
                    return jsonify({'error': 'Tenth percentage must be between 0 and 100'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid tenth percentage value'}), 400
        
        if data.get('twelfth_percentage') and str(data.get('twelfth_percentage')).strip():
            try:
                twelfth_pct = float(data.get('twelfth_percentage'))
                if not (0 <= twelfth_pct <= 100):
                    return jsonify({'error': 'Twelfth percentage must be between 0 and 100'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid twelfth percentage value'}), 400
        
        if data.get('graduation_year') and str(data.get('graduation_year')).strip():
            try:
                grad_year = int(data.get('graduation_year'))
                if not (1980 <= grad_year <= 2030):
                    return jsonify({'error': 'Invalid graduation year'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid graduation year value'}), 400
        
        # Check if user already has a draft
        existing_draft = Application.query.filter_by(
            student_id=current_user.id,
            status='draft'
        ).first()
        
        if existing_draft:
            # Update existing draft - allow updating with any provided values
            if 'course_applied' in data:
                existing_draft.course_applied = data['course_applied'] or existing_draft.course_applied
            if 'tenth_percentage' in data:
                if data['tenth_percentage'] and str(data['tenth_percentage']).strip():
                    existing_draft.tenth_percentage = float(data['tenth_percentage'])
            if 'tenth_board' in data:
                existing_draft.tenth_board = data['tenth_board'] or existing_draft.tenth_board
            if 'twelfth_percentage' in data:
                if data['twelfth_percentage'] and str(data['twelfth_percentage']).strip():
                    existing_draft.twelfth_percentage = float(data['twelfth_percentage'])
            if 'twelfth_board' in data:
                existing_draft.twelfth_board = data['twelfth_board'] or existing_draft.twelfth_board
            if 'previous_qualification' in data:
                existing_draft.previous_qualification = data['previous_qualification'] or existing_draft.previous_qualification
            if 'previous_institution' in data:
                existing_draft.previous_institution = data['previous_institution'] or existing_draft.previous_institution
            if 'graduation_year' in data:
                if data['graduation_year'] and str(data['graduation_year']).strip():
                    existing_draft.graduation_year = int(data['graduation_year'])
            
            # Update address fields if provided
            if 'address' in data:
                existing_draft.address = data['address'] or existing_draft.address
            if 'country' in data:
                existing_draft.country = data['country'] or existing_draft.country
            if 'state' in data:
                existing_draft.state = data['state'] or existing_draft.state
            if 'district' in data:
                existing_draft.district = data['district'] or existing_draft.district
            if 'pincode' in data:
                existing_draft.pincode = data['pincode'] or existing_draft.pincode
            
            db.session.commit()
            
            return jsonify({
                'message': 'Draft updated successfully',
                'application_id': existing_draft.id,
                'status': 'draft'
            }), 200
        else:
            # Create new draft with minimal required fields - allow completely empty form
            # Provide minimal defaults to satisfy database constraints
            application = Application(
                student_id=current_user.id,
                course_applied=data.get('course_applied') or 'Not Selected',
                tenth_percentage=float(data.get('tenth_percentage')) if data.get('tenth_percentage') and str(data.get('tenth_percentage')).strip() else 0.0,
                tenth_board=data.get('tenth_board') or 'Not Specified',
                twelfth_percentage=float(data.get('twelfth_percentage')) if data.get('twelfth_percentage') and str(data.get('twelfth_percentage')).strip() else 0.0,
                twelfth_board=data.get('twelfth_board') or 'Not Specified',
                previous_qualification=data.get('previous_qualification') or 'Not Specified',
                previous_institution=data.get('previous_institution') or 'Not Specified',
                graduation_year=int(data.get('graduation_year')) if data.get('graduation_year') and str(data.get('graduation_year')).strip() else 2024,
                # Provide default values for required fields
                address=data.get('address') or 'Not Specified',
                country=data.get('country') or 'Not Specified',
                state=data.get('state') or 'Not Specified',
                district=data.get('district') or 'Not Specified',
                pincode=data.get('pincode') or '000000',
                # Provide dummy binary data for documents (will be updated later)
                degree_certificate=b'draft',
                degree_certificate_filename='draft.pdf',
                id_proof=b'draft',
                id_proof_filename='draft.pdf',
                status='draft'
            )
            
            db.session.add(application)
            db.session.commit()
            
            return jsonify({
                'message': 'Draft saved successfully',
                'application_id': application.id,
                'status': 'draft'
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save draft', 'details': str(e)}), 500

@application_bp.route('/get-draft', methods=['GET'])
@auth_token_required
def get_draft():
    """Get user's draft application"""
    try:
        draft = Application.query.filter_by(
            student_id=current_user.id,
            status='draft'
        ).first()
        
        if not draft:
            return jsonify({'message': 'No draft found'}), 404
        
        # Helper function to clean up draft values for editing
        def clean_draft_value(value, default_indicators=['Not Specified', 'Not Selected', '']):
            if value in default_indicators:
                return ''
            return value or ''
        
        return jsonify({
            'draft': {
                'id': draft.id,
                'course_applied': clean_draft_value(draft.course_applied, ['Not Selected', '']),
                'tenth_percentage': draft.tenth_percentage if draft.tenth_percentage != 0.0 else '',
                'tenth_board': clean_draft_value(draft.tenth_board),
                'twelfth_percentage': draft.twelfth_percentage if draft.twelfth_percentage != 0.0 else '',
                'twelfth_board': clean_draft_value(draft.twelfth_board),
                'previous_qualification': clean_draft_value(draft.previous_qualification),
                'previous_institution': clean_draft_value(draft.previous_institution),
                'graduation_year': draft.graduation_year if draft.graduation_year != 2024 else '',
                'address': clean_draft_value(draft.address),
                'country': clean_draft_value(draft.country),
                'state': clean_draft_value(draft.state),
                'district': clean_draft_value(draft.district),
                'pincode': clean_draft_value(draft.pincode, ['Not Specified', '000000', '']),
                'date_created': draft.date_created.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve draft', 'details': str(e)}), 500

@application_bp.route('/submit', methods=['POST'])
@auth_token_required
def submit_application():
    """Submit final application"""
    print("=== SUBMIT APPLICATION DEBUG ===")
    try:
        # Check if user already has a submitted application
        existing_application = Application.query.filter_by(
            student_id=current_user.id,
            status='pending'
        ).first()
        
        if existing_application:
            print("ERROR: User already has pending application")
            return jsonify({'error': 'You already have a pending application'}), 400
        
        # Get data from request - handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            print(f"Received JSON data with keys: {list(data.keys()) if data else 'None'}")
        else:
            # Handle form data (multipart/form-data)
            data = request.form.to_dict()
            print(f"Received form data with keys: {list(data.keys()) if data else 'None'}")
            
            # Handle file uploads from form data
            files = request.files
            if 'degree_certificate' in files:
                file = files['degree_certificate']
                if file and file.filename:
                    import base64
                    data['degree_certificate'] = {
                        'data': base64.b64encode(file.read()).decode('utf-8'),
                        'filename': file.filename
                    }
            
            if 'id_proof' in files:
                file = files['id_proof']
                if file and file.filename:
                    import base64
                    data['id_proof'] = {
                        'data': base64.b64encode(file.read()).decode('utf-8'),
                        'filename': file.filename
                    }
        
        if not data:
            print("ERROR: No data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields for submission
        required_fields = ['course_applied', 'tenth_percentage', 'tenth_board', 
                          'twelfth_percentage', 'twelfth_board', 'previous_qualification',
                          'previous_institution', 'graduation_year', 'address', 
                          'country', 'state', 'district', 'pincode']
        
        missing_fields = []
        for field in required_fields:
            if not data.get(field) or str(data.get(field)).strip() == '':
                missing_fields.append(field)
        
        print(f"Missing fields: {missing_fields}")
        if missing_fields:
            print(f"ERROR: Missing required fields: {missing_fields}")
            return jsonify({
                'error': 'Missing required fields', 
                'missing_fields': missing_fields
            }), 400
        
        # Validate numeric fields
        print("Validating numeric fields...")
        try:
            tenth_pct = float(data.get('tenth_percentage'))
            twelfth_pct = float(data.get('twelfth_percentage'))
            grad_year = int(data.get('graduation_year'))
            print(f"Numeric validation passed: {tenth_pct}%, {twelfth_pct}%, {grad_year}")
            
            if not (0 <= tenth_pct <= 100) or not (0 <= twelfth_pct <= 100):
                print("ERROR: Invalid percentage range")
                return jsonify({'error': 'Percentages must be between 0 and 100'}), 400
            
            if not (1980 <= grad_year <= 2030):
                print("ERROR: Invalid graduation year range")
                return jsonify({'error': 'Invalid graduation year'}), 400
                
        except (ValueError, TypeError) as e:
            print(f"ERROR: Numeric validation failed: {e}")
            return jsonify({'error': 'Invalid numeric values for percentage or year'}), 400
        
        # Get draft if exists
        print("Checking for existing draft...")
        draft = Application.query.filter_by(
            student_id=current_user.id,
            status='draft'
        ).first()
        print(f"Found draft: {draft.id if draft else 'None'}")
        
        # Helper function to safely decode base64 and validate file size
        def process_file_upload(file_data, file_type):
            if not file_data or not isinstance(file_data, dict):
                print(f"No {file_type} file data provided")
                return b'', ''
            
            try:
                if 'data' not in file_data:
                    print(f"No data field in {file_type}")
                    return b'', ''
                
                # Remove data URL prefix if present (e.g., "data:application/pdf;base64,")
                base64_data = file_data['data']
                if ',' in base64_data:
                    base64_data = base64_data.split(',')[1]
                
                # Check base64 string length before decoding (rough size check)
                # Base64 encoding increases size by ~33%, so 5MB file becomes ~6.7MB base64
                max_base64_length = 6 * 1024 * 1024  # ~4.5MB original file limit
                if len(base64_data) > max_base64_length:
                    raise ValueError(f"{file_type} file too large (max 4.5MB allowed)")
                
                # Decode base64
                decoded_data = base64.b64decode(base64_data, validate=True)
                
                # Check actual decoded file size (strict limit: 5MB)
                max_file_size = 5 * 1024 * 1024  # 5MB limit
                if len(decoded_data) > max_file_size:
                    raise ValueError(f"{file_type} file size exceeds 5MB limit")
                
                # Validate minimum file size (prevent empty files)
                if len(decoded_data) < 100:  # At least 100 bytes
                    raise ValueError(f"{file_type} file is too small or empty")
                
                # Basic file type validation by checking magic bytes
                def validate_file_type(data):
                    # PDF magic bytes
                    if data.startswith(b'%PDF'):
                        return True
                    # JPEG magic bytes
                    if data.startswith(b'\xff\xd8\xff'):
                        return True
                    # PNG magic bytes
                    if data.startswith(b'\x89PNG\r\n\x1a\n'):
                        return True
                    return False
                
                if not validate_file_type(decoded_data):
                    raise ValueError(f"{file_type} file type not supported. Only PDF, JPG, and PNG files are allowed")
                
                filename = file_data.get('filename', f'{file_type}_document')
                
                # Validate filename
                if not filename or len(filename) > 255:
                    filename = f'{file_type}_document'
                
                # Sanitize filename
                import re
                filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
                
                print(f"Processed {file_type}: {len(decoded_data)} bytes, filename: {filename}")
                return decoded_data, filename
                
            except (base64.binascii.Error, ValueError) as e:
                raise ValueError(f"Invalid {file_type} file: {str(e)}")
        
        # Process file uploads with error handling
        print("Processing file uploads...")
        try:
            degree_cert_data, degree_cert_filename = process_file_upload(
                data.get('degree_certificate'), 'degree_certificate'
            )
            id_proof_data, id_proof_filename = process_file_upload(
                data.get('id_proof'), 'id_proof'
            )
            print(f"File processing successful: {len(degree_cert_data)} bytes, {len(id_proof_data)} bytes")
        except ValueError as e:
            print(f"ERROR: File processing failed: {e}")
            return jsonify({'error': str(e)}), 400
        
        if draft:
            print("Updating existing draft...")
            # Update draft to submitted
            try:
                draft.course_applied = data.get('course_applied')
                draft.tenth_percentage = tenth_pct
                draft.tenth_board = data.get('tenth_board')
                draft.twelfth_percentage = twelfth_pct
                draft.twelfth_board = data.get('twelfth_board')
                draft.previous_qualification = data.get('previous_qualification')
                draft.previous_institution = data.get('previous_institution')
                draft.graduation_year = grad_year
                draft.address = data.get('address')
                draft.country = data.get('country')
                draft.state = data.get('state')
                draft.district = data.get('district')
                draft.pincode = data.get('pincode')
                draft.status = 'pending'
                
                # Update file uploads
                draft.degree_certificate = degree_cert_data
                draft.degree_certificate_filename = degree_cert_filename
                draft.id_proof = id_proof_data
                draft.id_proof_filename = id_proof_filename
                
                print("Committing draft update to database...")
                db.session.commit()
                application_id = draft.id
                print(f"Successfully updated draft with ID: {application_id}")
            except Exception as db_error:
                print(f"Database update error: {db_error}")
                db.session.rollback()
                return jsonify({'error': 'Database update failed', 'details': str(db_error)}), 500
        else:
            print("Creating new application...")
            # Create new application
            try:
                application = Application(
                    student_id=current_user.id,
                    course_applied=data.get('course_applied'),
                    tenth_percentage=tenth_pct,
                    tenth_board=data.get('tenth_board'),
                    twelfth_percentage=twelfth_pct,
                    twelfth_board=data.get('twelfth_board'),
                    previous_qualification=data.get('previous_qualification'),
                    previous_institution=data.get('previous_institution'),
                    graduation_year=grad_year,
                    address=data.get('address'),
                    country=data.get('country'),
                    state=data.get('state'),
                    district=data.get('district'),
                    pincode=data.get('pincode'),
                    status='pending',
                    degree_certificate=degree_cert_data,
                    degree_certificate_filename=degree_cert_filename,
                    id_proof=id_proof_data,
                    id_proof_filename=id_proof_filename
                )
                
                print("Adding new application to database...")
                db.session.add(application)
                print("Committing new application to database...")
                db.session.commit()
                application_id = application.id
                print(f"Successfully created application with ID: {application_id}")
            except Exception as db_error:
                print(f"Database creation error: {db_error}")
                db.session.rollback()
                return jsonify({'error': 'Database creation failed', 'details': str(db_error)}), 500
        
        print("Application submission successful!")
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application_id,
            'status': 'pending'
        }), 201
        
    except Exception as e:
        print(f"UNEXPECTED ERROR in submit_application: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': 'Application submission failed', 'details': str(e)}), 500

@application_bp.route('/status', methods=['GET'])
@auth_token_required
def get_application_status():
    """Get user's application status"""
    try:
        application = Application.query.filter_by(student_id=current_user.id).first()
        
        if not application:
            return jsonify({'message': 'No application found'}), 404
        
        app_data = {
            'id': application.id,
            'course_applied': application.course_applied,
            'status': application.status,
            'date_created': application.date_created.isoformat(),
            'review_comments': application.review_comments
        }
        
        if application.reviewed_at:
            app_data['reviewed_at'] = application.reviewed_at.isoformat()
        
        if application.reviewer:
            app_data['reviewed_by'] = application.reviewer.name
        
        return jsonify({'application': app_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve application status', 'details': str(e)}), 500

@application_bp.route('/list', methods=['GET'])
@auth_token_required
def get_user_applications():
    """Get all applications for the current user"""
    try:
        applications = Application.query.filter_by(student_id=current_user.id).all()
        
        applications_list = []
        for app in applications:
            app_data = {
                'id': app.id,
                'course_applied': app.course_applied,
                'status': app.status,
                'tenth_percentage': app.tenth_percentage,
                'tenth_board': app.tenth_board,
                'twelfth_percentage': app.twelfth_percentage,
                'twelfth_board': app.twelfth_board,
                'previous_qualification': app.previous_qualification,
                'previous_institution': app.previous_institution,
                'graduation_year': app.graduation_year,
                'date_created': app.date_created.isoformat(),
                'review_comments': app.review_comments,
                'reviewed_at': app.reviewed_at.isoformat() if app.reviewed_at else None,
                # Add address fields
                'address': app.address,
                'country': app.country,
                'state': app.state,
                'district': app.district,
                'pincode': app.pincode,
                # Add document info
                'degree_certificate_filename': app.degree_certificate_filename,
                'id_proof_filename': app.id_proof_filename,
                'has_degree_certificate': bool(app.degree_certificate),
                'has_id_proof': bool(app.id_proof)
            }
            
            if app.reviewer:
                app_data['reviewed_by'] = app.reviewer.name
            
            applications_list.append(app_data)
        
        return jsonify({'applications': applications_list}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve applications', 'details': str(e)}), 500

@application_bp.route('/edit-profile', methods=['PUT'])
@auth_token_required
def edit_profile():
    """Edit user profile (limited fields after application submission)"""
    try:
        data = request.get_json()
        
        # Check if user has submitted application
        submitted_app = Application.query.filter_by(
            student_id=current_user.id,
            status='pending'
        ).first()
        
        # List of fields that can be edited after submission
        allowed_fields_after_submission = ['phone', 'address']
        
        # List of fields that cannot be edited after submission
        restricted_fields = ['name', 'email', 'date_of_birth']
        
        if submitted_app:
            # Check if trying to edit restricted fields
            for field in data.keys():
                if field in restricted_fields:
                    return jsonify({
                        'error': f'Cannot edit {field} after application submission',
                        'restricted_fields': restricted_fields,
                        'allowed_fields': allowed_fields_after_submission
                    }), 400
        
        # Update allowed fields
        for field, value in data.items():
            if hasattr(current_user, field):
                if not submitted_app or field in allowed_fields_after_submission:
                    setattr(current_user, field, value)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'updated_fields': list(data.keys())
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Profile update failed', 'details': str(e)}), 500

@application_bp.route('/admin/<int:application_id>', methods=['GET'])
@auth_token_required
@roles_required('admin')
def admin_get_application(application_id):
    """Get specific application details (admin only)"""
    try:
        application = Application.query.get_or_404(application_id)
        
        app_data = {
            'id': application.id,
            'student_id': application.student_id,
            'student_name': application.student.name,
            'student_email': application.student.email,
            'course_applied': application.course_applied,
            'status': application.status,
            'submitted_at': application.submitted_at.isoformat() if application.submitted_at else None,
            'review_comments': application.review_comments,
            'academic_records': application.academic_records,
            'personal_statement': application.personal_statement,
            'phone': application.phone,
            'address': application.address,
            'emergency_contact': application.emergency_contact,
            'date_of_birth': application.date_of_birth.isoformat() if application.date_of_birth else None,
            'gender': application.gender,
            'nationality': application.nationality,
            'passport_number': application.passport_number,
            'has_documents': bool(application.documents_path),
            'has_transcript': bool(application.transcript_path),
            'has_personal_statement': bool(application.personal_statement_path)
        }
        
        if application.reviewed_at:
            app_data['reviewed_at'] = application.reviewed_at.isoformat()
            
        if application.reviewer:
            app_data['reviewed_by'] = {
                'name': application.reviewer.name,
                'email': application.reviewer.email
            }
        
        return jsonify({
            'application': app_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get application details', 'details': str(e)}), 500

# Admin-only routes
@application_bp.route('/admin/list-all', methods=['GET'])
@auth_token_required
@roles_required('admin')
def admin_list_all_applications():
    """Get all applications with pagination and filtering (admin only)"""
    try:
        # Get query parameters
        status = request.args.get('status', None)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Build query
        query = Application.query
        
        if status:
            query = query.filter_by(status=status)
        
        # Paginate results
        applications = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        applications_list = []
        for app in applications.items:
            app_data = {
                'id': app.id,
                'course_applied': app.course_applied,
                'status': app.status,
                'tenth_percentage': app.tenth_percentage,
                'tenth_board': app.tenth_board,
                'twelfth_percentage': app.twelfth_percentage,
                'twelfth_board': app.twelfth_board,
                'previous_qualification': app.previous_qualification,
                'previous_institution': app.previous_institution,
                'graduation_year': app.graduation_year,
                'date_created': app.date_created.isoformat(),
                'review_comments': app.review_comments,
                'reviewed_at': app.reviewed_at.isoformat() if app.reviewed_at else None,
                # Add address fields
                'address': app.address,
                'country': app.country,
                'state': app.state,
                'district': app.district,
                'pincode': app.pincode,
                # Add document info (filenames only, not the binary data)
                'degree_certificate_filename': app.degree_certificate_filename,
                'id_proof_filename': app.id_proof_filename,
                'has_degree_certificate': bool(app.degree_certificate),
                'has_id_proof': bool(app.id_proof),
                'student': {
                    'id': app.student.id,
                    'name': app.student.name,
                    'email': app.student.email,
                    'phone': app.student.phone
                }
            }
            
            if app.reviewer:
                app_data['reviewed_by'] = {
                    'name': app.reviewer.name,
                    'email': app.reviewer.email
                }
            
            applications_list.append(app_data)
        
        return jsonify({
            'applications': applications_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': applications.total,
                'pages': applications.pages,
                'has_next': applications.has_next,
                'has_prev': applications.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve applications', 'details': str(e)}), 500

@application_bp.route('/admin/review/<int:application_id>', methods=['POST'])
@auth_token_required
@roles_required('admin')
def admin_review_application(application_id):
    """Review an application (admin only)"""
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        action = data.get('action')  # 'approve' or 'reject'
        comments = data.get('comments', '')
        
        current_app.logger.info(f"Admin review request - Application ID: {application_id}, Action: {action}, Comments: {comments}")
        
        if action not in ['approve', 'reject']:
            return jsonify({'error': 'Action must be approve or reject'}), 400
        
        application.status = 'approved' if action == 'approve' else 'rejected'
        application.reviewer_id = current_user.id
        application.review_comments = comments
        application.reviewed_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        current_app.logger.info(f"Application {application_id} {action}d successfully by admin {current_user.id}")
        
        return jsonify({
            'message': f'Application {action}d successfully',
            'application': {
                'id': application.id,
                'status': application.status,
                'review_comments': application.review_comments,
                'reviewed_at': application.reviewed_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Application review failed for ID {application_id}: {str(e)}")
        return jsonify({'error': 'Application review failed', 'details': str(e)}), 500

@application_bp.route('/admin/document/<int:application_id>/<document_type>', methods=['GET'])
@auth_token_required
@roles_required('admin')
def admin_view_document(application_id, document_type):
    """View/download application documents (admin only)"""
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Map document types to database fields
        document_fields = {
            'degree_certificate': ('degree_certificate', 'degree_certificate_filename'),
            'id_proof': ('id_proof', 'id_proof_filename')
        }
        
        if document_type not in document_fields:
            return jsonify({'error': 'Invalid document type'}), 400
        
        data_field, filename_field = document_fields[document_type]
        document_data = getattr(application, data_field)
        document_filename = getattr(application, filename_field)
        
        if not document_data:
            return jsonify({'error': 'Document not found'}), 404
        
        # Get the action parameter (view or download)
        action = request.args.get('action', 'view')
        
        if action == 'base64':
            # Return base64 encoded data for preview
            encoded_data = base64.b64encode(document_data).decode('utf-8')
            return jsonify({
                'filename': document_filename,
                'data': encoded_data,
                'content_type': 'application/octet-stream'
            })
        else:
            # Return file for download/view
            file_obj = io.BytesIO(document_data)
            
            # Determine content type based on file extension
            file_ext = document_filename.lower().split('.')[-1] if '.' in document_filename else ''
            content_type = {
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }.get(file_ext, 'application/octet-stream')
            
            return send_file(
                file_obj,
                as_attachment=(action == 'download'),
                download_name=document_filename,
                mimetype=content_type
            )
    
    except Exception as e:
        current_app.logger.error(f"Document viewing failed for application {application_id}, document {document_type}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve document', 'details': str(e)}), 500

@application_bp.route('/document/<int:application_id>/<document_type>', methods=['GET'])
@auth_token_required
def view_document(application_id, document_type):
    """View/download user's own application documents"""
    try:
        # Users can only view their own application documents
        application = Application.query.filter_by(
            id=application_id, 
            student_id=current_user.id
        ).first()
        
        if not application:
            return jsonify({'error': 'Application not found or access denied'}), 404
        
        # Map document types to database fields
        document_fields = {
            'degree_certificate': ('degree_certificate', 'degree_certificate_filename'),
            'id_proof': ('id_proof', 'id_proof_filename')
        }
        
        if document_type not in document_fields:
            return jsonify({'error': 'Invalid document type'}), 400
        
        data_field, filename_field = document_fields[document_type]
        document_data = getattr(application, data_field)
        document_filename = getattr(application, filename_field)
        
        if not document_data:
            return jsonify({'error': 'Document not found'}), 404
        
        # Get the action parameter (view or download)
        action = request.args.get('action', 'view')
        
        if action == 'base64':
            # Return base64 encoded data for preview
            encoded_data = base64.b64encode(document_data).decode('utf-8')
            return jsonify({
                'filename': document_filename,
                'data': encoded_data,
                'content_type': 'application/octet-stream'
            })
        else:
            # Return file for download/view
            file_obj = io.BytesIO(document_data)
            
            # Determine content type based on file extension
            file_ext = document_filename.lower().split('.')[-1] if '.' in document_filename else ''
            content_type = {
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }.get(file_ext, 'application/octet-stream')
            
            return send_file(
                file_obj,
                as_attachment=(action == 'download'),
                download_name=document_filename,
                mimetype=content_type
            )
    
    except Exception as e:
        current_app.logger.error(f"User document viewing failed for application {application_id}, document {document_type}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve document', 'details': str(e)}), 500

@application_bp.route('/offer-letter/<int:application_id>', methods=['GET'])
@auth_token_required
def download_offer_letter(application_id):
    """Generate and download offer letter for approved applications"""
    try:
        # Users can only download their own offer letter
        application = Application.query.filter_by(
            id=application_id, 
            student_id=current_user.id,
            status='approved'
        ).first()
        
        if not application:
            return jsonify({'error': 'Approved application not found or access denied'}), 404
        
        # Generate offer letter PDF
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=30,
            bottomMargin=30
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Professional color scheme
        dark_blue = colors.Color(0.2, 0.2, 0.4)
        light_gray = colors.Color(0.95, 0.95, 0.95)
        
        # Enhanced typography styles
        letterhead_style = ParagraphStyle(
            'Letterhead',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=5,
            textColor=dark_blue,
            alignment=1,
            fontName='Helvetica-Bold',
            letterSpacing=1
        )
        
        department_style = ParagraphStyle(
            'Department',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=20,
            textColor=colors.black,
            alignment=1,
            fontName='Helvetica',
            letterSpacing=0.5
        )
        
        document_title_style = ParagraphStyle(
            'DocumentTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            spaceBefore=20,
            textColor=colors.black,
            alignment=1,
            fontName='Helvetica-Bold',
            letterSpacing=2
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=10,
            spaceAfter=5,
            spaceBefore=10,
            textColor=dark_blue,
            fontName='Helvetica-Bold',
            backColor=light_gray,
            borderPadding=3
        )
        
        # LETTERHEAD
        story.append(Paragraph("UNIADMIT UNIVERSITY", letterhead_style))
        story.append(Paragraph("OFFICE OF ADMISSIONS", department_style))
        
        # University Address - reduced spacing
        address_style = ParagraphStyle(
            'AddressStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            alignment=1,
            spaceAfter=8
        )
        story.append(Paragraph("123 Education Avenue, Academic City, State 12345<br/>Phone: +1-555-0123 | Email: admissions@uniadmit.edu", address_style))
        
        # Horizontal line under letterhead
        line = Drawing(480, 2)
        line.add(Rect(0, 0, 480, 2, fillColor=dark_blue, strokeColor=None))
        story.append(line)
        story.append(Spacer(1, 15))
        
        # DOCUMENT TITLE
        document_title_style = ParagraphStyle(
            'DocumentTitle',
            parent=styles['Title'],
            fontSize=12,
            textColor=dark_blue,
            alignment=1,
            fontName='Helvetica-Bold',
            spaceAfter=10,
            leading=14
        )
        story.append(Paragraph("OFFICIAL LETTER OF ADMISSION", document_title_style))
        
        # Document reference and date - reduced spacing
        ref_date_data = [
            [f"Reference No: ADM/{application.id:04d}/{datetime.now().year}", f"Date: {datetime.now().strftime('%B %d, %Y')}"]
        ]
        ref_table = Table(ref_date_data, colWidths=[3*inch, 3*inch])
        ref_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(ref_table)
        story.append(Spacer(1, 10))
        
        # ADDRESSEE SECTION - reduced spacing
        addressee_style = ParagraphStyle(
            'AddresseeStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            spaceAfter=10,
            leftIndent=0
        )
        
        story.append(Paragraph(f"<b>To:</b><br/>{application.student.name}<br/>{application.student.email}<br/>{application.student.phone}", addressee_style))
        
        # SUBJECT LINE - reduced spacing
        subject_style = ParagraphStyle(
            'SubjectStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            spaceAfter=10
        )
        story.append(Paragraph(f"<b>Subject: Admission Approval for {application.course_applied}</b>", subject_style))
        
        # SALUTATION - reduced spacing
        salutation_style = ParagraphStyle(
            'SalutationStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            spaceAfter=10
        )
        story.append(Paragraph("Dear Mr./Ms. " + application.student.name.split()[-1] + ",", salutation_style))
        
        # MAIN CONTENT SECTIONS
        
        # Section 1: STUDENT INFORMATION
        story.append(Paragraph("1. STUDENT INFORMATION", section_title_style))
        student_data = [
            ['Full Name:', application.student.name],
            ['Email Address:', application.student.email],
            ['Contact Number:', application.student.phone],
            ['Application Reference:', f"ADM/{application.id:04d}/{datetime.now().year}"]
        ]
        
        student_table = Table(student_data, colWidths=[1.5*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        story.append(student_table)
        
        # Section 2: ADMISSION DECISION - reduced spacing
        admission_decision_style = ParagraphStyle(
            'AdmissionDecision',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            spaceAfter=8,
            leading=11,
            leftIndent=10,
            rightIndent=10
        )
        
        story.append(Paragraph("2. ADMISSION DECISION", section_title_style))
        story.append(Paragraph(
            f"We are pleased to inform you that your application for admission to <b>{application.course_applied}</b> "
            f"for the academic year <b>{application.graduation_year}-{application.graduation_year + 1}</b> has been "
            f"<b>APPROVED</b> by our Admissions Committee.<br/><br/>"
            f"Your academic credentials and qualifications have been thoroughly reviewed and found to meet "
            f"our university's admission standards.",
            admission_decision_style
        ))
        
        # Section 3: PROGRAM DETAILS
        story.append(Paragraph("3. PROGRAM DETAILS", section_title_style))
        program_data = [
            ['Program of Study:', application.course_applied],
            ['Academic Year:', f"{application.graduation_year}-{application.graduation_year + 1}"],
            ['Duration:', 'As per program curriculum'],
            ['Campus:', 'Main Campus, Academic City']
        ]
        
        program_table = Table(program_data, colWidths=[1.5*inch, 4*inch])
        program_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        story.append(program_table)
        
        # Section 4: ACADEMIC QUALIFICATIONS
        story.append(Paragraph("4. ACADEMIC QUALIFICATIONS REVIEWED", section_title_style))
        academic_data = [
            ['10th Grade Results:', f"{application.tenth_percentage}% from {application.tenth_board}"],
            ['12th Grade Results:', f"{application.twelfth_percentage}% from {application.twelfth_board}"],
            ['Previous Qualification:', application.previous_qualification],
            ['Previous Institution:', application.previous_institution]
        ]
        
        academic_table = Table(academic_data, colWidths=[1.8*inch, 3.7*inch])
        academic_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        story.append(academic_table)
        
        # Section 5: CONDITIONS AND REQUIREMENTS
        story.append(Paragraph("5. CONDITIONS AND NEXT STEPS", section_title_style))
        
        conditions_style = ParagraphStyle(
            'ConditionsStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            leftIndent=12,
            bulletIndent=3,
            spaceAfter=2,
            leading=10
        )
        
        conditions_text = [
            "a) Accept this admission offer through the student portal within <b>15 calendar days</b> from the date of this letter.",
            "b) Complete the fee payment process as outlined in the Fee Structure document (to be provided separately).",
            "c) Submit original academic documents for verification to the Registrar's Office.",
            "d) Complete medical examination and submit health clearance certificate.",
            "e) Attend the mandatory orientation program scheduled before commencement of classes.",
            "f) Comply with all university policies and regulations as outlined in the Student Handbook."
        ]
        
        for condition in conditions_text:
            story.append(Paragraph(condition, conditions_style))
        
        story.append(Spacer(1, 8))
        
        # Section 6: IMPORTANT DEADLINES
        story.append(Paragraph("6. IMPORTANT DEADLINES", section_title_style))
        
        deadlines_data = [
            ['Acceptance Deadline:', (datetime.now() + timedelta(days=15)).strftime('%B %d, %Y')],
            ['Document Submission:', (datetime.now() + timedelta(days=30)).strftime('%B %d, %Y')],
            ['Fee Payment Deadline:', (datetime.now() + timedelta(days=45)).strftime('%B %d, %Y')],
            ['Orientation Date:', 'To be announced separately']
        ]
        
        deadlines_table = Table(deadlines_data, colWidths=[2*inch, 3.5*inch])
        deadlines_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        story.append(deadlines_table)
        
        # Section 7: CONTACT INFORMATION
        story.append(Paragraph("7. CONTACT INFORMATION", section_title_style))
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            spaceAfter=8
        )
        
        story.append(Paragraph(
            "For any queries or assistance regarding your admission, please contact:<br/><br/>"
            "<b>Admissions Office</b><br/>"
            "Phone: +1-555-0123 | Email: admissions@uniadmit.edu<br/>"
            "Office Hours: Monday to Friday, 9:00 AM to 5:00 PM",
            contact_style
        ))
        
        # CLOSING - reduced spacing
        closing_style = ParagraphStyle(
            'ClosingStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            spaceAfter=10,
            leading=12
        )
        
        story.append(Paragraph(
            "We congratulate you on this achievement and look forward to welcoming you to the UniAdmit University community. "
            "We are confident that you will make significant contributions to our academic environment.",
            closing_style
        ))
        
        story.append(Paragraph("Sincerely,", closing_style))
        
        # SIGNATURES SECTION - reduced spacing
        story.append(Spacer(1, 15))
        
        signature_style = ParagraphStyle(
            'SignatureStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.black,
            leading=10
        )
        
        # Create signature table - reduced spacing
        signature_data = [
            ['', ''],
            ['_________________________', '_________________________'],
            ['Dr. Sarah Johnson', 'Prof. Michael Chen'],
            ['Director of Admissions', 'Registrar'],
            ['UniAdmit University', 'UniAdmit University']
        ]
        
        signature_table = Table(signature_data, colWidths=[2.7*inch, 2.7*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(signature_table)
        
        # FOOTER - reduced spacing
        story.append(Spacer(1, 10))
        
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=7,
            textColor=colors.grey,
            alignment=1,  # Center alignment
            leading=8
        )
        
        story.append(Paragraph(
            "This is an official document from UniAdmit University Admissions Office<br/>"
            "Please retain this letter for your records<br/><br/>"
            f"Document Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            footer_style
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        pdf_size = len(pdf_data)
        
        print(f"PDF generated successfully for application {application_id}, size: {pdf_size} bytes")
        
        if pdf_size == 0:
            raise ValueError("Generated PDF is empty")
        
        buffer.close()
        
        filename = f"offer_letter_{application.student.name.replace(' ', '_')}_{application.id}.pdf"
        
        # Create a new BytesIO object with the PDF data
        pdf_buffer = io.BytesIO(pdf_data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        current_app.logger.error(f"Offer letter generation failed for application {application_id}: {str(e)}")
        return jsonify({'error': 'Failed to generate offer letter', 'details': str(e)}), 500

@application_bp.route('/admin/stats', methods=['GET'])
@auth_token_required
@roles_required('admin')
def admin_get_statistics():
    """Get comprehensive statistics for admin dashboard"""
    try:
        from sqlalchemy import func
        
        # Total counts
        total_applications = Application.query.count()
        pending_applications = Application.query.filter_by(status='pending').count()
        approved_applications = Application.query.filter_by(status='approved').count()
        rejected_applications = Application.query.filter_by(status='rejected').count()
        draft_applications = Application.query.filter_by(status='draft').count()
        
        # Course-wise statistics
        course_stats = db.session.query(
            Application.course_applied,
            func.count(Application.id).label('count')
        ).group_by(Application.course_applied).all()
        
        # Monthly statistics (last 12 months)
        from datetime import datetime, timedelta
        twelve_months_ago = datetime.now() - timedelta(days=365)
        monthly_stats = db.session.query(
            func.DATE_FORMAT(Application.date_created, '%Y-%m').label('month'),
            func.count(Application.id).label('count')
        ).filter(Application.date_created >= twelve_months_ago).group_by('month').all()
        
        # Recent activity
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_applications = Application.query.filter(
            Application.date_created >= seven_days_ago
        ).count()
        
        # Average approval rate
        reviewed_apps = Application.query.filter(
            Application.status.in_(['approved', 'rejected'])
        ).count()
        approval_rate = (approved_applications / reviewed_apps * 100) if reviewed_apps > 0 else 0
        
        return jsonify({
            'overview': {
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'approved_applications': approved_applications,
                'rejected_applications': rejected_applications,
                'draft_applications': draft_applications,
                'approval_rate_percentage': round(approval_rate, 2)
            },
            'course_wise_stats': [
                {'course': stat.course_applied, 'count': stat.count}
                for stat in course_stats
            ],
            'monthly_trends': [
                {'month': stat.month, 'count': stat.count}
                for stat in monthly_stats
            ],
            'recent_activity': {
                'applications_last_7_days': recent_applications
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get statistics', 'details': str(e)}), 500

@application_bp.route('/admin/download-file/<int:application_id>/<file_type>', methods=['GET'])
@auth_token_required
@roles_required('admin')
def admin_download_application_file(application_id, file_type):
    """Download application files (admin only)"""
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        if file_type == 'degree_certificate':
            file_data = application.degree_certificate
            filename = application.degree_certificate_filename
        elif file_type == 'id_proof':
            file_data = application.id_proof
            filename = application.id_proof_filename
        else:
            return jsonify({'error': 'Invalid file type. Use degree_certificate or id_proof'}), 400
        
        if not file_data:
            return jsonify({'error': 'File not found'}), 404
        
        # Return file as base64 encoded string
        file_base64 = base64.b64encode(file_data).decode('utf-8')
        
        return jsonify({
            'filename': filename,
            'file_data': file_base64,
            'file_type': file_type,
            'student': {
                'name': application.student.name,
                'email': application.student.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to download file', 'details': str(e)}), 500

@application_bp.route('/admin/search', methods=['GET'])
@auth_token_required
@roles_required('admin')
def admin_search_applications():
    """Advanced search for applications (admin only)"""
    try:
        query = Application.query
        
        # Filter by status
        status = request.args.get('status')
        if status:
            query = query.filter(Application.status == status)
        
        # Filter by course
        course = request.args.get('course')
        if course:
            query = query.filter(Application.course_applied.ilike(f'%{course}%'))
        
        # Filter by student name
        student_name = request.args.get('student_name')
        if student_name:
            query = query.join(User).filter(User.name.ilike(f'%{student_name}%'))
        
        # Filter by date range
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date:
            query = query.filter(Application.date_created >= start_date)
        if end_date:
            query = query.filter(Application.date_created <= end_date)
        
        # Filter by percentage range
        min_percentage = request.args.get('min_percentage', type=float)
        max_percentage = request.args.get('max_percentage', type=float)
        if min_percentage is not None:
            query = query.filter(Application.twelfth_percentage >= min_percentage)
        if max_percentage is not None:
            query = query.filter(Application.twelfth_percentage <= max_percentage)
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        applications = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'applications': [{
                'id': app.id,
                'student': {
                    'name': app.student.name,
                    'email': app.student.email
                },
                'course_applied': app.course_applied,
                'status': app.status,
                'twelfth_percentage': app.twelfth_percentage,
                'date_created': app.date_created.isoformat(),
                'review_comments': app.review_comments
            } for app in applications.items],
            'pagination': {
                'page': applications.page,
                'per_page': applications.per_page,
                'total': applications.total,
                'pages': applications.pages
            },
            'filters_applied': {
                'status': status,
                'course': course,
                'student_name': student_name,
                'start_date': start_date,
                'end_date': end_date,
                'min_percentage': min_percentage,
                'max_percentage': max_percentage
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@application_bp.route('/admin/bulk-action', methods=['POST'])
@auth_token_required
@roles_required('admin')
def admin_bulk_action():
    """Perform bulk actions on applications (admin only)"""
    try:
        data = request.get_json()
        application_ids = data.get('application_ids', [])
        action = data.get('action')  # 'approve', 'reject', 'delete'
        comments = data.get('comments', '')
        
        if not application_ids or not action:
            return jsonify({'error': 'application_ids and action are required'}), 400
        
        if action not in ['approve', 'reject', 'delete']:
            return jsonify({'error': 'Action must be approve, reject, or delete'}), 400
        
        applications = Application.query.filter(Application.id.in_(application_ids)).all()
        
        if not applications:
            return jsonify({'error': 'No applications found'}), 404
        
        updated_applications = []
        failed_updates = []
        
        for app in applications:
            try:
                if action in ['approve', 'reject']:
                    if app.status == 'pending':
                        app.status = 'approved' if action == 'approve' else 'rejected'
                        app.reviewer_id = current_user.id
                        app.review_comments = comments
                        app.reviewed_at = datetime.now(timezone.utc)
                        updated_applications.append({
                            'id': app.id,
                            'student_name': app.student.name,
                            'course': app.course_applied,
                            'new_status': app.status
                        })
                    else:
                        failed_updates.append({
                            'id': app.id,
                            'reason': f'Cannot {action} application with status: {app.status}'
                        })
                elif action == 'delete':
                    updated_applications.append({
                        'id': app.id,
                        'student_name': app.student.name,
                        'course': app.course_applied,
                        'action': 'deleted'
                    })
                    db.session.delete(app)
            except Exception as e:
                failed_updates.append({
                    'id': app.id,
                    'reason': str(e)
                })
        
        db.session.commit()
        
        return jsonify({
            'message': f'Bulk {action} operation completed',
            'total_processed': len(application_ids),
            'successful_updates': len(updated_applications),
            'failed_updates': len(failed_updates),
            'updated_applications': updated_applications,
            'failed_updates': failed_updates,
            'action_performed': action,
            'comments_added': comments
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Bulk action failed', 'details': str(e)}), 500
