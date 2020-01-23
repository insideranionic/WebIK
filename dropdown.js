function myFunction() {
  document.getElementById("faq-id").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.faq')) {
    var dropdowns = document.getElementsByClassName("faq-text");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}