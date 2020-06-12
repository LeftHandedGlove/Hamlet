setInterval(updateCounter, 1000);

let counter = 0;

function updateCounter()
{
    counter = counter + 1;
    document.querySelector('h1').textContent = counter.toString();
    loadDoc(counter)
}

function loadDoc(counter)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("demo").value = counter.toString();
        }
    };
    xhttp.open("GET", "ajax_info.txt", true);
    xhttp.send();
}

// alert("Howdy")

/*
<?php
    echo "Howdy";
?>
*/
