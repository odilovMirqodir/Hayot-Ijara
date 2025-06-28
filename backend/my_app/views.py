from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Worker, CheckIn
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


@login_required
def index(request):
    # Today’s date (aware)
    today = timezone.now().date()

    # For widgets: last 7 & 30 days
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    checkins_last_7_days = CheckIn.objects.filter(check_in_time__date__gte=last_7_days).count()
    checkins_last_30_days = CheckIn.objects.filter(check_in_time__date__gte=last_30_days).count()

    # Total active workers
    total_workers = Worker.objects.count()

    # Top & lowest worker in last 30 days
    workers_qs = Worker.objects.annotate(
        checkin_count=Count(
            'checkins',
            filter=Q(checkins__check_in_time__date__gte=last_30_days)
        )
    )
    top_worker = workers_qs.order_by('-checkin_count').first()
    lowest_worker = workers_qs.order_by('checkin_count').first()

    top_worker_name = f"{top_worker.first_name} {top_worker.last_name}" if top_worker else "N/A"
    top_worker_checkins = top_worker.checkin_count if top_worker else 0

    lowest_worker_name = f"{lowest_worker.first_name} {lowest_worker.last_name}" if lowest_worker else "N/A"
    lowest_worker_checkins = lowest_worker.checkin_count if lowest_worker else 0

    # Get filter params
    search_query = request.GET.get('search', '').strip()
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')

    # Base queryset
    checkins = CheckIn.objects.select_related('worker').order_by('-check_in_time')

    # Apply search
    if search_query:
        checkins = checkins.filter(
            Q(worker__username__icontains=search_query) |
            Q(worker__first_name__icontains=search_query) |
            Q(worker__last_name__icontains=search_query)
        )

    # Apply date range
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            checkins = checkins.filter(check_in_time__date__gte=start_date)
        except ValueError:
            pass
    if end_date_str:
        try:
            # include whole end_date
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            checkins = checkins.filter(check_in_time__date__lte=end_date)
        except ValueError:
            pass

    # Paginate (10 per page)
    paginator = Paginator(checkins, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'checkins_last_7_days': checkins_last_7_days,
        'checkins_last_30_days': checkins_last_30_days,
        'total_workers': total_workers,
        'top_worker_name': top_worker_name,
        'top_worker_checkins': top_worker_checkins,
        'lowest_worker_name': lowest_worker_name,
        'lowest_worker_checkins': lowest_worker_checkins,
        'page_obj': page_obj,
        'search_query': search_query,
        'start_date': start_date_str,
        'end_date': end_date_str,
    }
    return render(request, 'index.html', context)


@login_required
def worker_detail(request, worker_id):
    # Fetch the worker or return 404 if not found
    worker = get_object_or_404(Worker, id=worker_id)

    # Get the last 10 check-ins for the worker
    checkins = worker.checkins.all().order_by('-check_in_time')[:10]

    # Calculate total check-ins
    total_checkins = worker.checkins.count()

    # Get the last check-in
    last_checkin = worker.checkins.order_by('-check_in_time').first()

    # Context to pass to the template
    context = {
        'worker': worker,
        'checkins': checkins,
        'total_checkins': total_checkins,
        'last_checkin': last_checkin,
    }

    return render(request, 'worker_detail.html', context)


def test_404(request):
    return render(request, '404.html', status=404)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Login yoki parol xato!')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
