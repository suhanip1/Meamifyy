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
