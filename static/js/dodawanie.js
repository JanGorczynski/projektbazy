let myDictionary ={
    "wojewodztwa":["id_woj","nazwa"],
    "powiaty": ["nazwa", "id_powiat", "id_woj"],
    "consumer": ["consumer_id", "id_grid_member"],
    "producers": ["id_producer", "id_grid_member"],
    "adres": ["id_adres", "ulica", "nr_domu"],
    "grid_member": ["id", "type_id", "adres_id"],
    "type": ["id_type", "nazwa"],
    "emergency_member": ["id", "grid_id", "emergency_id"],
    "emergency": ["id_emergency", "description"]
}

var value ="";
document.getElementById("myFrom").addEventListener("submit", function (event) {
    event.preventDefault();
    let form = document.getElementById("test");
    value = document.getElementById("tabele").value;
    console.log(value)
    let html = '<p>Wprowadź dane:</p>'
    let dbObj = myDictionary[value]
    for (i in dbObj){
        let column = dbObj[i];
        html+= `<p>${column}:</p><input type="text" id="${column}"><br></br>`
    }
    html+= '<button onclick="wprowadz(event)" >Wprowadź</button>'
    form.innerHTML = html;
});

function  wprowadz(event){
    event.preventDefault();
    console.log("wprowadz")
    let dbObj = myDictionary[value]
    let dane = {}
    for (i in dbObj){
        let column = dbObj[i];
        let val = document.getElementById(column).value;
        console.log(val);
        dane[column] = val ;
    }
    console.log(JSON.stringify(dane));
    
    fetch(`http://localhost:5000/${value}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(dane)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
}