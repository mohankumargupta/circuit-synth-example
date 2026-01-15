set shell := ["sh", "-c"]
set windows-shell := ["powershell", "-c"]

export KICAD_SYMBOL_DIR := "C:/Program Files/KiCad/9.0/share/kicad/symbols;C:/Users/mohan/Documents/KiCadLibraryLoader;C:/Users/mohan/Documents/KiCad/9.0/3rdparty/symbols/com_github_CDFER_JLCPCB-Kicad-Library;C:/Users/mohan/Documents/KiCad/9.0/3rdparty/symbols/com_github_espressif_kicad-libraries"

run:
  uv run main.py
  start "C:\Program Files\KiCad\9.0\bin\kicad.exe"
debug:
  uv run python -m debugpy --listen 5678 --wait-for-client main.py

