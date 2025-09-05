# Functional Requirement Document (FRD)
## UniAdmit University Admission Management System

### Document Information
- **Project:** UniAdmit University Admission Management System
- **Version:** 1.0
- **Date:** September 6, 2025
- **Document Type:** Functional Requirement Document

---

## 1. EXECUTIVE SUMMARY

### 1.1 Project Overview
The UniAdmit University Admission Management System is a comprehensive web-based application designed to streamline the university admission process for both students and administrative staff. The system provides a complete end-to-end solution for application submission, review, and management.

### 1.2 Business Objectives
- Digitize and automate the university admission process
- Reduce manual paperwork and processing time
- Provide transparent application tracking for students
- Enable efficient application review and management for administrators
- Generate comprehensive reports and analytics

### 1.3 System Overview
- **Frontend:** Vue.js 3 with Bootstrap 5 for responsive UI
- **Backend:** Flask with SQLAlchemy ORM and MySQL database
- **Authentication:** Flask-Security with role-based access control
- **File Management:** Binary storage for document uploads
- **PDF Generation:** ReportLab for official admission letters

---

## 2. STAKEHOLDER ANALYSIS

### 2.1 Primary Stakeholders
1. **Students/Applicants**
   - Submit admission applications
   - Track application status
   - Upload required documents
   - Receive admission decisions

2. **Admission Officers/Administrators**
   - Review and evaluate applications
   - Approve or reject applications
   - Generate admission letters
   - Manage application workflow

3. **System Administrators**
   - Manage user accounts
   - Configure system settings
   - Monitor system performance
   - Maintain data integrity

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 User Authentication and Authorization

#### 3.1.1 User Registration (FR-001)
**Description:** Allow new users to create accounts in the system.

**Requirements:**
- Users must provide: full name, email, phone number, password, complete address
- Email must be unique in the system
- Phone number must be exactly 10 digits
- Password must be minimum 6 characters
- Address fields: street address, country (text input), state, district, PIN code
- Account activation upon successful registration

**Acceptance Criteria:**
- Registration form validates all required fields
- System prevents duplicate email registrations
- User receives confirmation upon successful registration
- Account is immediately active for login

#### 3.1.2 User Login (FR-002)
**Description:** Authenticate users and provide access to appropriate features.

**Requirements:**
- Login using email and password
- Role-based access control (Student/Admin)
- Session management with authentication tokens
- Automatic logout after inactivity
- Remember user session across browser sessions

**Acceptance Criteria:**
- Valid credentials grant access to appropriate dashboard
- Invalid credentials show error message
- Role-based navigation and feature access
- Secure token-based authentication

#### 3.1.3 User Logout (FR-003)
**Description:** Allow users to securely terminate their session.

**Requirements:**
- Logout button in navigation bar dropdown
- Clear authentication tokens
- Redirect to login page
- Session cleanup

**Acceptance Criteria:**
- Logout button accessible from any page
- Complete session termination
- Cannot access protected pages after logout

### 3.2 Student Application Management

#### 3.2.1 Application Creation (FR-004)
**Description:** Enable students to create new admission applications.

**Requirements:**
- Multi-step application form with 4 stages:
  1. Basic Information (course, graduation year, previous qualification)
  2. Academic Details (10th/12th grade marks and boards)
  3. Document Upload (degree certificate, ID proof)
  4. Review and Submit
- Progress indicator showing current step
- Form validation at each step
- Save draft functionality at any stage

**Acceptance Criteria:**
- Step-by-step navigation with progress indication
- Field validation prevents invalid data entry
- Cannot proceed to next step without completing current step
- Draft saving works without requiring all fields

#### 3.2.2 Draft Management (FR-005)
**Description:** Allow students to save and continue applications later.

**Requirements:**
- Save draft without requiring all fields to be filled
- Auto-load existing draft when student returns
- Visual indication when editing a draft
- Smart step detection to start where user left off
- Overwrite existing draft with new saves

**Acceptance Criteria:**
- Empty form can be saved as draft
- Draft loads with previously entered data
- Form starts at appropriate step based on completion
- Clear indication that user is editing a draft

#### 3.2.3 Application Submission (FR-006)
**Description:** Allow students to submit completed applications for review.

**Requirements:**
- Final validation of all required fields
- Document upload verification
- Convert draft status to "pending"
- Confirmation message with application ID
- Prevent multiple submissions

**Acceptance Criteria:**
- All required fields must be filled before submission
- Both documents must be uploaded
- Application status changes to "pending"
- Student receives confirmation with unique application ID

#### 3.2.4 Application Status Tracking (FR-007)
**Description:** Enable students to track their application progress.

**Requirements:**
- Dashboard showing current application status
- Detailed status information with dates
- Course applied for and application ID
- Status-specific messages and guidance
- Access to submitted application details

**Acceptance Criteria:**
- Real-time status updates
- Clear status messages (draft, pending, approved, rejected)
- Application details viewable after submission
- Status history with timestamps

### 3.3 Document Management

#### 3.3.1 Document Upload (FR-008)
**Description:** Allow students to upload required documents.

**Requirements:**
- Support for PDF, JPG, PNG formats
- Maximum file size limit (10MB per file)
- Required documents: degree certificate, ID proof
- File preview and validation
- Secure storage in database

**Acceptance Criteria:**
- Only specified file formats accepted
- File size validation prevents oversized uploads
- Uploaded files viewable by student and admin
- Files stored securely with proper naming

#### 3.3.2 Document Download (FR-009)
**Description:** Enable authorized users to download uploaded documents.

**Requirements:**
- Students can download their own documents
- Administrators can download any application documents
- File integrity preservation
- Access control based on user roles

**Acceptance Criteria:**
- Download preserves original file format and quality
- Proper access control prevents unauthorized downloads
- File names are meaningful and identifiable

### 3.4 Administrative Functions

#### 3.4.1 Application Review (FR-010)
**Description:** Enable administrators to review and evaluate applications.

**Requirements:**
- List all applications with filtering and search capabilities
- Detailed application view with all submitted information
- Document viewing and download functionality
- Application status management (approve/reject)
- Review comments and feedback

**Acceptance Criteria:**
- Complete application information displayed clearly
- Documents accessible for review
- Status changes tracked with timestamps
- Review comments saved with applications

#### 3.4.2 Admission Letter Generation (FR-011)
**Description:** Generate official admission letters for approved applications.

**Requirements:**
- Professional PDF format with university letterhead
- Structured content with applicant and program details
- Academic qualifications summary
- Terms and conditions
- Digital signatures and official formatting
- Automatic generation upon approval

**Acceptance Criteria:**
- PDF contains all required information
- Professional formatting and layout
- Consistent branding and design
- Letter fits within 2 pages
- Generated automatically for approved applications

#### 3.4.3 Bulk Operations (FR-012)
**Description:** Enable administrators to perform operations on multiple applications.

**Requirements:**
- Bulk approve/reject functionality
- Bulk status updates
- Mass communication capabilities
- Batch processing with error handling

**Acceptance Criteria:**
- Multiple applications can be selected and processed
- Status updates apply to all selected applications
- Error handling for failed operations
- Audit trail for bulk operations

### 3.5 Dashboard and Analytics

#### 3.5.1 Student Dashboard (FR-013)
**Description:** Provide students with personalized dashboard showing their application status and options.

**Requirements:**
- Application status card with detailed information
- Quick access to create new application
- Draft continuation functionality
- Profile management links
- Recent activity timeline

**Acceptance Criteria:**
- Dashboard shows current application status
- Easy navigation to all student functions
- Visual indicators for draft applications
- Responsive design for all devices

#### 3.5.2 Admin Dashboard (FR-014)
**Description:** Provide administrators with comprehensive overview and management tools.

**Requirements:**
- Application statistics and metrics
- Recent activity feed
- Quick access to review functions
- System analytics and reports
- User management capabilities

**Acceptance Criteria:**
- Real-time statistics display
- Easy access to all administrative functions
- Visual charts and graphs for data
- Comprehensive activity tracking

### 3.6 System Administration

#### 3.6.1 User Management (FR-015)
**Description:** Enable system administrators to manage user accounts.

**Requirements:**
- View all user accounts
- Role assignment and modification
- Account activation/deactivation
- Password reset capabilities
- User activity monitoring

**Acceptance Criteria:**
- Complete user listing with search and filter
- Role changes take effect immediately
- Account status changes reflected in system access
- Activity logs maintained for audit purposes

#### 3.6.2 System Configuration (FR-016)
**Description:** Allow administrators to configure system settings.

**Requirements:**
- Application deadlines management
- System announcements
- Email notification settings
- Document upload limits
- Security parameter configuration

**Acceptance Criteria:**
- Configuration changes apply system-wide
- Settings persist across system restarts
- Validation prevents invalid configuration
- Change history maintained

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### 4.1 Performance Requirements
- **Response Time:** Page loads within 3 seconds under normal conditions
- **Throughput:** Support 100 concurrent users
- **Scalability:** Architecture supports horizontal scaling
- **Database Performance:** Query response time under 1 second

### 4.2 Security Requirements
- **Authentication:** Secure token-based authentication
- **Authorization:** Role-based access control
- **Data Protection:** Encryption for sensitive data
- **Input Validation:** SQL injection and XSS prevention
- **Session Management:** Secure session handling with timeout

### 4.3 Usability Requirements
- **User Interface:** Intuitive and responsive design
- **Accessibility:** WCAG 2.1 compliance
- **Browser Support:** Modern browsers (Chrome, Firefox, Safari, Edge)
- **Mobile Support:** Responsive design for mobile devices
- **User Guidance:** Clear instructions and error messages

### 4.4 Reliability Requirements
- **Availability:** 99.5% uptime during business hours
- **Error Handling:** Graceful error handling with user-friendly messages
- **Data Backup:** Regular automated backups
- **Recovery Time:** System recovery within 4 hours of failure

### 4.5 Compatibility Requirements
- **Platform Independence:** Web-based accessible from any OS
- **Database Compatibility:** MySQL 8.0 or higher
- **Framework Compatibility:** Vue.js 3, Flask 2.0+
- **File Format Support:** PDF, JPG, PNG for document uploads

---

## 5. BUSINESS RULES

### 5.1 Application Business Rules
1. Each student can have only one active application at a time
2. Applications cannot be modified after submission (pending status)
3. Draft applications can be saved without complete information
4. Submitted applications require all mandatory fields and documents
5. Application ID is unique and auto-generated

### 5.2 User Business Rules
1. Email addresses must be unique across all users
2. Students can only view and manage their own applications
3. Administrators can view and manage all applications
4. Phone numbers must be exactly 10 digits for registration
5. Passwords must meet minimum security requirements

### 5.3 Document Business Rules
1. Maximum file size of 10MB per document
2. Only PDF, JPG, PNG formats accepted
3. Two documents required: degree certificate and ID proof
4. Documents stored securely with access control
5. Original file names preserved for reference

### 5.4 Status Business Rules
1. Application status flow: Draft → Pending → Approved/Rejected
2. Only administrators can change application status
3. Status changes are logged with timestamp and reviewer information
4. Approved applications automatically generate admission letters
5. Rejected applications cannot be resubmitted (new application required)

---

## 6. ASSUMPTIONS AND CONSTRAINTS

### 6.1 Assumptions
- Users have basic computer literacy and internet access
- Modern web browsers are available to all users
- Email system is available for notifications
- University branding and content are provided
- Database server has sufficient storage capacity

### 6.2 Constraints
- Budget limitations for infrastructure
- Timeline constraints for development phases
- Integration with existing university systems may be required
- Compliance with educational data protection regulations
- Limited customization of core workflow processes

---

## 7. ACCEPTANCE CRITERIA

### 7.1 System Acceptance
- All functional requirements implemented and tested
- Non-functional requirements meet specified criteria
- Security requirements validated through testing
- Performance benchmarks achieved
- User acceptance testing completed successfully

### 7.2 User Acceptance
- Students can complete application process without assistance
- Administrators can efficiently manage application workflow
- System provides clear feedback and guidance
- Error handling provides meaningful user guidance
- Overall user satisfaction meets expectations

---

## 8. GLOSSARY

- **Admin Dashboard:** A centralized interface providing administrators with tools to manage applications, users, and system settings

- **Application:** A formal request for admission submitted by a student containing personal information, academic details, and supporting documents

- **Application Status:** The current state of an application in the workflow (Draft, Pending, Under Review, Approved, Rejected)

- **Authentication:** The process of verifying user identity through credentials (email and password)

- **Authorization:** The process of determining what resources and actions an authenticated user is permitted to access

- **Binary Storage:** Method of storing files (documents, images) as binary data directly in the database

- **Dashboard:** A user interface that provides an overview of key information and quick access to main functions

- **Draft:** An incomplete application that has been saved for later completion and submission

- **Admission Letter/Offer Letter:** Official PDF document confirming admission approval, generated automatically by the system

- **JWT (JSON Web Token):** A secure method for transmitting information between parties as a JSON object, used for session management

- **Multi-step Form:** A user interface pattern that breaks long forms into sequential sections or steps to improve user experience

- **ORM (Object-Relational Mapping):** A programming technique that converts data between incompatible type systems using object-oriented programming languages

- **PDF Generation:** Automated creation of PDF documents (admission letters) using the ReportLab library

- **Responsive Design:** Web design approach that ensures optimal viewing experience across different devices and screen sizes

- **Role-based Access Control (RBAC):** Security model that restricts system access based on assigned user roles (Student, Administrator)

- **Session Management:** Handling user login sessions, authentication state, and security tokens

- **SQLAlchemy:** Python SQL toolkit and ORM providing database abstraction layer

- **Stakeholder:** Individual or group with interest in or influence over the project (students, administrators, system administrators)

- **Upload Validation:** Process of checking uploaded files for format, size, and content requirements

- **User Role:** A designation that determines a user's permissions and access level within the system

- **Vue.js:** Progressive JavaScript framework used for building user interfaces and single-page applications

- **Workflow:** The sequence of processes through which an application passes from submission to final decision

---

## 9. APPENDICES

### Appendix A: System Architecture Overview
- Frontend: Vue.js 3 with Composition API and Pinia state management
- Backend: Flask RESTful API with SQLAlchemy ORM
- Database: MySQL with normalized schema design
- Authentication: Flask-Security with JWT tokens
- File Storage: Binary storage in database with base64 encoding

### Appendix B: API Endpoints Summary
- Authentication: /api/auth/login, /api/auth/register, /api/auth/logout
- Applications: /api/application/submit, /api/application/save-draft, /api/application/get-draft
- Admin: /api/application/admin/list, /api/application/admin/review, /api/application/admin/stats
- Documents: /api/application/download-document, /api/application/download-offer-letter

### Appendix C: Database Schema Overview
- Users table with role assignments
- Applications table with status tracking
- Binary document storage with metadata
- Audit trails for status changes and reviews

---

**Document Control:**
- Created: September 6, 2025
- Last Modified: September 6, 2025
- Version: 1.0
- Status: Final
