//Precisa importar las funciones del script respuestasServidor.js

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

