"""
URL configuration for hotels project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from users.views import UserAPIView, Authorization
from work_order.views import WorkOrderAPIView, WorkOrdersAPIView
from chatGPT.real_time_chat_views import home, new_chat, error_handler
from chatGPT.views import GetWorkOrderByOpenAiAPIView, AnalyzeWorkOrderAPIView
 
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^work-orders-openai/$', GetWorkOrderByOpenAiAPIView.as_view()),
    re_path(r'^analyze-work-orders-openai/$', AnalyzeWorkOrderAPIView.as_view()),
    path('chatGPT/', home, name='home'),
    path('new_chat/', new_chat, name='new_chat'),
    path('error-handler/', error_handler, name='error_handler'),
    re_path(r'^users/$', UserAPIView.as_view()),
    re_path(r'^auth/$', Authorization.as_view()),    
    re_path(r'^work-orders/$', WorkOrdersAPIView.as_view()),    
    re_path(r'^work-orders/(?P<work_order_id>\w{0,50})/$', WorkOrderAPIView.as_view()),
    
]
