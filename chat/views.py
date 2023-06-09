from django.http import JsonResponse
from django.shortcuts import render
from .models import Message, Chat
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers

# Create your views here.
@login_required(login_url='/login/')
def index(request):
  """_summary_

  Args:
      request (_type_): _description_

  Returns:
      _type_: _description_
  """
  if request.method == 'POST':
    print('Received data ' + request.POST['textmessage'])
    myChat = Chat.objects.get(id=1)
    new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
    serialized_message = serializers.serialize('json', [new_message])
    return JsonResponse(serialized_message[1:-1], safe=False)
  chatMessages = Message.objects.filter(chat__id=1)
  return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
  redirect = request.GET.get('next')
  if request.method == 'POST':
    user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
    if user:
      login(request, user)
      return HttpResponseRedirect(request.POST.get('redirect'))
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
  return render(request, 'auth/login.html', {'redirect': redirect})


def register_view(request):
  redirect = request.GET.get('next')
  if request.method == 'POST':
    user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
    if user:
      return render(request, 'register/register.html', {'userExists': True})
    else:
      user = User.objects.create_user(username='john', email='jlennon@beatles.com', password='glass onion')
      return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
  return render(request, 'auth/register.html', {'redirect': redirect})

# TODO 
# - An Telegram, whatsapp, Messenger orientieren
# - Text rot anzeigen bei Fehler
# - Text erst grau, nach erfolgreichen Request Text schwarz (oder ein Haken, dann zwei Haken, wie bei whatsapp)
# - Login Button deaktiviert, wenn leer
# - Ladeanimation
# - App responsive 
# - Dokumentation
