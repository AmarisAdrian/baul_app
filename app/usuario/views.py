from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from sweetify.views import SweetifySuccessMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from app.config.message import Message
from django.shortcuts import redirect

class ListUsuario(LoginRequiredMixin,ListView):
    model = User
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'usuario/usuario.html'
    context_object_name = 'user'

class UpdateUsuario(LoginRequiredMixin,SweetifySuccessMixin,UpdateView):
    login_url = '/perfil/login/'
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'usuario/editar-usuario.html'
    success_url = reverse_lazy('usuario:usuario')
    form_class = UserChangeForm
    success_message = 'Usuario actualizado exitosamente'
    #LAS SIGUIENTES FUNCIONES  NO SON COMPLETAMENTE NECESARIAS SOLO ES PARA VALIDAR SI ESTA HACIENDO EL POST#
    def get_context_data(self, **kwargs):      
        context = super(UpdateUsuario, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        usuario = self.model.objects.get(id=pk)       
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET) 
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        usuario = self.model.objects.get(id=id)
        form = self.form_class(self.request.POST,instance=usuario)    
        try:
            if form.is_valid():
                sw = form.save(commit=False)
                sw.save()
                Message.SuccessMessage(self.request,'El usuario se ha actualizado exitosamente') 
                return HttpResponseRedirect(self.get_success_url())           
            else:
                Message.ErrorMessage(self.request,'Los datos ya existen.Por favor intente con nuevos datos')
                return redirect('usuario:usuario')
        except Exception as ex:
            Message.ErrorMessage(self.request,ex)
            return redirect('usuario:usuario')


