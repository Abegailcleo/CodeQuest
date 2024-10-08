from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from ckeditor.fields import RichTextField


# Badge Model
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)

    def __str__(self):
        return self.name


# Course Model
class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Resource Model for Multiple Downloadable Resources
class Resource(models.Model):
    course = models.ForeignKey(Course, related_name='resources', on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} Points"

# Lesson Model to Structure Courses
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()  # This will store HTML content

    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"

# Quiz Model Associated with Lessons
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question

# UserProfile Model Consolidating User and Learner Information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed_courses = models.ManyToManyField(Course, blank=True)
    badges = models.ManyToManyField(Badge, blank=True)
    python_progress = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    points = models.IntegerField(default=0)  # Moved from Learner model

    def __str__(self):
        return f"{self.user.username}'s profile"

# UserCourseProgress Model to Track Progress in Each Course
class UserCourseProgress(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_profile', 'course', 'lesson')

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.course.title} ({self.progress}%)"

    def all_lessons_completed(self):
        # Check if all lessons for the associated course are completed
        lessons = self.course.lessons.all()
        return all(
            UserCourseProgress.objects.filter(course=self.course, lesson=lesson).filter(completed=True).exists() 
            for lesson in lessons
        )

@receiver(post_save, sender=UserCourseProgress)
def award_badges_on_lesson_completion(sender, instance, created, **kwargs):
    if instance.completed and instance.all_lessons_completed():
        badge, created = Badge.objects.get_or_create(
            name="Course Completer",
            defaults={"description": f"Completed all lessons in {instance.course.title}"}
        )
        instance.user_profile.badges.add(badge)
        instance.user_profile.points += 100  # Example: Award points for completing the course
        instance.user_profile.save()


def complete_lesson(user_profile, lesson):
    user_course_progress, created = UserCourseProgress.objects.get_or_create(
        user_profile=user_profile,
        course=lesson.course
    )
    user_course_progress.completed = True
    user_course_progress.save() 