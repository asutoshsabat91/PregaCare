
# PregaCare - Comprehensive Maternal Health Platform

A Django-based web application providing complete maternal health care solutions for women throughout their pregnancy journey and beyond.

## Features

### Core Health Tracking
- **Menstrual Cycle Tracking** - Monitor cycles, predict fertile windows, and track symptoms
- **Pregnancy Profile** - Week-by-week pregnancy monitoring with personalized insights
- **Nutrition Engine** - Dynamic nutrition plans based on pregnancy week and dietary preferences
- **Postpartum Care** - Recovery tracking with mental health monitoring
- **Pelvic Floor Rehabilitation** - Progressive exercises with strength tracking
- **BMI Calculator** - Body mass index tracking for healthy weight management

### Baby Care & Development
- **Baby Profiles** - Complete infant health and development tracking
- **Vaccination Tracker** - Automated immunization schedule management
- **Growth Records** - Track baby's physical development milestones
- **Milestone Tracking** - Monitor developmental achievements

### Healthcare Services
- **Telehealth Platform** - Connect with healthcare providers for virtual consultations
- **Appointment Management** - Schedule and manage video/audio/chat consultations
- **Medical Records** - Secure digital storage of health information
- **Provider Reviews** - Rate and review healthcare professionals

### AI Health Assistant
- **24/7 AI Chat** - Instant health advice and pregnancy guidance
- **Symptom Checker** - AI-powered symptom assessment with urgency recommendations
- **Medication Reminders** - Automated medication tracking and alerts
- **Health Insights** - Personalized recommendations based on health patterns

### Emergency Services
- **MEWS Assessment** - Maternal Early Warning System for vital signs monitoring
- **SOS Alert System** - Emergency notifications with location tracking
- **Emergency Contacts** - Quick access to important contacts and services

### Educational Resources
- **Health Articles** - Curated content on pregnancy, nutrition, and baby care
- **Educational Courses** - Free courses and workshops for mothers
- **NGO Support Network** - Connect with support organizations and communities
- **Financial Assistance** - Information about aid programs and support services

## Technology Stack

### Backend
- **Framework**: Django 3.1.3
- **Language**: Python 3.12.7
- **Database**: SQLite (with PostgreSQL/MySQL support)
- **Authentication**: Django's built-in authentication system
- **API**: Django REST Framework for mobile app integration

### Frontend
- **UI Framework**: Bootstrap 4.3.1
- **Icons**: Font Awesome 4.7.0
- **Styling**: Custom CSS with gradient designs
- **JavaScript**: jQuery 3.5.1 for interactions
- **Responsive Design**: Mobile-first approach

### Deployment
- **Web Server**: Django development server
- **Static Files**: Django static file management
- **Media Files**: User uploads and document storage

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 3.1+
- Node.js (for development dependencies)
- Git

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/asutoshsabat91/PregaCare.git
   cd PregaCare
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access Application**
   Open http://localhost:8000 in your web browser

## Project Structure

```
PregaCare/
├── Safeher/                 # Django project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── women/                  # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── templates/         # HTML templates
│   ├── static/           # Static files (CSS, JS, images)
│   └── migrations/        # Database migrations
├── media/                  # User uploaded files
├── db.sqlite3           # SQLite database (development)
└── manage.py             # Django management script
```

## Database Schema

### Core Models
- **User Management**: Signup, authentication, profile management
- **Health Tracking**: MenstrualCycle, PregnancyProfile, NutritionalPlan
- **Baby Care**: BabyProfile, VaccinationRecord, GrowthRecord
- **Healthcare**: HealthcareProvider, TelehealthAppointment
- **AI Assistant**: AIConversation, AISymptomChecker, AIMedicationReminder
- **Emergency**: MEWS_Assessment, SOS_Alert, EmergencyContact
- **Postpartum**: PostpartumProfile, MentalHealthCheck, PelvicFloorRehab

## Key Features Explained

### Smart Health Tracking
- **Cycle Prediction**: AI-powered fertile window calculations
- **Week-by-Week Updates**: Detailed pregnancy progress tracking
- **Personalized Nutrition**: Dynamic meal plans based on pregnancy stage
- **Risk Assessment**: MEWS scoring for early warning signs

### Connected Care Ecosystem
- **Provider Network**: Verified healthcare professionals
- **Appointment Scheduling**: Video, audio, and chat consultations
- **Record Management**: Comprehensive medical history tracking
- **Emergency Response**: Quick access to emergency services

### AI-Powered Insights
- **24/7 Availability**: Round-the-clock health guidance
- **Symptom Analysis**: Intelligent health assessment
- **Personalized Recommendations**: Tailored health advice
- **Medication Management**: Smart reminders and tracking

## Security Features

- **User Authentication**: Secure login/logout system
- **Data Encryption**: Sensitive data protection
- **Role-Based Access**: Different access levels for users/admins
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Cross-site request forgery prevention

## Responsive Design

### Mobile Optimization
- **Progressive Enhancement**: Works on all device sizes
- **Touch-Friendly**: Optimized for mobile interactions
- **Fast Loading**: Optimized assets and minimal JavaScript
- **Offline Support**: Service worker for basic offline functionality

### Accessibility
- **WCAG Compliance**: Web accessibility standards
- **Screen Reader Support**: Proper ARIA labels and roles
- **Keyboard Navigation**: Full keyboard accessibility
- **High Contrast**: Multiple color themes available

## Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   export DEBUG=False
   export ALLOWED_HOSTS=['yourdomain.com']
   export SECRET_KEY='your-secret-key'
   ```

2. **Database Migration**
   ```bash
   python manage.py migrate --settings=production
   ```

3. **Static File Collection**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Web Server Setup**
   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn Safeher.wsgi:application

   # Using uWSGI with Nginx
   uwsgi --http :8000 Safeher.wsgi
   ```

## Testing

### Test Coverage
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test women

# Generate coverage report
coverage run --source='.' manage.py test
coverage report
```

### Test Categories
- **Unit Tests**: Model and view function testing
- **Integration Tests**: Database and API integration
- **Functional Tests**: User workflow testing
- **UI Tests**: Frontend component testing

## Performance Optimization

### Database Optimization
- **Query Optimization**: Efficient database queries
- **Indexing Strategy**: Proper database indexes
- **Connection Pooling**: Database connection management
- **Caching Strategy**: Redis/Memcached integration

### Frontend Optimization
- **Asset Minification**: CSS and JavaScript compression
- **Image Optimization**: WebP format and lazy loading
- **CDN Integration**: Content delivery network setup
- **Browser Caching**: Proper cache headers

## API Documentation

### REST API Endpoints

#### Authentication
```
POST /api/login/          # User login
POST /api/logout/         # User logout
POST /api/register/       # User registration
GET  /api/profile/         # User profile
```

#### Health Data
```
GET  /api/menstrual-cycles/     # Get menstrual cycles
POST /api/menstrual-cycles/     # Create menstrual cycle
GET  /api/pregnancy-profile/    # Get pregnancy profile
POST /api/pregnancy-profile/    # Create/update pregnancy profile
```

#### Healthcare Services
```
GET  /api/providers/          # List healthcare providers
POST /api/appointments/       # Create appointment
GET  /api/appointments/       # List user appointments
```

## Contributing

### Development Workflow
1. **Fork Repository**
   ```bash
   git fork https://github.com/asutoshsabat91/PregaCare.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature-name
   ```

3. **Make Changes**
   - Follow coding standards
   - Write tests for new features
   - Update documentation

4. **Submit Changes**
   ```bash
   git add .
   git commit -m "Add feature description"
   git push origin feature-name
   ```

5. **Pull Request**
   - Create detailed PR description
   - Include screenshots for UI changes
   - Ensure all tests pass

### Code Standards
- **PEP 8 Compliance**: Follow Python style guidelines
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Minimum 80% test coverage required
- **Security**: Follow security best practices

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### License Summary
- Commercial use allowed
- Modification allowed
- Distribution allowed
- Private use allowed
- Liability disclaimer

## Support & Contact

### Getting Help
- **Documentation**: Project Wiki
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@pregacare.com

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Browser and version
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable

## Acknowledgments

### Core Technologies
- **Django Team** - Excellent web framework
- **Bootstrap Team** - Responsive UI framework
- **jQuery Team** - JavaScript library
- **Font Awesome** - Icon library

### Inspiration
- **Healthcare Professionals** - Medical expertise and guidance
- **Mothers Community** - User feedback and suggestions
- **Open Source Contributors** - Code improvements and features

---

## Quick Start

1. **Clone**: `git clone https://github.com/asutoshsabat91/PregaCare.git`
2. **Setup**: `cd PregaCare && python -m venv venv && source venv/bin/activate`
3. **Install**: `pip install -r requirements.txt`
4. **Migrate**: `python manage.py migrate`
5. **Run**: `python manage.py runserver`
6. **Access**: Open http://localhost:8000

**PregaCare - Empowering mothers with comprehensive digital health care solutions.**
  PregaCare is a comprehensive maternal health platform designed to support women throughout their pregnancy journey and beyond. Originally based on SAFehER, this enhanced version provides advanced features for menstrual tracking, fertility optimization, pregnancy monitoring, postpartum care, and emergency support.

  The platform offers informative resources about pregnancy, assists women in navigating healthcare challenges, provides direct access to medical consultations, and ensures safety through advanced monitoring systems. PregaCare addresses the critical need for a dedicated platform where pregnant women can manage their health, track their baby's development, and access emergency care when needed.

  PregaCare empowers women with comprehensive health tracking, nutritional guidance, mental health support, and emergency response capabilities, creating a complete ecosystem for maternal and child healthcare.


## Technology Stack:
  1) Django
  2) Bootstrap
  3) Javascript
  4) HTML5
  5) CSS


## Key Features:

### 🌸 Menstrual Tracking and Fertility Optimization
- Track menstrual cycles with start/end dates and flow intensity
- Calculate fertile windows and predict next periods
- Monitor symptoms and patterns for better fertility planning
- Personalized cycle length tracking

### 🤰 Week-by-Week and Trimester-Specific Nutritional Engine
- Detailed nutritional plans for each week of pregnancy
- Trimester-specific dietary recommendations
- Calorie, protein, iron, calcium, and folic acid tracking
- Foods to avoid and recommended supplements
- High-risk pregnancy nutritional considerations

### 🍼 The Fourth Trimester: Postpartum Recovery and Mental Health
- Postpartum recovery tracking based on delivery type
- Mental health monitoring with mood and anxiety assessments
- Sleep and appetite tracking
- Personalized recovery milestones and support

### 💪 Pelvic Floor Rehabilitation and Kinetic Progression
- Progressive pelvic floor exercise programs
- Muscle strength and endurance assessments
- Difficulty-based exercise progression
- Recovery progress tracking and notes

### 👶 Neonatal Care and Pediatric Vaccination Tracking
- Comprehensive baby profile management
- Growth tracking (weight, length, head circumference)
- Vaccination schedule management with due date reminders
- Developmental milestones tracking
- APGAR score and birth complication recording

### 🚨 Maternal Early Warning System (MEWS) and Emergency SOS
- Real-time vital signs monitoring (BP, heart rate, temperature, etc.)
- Automated MEWS scoring with risk level assessment
- Emergency contact management
- SOS alert system with location tracking
- Immediate medical attention recommendations

### 📋 Additional Features
- Medical notes and document management
- Educational magazine resources
- User role management (patients, healthcare providers)
- Secure data storage and privacy protection

### 🏥 Telehealth Integration
- **Healthcare Provider Directory**: Find and connect with verified healthcare professionals including OB-GYNs, midwives, nutritionists, mental health professionals, and pediatricians
- **Multi-format Consultations**: Schedule video calls, phone consultations, chat sessions, or in-person visits
- **Appointment Management**: Complete scheduling system with reminders, status tracking, and calendar integration
- **Medical Records**: Secure digital storage of consultations, diagnoses, treatment plans, and prescriptions
- **Provider Reviews**: Rate and review healthcare providers to help others make informed decisions
- **Real-time Availability**: See provider schedules, consultation fees, and available time slots
- **Follow-up Care**: Automated follow-up scheduling and care coordination

### 🤖 24/7 AI Conversational Agents
- **Intelligent Health Assistant**: Always-available AI companion for health queries and concerns
- **Symptom Checker**: Advanced AI-powered symptom assessment with urgency recommendations
- **Medical Knowledge Base**: Comprehensive, medically-reviewed information covering pregnancy, postpartum care, nutrition, mental health, and more
- **Personalized Conversations**: Context-aware AI that remembers your health history and provides tailored responses
- **Emergency Detection**: AI identifies urgent situations and escalates to human healthcare providers when needed
- **Medication Reminders**: Smart reminders with adherence tracking and dosage instructions
- **Health Insights**: AI analyzes your health patterns and provides personalized recommendations and alerts
- **Multi-language Support**: Conversational support in multiple languages for accessibility
- **Appointment Booking**: AI assistant can schedule appointments with healthcare providers based on availability and urgency


## Video Link:
https://youtu.be/S8VGYfEZrXU

*****************************

PPT Link:
https://drive.google.com/file/d/1EqVD5OBZlHg_rhSgbKWRTnKlAxFoR4sO/view?usp=sharing

***************************************************************
# How to Clone this repo

Open gitbash and type the following command:

##### git clone "https://github.com/somya51p/SAFehER/"

*************************************************************
Create virtual environment, Open Visual Studio code and type the following command in terminal:

##### pip install -r reqirements.txt

*************************************************************
Followed by these commands in terminal itself:

##### python manage.py migrate

##### python manage.py makemigrations women

##### python manage.py migrate

*************************************************************

To run the PregaCare app then type:

##### python manage.py runserver

This would make the app run in the browser..
**************************************************************

In order to access the django-admin, One must create a superuser so type the following command for the same:

##### python manage.py createsuperuser

Fill the required details and it would be created..

**************************************************************

# Enjoy using the PregaCare Web App..

**************************************************************
**************************************************************

### Made at:
<a href="https://hack36.com"> <img src="http://bit.ly/BuiltAtHack36" height=20px> </a>

