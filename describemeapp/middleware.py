# El middleware es un componente de Django que se ejecuta durante el procesamiento de una solicitud HTTP. 
# Puede modificar la solicitud o la respuesta en varias etapas del ciclo de vida de la solicitud.
#
# El propósito de este middleware es ajustar el request.path y request.path_info 
# para que Django reconozca correctamente las rutas de las vistas que deberían estar bajo el prefijo /describeme. 
# Esto es necesario cuando tu aplicación Django está alojada en un subdirectorio de la URL.

class PrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        script_name = '/describeme'
        if request.path.startswith(script_name):
            request.path_info = request.path[len(script_name):]
            request.path = request.path[len(script_name):]
        response = self.get_response(request)
        return response

'''
Explicación del código:
Inicialización (__init__):

El método __init__ se llama una vez, cuando el servidor se inicia.
Recibe el parámetro get_response, que es una función que Django utiliza para obtener la respuesta de la vista.
Llamada (__call__):

Este método se llama para cada solicitud entrante.
request.path es la ruta completa de la URL solicitada.
script_name es el prefijo que queremos manejar (en este caso, /describeme).
Si la ruta de la solicitud (request.path) comienza con este prefijo, el middleware elimina este prefijo de request.path_info y request.path.
Luego, se llama a get_response para continuar el procesamiento de la solicitud y obtener la respuesta.
Finalmente, el middleware devuelve la respuesta modificada.

Es necesario añadir este middleware en el archivo config.py 
'''