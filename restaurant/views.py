from django.shortcuts import render, redirect
from rest_framework import generics
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Menu, MenuItem, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import BookingSerializer, menuSerializer, UserSerializer, MenuItemSerializer,CategorySerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login, authenticate
from django.core import serializers
from datetime import datetime
from .forms import BookingForm, MenuItemForm, RegistrationForm
from . import templates
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book')  # Redirect to the home page or another page after registration
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def index(request):
    return render(request, 'index.html', {})

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                name=data['name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
                No_of_guests=data['No_of_guests']
                
            )            

            def send_reservation_notification(booking_data):
                # Get admin email address
                admin_email = 'littlereservations@gmail.com'  # Replace with your admin email
                # Load email template
                email_subject = 'New Reservation'
                email_body = render_to_string('reservation_email.html', {'booking': booking_data})
                text_content = strip_tags(email_body)
                # Send email
                send_mail(email_subject, text_content, 'littlereservations@gmail.com', [admin_email], html_message=email_body)
            
            booking.save()
            send_reservation_notification(data)
            return render(request, 'reservation_email.html', {'booking': data})
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

    
class BookingViewSet(viewsets.ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer
    permission_classes=[IsAuthenticated]


class menuView(generics.ListCreateAPIView):
    items=Menu.objects.all()
    serializer=menuSerializer()    

    def get(self, request):
        menu_data = Menu.objects.all()
        main_data = {"menu": menu_data}
        return render(request, 'menu.html', {"menu": main_data})

    def post(self, request):
        serializer=menuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({"status" : "success", "data":serializer.data})


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get(self, request, *args, **kwargs):
        # Render an HTML template for GET requests
        menu_item = self.get_queryset()
        return render(request, 'menu_item.html', {'menu_item': menu_item})

    def post(self, request, *args, **kwargs):
        form = MenuItemForm()
        if request.method == 'POST':
            form = MenuItemForm(request.POST)
            if form.is_valid():
                form.save()
        context = {'form':form}
        return render(request, 'menu_item.html', context)

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer