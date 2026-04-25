# AIU Admission System

A Django-based web application designed for managing student admissions for AIU. This system provides a comprehensive portal for prospective students to apply for programs, submit their details, and track their application status. It also includes an administrative dashboard for reviewing, shortlisting, and accepting applications based on specific prescreening criteria.

## Features

### Student Portal
- **User Registration & Authentication**: Secure sign-up, login, and logout functionalities.
- **Application Flow**: Step-by-step application process including:
  - Program Selection
  - Basic Information
  - Academic Information
  - Financial Information
  - Document Uploading
- **Dashboard & Status Tracking**: Students can view their application status and manage their submissions.

### Admin Dashboard
- **Application Review**: Admins can view a list of all applications and filter them by status.
- **Detailed Applicant View**: Access to individual applicant details and uploaded documents.
- **Application Processing**: Ability to shortlist and accept applications.
- **Statistics**: Visual statistics on applications received, shortlisted, and accepted.
- **Prescreening Criteria Management**: Admins can manage the criteria for shortlisting applicants (e.g., minimum CGPA, age limits, marital status, eligible countries).

## Technologies Used
- **Backend**: Python, Django 5.1
- **Database**: SQLite (Default)
- **Other Packages**: `pycountry` for dynamic country list loading.

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Navigate to the core project folder**:
   ```bash
   cd fyp
   ```

3. **Install Dependencies**:
   Ensure you have the required Python packages installed.
   ```bash
   pip install django pycountry
   ```

4. **Apply Database Migrations**:
   Set up the database tables and load the initial country data.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The application should now be accessible at `http://127.0.0.1:8000/`.

## Project Structure
- `fyp/` - The core Django project directory containing settings and root configurations.
- `bkend/` - The main application handling the admission logic, models, views, and templates.
- `media/` - Directory for user-uploaded documents and profile pictures.
- `Student Selection formula_reference.xlsx` - Reference file for selection formulas.

## Note on Initial Setup
The project is configured to automatically load country data from `pycountry` into the database upon initialization. If you encounter any database missing table errors initially, ensure that you have run the migrations as specified above.
