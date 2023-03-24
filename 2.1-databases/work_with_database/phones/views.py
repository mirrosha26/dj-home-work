from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Phone
from decimal import Decimal

def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort')
    page_number = request.GET.get('page')
    all_phones = Phone.objects.all()
    template = 'catalog.html'

    if sort == 'name':
        all_phones = all_phones.order_by('name')
    
    if sort == 'min_price':
        all_phones = all_phones.order_by('price')
    
    if sort == 'max_price':
        all_phones = all_phones.order_by('-price')

    if not page_number:
        page_number = 1

    paginator = Paginator(all_phones, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'phones': page_obj,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {
        'phone': phone
    }
    return render(request, template, context)
