# Describeme

Aplicación que sugiere términos relacionados a partir de una descripción corta.
Está dividida en dos componentes:

- Backend (demonio de sockets): carga grafos de asociación en español e inglés y responde peticiones por `localhost:5050`. Archivos clave en `describemeapp/`: `server.py`, `defineme_esp.py`, `defineme_eng.py`, `bitacora.py`.
- Frontend (Django): formularios web que envían la frase al demonio y muestran los términos devueltos. Código principal en `describemeapp/views.py` y plantillas en `describemeapp/templates/`.

El backend registra peticiones en `describemeapp/registros.tsv` mediante `Bitacora`.

## Requisitos previos

- Python 3.8+
- Virtualenv (`python -m venv`) recomendado
- Dependencias de sistema para compilar spaCy (por ejemplo, `build-essential`, `python3-dev` en Debian/Ubuntu)
- Corpus incluidos en `describemeapp/corpus/`:
  - `original.xls` (español)
  - archivos en `separados_florida/` (inglés)

## Instalación

1) Crear y activar entorno virtual:
```bash
cd /var/www/Describeme
python3 -m venv env
source env/bin/activate
```

2) Instalar dependencias de Python:
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm
```

3) Descargar datos NLTK requeridos (stopwords, wordnet, omw-1.4):
```bash
python - <<'PY'
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
PY
```

4) Verificar que `describemeapp/registros.tsv` sea escribible por el usuario que ejecuta el servicio.

## Ejecución local

1) Levantar el backend de sockets (requerido antes del front):
```bash
cd /var/www/Describeme
source env/bin/activate
cd describemeapp
python server.py
```
Escucha en `localhost:5050`, carga los grafos (puede tardar unos segundos) y se detiene escribiendo `salir` en STDIN.

2) Levantar el frontend Django en otra terminal:
```bash
cd /var/www/Describeme
source env/bin/activate
python manage.py migrate  # no hay modelos, pero prepara el entorno
python manage.py runserver 0.0.0.0:8000
```

3) Uso:
- Español: `http://localhost:8000/esp`
- Inglés: `http://localhost:8000/eng`

## Servicio systemd para el backend

El script `iniciademonio.sh` activa el entorno virtual y lanza `server.py`.
Ejemplo de unidad `/etc/systemd/system/midemonio.service` (ajuste usuario y rutas según su entorno):
```ini
[Unit]
Description=Inicia demonio Describeme
After=network.target

[Service]
ExecStart=/var/www/Describeme/iniciademonio.sh
Restart=always
WorkingDirectory=/var/www/Describeme
User=usuario
Group=www-data
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
```

Aplicar y habilitar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now midemonio.service
```

## Notas y mejoras

- El frontend depende del demonio; si no está corriendo en `localhost:5050`, las vistas `esp` y `eng` no devolverán términos.
- `registros.tsv` crece indefinidamente; considere rotarlo o moverlo a un directorio de logs.
- Podría integrarse el backend en el propio servidor web (Flask/FastAPI) para evitar mantener un proceso separado de sockets.
