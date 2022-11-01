from django import forms

from .models import Grupo, Tarefa, User

class TarefaModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['titulo'].widget.attrs.update({'placeholder': 'Título da tarefa...'})

    class Meta:
        model = Tarefa
        fields = ['titulo']


class GrupoModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['nome'].widget.attrs.update({'placeholder': 'Nome do grupo...'})

    class Meta:
        model = Grupo
        fields = ['nome']

class AddUsuarioForm(forms.Form):
    nome = forms.CharField(max_length=55)

    def clean_nome(self):
        nome = self.cleaned_data['nome']

        if User.objects.filter(username=nome).exists():
            return super().clean()
        
        else:
            raise forms.ValidationError('Usuario não existe')

    