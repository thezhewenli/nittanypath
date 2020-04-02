from django.shortcuts import render

def landing(request):
  logedinusername = 'User1'

  args = {'username': logedinusername}
  return render(request, 'registrar/landing.html', args)