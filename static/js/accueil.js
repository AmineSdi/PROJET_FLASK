const myForm = document.getElementById("form-dates");

myForm.addEventListener('submit',function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch("/api/declarations", {
        method: "GET",
        body: formData

    }).then(function(response) {
        return response.text();
    }).then(function (text) {
        document.getElementById("date-div").innerHTML = text;
    });

});