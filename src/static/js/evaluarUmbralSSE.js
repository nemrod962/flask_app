/*Librería para evaluar los SSE y mostrar notificaciones si se
sobrepasa umbral*/
/*
	REQUERE LAS LIBRERIAS
	<script type= "text/javascript" 
    src="{{ url_for('static',filename='js/jquery.js') }}">
    </script>
    {# JQuery cookies library#}
    <script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js">
    </script>
    {# Importo notificaciones gráficas #}
    <script src= "{{ url_for('static',filename='js/graphicalNotification.js') }}">
    </script>
*/

//Recibo los datos del sse (String) como argumento. De ahí sacaré el 
//número aleatorio escrito y las bases de datos en las que se ha
//alamcenado
function evaluarUmbralSSE(datosSSE)
{
    //Obtengo numero aleatorio de el SSE
    //el SSE tiene la siguiente estructura:
    //<rnd>,<fechams>#<listaDB>
    //44.65,fechams#Beebotte,MySQL,
    var num = getNumeroAleatorioSSE(datosSSE);
    var fecha = getFechaSSE(datosSSE);

    console.log("Numero: " + num);
    console.log("Fecha: " + fecha);

    //Obtengo umbral de las cookies
    //Empleo la libraria de cookies
    //var umbral = parseFloat(Cookies.get('umbral'));
    var umbral = getUmbralCookie();
    console.log("Mi umbral:" + umbral);
    
    //---
    //Base de datos empleada por el usuario (cookie)
    dbUser = getDBCookie();
    //Lista de las bases de datos en las que se
    //ha escrito el numero aleatorio
    dbSSE = getDBListSSE(datosSSE);
    //---

    //Si el valor 'umbral' no existe en la cookie, la
    //variable umbral tomará el valor 'NaN'.
    //Nos viene bien igualmente pues cualquier comparación
    //de tamaño de NaN con un número siempre será false,
    //por lo que no se activarán las notificaciones.
    evaluarNotificacionesSSE(num, umbral, dbSSE, dbUser);


}

/*
    DATOS DE LAS COOKIES DEL CLIENTE
*/
function getUmbralCookie()
{
    var umbral = parseFloat(Cookies.get('umbral'));
    return umbral;
}

function getDBCookie()
{
    var db = Cookies.get('db');
    //Como la base de datos por defecto es MongoDB
    //si db == undefined (no existe valor 'db' en la cookie)
    //le asiganmos "MongoDB"
    if(db == undefined)
        db="MongoDB";
    return db;
}

/*
    OBTENCION DE LOS CAMPOS DEL SSE RECIBIDO
*/

/*Obtiene la lista de las bases de datos en las que se ha escrito
el número aleatorio.*/
function getDBListSSE(datosSSE)
{
    //Obtengo la lista de las bases de datos en
    //el SSE, que tiene la siguiente estructura:
    //<rnd>#<listaDB>
    //44.65#Beebotte,MySQL,
    var dbl0 = String(datosSSE)
    //44.65#Beebotte,MySQL,
    var dbl1 = dbl0.split("#");
    //["45.65", "Beebotte,MySQL,"]
    var dbl2 = dbl1[1].split(",");
    //["Beebotte", "MySQL", ""]
    /*Con esto elimino los elementos "" */
    var dbl = dbl2.filter(Boolean)
    //["Beebotte", "MySQL"]
    return dbl
}

/*Obtiene el numero aleatorio instertado*/
function getNumeroAleatorioSSE(datosSSE)
{
    //Obtengo numero aleatorio de el SSE
    //el SSE tiene la siguiente estructura:
    //<rnd>#<listaDB>
    //44.65,fechams#Beebotte,MySQL,
    var num0 = String(datosSSE)
    //44.65,fechams#Beebotte,MySQL,
    //console.log('num0: ' + num0)
    var num1 = num0.split("#",1);
    //["44.65,fechams"]
    //console.log('num1: ' + num1)
    var num2 = num1[0].split(",")
    //[44.65, fechams]
    var num = num2[0];
    return num
}

/*Obtiene la fecha ne la que 
se ha obtenido el numero 
aleatorio instertado*/
function getFechaSSE(datosSSE)
{
    //Obtengo la fecha de el SSE
    //el SSE tiene la siguiente estructura:
    //<rnd>,<fechams>#<listaDB>
    //44.65,fechams#Beebotte,MySQL,
    var date0 = String(datosSSE)
    //44.65,fechams#Beebotte,MySQL,
    //console.log('date0: ' + date0)
    var date1 = date0.split("#",1);
    //["44.65,fechams"]
    //console.log('date1: ' + date1)
    var date2 = date1[0].split(",")
    //[44.65, fechams]
    var date = date2[1];
    return date
}

/*Recibe el número aleatorio escrito en la base de datos
y el umbral del usuario. Si el número escrito activa el umbral,
mostrará por pantalla una notificación en el navegador*/
function evaluarNotificacionesSSE(num, umbral, dbList, dbUser)
{   

    //Comprueba si el numero se ha escrito en la BD
    //que esta empleando actualmente el usuario, es decir,
    //si está diponible para el mismo.
    var esNumDisponible = (dbList.indexOf(dbUser)!=-1)
    //Indica si hay que sobrepasar o no
    //el umbral para activarlo.
    var umbralSuperior=true;
    //Los numeros < 0 indicaran umbrales
    //inferiores, es decir, si por ejemplo
    //tenemos el umbral -20, todos los 
    //números que se registren < que 20
    //activarán el umbral
    if(umbral < 0 )
    {
        //Paso umbral a positivo
        umbral *= -1
        //Indico que el umbral es inferior
        umbralSuperior=false
    }
    /*compruebo si el numero supera a el umbral a ser superado*/
    if(umbralSuperior)
    {
        if(num > umbral)
        {
            notifyMe("UMBRAL SUPERADO"
            + "\n*Número: " + num
            + "\n*Umbral: " + umbral
            + "\n*Bases de datos: " + dbList
            + "\n*Base datos Usuario: " + dbUser
            + "\n*Disponible? " + esNumDisponible);
        }
    }
    /*compruebo si el numero no supera a el umbral a no ser superado*/
    else
    {
        if(num < umbral)
        {
            notifyMe("UMBRAL INFERIOR"
            + "\n*Número: " + num
            + "\n*Umbral: " + umbral
            + "\n*Bases de datos: " + dbList
            + "\n*Base datos Usuario: " + dbUser
            + "\n*Disponible? " + esNumDisponible);
        }
    }

}
