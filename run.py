# run.py
import os
import textwrap
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

# ---------- CONFIG ----------
OUTPUT_DIR = "output"
ASSETS_DIR = "assets"
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final.mp4")
VOICE_FILE = os.path.join(OUTPUT_DIR, "voz.mp3")

# Duración por imagen (segundos)
DURACION_POR_IMAGEN = 3

# Resolución del video (por ejemplo 1080x1920 para vertical/TikTok)
W, H = 720, 1280

# Tipos de video disponibles (plantillas locales)
TEMPLATES = {
    "motivacion": [
        "Respira hondo. Hoy es un nuevo día para empezar de cero.",
        "Cada pequeño paso que das te acerca a tu meta.",
        "No te rindas cuando estés cansado; rindete cuando hayas terminado.",
        "Cree en ti. El primer paso es siempre el más difícil."
    ],
    "curiosidades": [
        "¿Sabías que las abejas comunican la ubicación de las flores mediante un baile?",
        "El corazón de un camarón está en su cabeza.",
        "El agua puede existir en estado líquido por encima de su punto de ebullición bajo presión.",
        "Los pulpos tienen tres corazones y sangre de color azul."
    ]
}
# ----------------------------

def generar_guion(template_name="motivacion"):
    if template_name in TEMPLATES:
        return TEMPLATES[template_name]
    # fallback: una mini plantilla si el nombre no existe
    return [
        "Este es un video automatizado.",
        "Generado con Termux, Python y MoviePy.",
        "Puedes personalizar la plantilla y el texto.",
        "¡Comparte si te gusta!"
    ]

def generar_voz(text_lines, lang='es'):
    full_text = " ".join(text_lines)
    tts = gTTS(text=full_text, lang=lang, slow=False)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tts.save(VOICE_FILE)
    return VOICE_FILE

def crear_imagen_con_texto(text, index, w=W, h=H, bgcolor=(30,30,30), textcolor=(255,255,255)):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    # crea imagen en blanco y escribe texto envuelto
    img = Image.new("RGB", (w, h), color=bgcolor)
    draw = ImageDraw.Draw(img)

    # intenta usar una font básica incluida; si no, usa la por defecto
    try:
        # path de fuente común en termux (puede variar). Si falla, se usa default.
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    margin = 60
    max_width = w - 2 * margin
    wrapped = textwrap.fill(text, width=30)  # ajusta ancho de texto
    # calcular posición vertical centrada aproximada
    text_w, text_h = draw.multiline_textsize(wrapped, font=font)
    x = margin
    y = (h - text_h) // 2
    draw.multiline_text((x, y), wrapped, font=font, fill=textcolor, align="center")
    filename = os.path.join(ASSETS_DIR, f"img_{index}.jpg")
    img.save(filename, quality=85)
    return filename

def crear_video(images, voz, salida=FINAL_VIDEO):
    clips = []
    for img in images:
        clip = ImageClip(img).set_duration(DURACION_POR_IMAGEN).set_fps(24).resize(width=W)
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(voz)
    # ajustar duración del audio si es más largo
    video = video.set_audio(audio)
    # exporta
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    video.write_videofile(salida, fps=24, codec="libx264", audio_codec="aac", threads=0)
    return salida

def main(template_name="motivacion"):
    print("Generando guion...")
    lines = generar_guion(template_name)

    print("Generando voz (gTTS)...")
    voz = generar_voz(lines)

    print("Generando imágenes...")
    images = []
    for i, line in enumerate(lines):
        img = crear_imagen_con_texto(line, i)
        images.append(img)

    print("Creando video final...")
    video_path = crear_video(images, voz)
    print("Video creado en:", video_path)

if __name__ == "__main__":
    # puedes cambiar aquí la plantilla: "motivacion" o "curiosidades"
    main(template_name="motivacion")

