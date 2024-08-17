document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        // Get the target element
        const target = document.querySelector(this.getAttribute('href'));

        // Get the target element's top position and subtract to show the gap
        const topPosition = target.getBoundingClientRect().top + window.pageYOffset - 200; // Adjust 50px to your needs

        // Smooth scroll to the adjusted position
        window.scrollTo({
            top: topPosition,
            behavior: 'smooth'
        });
    });
});
