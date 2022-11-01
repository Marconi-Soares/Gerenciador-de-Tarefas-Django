from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TarefaBase(models.Model):
    titulo = models.CharField(max_length=55)
    completo = models.BooleanField(default=False)

    class Meta:
        abstract = True
        default_related_name = 'tarefa'
        ordering = ['-completo']

    def __str__(self):
        return self.titulo


class Tarefa(TarefaBase):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(TarefaBase.Meta):
        pass

    def completar(self):
        self.completo = True
        self.save()


class Grupo(models.Model):
    nome = models.CharField(max_length=55)
    usuarios = models.ManyToManyField(User)

    class Meta:
        default_related_name='grupo'


    def __str__(self):
        return self.nome


class SubTarefa(TarefaBase):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='subtarefas')
    completado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta(TarefaBase.Meta):
        default_related_name = 'subtarefa'
    
    def completar(self, usuario):
        self.completo = True
        self.completado_por = usuario

