from django.urls import path 
from .views import *

urlpatterns = [ 
    path('', PaginaInicial.as_view(), name='pagina-inicial'),
    path('criar-tarefa/', CriarTarefa.as_view(), name='criar-tarefa'),
    path('criar-grupo', CriarGrupo.as_view(), name='criar-grupo'),

    path('grupo/<int:pk>', GrupoView.as_view(), name='grupo'),
    path('grupo/<int:grupo_id>/subtarefa/<int:pk>/completar/', 
    SubTarefaView.as_view(), name='completar-subtarefa'),
]
