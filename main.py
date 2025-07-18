from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
genai.configure(api_key="AIzaSyDxYnqI7rauFjB8PAa0z6yryAr3iXnblNM")
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users:
            return "Користувач з таким ім'ям вже існує!"

        users[username] = password
        save_users(users)
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('cars'))
        else:
            return 'Неправильний логін або пароль'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/ai", methods=["GET", "POST"])
def ai_chat():
    response_text = ""
    if request.method == "POST":
        user_question = request.form.get("question")
        try:
            response = model.generate_content(user_question)
            response_text = response.text
        except Exception as e:
            response_text = f"Помилка: {e}"
    return render_template("ai.html", response=response_text)

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/cars')
def cars():
    car_data = [
        {
            "brand": "BMW",
            "country": "Німеччина",
            "year": 1916,
            "description": "BMW відома своїми динамічними автомобілями та участю в автоспорті. Серія M є синонімом потужності та стилю. Компанія активно інвестує в електромобілі та нові технології.",
            "image": "BMW.jpg"
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
            "image": "mersedes.jpg"
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
    app.run(debug=True)