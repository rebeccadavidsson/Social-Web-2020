var btn = document.createElement("button");
btn.className = "addschedule"
btn.innerHTML = "Add to schedule";

var selector = document.querySelectorAll("body > div.rooster > div")

for (const button of selector) {
  button.addEventListener('click', function(e) {
    var result = e.target;
    ineer_html = result.parentElement.innerHTML;
    var data = new FormData();
    data.append('data', ineer_html)

    alert(ineer_html)
    
    var csrfToken = document.querySelector("#csrf input").value;

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/addschedule', true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    xhttp.send(data);

  });
}
