from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q



level =[
    ('3rd year bachelor\'s degree','L3'),
    ('2nd year master\'s degree','M2')
]

############################################################
class Admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
class DefenseSession(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    level = models.CharField(max_length=40 , choices=level , default = 'L3')

    def __str__(self):
        return f"Session from {self.start_date} to {self.end_date}"
    
class Defense(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='defenses')
    teachers = models.ManyToManyField('Teacher', related_name='defenses')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='defenses')
    session = models.ForeignKey(DefenseSession, on_delete=models.CASCADE, related_name='defenses')
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f"{self.subject.title}  - {self.scheduled_time}"


############################################################
class Department(models.Model):
    name = models.CharField(max_length=40, null=False)
    doyen = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def speciality_count(self):
        return self.speciality_set.count()

    @property
    def teacher_count(self):
        return self.teacher_set.count()

############################################################
    
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    belongs = models.ForeignKey(Department, on_delete=models.CASCADE , default = NULL)
    status=models.BooleanField(default=False)
    keyword= models.CharField(max_length=150 , default = NULL)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
   
    def __str__(self):
        return self.user.first_name
    
    @property
    def subject_count(self):
        return Defense.objects.filter(teachers=self).count()
    @property
    def subject_teacher_count(self):
        return Subject.objects.filter(teacher=self, valable=False).count()


    
############################################################
    
class Enterprise(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40 , null=False ) 
    status=models.BooleanField(default=False)

    @property
    def get_id(self):
        return self.user.id
   
    def __str__(self):
        return self.name
    @property
    def get_name(self):
        return self.user.username

############################################################   
    
class Speciality (models.Model):
    name = models.CharField(max_length=40 , null=False )
    department = models.ForeignKey(Department, on_delete=models.CASCADE , default = NULL)
    def __str__(self):
        return self.name
    @property
    def student_count(self):
        return self.student_set.count()
    @property
    def get_name(self):
        return self.name
############################################################

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    matricule = models.CharField(max_length=40, unique=True, null=False ,default = NULL)
    level = models.CharField(max_length=40 , choices=level , default = 'L3')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=False , default = NULL)
    binome = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='binome_of')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_id(self):
        return self.level
    @property
    def has_validated_choice(self):
        return SubjectChoice.objects.filter(student__in=[self, self.binome], validated_by_student=True).exists()
    def __str__(self):
        return self.user.first_name
    
    
class BinomeRequest(models.Model):
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='binome_request_sender')
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='binome_request_receiver')
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

class SubjectChoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_choices')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='chosen_by')
    validated_by_student = models.BooleanField(default=False)
    affected = models.BooleanField(default=False)
    TYPE_CHOICES = [
        (' ', ' '),
        ('allowed', 'allowed'),
        ('not-allowed', 'not-allowed')
    ]
    teacheraprove = models.CharField(max_length=40, choices=TYPE_CHOICES, default=' ')
    
    
    
############################################################
    
class Subject(models.Model):
    TYPE_CHOICES = [
        ('External', 'External'),
        ('Internal', 'Internal')
    ]
    type = models.CharField(max_length=40, choices=TYPE_CHOICES, default='Internal')
    title = models.CharField(max_length=100, null=False)
    level = models.CharField(max_length=40, choices=level, default='L3')
    description = models.CharField(max_length=250)
    keyword = models.CharField(max_length=100, null=False, default=NULL)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=False, default=NULL)
    STATUS_CHOICES = (
        ('PENDING', 'pending'),
        ('APPROVED', 'approved'),
        ('REJECTED', 'rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    valable = models.BooleanField(default=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    creator_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    creator_id = models.PositiveIntegerField(null=True, blank=True)
    creator = GenericForeignKey('creator_type', 'creator_id')
    validation_commission = models.ManyToManyField('Teacher', related_name='validation_commissions')
    rejection_reason = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title


class SubjectInteraction(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subject', 'teacher')


    


############################################################

class Result(models.Model):
    note = models.FloatField(null=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=NULL)
    defense = models.ForeignKey('Defense', on_delete=models.CASCADE, related_name='results', default=NULL)
    

    def __str__(self):
        return f"{self.student.user.first_name} {self.subject.title}"

############################################################
class Suivi(models.Model):
    choice = models.ForeignKey(SubjectChoice, on_delete=models.CASCADE , default = NULL)
    resume = models.CharField(max_length=150 , null=False )
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student.user.first_name+" "+self.subject.title