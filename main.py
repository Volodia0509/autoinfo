from flask import Flask, render_template, request, redirect, session, url_for
import requests
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# URL API
PHP_API_URL = "https://justconsole.tech/python/api.php?table=users_new"

@app.route('/')
def home():
    user = session.get('user')
    return render_template("index.html", user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Хешування пароля
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }

        try:
            response = requests.post(PHP_API_URL, json=data)
            if response.status_code == 200:
                return redirect('/login')
            else:
                return f"<p>Помилка при реєстрації: {response.text}</p>"
        except requests.exceptions.RequestException as e:
            return f"<p>Халепа з API: {str(e)}</p>"

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            response = requests.get(PHP_API_URL)
            users = response.json()
            user = next((u for u in users if u['username'] == username), None)

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                print(True)
                session['user'] = user['username']
                return redirect('/')
            else:
                print(False)
                return "<p>Невірний логін або пароль!</p>"

        except requests.exceptions.RequestException as e:
            return f"<p>Халепа з API: {str(e)}</p>"

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/cars')
def cars():
    car_data = [
        {
            "brand": "BMW",
            "country": "Німеччина",
            "year": 1916,
            "description": "BMW відома своїми динамічними автомобілями та участю в автоспорті. Серія M є синонімом потужності та стилю. Компанія активно інвестує в електромобілі та нові технології.",
            "image": "bmw.jpg"
        },
        {
            "brand": "Toyota",
            "country": "Японія",
            "year": 1937,
            "description": "Toyota є одним із лідерів світового автопрому. Вона відома своєю надійністю, гібридними технологіями (Prius) та моделлю Land Cruiser. Велику увагу приділяє екологічності.",
            "image": "toyota.jpg"
        },
        {
            "brand": "Ford",
            "country": "США",
            "year": 1903,
            "description": "Ford започаткував масове виробництво автомобілів. Відомі моделі — Mustang і F-150. Компанія має довгу історію в інноваціях і автомобільній інженерії.",
            "image": "ford.jpg"
        },
        {
            "brand": "Mercedes-Benz",
            "country": "Німеччина",
            "year": 1926,
            "description": "Mercedes-Benz є символом розкоші, комфорту та технічної досконалості. Її слоган — «Найкраще або нічого». Компанія активно розвиває електролінійку EQ.",
            "image": "mercedes.jpg"
        },
        {
            "brand": "Audi",
            "country": "Німеччина",
            "year": 1909,
            "description": "Audi поєднує сучасні технології, стильний дизайн та продуктивність. Відомі моделі — A4, A6, Q7. Quattro — фірмова система повного приводу.",
            "image": "audi.jpg"
        },
        {
            "brand": "Honda",
            "country": "Японія",
            "year": 1948,
            "description": "Honda виробляє як надійні авто, так і мотоцикли. Civic і Accord — одні з найпопулярніших моделей. Компанія також відома участю у Формулі-1.",
            "image": "honda.jpg"
        },
        {
            "brand": "Chevrolet",
            "country": "США",
            "year": 1911,
            "description": "Chevrolet має велику присутність у всіх класах авто. Її Camaro і Corvette — справжні американські мускулкари. Компанія також випускає SUV та електрокари.",
            "image": "chevrolet.jpg"
        },
        {
            "brand": "Lamborghini",
            "country": "Італія",
            "year": 1963,
            "description": "Lamborghini виробляє суперкарі з яскравим дизайном і надзвичайною потужністю. Моделі як Huracán та Aventador — символи швидкості та ексклюзивності.",
            "image": "lamborghini.jpg"
        },
        {
            "brand": "Ferrari",
            "country": "Італія",
            "year": 1939,
            "description": "Ferrari є легендою автоспорту і престижу. Її авто мають впізнаваний дизайн і неймовірну продуктивність. Це символ статусу і швидкості.",
            "image": "ferrari.jpg"
        },
        {
            "brand": "Volkswagen",
            "country": "Німеччина",
            "year": 1937,
            "description": "VW відомий моделями Golf, Passat і легендарним Beetle. Компанія активно переходить на електротягу з моделями ID. Входить до складу великого автоконцерну.",
            "image": "volkswagen.jpg"
        },
        {
            "brand": "Nissan",
            "country": "Японія",
            "year": 1933,
            "description": "Nissan виробляє практичні та інноваційні авто, такі як Qashqai і електричний Leaf. Компанія входить до альянсу Renault-Nissan-Mitsubishi.",
            "image": "nissan.jpg"
        },
        {
            "brand": "Porsche",
            "country": "Німеччина",
            "year": 1931,
            "description": "Porsche — це синонім спортивних авто. 911 — одна з найзнаменитіших моделей у світі. Компанія поєднує розкіш і продуктивність.",
            "image": "porsche.jpg"
        },
        {
            "brand": "Mazda",
            "country": "Японія",
            "year": 1920,
            "description": "Mazda відома своєю філософією «Zoom-Zoom» — задоволенням від водіння. Skyactiv-технології роблять авто економічними і продуктивними.",
            "image": "mazda.jpg"
        },
        {
            "brand": "Subaru",
            "country": "Японія",
            "year": 1953,
            "description": "Subaru славиться надійними повнопривідними авто, такими як Forester та Outback. Компанія цінується за безпеку й довговічність.",
            "image": "subaru.jpg"
        },
        {
            "brand": "Kia",
            "country": "Південна Корея",
            "year": 1944,
            "description": "Kia стрімко зросла в якості та дизайні. Моделі як Sportage та EV6 вражають сучасністю та інноваціями. Компанія має конкурентні ціни.",
            "image": "kia.jpg"
        },
        {
            "brand": "Hyundai",
            "country": "Південна Корея",
            "year": 1967,
            "description": "Hyundai — глобальний бренд з інноваційними авто. Моделі як Tucson, Santa Fe, та Ioniq — приклади сучасного дизайну й ефективності.",
            "image": "hyundai.jpg"
        },
        {
            "brand": "Jaguar",
            "country": "Велика Британія",
            "year": 1935,
            "description": "Jaguar поєднує британську елегантність і спортивність. Моделі як XF та F-Type мають вишуканий вигляд і чудову динаміку.",
            "image": "jaguar.jpg"
        },
        {
            "brand": "Tesla",
            "country": "США",
            "year": 2003,
            "description": "Tesla — лідер у сфері електромобілів. Компанія Ілона Маска створює авто майбутнього з автопілотом, великим запасом ходу і шаленим прискоренням.",
            "image": "tesla.jpg"
        },
        {
            "brand": "Peugeot",
            "country": "Франція",
            "year": 1810,
            "description": "Peugeot має глибоке коріння у французькому автопромі. Вона виробляє стильні та практичні авто, включаючи хетчбеки і кросовери.",
            "image": "peugeot.jpg"
        },
        {
            "brand": "Renault",
            "country": "Франція",
            "year": 1899,
            "description": "Renault — один із найстаріших європейських брендів. Компанія відома своїми міськими авто, участю у Формулі-1 і партнерством з Nissan.",
            "image": "renault.jpg"
        }
    ]

    return render_template("cars.html", cars=car_data)

if __name__ == '__main__':
    app.run(debug=True, port=5002)