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
from django.db import connection
from django.urls import reverse


@method_decorator(csrf_exempt, name="dispatch")
class Index(View):
    def get(self, request):
        user = request.user
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
            user.save()

            
            return redirect('index')
        except Exception as e:
            print(e)
            return JsonResponse({"Error": "Error al registrarse"})

    
@method_decorator(csrf_exempt, name="dispatch")
class UserSignIn(View):

    # def get(self,request):
    #     if request.user.is_authenticated:
    #         return redirect('index')
    #     return render(request,'login.html')
    
    # def post(self, request):
    #     username = request.POST.get('nickname')
    #     password = request.POST.get('contrasena')
    #     try:
    #         user_db = UserLogin.objects.get(username=username)
    #     except UserLogin.DoesNotExist:
    #         return render(request, 'login.html', {'error': 'Usuario no encontrado.'})

    #     if check_password(password, user_db.password):
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             if user.is_online:
    #                 return render(request, 'login.html', {'error': 'Ya existe una persona en línea con esta cuenta.'})
    #             login(request, user)
    #             user.is_online = True
    #             user.save()
    #             return redirect('home', user.username)
    #         else:
    #             return render(request, 'login.html', {'error': 'Credenciales inválidas.'})
    #     else:
    #         return render(request, 'login.html', {'error': 'Credenciales inválidas.'})


    ############################ VULNERABILIDAD INJECTION SQL ##################################
        def get(self,request):
            if request.user.is_authenticated:
                return redirect('index')
            return render(request,'login.html')
    
        def post(self, request):
            username = request.POST.get('nickname')
            password = request.POST.get('contrasena')
            query = f"SELECT * FROM myapp_userlogin WHERE username = '{username}'"
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    users = cursor.fetchall()
            except Exception as e:
                return render(request, 'login.html', {'error': f'Error en la consulta: {e}'})
            user_valid = None
            for u in users:
                db_username = u[4]  
                db_password = u[1]  
                if db_username == username and check_password(password, db_password):
                    user_valid = u
                    break
            if len(users) > 1:
                return render(request, 'login.html', {'error': f'Resultado del query: {users}'})
            elif not users:
                return render(request, 'login.html', {'error': 'Usuario no encontrado.'})
            elif not user_valid:
                return render(request, 'login.html', {'error': 'Credenciales inválidas.'})
            else:
                try:
                    user_obj = UserLogin.objects.get(username=username)
                except UserLogin.DoesNotExist:
                    user_obj = UserLogin.create_user(username=username)
                login(request, user_obj)
                return redirect('home', username)
            
@method_decorator(login_required, name="dispatch")
class UserLogout(View):
    def post(self, request):
        # if request.user.is_authenticated:  # Verifica si el usuario está autenticado
        user = request.user
        user.is_online = False  # Cambiar el campo is_online a False
        user.save()
        logout(request)  # Cierra la sesión del usuario

        

        return redirect('index')