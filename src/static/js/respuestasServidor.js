/*Contiene funciones para interpretar las respuestas recibidas
del servidor cuando estemos empleando javascript.
Tres situaciones (tipos respuesta):
-> JSON:
    Si es un json, la respuesta tendra los campos:
    {"url" : url_a_redireccionar, "code": codigo del resultado de la operacion}
    Interpretaré el código y redireccionaré a la url indicada si procede.
-> URL: 
    La respuesta es un url relativa (comienza por /. Por ejemplo: /tablas).
    Redireccioanré a la url indicada con window.location.href = url

-> Otra cosa (página html, lo más probable):
    Como estoy trabajando con javascript, lo que espero que me indique el 
    server es un código de operación (error o éxito) y/o una dirección a
    la que deberé dirigirme. Si no es ninguna de estas dos, lo más probable
    es que me esté enviando el html de la página de login porque mi sesión ha
    caducado.
    En cualquier caso, si recibo una respuesta que no es ni JSON ni una url,
    me redirigiré al menú principal. La propia aplicación me redirigirá a su vez 
    a la página de login si la sesión ha caducado.
*/

//Función que puede emplearse para DEBUG
function mostrarRespuestaServidor(resp)
{
    if(is_json(resp))
	{
        console.log("Respuesta: " + JSON.stringify(resp))
	}
    else
    {
    	console.log("Respuesta: " + resp)
    }
}

//Función más relevante. Tiene que emplearse como funcióin a utilizar como
//resultado de un POST. Por ejemplo:
//$.post(url,data,function()
//    {
//        interpretarRespuestaServidor(...);
//    }
//);
//->Comprueba si es un json y redirecciono
//->La funcion intérprete recibida indicara si el codigo recibido con la respuesta
//es valido o no. Si es valido, se empleará la url recibida para redireccionar
//al cliente.
//La funcion mensaje muestra un mensaje dependiendo del codigo recibido.
//Si es un json, la respuesta tendra los campos:
//{"url" : url_a_redireccionar, "code": codigo del resultado de la operacion}

function interpretarRespuestaServidor(resp, 
funcionInterprete=dummyFunc, funcionMensaje=dummyFunc)
{
    console.log('json? ' + is_json(resp))
    console.log('url? ' + is_url(resp))
    if(is_json(resp))
    {
        var url = resp['url'];
        var code = resp['code'];

        funcionMensaje(code)
        if(funcionInterprete)
        {   
            console.log('ACCEDER A: ' + url);
            window.location.href=url
        }
    }
    //Si no json compruebo si es una url
    else if(is_url(resp))
    {
        var url = resp;
        console.log('ACCEDER A: ' + url);
        window.location.href=url;
    }
    //La respuesta no contiene url. Redirigimos?
    //Redirigmos a la pagina principal
    else
    {
        var url = '/';
        console.log('ACCEDER A: ' + url);
        window.location.href=url;
    }

}

//Funcion empleada por defecto como funcion interprete
//y mensaje en interpretarRespuestaServidor() si no se
//especifica ninguna. Simplemente devuleve true pòr lo
//que se redirecciona al contenido del campo url del 
//JSON recibido.
function dummyFunc()
{
    return true;
}


/* Comprobacón Tipo Respuesta*/

//Devuelve 1 si el argumento es una url relativa (empleada 
//para redireccionar dentro de la propia web),
//0 en caso contrario.
function is_url(url)
{
    return url.charAt(0) == '/';
}

//No se utiliza
function is_html(html)
{
    return html.contains('<html')
}
//Devuelve 1 si el argumento es un JSON,
//0 en caso contrario
if ( typeof is_json != "function" )
function is_json( _obj )
{
    var _has_keys = 0 ;
    for( var _pr in _obj )
    {
        if ( _obj.hasOwnProperty( _pr ) && !( /^\d+$/.test( _pr ) ) )
        {
           _has_keys = 1 ;
           break ;
        }
    }

    return ( _has_keys && _obj.constructor == Object && _obj.constructor != Array ) ? 1 : 0 ;
}
