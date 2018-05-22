/*Obtiene el atributo 'value' del botón que se ha pulsado.
Este valor contendrá la opción seleccionada, que será interpretada
por el servidor, el cual devolverá una url en la se podrá
acceder a la funcionalidad indicada por la función.*/

/*Es necesario que los botones del template sean de la clase
botonMenu para que se mande al servidor su valor cuando
se pulsen.*/

function enviarOpcionBotones()
{
    //Envío petición POST a flask mediante jQuery.
    $('.botonMenu').map(function()
    {
 		$(this).click(function()
        {
            var opcion = $(this).attr('value');
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
            console.log('param: ' + datosEnviar);
            //Enviamos POST
            //url actual
            var url = window.location.href;
			$.post(url, datosEnviar, function(e)
            {
                console.log(' resp. server: ' + e)
                window.location=e;
            });
        });
    });
}
