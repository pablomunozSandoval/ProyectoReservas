from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from .models import Doctor, Appointment

def create_default_user():
    if not User.objects.filter(username='jhon').exists():
        User.objects.create_user(username='jhon', password='123456')

def login_view(request):
    create_default_user()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Reserv/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'Reserv/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'Reserv/register.html', {'error': 'El nombre de usuario ya está registrado.'})
        
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'Reserv/register.html')



def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Usar los datos fijos definidos en la variable DOCTORES
    return render(request, 'Reserv/home.html', {'doctors': DOCTORES})


def citas_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'Reserv/citas.html', {'appointments': appointments})


def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Datos fijos de los médicos
DOCTORES = [
    {
        "id": 1,
        "name": "Dr. John Smith",
        "especialidad": "Cardiología",
        "descripcion": "Especialista en enfermedades del corazón con más de 15 años de experiencia.",
        "horarios": "Lunes a Viernes, 9:00 AM - 3:00 PM",
        "disponible": True,
    },
    
    {
        "id": 2,
        "name": "Dra. Emily Carter",
        "especialidad": "Pediatría",
        "descripcion": "Atención especializada para niños y adolescentes.",
        "horarios": "Lunes a Viernes, 10:00 AM - 5:00 PM",
        "disponible": True,
    },
    {
        "id": 3,
        "name": "Dr. Carlos Martínez",
        "especialidad": "Neurología",
        "descripcion": "Experto en trastornos del sistema nervioso.",
        "horarios": "Martes y Jueves, 8:00 AM - 1:00 PM",
        "disponible": False,
    },
    {
        "id": 4,
        "name": "Dra. Ana López",
        "especialidad": "Dermatología",
        "descripcion": "Especialista en problemas de la piel.",
        "horarios": "Miércoles y Viernes, 9:00 AM - 2:00 PM",
        "disponible": True,
    },
    {
        "id": 5,
        "name": "Dr. Michael Brown",
        "especialidad": "Ortopedia",
        "descripcion": "Tratamiento de lesiones musculoesqueléticas.",
        "horarios": "Lunes a Jueves, 11:00 AM - 4:00 PM",
        "disponible": True,
    },
]

# Lista de reservas para controlar las reservas
reservas = [None] * 5  # Un máximo de 5 reservas

def reserve_view(request, doctor_id):
    # Buscar el doctor por id
    doctor = next((d for d in DOCTORES if d["id"] == doctor_id), None)
    
    if doctor is None:
        return redirect('home')  # Si no se encuentra el doctor, redirigir a home

    # Verificar si ya se ha hecho una reserva para este doctor
    if reservas[doctor_id - 1] is not None:
        return render(request, 'reserv/error.html', {'message': 'ya tiene una reserva con este doctor .'})

    # Si el doctor está disponible y no tiene reserva
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre')
        if nombre_cliente:
            # Realizar la reserva
            reservas[doctor_id - 1] = nombre_cliente
            doctor['disponible'] = False  # Marcar al doctor como no disponible
            return render(request, 'reserv/exito.html', {'doctor': doctor, 'nombre_cliente': nombre_cliente})
        else:
            return render(request, 'reserv/error.html', {'message': 'Por favor ingrese su nombre para realizar la reserva.'})

    return render(request, 'reserv/reserva.html', {'doctor': doctor})

def mis_citas(request):
    # Filtrar las citas reservadas por el usuario
    citas_reservadas = []
    
    # Iteramos sobre las reservas y los doctores para encontrar las citas que el usuario ha hecho
    for idx, reserva in enumerate(reservas):
        if reserva is not None:  # Si hay una reserva para ese doctor
            doctor = DOCTORES[idx]  # Obtener el doctor correspondiente
            citas_reservadas.append({
                "doctor": doctor,
                "nombre_cliente": reserva
            })

    if not citas_reservadas:
        mensaje = "No tienes citas reservadas."
    else:
        mensaje = None

    return render(request, 'reserv/mis_citas.html', {'citas': citas_reservadas, 'mensaje': mensaje})