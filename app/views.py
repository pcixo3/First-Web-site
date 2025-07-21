from django.shortcuts import render, redirect
from .models import Car, Category
from .forms import CarForm

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


def car_create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CarForm()

    return render(request, 'app/create_car.html', {'form': form, 'categories': categories})


def car_update(request, car_id):
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
    car = Car.objects.get(id=car_id)
    car.delete()
    return redirect('index')
