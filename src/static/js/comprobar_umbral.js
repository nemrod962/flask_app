/*comprobaciones del umbral del usuario a cambiar.*/

/*Precisa de los scripts 
    ->respuestasServidor.js:
        Interpretar la respuesta recibida por el servidor.
*/

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

//Muestra mensaje en caso de haber introducido
//umbral no válido.
function mostrarComprobacionUmbral(n)
{
    if(n==101)
    {
        window.alert("Introduce un número válido!")
    }
    else if(n==102)
    {
        window.alert("El valor debe estar comprendido entre -100 y 100")
    }
}

//LLAMADA DESDE EL TEMPLATE
/*Enviar unbral en changeUmbral.html.
Interpreta los valores devueltos por comprobarUmbral() y muestra
avisos por pantalla.
Si está todo bien, enviará los datos al servidor con postUmbral().*/
function enviarUmbral(n)
{
    console.log("func - enviarUmbral");
    n=comprobarUmbral(n);
    //muestro mensaje de resultado de comprobar umbral
    mostrarComprobacionUmbral(n);
    console.log("func - enviarUmbral: n = " + n);
    if(n!=101 && n!=102)
    {
        //Hago el post a la misma direccion en la que estoy
        url = window.location.href
        datos ='umbral=' + n 
        $.post(url, datos,function(e)
        {
            //respuestasServidor.js
            //mostrarRespuestaServidor(e)
            
            interpretarRespuestaServidor(e,
            interpretarRespuestaUmbral,
            mostrarMensajeUmbral);
        }
        );
    }
}

//Funciones para interpretacion de la respuesta del server.
//Requeridos por la funcion interpretarRespuestaServidor()
//en respuestasServidor.js
/*  
Dado el número de retorno obtenido de la funcion
getUmbral() del servidor, indicamos si el proceso
de cambiar el umbral se ha realizado con éxito.
    Codigos:
        #-> -100 a 101 : Asignación umbral válida. Todo bien. Devuelvo true.
        #-> 102: El usuario es 'None'. Es el valor que se obtiene cuando no se
        ha iniciado sesión o la sesión ha caducado.Devulevo false.
        #-> 103: Indica que el nombre de usuario recibido no es válido, ya sea
        por tipo (no string) o longitud. Devuelvo false.
        #-> 104: El usuario indicado no se ha encontrado en la base de datos.
        Devuelvo false.
        #-> 105: No se ha iniciado sesión. Devuelvo false.
*/
function interpretarRespuestaUmbral(n)
{
    //n recibido es String
    n=parseFloat(n)
    switch(n)
    {
        case 102:
            return false
        case 103:
            return false
        case 104:
            return false
        case 105:
            return false
        default:
            return true
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
function mostrarMensajeUmbral(n)
{
    var msg=0
    //n recibido es String
    n=parseFloat(n)
    var mostrar=false;
    switch(n)
    {
        case 102:
            msg="No ha iniciado sesión o su sesión ha caducado."
            msg+=" Por favor, inicie sesión."
            mostrar=true;
            break;
        case 103:
            msg="El nombre de usuario recibido no es válido."
            mostrar=true;
            break;
        case 104:
            msg="El usuario indicado no se ha encontrado en la base de datos."
            mostrar=true;
            break;
        case 105:
            msg="No se ha iniciado sesión."
            mostrar=true;
            break;
        default:
            msg="El umbral se ha cambiado satisfactoriamente."
            mostrar=true;
            break;
    }
    if(mostrar)
    {
        window.alert(msg);
    }
    return msg
}

//-----------------------------------------------------------------------------

//LLAMADA DESDE EL TEMPLATE
/*Enviar unbral en el form de changeUmbral.html.
Interpreta los valores devueltos por comprobarUmbral() y muestra
avisos por pantalla.
Similar a enviarUmbral() pero obtiene los datos del form, los comprueba,
y si son correctos, los envía.
Si está todo bien, enviará los datos al servidor con postUmbral().*/
//En vez de recibir el supuesto umbral, recibe una cadena que
//se empleará como selector del form.
function enviarUmbralForm(selectForm)
{
    $(selectForm).submit(function(e)
    {
        //Obtengo en lista datos una lista de pares de datos
        //con nombre del campo y su valor
        //[{ name: "umbral", value: "17" }, ...]
        //listaDatos[0]['name'] ==> 'umbral'
        var listaDatos = $(selectForm).serializeArray();
        console.log("Los datos del form:");
        console.log(listaDatos);
		//Obtengo el valor del umbral del form
    	var umbralForm = NaN
		for(i in listaDatos)
        {
            if(listaDatos[i]['name']=="umbral")
            {
                umbralForm = listaDatos[i]['value']
            }
        }
		console.log("umbral obtenido del form: " + umbralForm);

        console.log("func - enviarUmbral");
        n=comprobarUmbral(umbralForm);
        //muestro mensaje de resultado de comprobar umbral
        mostrarComprobacionUmbral(n);
        console.log("func - enviarUmbral: n = " + n);
        if(n!=101 && n!=102)
        {
            //Obtengo direccion del form a la que enviaré el post
            url = $(selectForm).attr('action')
            //Utilizo el numero que he parseado en vez
            //de el obtenido directamente del form.
            //Ya que 'n' lo hemos podido alterar para
            //que sea un numero(p.ej: 12,12 -> 12.12)
            datos ='umbral=' + n 
            $.post(url, datos,function(res)
            {
                //respuestasServidor.js
                //mostrarRespuestaServidor(e)
                
                interpretarRespuestaServidor(res,
                interpretarRespuestaUmbral,
                mostrarMensajeUmbral);
            },'json');
        }
        //Evitamos el comportamiento por defecto del form, de
        //forma que no envía por su cuenta el formulario al servidor
        e.preventDefault();
    });
}
