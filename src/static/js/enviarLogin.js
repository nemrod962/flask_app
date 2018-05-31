//Envia datos a /login medianto PSOT
function enviarLogin(user, pass)
{
    //Post a la misma url
    var url = window.location.href;
    //Datos en el POST
    var datos='user='+user+"&"+'pass='+pass;
    $.post(url,datos,function(respuesta)
    {
        //respuestasServidor.js
        interpretarRespuestaServidor(
        respuesta,
        interpretarRespuestaLogin,
        mostrarMensajeLogin);
    });
}
//comprueba respuesta
function interpretarRespuestaLogin(codigo)
{
    console.log('Codigo recibido server:' + codigo);
    //codigo == 1 indica exito, 0 indica fallo en las credenciales.
    return codigo==1;
}

function mostrarMensajeLogin(codigo)
{
    if(codigo!=1)
    {
        window.alert("Credenciales aportadas no válidas");
    }
}

/*Similar a enviarLogin(), pero en vez de un boton, empleando
un formulario.

-> el form tiene un atributo que es 'action', donde se indica
a donde se debe enviar la respuesta. Emplearemos este atributo
para espcificar la direccion a la que enviaremos el post de JQuery.

->No hace falta que creemos la variable 'datos' (cadena con argumentos),
ya que podemosobtenerlos directamente con la funcion serialize().
*/
//Recibiremos unicamente la cadena identificadora para
//seleccionar el form con JQuery.

function enviarLoginForm(formSelect)
{
    $(formSelect).submit(function(e){
        //console.log($(this).serialize());//= "user=<usuario>&pass=<password>"
        $.post($(this).attr('action'),
        $(this).serialize(),
        function(respuesta)
        {
            //respuestasServidor.js
            interpretarRespuestaServidor(
            respuesta,
            interpretarRespuestaLogin,
            mostrarMensajeLogin);
        }, 'json');
        //Notice that you have to return false from the method that handles the
        //submit event, otherwise the form will be posted also.
        //return false;
        //También puede utilizarse el preventDefault().
        e.preventDefault();
    });
}
