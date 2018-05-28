//Precisa importar las funciones del script respuestasServidor.js

//Actualizacionde enviarOpcionBotones.js para el nuevo menú

//LEGACY - DEPRECATED
/*Obtiene el atributo 'value' del botón que se ha pulsado.
Este valor contendrá la opción seleccionada, que será interpretada
por el servidor, el cual devolverá una url en la se podrá
acceder a la funcionalidad indicada por la función.*/

/*Es necesario que los botones del template sean de la clase
botonMenu para que se mande al servidor su valor cuando
se pulsen.*/

//Se puede recibir como argumento opcional la url
//a la que se enviará el post. Si no se recibe ninguna,
//el post se enviará a la misma url en la que se 
//está actualmente
function enviarOpcionBotones(url=window.location.href)
{
    //Asigno funciona  todos los botones
    //Envío petición POST a flask mediante jQuery.
    $('.botonMenu').each(function()
    {
 		$(this).click(function()
        {
            var datosEnviar = obtenerValorMenu($(this))
            console.log('param: ' + datosEnviar);
            //Enviamos POST
            //url actual
            //var url = window.location.href;
			$.post(url, datosEnviar, function(e)
            {
                //De static/js/respuestasServidor.js
                mostrarRespuestaServidor(e);
                interpretarRespuestaServidor(e);
                //window.location=e
            });
        });
    });
}

//LEGACY - DEPRECATED
//Obtiene los valores de la opcion seleccionada
//( $.(this) ) y los devulve con el formato 
//apropiado para enviarlos como datos de un POST.
function obtenerValorMenu(elem)
{
    //var opcion = $(this).attr('value');
    var opcion = elem.attr('value');
    var datosEnviar = 'opcion='+opcion ;
    //En caso de utilizarlo en el menu principal
    //para obtener el texto en la 
    //caja de texto del umbral
    var umbralTxt;
    if(opcion == "umbral")
    {
        umbralTxt = $('.textoMenu').val();
    }
    console.log('soy el boton:' + opcion);
    if(umbralTxt != undefined)
    {
        datosEnviar += '&umbralTxt='+umbralTxt;
        console.log('Umbral:' + umbralTxt);
    }
    return datosEnviar;
}

//NUEVOS

/*
    Envio al servidor la opción 
    representada por el boton pulsado
    mediante un POST.
    PARAMETROS:
    -> lista de botones (objetos JQuery) que contendran las opciones.
    $("button")
    -> nombre del atributo del boton que contendrá. P.ej. "value"
    la opción a enviar al servidor
    -> nombre del campo con el que se enviará el valor al 
    servidor. Por defecto es "opcion".
    -> url a la que enviar el POST. Por defecto sera la actual.
    window.location.href
*/
function enviarOpcionMenu(listaBotones, atrib, campo, url)
{
    campo="opcion";
    url = window.location.href;
    listaBotones.each(function()
    {
        $(this).click(function()
        {
            var valor = obtenerOpcion($(this), atrib);
            datosEnviar = campo + "=" + valor;
            $.post(url,datosEnviar,function(e)
            {
                //De static/js/respuestasServidor.js
                interpretarRespuestaServidor(e);
            });
        });
    });
    
}

//Obtiene los valor del atributo de el elemento 
//pulsado (boton) ( $.(this) ) y lo devulve.
function obtenerOpcion(elem, atrib)
{
    //var opcion = $(this).attr('value');
    var opcion = elem.attr(atrib);
    return opcion;
}

/*
PARA ACTUALIZAR LA DIRECCION A LA QUE REDIRIGIR DEPENDIENDO DEL UMBRAL
-> Recibe el objeto Jquery del link ($("#link_umbral")) 
del umbral y sobrescribe su comportamiento para 
que redirija a la pagina del umbral del 
numero introducido en el area de texto
-> Tambień precisa del objeto jquery del input
type text de donde obtener el umbral ($(".textoMenu")) 
-> Y la url base de la redireccion '{{url_for("blueApp.webUmbral")}}'
*/

function actualizarLinkUmbral(objLinkUmbral, objTextoUmbral, url_redirigir)
{
	/*Sobrescribo comportamiento de link_umbral para que incluya
    en la url a la que redirige el umbral introducido en el área de texto*/
    objLinkUmbral.click(function()
    {
        var url = url_redirigir;
        var txtUmbral =  objTextoUmbral.val();
        if(txtUmbral != "")
        {
            var umbral = parseFloat(txtUmbral);
            console.log("umbral:" + umbral);
            console.log("url:" + url);
            url+="/"+umbral;
        }
        console.log("url:" + url);
        //window.alert(url);
        objLinkUmbral.attr("href", url);
    });

}

