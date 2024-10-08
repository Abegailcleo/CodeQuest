from django.contrib import admin
from .models import Badge, Course, Resource, Lesson, Quiz, UserProfile, UserCourseProgress
from django.contrib import messages

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    
   
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'course', 'lesson', 'progress', 'completed', 'last_accessed')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed_courses', 'badges', 'python_progress', 'current_streak', 'points')




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('level', 'created_at')
    inlines = [LessonInline]

admin.site.register(Badge)
admin.site.register(Resource)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson')
    search_fields = ('question',)
    list_filter = ('lesson',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'current_streak', 'badge_count')
    search_fields = ('user__username',)

    def badge_count(self, obj):
        return obj.badges.count()
    badge_count.short_description = 'Number of Badges'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    search_fields = ('title', 'content')
    list_filter = ('course',)


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'course', 'lesson', 'progress', 'completed', 'last_accessed')
    search_fields = ('user_profile__user__username', 'course__title', 'lesson__title')  # Add lesson search
    list_filter = ('course', 'completed')
