from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddUsuarioForm, TarefaModelForm, GrupoModelForm
from .models import *

class PaginaInicial(LoginRequiredMixin, ListView):
    model = Tarefa
    context_object_name = 'lista_de_tarefas'
    template_name = 'todo_list/paginaInicial.html'

    def get_context_data(self, **kwargs):
        pesquisa = self.request.GET.get('pesquisa') or None
        context = super().get_context_data(**kwargs)
        usuario = self.request.user 
        context['lista_de_tarefas'] = context['lista_de_tarefas'].filter(usuario=usuario)
        context['numero_de_tarefas_incompletas'] = context['lista_de_tarefas'].count()
        context['lista_de_grupos'] = usuario.grupo.all()

        if pesquisa:
            context['pesquisa'] = pesquisa
            context['lista_de_tarefas'] = context['lista_de_tarefas'].filter(titulo__icontains=pesquisa)

        return context


class CriarTarefa(LoginRequiredMixin, CreateView):
    form_class = TarefaModelForm
    template_name = 'forms/criarTarefa.html'
    success_url = reverse_lazy('pagina-inicial')

    def get_current_user(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.usuario = self.get_current_user()
        return super().form_valid(form)
    

class CriarGrupo(LoginRequiredMixin, CreateView):
    template_name = 'forms/criarGrupo.html'
    form_class = GrupoModelForm

    def get_success_url(self, pk):
        self.success_url = f'grupo/{pk}'
        return self.success_url


    def form_valid(self, form):
        usuario = self.request.user

        self.object = form.save()
        self.object.usuarios.add(usuario)

        return HttpResponseRedirect(self.get_success_url(self.object.id))


class GrupoView(LoginRequiredMixin, UpdateView):
    model = Grupo
    form_class = GrupoModelForm
    template_name = 'todo_list/grupo.html'
    context_object_name = 'grupo'

# VERBOS
    def get(self, request, *args: str, **kwargs):

        if self.is_membro():
            return super().get(request, *args, **kwargs)
        
        return redirect('pagina-inicial')

    def post(self, request, *args: str, **kwargs):
        if self.is_membro():

            titulo = request.POST.get('titulo')
            nome_de_usuario = request.POST.get('nome')

            if titulo:
                self.criar_subtarefa(titulo)
                return self.voltar_ao_grupo()  
            
            elif nome_de_usuario:
                grupo = self.get_object()
                form = AddUsuarioForm(self.request.POST)
            
                if form.is_valid():
                    usuario = User.objects.get(username=nome_de_usuario)
                    grupo.usuarios.add(usuario)
                    return self.voltar_ao_grupo()

                else: 
                    return render(self.request, 'todo_list/grupo.html', self.get_context_data(add_usuario_form=form))

            return self.voltar_ao_grupo()

        return redirect('pagina-inicial')

# VERIFICAÇÕES
    def is_membro(self):
        grupo = self.get_object()
        usuario = self.get_usuario() 
        return usuario.grupo.filter(pk=grupo.id).exists()


# PEGADORES
    def get_usuario(self):
        return self.request.user

    def get_context_data(self, **context):
        grupo = self.get_object()

        context['grupo'] = grupo
        
        context['lista_de_subtarefas'] = grupo.subtarefas.all().filter(completo=False)
        context['lista_de_subtarefas_completas'] = grupo.subtarefas.filter(completo=True)
        
        context['lista_de_usuarios'] = grupo.usuarios.all()
        context.setdefault('add_usuario_form', AddUsuarioForm())
        
        return context


# AÇÕES
    def criar_subtarefa(self, titulo):
        grupo = self.get_object()
        SubTarefa.objects.create(titulo=titulo, grupo=grupo)

    def voltar_ao_grupo(self):
        grupo = self.get_object()
        return redirect('grupo', pk=grupo.id)


class SubTarefaView(LoginRequiredMixin, UpdateView):
    model = SubTarefa
    template_name = ''

    def getUsuario(self):
        return self.request.user

    def get(self, request, *args: str, **kwargs):
        grupo = kwargs['grupo_id']
        
        if self.is_membro(grupo):
            return redirect('grupo', pk=grupo)
        
        return redirect('pagina-inicial')

    def is_membro(self, grupo):
        usuario = self.getUsuario() 
        return usuario.grupo.filter(pk=grupo).exists()
