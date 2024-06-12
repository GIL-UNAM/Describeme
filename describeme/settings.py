"""
Django settings for describeme project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v#pjrc(%$-*xf*i5889bkty)6!xyh(rrfho%%ws27o1s0#n&85'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["devsys.iingen.unam.mx", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'describemeapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'describemeapp.middleware.PrefixMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Define SCRIPT_NAME
# FORCE_SCRIPT_NAME indica a Django que todas las URLs generadas deben tener el prefijo /describeme.
# Esto afecta cómo se generan las URLs en las plantillas y redirecciones, asegurando que siempre incluyan el prefijo necesario.
# trabaja en conjunto con el middleware definido en la app describemeapp

FORCE_SCRIPT_NAME = '/describeme'

#Flujo de una Solicitud
# Solicitud Entrante:

# Un usuario solicita https://devsys.iingen.unam.mx/describeme/esp.
# Middleware PrefixMiddleware:

# El middleware detecta el prefijo /describeme.
# Modifica request.path de /describeme/esp a /esp.
# Procesamiento de Django:

# Django maneja la solicitud basándose en la ruta /esp.
# La vista correspondiente se llama y genera una respuesta.
# Respuesta:

# La respuesta es enviada de vuelta al usuario.
# Generación de URLs:

# Con FORCE_SCRIPT_NAME, cualquier URL generada en las plantillas incluirá el prefijo /describeme.

# Integración de Apache con Django a través de VirtualHost
# Los archivos de configuración de Apache que has proporcionado establecen la forma en que Apache maneja las solicitudes y 
# las redirige a tu aplicación Django utilizando mod_wsgi. 
# Vamos a desglosar cómo esto se relaciona con el middleware y las configuraciones de Django que hemos discutido.

# Configuración de Apache (VirtualHost)
# Ejemplo de configuración relevante para tu aplicación describeme:

# apache
# Copiar código
# <VirtualHost *:8345>
#     ServerAdmin webmaster@localhost

#     # ruta del proyecto describeme
#     DocumentRoot /var/www/proyectosdjango/describeme

#     # ruta de los logs
#     ErrorLog /var/www/produccion/logs/describeme/error.log
#     CustomLog /var/www/produccion/logs/describeme/access.log combined

#     # establece el directorio de donde toma los static
#     Alias /static /var/www/produccion/describeme/staticFiles

#     WSGIDaemonProcess describeme python-home=/var/www/proyectosdjango/describeme/env python-path=/var/www/proyectosdjango/describeme
#     WSGIScriptAlias /describeme /var/www/proyectosdjango/describeme/describeme/wsgi.py process-group=describeme application-group=%{GLOBAL}
# </VirtualHost>
# Desglose de la Configuración:
# VirtualHost:

# Define un bloque de configuración para un servidor virtual escuchando en el puerto 8345.
# DocumentRoot:

# Establece el directorio raíz para el contenido del sitio web. En este caso, es /var/www/proyectosdjango/describeme.
# ErrorLog y CustomLog:

# Establecen las rutas para los archivos de registro de errores y de acceso.
# Alias /static:

# Define un alias para los archivos estáticos de la aplicación. Apunta a /var/www/produccion/describeme/staticFiles.
# WSGIDaemonProcess:

# Define un proceso demonio para la aplicación Django. Especifica el entorno virtual (python-home) y el directorio del proyecto (python-path).
# WSGIScriptAlias:

# Este es el punto clave. Define una alias URL (/describeme) que apunta al archivo wsgi.py de tu proyecto Django. 
# Esto significa que cualquier solicitud que comience con /describeme será manejada por tu aplicación Django.


# *Flujo de la Solicitud con Apache y Django Middleware*

# Solicitud Entrante a Apache:

# El usuario accede a https://devsys.iingen.unam.mx/describeme/esp.
# Apache recibe la solicitud en el puerto 80 y la redirige al puerto 8345 según la configuración de VirtualHost.
# Redirección por WSGIScriptAlias:

# Apache ve que la solicitud es para /describeme y la redirige al wsgi.py de Django correspondiente a /var/www/proyectosdjango/describeme/describeme/wsgi.py.
# Manejo por PrefixMiddleware:

# El middleware PrefixMiddleware entra en acción.
# Modifica request.path de /describeme/esp a /esp para que Django pueda procesar la ruta correctamente.
# Procesamiento de Django:

# Django recibe la solicitud con la ruta modificada (/esp).
# Busca la vista correspondiente y genera la respuesta.
# Generación de URLs en Plantillas:

# Gracias a la configuración FORCE_SCRIPT_NAME, cualquier URL generada por Django incluirá el prefijo /describeme.
# Respuesta a Apache y luego al Navegador:

# Django envía la respuesta generada a Apache.
# Apache entrega la respuesta al navegador del usuario.
# Resumen y Beneficios
# Apache se encarga de la redirección y manejo de las solicitudes hacia la aplicación Django utilizando mod_wsgi.
# WSGIScriptAlias en la configuración de Apache asegura que las solicitudes con el prefijo /describeme sean manejadas por el wsgi.py de Django.
# PrefixMiddleware ajusta el request.path dentro de Django para que las rutas internas sean manejadas correctamente.
# FORCE_SCRIPT_NAME asegura que todas las URLs generadas por Django tengan el prefijo correcto, manteniendo la consistencia en la navegación del sitio.
# Con esta integración, logras que tu aplicación Django funcione correctamente bajo un subdirectorio específico, 
# manejado por Apache, y se aseguran las rutas adecuadas para todas las solicitudes y URLs generadas.





ROOT_URLCONF = 'describeme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'describeme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/describeme/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
