import os
from openai import OpenAI
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_song_data(title: str, group: str) -> dict:
    text =f" Это запрос с сервера\
            ты должен выдать для песни {group} {title} в строгом формате ответ вот формат дополни его без лишних коментариев (слово отвнт писать не нужно резделение между словом и ответом обязательно ':-' )\
            effects:-ответ\
            guitar_model:-ответ\
            amplifier:-ответ\
            description:-ответ"
    
    

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "user", "content": text}
        ]
    )
    
    res = response.choices[0].message.content.split('\n')
    return {
        'effects': res[0].split(':-')[1],
        'guitar_model': res[1].split(':-')[1],
        'amplifier': res[2].split(':-')[1],
        'description': res[3].split(':-')[1],
    }

model = WhisperModel("base", device="cpu", compute_type="int8")

def recognize_song_from_file(file_path):
    segments, info = model.transcribe(file_path, beam_size=5)
    recognized_text = " ".join([segment.text.strip() for segment in segments])

    prompt = f"""
        я даю тебе текст песни ты должен дать только информацию по ней и ничего больше даже если ты не уверен что это за песня 
        текст может быть местами не точный его делала такая же тупая нейронка как и ты по этому надо именно проанализировать ВЕСЬ ТЕКСТ И НА ОСНОВЕ ВСЕГО ТЕКСТА 
        и понять с начала название песни и группу а потом уже зная эти факты найти и другие
        ничего не каментируй это ответ для сервера 
        ответ должен быть получен в любом случае (именно факты а не то что ты не знаешь что это никаких Unknown и подобного)
        Ответ в строгом формате:
        name_song:-ответ
        name_group:-ответ 
        effects:-ответ  
        guitar_model:-ответ  
        amplifier:-ответ  
        description:-ответ


        \"\"\"{recognized_text}\"\"\"
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты должен отвечать в строгом формате для сервера"},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content

    lines = content.strip().split('\n')
    return {
        'song_name': lines[0].split(':-', 1)[1].strip(),
        'group_name': lines[1].split(':-', 1)[1].strip(),
        'effects': lines[2].split(':-', 1)[1].strip(),
        'guitar_model': lines[3].split(':-', 1)[1].strip(),
        'amplifier': lines[4].split(':-', 1)[1].strip(),
        'description': lines[5].split(':-', 1)[1].strip(),
    }
