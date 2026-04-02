from django.shortcuts import redirect


def index(request):
    return redirect('catalog')


def show_catalog(request):
    return redirect('catalog:catalog')


def show_product(request, slug):
    return redirect('catalog:phone_detail', slug=slug)
