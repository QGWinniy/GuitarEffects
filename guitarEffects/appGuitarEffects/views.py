from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Song, Group
from .forms import SongForm, GptSongForm, FileSongForm
import openai
from .gpt import generate_song_data, recognize_song_from_file
from django.core.files.storage import default_storage
from threading import Thread

def form_default(request):
    song_form = SongForm(request.POST)
    if song_form.is_valid():
        cd = song_form.cleaned_data
        group_name = cd['group'].strip()
        group = Group.objects.get_or_create(name=group_name)[0] if group_name else None

        Song.objects.create(
            title=cd['title'],
            group=group,
            effects=cd['effects'],
            guitar_model=cd['guitar_model'],
            amplifier=cd['amplifier'],
            description=cd['description'],
        )
        return redirect('/')
    
def form_gpt(request):
    gpt_form = GptSongForm(request.POST)
    if gpt_form.is_valid():
        cd = gpt_form.cleaned_data
        title = cd['title'].strip()
        group_name = cd['group'].strip()

        def process_gpt(title, group_name):
            extra = generate_song_data(title, group_name)
            group, _ = Group.objects.get_or_create(name=group_name)
            Song.objects.create(
                title=title,
                group=group,
                effects=extra.get('effects', ''),
                guitar_model=extra.get('guitar_model', ''),
                amplifier=extra.get('amplifier', ''),
                description=extra.get('description', ''),
            )

        Thread(target=process_gpt, args=(title, group_name)).start()
        return redirect('/')
    

def form_file(request):
    file_form = FileSongForm(request.POST, request.FILES)
    if file_form.is_valid():
        audio_file = file_form.cleaned_data['audio_file']
        file_path = default_storage.save(f"temp/{audio_file.name}", audio_file)

        def process_audio(path):
            extra = recognize_song_from_file(path)
            group, _ = Group.objects.get_or_create(name=extra.get('group_name', ''))
            Song.objects.create(
                title=extra.get('song_name', ''),
                group=group,
                effects=extra.get('effects', ''),
                guitar_model=extra.get('guitar_model', ''),
                amplifier=extra.get('amplifier', ''),
                description=extra.get('description', ''),
            )
            default_storage.delete(path)

        Thread(target=process_audio, args=(file_path,)).start()

        return redirect('/')

def index(request):
    song_form = SongForm()
    gpt_form  = GptSongForm()
    file_form = FileSongForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type', '') 

        if form_type == 'gpt':
            return form_gpt(request)
        elif form_type == 'file':
            return form_file(request)
        else:
            return form_default(request)

    query = request.GET.get('q', '').strip()
    songs = Song.objects.all().order_by('title')
    if query:
        songs = songs.filter(title__icontains=query)

    return render(
        request,
        'index.html',
        {
            'form': song_form,
            'gpt_form': gpt_form,
            'file_form': file_form,
            'songs': songs,
        },
    )

def search_results(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return redirect('/')

    songs = Song.objects.filter(title__icontains=query).order_by('title')
    return render(request, 'results.html', {'songs': songs, 'query': query})

def song_detail(request, song_id):
    song_obj = get_object_or_404(Song, id = song_id)
    return render(request, 'song.html', {'song': song_obj})

def group_detail(request, group_id):
    group_obj = get_object_or_404(Group, id = group_id)
    songs_obj = group_obj.songs.all()

    return render(request, 'group.html', {
        'group' : group_obj,
        'songs': songs_obj
    })

