
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from classes.forms import  AprovacaoForm
from .models import Atividade, ComentarioAtividade, RespostaAtividade ,Turma,AlunoTurma,Professor
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import FileResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from datetime import datetime
def login_user(request):
    return render(request, 'login.html')
def submit_login(request):
    if request.POST:
        username= request.POST.get('username')
        password= request.POST.get('password')
        usuario= authenticate(username=username, password=password )
        if usuario is not None:
            login(request,usuario)
        else:
            messages.error(request, "usuario ou senha invalidos")
            return redirect('/turmas')
            
    return redirect('/turmas')



def cadastrar(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        is_prof = request.POST.get("is_prof", False)

        hashed_password = make_password(password)
        u=User.objects.create(username=username, password=hashed_password, email=email)
        u.save()
        login(request,u)

        if is_prof:
          Professor.objects.create(user=u)
        return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')


def nova_turma(request):
    if request.method=="GET":
        return render(request, 'nova_turma.html')
@login_required(login_url='/accounts/login')
def join_turma(request):
    if request.method == 'POST':
        codigo_turma = request.POST['codigo_turma']
        aluno = request.user

        if AlunoTurma.join_turma(codigo_turma, aluno):
             messages.success(request, "Você foi adicionado à turma com sucesso.'")
        else:
            mensagem = 'O código da turma é inválido. Tente novamente.'
        
        return redirect("/turmas",)

    return redirect('/turmas')




@login_required(login_url='/accounts/login')
def turmas(request):
    professor = Professor.objects.filter(user=request.user).first()
    if professor:
        turma = Turma.objects.filter(professor=professor)
        
    else:
        turma = Turma.objects.filter(alunoturma__aluno=request.user)
    return render(request, 'turmas.html', {'turma': turma})



@login_required(login_url='/accounts/login')
def crir_turma(request):
    if request.method== "GET":
        return render(request, "criar_turma.html")
    else:
        sala=request.POST.get("sala")
        descricao=request.POST.get("descricao")
        professor = Professor.objects.get(user=request.user)
        Turma.objects.create(sala=sala,descricao=descricao,professor=professor)

        return redirect("/turmas")


@login_required(login_url='/accounts/login')
def criar_atividade(request):
    turmas = Turma.objects.filter(professor=request.user.professor)
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_entrega = request.POST.get('data_entrega')
        material = request.FILES.get('material') 
        turma_id = request.POST.get("turma")
        professor = request.user.professor
        turma = Turma.objects.get(id=turma_id)
        atividade = Atividade(titulo=titulo, descricao=descricao, data_entrega=data_entrega, professor=professor, material=material, turma=turma)
        atividade.save()
        return redirect('visualizar_atividades', turma_id=turma_id)
    else:
        return render(request, 'criar_atividade.html', {'turmas': turmas})

def editar_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_entrega = request.POST.get('data_entrega')
        material = request.FILES.get('material')
        professor = request.user.professor
        atividade.titulo = titulo
        atividade.descricao = descricao
        atividade.data_entrega = data_entrega
        atividade.material = material
        atividade.professor = professor
        atividade.save()
        messages.success(request, 'Atividade editada com sucesso.')
        return redirect('visualizar_atividades', turma_id=atividade.turma.pk)
    else:
        context = {'atividade': atividade}
        return render(request, 'editar_atividade.html', context=context)

def deletar_atividade(request, pk):
    try:
        atividade = Atividade.objects.get(pk=pk, professor=request.user.professor)
        turma = atividade.turma
    except Atividade.DoesNotExist:
        messages.error(request, 'Atividade não encontrada ou você não tem permissão para excluí-la.')
        return redirect("detalhes")
    turma_id = turma.id
    atividade.delete()
    messages.success(request, 'Atividade excluída com sucesso.')
    return redirect("visualizar_atividades", turma_id=turma_id)


def visualizar_atividades(request, turma_id,):
    atividades = Atividade.objects.filter(turma_id=turma_id,)

    return render(request, 'visualizar_atividades.html', {'atividades': atividades})




def atividades_pendentes(request, ):
    usuario= request.user
    atividades = Atividade.objects.filter(turma_id=turma_id).exclude(respostaatividade__aluno=usuario).filter(data_entrega__lt=timezone.now())

    return render(request, 'atividades_pendentes.html', {'atividades': atividades})


def detalhes_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    if atividade.material:
        atividade.material_url = atividade.material.url

   

    
    return render(request, 'detalhes_atividade.html', {'atividade': atividade})

    


def add_comentario(request, pk):
    atividade = Atividade.objects.get(pk=pk)
    comentario_texto = request.POST['comentario']
    comentario_autor = request.user.username
    comentario = ComentarioAtividade(comentario=comentario_texto, atividade=atividade, autor=comentario_autor)
    comentario.save()
    return redirect('detalhes_atividade', pk=atividade.id)


def excluir_comentario(request, pk):
    comentario = get_object_or_404(ComentarioAtividade, pk=pk)
    atividade = comentario.atividade
    if request.user.username == comentario.autor or request.user.professor:
        comentario.delete()
        return redirect('detalhes_atividade', pk=atividade.pk)
    else:
        return redirect('detalhes_atividade', pk=atividade.pk)



@login_required(login_url='/login/')
def pendente(request):
    usuario = request.user
    atividades = Atividade.objects.filter(turma__alunoturma__aluno=usuario).exclude(respostaatividade__aluno=usuario).filter(data_entrega__lt=timezone.now())
    context = {'atividades': atividades}
    return render(request, 'pendentes.html', context)


def enviar_atividade(request,pk):
        if request.method == 'POST':
           if request.method == 'POST':
              atividade = Atividade.objects.get(pk=pk)
              resposta = RespostaAtividade()
              resposta.aluno = request.user
              resposta.atividade = atividade
              resposta.arquivo = request.FILES['resposta']
              resposta.save()
        return render(request, 'detalhes_atividade.html', {'atividade': atividade})

def listar_respostas(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    respostas = RespostaAtividade.objects.filter(atividade=atividade)
    return render(request, 'listar_respostas.html', {'atividade': atividade, 'respostas': respostas})


def aprovar_resposta(request, pk):
    resposta = get_object_or_404(RespostaAtividade, pk=pk)
    if request.method == 'POST':
        form = AprovacaoForm(request.POST, instance=resposta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resposta avaliada com sucesso.')
            return redirect('listar_respostas', pk=resposta.atividade.pk)
    else:
        form = AprovacaoForm(instance=resposta)
    return render(request, 'aprovar_resposta.html', {'form': form, 'resposta': resposta})


@login_required(login_url='/login/')
def ver_resposta(request, pk):
    resposta = get_object_or_404(RespostaAtividade, pk=pk)
    response = FileResponse(resposta.arquivo)
    response['Content-Disposition'] = f'attachment; filename="{resposta.arquivo.name}"'
    return response


