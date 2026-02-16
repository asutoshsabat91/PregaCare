from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from . models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    """Main dashboard view with all PregaCare features"""
    context = {
        'user': request.user,
        'title': 'PregaCare Dashboard'
    }
    return render(request, 'dashboard.html', context)

@login_required
def menstrual_tracking(request):
    """Menstrual tracking page"""
    if request.method == 'POST':
        # Handle cycle creation
        if 'cycle_start' in request.POST:
            try:
                from datetime import datetime, timedelta
                cycle_start = datetime.strptime(request.POST.get('cycle_start'), '%Y-%m-%d').date()
                cycle_length = int(request.POST.get('cycle_length', 28))
                
                # Create menstrual cycle
                cycle = MenstrualCycle.objects.create(
                    user=request.user,
                    cycle_start=cycle_start,
                    cycle_length=cycle_length,
                    period_length=int(request.POST.get('period_length', 5)),
                    fertile_window_start=cycle_start + timedelta(days=8),
                    fertile_window_end=cycle_start + timedelta(days=13),
                    next_period_date=cycle_start + timedelta(days=cycle_length),
                    notes=request.POST.get('notes', '')
                )
                messages.success(request, 'Menstrual cycle added successfully!')
                return redirect('menstrual_tracking')
            except Exception as e:
                messages.error(request, f'Error adding cycle: {str(e)}')
    
    # GET request - display existing data
    try:
        cycles = MenstrualCycle.objects.filter(user=request.user).order_by('-cycle_start')
    except:
        cycles = []
    
    # Calculate stats if cycles exist
    avg_cycle = 28
    fertile_days = 5
    if cycles:
        cycle_lengths = [c.cycle_length for c in cycles]
        if cycle_lengths:
            avg_cycle = sum(cycle_lengths) // len(cycle_lengths)
    
    context = {
        'user': request.user,
        'cycles': cycles,
        'avg_cycle': avg_cycle,
        'fertile_days': fertile_days,
        'title': 'Menstrual Tracking - PregaCare'
    }
    return render(request, 'menstrual_tracking.html', context)

@login_required
def pregnancy_profile(request):
    """Pregnancy profile page"""
    if request.method == 'POST':
        # Handle profile creation
        if 'last_menstrual_period' in request.POST:
            try:
                from datetime import datetime, timedelta
                lmp = datetime.strptime(request.POST.get('last_menstrual_period'), '%Y-%m-%d').date()
                due_date = lmp + timedelta(days=280)  # Approximate due date
                
                # Create pregnancy profile
                profile = PregnancyProfile.objects.create(
                    user=request.user,
                    last_menstrual_period=lmp,
                    due_date=due_date,
                    current_trimester=1,  # Default to first trimester
                    is_high_risk=request.POST.get('high_risk') == 'true'
                )
                messages.success(request, 'Pregnancy profile created successfully!')
                return redirect('pregnancy_profile')
            except Exception as e:
                messages.error(request, f'Error creating profile: {str(e)}')
        
        # Handle nutrition plan generation
        elif 'pregnancy_week' in request.POST:
            try:
                profile = PregnancyProfile.objects.get(user=request.user)
                week = int(request.POST.get('pregnancy_week'))
                
                # Calculate nutritional needs based on pregnancy week
                calories_needed = 2000 + (week * 50)  # Basic calculation
                protein_grams = 50 + (week * 2)
                iron_mg = 27 + (week * 1)
                calcium_mg = 1000 + (week * 10)
                folic_acid_mcg = 400 + (week * 5)
                
                # Create nutritional plan
                plan = NutritionalPlan.objects.create(
                    pregnancy_profile=profile,
                    week=week,
                    trimester=(week - 1) // 13 + 1,  # Calculate trimester
                    calories_needed=calories_needed,
                    protein_grams=protein_grams,
                    iron_mg=iron_mg,
                    calcium_mg=calcium_mg,
                    folic_acid_mcg=folic_acid_mcg
                )
                messages.success(request, 'Nutrition plan generated successfully!')
                return redirect('pregnancy_profile')
            except Exception as e:
                messages.error(request, f'Error generating nutrition plan: {str(e)}')
    
    # GET request - display existing data
    try:
        profile = PregnancyProfile.objects.get(user=request.user)
        nutritional_plans = NutritionalPlan.objects.filter(pregnancy_profile=profile)
        
        # Calculate pregnancy stats
        current_date = date.today()
        days_pregnant = (current_date - profile.last_menstrual_period).days
        weeks_pregnant = days_pregnant // 7
        days_remaining = (profile.due_date - current_date).days
        weeks_remaining = days_remaining // 7
        
        pregnancy_stats = {
            'days_pregnant': days_pregnant,
            'weeks_pregnant': weeks_pregnant,
            'days_remaining': days_remaining,
            'weeks_remaining': weeks_remaining,
            'trimester_progress': ((weeks_pregnant - 1) % 13) / 13 * 100,
            'overall_progress': (weeks_pregnant / 40) * 100
        }
    except PregnancyProfile.DoesNotExist:
        profile = None
        nutritional_plans = []
        pregnancy_stats = {}
    
    context = {
        'user': request.user,
        'profile': profile,
        'nutritional_plans': nutritional_plans,
        'pregnancy_stats': pregnancy_stats,
        'title': 'Pregnancy Profile - PregaCare'
    }
    return render(request, 'pregnancy_profile.html', context)

@login_required
def nutrition_engine(request):
    """Nutrition engine page"""
    if request.method == 'POST':
        # Handle nutrition plan generation
        if 'pregnancy_week' in request.POST:
            try:
                from datetime import datetime
                week = int(request.POST.get('pregnancy_week'))
                
                # Get or create pregnancy profile
                profile, created = PregnancyProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'last_menstrual_period': datetime.now().date() - timedelta(weeks=week),
                        'due_date': datetime.now().date() + timedelta(weeks=40-week),
                        'current_trimester': (week - 1) // 13 + 1,
                        'is_high_risk': False
                    }
                )
                
                # Calculate nutritional needs based on pregnancy week
                calories_needed = 2000 + (week * 50)
                protein_grams = 50 + (week * 2)
                iron_mg = 27 + (week * 1)
                calcium_mg = 1000 + (week * 10)
                folic_acid_mcg = 400 + (week * 5)
                
                # Create nutritional plan
                plan = NutritionalPlan.objects.create(
                    pregnancy_profile=profile,
                    week=week,
                    trimester=(week - 1) // 13 + 1,
                    calories_needed=calories_needed,
                    protein_grams=protein_grams,
                    iron_mg=iron_mg,
                    calcium_mg=calcium_mg,
                    folic_acid_mcg=folic_acid_mcg
                )
                messages.success(request, 'Nutrition plan generated successfully!')
                return redirect('nutrition_engine')
            except Exception as e:
                messages.error(request, f'Error generating nutrition plan: {str(e)}')
    
    # GET request - display existing data or sample data
    try:
        profile = PregnancyProfile.objects.get(user=request.user)
        current_week = profile.current_week or 20  # Default to week 20
        nutritional_plan = NutritionalPlan.objects.filter(
            pregnancy_profile=profile
        ).order_by('-week').first()
    except PregnancyProfile.DoesNotExist:
        # Create sample data for demonstration
        current_week = 20
        nutritional_plan = type('NutritionalPlan', (), {
            'week': 20,
            'trimester': 2,
            'calories_needed': 3000,
            'protein_grams': 90,
            'iron_mg': 47,
            'calcium_mg': 1200,
            'folic_acid_mcg': 500
        })()
    
    # Generate food recommendations based on week
    food_recommendations = generate_food_recommendations(current_week)
    
    # Calculate nutrition stats
    nutrition_stats = {
        'total_calories': nutritional_plan.calories_needed if nutritional_plan else 3000,
        'protein_percentage': round((nutritional_plan.protein_grams * 4) / nutritional_plan.calories_needed * 100, 1) if nutritional_plan else 12,
        'iron_daily_value': round((nutritional_plan.iron_mg / 27) * 100, 1) if nutritional_plan else 174,
        'calcium_daily_value': round((nutritional_plan.calcium_mg / 1000) * 100, 1) if nutritional_plan else 120,
        'folic_acid_daily_value': round((nutritional_plan.folic_acid_mcg / 400) * 100, 1) if nutritional_plan else 125
    }
    
    context = {
        'user': request.user,
        'current_week': current_week,
        'nutritional_plan': nutritional_plan,
        'food_recommendations': food_recommendations,
        'nutrition_stats': nutrition_stats,
        'title': 'Nutrition Engine - PregaCare'
    }
    return render(request, 'nutrition_engine.html', context)

def generate_food_recommendations(week):
    """Generate food recommendations based on pregnancy week"""
    trimester = (week - 1) // 13 + 1
    
    recommendations = {
        'protein_rich': [
            'Lean chicken breast (3oz) - 26g protein',
            'Salmon (3oz) - 22g protein + Omega-3',
            'Greek yogurt (1 cup) - 20g protein',
            'Lentils (1 cup cooked) - 18g protein',
            'Quinoa (1 cup cooked) - 8g protein'
        ],
        'iron_rich': [
            'Spinach (1 cup cooked) - 6.4mg iron',
            'Lean beef (3oz) - 3mg iron',
            'Pumpkin seeds (1oz) - 2.5mg iron',
            'Fortified cereal (1 cup) - 18mg iron',
            'Dark chocolate (1oz) - 3.4mg iron'
        ],
        'calcium_rich': [
            'Greek yogurt (1 cup) - 200mg calcium',
            'Milk (1 cup) - 300mg calcium',
            'Cheese (1oz) - 200mg calcium',
            'Kale (1 cup cooked) - 94mg calcium',
            'Almonds (1oz) - 75mg calcium'
        ],
        'folic_acid_rich': [
            'Lentils (1 cup cooked) - 358mcg folic acid',
            'Spinach (1 cup raw) - 194mcg folic acid',
            'Asparagus (1 cup) - 268mcg folic acid',
            'Broccoli (1 cup) - 168mcg folic acid',
            'Fortified breakfast cereal (1 cup) - 400mcg folic acid'
        ]
    }
    
    # Add trimester-specific recommendations
    if trimester == 1:
        recommendations['additional'] = [
            'Ginger tea for nausea relief',
            'Small frequent meals to manage morning sickness',
            'Folic acid supplements (400-800mcg daily)',
            'Plenty of water (8-10 glasses daily)'
        ]
    elif trimester == 2:
        recommendations['additional'] = [
            'Increase protein intake for baby growth',
            'Calcium-rich foods for bone development',
            'Omega-3 fatty acids for brain development',
            'Iron-rich foods to prevent anemia'
        ]
    else:
        recommendations['additional'] = [
            'High-fiber foods to prevent constipation',
            'Small, frequent meals to ease digestion',
            'Continue iron and calcium intake',
            'Stay hydrated for amniotic fluid levels'
        ]
    
    return recommendations

@login_required
def postpartum_care(request):
    """Postpartum care page"""
    if request.method == 'POST':
        # Handle postpartum profile creation
        if 'delivery_date' in request.POST:
            try:
                from datetime import datetime
                delivery_date = datetime.strptime(request.POST.get('delivery_date'), '%Y-%m-%d').date()
                baby_weight = float(request.POST.get('baby_birth_weight', 3.0))
                delivery_type = request.POST.get('delivery_type', 'normal')
                
                # Create postpartum profile
                profile = PostpartumProfile.objects.create(
                    user=request.user,
                    delivery_date=delivery_date,
                    recovery_notes=request.POST.get('recovery_notes', '')
                )
                
                # Create baby profile linked to postpartum
                BabyProfile.objects.create(
                    postpartum_profile=profile,
                    birth_weight=baby_weight,
                    delivery_type=delivery_type
                )
                
                messages.success(request, 'Postpartum profile created successfully!')
                return redirect('postpartum_care')
            except Exception as e:
                messages.error(request, f'Error creating postpartum profile: {str(e)}')
    
    # GET request - display existing data
    try:
        profile = PostpartumProfile.objects.get(user=request.user)
        mental_health_checks = MentalHealthCheck.objects.filter(
            postpartum_profile=profile
        ).order_by('-check_date')
        pelvic_floor_rehab = PelvicFloorRehab.objects.filter(
            postpartum_profile=profile
        ).order_by('-assessment_date')
        
        # Calculate postpartum stats
        current_date = date.today()
        days_postpartum = (current_date - profile.delivery_date).days
        weeks_postpartum = days_postpartum // 7
        
        postpartum_stats = {
            'days_postpartum': days_postpartum,
            'weeks_postpartum': weeks_postpartum,
            'recovery_score': 85,  # Placeholder calculation
            'mental_health_score': 90,  # Placeholder calculation
            'total_checkins': len(mental_health_checks),
            'rehab_sessions': len(pelvic_floor_rehab)
        }
    except PostpartumProfile.DoesNotExist:
        profile = None
        # Create sample data for demonstration
        mental_health_checks = [
            type('MentalHealthCheck', (), {
                'check_date': '2024-01-15',
                'mood_score': 8,
                'anxiety_level': 3,
                'sleep_quality': 7,
                'notes': 'Feeling good today'
            })(),
            type('MentalHealthCheck', (), {
                'check_date': '2024-01-22',
                'mood_score': 7,
                'anxiety_level': 4,
                'sleep_quality': 6,
                'notes': 'Some anxiety about baby care'
            })()
        ]
        
        pelvic_floor_rehab = [
            type('PelvicFloorRehab', (), {
                'assessment_date': '2024-01-10',
                'strength_score': 6,
                'exercises_completed': ['Kegels', 'Squats'],
                'notes': 'Good progress'
            })(),
            type('PelvicFloorRehab', (), {
                'assessment_date': '2024-01-20',
                'strength_score': 7,
                'exercises_completed': ['Kegels', 'Bridge'],
                'notes': 'Improving well'
            })()
        ]
        
        postpartum_stats = {
            'days_postpartum': 30,
            'weeks_postpartum': 4,
            'recovery_score': 85,
            'mental_health_score': 90,
            'total_checkins': 2,
            'rehab_sessions': 2
        }
    
    context = {
        'user': request.user,
        'profile': profile,
        'mental_health_checks': mental_health_checks,
        'pelvic_floor_rehab': pelvic_floor_rehab,
        'postpartum_stats': postpartum_stats,
        'title': 'Postpartum Care - PregaCare'
    }
    return render(request, 'postpartum_care.html', context)

@login_required
def baby_care(request):
    """Baby care page"""
    if request.method == 'POST':
        # Handle vaccination record creation
        if 'vaccine_name' in request.POST:
            try:
                # Get or create baby profile
                baby_name = request.POST.get('baby_name', 'Baby')
                baby, created = BabyProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'name': baby_name,
                        'birth_date': datetime.now().date() - timedelta(days=30),
                        'birth_weight': 3.2,
                        'birth_length': 50,
                        'apgar_score': 9
                    }
                )
                
                # Create vaccination record
                VaccinationRecord.objects.create(
                    baby=baby,
                    vaccine_name=request.POST.get('vaccine_name'),
                    scheduled_date=datetime.strptime(request.POST.get('scheduled_date'), '%Y-%m-%d').date(),
                    administered_date=datetime.strptime(request.POST.get('administered_date'), '%Y-%m-%d').date() if request.POST.get('administered_date') else None,
                    notes=request.POST.get('notes', '')
                )
                messages.success(request, 'Vaccination record added successfully!')
                return redirect('baby_care')
            except Exception as e:
                messages.error(request, f'Error adding vaccination record: {str(e)}')
        
        # Handle growth record creation
        elif 'weight' in request.POST:
            try:
                baby_name = request.POST.get('baby_name', 'Baby')
                baby, created = BabyProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'name': baby_name,
                        'birth_date': datetime.now().date() - timedelta(days=30),
                        'birth_weight': 3.2,
                        'birth_length': 50,
                        'apgar_score': 9
                    }
                )
                
                # Create growth record
                GrowthRecord.objects.create(
                    baby=baby,
                    weight=float(request.POST.get('weight')),
                    height=float(request.POST.get('height', 50)),
                    head_circumference=float(request.POST.get('head_circumference', 35)),
                    record_date=datetime.strptime(request.POST.get('record_date'), '%Y-%m-%d').date(),
                    notes=request.POST.get('notes', '')
                )
                messages.success(request, 'Growth record added successfully!')
                return redirect('baby_care')
            except Exception as e:
                messages.error(request, f'Error adding growth record: {str(e)}')
    
    # GET request - display existing data
    try:
        postpartum_profile = PostpartumProfile.objects.get(user=request.user)
        baby_profiles = BabyProfile.objects.filter(postpartum_profile=postpartum_profile)
        vaccination_records = []
        growth_records = []
        
        for baby in baby_profiles:
            vaccination_records.extend(VaccinationRecord.objects.filter(baby=baby))
            growth_records.extend(GrowthRecord.objects.filter(baby=baby))
    except PostpartumProfile.DoesNotExist:
        # Create sample data for demonstration
        baby_profiles = []
        vaccination_records = []
        growth_records = []
        
        # Add sample vaccination records
        sample_vaccines = [
            {'vaccine_name': 'BCG', 'baby_name': 'Sample Baby', 'scheduled_date': '2024-01-15', 'administered_date': '2024-01-15'},
            {'vaccine_name': 'Hepatitis B', 'baby_name': 'Sample Baby', 'scheduled_date': '2024-02-15', 'administered_date': '2024-02-15'},
            {'vaccine_name': 'DPT', 'baby_name': 'Sample Baby', 'scheduled_date': '2024-03-15', 'administered_date': '2024-03-15'},
        ]
        
        for vaccine_data in sample_vaccines:
            # Create a simple object-like structure for template
            vaccine_obj = type('Vaccine', (), vaccine_data)
            vaccination_records.append(vaccine_obj)
        
        # Add sample growth records
        sample_growth = [
            {'weight': 3.5, 'height': 52, 'head_circumference': 36, 'baby_name': 'Sample Baby', 'record_date': '2024-01-15'},
            {'weight': 4.2, 'height': 55, 'head_circumference': 37, 'baby_name': 'Sample Baby', 'record_date': '2024-02-15'},
        ]
        
        for growth_data in sample_growth:
            growth_obj = type('Growth', (), growth_data)
            growth_records.append(growth_obj)
    
    context = {
        'user': request.user,
        'baby_profiles': baby_profiles,
        'vaccination_records': vaccination_records,
        'growth_records': growth_records,
        'title': 'Baby Care - PregaCare'
    }
    return render(request, 'baby_care.html', context)

@login_required
def telehealth(request):
    """Telehealth page"""
    try:
        providers = HealthcareProvider.objects.all()
        # Use a simple query without the problematic field
        appointments = []
    except:
        providers = []
        appointments = []
    
    context = {
        'user': request.user,
        'providers': providers,
        'consultations': appointments,  # Use 'consultations' to match template
        'title': 'Telehealth - PregaCare'
    }
    return render(request, 'telehealth.html', context)

@login_required
def ai_assistant(request):
    """AI assistant page"""
    try:
        conversations = AIConversation.objects.filter(user=request.user).order_by('-last_activity')
        symptom_checks = AISymptomChecker.objects.filter(user=request.user).order_by('-created_at')
        medication_reminders = AIMedicationReminder.objects.filter(user=request.user, is_active=True)
        health_insights = AIHealthInsight.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    except:
        conversations = []
        symptom_checks = []
        medication_reminders = []
        health_insights = []
    
    context = {
        'user': request.user,
        'conversations': conversations,
        'symptom_checks': symptom_checks,
        'medication_reminders': medication_reminders,
        'health_insights': health_insights,
        'title': 'AI Assistant - PregaCare'
    }
    return render(request, 'ai_assistant.html', context)

@login_required
def emergency_services(request):
    """Emergency services page"""
    try:
        mews_assessments = MEWS_Assessment.objects.filter(user=request.user).order_by('-assessment_date')
        emergency_contacts = EmergencyContact.objects.filter(user=request.user)
        sos_alerts = SOS_Alert.objects.filter(user=request.user).order_by('-alert_time')
    except:
        mews_assessments = []
        emergency_contacts = []
        sos_alerts = []
    
    context = {
        'user': request.user,
        'mews_assessments': mews_assessments,
        'emergency_contacts': emergency_contacts,
        'sos_alerts': sos_alerts,
        'title': 'Emergency Services - PregaCare'
    }
    return render(request, 'emergency_services.html', context)

@login_required
def pelvic_floor_rehab(request):
    """Pelvic floor rehabilitation page"""
    try:
        postpartum_profile = PostpartumProfile.objects.get(user=request.user)
        rehab_records = PelvicFloorRehab.objects.filter(
            postpartum_profile=postpartum_profile
        ).order_by('-assessment_date')
        exercise_progress = ExerciseProgress.objects.filter(
            rehab__in=rehab_records
        ).order_by('-completion_date')
    except PostpartumProfile.DoesNotExist:
        rehab_records = []
        exercise_progress = []
    
    context = {
        'user': request.user,
        'rehab_records': rehab_records,
        'exercise_progress': exercise_progress,
        'title': 'Pelvic Floor Rehabilitation - PregaCare'
    }
    return render(request, 'pelvic_floor_rehab.html', context)

@login_required
def vaccination_tracker(request):
    """Vaccination tracker page"""
    try:
        postpartum_profile = PostpartumProfile.objects.get(user=request.user)
        baby_profiles = BabyProfile.objects.filter(postpartum_profile=postpartum_profile)
        vaccination_records = []
        for baby in baby_profiles:
            vaccination_records.extend(VaccinationRecord.objects.filter(baby=baby))
    except PostpartumProfile.DoesNotExist:
        vaccination_records = []
    
    context = {
        'user': request.user,
        'vaccination_records': vaccination_records,
        'title': 'Vaccination Tracker - PregaCare'
    }
    return render(request, 'vaccination_tracker.html', context)

@login_required
def educational_resources(request):
    """Educational resources page"""
    context = {
        'user': request.user,
        'title': 'Educational Resources - PregaCare'
    }
    return render(request, 'educational_resources.html', context)

def home(request):
    return render(request, 'home.html')

def signup1(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        e = request.POST['email']
        p = request.POST['pwd']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user,contact=c,role=r)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'signup.html', d)

def userlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login.html', d)

def Logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    d = {'data':data, 'user':user}
    return render(request, 'profile.html', d)

@login_required
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    error = False
    if request.method == 'POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        c=request.POST['contact']
        u=request.POST['username']
        user.first_name = f
        user.last_name = l
        data.contact = c
        user.username = u
        user.save()
        data.save()
        error=True
    d = {'data':data, 'user':user, 'error':error}
    return render(request, 'edit_profile.html', d)

@login_required
def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method == 'POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact = request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request, 'changepassword.html',d)

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login_admin.html', d)

@staff_member_required(login_url='/login_admin/')
def admin_home(request):
    return render(request, 'admin_home.html')

@staff_member_required(login_url='/login_admin/')
def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()

    d = {'users':users}
    return render(request, 'view_users.html',d)

@staff_member_required(login_url='/login_admin/')
def delete_user(request,pid):
    if not request.user.is_staff:
        return redirect('view_users')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

@login_required
def menstrual(request):
    return render(request, 'menstrual.html')

@login_required
def bmi(request):
    """BMI calculator page"""
    context = {
        'user': request.user,
        'title': 'BMI Calculator - PregaCare'
    }
    return render(request, 'bmi_calculator.html', context)

@login_required
def browse(request):
    return render(request, 'browse.html')

@login_required
def information(request):
    return render(request, 'information.html')

@login_required
def vaccine(request):
    return render(request, 'vaccine.html')

@login_required
def magazine(request):
    return render(request, 'magazine.html')

@login_required
def ngos(request):
    return render(request, 'ngos.html')

@login_required
def helpline(request):
    return render(request, 'helpline.html')

@login_required
def upload_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method == 'POST':
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),reportfile=n,filetype=f,description=d,status="pending")

            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'upload_queries.html')

@login_required
def faq(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(status="Accept")

    d = {'notes':notes}
    return render(request, 'faq.html',d)

@staff_member_required(login_url='/login_admin/')
def pending_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Notes.objects.filter(status="pending")

    d = {'notes':notes}
    return render(request, 'pending_queries.html',d)

@staff_member_required(login_url='/login_admin/')
def accepted_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Notes.objects.filter(status="Accept")

    d = {'notes':notes}
    return render(request, 'accepted_queries.html',d)

@staff_member_required(login_url='/login_admin/')
def rejected_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Notes.objects.filter(status="Reject")

    d = {'notes':notes}
    return render(request, 'rejected_queries.html',d)

@staff_member_required(login_url='/login_admin/')
def all_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Notes.objects.all()

    d = {'notes':notes}
    return render(request, 'all_queries.html',d)

@staff_member_required(login_url='/login_admin/')
def assign_status(request,pid):
    if not request.user.is_staff:
        return redirect('login_admin')
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'notes':notes,'error':error}
    return render(request, 'assign_status.html', d)

@login_required
def delete_notes(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return redirect('all_queries')

@staff_member_required(login_url='/login_admin/')
def pending_m(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Magazines.objects.filter(status="pending")

    d = {'notes':notes}
    return render(request, 'pending_m.html',d)

@staff_member_required(login_url='/login_admin/')
def accepted_m(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Magazines.objects.filter(status="Accept")

    d = {'notes':notes}
    return render(request, 'accepted_m.html',d)

@staff_member_required(login_url='/login_admin/')
def rejected_m(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Magazines.objects.filter(status="Reject")

    d = {'notes':notes}
    return render(request, 'rejected_m.html',d)

@staff_member_required(login_url='/login_admin/')
def all_m(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    notes = Magazines.objects.all()

    d = {'notes':notes}
    return render(request, 'all_m.html',d)

@staff_member_required(login_url='/login_admin/')
def assignstatus_m(request,pid):
    if not request.user.is_staff:
        return redirect('login_admin')
    notes = Magazines.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'notes':notes,'error':error}
    return render(request, 'assignstatus_m.html', d)

@login_required
def delete_m(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    notes = Magazines.objects.get(id=pid)
    notes.delete()
    return redirect('all_notes')

@login_required
def upload_m(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method == 'POST':
        n = request.FILES['magazinesfile']
        f = request.POST['magazinestype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Magazines.objects.create(user=u,uploadedate=date.today(),magazinesfile=n,magazinestype=f,description=d,status="pending")

            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'upload_m.html')

@login_required
def view_m(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Magazines.objects.filter(status="Accept")

    d = {'notes':notes}
    return render(request, 'view_m.html',d)