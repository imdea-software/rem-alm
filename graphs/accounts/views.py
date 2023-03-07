from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def activate_user_profile(request):
    if request.method == "GET":
        if request.user.is_superuser:
            users = User.objects.all()
            return render(request,'accounts/activate_profile.html',{'users':users})
        else:
            return render(request,'accounts/activate_profile.html',{'messages':'No tienes permisos para activar un perfil de usuario.'})

    if request.method == "POST":
        if request.user.is_superuser:
            try:
                request_data = request.POST.copy()
                user = User.objects.get(username=request_data['user'])    

                    
                    
                return render(request,'registration/activate.html',{'account':user})
            except Exception as e:
                message =('Ha habido un error al intentar crear el perfil. Error: ',e)
                return render(request,'registration/activate_edit.html',{'messages':message})
        # else:
            # return render(request,'accounts/activate_profile.html',{'messages':'No tienes permisos para activar un perfil de usuario.'})  