import uuid

from django.db import models

# Create your models here.
class Course(models.Model):
	class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
	
	id = models.UUIDField(primary_key=True, defualt=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='modules'
    )
    title = models.CharField(max_length=255)
    lesson = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} -> {self.title}"


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='lessons'
    )
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        related_name='lessons'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):



class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    text = models.TextField()
    is_boolean = models.BooleanField(default=False, help_text="Designates if this is a True/False question")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Q: {self.text[:50]}"


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='choices'
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False, help_text="Designates if this choice is the correct answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Correct" if self.is_correct else "Incorrect"
        return f"{self.text} ({status})"
