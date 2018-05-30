//Var globales para poder actualizar mediante SSE
var listaNumerosGlobal = [];
/*
 - elem es el elemento html donde insertaremos la tabla creada. 
 Típicamente será un <div>.
 - lista datos es una lista que contiene varias listas con los
datos a tratar.*/
function crearTablaMedia(elem, listasDatos)
{
    //Damos formato a listasDatos
    //listaDatos = [ listaNumeros, listaFechasMS]
    for(indice in listasDatos)
    {
        listasDatos[indice] = flaskToArray(listaDatos[indice]);
    }
    //DEBUG
    for(indice in listasDatos)
    {
        console.log('DATOS[' +indice+']: ' + listasDatos[indice])
        console.log('primer elem: ' + listasDatos[indice][0])
    }
    
    //Para crear la tabla necesito el elem, listaCabeceras
    //y listaDatos.

    //getResMedia() solo recibe una lista con los numeros aleatorios
    //por lo que solo tendremos que pasarle listasDatos[0] que es la
    //que los contiene.
    var listaNumeros = listasDatos[0]
    var dato=getResMedia(listaNumeros);
    //getResMedia devuelve la media de la lista.
    //Esta media la meteremos en una lista dentro de otra lista 
    //de forma que tengamos una lista de listas. Esto es para poder 
    //utilizar esta lista como argumento de la funcion crear tabla
    var listaDato = [[dato]]
    listaCabeceras=["Media"];

    //creo tabla
    crearTabla(elem,listaCabeceras,listaDato,true);

    //Actualizo variable global si no esta 
    //inicializada.
    if(listaNumerosGlobal.length == 0)
    {
        listaNumerosGlobal = listaNumeros;
    }
}

/*Realiza la operación media con los datos recibidos (numeros aleatorios en la
 * base de datos) y devuelve el resultado

listaDatos = listaNumeros.

La función devolverá la media de los números almacenados en la base de datos.
*/
function getResMedia(listaDatos)
{
    console.log('- getResMedia()');

    //Obtengo la longitud/numero de elementos en la lista
    var longNumeros=listaDatos.length;

    //Aviso
    if(longNumeros==0)
    {
        console.log('Lista números vacía!');
    }
    
    //Almacenare la suma de todos los numeros en la lista
    var sumatorio = 0;

    for(var i=0;i<longNumeros;i++)
    {
        sumatorio+=listaDatos[i];
    }
    
    //hallo media
    var media=sumatorio/longNumeros

    //DEBUG
    console.log('longitud lista: ' + longNumeros);
    console.log('sumatorio: ' + sumatorio);
    console.log('media: ' + media);

    //retornamos la media de los numeros
    return media;
}

/*Actualizar Media mediante SSE*/
function updateTableMediaSSE(datosSSE, divTabla)
{
    //Obtengo el numero añadido mediante SSE
    var num = getNumeroAleatorioSSE(datosSSE);
    //Lo añado a la lista de numeros global
    listaNumerosGlobal.push(num);
    //Vuelvo a crear la tabla de medias
    //Meto listaNumerosGlobal en una lista
    //pues crearTablaMedia recibe una lista
    //de listas con los datos
    crearTablaMedia(divTabla, [listaNumerosGlobal])
}
