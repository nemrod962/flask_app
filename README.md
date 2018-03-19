# flask_app

Aplicación Flask de servidor. Este servidor obtiene el primer número aleatorio generado por http://www.numeroalazar.com.ar/. El número obtenido es almacenado junto con su tiempo de obtención (en milisegundos) en dos bases de datos:
* Una base de datos local: MySQL.
* Otra base de datos online: Beebotte.

Se puede acceder a esta aplicación a través de un navegador cualquiera. Se emplea el puerto 5000.

Dentro de la aplicación se puede seleccionar cuál de las dos bases de datos se va a emplear para realizar las diferentes operaciones con los datos.

Las operaciones disponibles son:

* Ver el contenido de la base de datos seleccionada en forma de tabla
* Calcular la media de los valores contenidos en la base de datos.
* Especificar un umbral y obtener los últimos números obtenidos que superaron superior e inferiormente el umbral especificado.
* Obtener las gráficas sobre los valores que ofrece Beebotte en su propia web.

## Instalación

Para instalar un entorno virtual con flask para poder ejecutar la aplicación se pueden utilizar los scripts proporcionados en el repositorio:

* Copiar contenido del repositorio

```shell
git clone https://github.com/pablopenna/flask_app
```

* Instalar python, virtualenv y sus dependencias:

```shell
bash -x instalar_flask.txt
```

* Instalar PhantomJS (necesario para obtener las gráficas de Beebotte):

```shell
bash -x instalar_phantomjs.txt
```

* Instalar las librerías que la aplicación necesita

```shell
pip install -r requirements.txt
```

* Ejecutar la aplicación. Es importante hacerlo desde dentro del directorio 'src', ya que se buscan los archivos de credenciales en la ruta relatica './credentials/'.

```shell
cd src
python main_flask.py
```
