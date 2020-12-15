from django.contrib import admin
from .models import *
# Register your models here.

#Pedagogical_Module
admin.site.register(Evidence)
admin.site.register(Question)
admin.site.register(Alternative)
admin.site.register(Network)
admin.site.register(Course)
admin.site.register(CourseQuestion)
admin.site.register(Subject)
admin.site.register(NetworkSubject)
admin.site.register(Step)
#Student_Module
admin.site.register(Student)
admin.site.register(StudentSubject)
admin.site.register(StudentCourse)
admin.site.register(StudentCourseEvidence)
admin.site.register(StudentCourseStep)
admin.site.register(StudentCourseSubject)