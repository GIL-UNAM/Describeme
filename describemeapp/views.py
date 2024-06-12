from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .client import creaSocket, enviaMensaje, cierraSocket

# Formulario en español
class Formulario(forms.Form):
    oracion = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control mb-2', 'id':'inlineFormInput', 'placeholder':'Oración', 'style': 'width:600px'}))
    #cantidadTerminos = forms.IntegerField(label="Términos", max_value=100, min_value=1, widget=forms.NumberInput(attrs={'class':'form-control', 'id':'inlineFormTerms', 'placeholder':'No.', 'style': 'width:75px'}))


# Formulario en inglés
class Form(forms.Form):
    phrase = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control mb-2', 'id':'inlineFormInput', 'placeholder':'Phrase', 'style': 'width:600px'}))
    #noTerms = forms.IntegerField(label="Términos", max_value=100, min_value=1, widget=forms.NumberInput(attrs={'class':'form-control', 'id':'inlineFormTerms', 'placeholder':'No.', 'style': 'width:75px'}))


# Página de inicio.
def index(request):
    return render(request, "describemeapp/index.html")


# Vista en español.
def esp(request):

    # Comprueba si el método es POST
    if request.method == "POST":

        # Toma los datos que envió el usuario y los guarda como formulario
        formulario = Formulario(request.POST)

        # Comprueba si los datos del formulario son válidos
        if formulario.is_valid():

            # Guarda los datos ingresados por el usuario
            oracion = formulario.cleaned_data["oracion"]
            #cantidadTerminos = formulario.cleaned_data["cantidadTerminos"]
            #enviar = formulario.cleaned_data["enviar"]

            # Crea el socket
            cliente = creaSocket()

            # Envía la oración al servidor y recibe la respuesta
            terminos = enviaMensaje(cliente, oracion, "ESP")
            print(terminos)
            # Cierra el socket
            cierraSocket(cliente)

            # Muestra la página con la respuesta del servidor
            return render(request, "describemeapp/esp.html", {
                "formulario": Formulario(),
                "terminos": terminos,
                "oracion": oracion
            })

        else:

            # Si el formulario es inválido, re-renderiza la página con la información introducida
            return render(request, "describemeapp/esp.html", {
                "formulario": formulario
            })

    return render(request, "describemeapp/esp.html", {
        "formulario": Formulario()
    })



# Vista en inglés.
def eng(request):

    # Comprueba si el método es POST
    if request.method == "POST":

        # Toma los datos que envió el usuario y los guarda como formulario
        formulario = Form(request.POST)

        # Comprueba si los datos del formulario son válidos
        if formulario.is_valid():

            # Guarda los datos ingresados por el usuario
            oracion = formulario.cleaned_data["phrase"]
            #noTerms = formulario.cleaned_data["noTerms"]

            # Crea el socket
            cliente = creaSocket()

            # Envía la oración al servidor y recibe la respuesta
            terminos = enviaMensaje(cliente, oracion, "ENG")

            # Cierra el socket
            cierraSocket(cliente)

            # Muestra la página con la respuesta del servidor
            return render(request, "describemeapp/eng.html", {
                "formulario": Form(),
                "terminos": terminos,
                "oracion": oracion
            })

        else:

            # Si el formulario es inválido, re-renderiza la página con la información introducida
            return render(request, "describemeapp/eng.html", {
                "formulario": formulario
            })

    return render(request, "describemeapp/eng.html", {
        "formulario": Form()
    })
