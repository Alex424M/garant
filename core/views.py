from decimal import Decimal
from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import ApplicationForm, RegisterForm
from .models import Property, Application
from django.contrib.auth.decorators import login_required

def catalog(request):
    login_form = AuthenticationForm()
    deal_type = request.GET.get('type')
    properties = Property.objects.all()
    if deal_type:
        properties = Property.objects.filter(deal_type=deal_type)
    
    rooms = request.GET.getlist('rooms')
    property_type = request.GET.get('property_type')
    if rooms:
        properties = properties.filter(rooms__in=rooms)
        
    if property_type:
        properties = properties.filter(property_type=property_type)

    area_start = request.GET.get('areaStart')
    area_end = request.GET.get('areaEnd')
    if area_start:
        try:
            properties = properties.filter(area__gte=area_start)
        except ValueError:
            pass
    if area_end:
        try:
            properties = properties.filter(area__lte=area_end)
        except ValueError:
            pass

    price_start = request.GET.get('priceStart')
    price_end = request.GET.get('priceEnd')
    if price_start:
        try:
            properties = properties.filter(price__gte=price_start)
        except:
            pass
    if price_end:
        try:
            properties = properties.filter(price__lte=price_end)
        except:
            pass
    selected_rooms = request.GET.getlist('rooms')

    paginator = Paginator(properties, 6)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    query_params.pop('page', None)
    
    if deal_type == 'rent':
        title = 'Аренда недвижимости'
    elif deal_type == 'sale':
        title = 'Продажа недвижимости'
    elif property_type == 'house':
        title = 'Дома'
    else:
        title = 'Все объекты'

    return render(request, 'core/catalog.html', {
        'properties': properties,
        'title': title,
        'selected_rooms': selected_rooms,
        'page_obj': page_obj,
        'query_params': query_params.urlencode(),
        "login_form": login_form,
        "page_number" : page_number
    })

def index(request):
    login_form = AuthenticationForm()
    properties_rent = Property.objects.filter(deal_type="rent").order_by('-created_at')[:8]
    properties_buy = Property.objects.filter(deal_type="sale").order_by('-created_at')[:8]
    return render(request, 'core/index.html', {
        'properties_rent': properties_rent,
        'properties_buy': properties_buy,
        "login_form": login_form
    })

def property_detail(request, pk):
    login_form = AuthenticationForm()
    property = get_object_or_404(Property, pk=pk)
    images = property.images.all()
    price_meter = property.price /  Decimal(property.area)
    price_meter = int(price_meter)
    if property.deal_type == 'rent':
        title = 'Аренда недвижимости'
    elif property.deal_type == 'sale':
        title = 'Продажа недвижимости'
    if property.property_type == 'apartment':
        property_type = 'Квартира'
    elif property.property_type == 'Дом':
        property_type = 'Дом'
    return render(request, 'core/property_detail.html', {
        'property': property,
        'images':images,
        'price_meter':price_meter,
        'title': title,
        'property_type':property_type,
        "login_form": login_form
    })

@login_required
def submit_application(request):
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        
        # Находим объект недвижимости, на который подали заявку
        property_obj = Property.objects.get(id=property_id)
        
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.property = property_obj
            application.user = request.user
            application.name = request.user.get_full_name()
            application.email = request.user.email
            application.save()

            return redirect("property_detail", pk=property_id)
        return render(request, "core/property_detail.html", {
            "property": property_obj,
            "form": form
        })
    return redirect("index")

@login_required
def profile_view(request):
    user = request.user
    applications = Application.objects.filter(user=user).order_by('-created_at')


    return render(request, "core/profile.html", {
        "user": user,
        "applications": applications
    })
@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()
        return redirect("profile")

    return render(request, "core/edit_profile.html", {
        "user": user
    })
@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == "POST":
        application.delete()
        return redirect("profile")

    return redirect("profile")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url if next_url else "index")

    return redirect("index")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            login(request, user)
            return redirect("index")
        # если ошибки — просто вернуть страницу с form
        return render(request, "core/index.html", {
            "register_form": form
        })
    return redirect("index")

def logout_view(request):
    logout(request)
    return redirect("index")

def apply(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.property = property
            application.save()
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form})