<?php
    session_start();

    $authorized = false;
    if (!isset($_SESSION['authorized'])) {    
        
        // Authentication - by POST, automatic
        if ($_POST['password'] == '') {
            $_SESSION['authorized'] = true;
            $authorized = true;
        }
        
        // Authentication - by referrer, automatic
        if ($_SERVER['REMOTE_ADDR'] == '127.0.0.1') {
            $_SESSION['authorized'] == true;
            $authorized = true;
        }
    } else $authorized = true;

    if (isset($_POST['gurl'])) {     // Plain POST URL get
        if (!$authorized) die();
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'http://127.0.0.1:8080'.$_POST['gurl']);
        curl_setopt($ch, CURLOPT_PORT, 8080);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $data = curl_exec($ch);
        if (!$data) die('cURL failed: '.curl_error());
        curl_close($ch);
        header('Content-Type: application/json', true);
        echo $data;
    }

?>