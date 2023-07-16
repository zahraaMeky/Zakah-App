from django.urls import path
from .import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('zakah_type/', views.zakah_types, name='type'),
    path('zakah_sub_type/',views.zakah_Sub_types ,name='sub_type'),
    path('zakah_type/zakah_sub_Donate/', views.zakah_sub_Donate,name='type_Donate'),
    path('zakah_sub_Donate/', views.zakah_sub_Donate,name='donate_sub'),
    path('zakah_thanks/', views.zakah_thanks,name='thanks'),
    path('zakah_sub_Donate/get_money/', views.get_money,name='get_money'),
]