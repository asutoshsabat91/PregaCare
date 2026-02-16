from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=10,null=True)
    role = models.CharField(max_length=15,null=True)

    # def __str__(self):
    #     return self.user.username


class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    uploadingdate = models.CharField(max_length=10,null=True)
    reportfile = models.FileField(null=True)
    filetype = models.CharField(max_length=30,null=True)
    description = models.CharField(max_length=300,null=True)
    status = models.CharField(max_length=30,null=True)

    # def __str__(self):
    #     return self.signup.user.username+" "+self.status


class Magazines(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    uploadedate = models.CharField(max_length=10,null=True)
    magazinesfile = models.FileField(null=True)
    magazinestype = models.CharField(max_length=30,null=True)
    description = models.CharField(max_length=300,null=True)
    status = models.CharField(max_length=30,null=True)

    # def __str__(self):
    #     return self.signup.user.username+" "+self.status


# Menstrual Tracking and Fertility Optimization
class MenstrualCycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    period_start_date = models.DateField()
    period_end_date = models.DateField()
    cycle_length = models.IntegerField(default=28)  # Average cycle length
    flow_intensity = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ])
    symptoms = models.TextField(blank=True, help_text="Note any symptoms like cramps, headaches, etc.")
    
    def __str__(self):
        return f"{self.user.username} - {self.period_start_date}"
    
    @property
    def next_period_date(self):
        return self.period_start_date + timedelta(days=self.cycle_length)
    
    @property
    def fertile_window_start(self):
        ovulation_day = self.period_start_date + timedelta(days=self.cycle_length - 14)
        return ovulation_day - timedelta(days=5)
    
    @property
    def fertile_window_end(self):
        ovulation_day = self.period_start_date + timedelta(days=self.cycle_length - 14)
        return ovulation_day + timedelta(days=1)


# Week-by-Week and Trimester-Specific Nutritional Engine
class PregnancyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_menstrual_period = models.DateField()
    due_date = models.DateField()
    current_trimester = models.IntegerField(choices=[
        (1, 'First Trimester'),
        (2, 'Second Trimester'),
        (3, 'Third Trimester'),
    ])
    is_high_risk = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - Due: {self.due_date}"
    
    @property
    def current_week(self):
        today = date.today()
        weeks_passed = (today - self.last_menstrual_period).days // 7
        return min(weeks_passed, 42)  # Pregnancy is typically 42 weeks max
    
    @property
    def days_remaining(self):
        return (self.due_date - date.today()).days


class NutritionalPlan(models.Model):
    pregnancy_profile = models.ForeignKey(PregnancyProfile, on_delete=models.CASCADE)
    week = models.IntegerField()
    trimester = models.IntegerField()
    calories_needed = models.IntegerField()
    protein_grams = models.IntegerField()
    iron_mg = models.IntegerField()
    calcium_mg = models.IntegerField()
    folic_acid_mcg = models.IntegerField()
    foods_recommended = models.TextField()
    foods_to_avoid = models.TextField()
    supplements = models.TextField()
    
    def __str__(self):
        return f"Week {self.week} - Trimester {self.trimester}"


# The Fourth Trimester: Postpartum Recovery and Mental Health
class PostpartumProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    delivery_date = models.DateField()
    delivery_type = models.CharField(max_length=20, choices=[
        ('vaginal', 'Vaginal Birth'),
        ('c_section', 'C-Section'),
    ])
    baby_weight = models.FloatField(help_text="Baby weight in kg")
    complications = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Postpartum since {self.delivery_date}"
    
    @property
    def weeks_postpartum(self):
        return (date.today() - self.delivery_date).days // 7


class MentalHealthCheck(models.Model):
    postpartum_profile = models.ForeignKey(PostpartumProfile, on_delete=models.CASCADE)
    check_date = models.DateField(auto_now_add=True)
    mood_score = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    anxiety_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    sleep_hours = models.FloatField()
    appetite_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.postpartum_profile.user.username} - {self.check_date}"


# Pelvic Floor Rehabilitation and Kinetic Progression
class PelvicFloorRehab(models.Model):
    postpartum_profile = models.ForeignKey(PostpartumProfile, on_delete=models.CASCADE)
    assessment_date = models.DateField()
    muscle_strength = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    endurance_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    exercises_prescribed = models.TextField()
    progress_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.postpartum_profile.user.username} - {self.assessment_date}"


class ExerciseProgress(models.Model):
    rehab = models.ForeignKey(PelvicFloorRehab, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    sets = models.IntegerField()
    repetitions = models.IntegerField()
    duration_minutes = models.IntegerField()
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    completion_date = models.DateField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.exercise_name} - {self.completion_date}"


# Neonatal Care and Pediatric Vaccination Tracking
class BabyProfile(models.Model):
    postpartum_profile = models.ForeignKey(PostpartumProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_weight = models.FloatField(help_text="Weight in kg")
    birth_length = models.FloatField(help_text="Length in cm")
    apgar_score = models.IntegerField()
    complications = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - Born {self.birth_date}"
    
    @property
    def age_in_months(self):
        today = date.today()
        months = (today.year - self.birth_date.year) * 12 + (today.month - self.birth_date.month)
        return months


class VaccinationRecord(models.Model):
    baby = models.ForeignKey(BabyProfile, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    due_date = models.DateField()
    administered_date = models.DateField(null=True, blank=True)
    administered_by = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    next_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.baby.name} - {self.vaccine_name}"
    
    @property
    def is_overdue(self):
        if self.administered_date:
            return False
        return date.today() > self.due_date


class GrowthRecord(models.Model):
    baby = models.ForeignKey(BabyProfile, on_delete=models.CASCADE)
    record_date = models.DateField()
    weight = models.FloatField(help_text="Weight in kg")
    length = models.FloatField(help_text="Length in cm")
    head_circumference = models.FloatField(help_text="Head circumference in cm")
    milestones = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.baby.name} - {self.record_date}"


# Maternal Early Warning System (MEWS) and Emergency SOS
class MEWS_Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    assessment_date = models.DateTimeField(auto_now_add=True)
    systolic_bp = models.IntegerField()
    diastolic_bp = models.IntegerField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    temperature = models.FloatField()
    oxygen_saturation = models.IntegerField()
    consciousness_level = models.IntegerField(choices=[(i, i) for i in range(1, 5)])
    urine_output = models.FloatField(help_text="Urine output in ml/hour")
    
    def __str__(self):
        return f"{self.user.username} - {self.assessment_date}"
    
    @property
    def mews_score(self):
        score = 0
        
        # Blood pressure scoring
        if self.systolic_bp < 90 or self.systolic_bp > 220:
            score += 3
        elif self.systolic_bp < 100 or self.systolic_bp > 200:
            score += 2
        elif self.systolic_bp < 110 or self.systolic_bp > 180:
            score += 1
            
        # Heart rate scoring
        if self.heart_rate < 40 or self.heart_rate > 130:
            score += 3
        elif self.heart_rate < 50 or self.heart_rate > 110:
            score += 2
        elif self.heart_rate < 60 or self.heart_rate > 100:
            score += 1
            
        # Respiratory rate scoring
        if self.respiratory_rate < 8 or self.respiratory_rate > 30:
            score += 3
        elif self.respiratory_rate < 10 or self.respiratory_rate > 25:
            score += 2
        elif self.respiratory_rate < 12 or self.respiratory_rate > 20:
            score += 1
            
        # Temperature scoring
        if self.temperature < 35.0 or self.temperature > 38.5:
            score += 2
        elif self.temperature < 35.5 or self.temperature > 38.0:
            score += 1
            
        # Oxygen saturation scoring
        if self.oxygen_saturation < 91:
            score += 3
        elif self.oxygen_saturation < 93:
            score += 2
        elif self.oxygen_saturation < 95:
            score += 1
            
        # Consciousness level scoring
        if self.consciousness_level < 3:
            score += 3
        elif self.consciousness_level == 3:
            score += 1
            
        # Urine output scoring
        if self.urine_output < 0.5:
            score += 3
        elif self.urine_output < 1.0:
            score += 2
            
        return score
    
    @property
    def risk_level(self):
        score = self.mews_score
        if score >= 7:
            return "HIGH - Immediate medical attention required"
        elif score >= 5:
            return "MEDIUM - Consult healthcare provider soon"
        elif score >= 3:
            return "LOW - Monitor closely"
        else:
            return "NORMAL"


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.relationship}"


class SOS_Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    alert_time = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=50, choices=[
        ('medical', 'Medical Emergency'),
        ('personal', 'Personal Safety'),
        ('other', 'Other'),
    ])
    location = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.alert_time} - {self.alert_type}"


# Telehealth Integration Models
class HealthcareProvider(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    availability = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"


class TelehealthAppointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telehealth_appointments')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    consultation_type = models.CharField(max_length=20, choices=[
        ('video', 'Video Call'),
        ('audio', 'Audio Call'),
        ('chat', 'Text Chat'),
    ])
    duration_minutes = models.IntegerField(default=30)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.provider.name} - {self.appointment_date}"


# AI Conversational Agent Models
class AIConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation_id = models.CharField(max_length=100, unique=True, default='default_conversation')
    last_activity = models.DateTimeField(auto_now=True)
    message_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.conversation_id}"


class AIMessage(models.Model):
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField()
    is_from_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{'User' if self.is_from_user else 'AI'}: {self.message_text[:50]}..."


class AISymptomChecker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()
    ai_analysis = models.TextField()
    severity_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at} - {self.severity_level}"


class AIMedicationReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=100)
    reminder_time = models.TimeField(default='09:00:00')
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.medication_name}"


class AIHealthInsight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insight_type = models.CharField(max_length=50, choices=[
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise'),
        ('mental_health', 'Mental Health'),
        ('sleep', 'Sleep'),
        ('general', 'General'),
    ])
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"