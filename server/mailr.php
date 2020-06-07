<?php
date_default_timezone_set("Asia/Kolkata");
$logDir = "./logs";
if (!file_exists($logDir)) {
    mkdir($logDir, 0777, true);
}
function get_ip(){
    $ipaddress = '';
    if (getenv('HTTP_CLIENT_IP'))
        $ipaddress = getenv('HTTP_CLIENT_IP');
    else if(getenv('HTTP_X_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_X_FORWARDED_FOR');
    else if(getenv('HTTP_X_FORWARDED'))
        $ipaddress = getenv('HTTP_X_FORWARDED');
    else if(getenv('HTTP_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_FORWARDED_FOR');
    else if(getenv('HTTP_FORWARDED'))
       $ipaddress = getenv('HTTP_FORWARDED');
    else if(getenv('REMOTE_ADDR'))
        $ipaddress = getenv('REMOTE_ADDR');
    else
        $ipaddress = 'UNKNOWN';
    return $ipaddress;
}

$to = $_POST['to'];
$from = $_POST['from'];
$subject = $_POST['subject'];
$body = $_POST['body'];
$headers = "From: ".$from."\r\n"."CC: ".$to;

$logFile = $logDir."/".$to.".log";
$file = fopen($logFile,"a+");
fwrite($file,"\n\nIP: ".get_ip());
fwrite($file,"\nTime: ".date("Y-m-d h:i:sa"));
fwrite($file,"\nFrom: ".$from);
fwrite($file,"\nSubject: ".$subject);
fwrite($file,"\nBody: ".$body);


if(mail($to,$subject,$body,$headers)){
    echo "True";
}else{
    echo "False";
}

?>


