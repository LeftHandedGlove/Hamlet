<?php echo date('Y-m-d H:i:s') . "<br>"; ?>


<?php
    $sys_stat_path = "system_status.json";
    $sys_stat_text = file_get_contents($sys_stat_path);
    if ($sys_stat_text == false)
    {
        echo "Unable to find $sys_stat_path";
    }
    
    $sys_stat_json = json_decode($sys_stat_text, true);
    if($sys_stat_json == null)
    {
        echo "Unable to parse $sys_stat_path" . "<br>";
        echo "File Contents:" . "<br>";
        echo nl2br("$sys_stat_text") . "<br>";
    }
    
    foreach ($sys_stat_json as $sys_field => $sys_value) 
    {
        if ($sys_field == "Units")
        {
            echo "$sys_field";
            foreach ($sys_value as $unit_json)
            {
                echo gettype($unit_json);
            }
        }
        //print_r($sys_field)
        //print_r($sys_value)
    }
?>
