from .models import Group, Song
from django.forms import ModelForm, TextInput, CharField
from django import forms

class SongForm(forms.Form):
    title = forms.CharField(label="Название песни", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))
    group = forms.CharField(label="Группа", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))
    effects = forms.CharField(label="Эффекты", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))
    guitar_model = forms.CharField(label="Модель гитары", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))
    amplifier = forms.CharField(label="Усилитель", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))
    description = forms.CharField(label="Описание", required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '3',
    }))


class GptSongForm(forms.Form):
    title = forms.CharField(label='Название песни', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))
    group = forms.CharField(label='Группа', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'rows': '3',
    }))

class FileSongForm(forms.Form):
    audio_file = forms.FileField(label="Аудиофайл песни", required=True)