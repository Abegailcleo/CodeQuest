from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import subprocess
from .models import UserProfile, Badge, Learner, Course, Lesson

# Welcome View
def welcome(request):
    return render(request, 'welcome.html')

# Home View
@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'home.html', context)

# Course List View
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# Course Detail View (this view will handle selected course)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})

# Module View (if needed)
def module(request):
    return render(request, 'module.html')

# Leaderboard View
@login_required
def leaderboard(request):
    top_learners = Learner.objects.order_by('-points')[:10]
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'top_learners': top_learners,
        'user_profile': user_profile,
    }
    return render(request, 'leaderboard.html', context)

# Profile View
@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    completed_courses = user_profile.completed_courses.all()
    badges = user_profile.badges.all()
    return render(request, 'profile.html', {
        'user': request.user,
        'completed_courses': completed_courses,
        'badges': badges,
    })

# Coding Exercise View
def coding_exercise(request):
    if request.method == 'POST':
        submitted_code = request.POST.get('code')
        return HttpResponse(f"Submitted code:<br><pre>{submitted_code}</pre>")
    return render(request, 'coding_exercise.html')

# Submit Code View
def submit_code(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        code = data.get('code')
        try:
            with open('temp_code.py', 'w') as file:
                file.write(code)
            result = subprocess.run(['python3', 'temp_code.py'], capture_output=True, text=True)
            return JsonResponse({'result': result.stdout + result.stderr})
        except Exception as e:
            return JsonResponse({'result': str(e)})
    return JsonResponse({'result': 'Invalid request method.'})

# Sign-Up View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)  # Create UserProfile if it doesn't exist
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up and logged in.')
            return redirect('home')
        else:
            for error in form.errors.values():
                for err in error:
                    messages.error(request, err)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')  # Render login template if not POST
