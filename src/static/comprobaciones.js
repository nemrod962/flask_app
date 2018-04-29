
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
    //Qué hacer con la respuesta
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

/*Enviar unbral en changeUmbral.html.
Interpreta los valores devueltos por comprobarUmbral() y muestra
avisos por pantalla.
Si está todo bien, enviará los datos al servidor.*/
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
        enviarPost("umbral",n,window.location.href)
    }
}


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
        //Si lo recibido es una url, redirigimos
        if(resp.charAt(0) == '/')
        {
            window.location.href=resp
        }
    };
    //Muy importante poner 'umbral=', ya que el mensaje sera interpretado por
    //el servidor como un form, el cual debe tener la estructura de
    //variable=valor
    //MUY IMPORTANTE UTILIZAR '&' PARA CONCATENAR VALORES!
    mensaje.send('username='+name+"&"+'password='+pass+"&"+'umbral='+umbral);
    console.log('mensaje enviado');

}
console.log("fin comprobaciones")
//-----------------------------------------------------
    
    

