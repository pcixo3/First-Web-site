from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Car, Category
from .forms import CarForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CarForm()

    cars = Car.objects.all()
    return render(request, 'app/index.html', {'form': form, 'cars': cars})


def detail_view(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'app/detail.html', {'car': car})

@login_required(login_url='login')
def car_create(request):
    categories = Category.objects.all()

    if request.method == "POST":
        form = CarForm(request.POST)
        files = request.FILES.getlist('images')  # Получаем список файлов

        if form.is_valid():
            car = form.save()  # Сохраняем объект Car

            # Сохраняем все загруженные изображения
            for f in files:
                CarImage.objects.create(car=car, image=f)

            return redirect('index')
    else:
        form = CarForm()

    return render(request, 'app/create_car.html', {'form': form, 'categories': categories})


def car_update(request, car_id):
    if not request.user.is_authenticated:
        return redirect('login')

    car = Car.objects.get(id=car_id)

    if request.method == 'POST':
        car.title = request.POST['title']
        car.model = request.POST['model']
        car.category = request.POST['category']
        car.year = request.POST['year']
        car.image = request.FILES['image']
        car.price = request.POST['price']
        car.description = request.POST['description']

        category_id = request.POST['category_id']
        category = Category.objects.get(id=category_id)

        car.save()
        return redirect('detail_view', car_id)

    return render(request, 'app/update_car.html', {'car': car})


def car_delete(request, car_id):
    if not request.user.is_authenticated:
        return redirect('login')

    car = Car.objects.get(id=car_id)
    car.delete()
    return redirect('index')

def user_register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт был создан!')
            return redirect('index')

        for field, errors in form.errors.items():

            for error in errors:
                messages.error(request, f'{error}')

    form = UserCreationForm()

    return render(request, 'app/register.html', {'form': form})
def user_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('index')

        messages.error(request, 'Неправильный логин или пароль')

    return render(request, 'app/user_login.html')


def user_logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')

def about_us(request):
    return render(request, 'app/about_us.html')
