/*REQUIERE PLOTLY.JS*/

/*Función de prueba para crear un grafo con datos fijos.*/
function crearGrafoSimpleTest(elem, datosX, datosY)
{
    Plotly.plot( 
        elem, 
        [{
            x: [1, 2, 3, 4, 5],
            y: [1, 2, 4, 8, 16] 
        }], 
        { margin: { t: 0 } } 
    );

}

/* Función básica para crear las gráficas. El resto de funciones
dependerán de esta.
Hay que especifiar el elemente donde escribir la gráfica, los
datos de los ejes X e Y, así como el tipo y modo de la gráfica.
Tipos conocidos:
    - scatter (líneas - puntos)
    - bar (barras)

modos conocidos:
    - markers (si se emplea junto con scatter no se 
    dibujan líneas para unir los puntos).
    
*/
function crearGrafo(elem, datosX, datosY, tipo, modo)
{
    var trace1 = {
        x: datosX,
        y: datosY,
        type: tipo,
        mode: modo
    }

    //Si se emplea Plotly.plot en lugar de 
    //Plotly.newPlot, la gráfica generada se
    //añadirá a la ya existente en vez de
    //sobrescribirla.
    Plotly.newPlot( 
        elem, 
        [trace1], 
        { margin: { t: 0 } } 
    );

}

/*
Crea una gráfica simple con los datos recibdos en el elemento elem.
Gráfica de líneas.
    -> elem es el elemento html en el que escribiremos
    la gráfica
    -> datosX es una lista con los datos del ejeX
    -> datosY es una lista con los datos del ejeY
*/
function crearGrafoSimple(elem, datosX, datosY)
{
    crearGrafo(elem,datosX,datosY,'scatter','markers');
}

function crearGrafoSimpleOrdenado(elem, datosX, datosY)
{   
    var ordenado=true;
    for(var i=0;i<datosX.length-1;i++)
    {
        if(datosX[i]>datosX[i+1])
        {
            ordenado=false;
        }
    }
    if(!ordenado)
    {
        datosX=datosX.reverse();
        datosY=datosY.reverse();
    }
    crearGrafoSimple(elem,datosX,datosY);
}


/*
Crea una gráfica simple con los datos recibdos en el elemento elem.
Gráfica de barras.
    -> elem es el elemento html en el que escribiremos
    la gráfica
    -> datosX es una lista con los datos del ejeX
    -> datosY es una lista con los datos del ejeY
*/
function crearGrafoBarras(elem, datosX, datosY)
{
    crearGrafo(elem,datosX,datosY,'bar','None');
}

/* GRAFOS ESPECIFICOS.*/
/* GRAFOS CON LAS FRECUENCIAS DE LOS NUMEROS ALEATORIOS */

/* Para creaer este grafo, trabajeremos principalmente con la lista de números.
No necesitaremos la lista de fehcas en principio.*/
function crearGrafoFreq(elem,listaNumeros,anchuraIntervalo)
{
    anchuraIntervalo = parseInt(anchuraIntervalo);
    //Si la anchura recibida no es un número
    if(isNaN(anchuraIntervalo))
    {
        anchuraIntervalo=10;
    }
    //Si la anchura recibida es 0 o menor que 0
    if(anchuraIntervalo<=0)
    {
        anchuraIntervalo=1;
    }
    //Indico el valor maximo que pude tener 
    //un numero, necesario para crear
    //la lista de intervalos
    //var limite = 100;
    var limite = parseFloat(getLimiteSuperiorNumerico(listaNumeros))
    //------------- 
    //Creo una lista con los intervalos que tendré.
    //Esta lista la pondré en el eje X de la gráfica.
    var listaIntervalos = getListaIntervalos(listaNumeros, anchuraIntervalo, limite)
    console.log('listaIntervalos: ' + listaIntervalos);
    //-----

    //En esta lista almacenaré cuantos números hay en cada intervalo.
    var listaContadoresIntervalos = getListaContadoresIntervalos(listaNumeros,
        listaIntervalos, anchuraIntervalo);
    console.log('listaNumeros: ' + listaNumeros);
    console.log('listaContadores: ' + listaContadoresIntervalos);

    //Creo gráfica
    crearGrafoBarras(elem,listaIntervalos,listaContadoresIntervalos);

}
/*
Función que dada la lista de los números y la anchura de los
intervalos, devuelve una lista que contiene los intervalos.
También necesito conocer el límite superior de los números para
poder definir el último intervalo.
*/
function getListaIntervalos(listaNumeros, anchuraIntervalo, limite)
{
    //Creo una lista con los intervalos que tendré.
    //Esta lista la pondré en el eje X de la gráfica.
    var listaIntervalos = [];
    //Creo lista con los intervalos
    var indice = 0;
    while(indice < limite)
    {
        indice+=anchuraIntervalo
        if(indice > limite)
        {
            indice=limite;
        }
        listaIntervalos.push(indice);
    }
    //La lista intervalos contiene en cada posición un número
    //indica el límite superior del intervalo.
    //Si, por ejemplo, la anchura del intervalo es 20 y
    //el elemento [1] de la lista es 40, quiere decir que
    //ese intervalo es de 20 a 40.
    //Almacenaremos en la lista los intervalos como cadenas
    //que expresen de forma más clara el intervalo

    //En caso de que la anchura de intervalos sea mayor que el limite,
    //limito la anchura para que se cree bien la etiqueta del intervalo
    //al restar la anchura de intervalo
    if(anchuraIntervalo>limite)
    {
        anchuraIntervalo=limite;
    }
    for(var i=0;i<listaIntervalos.length;i++)
    {
        listaIntervalos[i]=String(
            listaIntervalos[i] - anchuraIntervalo + " - "
            + listaIntervalos[i]);
    }
    //La lista de intervalos creada estará en el eje X

    return listaIntervalos;
    
}

/*Dadas las listas con los números y los intervalos,
generará una lista con los contadores de cuántos números 
de la lista de Números hay en cada intervalo.*/
function getListaContadoresIntervalos(listaNumeros, listaIntervalos,
anchuraIntervalo)
{
    //Creo una lista con los intervalos que tendré.
    //Esta lista la pondré en el eje X de la gráfica.
    var listaContadoresIntervalos = [];
    //La inicializo poniendo los contadores de cada intervalo a 0.
    //Deberá tener la misma longitud que la lista de intervalos.
    for(var i=0; i<listaIntervalos.length;i++)
    {
        listaContadoresIntervalos[i]=0;
    }

    //Recorrer la lista de números aleatorios 
    //Clasificándolos según el intervalo en el que se encuentren.
    var indice = 0;
    for(var i=0;i<listaNumeros.length;i++)
    {
        //Obtengo el índice del intervalo al que 
        //pertenece el número. La clave del éxito
        //es esta siguiente línea.
        indice = parseInt(listaNumeros[i]/anchuraIntervalo);
        //incremento contador
        listaContadoresIntervalos[indice]++;
    }
    return listaContadoresIntervalos;
}
/*
Función que dada la lista con los números aleatorios
devuelve el más alto (límite superior) y lo redondea a 
entero.
Si la lista de los datos no contiene elementos numéricos,
esta función devolverá 100 como límite superior.
*/
function getLimiteSuperiorNumerico(listaDatos)
{
    var limite = parseFloat(getLimiteSuperior(listaDatos));
    if(isNaN(limite))
    {
        limite=100;
    }
    //Redondear a Int. Queda mejor
    //que el limite superior sea tambien
    //un numero entero en vez de un decimal.
    if(limite % 1 > 0)
    {
        limite=parseInt(limite)+1;
    }
    else
    {
        limite=parseInt(limite);
    }

    return limite
}

/*
Función que dada una lista devuelve el valor
del elemento más alto (límite superior) en caso de
que la lista contenga valores numéricos.
*/
function getLimiteSuperior(listaDatos)
{
    lim=listaDatos[0];
    for(var i=0;i<listaDatos.length;i++)
    {
        if(listaDatos[i]>lim)
        {
            lim=listaDatos[i];
        }
    }
    return lim;
}
