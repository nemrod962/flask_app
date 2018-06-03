var test = "fueraantes";
var res = "placeholder";
console.log('Antes de ejecutar la funcion.');
function myfunc()
{
    //Comentario
    console.log('SECRETO: el caballo blanco de Santiago es Blanco.');
    var test = "cadenasecreta";
    console.log('test: ' + test)
    //document.write('SOY LA FUNCION');
    //document.write('<br>');
    //document.write('PUEDES MODIFICARME EN TIEMPO DE EJECUCION!!!');
    //document.write('<br>'+test)
}

function enviarRespuestaServidor(datos, funcion=mostrarRespuesta)
{
    console.log('DEBUG: FUNC -> ' + funcion)
    var url = window.location.href;
    $.post(url,datos,funcion);
    /*
    $.post(url,datos, function(e)
    {
        console.log("YA");
        console.log(e);
    });
    */
}

function mostrarRespuesta(resp)
{
    console.log('RESPUEsTA: ');
    console.log(resp);
    console.log("var1: " + resp["var1"]);
    res=resp;
    window.alert("resp: " + JSON.stringify(resp));
}

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

test = "fueradespues";
console.log('Despues de ejecutar la funcion.');
