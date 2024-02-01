// Timer for Django messages

document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
    document.querySelectorAll('.alert').forEach(function(message) {
      message.style.display = 'none';
    });
  }, 5000);
});
