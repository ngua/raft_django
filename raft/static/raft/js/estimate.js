const form = $('form');
const reloadButton = $('reload');

document.addEventListener('DOMContentLoaded', () => {
  const choices = document.querySelectorAll('input[type="checkbox"]');
  Array.prototype.forEach.call(choices, choice => choice.classList.add('uk-checkbox'))
  form.addEventListener('submit', (e) => {submitFormData(e)})
  reloadButton.addEventListener('click', () => {
    $('total').classList.toggle('visible');
    $('estimate').classList.toggle('visible');
  });
});

function submitFormData(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const csrf = Cookies.get('csrftoken');
  const errorContainers = document.querySelectorAll('.uk-text-danger');
  errorContainers.forEach(errorContainer =>
    errorContainer.innerText = ''
  )

  fetch(document.referrer, {
    method: 'POST',
    body: formData,
    headers: new Headers({
      'X-CSRFToken': csrf
    })
  }).then(response => response.json())
    .then(data => {
      if (!data.success) {
        const errors = data.errors;
        Object.entries(errors).map(
          ([k, v]) => displayErrors(k, v)
        );
      } else {
        const total = data.total;
        displayTotal(total);
      }
    }).catch(error => {
      console.log(`Error: ${error}`);
    })
}

function displayErrors(id, errorMessages) {
  const errorContainer = $(id);
  errorMessages.forEach(message =>
    appendError(errorContainer, message)
  );
}

function appendError(errorContainer, message) {
  const errorSpan = document.createElement('span');
  errorSpan.classList.add('uk-animation-fade');
  errorSpan.innerText = message;
  errorContainer.appendChild(errorSpan);
}

function displayTotal(total) {
  const formDisplay = $('estimate');
  const totalDisplay = $('total-display');
  const totalContainer = $('total');

  formDisplay.classList.remove('visible');
  totalContainer.classList.add('visible');
  totalDisplay.innerText = total;
}
