/*Convierte las listas recibidas del servidor (las
cuales son interpretadas como strings) a listas 
reconocidas por javascript para trabajar con ellas.*/
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
        //var date = new Date(lista[i]);
        //listaDT[i] = date.toLocaleString();
        listaDT[i] = dateToDatetime(lista[i])
    }
    return listaDT;
}

/*Pasa una fecha de ms a formato datetime*/
function dateToDatetime(fechams)
{
    //Parseo a float porque si no no funciona
    fechams = parseFloat(fechams)
    var date = new Date(fechams);
    date = date.toLocaleString();
    return date;
}
