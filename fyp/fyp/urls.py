# filepath: c:\projects\AIU Addmision\fyp\fyp\urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', include('bkend.urls')),  # Include URLs from the `bkend` app

]
