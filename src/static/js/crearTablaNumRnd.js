//Importar script con las operaciones básicas sobre arrays
/*
//Empleo jQuery
$.getScript("/static/js/arrayOps.js", function() {
   alert("Script loaded but not necessarily executed.");
   });
*/
/*
function dynamicallyLoadScript(url) {
    // Make a script DOM node
    var script = document.createElement("script");
    // Set it's src to the provided URL
    script.src = url;    
    // Add it to the end of the head section of 
    //the page (could change 'head' to 'body' to 
    //add it to the end of the body section instead)
    document.head.appendChild(script); 
}
dynamicallyLoadScript('/static/js/arrayOps.js')
*/
//No funciona ninguno de los dos. Hay que importar ambos en el template.

//---------------------------------------------------------------------------
/*
 - elem es el elemento html donde insertaremos la tabla creada. 
  Típicamente será un <div>.
 - listaCabeceras lista con las cabeceras de las tablas
 - listaListas es una lista que contiene varias listas con los
   datos a tratar.
*/

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
    //listaDatos = [ listaNumeros, listaFechasMS]
    //listaDatos[1] = listaFechasMS
    var listaFechaFormato = [];
    if(typeof listaListas[1][0] == 'number')
    {
        listaFechaFormato = parseDateArrayToDatetime(listaDatos[1]);
        console.log('fechFOrmato: ' + listaFechaFormato);
        listaCabeceras.push("fecha formato");
        listaListas.push(listaFechaFormato);
    }

    crearTabla(elem, listaCabeceras, listaListas)

}
