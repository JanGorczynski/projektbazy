document.getElementById("myFrom").addEventListener("submit", function (event) {
    event.preventDefault();
    clear();
    var value = document.getElementById("tabele").value;
    if (value=="production"){
        document.getElementById("input").innerHTML = 
        '<p>Podaj Id czlonka sieci ktorego produkcje chcesz zobaczyc:</p><input type="text" id="id_grid"><button onclick="showProducerRecords()">Zatwierdź</button>';
    }
    else if (value=="consumption"){
        document.getElementById("input").innerHTML = 
        '<p>Podaj Id czlonka sieci ktorego pobór chcesz zobaczyc:</p><input type="text" id="id_grid"><button onclick="showConsumerRecords()">Zatwierdź</button>';
    }
    else if (value=="add_cons"){
        document.getElementById("input").innerHTML = 
        '<p>Podaj Id czlonka sieci:</p><input type="text" id="id_grid"><br></br><p>Podaj ilosc:</p><input type="text" id="ilosc"><br></br><p>Podaj date YYYY-MM-DD:</p><input type="text" id="data"><button onclick="add_consumer_record()">Zatwierdź</button>'
    }
    else if(value=="add_prod"){
        document.getElementById("input").innerHTML = 
        '<p>Podaj Id czlonka sieci:</p><input type="text" id="id_grid"><br></br><p>Podaj ilosc:</p><input type="text" id="ilosc"><br></br><p>Podaj date YYYY-MM-DD:</p><input type="text" id="data"><button onclick="add_producer_record()">Zatwierdź</button>'
    }
})

function add_consumer_record(){
    var id = document.getElementById("id_grid").value;
    var amount = document.getElementById("ilosc").value;
    var date = document.getElementById("data").value;
    request = 'http://localhost:5000/consumer_records?id_grid='+id+"&amount="+amount+"&date='"+date+"'";
    console.log(request)
    
    fetch(request, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        window.alert("Succecfully added to data base");
    }) .catch(error => {
        console.error('Error:', error);
        window.alert("Something is wrong");
      });
}

function add_producer_record(){
    var id = document.getElementById("id_grid").value;
    var amount = document.getElementById("ilosc").value;
    var date = document.getElementById("data").value;
    request = 'http://localhost:5000/producer_records?id_grid='+id+"&amount="+amount+"&date='"+date+"'";
    console.log(request)
    
    fetch(request, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        window.alert("Succecfully added to data base");
    }) .catch(error => {
        console.error('Error:', error);
        window.alert("Something is wrong");
      });
}




function showProducerRecords(){
    var id = document.getElementById("id_grid").value;
    fetch("http://localhost:5000/producer_records?id=" + id).then(response => response.json())
    .then(data=>{
        displayData(data);
    })
}

function showConsumerRecords(){
    var id = document.getElementById("id_grid").value;
    fetch("http://localhost:5000/consumer_records?id=" + id).then(response => response.json())
    .then(data=>{
        displayData(data);
    })
}

function displayData(data){
        console.log(data)
        let columns = [];
        let html = "";
        if (data["items"].length==0){
            html = "Brak danych dla tego id"
        }
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
        table = document.getElementById("myTable");
        table.innerHTML = html;
}

function clear(){
    document.getElementById("input").innerHTML ="";
    document.getElementById("myTable").innerHTML="";

}