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

console.log("hello there!");

function notifyMe(msg, title = "Rnd - Lender", image) {
  requestNotificationPermission();
  if (Notification.permission !== "granted")
    Notification.requestPermission();
  else {
    var notification = new Notification(title, {
      icon: 'http://cdn.sstatic.net/stackexchange/img/logos/so/so-icon.png',
      body: msg,
    });
    
    /*
    notification.onclick = function () {
      window.open("http://stackoverflow.com/a/13328397/1269037");      
    };
    */
  }

}
