from django.forms import modelformset_factory
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from ..models import Encuesta, Opcion
from ..forms import EncuestaForm



class ListaPreguntas(ListView):
    model = Encuesta
    template_name = 'list.html'


class NuevaEncuesta(CreateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'modal_generic.html'
    success_url = reverse_lazy('home')
    url_redirect = success_url

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
        context = super(NuevaEncuesta, self).get_context_data(**kwargs)
        OpcionFormSet = modelformset_factory(
            Opcion, form=OpcionForm, max_num=4, min_num=1, extra=3)
        formset = OpcionFormSet(queryset=Opcion.objects.none())
        context = super().get_context_data(**kwargs)
        context['formset'] = formset
        context['form_name'] = 'form_encuesta_new'
        context['modal_title'] = 'Crear Nueva Encuesta'
        context['action'] = 'add'
        return context
        


def modificaEncuesta(request, pk):
    context = {}
    OpcionFormset = modelformset_factory(
        Opcion, form=OpcionForm, max_num=4, min_num=1, extra=3)
    encuesta = Encuesta.objects.get(id=pk)
    opciones = Opcion.objects.filter(encuesta=encuesta.id)
    form = EncuestaForm(instance=encuesta)
    formset = OpcionFormset(queryset=opciones)
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        formset = OpcionFormset(request.POST, queryset=opciones)
        if form.is_valid():
            if formset.is_valid():
                form.save()
                opcs = formset.save(commit=False)
                for op in opcs:
                    op.encuesta_id = encuesta.id
                    op.save()
                return redirect('/')
    context['formset'] = formset
    context['form'] = form
    return render(request, 'editar.html', context)



class BorraEncuesta(DeleteView):
    model = Encuesta
    template_name = 'borrar.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pregunta = Encuesta.objects.get(id=self.object.id)
        context['pregunta'] = pregunta
        return context