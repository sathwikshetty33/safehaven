from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
                return redirect('chatcreate',user.id)
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
def chatcreate(request, userid):
    target_user = get_object_or_404(User, id=userid)
    # Check if a conversation between these users exists
    convo, created = conversation.objects.get_or_create(
        user=request.user  # Assuming a "user" ForeignKey in the conversation model
    )
    return redirect('chat', convo.id)