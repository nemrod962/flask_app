function flaskToArray(lista)
{
    console.log("Antes: " + lista)
    console.log("tipo: " + typeof lista)
    console.log("primer elem: " + lista[0])

    lista = String(lista)
    //quito espacios y corchetes
    lista = lista.replace(/,/g,'_')
    lista = lista.replace(/ /g,'')
    lista = lista.replace(/\[/g,'')
    lista = lista.replace(/\]/g,'')
    
    console.log("despues: " + lista)
    console.log('tipo lista: ' + typeof lista)
    //Convierto en lista
    var lista2 = lista.split("_")

    console.log("despues 2: " + lista2)
    console.log("tipo 2: " + typeof lista2)
    console.log("primer elem: " + lista2[0])

    //Intento parsear a float
    for(i in lista2)
    {
        var temp = parseFloat(lista2[i])
        if(!isNaN(temp))
        {
            lista2[i]=temp
        }
    }
    
    /*Comprobamos is hay fechas y parseamos*/
    if(isUnparsedDateArray(lista2))
    {
        lista2=parseDateArray(lista2)
    }

    return lista2

}
/*Comprobamos si la lista recibida contiene fechas con el
formato u&#39;<fechaMS>&#39;.
Se comprueba solo el formato del primer elemento.*/
function isUnparsedDateArray(lista)
{
    //El tipo de los elementos de lista
    //puede ser 'number' ya que se han
    //parseado rpeviamente.
    var tempStr = String(lista[i])
    var tempLst = tempStr.split(";")
    //Si hay tres campos al dividirlo por ';'
    //lo más probable es que el campo tenga el
    //formato que queremos parsear ('u&#39;1524245391353&#39;')
    //
    //tempLst = Array [ "u&#39", "1524245391353&#39", "" ]
    if(tempLst.length == 3)
    {   
        return true;
    }
    return false;

}
/*u&#39;1524245391353&#39; -> 1524245391353.
La lista recibida ya es un array pues se ha 
parseado con flaskToArray().
Se devuelve el resultado de parsear las fechas
en las listas.
Si no hay fehcas, se devolverá la lista intacta.*/
function parseDateArray(lista)
{
    for(i in lista)
    {
        //El tipo de los elementos de lista
        //puede ser 'number' ya que se han
        //parseado rpeviamente.
        var tempStr = String(lista[i])
        var tempLst = tempStr.split(";")
        //Si hay tres campos al dividirlo por ';'
        //lo más probable es que el campo tenga el
        //formato que queremos parsear ('u&#39;1524245391353&#39;')
        //
        //tempLst = Array [ "u&#39", "1524245391353&#39", "" ]
        if(tempLst.length == 3)
        {   
            //tempLst[1] = "1524245391353&#39"
            var tempVal = parseFloat(tempLst[1])
            if (!isNaN(tempVal))
            {
                lista[i] = parseFloat(tempVal)
            }
        }
    }

    return lista
}

/*Dada una lista que contenga fechas ya parseadas,
devuelve otra lista con esas fechas en formato datetime*/
function parseDateArrayToDatetime(lista)
{
    var listaDT = [];
    for(i in lista)
    {
        var date = new Date(lista[i]);
        listaDT[i] = date.toLocaleString();
    }
    return listaDT;
}

/*Recibe como parametro un elemento (div) dentro
del cual se generará la tablas HTML.
-> La variable listaCabeceras contendrá una lista con el
nombre de las difentes columnas.
-> La variable listaListas contendrá una lista de los diferentes
arrays en los que estan contenidos los datos a mostrar. DEBEN ESTAR
ORDENADOS EN EL MISMO ORDEN QUE EN LISTA CABECERAS.

Por ejemplo:
si listaCabeceras = ['nombre', 'dni']
entonces listaListas = [ listaNombres, listaDnis].

si listaListas = [ listaDnis, listaNombres], los nombres 
se mostrarán en la columna de los DNIs y viceversa.
*/
function crearTabla(elem, listaCabeceras, listaListas) {
    
    /*
    var temp = new Array(listaListas[0]);
    temp = flaskToArray(temp);
    console.log("DENTRO - ARRAY: " + temp);
    console.log("DENTRO - ARRAY - tipo: " + typeof temp);
    for(k in temp)
    {
        console.log("DENTRO: " + temp[k]);
    }
    */

    /*
    //Convertir listas a listas de verdad
    listaCabeceras = flaskToArray(listaCabeceras)
    for(indice in listaListas)
    {
        listaListas[indice] = flaskToArray(listaListas[indice])
    }

    console.log('tras conversion: ')
    console.log('CAB: ' + listaCabeceras)
    console.log('primer elem: ' + listaCabeceras[0])
    for(indice in listaListas)
    {
        console.log('DATOS[' +indice+']: ' + listaListas[indice])
        console.log('primer elem: ' + listaListas[indice][0])
    }
    */

    /*Creo tabla*/
    var tabla = document.createElement('TABLE');

    //Borde de la tabla
    tabla.border='1';
    //Cuerpo tabla
    var cuerpoTabla = document.createElement('TBODY');
    //Añado cuerpo a la tabla
    tabla.appendChild(cuerpoTabla)

    //Cabeceras -> listaCabeceras

    //Cojo la longitud de la primera lista en 
    //listaListas. Añado una fila por cada uno 
    //de los valores que tiene.

    //Empiezo en -1, ya que cuando i==-1 en lugar
    //de añadir una fila añadiré las cabeceras
    var numFilas = listaListas[0].length
    for(var i=-1;i<numFilas;i++)
    {
        //console.log('i' + i);
        //Creo fila generica a añadir a la tabla
        var fila = document.createElement('TR')
        cuerpoTabla.appendChild(fila)
        
        //En la primera iteración añado las cabeceras a la tabla.
        if(i == -1)
        {
            for(j in listaCabeceras)
            {
                //Creo objecto celda
                var celda = document.createElement('TH');
                //Creo contenido de la celda
                celda.appendChild(document.createTextNode(listaCabeceras[j]));
                //añado celda a la lista
                fila.appendChild(celda)
            }
        }
        //Si no es la primera iteración, añado datos
        else
        {
            for(j in listaListas)
            {
                //Creo objecto celda
                var celda = document.createElement('TD');
                //Creo contenido de la celda
                //listaListas[j] - lista j en listaListas
                //listaLista[j][i] - elemento i de la lista j en listaListas
                celda.appendChild(document.createTextNode(listaListas[j][i]));
                //añado celda a la lista
                fila.appendChild(celda)
            }
        }
    }
    //Finalmente, añado la tabla creada al elemento
    //recibido como parámetro
    elem.appendChild(tabla);
    //console.log('fin - ' + elem.innerHTML);

    //devolvemos tabla
    return tabla
}

//---------------------------------------------------------------------------
function crearTablaRandom(elem, listaCabeceras, listaListas)
{
    //Dar formato a las "listas" recibidas
    listaCabeceras = flaskToArray(listaCabeceras)
    for(indice in listaListas)
    {
        listaListas[indice] = flaskToArray(listaListas[indice])
    }

    //DEBUG
    console.log('tras conversion: ')
    console.log('CAB: ' + listaCabeceras)
    console.log('primer elem: ' + listaCabeceras[0])
    for(indice in listaListas)
    {
        console.log('DATOS[' +indice+']: ' + listaListas[indice])
        console.log('primer elem: ' + listaListas[indice][0])
    }
    
    //Crear lista con las fechas en formato
    var listaFechaFormato = [];
    if(typeof listaDatos[1][0] == 'number')
    {
        listaFechaFormato = parseDateArrayToDatetime(listaDatos[1]);
        console.log('fechFOrmato: ' + listaFechaFormato);
        listaCabeceras.push("fecha formato");
        listaDatos.push(listaFechaFormato);
    }

    crearTabla(elem, listaCabeceras, listaDatos)

}
