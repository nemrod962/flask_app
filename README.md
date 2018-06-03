# flask_app

Aplicación Flask de servidor. Este servidor obtiene el primer número aleatorio generado por http://www.numeroalazar.com.ar/. El número obtenido es almacenado junto con su tiempo de obtención (en milisegundos) en dos bases de datos:
* ~~Una base de datos local: MySQL~~(obsoleto).
* Una base de datos local: MongoDB.
* Otra base de datos online: Beebotte.

Se puede acceder a esta aplicación a través de un navegador cualquiera. Se emplea el puerto 5000.

Dentro de la aplicación se puede seleccionar cuál de las dos bases de datos se va a emplear para realizar las diferentes operaciones con los datos.

Las operaciones disponibles son:
* Obtener un número aleatorio de la base de datos
* Ver el contenido de la base de datos seleccionada en forma de tabla
* Calcular la media de los valores contenidos en la base de datos.
* Especificar un umbral y obtener los últimos números obtenidos que superaron superior e inferiormente el umbral especificado.
* Obtener las gráficas sobre los valores que ofrece Beebotte en su propia web.
* Obtener gráfica de puntos con los números en las bases de datos y crear un grafo de frecuencias.

Otras características de la aplicación son:
* Google Sign-in
* Notificaciones de escritorio cuando se activa el umbral de usuario.

## Instalación

Para instalar un entorno virtual con flask para poder ejecutar la aplicación se pueden utilizar los scripts proporcionados en la carpeta scripts/ el repositorio:

* Copiar contenido del repositorio

```shell
git clone https://github.com/pablopenna/flask_app
```

* Instalar python, virtualenv y sus dependencias:

```shell
cd scripts/
bash -x instalar_flask.txt
```

* Instalar PhantomJS (necesario para obtener las gráficas de Beebotte):

```shell
bash -x instalar_phantomjs.txt
```
* Iniciar el entorno virtual
```shell
cd ..
bash -x init_flask.txt
```
* Instalar las librerías que la aplicación necesita

```shell
pip install -r scripts/requirements.txt
```

* Tener MongoDB instalado. Puede emplearse un contenedor de Docker como alternativa:
  - Instalar Docker: [Docker Install Guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
  - Descargar imagen mongo y crear contenedor [Docker Mongo Page](https://hub.docker.com/_/mongo/). Es importante que al crear el contenedor se vincule el puerto 27017 del contenedor a uno del host para poder acceder a mongoDB desde la aplicación flask. Por ejemplo, para vincular el puerto 27017 del contenedor al 8080 del host: `docker run ... -p 8080:27017 ...`.
  - Especificar la configuración de mongoDB en el fichero src/credentials/mongo_credentials.json (usuario, contraseña, host, puerto y base de datos.)
  - Alternativamente pueden emplearse los scripts en scripts/dockerScripts/
    - Instalar Docker `bash -x installDockerUbuntu.sh`.
    - Crear contenedor `bash -x installMongoDocker.sh`. Especificar las credenciales deseadas modificando el archivo `mongoAddAdminConfig`.
    - Especificar la configuración de mongoDB en el fichero src/credentials/mongo_credentials.json (usuario, contraseña, host, puerto y base de datos.)
  

* Ejecutar la aplicación utilizando el script `launch_app.sh` habiendo introducido previamente en él el nombre de tu contenedor de MongoDB.

```shell
./launch_app.sh
```
