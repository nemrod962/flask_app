/*Funciones basicas para crear tablas que emplearán otros scripts
como crearTablaNumRnd, crearTablaMedia, etc.*/
/*
    CREACION TABLAS GENERICAS
*/

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

-> Si overwrite = false, al crear una tabla se añadira como
hijo del elemento 'elem' sin afectar el resto. Por el contrario, 
si esto es true, se eliminarán todos los hijos del elemento antes
de insertar la tabla
*/
function crearTabla(elem, listaCabeceras, listaListas, overwrite=false) {

    if(overwrite){
        //ATENCION
        /*Limpio elemento que contendrá la tabla.*/
        //Elimino hijos
        while (elem.firstChild) {
            elem.removeChild(elem.firstChild);
        }
    }

    /*Creo tabla*/
    var tabla = document.createElement('TABLE');
    //Añado atributo id a la tabla para
    //poder referenciarla facilmente
    tabla.setAttribute("id", "myTable");

    //Borde de la tabla
    tabla.border='1';
    //Cuerpo tabla
    var cuerpoTabla = document.createElement('TBODY');
    cuerpoTabla.setAttribute("id", "myTableBody");
    
    //Añado cuerpo a la tabla
    tabla.appendChild(cuerpoTabla)

    //Cabeceras -> listaCabeceras

    //Cojo la longitud de la primera lista en 
    //listaListas. Añado una fila por cada uno 
    //de los valores que tiene.

    //Empiezo en -1, ya que cuando i==-1 en lugar
    //de añadir una fila añadiré las cabeceras
    var numFilas = listaListas[0].length
    
    //Si listaListas solo es una lista con datos, 
    //listaListas[0].length dará null, pues
    //listaListas[0] será un elemento (string, number...)
    //no un array. Si esto es así el siguiente bucle for
    //no se ejecutará.
    if(numFilas==null)
    {
        console.log("crearTabla() - el array de datos no contiene listas!");
        console.log("ATENCION: no se puede crear la tabla.");
        console.log("Formato de la lista de datos incorrecto.");
    }

    for(var i=-1;i<numFilas;i++)
    {
        //En la primera iteración añado las cabeceras a la tabla.
        if(i == -1)
        {
            addHeader(tabla, listaCabeceras);
        }
        //Si no es la primera iteración, añado datos
        else
        {
            addRowBottom(cuerpoTabla, listaListas, i);
        }
    }
    //Finalmente, añado la tabla creada al elemento
    //recibido como parámetro
    elem.appendChild(tabla);
    //console.log('fin - ' + elem.innerHTML);
    //devolvemos tabla
    return tabla
}

/*Añade una fila con 
las cabeceras a la tabla.*/
function addHeader(tabla, listaCabeceras)
{
    //Creo elemento <tr> en la primera fila
    //ya que serán las cabeceras
    var row = tabla.insertRow(0);
    //Por cada uno de los elementos en la lista de las cabeceras
    //añado una celda.
    for(j in listaCabeceras)
    {
        //Creo objecto celda
        var celda = document.createElement('TH');
        //Creo contenido de la celda
        celda.appendChild(document.createTextNode(listaCabeceras[j]));
        //añado celda a la fila
        row.appendChild(celda)
    }

}

/*Añade fila al final de la tabla*/
/*Funcion empleada en crearTabla()*/
/*Esta funcion es la utilizada cuando creamos
las tablas con los datos iniciales recibidos del servidor.
En estas listas recibidas del servidor primero esán los 
números más actuales. Empezamos añadiendo estos, y por
cada número en estas listas añadimos una fila para cada
uno de ellos. La tabla crece hacia abajo*/
/*Debe recibir el elemento TBODY en vez de TABLE*/
function addRowBottom(cuerpoTabla, listaListas, indice)
{
    //Creo fila generica a añadir al
    //final de la tabla
    var fila = document.createElement('TR')
    cuerpoTabla.appendChild(fila)
    /*ATENCION: Si se quiere crear una tabla
    con una sola columna, la lista con los datos
    de esta columna debe estar metida en otra 
    lista de forma que se ejecute el siguiente
    bucle. Si no, no se añadiran los datos a la
    tabla*/
    for(j in listaListas)
    {
        //Creo objecto celda
        var celda = document.createElement('TD');
        //Creo contenido de la celda
        //listaListas[j] - lista j en listaListas
        //listaLista[j][i] - elemento i de la lista j en listaListas
        celda.appendChild(document.createTextNode(listaListas[j][indice]));
        //añado celda a la lista
        fila.appendChild(celda)
    }
}

/*Añade fila al inicio de la tabla*/
/*Esta funcion es la utilizada para actualizar la tabla
con los datos recibidos del SSE*/
/*Añado una fila con los elementos en el indice especificado
de cada una de las filas en listaListas*/
/*
L1  L2  L3
1   1   1
2   2   2 <- indice = 1
3   3   3

Creo fila: 2    2   2
*/
function addRowTop(tabla, listaListas, indice)
{
    // Create an empty <tr> element and add it to the 2st (under headers) position of the table:
    // Index begins in 0.
    var fila = tabla.insertRow(1);
    /*ATENCION: Si se quiere crear una tabla
    con una sola columna, la lista con los datos
    de esta columna debe estar metida en otra 
    lista de forma que se ejecute el siguiente
    bucle. Si no, no se añadiran los datos a la
    tabla*/
    for(j in listaListas)
    {
        //Creo objecto celda
        var celda = document.createElement('TD');
        //Creo contenido de la celda
        //listaListas[j] - lista j en listaListas
        //listaLista[j][i] - elemento i de la lista j en listaListas
        celda.appendChild(document.createTextNode(listaListas[j][indice]));
        //añado celda a la lista
        fila.appendChild(celda)
    }
}

/*Añade fila al inicio de la tabla*/
/*Esta funcion es la utilizada para actualizar la tabla
con los datos recibidos del SSE*/
/*Añado una fila con los elementos en el indice especificado
de cada una de las filas en listaListas*/
/*Similar a la funcion anterior pero recibe una lista
con los datos, en vez de una lista de listas, por lo
que el indice ya no es necesario*/
/*
lista = [2,2,2]
Creo fila: 2    2   2
*/
function addSingleRowTop(tabla, listaDatos)
{
    // Create an empty <tr> element and add it to the 2st (under headers) position of the table:
    // Index begins in 0.
    var fila = tabla.insertRow(1);
    for(j in listaDatos)
    {
        //Creo objecto celda
        var celda = document.createElement('TD');
        //Creo contenido de la celda
        //listaListas[j] - lista j en listaListas
        //listaLista[j][i] - elemento i de la lista j en listaListas
        celda.appendChild(document.createTextNode(listaDatos[j]));
        //añado celda a la lista
        fila.appendChild(celda)
    }
}

function testAddRow()
{
    var table = document.getElementById("myTable");
    // Create an empty <tr> element and add it to the 2st (under headers) position of the table:
    var row = table.insertRow(1);

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new"
    // <tr> element:
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);

    // Add some text to the new cells:
    cell1.innerHTML = "NEW CELL1";
    cell2.innerHTML = "NEW CELL2"; 
}


