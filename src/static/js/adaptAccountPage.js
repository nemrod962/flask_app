/*Recibo un div. Dentro del div hay varios divs que contienen
la representación de los datos del usuario. Dentro de estos divs a su vez
hay un elemento de la clase "userInfo". Si ese elemento contiene None,
borraremos el div entero.

El Div superior que recibiremos es de la clase 'userInfoBlock'.

Los diferentes divs con representaciones de la info de usuario
son de la clase 'userInfoDiv'.

Dentro de los divs de la clase 'userInfoDiv' hay elementos <span>
de la clase 'userInfo', cuyo contenido debemos revisar.
*/
function checkCamposVacios(divGeneral)
{
    console.log('funcion - checkCampoVacio()');
    //console.log('elem: ' + divGeneral);
    //console.log('elem: ' + divGeneral.innerHTML);

    var divsInfo = divGeneral.getElementsByClassName('userInfoDiv');
    //console.log('divsInfo : ' + divsInfo );
    //for(div of divsInfo) {

    //Guardaremos los indices a borrar para 
    //borrar los elementos tras finalizar el for
    var listaIndicesABorrar = [];

    for(var i=0; i<divsInfo.length; i++) {
        div = divsInfo[i];
        //console.log('div:' + div )
        console.log('div_in:' + div.innerHTML);
        //span class = 'userInfo'
        var span = div.getElementsByClassName('userInfo');
        //Como me devuelve un array, cojo el primer elemento ([0]).
        //console.log('span:' + span[0]);
        //console.log('span_in:' + span[0].innerHTML);
        //html interior de 'userInfo'
        var info = span[0].innerHTML;
        //console.log('text(0):' + info );
        //elimino espacios en blanco
        info = info.replace(/ /g,'');
        //console.log('text(1):' + info );

        console.log('resultado:<' + info + '>');
        if(info == 'None')
        {
            console.log('borrar');
            //borramos el div de la clase 
            //'userInfoDiv', que contiene datos
            //que estan vacios y osn inutiles
            div.parentNode.removeChild(div);

            //Al borrar cambiará el array: el elemento
            //que estaba en la posicion i+1 antes de borrar
            //el elemento en la posicion i, estará en la posición
            //i tras borrarlo. Para no saltarnos ese elemento, reduciremos
            //el indice i en 1.
            i--;
        }
        else
        {
            console.log('NO borrar');
        }
    }

}

//Compruebo los campos al cargar la página
window.onload = checkCamposVacios(document.getElementsByClassName('userInfoBlock')[0])

