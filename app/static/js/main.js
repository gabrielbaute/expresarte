document.addEventListener('DOMContentLoaded', () => {
  // Hamburguesa responsive (ok)
  const burgers = document.querySelectorAll('.navbar-burger');
  burgers.forEach(burger => {
    burger.addEventListener('click', () => {
      const target = document.getElementById(burger.dataset.target);
      burger.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });

  // Mostrar modal si hay mensaje flash
  const flashModal = document.getElementById('flash-modal');
  if (flashModal) {
    flashModal.classList.add('is-active');
  }

  // Cierre del modal
  const modalBackground = flashModal?.querySelector('.modal-background');
  const modalCloseButton = flashModal?.querySelector('.modal-close-button');

  [modalBackground, modalCloseButton].forEach(el => {
    if (el) {
      el.addEventListener('click', () => {
        flashModal.classList.remove('is-active');
      });
    }
  });
});
