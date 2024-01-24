from django.urls import path, include
from django.contrib import admin
from restaurant import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    path('registration/', views.registration_view, name='registration'), #you have to register through restaurant/registration to access menu
    path('menu/', views.menuView.as_view(), name='menu'),
    path('menu-item/', views.MenuItemsView.as_view(), name='menu-item'),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    #path('menu/', views.menu, name="menu"),
    #path('bookings/', include(router.urls), name='bookings'),
    path('about/', views.about, name="about"),    
    path('book/', views.book, name='book'),
    path('bookings/', views.bookings, name='bookings'),
    #path('bookings/', views.bookings.as_view(), name='bookings'),
    path('', include(router.urls)),
    path('reservations/', views.reservations, name="reservations"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),    
    path('category', views.CategoriesView.as_view()),
    path('api-token-auth/', obtain_auth_token),
    
    
]