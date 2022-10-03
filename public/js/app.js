let contact_window = document.getElementById('contact_window');
let contact_button = document.getElementById('contact_button');
let close_contact_button = document.getElementById('close_contact_button');

// Ouvre la modal avec le boutton
contact_button.addEventListener('click', function() {
    contact_window.showModal();
});

// Ferme la modal avec le boutton
close_contact_button.addEventListener('click', function() {
    contact_window.close();
});

// Ferme la modal lorsqu'on clique à l'extérieur
window.onclick = function(event) {
    if (event.target == contact_window) {
        contact_window.close();
    }
}

$('.header__navbar--toggle').click(function(e) {
    e.preventDefault();
    $('.header__navbar').toggleClass('is_open');
});