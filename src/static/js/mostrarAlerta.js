/*Script que empleará el diálogo de jquery-ui presente en cada página para
 * mostrar alertas al usuario. Se empleará como alternativa awindow.alert().
    > La id del dialog es "miDialogo".
    > La id del <span> del diálogo es "miDialogoTexto".*/

//Variables globales. Ids a emplear
var idDialogo = "miDialogo"
var idTexto = "miDialogoTexto"

//Recibiré como parámetro el mensaje a mostrar en el diálogo
function mostrarAlerta(msg)
{
    //Asigno mensaje al texto del dialogo
    $("#"+idTexto).html(msg);
    //muestro diálogo
    $("#"+idDialogo).dialog("open");
}
