from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
# Create your views here.

class Login(LoginView):
    template_name = 'auth_app/login.html'
    next_page = reverse_lazy('pagina-inicial')
    
class Logout(LogoutView):
    next_page = reverse_lazy('login')


class Registrar(FormView):
    form_class = UserCreationForm
    template_name = 'auth_app/registro.html'
    success_url = reverse_lazy('pagina-inicial')

    def form_valid(self, form):
        form.save()
        
        usuarioAuthenticado = self.get_usuarioAuthenticado()
        self.logar(usuarioAuthenticado)
        
        return super().form_valid(form)

    def get_usuarioAuthenticado(self):
        nome = self.request.POST.get('username')
        senha = self.request.POST['password1']

        usuario = authenticate(self.request, username=nome, password=senha)
        return usuario

    def logar(self, usuario):
        return login(self.request, usuario)