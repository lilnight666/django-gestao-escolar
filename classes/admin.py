from django.contrib import admin
from .models import Atividade,RespostaAtividade,Turma,AlunoTurma

admin.site.register(Atividade)
admin.site.register(RespostaAtividade)
admin.site.register(Turma)
admin.site.register(AlunoTurma)

