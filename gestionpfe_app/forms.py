from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.core.validators import MaxValueValidator
from . import models
from django.utils import timezone

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'ex-usthbmaildz'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'password1',
        'id': 'password',
    }))


class AdminLoginForm(LoginForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)  # Applique les validations de base
        if not user.groups.filter(name='ADMIN').exists():
            raise forms.ValidationError("Connection denied. You are not authorized to log in as an administrator.", code='invalid_login')

class TeacherLoginForm(LoginForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.groups.filter(name='TEACHER').exists():
            raise forms.ValidationError("Connection denied. You are not authorized to log in as a teacher.", code='invalid_login')


class StudentLoginForm(LoginForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.groups.filter(name='STUDENT').exists():
            raise forms.ValidationError("Connection denied. You are not authorized to log in as a student.", code='invalid_login')


class EnterpriseLoginForm(LoginForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.groups.filter(name='ENTREPRISE').exists():
            raise forms.ValidationError("Connection denied. You are not authorized to log in as an enterprise.", code='invalid_login')



class SigupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'inputtxt'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'inputtxt'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'inputtxt'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'inputtxt'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'inputtxt',
        'id': 'password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'inputtxt',
        'id': 'password1',
    }))
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class SigupEntForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'inputtxt'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'inputtxt'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'inputtxt',
        'id': 'password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'inputtxt',
        'id': 'password1',
    }))
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class SigupEnt1Form(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'inputtxt'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'inputtxt'
    }))
    class Meta:
        model = User
        fields = ['username', 'email']

class Sigup1Form(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'inputtxt'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'inputtxt'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'inputtxt'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'inputtxt'
    }))

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']

    
class AdminForm(forms.ModelForm):
    status = forms.BooleanField(label='Status', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'checkbox'
    }))
    class Meta:
        model = models.Admin
        fields = ('status',)

class EntrepriseForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'inputtxt',  
        'placeholder': 'Name Of The Entreprise'  
    }))
    status = forms.BooleanField(label='Status', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'checkbox'
    }))
    class Meta:
        model=models.Enterprise
        fields=['name','status']

class DepartmentAddForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'inputtxt',
        'placeholder': 'Name Of The Department'
    }))
    doyen = forms.ModelChoiceField(queryset=models.Teacher.objects.all(), empty_label="Select the Leader", required=False ,widget=forms.Select(attrs={
        'class': 'inputtxt' 
        
    }))

    class Meta:
        model = models.Department
        fields = ['name', 'doyen']



class DepartmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'inputtxt',
        'placeholder': 'Name Of The Department'
    }))
    doyen = forms.ModelChoiceField(queryset=models.Teacher.objects.none(), required=False)

    class Meta:
        model = models.Department
        fields = ['name', 'doyen']

    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)
        super(DepartmentForm, self).__init__(*args, **kwargs)
        if department_id:
            self.fields['doyen'].queryset = models.Teacher.objects.filter(belongs_id=department_id)
        self.fields['doyen'].widget.attrs.update({'class': 'inputtxt'})


class SpecialityForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'inputtxt',  
        'placeholder': 'Name Of The Speciality'  
    }))
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),empty_label="Department" ,widget=forms.Select(attrs={
        'class': 'inputtxt' 
        
    }))
    class Meta:
        model=models.Speciality
        fields=['name','department']

   
class TeacherForm(forms.ModelForm):
    belongs = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Select Department", widget=forms.Select(attrs={
        'class': 'departchoose'
    }))
   
    status = forms.BooleanField(label='Status', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'checkbox'
    }))
    
    class Meta:
        model=models.Teacher
        fields=['belongs' ,'status']

class TeacherKeywordsForm(forms.ModelForm):
    keyword = forms.CharField(max_length=150, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Your Keywords',
        'class': 'description'
    }))
    class Meta:
        model=models.Teacher
        fields=['keyword']





class StudentForm(forms.ModelForm):
    matricule = forms.CharField(max_length=40, required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'Register',
        'class': 'inputtxt',
        'min': 1,
    }))
    speciality = forms.ModelChoiceField(queryset=models.Speciality.objects.all(), empty_label="Select Speciality", widget=forms.Select(attrs={
        'class': 'departchoose' 
         }))
    level = forms.ChoiceField(choices=models.level, widget=forms.Select(attrs={
        'class': 'departchoose' 
          }))
    status = forms.BooleanField(label='Status', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'checkbox'
    }))
    
    class Meta:
        model=models.Student
        fields=['matricule','speciality','level','status']



####################################################################################################################
class SubjectForm(forms.ModelForm):
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        'placeholder': 'Title',
        'class': 'inputtxt'
    }))
    
    level = forms.ChoiceField(choices=models.level, widget=forms.Select(attrs={
        'class': 'departchoose' 
          }))
    speciality = forms.ModelChoiceField(queryset=models.Speciality.objects.all(),empty_label='Choose Speciality', widget=forms.Select(attrs={
        'class': 'departchoose' 
         }))
    description = forms.CharField(max_length=250,widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'class': 'description'
    }))
    keyword = forms.CharField(max_length=150,widget=forms.TextInput(attrs={
        'placeholder': 'Keywords',
        'class': 'inputtxt'
    }))
   
    class Meta:
        model=models.Subject
        fields=['title','speciality','level','description','keyword']
        

class SubjectviewForm(forms.ModelForm):
    type = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'inputtxt'
    }))
    title = forms.CharField(widget=forms.TextInput(attrs={
        
        'readonly': 'readonly',
        'class': 'inputtxt'
    }))
    teacher = forms.CharField(widget=forms.TextInput(attrs={
        
        'readonly': 'readonly',
        'class': 'inputtxt'
    }))
    level = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'inputtxt' 
          }))
    speciality = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'inputtxt' 
         }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'readonly': 'readonly',
        'class': 'description'
    }))
    rejection_reason = forms.CharField(widget=forms.Textarea(attrs={
        'readonly': 'readonly',
        'class': 'description'
    }))
    keyword = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'inputtxt'
    }))
   
    class Meta:
        model=models.Subject
        fields=['type','title','speciality','level','description','keyword','rejection_reason']
        


class RejectSubjectForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'inputtxt'
    }))
    description = forms.CharField(max_length=150, widget=forms.Textarea(attrs={
        'readonly': 'readonly',
        'class': 'description'
    }))
    rejection_reason = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Rejection Reason',
        'class': 'inputtxt'
    }))

    class Meta:
        model = models.Subject
        fields = ['title', 'description', 'rejection_reason']

class SubjectFilterForm(forms.Form):
    subject_type = forms.ChoiceField(
        choices=[
            ('', 'All'), 
            ('External', 'External'),
            ('Internal', 'Internal')
        ],
        required=False,
        label="Type of subject"
    )

###########################################################################################################

class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'email',
        'class': 'ex-usthbmaildz-jki'
    }))
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={
        'placeholder': 'your meesage',
        'class': 'feedbacktxt'
    }))


class DefenseSessionForm(forms.ModelForm):
    class Meta:
        model = models.DefenseSession
        fields = ['start_date', 'end_date','level']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'inputtxt'}, format='%d-%m-%YT%H:%M'),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'inputtxt'}, format='%d-%m-%YT%H:%M'),
            'level': forms.Select(attrs={'class': 'inputtxt'}),
        }
    def __init__(self, *args, **kwargs):
        super(DefenseSessionForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%d-%m-%YT%H:%M',)
        self.fields['end_date'].input_formats = ('%d-%m-%YT%H:%M',)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date < timezone.now():
                self.add_error('start_date', 'Start date cannot be in the past.')
            if end_date <= start_date:
                self.add_error('end_date', 'End date must be after the start date.')

        return cleaned_data
    
class ResultForm(forms.ModelForm):
    class Meta:
        model = models.Result
        fields = ['note']
        widgets = {
            'note': forms.NumberInput(attrs={
                'placeholder': 'Grade',
                'class': 'inputtxt',
                'min': 0,
                'max': 20
            })
        }

    student_choice = forms.ModelChoiceField(queryset=None, required=True, empty_label=None, widget=forms.Select(attrs={
        'class': 'inputtxt'
    }))

    def __init__(self, *args, **kwargs):
        defense_id = kwargs.pop('defense_id', None)
        teacher = kwargs.pop('teacher', None)
        super(ResultForm, self).__init__(*args, **kwargs)
        defense = models.Defense.objects.get(id=defense_id)
        students = [defense.student]
        if defense.student.binome:
            students.append(defense.student.binome)

        # Exclude students who have already been graded by the current teacher
        graded_students = models.Result.objects.filter(defense=defense, teacher=teacher).values_list('student', flat=True)
        self.fields['student_choice'].queryset = models.Student.objects.filter(id__in=[s.id for s in students]).exclude(id__in=graded_students)
        self.fields['student_choice'].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name}"

       
        

class SuiviForm(forms.ModelForm):
    resume = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Summary',
        'class': 'description'
    }))

    class Meta:
        model = models.Suivi
        fields = ['resume']