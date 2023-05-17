from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
import string
import random


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) :
        return self.user.username
    
class Turma(models.Model):
    sala = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    codigo = models.CharField(max_length=7, unique=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.gerar_codigo_unico()
        return super().save(*args, **kwargs)

    def gerar_codigo_unico(self):
        caracteres = string.ascii_uppercase + string.digits
        codigo = ''.join(random.choice(caracteres) for _ in range(7))
        while Turma.objects.filter(codigo=codigo).exists():
            codigo = ''.join(random.choice(caracteres) for _ in range(7))
        return codigo
    
    def __str__(self) :
        return self.sala
    


class AlunoTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def join_turma(codigo, aluno):
        try:
            turma = Turma.objects.get(codigo=codigo)
        except Turma.DoesNotExist:
            return False
        
        AlunoTurma.objects.get_or_create(turma=turma, aluno=aluno)
        return True
    def __str__(self) -> str:
        return self.aluno.username

from django.utils import timezone

class Atividade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_entrega = models.DateField(blank=True,null=True)
    material= models.FileField(upload_to='media/', blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    entregue_com_atraso = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.concluida = False
    
        return super().save(*args, **kwargs)
    
    def get_atividade_pendente(self):
        return not self.concluida and self.data_entrega < timezone.now().date()

    def get_absolute_url(self):
        return reverse('detalhes_atividade', args=[str(self.id)])
    

    def get_absolute_url(self):
        return reverse('detalhes_atividade', args=[str(self.id)])
    
    def comentarios(self):
        return ComentarioAtividade.objects.filter(atividade=self)
class ComentarioAtividade(models.Model):
    comentario = models.TextField(default="")
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    autor = models.CharField(max_length=100)

    def __str__(self):
        return self.comentario




class RespostaAtividade(models.Model):
    APROVADO = 'A'
    REPROVADO = 'R'
    PENDENTE = 'P'
    APROVACAO_CHOICES = [
        (APROVADO, 'Aprovado'),
        (REPROVADO, 'Reprovado'),
        (PENDENTE, 'Pendente'),
    ]
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='media/', blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    aprovacao = models.CharField(max_length=1, choices=APROVACAO_CHOICES, default=PENDENTE,)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.atividade.concluida = True
            self.atividade.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.atividade.concluida = False
        self.atividade.save()
        return super().delete(*args, **kwargs)
