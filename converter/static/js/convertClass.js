var myModal = document.getElementById('exampleModal')
var myInput = document.getElementById('exampleModalLabel')

myModal.addEventListener('shown.bs.modal', function (e) {
  myInput.focus()
})

$('#exampleModal').on('hidden.bs.modal', function (e) {
  var input = document.querySelector("#exampleModal > div > div > div.modal-body");
  input.innerHTML = ""
})

var btn = document.createElement("button");
btn.className = "addschedule"
btn.innerHTML = "Add to schedule";

var selector = document.querySelectorAll("body > div.rooster > div")

for (const button of selector) {

  button.setAttribute("data-toggle", "modal");
  button.setAttribute("data-target", "#exampleModal");
  // button.setAttribute("class", "btn btn-info btn-lg");

  // console.log(button);
  button.addEventListener('click', function(e) {
    var result = e.target;
    ineer_html = result.parentElement.innerHTML;
    var data = new FormData();
    data.append('data', ineer_html)

    var input = document.querySelector("#exampleModal > div > div > div.modal-body");
    console.log(input);
    input.innerHTML += ineer_html;

    // alert(ineer_html)

    var csrfToken = document.querySelector("#csrf input").value;

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/addschedule', true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    xhttp.send(data);

  });
}
