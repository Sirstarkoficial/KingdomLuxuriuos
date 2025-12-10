cd ~
curl -L -o install_auto_reels.sh "data:,PLACEHOLDER"
# (Pero en vez del placeholder copia/pega el contenido del script que te doy abajo)
chmod +x install_auto_reels.sh
./install_auto_reels.sh
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
# Instalador/creador del proyecto AutoReels para Termux
# Crea estructura, instala dependencias y deja todo listo.
# Ajustes básicos:
PROJECT_DIR="$HOME/auto_reels"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_BIN="python3"
# Token y chat (los tuyos)
TELEGRAM_TOKEN="8179830707:AAHagrl8_ySVgIZw40If1FXsKoCk57uDA9o"
TELEGRAM_CHAT="7787175272"
# Usuario (informativo)
TELEGRAM_USER="@Alvarogtz1"
echo "== Instalando paquetes del sistema en Termux =="
pkg update -y
pkg install -y python ffmpeg wget git nano
echo "== Actualizando pip y creando entorno =="
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel
$PYTHON_BIN -m pip install virtualenv || true
# Crear proyecto
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
# Crear virtualenv e instalar deps
$PYTHON_BIN -m virtualenv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install moviepy Pillow gTTS requests python-dotenv
