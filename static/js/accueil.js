$(document).ready(function(){
$('#search-date').click(function(event){
    event.preventDefault();
    if($('#id-du').val() < $('#id-au').val()) {
        $.ajax({
            data: {
                du: $('#id-du').val(),
                au: $('#id-au').val()
            },
            type: 'GET',
            url: 'api/declarations',
            dataType: 'JSON',
            async: false,
            success: function (data) {
                let tableResultat = "";
                let table = "<div>" +
                    "<h2 class=\"text-center\" style=\"margin-bottom: 20px;\">Les déclarations</h2>" +
                    "<table>" +
                    "<tr>" +
                    "<th>Nom de l'arrondissement</th><th>Nom de quartier</th></tr>";
                tableResultat += table;

                for (let i = 0; i < data.dict.length; i++) {
                    let nom_arrond = data.dict[i].nom_arrond;
                    let nom_qr = data.dict[i].nom_qr;

                    let dataTable = "<tr> " + "<td>" + nom_arrond + "</td>" + "<td>" + nom_qr
                        + "</td>" + " </tr> "
                    tableResultat += dataTable;
                }
                tableResultat += "</table></div>";
                $("#date-div").append(tableResultat);
            },

            error: function (e) {
                alert('Erreur: ' + e);
            }
        });
    }
    else
        alert("la deuxième date doit être supérieur à la première!");
});

});