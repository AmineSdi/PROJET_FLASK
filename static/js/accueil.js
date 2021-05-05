
const myForm = document.getElementById("form-dates");

myForm.addEventListener("submit",(e) => {

    e.preventDefault();

    // On récupère les deux dates
    const du = document.getElementById("id-du").value;
    const au = document.getElementById("id-au").value;

    if (du == "" || au == "") {
        document.getElementById("msg_error").innerHTML = "Veuillez saisir toutes les informations demandées";
        document.getElementById("msg_error").style.color = "red";

    }
    //On va valider les dates
    let valid_date1 = valider_iso(du);
    let valid_date2 = valider_iso(au);

    
    if ((valid_date1 == false && du != "") || (valid_date2 == false && au != "") ) {
    
        document.getElementById("msg_error").innerHTML = "Les dates doivent correspondre au format ISO8601\n"
        document.getElementById("msg_error").style.color = "red";
    } else {

        fetch("/api/declarations?du=" + du + "&au=" + au , {
            method: 'GET',
            dataType: 'JSON',
            async: false,
            
        }).then(function (response) {
            return response.json();
        }).then(function (json) {

            var table = document.getElementById('date-div');
            json.forEach((object) => {
                var tr = document.createElement('tr');
                tr.innerHTML = '<td>' + object.nom_arrond + '</td>' +
                '<td>' + object.nom_qr + '</td>';
                table.appendChild(tr);
            });
            
        })
        
    }


});

function valider_iso(input){

   if (!input.match(/^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])/g)) {
    return false;
  }
  document.getElementById("msg_error").innerHTML = ""
  return true;
}

    