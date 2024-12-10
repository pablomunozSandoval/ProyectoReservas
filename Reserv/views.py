from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from .models import Doctor, Appointment
from app.firebase_config import db
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Verificar las credenciales en Firestore
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username).where('password', '==', password).stream()

        user_exists = False
        user_data = None
        for user in query:
            user_exists = True
            user_data = user.to_dict()
            break
        
        if user_exists:
            # Crear el usuario en Django si no existe
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)
            
            # Autenticar al usuario en Django
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                role = user_data.get('role')
                if role == 'doctor':
                    return redirect('home')
                elif role == 'cliente':
                    return redirect('home')
            else:
                messages.error(request, 'Error de autenticación en Django')
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    # Si no es una solicitud POST, renderizar la página de login
    return render(request, 'Reserv/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Verificar si el usuario ya existe en Firestore
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username).stream()
        
        user_exists = False
        for user in query:
            user_exists = True
            break
        
        if user_exists:
            return render(request, 'Reserv/register.html', {'error': 'El nombre de usuario ya está registrado.'})
        
        # Crear el usuario en Firestore
        users_ref.add({
            'username': username,
            'password': password
        })
        
        # Crear el usuario en Django
        User.objects.create_user(username=username, password=password)
        
        return redirect('login')
    return render(request, 'Reserv/register.html')

@login_required
def home(request):
    # Obtener la lista de doctores desde Firestore
    doctors_ref = db.collection('doctors')
    doctors = [doc.to_dict() for doc in doctors_ref.stream()]
    
    return render(request, 'Reserv/home.html', {'doctors': doctors})

@login_required
def citas_view(request):
    # Obtener las citas del usuario desde Firestore
    appointments_ref = db.collection('appointments').where('user', '==', request.user.username).stream()
    appointments = [appointment.to_dict() for appointment in appointments_ref]
    
    return render(request, 'Reserv/citas.html', {'appointments': appointments})

def logout_view(request):
    logout(request)
    return redirect('login')

# Lista de control para reservas
reservas = [None] * 5  # Un máximo de 5 reservas

@login_required
def reserve_view(request, doctor_id):
    # Buscar el doctor por id en Firestore
    doctor_ref = db.collection('doctors').document(str(doctor_id))
    doctor = doctor_ref.get().to_dict()
    
    if doctor is None:
        return redirect('home')  # Si no se encuentra el doctor, redirigir a home

    # Verificar si ya se ha hecho una reserva para este doctor
    if reservas[doctor_id - 1] is not None:
        return render(request, 'Reserv/error.html', {'message': 'Ya tiene una reserva con este doctor.'})

    # Si el doctor está disponible y no tiene reserva
    if request.method == 'POST':
        nombre_cliente = request.user.username  # Usar el nombre de usuario autenticado
        if nombre_cliente:
            # Realizar la reserva en Firestore
            db.collection('reservations').add({
                'doctor_id': doctor_id,
                'nombre_cliente': nombre_cliente
            })
            reservas[doctor_id - 1] = nombre_cliente
            doctor_ref.update({'available': False})  # Marcar al doctor como no disponible en Firestore
            return render(request, 'Reserv/exito.html', {'doctor': doctor, 'nombre_cliente': nombre_cliente})
        else:
            return render(request, 'Reserv/error.html', {'message': 'Por favor ingrese su nombre para realizar la reserva.'})

    return render(request, 'Reserv/reserva.html', {'doctor': doctor})

@login_required
def mis_citas(request):
    # Filtrar las citas reservadas por el usuario desde Firestore
    reservations_ref = db.collection('reservations').where('nombre_cliente', '==', request.user.username).stream()
    citas_reservadas = [reservation.to_dict() for reservation in reservations_ref]

    if not citas_reservadas:
        mensaje = "No tienes citas reservadas."
    else:
        mensaje = None

    return render(request, 'Reserv/mis_citas.html', {'citas': citas_reservadas, 'mensaje': mensaje})