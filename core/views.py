from django.contrib  import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Paragraph, StudentResult
from .forms import RegisterForm, OTPForm, ParagraphForm, AnswerForm, StudentInfoForm
import random

def home(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def admin_upload(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            paragraph = Paragraph.objects.create(
                content=content,
                created_by=request.user
            )
            messages.success(request, 
                f"Content uploaded successfully! OTP: {paragraph.otp}")
            return redirect('admin_upload')
        else:
            messages.error(request, "Please provide reading content")
    
    return render(request, 'core/admin_upload.html')


def student_access(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                paragraph = Paragraph.objects.get(otp=otp)
                request.session['paragraph_id'] = paragraph.id
                request.session['score'] = 0
                request.session['question_count'] = 0
                return render(request, 'core/reading_page.html', {
                    'paragraph': paragraph,
                })
            except Paragraph.DoesNotExist:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'core/student_access.html', {'form': form})

def check_answer(request):
    if request.method == 'POST':
        paragraph_id = request.session.get('paragraph_id')
        current_word = request.POST.get('current_word', '').strip()
        user_answer = request.POST.get('answer', '').strip().lower()
        
        # Get or initialize score from session
        score = request.session.get('score', 0)
        question_count = request.session.get('question_count', 0)
        
        # Check if answer is correct
        is_correct = user_answer == current_word.lower()
        
        if is_correct:
            score += 1
            request.session['score'] = score
        
        request.session['question_count'] = question_count + 1
        
        paragraph = Paragraph.objects.get(id=paragraph_id)
        return render(request, 'core/result.html', {
        'score': score,
        'correct_word': current_word,
        'student_name': request.user.username
    })

    return redirect('student_access')

def complete_reading(request):
    if request.method == 'POST':
        form = StudentInfoForm(request.POST)
        if form.is_valid():
            paragraph_id = request.session.get('paragraph_id')
            score = request.session.get('score', 0)
            question_count = request.session.get('question_count', 0)
            
            paragraph = Paragraph.objects.get(id=paragraph_id)
            # Create the result with all fields
            StudentResult.objects.create(
                student_name=form.cleaned_data['student_name'],
                paragraph=paragraph,
                score=score,
                total_questions=question_count  # Now this field exists
            )
            
            # Clear session data
            request.session.pop('paragraph_id', None)
            request.session.pop('score', None)
            request.session.pop('question_count', None)
            
            return render(request, 'core/final_result.html', {
        'score': score,
        'total_questions': question_count,
        'student_name': form.cleaned_data['student_name']
    })
    else:
        form = StudentInfoForm()
    return render(request, 'core/complete_reading.html', {'form': form})

@login_required
def view_results(request):
    if request.user.is_staff:
        # Admin sees all results
        results = StudentResult.objects.all().order_by('-created_at')
    else:
        # Teachers see only their students' results
        results = StudentResult.objects.filter(paragraph__created_by=request.user).order_by('-created_at')
    
    return render(request, 'core/view_results.html', {'results': results})

def result_detail(request, result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    return render(request, 'core/result_detail.html', {'result': result})