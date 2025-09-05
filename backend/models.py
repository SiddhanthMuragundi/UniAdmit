from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timezone
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

# Association table for roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    date_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    applications = db.relationship(
        'Application',
        backref='student',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    course_applied = db.Column(db.String(255), nullable=False)
    
    # Academic details
    tenth_percentage = db.Column(db.Float, nullable=False)
    tenth_board = db.Column(db.String(255), nullable=False)
    twelfth_percentage = db.Column(db.Float, nullable=False)
    twelfth_board = db.Column(db.String(255), nullable=False)
    
    previous_qualification = db.Column(db.String(255), nullable=False)
    previous_institution = db.Column(db.String(255), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    
    # Address details
    address = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    
    # Document files stored as binary data
    degree_certificate = db.Column(db.LargeBinary, nullable=False)
    degree_certificate_filename = db.Column(db.String(255), nullable=False)
    id_proof = db.Column(db.LargeBinary, nullable=False)
    id_proof_filename = db.Column(db.String(255), nullable=False)
    
    # Application status
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, rejected
    
    # Review details
    reviewed_by = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='SET NULL'),
        nullable=True
    )
    review_comments = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # Admission details (for approved applications)
    admission_letter_path = db.Column(db.String(500), nullable=True)
    
    date_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])

# Enable foreign key support for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        pass