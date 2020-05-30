<?php echo date('Y-m-d H:i:s'); ?>
<?php 
    $myfilename = "hello.txt";
    if(file_exists($myfilename)){
        echo file_get_contents($myfilename);
    }
?>
