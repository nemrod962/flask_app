//Funcion para el signin de Google. 
//Es ejecutada cuando se pulsa el boton de google del template. 
//Obtiene datos usario y envia token al servidor flask.
console.log('antes del script')
function onSignIn(googleUser) {
    console.log('dentro del script')
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
      console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send('idtoken=' + id_token);
    console.log('mensaje enviado');
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

console.log('Fin script');
