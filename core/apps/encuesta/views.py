from django.db.models.aggregates import Count
from django.forms import modelformset_factory
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import EncuestaForm, OpcionForm, RespuestaForm, TagForm
from .models import Encuesta, Opcion, Respuesta, Tag





def nuevaRespuesta(request, pk):
    context = {}
    encuesta = Encuesta.objects.get(id=pk)
    opciones = Opcion.objects.filter(encuesta=encuesta.id)
    form = RespuestaForm()
    form.fields['opcion'].queryset = opciones
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context['encuesta'] = encuesta
    context['opciones'] = opciones
    context['form'] = form
    return render(request, 'responder.html', context)


class ResultadoEncuesta(DetailView):
    model = Encuesta
    template_name = 'resultados.html'

    def get_context_data(self, **kwargs):
        context = super(ResultadoEncuesta, self).get_context_data(**kwargs)
        encuesta = kwargs['object']
        opciones = Opcion.objects.filter(encuesta=encuesta.id)
        respuestas = Opcion.objects.filter(
            encuesta_id=encuesta.id).order_by('titulo').annotate(resultado=Count('respuesta'))
        total = Respuesta.objects.filter(
            opcion__encuesta_id=encuesta.id).count()
        context['encuesta'] = encuesta
        context['opciones'] = opciones
        context['respuestas'] = respuestas
        context['total'] = total
        return context




class ListaTag(ListView):
    model = Tag
    template_name = 'tags_listado.html'

    
class NuevoTag(CreateView):
    model = Tag
    template_name = 'modal_generic.html'
    form_class = TagForm
    success_url = reverse_lazy('lista-tag')
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super(NuevoTag, self).get_context_data(**kwargs)
        form = TagForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        context['form_name'] = 'form_tag_new'
        context['modal_title'] = 'Crear Nuevo Tag'
        context['action'] = 'add'
        return context
    


class BorraTag(DeleteView):
    model = Tag
    template_name = 'tags_borrar.html'
    success_url = '/tag/listado/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(id=self.object.id)
        context['tag'] = tag
        return context


class ListaReporte(ListView):
    model = Encuesta
    template_name = 'reporte_listado.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaReporte, self).get_context_data(**kwargs)
        usuarios = User.objects.all().order_by('username')
        tags = Tag.objects.all().order_by('nombre')
        if self.request.method == 'GET':
            preguntas = ""
            try:
                usuario = int(self.request.GET.get('userSel'))
                tag = int(self.request.GET.get('tagSel'))
                if usuario > 0 and tag > 0:
                    preguntas = Encuesta.objects.filter(
                        usuario=usuario, tag=tag).order_by('vence')
                elif usuario > 0 and tag == 0:
                    preguntas = Encuesta.objects.filter(
                        usuario=usuario).order_by('vence')
                elif usuario == 0 and tag > 0:
                    preguntas = Encuesta.objects.filter(
                        tag=tag).order_by('vence')
                else:
                    preguntas = Encuesta.objects.all().order_by('vence')
            except Exception:
                preguntas = Encuesta.objects.all().order_by('vence')
        context['usuarios'] = usuarios
        context['tags'] = tags
        context['preguntas'] = preguntas
        return context
