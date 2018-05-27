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
    return codigo==1;
}

function mostrarMensajeLogin(codigo)
{
    if(codigo!=1)
    {
        window.alert("Credenciales aportadas no válidas");
    }
}
