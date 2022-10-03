let contact_window = document.getElementById('contact_window')
let contact_button = document.getElementById('contact_button')

contact_button.addEventListener('click', function onOpen() {
    contact_window.showModal();
});

$('.header__navbar--toggle').click(function(e) {
    e.preventDefault();
    $('.header__navbar').toggleClass('is_open');
})