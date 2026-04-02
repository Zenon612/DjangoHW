from django.shortcuts import render, get_object_or_404
from catalog.models import Phone


def catalog(request):
    sort_param = request.GET.get('sort', 'name')

    sort_mapping = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }
    order_by = sort_mapping.get(sort_param, 'name')

    phones = Phone.objects.all().order_by(order_by)

    return render(request, 'catalog/catalog.html', {
        'phones': phones,
        'current_sort': sort_param,
    })


def phone_detail(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    return render(request, 'catalog/phone_detail.html', {'phone': phone})