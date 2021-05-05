
$(function() {

    $("#msg-nom").hide();
    $("#msg-email").hide();
    $("#msg-list").hide();
    $("#msg-mdp").hide();

    var err_nom = false;
    var err_email = false;
    var err_list = false;
    var err_mdp = false;
   

    $("#id-nom").focusout(function(){
       valider_nom();
    });
    $("#id-email").focusout(function() {
       valider_email();
    });
    $("#id-list").focusout(function() {
       valider_list();
    });
    $("#id-mdp").focusout(function() {
       valider_mdp();
    });
   

    function valider_nom() {
        var nom = $("#id-nom").val();

        if(nom == "" || nom == null) {
    
           $("#msg-nom").html("Le nom complet est obligatoire");
           $("#msg-nom").show();
           $("#id-nom").css("border-bottom", "2px solid #F90A0A");

        err_nom = true;

        } else {

            $("#msg-nom").hide();
            $("#id-nom").css("border-bottom","2px solid #34f458");
            err_nom = false;
        }
    }

    function valider_email() {
        var email = $("#id-email").val();
        var pattern = /^[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+/g;

        if(email == "" || email == null) {
            $("#msg-email").html("L\'utilisateur doit avoir un email.");
            $("#msg-email").show();

            err_email = true;
        } else {
            $("#msg-email").hide();
            err_email = false;
        }
    
        if(!pattern.test(email) && email != "") {
            $("#msg-email").html("Le format de l\'email est invalide");
            $("#msg-email").show();
            $("#id-email").css("border-bottom", "2px solid #F90A0A");

            err_email = true;
        } else {
            $("#msg-email").hide();
            err_email = false;
        }
       
    }

    function valider_list() {
        var list = $("#id-list-qr").val();

        if(list == "" || list == null) {
            $("#msg-list").html("L\'utilisateur doit sélectionner un quartier");
            $("#msg-list").show();
            $("#id-list-qr").css("border-bottom", "2px solid #F90A0A");
            err_list = true;
        } else {
            $("#msg-list").hide();
            err_list = false;
        }
    
    }

    function valider_mdp() {
        var mdp = $("#id-mdp").val();

        if(mdp == "" || mdp == null) {
            $("#msg-mdp").html("L\'utilisateur doit avoir un mot de passe.");
            $("#msg-mdp").show();
            $("#id-mdp").css("border-bottom", "2px solid #F90A0A");
            err_mdp = true;
        } else {
            $("#msg-mdp").hide();
            err_mdp = false;
        }
        
    }

    $("#form-user").submit(function() {
        err_nom = false;
        err_email = false;
        err_list = false;
        err_mdp = false;
       
       valider_nom();
       valider_email();
       valider_list();
       valider_mdp();

       if (err_nom === false && err_email === false && err_list === false && err_mdp === false) {
          alert("Registration Successfull");


          return true;
       } else {
          alert("Please Fill the form Correctly");
          return false;
       }

    });
 });