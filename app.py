from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Cargar el modelo entrenado desde el archivo
model = joblib.load('wine_price_model.joblib')

# Tasas de conversión (ejemplos, asegúrate de usar tasas reales y actualizadas)
conversion_rates = {
    'usd': 1.0,
    'eur': 0.92,
    'dop': 59.01,
    'pab': 1.0,
    'mxn': 17.77
}

# Crear la función de estimación del precio del vino
def estimate_wine_price(wine_name, wine_year, wine_country, wine_region, winery, wine_rating, currency):
    """
    Estima el precio de un vino basado en su nombre, año, país, región, bodega y calificación.

    Parámetros:
    wine_name (str): Nombre del vino.
    wine_year (int): Año del vino.
    wine_country (str): País de origen del vino.
    wine_region (str): Región de origen del vino.
    winery (str): Nombre de la bodega.
    wine_rating (float): Calificación del vino.
    currency (str): Moneda en la que se desea obtener el precio.

    Retorna:
    float: Precio estimado del vino en la moneda especificada.
    """
    # Crear un DataFrame con los datos de entrada
    input_data = pd.DataFrame({
        'wine_name': [wine_name],
        'wine_year': [wine_year],
        'wine_country': [wine_country],
        'wine_region': [wine_region],
        'winery': [winery],
        'wine_rating': [wine_rating]
    })

    # Predecir el precio del vino en USD
    estimated_price_usd = model.predict(input_data)[0]

    # Convertir el precio a la moneda especificada
    conversion_rate = conversion_rates.get(currency, 1.0)
    estimated_price = estimated_price_usd * conversion_rate

    return estimated_price

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/calculate')
def calculate():
    return render_template('calculate.html')

@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    # Obtener datos del formulario
    wine_name = request.form['wine_name']
    wine_year = int(request.form['wine_year'])
    wine_country = request.form['wine_country']
    wine_region = request.form['wine_region']
    winery = request.form['winery']
    wine_rating = float(request.form['wine_rating'])
    currency = request.form['currency']
    
    # Estimar el precio del vino
    estimated_price = estimate_wine_price(wine_name, wine_year, wine_country, wine_region, winery, wine_rating, currency)
    
    # Crear el mensaje para mostrar en el HTML
    currency_symbols = {
        'usd': '$',
        'eur': '€',
        'dop': 'RD$',
        'pab': 'B/.',
        'mxn': 'MX$'
    }
    currency_symbol = currency_symbols.get(currency, '$')
    message = f'El precio estimado del vino es: {currency_symbol}{estimated_price:.2f} {currency.upper()}'
    
    return render_template('calculate.html', message=message, wine_name=wine_name, wine_year=wine_year, wine_country=wine_country, wine_region=wine_region, winery=winery, wine_rating=wine_rating, currency=currency)

if __name__ == '__main__':
    app.run(debug=True)
