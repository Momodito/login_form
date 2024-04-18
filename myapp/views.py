from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import json
from .models import UserLogin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


@method_decorator(csrf_exempt, name="dispatch")
class Index(View):
    def get(self, request):
        user = request.user
        print(user.username)
        return render(request,'index.html', context={"username" : user.username})

@method_decorator(login_required, name="dispatch")
class Home(View):

    def get(self, request, username = None):
        try:
            user = UserLogin.objects.get(username = username)
            return render(request, 'home.html', context={"username" : user.username})
        
        
        except UserLogin.DoesNotExist:
        
            return redirect('index')

            
        
        
@method_decorator(csrf_exempt, name="dispatch")
class UserRegistration(View):

    def get(self,request):
        return render(request,'register.html')

    def post(self, request):
        try:
            name = request.POST.get('name')
            last_name = request.POST.get('lastname')
            username = request.POST.get('nickname')
            email = request.POST.get('email')
            password = request.POST.get('contrasena')
            hashed_password = make_password(password)
            user = UserLogin(first_name=name, last_name=last_name, username=username, email=email, password=hashed_password)
            print(user)
            user.save()

            
            return redirect('index')
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Error al registrarse"})

    
@method_decorator(csrf_exempt, name="dispatch")
class UserSignIn(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request,'login.html')
    
    def post(self, request):

        username = request.POST.get('nickname')
        password = request.POST.get('contrasena')
        user_db = UserLogin.objects.get(username = username)

        if check_password(password, user_db.password):
            print("Ok")
            user = authenticate(request, username = username, password = password)

        
            login(request, user)

            if user.is_online == True:

                return JsonResponse({'message': 'Ya existe una persona en línea con esta cuenta'}, status=401)
            user.is_online = True  # Cambiar el campo is_online a True

            user.save()

            # username = request.user.username
            # return render(request, 'home.html', {'username': username})

            return redirect('home', user.username)
            
        
        else:
            return JsonResponse({'message': 'Credenciales inválidas'}, status=401)
        
@method_decorator(login_required, name="dispatch")
class UserLogout(View):
    def post(self, request):
        # if request.user.is_authenticated:  # Verifica si el usuario está autenticado
        user = request.user
        user.is_online = False  # Cambiar el campo is_online a False
        user.save()
        logout(request)  # Cierra la sesión del usuario

        

        return redirect('index')