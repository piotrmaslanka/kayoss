<?php
/*    session_start();
    $_SESSION['authorized'] = true;     // #todo placeholder
    if (!isset($_SESSION['authorized'])) {
        if (isset($_SESSION['password'])) {
            if ($_SESSION['password'] == 'x')
                $_SESSION['authorized'] == true;
        } else
            die();
    }
    */
    if (isset($_POST['gurl'])) {     // Plain POST URL get
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