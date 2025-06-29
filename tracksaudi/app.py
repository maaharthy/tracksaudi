from flask import Flask, render_template, request
import requests

app = Flask(__name__)

AFTERSHIP_API_KEY = "asat_693c664998a64aa992eb0f5d6da01643"
AFTERSHIP_API_URL = "https://api.aftership.com/v4"

HEADERS = {
    "aftership-api-key": AFTERSHIP_API_KEY,
    "Content-Type": "application/json"
}

# جلب قائمة شركات الشحن من AfterShip
def get_couriers():
    response = requests.get(f"{AFTERSHIP_API_URL}/couriers/all", headers=HEADERS)
    if response.status_code == 200:
        couriers = response.json()['data']['couriers']
        # نعيد اسم الشركة والكود
        return [(c['name'], c['slug']) for c in couriers]
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    couriers = get_couriers()
    result = None
    if request.method == 'POST':
        tracking_number = request.form['tracking_number']
        courier_slug = request.form['courier']

        url = f"{AFTERSHIP_API_URL}/trackings/{courier_slug}/{tracking_number}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            result = response.json()
        else:
            result = {"error": "لم يتم العثور على الشحنة أو حدث خطأ."}
    return render_template("index.html", couriers=couriers, result=result)

if __name__ == '__main__':
    app.run(debug=True)