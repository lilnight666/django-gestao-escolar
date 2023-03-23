"""cursos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from classes import views 
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('cadastro/', views.cadastrar, name="cadastrar"),
    path('',RedirectView.as_view(url='turmas/')),
    path('turmas/', views.turmas, name='turmas'),
    path('turma/join/',views.join_turma, name='join_turma'),
    path('criar_turma/',views.crir_turma, name="criar_turma"),
    path('atividades/<int:turma_id>/visualizar/', views.visualizar_atividades, name='visualizar_atividades'),
    path('atividades/criar/', views.criar_atividade, name='criar_atividade'),
    path('editar_atividade',views.editar_atividade,name="editar_atvidade"),
    path('deletar_atividade/<int:pk>',views.deletar_atividade,name="deletar_atividade"),
    path('atividades/<int:atividade_id>/enviar/', views.enviar_resposta, name='enviar_resposta'),
    path('enviar_resposta/<int:pk>', views.enviar_resposta, name='enviar_resposta'),
    path('listar_respostas/<int:pk>/', views.listar_respostas, name='listar_respostas'),
    path('aprovar_resposta/<int:pk>/', views.aprovar_resposta, name='aprovar_resposta'),
    path('accounts/login/', views.login_user, name='login'),
    path('download_resposta/<int:pk>/', views.download_resposta, name='download_resposta'),
    path('accounts/login/submit', views.submit_login),
    path('logout/', views.logout_user, name='logout'),
   
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    
