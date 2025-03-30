"""
URL configuration for Momreceipes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import login, signup
from home.views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('recipe/<uuid:recipe_id>/', recipe_detail, name='recipe_detail'),
    path("add_recipe/", add_recipe, name="add_recipe"),
    path('recipe/<uuid:recipe_id>/delete/', delete_recipe, name='delete_recipe'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
