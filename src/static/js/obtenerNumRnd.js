/* obtenerNumRnd.js */
/* Empleado en la página /random */
/*Implementa la funcionalidad del html random.html, el cual consiste en mostrar
 * un numero aleatorio aleatorio contenido en la base de datos.
 Reicbiremos del servidor una lista de los numeros aleatorio y las fechas de
 obtencion. Generaremos un indice aleatorio de estas listas para obtener un
 numero aleatorio aleatorio y mostrarlo en la página web.*/

//Variables globales para poder compartirlas entre funciones
var listaGlobalNumero = [];
var listaGlobalFecha = [];
//selector del span en el que mostrare el numero
var selectSpanGlobal;
//selector del div en el que creare las tablas
//con los datos del numero aleatorio
var selectDivGlobal;

/*FUNCION INICIAL. Se llama una única vez al inicio para inicializar las listas
 * y asignar funcionalidad al boton*/
/*Recibe como argumento 
-> Las listas de numeros y fechas de flask, sin parsear,
-> Selector del boton (cadena para poder seleccionarlo en JQuery) de la 
pagina para asignarle la funcionalidad de que cuando se pulse muestre
otro numero aleatorio
-> Selector del span donde se mostrará el número aleatorio
-> Selector del div donde creare la tabla con los datos del 
numero aleatorio.*/
function mostrarNumeroAleatorio(listaNum, listaDate, selectButton, selectSpan, selectDiv)
{
    //Parseo listas
    listaNum = flaskToArray(listaNum)
    listaDate = flaskToArray(listaDate)

    //asigno variables globales
    listaGlobalNumero = listaNum;
    listaGlobalFecha = listaDate;
    selectSpanGlobal = selectSpan;
    selectDivGlobal = selectDiv;

    //Asigno funcionalidad al boton
    $(selectButton).click(function()
    {
        refrescarNumeroAleatorio();
    });

    console.log("HOLA!");
    refrescarNumeroAleatorio();
}

/*Una vez que tengamos las lista parseadas podemos llamar a esta funcion para
 * mostrar otro numero aleatorio en la pagina*/
function refrescarNumeroAleatorio()
{
    //Obtengo longitud de la lista con los numeros aleatorio
    var longitud = listaGlobalNumero.length;

    //Genero numero aleatorio que empleare como indice
    //Math.random() genera numero del 0 (inclusivo)
    //al 1 (exclusivo)
    var indiceAleatorio = parseInt(Math.random() * longitud);

    //El numero en el indice en la lista sera el
    //numero aleatorio a mostrar
    var num = listaGlobalNumero[indiceAleatorio];
    var date = listaGlobalFecha[indiceAleatorio];

    //Asigno el valor del span al numero aleatorio
    $(selectSpanGlobal).html(num);

    //Preparo variables para la tabla
    var listaCab = ["Numero","Fecha"];
    //La lista de datos que recibe 
    //crearTablaNumRnd() es una lista de listas
    var listaDatos = [[num], [date]];

    //Creo tabla (utilzo crearTablaNumRnd()
    //porque tiene el mismo formato que la 
    //tabla que quiero crear).
    var mydiv = $(selectDivGlobal)[0];
    crearTablaRandom(mydiv,listaCab,listaDatos);
}
