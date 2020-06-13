setInterval(updateCounter, 1000);

let counter = 0;

function updateCounter()
{
    counter = counter + 1;
    document.querySelector('h1').textContent = counter.toString();
    loadDoc(counter);
}

function loadDoc(counter)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("demo").innerHTML = counter.toString();
        }
    };
    xhttp.open("GET", "ajax_info.txt", true);
    xhttp.send();
}

function loadQueryServer()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("query-server-section").innerHTML = this.response;
        }
    };
    xhttp.open("GET", "query-server.php", true);
    xhttp.send();
}

// alert("Howdy")

/*
<?php
    echo "Howdy";
?>
*/
