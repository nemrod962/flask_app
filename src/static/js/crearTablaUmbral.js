/*
 - elem es el elemento html donde insertaremos la tabla creada. 
 Típicamente será un <div>.
 - lista datos es una lista que contiene varias listas con los
datos a tratar.*/

//VARIABLES GLOBALES
//Lista con datos globales para poder actualizar
//mediante SSE.
//Tras inicializarse, tendrá la siguiente estructura
//listaDatos = [ listaNumeros, listaFechasMS, listaFecha]
var listaGlobalDatos = [];
//lista global con las cabeceras a utilizar
var listaCabeceras=["Umbral","Último Numero Superior",
"Fecha Obtención Núm. Superior","Último Numero Inferior",
"Fecha Obtención Núm. Inferior"];
//umbral, de forma que lo tengo disponible en la funcion SSE
var umbralGlobal;

function crearTablaUmbral(elem, listasDatos, umbral)
{
    //TRATAMIENTO ARGUMENTOS RECIBIDOS
    
    //No hace falta parsearlo, pues se parsea
    //en las funciones getResUmbralSuperior() y
    //getResUmbralInferior().
    //umbral=parseFloat(umbral);

    //Compruebo si umbral es un numero
    if(isNaN(umbral))
    {
        window.alert("El umbral introducido: " + umbral + " NO es válido.");
        window.alert("Cambiando a valor por defecto: 50");
        umbral=50;
    }

    //Guardo umbral en variable global para tenerlo disponible en 
    //la funcion SSE
    umbralGlobal = umbral;

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
    //listaDatos[1] = listaFechasMS

    //Crear lista con las fechas en formato
    //listaDatos = [ listaNumeros, listaFechasMS]
    //listaDatos[1] = listaFechasMS
    var listaFechaFormato = [];
    if(typeof listasDatos[1][0] == 'number')
    {
        listaFechaFormato = parseDateArrayToDatetime(listaDatos[1]);
        console.log('fechFOrmato: ' + listaFechaFormato);
        listasDatos.push(listaFechaFormato);
    }
    
    //Para crear la tabla necesito el elem, listaCabeceras
    //y listaDatos.
    listaResultados=getResUmbral(listasDatos, umbral);
    //listaCabeceras=["Umbral","Numero Superior","Fecha Obtención Núm. Superior","Numero Inferior","Fecha Obtención Núm. Inferior"];

    //creo tabla
    crearTabla(elem,listaCabeceras,listaResultados);

    //Actualizo variable global si esta vacia con la lista de los datos
    if(listaGlobalDatos.length == 0)
    {
        listaGlobalDatos = listaDatos;
    }
}

/*Realiza la operación umbral con los datos recibidos y genera los datos de
respuesta.

listasDatos = [listaNumeros, listaFechasMS, listaFechasFormato].

A su vez, esta función emplea las funciones getResUmbralSuperior() y 
getResUmbralInferior para obtener el resultado de buscar los numeros
superiores e inferiores al umbral más recientes.

La función devolverá una lista con los datos del resultado de ralizar la
función umbral. Esta lista con los resultados estará formateada de forma
que se puede emeplear con la función crearTabla().*/
function getResUmbral(listasDatos, umbral)
{
    console.log('- getResUmbral()');
    /*
    for(var index=0;index<listasDatos.length;index++)
        console.log('listas (1 elem): ' + listasDatos[index][0])
    */
    //Avisos
    var longNumeros=listasDatos[0].length
    var longFechas=listasDatos[1].length
    if(longNumeros==0)
    {
        console.log('Lista números vacía!');
    }
    if(longNumeros != longFechas)
    {   
        console.log('Listas de diferente longitud!');
    }

    //umbral superior
    listaUmbSup = getResUmbralSuperior(listaDatos, umbral);

    //umbral inferior
    listaUmbInf = getResUmbralInferior(listaDatos, umbral);

    //ensamblar ambos resultados
    listaUmb = []
    //Añado umbral.
    //meto un array de longitud 1 con
    //el dato como unico elemento, ya que la
    //funcion crearTabla recibe una lista de
    //listas con los datos.
    //Esto lo hago de forma que listaUmb
    //sea una lista de listas, cada una conteniendo
    //un único elemento.
    listaUmb.push([umbral])
    //Añado resultado superior
    for(var i=0;i<listaUmbSup.length;i++)
    {
        //No añado la fecha en ms
        if(i!=1)
        {
            listaUmb.push([listaUmbSup[i]])
        }
    }
    //añado resultado inferior
    for(var i=0;i<listaUmbInf.length;i++)
    {
        //No añado la fecha en ms
        if(i!=1)
        {
            listaUmb.push([listaUmbInf[i]])
        }
    }

    console.log('listaFinal: ' + listaUmb)
    //listaumb contiene los datos a mostrar en la tabla
    return listaUmb;
}

/*Función que busca el número aleatorio añadido superior al umbral
más recientemente.

El formato de la lista resultado es el siguiente:
listaResultado = [numeroSuperior, fechaObtencionMs, fechaObtencion]*/
function getResUmbralSuperior(listasDatos, umbral)
{
    //Umbral Superior
    var longNumeros=listasDatos[0].length
    var longFechas=listasDatos[1].length
    //variable con número superior al umbral especificado
    var resNumSup = parseFloat(umbral);
    //variable con la fecha de obtención del
    //número superior al umbral indicado por 
    //la variable anterior.
    var resDateSup = 0;
    var resDateSupFormat = "placeholder";
    //Indica se se ha encontrado un resultado.
    //Si por ejemplo se especifica como umbral
    //500, no se va a encontrar ningún resultado.
    //Si no se encuentra ningún resultado, deberá
    //indicarse.
    var resFound=false;
    //DEBUG
    console.log('longitud listas: ');
    console.log('numeros: ' + longNumeros);
    console.log('fechas: ' + longFechas);
    //Recorremos lista de los números aleatorios
    for(var index=0;index<longNumeros;index++)
    {
        //Si el numero es mayor que el umbral
        //sera cnadidato
        if(listasDatos[0][index]>umbral)
        {
            //El candidato será el nuevo
            //resultado si su fecha de obtención
            //es más reciente que la del resultado
            //actual.
            if(listasDatos[1][index]>resDateSup)
            {
                //El candidato pasa a ser el
                //nuevo resultado
                resNumSup=listasDatos[0][index]
                resDateSup=listasDatos[1][index]
                resDateSupFormat=listasDatos[2][index]
                //He encontrado al menos un resultado
                resFound=true;
            }
        }
    }

    //Si no se ha encontrado ningun resultado, 
    //lo indico.
    if(!resFound)
    {
        resNumSup=" - "
        resDateSup=" - "
        resDateSupFormat=" - "
    }

    console.log("Umbral Superior:");
    console.log("Numero: " + resNumSup);
    console.log("Fecha: " + resDateSup);
    console.log("Fecha: " + resDateSupFormat);
    
    //Ensamblamos resultado
    listaResultado=[resNumSup, resDateSup, resDateSupFormat];
    return listaResultado;
}

/*Función que busca el número aleatorio añadido inferior al umbral
más recientemente.

El formato de la lista resultado es el siguiente:
listaResultado = [numeroInferior, fechaObtencionMs, fechaObtencion]*/
function getResUmbralInferior(listasDatos, umbral)
{
    //Umbral Inferior
    var longNumeros=listasDatos[0].length
    var longFechas=listasDatos[1].length
    //variable con número superior al umbral especificado
    var resNumInf = parseFloat(umbral);
    //variable con la fecha de obtención del
    //número superior al umbral indicado por 
    //la variable anterior.
    var resDateInf = 0;
    var resDateInfFormat = "placeholder";
    //Indica se se ha encontrado un resultado.
    //Si por ejemplo se especifica como umbral
    //500, no se va a encontrar ningún resultado.
    //Si no se encuentra ningún resultado, deberá
    //indicarse.
    var resFound=false;
    //DEBUG
    console.log('longitud listas: ');
    console.log('numeros: ' + longNumeros);
    console.log('fechas: ' + longFechas);
    //Recorremos lista de los números aleatorios
    for(var index=0;index<longNumeros;index++)
    {
        //Si el numero es mayor que el umbral
        //sera cnadidato
        if(listasDatos[0][index]<umbral)
        {
            //El candidato será el nuevo
            //resultado si su fecha de obtención
            //es más reciente que la del resultado
            //actual.
            if(listasDatos[1][index]>resDateInf)
            {
                //El candidato pasa a ser el
                //nuevo resultado
                resNumInf=listasDatos[0][index]
                resDateInf=listasDatos[1][index]
                resDateInfFormat=listasDatos[2][index]
                //He encontrado al menos un resultado
                resFound=true;
            }
        }
    }

    //Si no se ha encontrado ningun resultado, 
    //lo indico.
    if(!resFound)
    {
        resNumInf=" - "
        resDateInf=" - "
        resDateInfFormat=" - "
    }
    console.log("Umbral Inferior:");
    console.log("Numero: " + resNumInf);
    console.log("Fecha: " + resDateInf);
    console.log("Fecha: " + resDateInfFormat);

    //Ensamblo resultado
    listaResultado = [resNumInf, resDateInf, resDateInfFormat];
    return listaResultado;
}

//-----------------------------------------------------------------------------
////SSE
/*Funcion a llamar cuando se reciba un SSE para añadir
fila con los datos*/
//Se emplean funciones de evaluarUmbralSSE.js, arrayOps y tableOps.js
function updateTableUmbralSSE(datosSSE, divTabla)
{
    //Solo actualizo si el numero registrado esta disponible en
    //la base de datos que esta empleando el usuario
    if(estaNumeroDisponibleSSE(datosSSE))
    {
        //Parseo datos SSE
        var num = getNumeroAleatorioSSE(datosSSE);
        //fechams
        var fechams = getFechaSSE(datosSSE);
        //fecha datetime
        var fecha = dateToDatetime(fechams);

        //actualizar datos globales	
        //listaGlobalDatos = [listaNumeros, listaFechasMS, listaFechasFormato].
        //añado numero
        listaGlobalDatos[0].push(num);
        //añado fecha ms
        listaGlobalDatos[1].push(fechams);
        //añado fecha datetime
        listaGlobalDatos[2].push(fecha);

        //actualizo tabla
        var listaResultados=getResUmbral(listaGlobalDatos, umbralGlobal);
        crearTabla(divTabla,listaCabeceras,listaResultados,true);
    }
}

//-----------------------------------------------------------------------------
/*Preparar todo para recalcular la tabla.
    > Asigna al boton la funcion recalcular la tabla al pulsarlo.
    > Asigna al input text la funcion isNumberKey() en el
    evento onKeyPress() de forma que solo se puedan introducir numeros
    en él.*/
function prepararRecalcularTabla(divTabla, selectorUmbral, selectorBoton,
selectorForm)
{
    //Asigno funcional input en el evento onKeyPress
    soloNumeros(selectorUmbral);
    //Asigno funcion al boton
    //asignarRecalcularBoton(divTabla, selectorUmbral, selectorBoton);
    //Asigno funcion al form
    asignarRecalcularForm(divTabla, selectorUmbral, selectorForm);
}

//Actualización de la tabla.
//Ahora el umbral se especificará en la propia pantalla. Se introducirá
//en un input number y se recalculará la tabla cuando se pulse un botón al
//lado del input text.
function recalculateTableUmbral(divTabla, selectorUmbral)
{
    //Obtiene valor umbral
    //Al ser input type=number devuelve "" si su contenido
    //no es un ńumero. Tampoco admite numeros decimales
    var umbral = parseFloat($(selectorUmbral).val());
    //Sino es un número mostramos mensaje.
    if(isNaN(umbral))
    {
        window.alert("Introduce un número válido.");
    }
    //Si es un número. proseguimos.
    else
    {
        //Guardo umbral en variable global para tenerlo disponible en 
        //la funcion SSE
        umbralGlobal = umbral;
        //actualizo tabla
        var listaResultados=getResUmbral(listaGlobalDatos, umbral);
        crearTabla(divTabla,listaCabeceras,listaResultados,true);
    }
}

/*Asigna la función reculacular al botón indicado.*/
function asignarRecalcularBoton(divTabla, selectorUmbral, selectorBoton)
{
    $(selectorBoton).click(function()
    {
        recalculateTableUmbral(divTabla, selectorUmbral);
    });
}

/*Asigna la función reculcular al ahcer submit del form indicado. Alternativa 
a asignarle esta función al botón*/
function asignarRecalcularForm(divTabla, selectorUmbral, selectorForm)
{
    $(selectorForm).submit(function()
    {
        recalculateTableUmbral(divTabla, selectorUmbral);
        return false;
    });
}

/*Dado el selector de un input text, solo permite intorducir numeros.*/
function soloNumeros(selectorUmbral)
{
    $(selectorUmbral).keypress(function(evento)
    {
        return isNumberKey(evento);
    });
}

/*Funcion para asignar al evento onKeyPress de un input tag,
de forma que solo permita numeros*/
function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    //no decimals
    //if (charCode > 31 && (charCode < 48 || charCode > 57))
    //decimals
    if (charCode > 31 && (charCode != 46 &&(charCode < 48 || charCode > 57)))
        return false;
    return true;
}
