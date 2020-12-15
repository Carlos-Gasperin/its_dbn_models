from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Student(models.Model):
    name = models.CharField(max_length=100, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Evidence(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pk} - {self.name}'

class Question(models.Model):
    description = models.CharField(default='', max_length=255)

    def __str__(self):
        return f'{self.description}'

class Step(models.Model):
    question = models.ForeignKey(Question, related_name='steps', on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    evidences = models.ManyToManyField(Evidence, blank=True)

    def __str__(self):
        return f'{self.content}'

class Alternative(models.Model):
    BLANK_EXPRESSION = 'blank expression'
    MULTIPLE_CHOICE = 'multiple choice'

    CHOICES = [
        (BLANK_EXPRESSION, 'Expressão'),
        (MULTIPLE_CHOICE, 'Múltipla escolha')
    ]

    step = models.ForeignKey(Step, related_name='alternatives', on_delete=models.CASCADE)
    content = models.TextField(max_length=50)
    category = models.CharField(max_length=85, choices=CHOICES, default=MULTIPLE_CHOICE)
    number = models.CharField(max_length=5, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.step.id} {self.number} {self.status} {self.content}'

class Network(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pk} - {self.name}'

class Course(models.Model):
    name = models.CharField(max_length=255)
    network = models.ForeignKey(Network, related_name='courses', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.name}'

class CourseQuestion(models.Model):
    course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='courses', on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.course.name} - {self.number} - {self.question}'

class Subject(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pk} - {self.name}'

class NetworkSubject(models.Model):
    network = models.ForeignKey(Network, related_name='subjects', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='networks_subjects', on_delete=models.CASCADE)
    parents = models.ManyToManyField(Subject, related_name='networks_subjects_parents', null=True, blank=True)
    evidences = models.ManyToManyField(Evidence,related_name='networks_subjects_evidences', null=True, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.network.name} - {self.subject.name}'

class StudentCourse(models.Model):
    course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='courses', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class StudentCourseEvidence(models.Model):
    course = models.ForeignKey(Course, related_name='student_evidences', on_delete=models.CASCADE)
    evidence = models.ForeignKey(Evidence, related_name='student_courses', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='courses_evidences', on_delete=models.CASCADE)
    time_slices = models.IntegerField(default=0)
    observations = models.CharField(default='', max_length=255)

    def __str__(self):
        return f'{self.student.user.username} - {self.evidence.name}' # pylint: disable=maybe-no-member

class StudentCourseSubject(models.Model):
    course = models.ForeignKey(Course, related_name='student_subjects', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='student_courses', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='courses_subjects', on_delete=models.CASCADE)
    time_slice = models.IntegerField(default=0)
    true_probability = models.DecimalField(default=0.5, decimal_places=10, max_digits=10)

class StudentCourseStep(models.Model):
    course = models.ForeignKey(Course, related_name='students_steps', on_delete=models.CASCADE)
    step = models.ForeignKey(Step, related_name='students_courses', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='courses_steps', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class StudentSubject(models.Model):
    subject = models.ForeignKey(Subject, related_name='students_subjects', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='subjects', on_delete=models.CASCADE)
    # time_slice = models.IntegerField(default=0) #Future proofing
    true_probability = models.DecimalField(default=0.5, decimal_places=10, max_digits=10) #Future proofing
    level = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student.user.username} - {self.subject.name}(T: {self.time_slice})'
        