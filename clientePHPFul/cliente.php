<?php
    include'./httpful.phar');
    $uri = "http://192.168.65.129/employes";
    $response = \Httpful\Request::get($url)->send();
    echo count($response);
 ?>