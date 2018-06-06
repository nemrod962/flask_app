/*Script que empleará el diálogo de jquery-ui presente en cada página para
 * mostrar alertas al usuario. Se empleará como alternativa a window..alert().
    > La id del dialog es "miDialogo".
    > La id del <span> del diálogo es "miDialogoTexto".*/

//Variables globales. Ids a emplear
var idDialogo = "miDialogo"
var idTexto = "miDialogoTexto"

//Recibiré como parámetro el mensaje a mostrar en el diálogo
function mostrarAlerta(msg)
{
    /*Solo muestro el mensaje si se ha cargado toda la página.
    Si no espero, existe el riesgo de que intente mostrar el 
    diálogo cuando todavía no se ha cargado, lo que provocará 
    un error e impedirá que se carguen el resto de scripts.*/
    if(document.readyState === "complete")
    {
        //Asigno mensaje al texto del dialogo
        $("#"+idTexto).html(msg);
        //muestro diálogo
        $("#"+idDialogo).dialog("open");
    }   
    else
    {
        console.log("ATENCION: no se ha mostrado el diálogo porque" + 
        "todavia no ha cargado");
    }
}
