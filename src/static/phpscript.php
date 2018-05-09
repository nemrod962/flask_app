<?php
    $url=$_POST['https://beebotte.com/dash/09db3e70-df3a-11e7-bfef-6f68fef5ca14?shareid=shareid_MO4DtM8x1potiMSM'];
    if($url!="")
        echo file_get_contents($url);
?>
