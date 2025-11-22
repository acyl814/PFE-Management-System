from django.contrib import admin
from .models import Department, Admin, Teacher,Enterprise ,Student, Speciality, Subject,BinomeRequest, Result, SubjectChoice ,Defense,DefenseSession, Suivi ,SubjectInteraction

admin.site.register(Department)
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Enterprise)
admin.site.register(Student)
admin.site.register(Speciality)
admin.site.register(Subject)
admin.site.register(Result)
admin.site.register(SubjectChoice)
admin.site.register(Defense)
admin.site.register(DefenseSession)
admin.site.register(BinomeRequest)
admin.site.register(Suivi)
admin.site.register(SubjectInteraction)