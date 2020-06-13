setInterval(updateLastUpdate, 1000);
setInterval(updateSystemStateFromDatabase, 1000);


function updateLastUpdate()
{
    var currentDate = new Date();
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var dateStr = "Last Update: " + months[currentDate.getMonth()] + ". " +
                  ("00" + currentDate.getDate()).slice(-2) + ", " +
                  currentDate.getFullYear() + " " +
                  ("00" + currentDate.getHours()).slice(-2) + ":" +
                  ("00" + currentDate.getMinutes()).slice(-2) + ":" +
                  ("00" + currentDate.getSeconds()).slice(-2);
    document.getElementById("last-update").innerHTML = dateStr;
}


function updateSystemStateFromDatabase()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("query-server-section").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "scripts/query-server.php", true);
    xhttp.send();
}

