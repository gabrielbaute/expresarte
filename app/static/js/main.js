document.addEventListener('DOMContentLoaded', () => {
  // Menú de hamburguesas para teléfono
  const burgers = Array.from(document.querySelectorAll('.navbar-burger'));
  
  burgers.forEach(burger => {
    burger.addEventListener('click', () => {
      const targetId = burger.dataset.target;
      const target = document.getElementById(targetId);

      burger.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });

  // Cierre manual de notificaciones flash
  const deleteButtons = document.querySelectorAll('.notification .delete');
  deleteButtons.forEach(button => {
    const notification = button.parentNode;
    button.addEventListener('click', () => {
      notification.classList.add('is-hidden');
    });
  });

  // Ejemplo opcional para mostrar mensaje flash en un modal (si decides hacerlo)
  const flashModal = document.getElementById('flash-modal');
  const modalMessage = document.getElementById('flash-message-content');

  const notifications = document.querySelectorAll('.notification-container .notification');
  notifications.forEach(note => {
    const message = note.textContent.trim();
    if (flashModal && modalMessage) {
      modalMessage.textContent = message;
      flashModal.classList.add('is-active');
    }
  });

  // Cierre del modal
  const modalClose = document.querySelectorAll('.modal-close, .modal-background');
  modalClose.forEach(el => {
    el.addEventListener('click', () => {
      flashModal.classList.remove('is-active');
    });
  });
});