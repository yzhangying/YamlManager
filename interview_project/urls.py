"""zy_interview_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from interview_project import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # re_path('^$', views.index, name='index'),
    re_path('^sign_up$', views.sign_up, name='sign_up'),
    re_path('^login$', views.userlogin, name='login'),
    re_path('^logout$', views.userlogout, name='logout'),
    re_path('^create_cluster$', views.create_cluster, name='create_cluster'),
    re_path('^connection_cluster$', views.connection_cluster, name='connection_cluster'),
    re_path('^$', views.manage, name='manage'),
    re_path('^template_manage$', views.template_mange, name='template_manage'),
    re_path('^upload_file$', views.upload_file, name='upload_file'),
    re_path('^detail_files$', views.detail_files, name='detail_files'),
    re_path('^del_file$', views.del_file, name='del_file'),
    re_path('^edit_yaml$', views.edit_yaml, name='edit_yaml'),
    re_path('^template_list$', views.template_list, name='template_list'),
    re_path('^template_create$', views.template_create, name='template_create'),
    re_path('^get_template_args$', views.get_template_args, name='get_template_args'),
    re_path('^template_detail$', views.template_detail, name='template_detail'),
    re_path('^template_edit$', views.template_edit, name='template_edit'),
    re_path('^del_template$', views.del_template, name='del_template'),
]
