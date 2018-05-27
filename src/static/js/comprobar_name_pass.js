/*comprobaciones de nombre de usuario y contraseña para el registro
de usuarios*/

/*Precisa de los scripts 
    ->comprobaciones_umbral.js:
        Comprobaciones del umbral del usuario a crear.
    ->respuestasServidor.js:
        Interpretar la respuesta recibida por el servidor.
*/

/*Comprobar nombre de usuario introducido.
Debe tener una longitud mayor de 4 caracteres 
y no puede tener caracteres especiales.*/
function comprobarNombre(name)
{
    name=String(name)
    if(name.length<4)
    {
        //Debe tener más de 4 carácteres de longitud
        return 1
    }
    else
    {
        //No se permiten caracteres especiales
        //Expresion regular con los carácteres espciales
        var spchars = /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
        //Busco cualquier caracter especial en el nombre
        var n = name.search(spchars);
        //Si n no es -1, quiere decir que hay carácteres especiales en el
        //nombre
        console.log("caracter especial encontrado en: "+ n);
        if(n!=-1)
        {
            //console.log("El nombre de usuario contiene carácteres especiales")
            return 2
        }
        else
        {
            //nombre correcto
            return 0
        }
    }
}

/*Comprobar campos constraseñas.
Debe de ser de al menos 4 caracteres de longitud.
También debe haber dos campos para introducir las contraseñas
y estas deben coincidir.*/
function comprobarContrasena(pass, passRep)
{
    pass=String(pass)
    passRep=String(passRep)
    console.log('pass: ' + pass)
    console.log('passRep: ' + passRep)
    if(pass.length<4)
    {
        //console.log("La contraseña debe ser de mas de 3 carácteres de longitud");
        return 1
    }
    if(pass==passRep)
    {
        //console.log('contraseñas coinciden!');
        return 0;
    }
    else
    {
        //console.log('contraseñas NO coinciden!');
        return 2;

    }
}


function mostrarComprobacionNombre(res1)
{
    if(res1==1)
    {
        window.alert("El nombre de usuario debe ser de al menos 4 carácteres de longitud");

    }
    else if(res1==2)
    {
        window.alert("El nombre de usuario contiene carácteres especiales")

    }
}

function mostrarComprobacionContrasenna(res2)
{
    if(res2==1)
    {
        window.alert("La contraseña debe ser de al menos 4 carácteres de longitud");
    }
    else if(res2==2)
    {
        window.alert('Las contraseñas NO coinciden!');
    }
}


//--------------------------


/*

REGISTRO

*/

/*Comprobación específica para la página del registro (register.html).
Comprueba todos los campos.
Si están todos bien, llama a la función $.post() para
enviar datos al servidor.*/
function comprobarRegistro(name,pass,passRep,umbral)
{
    res1=comprobarNombre(name);
    //muestro mensaje de resultado de comprobar nombre usuario
    mostrarComprobacionNombre(res1)

    res2=comprobarContrasena(pass,passRep);
    //muestro mensaje de resultado de comprobar contraseña
    mostrarComprobacionContrasenna(res2)
    
    res3=comprobarUmbral(umbral);
    //muestro mensaje de resultado de comprobar umbral
    mostrarComprobacionUmbral(res3)
    //Actualizo umbral, ya que comprobarUmbral() parsea
    //el umbral.P.ej: 12,12 -> 12.12
    umbral=res3

    if(res1==0 && res2==0 && res3<=100)
    {
        console.log('Enviar Campos...')
        //Datos a enviar
        datos='username='+name+"&"+'password='+pass+"&"+'umbral='+umbral;
        //Hago el post a la misma direccion en la que estoy
        url = window.location.href;
        //Envio datos al server.
        $.post(url,datos,function(e)
        {
            //respuestasServidor.js
            //mostrarRespuestaServidor(e)
            
            interpretarRespuestaServidor(e,
            interpretarRespuestaRegistro,
            mostrarMensajeRegistro);
            
            
        }      
        );
    }
}


//Funciones para interpretacion de la respuesta del server.
//Requeridos por la funcion interpretarRespuestaServidor()
//en respuestasServidor.js

/*  
Dado el número de retorno obtenido de la funcion
crear usuario del servidor, indicamos si el proceso
de crear el usuario se ha realizado con éxito.
    Codigos:
        #-> -1 : tipos de argumentos no válidos
        #-> -2 : tipo de umbral no válido
        #-> -3 : la longitud del usuario y la contraseña
        #no son superiores a 4 caracteres.
        #-> -4 : El nombre 'None' no está permitido.
        #-> -5 : El nombre de usuario ya existe.
        #-> -6 : No hay conexion con mongoDb
*/
function interpretarRespuestaRegistro(n)
{
    //n recibido es String
    n=parseInt(n)
    pasar=false;
    switch(n)
    {
        case 0:
            //msg="El usuario se ha creado satisfactoriamente."
            pasar = true;
            break;
        case -1:
            //msg="Tipos de datos de Usuario y/o contraseña no validos."
            break;
        case -2:
            //msg="tipo de dato de umbral no válido."
            break;
        case -3:
            //msg="la longitud del usuario y la contraseña no son superiores a 4 caracteres."
            break;
        case -4:
            //msg= "El nombre 'None' no está permitido."
            break;
        case -5:
            //msg= "El nombre de usuario ya existe."
            break;
        case -6:
            //msg= "No hay conexion con mongoDB."
            break;
    }
    console.log("DEBERIA PASAR: " + pasar);
    return pasar;
}


/*  
Dado el número de retorno obtenido de la funcion
crear usuario del servidor, mostramos mensaje al cliente.
    Codigos:
        #-> -1 : tipos de argumentos no válidos
        #-> -2 : tipo de umbral no válido
        #-> -3 : la longitud del usuario y la contraseña
        #no son superiores a 4 caracteres.
        #-> -4 : El nombre 'None' no está permitido.
        #-> -5 : El nombre de usuario ya existe.
        #-> -6 : No hay conexion con mongoDb
*/
function mostrarMensajeRegistro(n)
{
    var msg="placeholder"
    //n recibido es String
    n=parseInt(n)
    switch(n)
    {
        case 0:
            msg="El usuario se ha creado satisfactoriamente."
            break;
        case -1:
            msg="Tipos de datos de Usuario y/o contraseña no validos."
            break;
        case -2:
            msg="tipo de dato de umbral no válido."
            break;
        case -3:
            msg="la longitud del usuario y la contraseña no son superiores a 4 caracteres."
            break;
        case -4:
            msg= "El nombre 'None' no está permitido."
            break;
        case -5:
            msg= "El nombre de usuario ya existe."
            break;
        case -6:
            msg= "No hay conexion con mongoDB."
            break;
    }
    window.alert(msg)
    return msg
}

