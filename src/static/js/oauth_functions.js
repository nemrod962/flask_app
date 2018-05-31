//Funcion para el signin de Google. 
//Es ejecutada cuando se pulsa el boton de google del template. 
//Obtiene datos usario y envia token al servidor flask.
console.log('inicio script jsoauth')

/*El boton de google ejecuta la funcion onSignIn según carga, por
lo que no da tiempo al usuario a pulsar el boton.
Empleamos la variable 'espera' de forma que cuando se ejecute la funcion 
onSignIn, no se produzca el login (no envia datos al servidor)
si no se ha hecho click en el botón.*/
var espera=true;

function validarSignIn() {
	console.log("Validado!");
    espera=false;
}

function onSignIn(googleUser) {
    if(espera)
    {
        signOut();
        console.log('espera');
    }
    else
    {
        console.log('onSignIn - dentro del script')
        var profile = googleUser.getBasicProfile();
        console.log('ID: ' + profile.getId()); 
        console.log('Name: ' + profile.getName());
        console.log('Image URL: ' + profile.getImageUrl());
        console.log('Email: ' + profile.getEmail()); 
        console.log('Enviando mensaje...')
        
        var id_token = googleUser.getAuthResponse().id_token;    
        var xhr = new XMLHttpRequest();
        var url = window.location.origin + '/jsoauthdata/'
        xhr.open('POST', url);
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
    googleAuth.signOut();
    googleAuth.disconnect();
}

/*Funciones para boton custom. Define el estilo
del botón.*/
function renderButton() {
      gapi.signin2.render('my-signin2', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSignIn,
        'onfailure': signOut
      });
}
console.log('Fin script jsoauth');
