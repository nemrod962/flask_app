
console.log("inicio comprobaciones")

function comprobarUmbral(umb)
{

    console.log("func - comprobarUmbral");
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
    if(umb > 100 || umb < -100)
    {
        umb=102
    }
    return umb;
}

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

console.log("fin comprobaciones")
