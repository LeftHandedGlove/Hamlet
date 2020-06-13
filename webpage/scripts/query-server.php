<?php
    $serverName = "localhost";
    $userName = "hamlet";
    $password = "hamlet";
    $dbName = "exampledb";
    
    // Create the connection
    $conn = new mysqli($serverName, $userName, $password, $dbName);
    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    
    $sqlQuery = "SELECT * FROM system_state";
    $result = $conn->query($sqlQuery);
    
    // Display the results
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "id: " .$row["id"] . " - CPU Temp: " . $row["cpu_temp"] . " - GPU Temp: " . $row["gpu_temp"] . "<br>";
        }
    } else {
        echo "0 results";
    }
    $conn->close();
?>
