from moviepy.editor import *
from gtts import gTTS
import os, json, random, datetime

def generar_video(texto):
    resolucion = (1080,1920)
    duracion = 15
    
    # Audio TTS
    tts = gTTS(texto, lang="es", slow=False)
    tts_file = "temp/voz.mp3"
    tts.save(tts_file)

    audio = AudioFileClip(tts_file)
    duracion = audio.duration
    
    # Fondo simple (negro)
    fondo = ColorClip(size=resolucion, color=(0,0,0), duration=duracion)
    
    # Texto usando caption (funciona en Termux)
    texto_clip = TextClip(
        texto,
        fontsize=70,
        color="white",
        size=(900, None),
        method="caption"
    ).set_position(("center", "center")).set_duration(duracion)

    final = CompositeVideoClip([fondo, texto_clip]).set_audio(audio)

    nombre = f"out/video_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    final.write_videofile(nombre, fps=30)
    return nombre

def main():
    print("Generando video de prueba...")

    texto = "Dato curioso: ¿sabías que los pulpos tienen tres corazones?"
    archivo = generar_video(texto)

    print(f"Video generado: {archivo}")

main()
