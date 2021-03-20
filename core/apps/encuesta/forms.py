from typing import Text
from django import forms
from django.db.models import fields
from django.forms import (ModelForm, inlineformset_factory,
                          modelformset_factory, widgets)
from django.forms.formsets import formset_factory

from .models import Encuesta, Opcion, Respuesta, Tag


class EncuestaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['pregunta'].widget.attrs['placeholder'] = 'Ingrese pregunta'
        self.fields['pregunta'].widget.attrs['autofocus'] = True
            
    tag = forms.ModelChoiceField(required=False,
                                 queryset=Tag.objects.filter().order_by('nombre'),
                                 widget=forms.Select(attrs={'class': 'form-control', },
                                                     ))
    
    class Meta:
        model = Encuesta
        fields = ['pregunta', 'vence', 'tag']
        

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['nombre', ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': "form-control",
                                             'placeholder': "Ingrese nombre...",
                                             'autocomplete': "off"}),
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

        

class OpcionForm(ModelForm):
    titulo = forms.CharField(required=False,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': "Ingrese opción...",
                                        'autocomplete': "off"},
                             ))

    class Meta:
        model = Opcion
        fields = ['titulo', ]
        labels = {'titulo': 'Opcion', }


# class RespuestaForm(ModelForm):
#     # opciones = forms.ModelChoiceField(required=False,
#     #                                   widget=forms.Select(attrs={'class': 'form-control', 'placeholder': "Ingrese tag...",
#     #                                                              'autocomplete': "off", },
#     #                                                       ))

#     class Meta:
#         model = Respuesta
#         fields = ['opcion']
#         widgets = {
#             'opcion': forms.Select(attrs={'class': 'form-control border-left-primary',
#                                           'placeholder': "Ingrese tag...",
#                                           'autocomplete': "off", }),
#         }
