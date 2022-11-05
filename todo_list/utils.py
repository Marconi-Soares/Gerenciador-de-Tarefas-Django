from django.shortcuts import redirect

class AbstractUtil:
    """
    Classe com métodos comuns a todas as views
    """

    #PEGADORES
    def get_usuario(self):
        """
        Retorna o usuário da request.
        """
        return self.request.user

    def get_acao(self):
        """
        Retorna o que foi passado como 'acao' nos kwargs.
        """
        acao = self.kwargs['acao']
        return acao

    #AÇÕES
    def perform_acao(self, acao):
        """
        Switch case que define o que deve ser feito com base na 'acao' recebida. Deve ser implementada.
        """
        pass

class TarefaUtil(AbstractUtil):
    """
    Classe para ser usada em views relacionadas aos models Tarefa e SubTarefa
    """

    #VALIDAÇÕES
    def is_dono_da_tarefa(self, tarefa=None):
        """
        Retorna se o usuário da request é criador da tarefa.
        """
        usuario = self.get_usuario()
        tarefa = tarefa or self.get_object()

        if tarefa.usuario == usuario:
            return True

        return False


class GrupoUtil(AbstractUtil):
    """
    Classe para ser usada em views relacionadas ao model Grupo
    """

    #PEGADORES
    def get_grupo_url(self, grupo=None):
        """
        Retorna a detailview do grupo.
        """
        grupo = grupo or self.get_object()
        
        return redirect('grupo', pk=grupo.id)
    
    #VERIFICAÇÕES
    def is_membro(self, grupo=None):
        """
        Retorna se o usuario da request está na lista de usuarios do grupo.
        """
        grupo = grupo or self.get_object()
        usuario = self.get_usuario() 

        return usuario in grupo.usuarios.all()


class TarefaGrupoUtil(TarefaUtil, GrupoUtil):
    """
    Junção entre a TarefaUtil e GrupoUtil
    """