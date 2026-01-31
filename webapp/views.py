from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import Head, Order
from django.db import transaction
from datetime import date

# Create your views here.
@login_required
def home_view(request):
    username = request.user.get_username()
    orders = Order.objects.filter(user=request.user)[:4]
    today = date.today()
    status = ''

    for order in orders:
        days_until = (order.expected_arrival_date - today).days

        if days_until < 0:
            status = "Arrived"
        else:
            status = f"Arriving in {days_until} days"

    return render(request, 'home/home.html', {'username': username, 'user': request.user, "orders": orders, "status": status})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error = "Invalid Credentials."
            return render(request, 'accounts/login.html', {"error": error})
    return render(request, 'accounts/login.html')

@login_required
def stocks_view(request):
    query = request.GET.get('q')
    sale_status = request.GET.get('sale_status')
    heads = Head.objects.all()
    
    if query:
        heads = heads.filter(animal__icontains=query)

    if sale_status == '1':
        heads = heads.filter(ready_for_sale=True)
    elif sale_status == '0':
        heads = heads.filter(ready_for_sale=False)

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_records')

        with transaction.atomic():
            records = Head.objects.filter(id__in=selected_ids)

            for record in records:
                Order.objects.create(
                    animal=record.animal,
                    animal_id=record.pk,
                    total_price=(record.price_per_kilo * record.weight),
                    user=request.user,
                )
            records.delete()

    return render(request, 'home/stocks.html', {"heads": heads})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    else:
        return render(request, "accounts/logout.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = str(form.cleaned_data.get("username"))
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username, password=password)
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'accounts/register.html', {"form": form})
    return render(request, 'accounts/register.html', {"form": RegisterForm(request.POST)})

@login_required
def shipping_view(request):
    all_orders = Order.objects.filter(user=request.user)
    return render(request, 'home/shipping.html', {'orders': all_orders})

def about_view(request):
    return render(request, 'home/about.html')    