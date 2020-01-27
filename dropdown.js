var slides = document.querySelectorAll('#slides .slide');
var currentSlide = 0;
var slideInterval = setInterval(nextSlide,2000);

function nextSlide() {
    slides[currentSlide].className = 'slide';
    currentSlide = (currentSlide+1)%slides.length;
    slides[currentSlide].className = 'slide showing';
}



window.addEventListener('load', function() {
  var role = window.location.search.split('=')[1].split(',');
  if (role) {
    document.getElementById('selectRole').value = role;
  }
});
