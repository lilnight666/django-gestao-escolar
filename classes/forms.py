from django import forms
from .models import RespostaAtividade

class RespostaForm(forms.ModelForm):
    class Meta:
        model = RespostaAtividade
        fields = ['arquivo']
        
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
        }

        required = {
            'aprovacao': False
        }



class AprovacaoForm(forms.ModelForm):
    class Meta:
        model = RespostaAtividade
        fields = ('aprovacao',)
        labels = {'aprovacao': 'Avaliar '}
        widgets = {
            'aprovacao': forms.RadioSelect(choices=RespostaAtividade.APROVACAO_CHOICES)
        }
     