const form = $('form');

document.addEventListener('DOMContentLoaded', () => {
  const choices = document.querySelectorAll('input[type="radio"]');
  Array.prototype.forEach.call(choices, choice => choice.classList.add('uk-radio'))

  const csrf = Cookies.get('csrftoken');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
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
          )
        } else {
          $('main').innerText = data.total;
        }
      }).catch(error => {
        console.log(`Error: ${error}`)
      })
  })
});

function displayErrors(id, errorMessages) {
  const errorDisplay = $(id);
  errorMessages.forEach(message =>
    appendError(errorDisplay, message)
  )
}

function appendError(errorDisplay, message) {
  errorDisplay.innerText += message;
}
