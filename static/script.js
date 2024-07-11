const resultContainer = document.getElementById('result-container');
const wineForm = document.getElementById('wineForm');

function calculatePrice(wineData) {
  
  const price = calculate_price_function(wineData);
  return price;
}

wineForm.addEventListener('submit', (event) => {
  event.preventDefault(); 

  const wineData = {
    name: document.getElementById('wine_name').value,
    year: parseInt(document.getElementById('wine_year').value),
    country: document.getElementById('wine_country').value,
    // ... Get data from other form inputs
  };

  calculatePrice(wineData).then(price => {
    const message = `¡Hola Mundo! El precio estimado de tu vino es: ${price}`;
    displayMessage(message);
  });
});

function displayMessage(message) {
  resultContainer.innerHTML = message;
}
