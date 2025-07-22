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

@app.route('/pdr')
def pdr():
    return render_template('pdr.html')

@app.route('/cars')
def cars():
    car_data = [
        {
            "brand": "BMW",
            "country": "Німеччина",
            "year": 1916,
            "description": "BMW відома своїми динамічними автомобілями та участю в автоспорті. Серія M є синонімом потужності та стилю. Компанія активно інвестує в електромобілі та нові технології.",
            "price": 30000,
            "image": "BMW.jpg"
        },
        {
            "brand": "Toyota",
            "country": "Японія",
            "year": 1937,
            "description": "Toyota є одним із лідерів світового автопрому. Вона відома своєю надійністю, гібридними технологіями (Prius) та моделлю Land Cruiser. Велику увагу приділяє екологічності.",
            "price": 26000,
            "image": "toyota.jpg"
        },
        {
            "brand": "Ford",
            "country": "США",
            "year": 1903,
            "description": "Ford започаткував масове виробництво автомобілів. Відомі моделі — Mustang і F-150. Компанія має довгу історію в інноваціях і автомобільній інженерії.",
            "price": 25000,
            "image": "ford.jpg"
        },
        {
            "brand": "Mercedes-Benz",
            "country": "Німеччина",
            "year": 1926,
            "description": "Mercedes-Benz є символом розкоші, комфорту та технічної досконалості. Її слоган — «Найкраще або нічого». Компанія активно розвиває електролінійку EQ.",
            "price": 29000,
            "image": "mersedes.jpg"
        },
        {
            "brand": "Audi",
            "country": "Німеччина",
            "year": 1909,
            "description": "Audi поєднує сучасні технології, стильний дизайн та продуктивність. Відомі моделі — A4, A6, Q7. Quattro — фірмова система повного приводу.",
            "price": 31000,
            "image": "audi.jpg"
        },
        {
            "brand": "Honda",
            "country": "Японія",
            "year": 1948,
            "description": "Honda виробляє як надійні авто, так і мотоцикли. Civic і Accord — одні з найпопулярніших моделей. Компанія також відома участю у Формулі-1.",
            "price": 26000,
            "image": "honda.jpg"
        },
        {
            "brand": "Chevrolet",
            "country": "США",
            "year": 1911,
            "description": "Chevrolet має велику присутність у всіх класах авто. Її Camaro і Corvette — справжні американські мускулкари. Компанія також випускає SUV та електрокари.",
            "price": 19000,
            "image": "chevrolet.jpg"
        },
        {
            "brand": "Lamborghini",
            "country": "Італія",
            "year": 1963,
            "description": "Lamborghini виробляє суперкарі з яскравим дизайном і надзвичайною потужністю. Моделі як Huracán та Aventador — символи швидкості та ексклюзивності.",
            "price": 45000,
            "image": "lamborghini.jpg"
        },
        {
            "brand": "Ferrari",
            "country": "Італія",
            "year": 1939,
            "description": "Ferrari є легендою автоспорту і престижу. Її авто мають впізнаваний дизайн і неймовірну продуктивність. Це символ статусу і швидкості.",
            "price": 50000,
            "image": "ferrari.jpg"
        },
        {
            "brand": "Volkswagen",
            "country": "Німеччина",
            "year": 1937,
            "description": "VW відомий моделями Golf, Passat і легендарним Beetle. Компанія активно переходить на електротягу з моделями ID. Входить до складу великого автоконцерну.",
            "price": 28000,
            "image": "volkswagen.jpg"
        },
        {
            "brand": "Nissan",
            "country": "Японія",
            "year": 1933,
            "description": "Nissan виробляє практичні та інноваційні авто, такі як Qashqai і електричний Leaf. Компанія входить до альянсу Renault-Nissan-Mitsubishi.",
            "price": 26000,
            "image": "nissan.jpg"
        },
        {
            "brand": "Porsche",
            "country": "Німеччина",
            "year": 1931,
            "description": "Porsche — це синонім спортивних авто. 911 — одна з найзнаменитіших моделей у світі. Компанія поєднує розкіш і продуктивність.",
            "price": 44000,
            "image": "porsche.jpg"
        },
        {
            "brand": "Mazda",
            "country": "Японія",
            "year": 1920,
            "description": "Mazda відома своєю філософією «Zoom-Zoom» — задоволенням від водіння. Skyactiv-технології роблять авто економічними і продуктивними.",
            "price": 26000,
            "image": "mazda.jpg"
        },
        {
            "brand": "Subaru",
            "country": "Японія",
            "year": 1953,
            "description": "Subaru славиться надійними повнопривідними авто, такими як Forester та Outback. Компанія цінується за безпеку й довговічність.",
            "price": 25000,
            "image": "subaru.jpg"
        },
        {
            "brand": "Kia",
            "country": "Південна Корея",
            "year": 1944,
            "description": "Kia стрімко зросла в якості та дизайні. Моделі як Sportage та EV6 вражають сучасністю та інноваціями. Компанія має конкурентні ціни.",
            "price": 22000,
            "image": "kia.jpg"
        },
        {
            "brand": "Hyundai",
            "country": "Південна Корея",
            "year": 1967,
            "description": "Hyundai — глобальний бренд з інноваційними авто. Моделі як Tucson, Santa Fe, та Ioniq — приклади сучасного дизайну й ефективності.",
            "price": 21000,
            "image": "hyundai.jpg"
        },
        {
            "brand": "Jaguar",
            "country": "Велика Британія",
            "year": 1935,
            "description": "Jaguar поєднує британську елегантність і спортивність. Моделі як XF та F-Type мають вишуканий вигляд і чудову динаміку.",
            "price": 27000,
            "image": "jaguar.jpg"
        },
        {
            "brand": "Tesla",
            "country": "США",
            "year": 2003,
            "description": "Tesla — лідер у сфері електромобілів. Компанія Ілона Маска створює авто майбутнього з автопілотом, великим запасом ходу і шаленим прискоренням.",
            "price": 26000,
            "image": "tesla.jpg"
        },
        {
            "brand": "Peugeot",
            "country": "Франція",
            "year": 1810,
            "description": "Peugeot має глибоке коріння у французькому автопромі. Вона виробляє стильні та практичні авто, включаючи хетчбеки і кросовери.",
            "price": 24000,
            "image": "peugeot.jpg"
        },
        {
            "brand": "Renault",
            "country": "Франція",
            "year": 1899,
            "description": "Renault — один із найстаріших європейських брендів. Компанія відома своїми міськими авто, участю у Формулі-1 і партнерством з Nissan.",
            "price": 26000,
            "image": "renault.jpg"
        },
        {
            "brand": "Bugatti",
            "country": "Франція",
            "year": 1909,
            "description": "Bugatti — це втілення розкоші та швидкості. Відомий завдяки моделі Veyron та Chiron, бренд встановлює нові стандарти у світі гіперкарів.",
            "price": 100000,
            "image": "bugatti.jpg.jpg"
        },
        {
            "brand": "McLaren",
            "country": "Велика Британія",
            "year": 1963,
            "description": "McLaren відомий своїми надшвидкими спорткарами та інженерною досконалістю. Участь у Формулі-1 закладена в його ДНК.",
            "price": 70000,
            "image": "mclaren.jpg"
        },
        {
            "brand": "Alfa Romeo",
            "country": "Італія",
            "year": 1910,
            "description": "Alfa Romeo — італійська пристрасть у кожній деталі. Автомобілі поєднують елегантність, динаміку і гоночний дух.",
            "price": 51000,
            "image": "alfa_romeo.jpg"
        },
        {
            "brand": "Citroën",
            "country": "Франція",
            "year": 1919,
            "description": "Citroën славиться нестандартними рішеннями та комфортом. Її авто зручні для щоденного використання і мають унікальний дизайн.",
            "price": 26000,
            "image": "citroen.jpg"
        },
        {
            "brand": "Skoda",
            "country": "Чехія",
            "year": 1895,
            "description": "Skoda — надійний європейський бренд, що пропонує зручні та доступні авто. Популярний серед сімей за практичність.",
            "price": 27000,
            "image": "skoda.jpg"
        },
        {
            "brand": "Fiat",
            "country": "Італія",
            "year": 1899,
            "description": "Fiat спеціалізується на компактних авто для міста. Легендарна модель 500 стала символом італійського стилю на дорогах.",
            "price": 24000,
            "image": "fiat.jpg"
        },
        {
            "brand": "Volvo",
            "country": "Швеція",
            "year": 1927,
            "description": "Volvo асоціюється з безпекою, екологічністю та комфортом. Моделі XC60 та XC90 популярні серед родин і в містах.",
            "price": 39000,
            "image": "volvo.jpg"
        },
        {
            "brand": "Jeep",
            "country": "США",
            "year": 1941,
            "description": "Jeep — ікона позашляховиків, відома завдяки моделі Wrangler. Компанія має багату історію військових і цивільних 4x4.",
            "price": 36000,
            "image": "jeep.jpg"
        },
        {
            "brand": "Chrysler",
            "country": "США",
            "year": 1925,
            "description": "Chrysler — це класичний американський бренд, який пропонує як седани, так і мінівени. Відомий увагою до комфорту.",
            "price": 33000,
            "image": "chrysler.jpg"
        },
        {
            "brand": "Dodge",
            "country": "США",
            "year": 1900,
            "description": "Dodge виробляє агресивні мускулкари та потужні пікапи. Моделі Challenger і Charger — культ серед шанувальників швидкості.",
            "price": 30000,
            "image": "dodge.jpg"
        },
        {
            "brand": "Acura",
            "country": "Японія",
            "year": 1986,
            "description": "Acura — преміальний підрозділ Honda. Компанія виробляє надійні авто з акцентом на комфорт і технології.",
            "price": 26000,
            "image": "acura.jpg"
        },
        {
            "brand": "Genesis",
            "country": "Південна Корея",
            "year": 2015,
            "description": "Genesis — люксовий бренд Hyundai. Вирізняється високим рівнем дизайну, технологій та увагою до деталей.",
            "price": 22000,
            "image": "genesis.jpg"
        },
        {
            "brand": "Lexus",
            "country": "Японія",
            "year": 1989,
            "description": "Lexus — це поєднання японської надійності та преміальної якості. Моделі RX і LS вважаються еталонними у своєму класі.",
            "price": 32000,
            "image": "lexus.jpg"
        },
        {
            "brand": "Opel",
            "country": "Німеччина",
            "year": 1862,
            "description": "Opel — традиційний німецький бренд, що пропонує практичні та доступні авто для кожного дня. Astra та Corsa — найпопулярніші.",
            "price": 26000,
            "image": "opel.jpg"
        },
        {
            "brand": "Seat",
            "country": "Іспанія",
            "year": 1950,
            "description": "Seat — молодіжний бренд у складі Volkswagen Group. Його авто поєднують європейську якість з динамічним дизайном.",
            "price": 27000,
            "image": "seat.jpg"
        },
        {
            "brand": "Mini",
            "country": "Велика Британія",
            "year": 1959,
            "description": "Mini — іконічний міський автомобіль. Його унікальний дизайн і маневреність роблять його ідеальним для мегаполісів.",
            "price": 19000,
            "image": "mini.jpg"
        },
        {
            "brand": "Rimac",
            "country": "Хорватія",
            "year": 2009,
            "description": "Rimac — революційний електричний бренд, відомий гіперкарами з космічним прискоренням. Є лідером у електроінноваціях.",
            "price": 80000,
            "image": "rimac.jpg"
        },
        {
            "brand": "Lucid",
            "country": "США",
            "year": 2007,
            "description": "Lucid створює преміальні електрокари з великим запасом ходу. Модель Air конкурує з Tesla і пропонує розкіш на новому рівні.",
            "price": 37000,
            "image": "lucid.jpg"
        },
        {
            "brand": "BYD",
            "country": "Китай",
            "year": 1995,
            "description": "BYD — один з найбільших виробників електромобілів у світі. Компанія швидко розвивається і пропонує конкурентоспроможні моделі.",
            "price": 26000,
            "image": "byd.jpg"
        },
        {
            "brand": "Tata",
            "country": "Індія",
            "year": 1945,
            "description": "Tata виробляє надійні авто, адаптовані до складних умов доріг. Компанія активно інвестує в електромобілі та бюджетні моделі.",
            "price": 15000,
            "image": "tata.jpg"
        },
        {
            "brand": "Saab",
            "country": "Швеція",
            "year": 1945,
            "description": "Saab — унікальний бренд з авіаційною спадщиною. Відомий своїми безпечними і технологічно розвиненими авто.",
            "price": 26000,
            "image": "saab.jpg"
        },
        {
            "brand": "Lancia",
            "country": "Італія",
            "year": 1906,
            "description": "Lancia мала багату історію в ралі і розробці інновацій. Незважаючи на спад популярності, бренд залишив слід у світі авто.",
            "price": 26000,
            "image": "lancia.jpg"
        },
        {
            "brand": "Rover",
            "country": "Велика Британія",
            "year": 1878,
            "description": "Rover — історичний британський бренд, що поєднував традиції і простоту. Колись був частиною культури середнього класу.",
            "price": 28000,
            "image": "rover.jpg"
        },
        {
            "brand": "Pagani",
            "country": "Італія",
            "year": 1992,
            "description": "Pagani створює унікальні гіперкари ручної збірки. Моделі як Zonda та Huayra — справжнє мистецтво на колесах.",
            "price": 60000,
            "image": "pagani.jpg"
        },
        {
            "brand": "Koenigsegg",
            "country": "Швеція",
            "year": 1994,
            "description": "Koenigsegg виготовляє одні з найшвидших авто у світі. Компанія відома інноваціями та технологічною досконалістю.",
            "price": 59000,
            "image": "koenigsegg.jpg"
        }
    ]
    return render_template("cars.html", cars=car_data)


if __name__ == '__main__':
    app.run(debug=True)