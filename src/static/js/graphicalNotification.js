/* Script para la creación de notificaiones gráficas. Este script es empleado
 * por evaluarUmbralSSE.js para crear una notificación en la pantalla del
 * cliente cuando se registre un numero que active el umbral.*/
// request permission on page load
function requestNotificationPermission()
{
    document.addEventListener('DOMContentLoaded', function () {
      if (!Notification) {
        alert('Desktop notifications not available in your browser. Try Chromium.'); 
        return;
      }

      if (Notification.permission !== "granted")
        Notification.requestPermission();
    });
}

function notifyMe(msg, title = "Rnd - Lender", image) {
  requestNotificationPermission();
  if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification(title, {
      //icon: 'http://cdn.sstatic.net/stackexchange/img/logos/so/so-icon.png',
      icon: window.location.origin + '/static/logo_rndlender.png',
      body: msg,
    });
    
    /*
    notification.onclick = function () {
      window.open("http://stackoverflow.com/a/13328397/1269037");      
    };
    */
  }

}
