const toggle = $('toggle');
const togglers = document.querySelectorAll('.toggler');
let current = 'vnd';

toggle.addEventListener('click', () => {
  current = current === 'vnd' ? 'usd' : 'vnd'
  Array.prototype.forEach.call(togglers, toggler => toggleOnOff(toggler));
  fetch(`${window.origin}/convert/`, {
    method: 'POST',
    body: JSON.stringify({'currency': current})
  })
    .then(response => response.json())
    .then(json => {
      Object.entries(json).map(
        ([k, v]) => displayConversions(k, v)
      );
    })
    .catch(err => {
      console.log(`Error: ${err}`)
    })
})

function toggleOnOff(elem) {
  if (elem.classList.contains('uk-card-primary')) {
    elem.classList.replace('uk-card-primary', 'uk-card-secondary');
  } else {
    elem.classList.replace('uk-card-secondary', 'uk-card-primary');
  }
}

function displayConversions(id, price) {
  const display = $(id);
  const isFree = new RegExp('[₫\$]0(\.00)?');
  if (!isFree.test(price)) {
    display.innerText = price;
  }
}
