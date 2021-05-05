
const myForm = document.getElementById("form-user");

myForm.addEventListener("submit",(e) => {


    e.preventDefault();

    // On récupère les ddonnées formulaire
    const nom = document.getElementById("id-nom").value;
    const email = document.getElementById("id-email").value;
    const mdp = document.getElementById("id-mdp").value;
    const list_qr = document.getElementById("id-list-qr").value;

    
   
    valid_nom = valider_nom(nom);
    valid_email = valider_email(email);
    valid_mdp = valider_mdp(mdp);
    valid_list = valider_list(list_qr);

    if (valid_nom == true && valid_email == true && valid_mdp == true && valid_list == true) {
        return true;
    } else {
        return false;
    }

});


function valider_nom(input) {
    if(input == "" || input == null) {
        document.getElementById("msg-nom").innerHTML ="Le profil doit contenir un nom.";
        return false;
    } else {
        document.getElementById("msg-nom").innerHTML ="";
        return true;
    }
}

function valider_mdp(input) {
    if(input == "" || input == null) {
        document.getElementById("msg-mdp").innerHTML ="Le profil doit contenir un mot de passe.";
        return false;
    } else {
        document.getElementById("msg-mdp").innerHTML ="";
        return true;
    }
  
}

function valider_list(input) {
    if(input == "" || input == null) {
        document.getElementById("msg-list").innerHTML ="Il faut sélectionner un quartier.";
        return false;
    } else {
        document.getElementById("msg-list").innerHTML ="";
        return true;
    }

}

function valider_email(input) {
    if(input == "" || input == null) {
        document.getElementById("msg-email").innerHTML ="Le profil doit contenir un email.";
        return false;
    } else {
        document.getElementById("msg-email").innerHTML ="";
    }

    if(!input.match(/^[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+/g) && input != "") {
        document.getElementById("msg-email").innerHTML = "Le format de l'email est invalide."
        return false;
    } else {
        document.getElementById("msg-email").innerHTML = "";
        return true;
    }
   
}

 