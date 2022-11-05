from django.urls import path 
from .views import *

urlpatterns = [ 
    path('', PaginaInicial.as_view(), name='pagina-inicial'),
    path('criar-tarefa/', CriarTarefa.as_view(), name='criar-tarefa'),
    path('criar-grupo', CriarGrupo.as_view(), name='criar-grupo'),

    path('tarefa/<int:pk>/actions/<str:acao>', TarefaActions.as_view(), name='tarefa-actions'),

    path('grupo/<int:pk>/', GrupoView.as_view(), name='grupo'),

    path('grupo/<int:pk>/actions/<str:acao>', GrupoActions.as_view(), name='grupo-actions'),
    path('grupo/<int:grupo>/subtarefa/<int:pk>/actions/<str:acao>', SubTarefaActions.as_view(), name='subtarefa-actions')
]
