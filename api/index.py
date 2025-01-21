import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LigaMxScrapper import app

# Necesario para Vercel
handler = app 