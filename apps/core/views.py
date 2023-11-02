from django.shortcuts import render
from decouple import config

# Create your views here.
def core(request):
    server_address = request.META['HTTP_HOST']
    if server_address == '127.0.0.1:8000':
        # Enlace local
        admin_link = 'http://127.0.0.1:8000/admin/'
        swagger_link = 'http://127.0.0.1:8000/swagger/'
    else:
        # Enlace de producción
        admin_link = config('ADMIN_URL')
        swagger_link = config('SWAGGER_URL')

    context = {
        'admin_link': admin_link,
        'swagger_link': swagger_link,
    }
    return render(request, 'core/home.html', context)