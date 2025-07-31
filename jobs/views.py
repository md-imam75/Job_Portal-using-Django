from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm
from django.db.models import Q

def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    is_employer = request.user.groups.filter(name='Employer').exists() if request.user.is_authenticated else False
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'is_employer': is_employer})

@login_required
def post_job(request):
    if not request.user.groups.filter(name='Employer').exists():
        return redirect('home')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('my_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def my_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job)
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        action = request.POST.get('action')
        application = get_object_or_404(Application, id=app_id, job=job)
        if action in ['Approved', 'Rejected']:
            application.status = action
            application.save()
        return redirect('applicants', job_id=job_id)
    return render(request, 'jobs/applicants.html', {'job': job, 'applications': applications})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    status_filter = request.GET.get('status')
    applications = Application.objects.filter(applicant=request.user)
    if status_filter in ['Pending', 'Approved', 'Rejected']:
        applications = applications.filter(status=status_filter)
    return render(request, 'jobs/my_applications.html', {'applications': applications, 'status_filter': status_filter})