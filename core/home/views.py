from cmath import sin
from math import *

from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from groq import Groq
from .models import *
from .forms import *
key = "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"
import json
# Create your views here.


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def register_ngo(request):
    """
    Handles NGO registration.
    """
    if request.method == 'POST':
        form = NgoRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'NGO registered successfully!'}, status=201)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = NgoRegisterForm()
    return render(request, 'register_ngo.html',{'form':form})


def nog_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                ngos = ngo.objects.filter(username=user)
                if ngos is not None:
                    login(request, user)
                    return redirect('chatcreate')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'bot/login.html', {'form': form})
def llm(question, convoid):
    """
    Function to interact with the Groq API for generating responses about natural calamities.
    """
    prompt = f"""
    You are a natural calamity response assistant. Your task is to:
    - Provide accurate and concise information related to the user's question about natural calamities.
    - Craft your response based on verified data and include actionable advice when applicable.

    Context:
    - Conversation ID: {convoid}
    - User's Input: {question}

    Your Response Format:
    Response: [Provide a single accurate and concise response.]
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=key)

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            temperature=0.7,
            top_p=1,
        )

        response_text = completion.choices[0].message.content
        print("Groq API Raw Response Content:", response_text)  # Debugging output

        # Extract the response content
        response = response_text.split("Response:")[1].strip() if "Response:" in response_text else "Sorry, I couldn't process your question."
        return response

    except Exception as e:
        print(f"Error with Groq API: {e}")
        return "Sorry, there was an issue processing your question. Please try again."

def chat(request, convoid):
    convo = get_object_or_404(conversation, id=convoid)

    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        data = json.loads(request.body)
        user_response = data.get('response')

        if user_response:
            # Save user's message
            questions.objects.create(convo=convo, question=user_response, user='user')

            # Generate AI response
            ai_response = llm(user_response, convoid)

            # Save AI response
            questions.objects.create(convo=convo, question=ai_response, user='ai')

            return JsonResponse({"response": ai_response})

        return JsonResponse({"error": "Invalid response"}, status=400)

    # For GET requests, render the chat page with existing messages
    questions_list = questions.objects.filter(convo=convo)

    # Initialize conversation if no questions exist
    if not questions_list.exists():
        default_message = "Welcome! Ask me anything about natural calamities, and I'll provide accurate information."
        questions.objects.create(convo=convo, question=default_message, user='ai')
        questions_list = questions.objects.filter(convo=convo)

    return render(request, 'bot.html', {
        'convo': convo,
        'questions': questions_list,
    })
def chatcreate(request):
    # Check if a conversation between these users exists
    convo, created = conversation.objects.get_or_create(
        user=request.user  # Assuming a "user" ForeignKey in the conversation model
    )
    return redirect('chat', convo.id)
@login_required
def public_chat(request):
    messages = ChatMessage.objects.all().order_by('timestamp')

    # Adjust the query based on your model fields
    ngo_users = ngo.objects.values_list('username', flat=True)  # Replace 'user__username' with 'username'

    return render(request, 'chat.html', {
        'messages': messages,
        'ngo_users': list(ngo_users),  # Pass the list of usernames
        'current_user': request.user.username,  # Pass the logged-in user's username
    })
@login_required
def send_message(request):
    if request.method == "POST":
        user = request.user
        try:
            ngo_user = ngo.objects.get(username=user, verified=True)
        except ngo.DoesNotExist:
            return JsonResponse({'error': 'You are not authorized to send messages.'}, status=403)

        message_content = request.POST.get('message', '').strip()
        if not message_content:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        message = ChatMessage.objects.create(user=user, message=message_content)
        return JsonResponse({'username': user.username, 'message': message.message})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def get_messages(request):
    messages = ChatMessage.objects.order_by('-timestamp')[:50][::-1]
    response_data = [
        {'username': msg.user.username, 'message': msg.message, 'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
        for msg in messages
    ]
    return JsonResponse({'messages': response_data})

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_of_earth_km = 6371  # Radius of Earth in kilometers
    return radius_of_earth_km * c

def nearby_shelters(request):
    user_lat = request.GET.get('latitude')
    user_lon = request.GET.get('longitude')

    if not user_lat or not user_lon:
        return JsonResponse({'error': 'Latitude and Longitude are required.'}, status=400)

    try:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
    except ValueError:
        return JsonResponse({'error': 'Invalid latitude or longitude values.'}, status=400)

    shelters = shelters.objects.all()
    shelter_data = []

    for shelter in shelters:
        distance = calculate_distance(user_lat, user_lon, float(shelter.latitude), float(shelter.longitude))
        shelter_data.append({
            'name': shelter.name,
            'address': shelter.address,
            'lat': shelter.latitude,
            'lng': shelter.longitude,
            'distance': round(distance, 2)
        })

    shelter_data.sort(key=lambda x: x['distance'])  # Sort shelters by distance

    return JsonResponse(shelter_data, safe=False)

def distress_view(request):
    dis = distress.objects.all()
    return render(request,'distress.html',{'dis':dis})

def disdel(request, did):
    d = get_object_or_404(distress,id=did)
    d.delete()
    print("deleted")
    return redirect('distress')
def shelter_view(request):
    sh = shelters.objects.all()
    return render(request,'shelter.html',{'shelters':sh})
def home(request):
    return render(request,'home.html')
def earthquake(request):
    return render(request,'earthquake.html')
def tsunami(request):
    return render(request,'tsunami.html')
def floods(request):
    return render(request,'floods.html')

@csrf_exempt
@login_required
def submit_distress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_distress = distress.objects.create(
                user=request.user,
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Distress signal recorded successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)


client = Groq(api_key=key)


def validate_alert_with_groq(latitude, longitude, calamity_type):
    try:
        # Construct the prompt for Groq
        prompt = f"""Given the following information about a potential disaster alert:
        Location: Latitude {latitude}, Longitude {longitude}
        Type of Calamity: {calamity_type}

        Based on this information, analyze if this could be a genuine alert. Consider:
        1. Is this location prone to {calamity_type}?
        2. Are there any known active disasters in this region?
        3. Is this a reasonable alert given the geographical context?

        Respond with only 'yes' or 'no'.
        """

        # Make API call to Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",  # or your preferred model
            temperature=0.1,
            max_tokens=1,
        )

        # Get the response
        response = chat_completion.choices[0].message.content.strip().lower()
        return response == 'yes'

    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        return False  # Default to False in case of API errors

@csrf_exempt
@login_required
def submit_distress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            concern_type = data.get('concern_type')

            # Validate alert with Groq API
            is_valid = validate_alert_with_groq(latitude, longitude, concern_type)

            if is_valid:
                # Create distress object only if validated
                new_distress = distress.objects.create(
                    user=request.user,
                    latitude=latitude,
                    longitude=longitude
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Distress signal validated and recorded successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Alert validation failed. Please verify your information.'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def distress_list(request):
    dis = distress.objects.all()
    return render(request, 'distress.html', {'dis': dis})