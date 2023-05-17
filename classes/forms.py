from django import forms
from .models import RespostaAtividade
from django import forms
from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    def get_context(self, name, value, attrs):
        attrs.pop('required', None)
        return super().get_context(name, value, attrs)







class AprovacaoForm(forms.ModelForm):
    class Meta:
        model = RespostaAtividade
        fields = ('aprovacao',)
        labels = {'aprovacao': 'Avaliar '}
        widgets = {
            'aprovacao': forms.RadioSelect(choices=RespostaAtividade.APROVACAO_CHOICES)
        }
     