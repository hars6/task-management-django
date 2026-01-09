from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.db.models import Q # Import Q for advanced search
from django.contrib import messages
from django.contrib.auth.models import User

# --- Auth View ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately after registration
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Task Views (Protected) ---

@login_required
def task_list(request):
    # 1. Start with all tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user).order_by('due_date')

    # 2. Get data from the Search Bar
    search_query = request.GET.get('search')
    if search_query:
        # Search in Title OR Description
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # 3. Get data from the Filter Dropdown
    status_filter = request.GET.get('status')
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks, 
        'request': request # Pass request to keep search terms in the box
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user # Assign the task to the logged-in user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'type': 'Create'})

@login_required
def task_update(request, pk):
    # Ensure user can only edit their own task
    task = get_object_or_404(Task, pk=pk, user=request.user) 
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'type': 'Update'})

@login_required
def task_delete(request, pk):
    # Ensure user can only delete their own task
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'registration/reset_password.html')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful! You can now login.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "User with that username does not exist.")

    return render(request, 'registration/reset_password.html')