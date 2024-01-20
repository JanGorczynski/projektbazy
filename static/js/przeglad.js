
document.getElementById("myFrom").addEventListener("submit", function (event) {
    event.preventDefault();
    let table = document.getElementById("myTable");
    var value = document.getElementById("tabele").value;
    url = "http://localhost:5000/" + value;
    console.log(url)
    fetch(url).then(response => response.json())
    .then(data => {
        let columns = [];
        let html = "";
        for(var i in data["items"][0]){
            columns.push(i);
        }
        html += "<tr>";
        for(var i in columns){
            html += "<th>" + columns[i] + "</th>";
        }
        html += "</tr>";
        
        for(var i in data["items"]){
            html += "<tr>";   
            for (var j in data["items"][i]){
                html += "<td>";
                html += data["items"][i][j];
                html += "</td>";
            }
            console.log(data["items"][i])
            html += "</tr>"
        }
        table.innerHTML = html;
    })
    .catch(error => console.error('Error:', error));
});