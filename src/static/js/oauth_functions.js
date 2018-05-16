//Funcion para el signin de Google. 
//Es ejecutada cuando se pulsa el boton de google del template. 
//Obtiene datos usario y envia token al servidor flask.
console.log('inicio script jsoauth')

/*El boton de google ejecuta la funcion onSignIn según carga, por
lo que no da tiempo al usuario a pulsar el boton.
Empleamos la variable 'espera' de forma que la primera vez
que se ejecute la funcion onSignIn (carga de la página) haga
logout y asi cuando se haga vlivk en el boton pida al usuario
que seleccione su cuenta.*/
var espera=true;


function onSignIn(googleUser) {
    if(espera)
    {
        signOut();
        console.log('espera');
        espera=false;
    }
    else
    {

        if(googleUser['g-oauth-window']){
            console.log('si');
        }else if(googleUser['error']) {
            console.log('no');
        }
        console.log('onSignIn - dentro del script')
        var profile = googleUser.getBasicProfile();
        console.log('ID: ' + profile.getId()); 
        console.log('Name: ' + profile.getName());
        console.log('Image URL: ' + profile.getImageUrl());
        console.log('Email: ' + profile.getEmail()); 
        console.log('Enviando mensaje...')
        
        var id_token = googleUser.getAuthResponse().id_token;    
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://dominioppr.com:5000/jsoauthdata/');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            //respuesta servidor
            resp = xhr.responseText;
            console.log('RESPONSE FROM SERVER: ' + resp);
            //Si lo recibido es una url, redirigimos
            if(resp.charAt(0) == '/')
            {
                window.location.href=resp
            }
        };
        xhr.send('idtoken=' + id_token);
        console.log('mensaje enviado');
    }
}

//Funcion para el log out de Google. Elimina el log in
//del usuario de forma que tenga que volver a indicar su 
//cuenta para iniciar sesion.
function signOut()
{
    googleAuth=gapi.auth2.getAuthInstance();
    console.log('success?')
    googleAuth.disconnect();
}

//Impide que se mantenga el boton iniciado de 
//forma que cuando carguemos la pagina no haga log in inmediatamente

//ERROR: gapi is not defined
//window.onbeforeunload = signOut();

/*No funcionan
window.onbeforeunload = function(e){
    console.log("onbefreunload")
    gapi.auth2.getAuthInstance().disconnect();
};

document.onload = function(e){
    window.alert("onload")
    gapi.auth2.getAuthInstance().disconnect();
};
*/
console.log('Fin script jsoauth');
