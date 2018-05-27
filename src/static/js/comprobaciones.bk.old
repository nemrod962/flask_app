
console.log("inicio comprobaciones")
/*Comprobaciones generales. Aplicables en diferentes lugares*/

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

/*Comprueba el valor del umbral dado.
Intentará obtener un número del argumento que se le pasa.
Los valores 101 y 102 son utilizados en la función enviarUmbral()
de forma que se avise al usuario del error cometido.*/
function comprobarUmbral(umb)
{

    //console.log("func - comprobarUmbral");
    //Convierto a float
    if(typeof umb != "number")
    {
        console.log("Umbral NO es number! Convirtiendo...")
        //Sustituyo , por .
        umb=umb.replace(/,/g,'.')
        //Convierto en número
        umb=parseFloat(umb)
        console.log("CONVERTIDO: " + umb)
    }

    //Si no se ha introducido un numero, umb = NaN (Not a Number)
    //En sese caso, le pondremos el valor por defecto 101
    if(isNaN(umb))
    {
        umb=101
    }
    //Los valores del umbral deben estar comprendidos entre -100 y 100
    else if(umb > 100 || umb < -100)
    {
        umb=102
    }
    return umb;
}

//Hacer petición post del campo 'nombre' con el valor 'valor' a 
//la dirección 'direccion'.
//Sólo utilizable cuando enviamos un solo dato.
function enviarPost(nombre, valor, direccion)
{
    console.log("func - enviarPost");
    //Una vez aqui deberiamos tener un numero en umb
    //Peticion a enviar al servidor con los datos
    var mensaje = new XMLHttpRequest();
    console.log("DIRECCION: " + direccion)
    mensaje.open('POST', direccion);
    //mensaje.open('POST', 'http://dominioppr.com:5000/cambiarUmbral');
    mensaje.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    //mensaje.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	mensaje.onload = function() {
        //respuesta servidor
        resp = mensaje.responseText;
        console.log('RESPONSE FROM SERVER: ' + resp);
        //Si lo recibido es una url, redirigimos
        if(resp.charAt(0) == '/')
        {
            window.location.href=resp
        }
    };
    //Muy importante poner 'umbral=', ya que el mensaje sera interpretado por
    //el servidor como un form, el cual debe tener la estructura de
    //variable=valor
    mensaje.send(nombre + '=' + valor);
    console.log('mensaje enviado');
}


/*Funciones específicas. Funciones específicas para determinadas páginas*/

/*

CAMBIAR UMBRAL

*/

function postUmbral(valor, direccion)
{
    console.log("func - enviarPost");
    //Una vez aqui deberiamos tener un numero en umb
    //Peticion a enviar al servidor con los datos
    var mensaje = new XMLHttpRequest();
    console.log("DIRECCION: " + direccion)
    mensaje.open('POST', direccion);
    //mensaje.open('POST', 'http://dominioppr.com:5000/cambiarUmbral');
    mensaje.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    //mensaje.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	mensaje.onload = function() {
        //respuesta servidor
        resp = mensaje.responseText;
        console.log('RESPONSE FROM SERVER: ' + resp);
        //Interpreto codigo obtenido del server.
        //La respuesta tiene el siguiente formato:
        //UMB:<codigo>
        var codigo = resp.split(":")[1]
        codigo=parseFloat(codigo)
        //interpretamos mensaje
        codigomsg=obtenerMensajeAlertaUmbral(codigo)
        window.alert(codigomsg)
        //Si lo recibido esta entre -100 y 101, la
        //asignacion de umbral es valida. Redirigmos
        //al menu principal
        if(codigo >= -100 && codigo <= 101)
        {
            console.log('redirigir: ' + "/" )
            window.location.href='/'
        }
    };
    //Muy importante poner 'umbral=', ya que el mensaje sera interpretado por
    //el servidor como un form, el cual debe tener la estructura de
    //variable=valor
    mensaje.send('umbral=' + valor);
    console.log('mensaje enviado');
}
/*Enviar unbral en changeUmbral.html.
Interpreta los valores devueltos por comprobarUmbral() y muestra
avisos por pantalla.
Si está todo bien, enviará los datos al servidor con postUmbral().*/
function enviarUmbral(n)
{
    console.log("func - enviarUmbral");
    n=comprobarUmbral(n);
    console.log("func - enviarUmbral: n = " + n);
    if(n==101)
    {
        window.alert("Introduce un número válido!")
    }
    else if(n==102)
    {
        window.alert("El valor debe estar comprendido entre -100 y 100")
    }
    else
    {
        postUmbral(n,window.location.href)
    }
}

/*  
Dado el número de retorno obtenido de la funcion
crear getUmbral() del servidor, mostramos mensaje al cliente.
    Codigos:
        #-> -100 a 101 : Asignación umbral válida. Todo bien.
        #-> 102: El usuario es 'None'. Es el valor que se obtiene cuando no se
        ha iniciado sesión o la sesión ha caducado.
        #-> 103: Indica que el nombre de usuario recibido no es válido, ya sea
        por tipo (no string) o longitud.
        #-> 104: El usuario indicado no se ha encontrado en la base de datos.
        #-> 105: No se ha iniciado sesión.
*/
function obtenerMensajeAlertaUmbral(n)
{
    var msg=0
    //n recibido es String
    n=parseFloat(n)
    switch(n)
    {
        case 102:
            msg="No ha iniciado sesión o su sesión ha caducado."
            msg+=" Por favor, inicie sesión."
            break;
        case 103:
            msg="El nombre de usuario recibido no es válido."
            break;
        case 104:
            msg="El usuario indicado no se ha encontrado en la base de datos."
            break;
        case 105:
            msg="No se ha iniciado sesión."
            break;
        default:
            msg="El umbral se ha cambiado satisfactoriamente."
            break;
    }
    return msg
}
/*

REGISTRO

*/

/*Comprobación específica para la página del registro (register.html).
Comprueba todos los campos.
Si están todos bien, llama a la función enviarRegistro() para
enviar datos al servidor.*/
function comprobarRegistro(name,pass,passRep,umbral)
{
    res1=comprobarNombre(name);
    if(res1==1)
    {
        window.alert("El nombre de usuario debe ser de al menos 4 carácteres de longitud");

    }
    else if(res1==2)
    {
        window.alert("El nombre de usuario contiene carácteres especiales")

    }

    res2=comprobarContrasena(pass,passRep);
    if(res2==1)
    {
        window.alert("La contraseña debe ser de al menos 4 carácteres de longitud");
    }
    else if(res2==2)
    {
        window.alert('Las contraseñas NO coinciden!');
    }
    
    res3=comprobarUmbral(umbral);
    //Actualizo umbral, ya que comprobarUmbral() parsea
    //el umbral.P.ej: 12,12 -> 12.12
    umbral=res3
    if(res3==101)
    {
        window.alert("Introduce un número válido como umbral.")
    }
    else if(res3==102)
    {
        window.alert("El umbral debe estar comprendido entre -100 y 100.")
    }

    if(res1==0 && res2==0 && res3<=100)
    {
        console.log('Enviar Campos...')
        enviarRegistro(name,pass,umbral)
    }
}

function enviarRegistro(name,pass,umbral)
{
    console.log("func - enviarRegistro");
    //Una vez aqui deberiamos tener un numero en umb
    //Peticion a enviar al servidor con los datos
    var mensaje = new XMLHttpRequest();
    //De momento, lo envio a la misma ruta en la que estoy.
    direccion=window.location.href
    //DEBUG
    console.log("DIRECCION: " + direccion)
    mensaje.open('POST', direccion);
    //mensaje.open('POST', 'http://dominioppr.com:5000/cambiarUmbral');
    mensaje.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    //mensaje.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    //Qué hacer con la respuesta
	mensaje.onload = function() {
        //respuesta servidor
        resp = mensaje.responseText;
        console.log('RESPONSE FROM SERVER: ' + resp);
        //El formato con el que se recibe es:
        //<indicadorOperacion>,<urlRedirección>
        /*Indicador Operacion:
		#->  0 : Creación de usuario correcta
        #-> -1 : tipos de argumentos no válidos
        #-> -2 : tipo de umbral no válido
        #-> -3 : la longitud del usuario y la contraseña
        #no son superiores a 4 caracteres.
        #-> -4 : El nombre 'None' no está permitido.
        #-> -5 : El nombre de usuario ya existe.
        #-> -6 : No hay conexion con mongoDb
        */

        //Primero, separo ambos
        var vectorResp=resp.split(",")
        //obtengo mensaje de resultado de operacion y lo muestro
        var msg=obtenerMensajeAlertaRegistro(vectorResp[0]);
        window.alert(msg);
        //Si el indicador de operacion es 0, redirijo a
        //la url indicada en la respuesta
        if(parseInt(vectorResp[0]) == 0)
        {
            window.location.href=vectorResp[1];
        }
    };
    //Muy importante poner 'umbral=', ya que el mensaje sera interpretado por
    //el servidor como un form, el cual debe tener la estructura de
    //variable=valor
    //MUY IMPORTANTE UTILIZAR '&' PARA CONCATENAR VALORES!
    mensaje.send('username='+name+"&"+'password='+pass+"&"+'umbral='+umbral);
    console.log('mensaje enviado');

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
function obtenerMensajeAlertaRegistro(n)
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
    return msg
}
console.log("fin comprobaciones")
//-----------------------------------------------------
    
    

