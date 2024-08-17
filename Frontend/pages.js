document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute('href'));

        const topPosition = target.getBoundingClientRect().top + window.pageYOffset - 200; 

        window.scrollTo({
            top: topPosition,
            behavior: 'smooth'
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel-inner');
    const items = document.querySelectorAll('.carousel-item');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    let currentIndex = 0;

    function showSlide(index) {
        carousel.style.transform = `translateX(-${index * 100}%)`;
    }

    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        showSlide(currentIndex);
    });

    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % items.length;
        showSlide(currentIndex);
    });
});


document.querySelector('.flip-card').addEventListener('click', function() {
    const flipCardInner = this.querySelector('.flip-card-inner');
    if (flipCardInner.style.transform == "rotateY(180deg)") {
      flipCardInner.style.transform = "rotateY(0deg)";
    } else {
      flipCardInner.style.transform = "rotateY(180deg)";
    }
  });
  