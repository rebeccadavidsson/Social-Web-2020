var myModal = document.getElementById('exampleModal')
var myInput = document.getElementById('exampleModalLabel')

myModal.addEventListener('shown.bs.modal', function (e) {
  myInput.focus()
});

$('#exampleModal').on('hidden.bs.modal', function (e) {
  var input = document.querySelector("#exampleModal > div > div > div.modal-body");
  input.innerHTML = ""
});

// Create date
var ptag = ""
var dateselector = document.querySelectorAll("body > div.rooster > p, body > div.rooster > div" )
dateselector.forEach((item, i) => {
  if (item.classList.contains("title")) {
    temp = item.innerHTML
    ptag = "<p class='dag' syle='display:none; visibility:hidden;'>" + temp + "</p>"
  }
  else {

    item.innerHTML += ptag

    item.childNodes.forEach(function(elm) {
      try {
        elm.classList.contains("row")
        elm.appendChild(ptag)
      } catch (e) {
        // Do nothing
      };
    });
  };

  item.setAttribute("name", temp)
});

var selector = document.querySelectorAll("body > div.rooster > div")

for (const button of selector) {

  var btn = document.createElement("button");
  btn.className = "addschedule"
  btn.innerHTML = "Add";

  btn.setAttribute("data-toggle", "modal");
  btn.setAttribute("data-target", "#exampleModal");


  btn.addEventListener('click', function(e) {
    var result = e.target;
    ineer_html = result.parentElement.parentElement.innerHTML;

    var data = new FormData();
    data.append('data', ineer_html)

    var input = document.querySelector("#exampleModal > div > div > div.modal-body");

    input.innerHTML += ineer_html;

    var csrfToken = document.querySelector("#csrf input").value;

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/addschedule', true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    xhttp.send(data);

  });
  button.childNodes.item(1).appendChild(btn);

}
