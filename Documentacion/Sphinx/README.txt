Crear documentación con Sphinx

1. Instalamos sphinx con el comando "sudo apt install python-sphinx -y"
2. Creamos una carpeta "docs" en el directorio del proyecto
3. Nos colocamos en el terminal en la carpeta "docs" y lanzamos el comando
   "sphinx-quickstart"
4. Seleccionamos las opciones a nuestro gusto y continuamos
5. Descomentamos los imports de "os", "sys" y la linea de sys.path.insert,
   a la que le modificamos la ruta a "abspath('..'))"
6. En extensions modificamos la linea para que quede de esta forma: 
   extensions = ['sphinx.ext.autodoc']
7. (Opcional) Sphinx permite buscar un tema personalizado en Sphinx Themes,
   donde podemos ver los pasos de instalación del tema y descargar su fichero
   "conf.py"
8. Añadimos la linea "modules" en el fichero "index.rst"
9. Lanzamos el comando "sphinx-apidoc -o <ruta_salida> <ruta_codigo>"
10. Por último lanzamos el comando "make html" y se genera nuestra
    documentación en: "/docs/_build/html/index.html"
