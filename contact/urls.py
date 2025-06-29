from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [

    path('search/', views.search, name='search'),
    path('', views.index, name='index'),

    #CRUD

    #(Read)
    path('contact/<int:contact_id>/', views.contact, name='contact'),

    #(Update)
    path('contact/<int:contact_id>/update/', views.update, name='update'),

    #(Create)
    path('contact/create/', views.create, name='create'),

    #(Delete)
    path('contact/<int:contact_id>/delete', views.delete, name='delete'),


    path('user/create/', views.register, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/update/', views.user_update, name='user_update' )
    
    ]



