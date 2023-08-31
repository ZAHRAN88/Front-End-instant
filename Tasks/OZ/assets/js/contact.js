document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contactForm');
    const confirmationMessage = document.getElementById('confirmationMessage');

    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (contactForm.checkValidity()) {
            confirmationMessage.textContent = 'Thank you for your message! We will get back to you soon.';
            confirmationMessage.style.display = 'block';
            contactForm.reset();
        } else {
            event.stopPropagation();
        }

        contactForm.classList.add('was-validated');
    });
});
