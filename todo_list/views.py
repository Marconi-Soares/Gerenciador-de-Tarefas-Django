from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddUsuarioForm, TarefaModelForm, GrupoModelForm
from .models import *
from .utils import *

class PaginaInicial(LoginRequiredMixin, ListView, TarefaUtil):
    """
    Página com acesso aos grupos e as tarefas.
    """
    model = Tarefa
    context_object_name = 'lista_de_tarefas'
    template_name = 'todo_list/paginaInicial.html'

    #PEGADORES
    def get_context_data(self, **kwargs):
        usuario = self.get_usuario()
        tarefas_do_usuario = Tarefa.objects.filter(usuario=usuario)

        context = {
            'lista_de_tarefas': tarefas_do_usuario.order_by('completo'),
            'numero_de_tarefas_incompletas': tarefas_do_usuario.filter(completo=False).count(),
            'lista_de_grupos': usuario.grupo.all()
        }
       
        pesquisa = self.request.GET.get('pesquisa') or None
        if pesquisa is not None:
            context['pesquisa'] = pesquisa
            context['lista_de_tarefas'] = tarefas_do_usuario.filter(titulo__icontains=pesquisa)

        return context


class CriarTarefa(LoginRequiredMixin, CreateView, TarefaUtil):
    """
    View responsável por criar novas tarefas
    """
    form_class = TarefaModelForm
    template_name = 'forms/criarTarefa.html'
    success_url = reverse_lazy('pagina-inicial')

    #AÇÕES
    def form_valid(self, form):
        form.instance.usuario = self.get_usuario()
        return super().form_valid(form)
    

class TarefaActions(LoginRequiredMixin, UpdateView, TarefaUtil):
    """
    Ações relacionadas as tarefas
    """
    model = Tarefa 
    fields = [] 

    #VERBOS
    def get(self, request, *args: str, **kwargs):
        return redirect('pagina-inicial')

    def post(self, request, *args: str, **kwargs):
        if self.is_dono_da_tarefa():
            acao = self.get_acao()
            self.perform_acao(acao)

        return redirect('pagina-inicial')

    #AÇÕES
    def perform_acao(self, acao):
        tarefa = self.get_object()

        if acao == 'completar':
            tarefa.completar()

        elif acao == 'apagar':
            tarefa.delete()


class CriarGrupo(LoginRequiredMixin, CreateView, GrupoUtil):
    """
    View responsável por criar novos grupos, adicionar o usuário da request neste e redirecioná-lo para uma detailview do grupo criado.
    """
    template_name = 'forms/criarGrupo.html'
    form_class = GrupoModelForm

    #AÇÕES
    def form_valid(self, form):
        usuario = self.get_usuario()

        grupo = form.save()
        grupo.usuarios.add(usuario)

        return self.get_grupo_url(grupo)


class GrupoView(LoginRequiredMixin, UpdateView, GrupoUtil):
    """
    Uma view que permite acesso as subtarefas e os usuários de um grupo.
    """
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
        if not self.is_membro():
            return self.get_grupo_url()
        
        nome_de_usuario = request.POST.get('nome')
        form = AddUsuarioForm(self.request.POST)
    
        if form.is_valid():
            self.add_usuario(nome_de_usuario)
            return self.get_grupo_url()

        else: 
            return render(self.request, 'todo_list/grupo.html', self.get_context_data(add_usuario_form=form))


#PEGADORES
    def get_context_data(self, **context):
        grupo = self.get_object()

        context['grupo'] = grupo
        context['lista_de_subtarefas'] = grupo.subtarefas.all().order_by('completo')
        context['lista_de_usuarios'] = grupo.usuarios.all()
        context.setdefault('add_usuario_form', AddUsuarioForm())
        
        return context


# AÇÕES
    def add_usuario(self, nome_de_usuario):
        grupo = self.get_object()
        usuario = User.objects.get(username=nome_de_usuario)
        grupo.usuarios.add(usuario)


class GrupoActions(LoginRequiredMixin, UpdateView, GrupoUtil):
    """
    Ações relacionadas a um grupo.
    """
    model = Grupo
    fields = []

    #VERBOS
    def get(self, request, *args: str, **kwargs):
        if self.is_membro():
            return self.get_grupo_url()
    
        return redirect('pagina-inicial')

    def post(self, request, *args: str, **kwargs):
        acao = self.get_acao()

        if self.is_membro():
            self.perform_acao(acao)
            return self.get_grupo_url()

        return redirect('pagina-inicial')

    #AÇÕES
    def perform_acao(self, acao):
        if acao == 'criar-subtarefa':
            titulo = self.request.POST.get('titulo')
            self.criar_subtarefa(titulo=titulo)

        elif acao == 'sair-do-grupo':
            self.sair_do_grupo()
            return redirect('pagina-inicial')

    def criar_subtarefa(self, titulo):
        """
        Cria uma nova subtarefa
        """
        grupo = self.get_object()
        SubTarefa.objects.create(titulo=titulo, grupo=grupo)

    def sair_do_grupo(self):
        """
        Remove o usuário da request do grupo.
        """
        grupo = self.get_object()
        usuario = self.get_usuario()

        grupo.remover(usuario)

class SubTarefaActions(LoginRequiredMixin, UpdateView, TarefaGrupoUtil):
    """
    Ações relacionadas a subtarefas.
    """
    model = SubTarefa
    fields = []

    #VERBOS
    def get(self, request, *args, **kwargs):
        grupo = self.get_object().grupo
        return self.get_grupo_url(grupo)

    def post(self, request, *args, **kwargs):
        acao = self.get_acao()
        grupo = self.get_object().grupo

        if self.is_membro(grupo):
            self.perform_acao(acao)
        
        return self.get_grupo_url(grupo)

    #AÇÕES
    def perform_acao(self, acao):
        subtarefa = self.get_object()
        usuario = self.get_usuario()

        if acao == 'completar':
            subtarefa.completar(usuario)
        
        elif acao == 'apagar':
            subtarefa.delete()
