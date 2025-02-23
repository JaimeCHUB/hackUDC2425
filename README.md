# hackUDC2425

Referencias Licencia MIT:
https://choosealicense.com/licenses/mit/
https://opensource.org/license/MIT

## ¿Cuál es su nombre?  
Somos Hacktech

## ¿Qué hace? ¿Qué problema soluciona?  
Hemos implementado un motor de búsqueda web que utiliza las API oficiales de Inditex. Este proyecto busca facilitar el acceso a productos de las marcas que componen Inditex, utilizando sus APIs para realizar búsquedas personalizadas. Puede usarse para tener un acercamiento al tema de la necesidad y al sistema frontend/backend requerido para su implementación.  

## ¿De qué depende? ¿Qué necesito instalar y usarlo?  
Este proyecto depende de varias herramientas y frameworks de libre uso. Primero, es fundamental contar con acceso a la API oficial de Inditex para que las búsquedas funcionen correctamente. Además, para el servicio REST y la comunicación con el cliente, usamos el framework FastAPI de Python, por lo que es necesario instalar el módulo correspondiente a este junto con sus dependencias. Las dependencias básicas serán uvicorn para ejecutar el servidor y requests para manejar las peticiones

## ¿Cómo funciona?  
El sistema consta de dos módulos principales, frontend y backend. El frontend está diseñado en JavaScript-CSS-HTML básico y se encarga de interactuar con la siguiente capa de lógica de negocio, enviando solicitudes de búsqueda y mostrando los resultados. El backend está desarrollado en Python utilizando FastAPI y se comunica con la API de Inditex para obtener los datos de productos. La comunicación entre estos módulos se realiza a través de un sistema de mensajes en formato Json, que luego son procesadas y consultas por los módulos correspondientes a la comunicación.

## ¿Qué funciona? ¿Qué no funciona?  
**Funciona:**  
- La interacción entre el frontend y el backend a través de mensajes en formato JS-API REST y Python-API.
- El backend puede realizar búsquedas correctamente utilizando la API de Inditex.
- El frontend muestra los resultados de manera adecuada al usuario.

**No funciona:**  
- El filtrado es muy básico y puede encontrarse no conformidades
- Algunas búsqueda pueden cometer funciones erróneas
- 
## ¿Dónde puedo preguntar si encuentro un problema o tengo dificultades?  
En caso de encontrar problemas, puedes abrir un *issue* en nuestro repositorio. Trataremos de resolverlo lo antes posible. No contamos con redes sociales tales como discord para el contacto directo con interesados

## ¿Cómo puedo contribuir?  
Si quieres contribuir al proyecto, hay varias formas de hacerlo. Puedes empezar reportando cualquier error o sugerencia de mejora en el repositorio. También admitimos mejoras de documentación o proposición de nuevas funcionalidades útiles. Si quieres crear un proyecto nuevo que difiera de este usando su base, siempre puedes hacer un *fork* del repositorio.

## ¿Quiénes han contribuido?  
Este proyecto es completamente nuevo, por lo que aún no tenemos contribuciones externas. Estamos trabajando en ello y esperamos que otros se unan pronto para ayudarnos a mejorar y expandir el proyecto.

## ¿Qué licencia tiene?  
Usamos la licencia MIT. Entendemos que el objetivo principal de nuestro proyecto, Inditex, no es ofrecer un uso libre de sus productos a todos sus posibles clientes. Por lo tanto, esta licencia equilibra el uso de software libre con el interés de otros colaboradores y la necesidad de soluciones para cualquier empresa que requiera este software.  

## Where can I ask if I've found an issue or troubles?
A nosotros, pues como desarrolladores tenemos la responsabilidad de explicar al cliente el funcionamiento y posibles riesgos y problemáticas que le vayan a surgir durante el desarrollo de su software.

## ¿Como puedo contribuir?
Con un portal de issues, para que los problemas puedan ser identificados a tiempo y una serie de recomendaciones para evitarlos y solventarlos.

## ¿Quién contribuyó?
No tenemos ningún contribuidor externo, solo trabajamos los 4 internos.

## ¿Que licencia tiene?
Dependencias y sus Licencias
1. **FastAPI**:
   - **Licencia**: MIT License
   - **Descripción**: FastAPI es un framework web moderno y de alto rendimiento para construir APIs con Python 3.6+ basado en estándares como OpenAPI y JSON Schema.
2. **Requests**:
   - **Licencia**: Apache License 2.0
   - **Descripción**: Requests es una librería HTTP simple y elegante para Python, construida para hacer solicitudes HTTP de manera fácil y rápida.
