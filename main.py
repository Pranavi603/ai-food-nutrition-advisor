from fastapi import FastAPI, Form, Request, UploadFile, File, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

food_data = {

# Grains / Staple foods
"rice": {"calories":130,"protein":2.7,"carbs":28,"fats":0.3,"sugar":0,"fiber":0.4,"vitamins":1,"minerals":1,"water":68},
"chapathi": {"calories":120,"protein":3,"carbs":20,"fats":1,"sugar":0,"fiber":2,"vitamins":1,"minerals":1,"water":60},
"roti": {"calories":110,"protein":3,"carbs":18,"fats":0.8,"sugar":0,"fiber":2,"vitamins":1,"minerals":1,"water":60},
"brown rice": {"calories":123,"protein":2.6,"carbs":25,"fats":1,"sugar":0,"fiber":1.8,"vitamins":1,"minerals":2,"water":70},
"bread": {"calories":79,"protein":3,"carbs":15,"fats":1,"sugar":2,"fiber":1.5,"vitamins":1,"minerals":1,"water":35},
"poha": {"calories":180,"protein":4,"carbs":30,"fats":5,"sugar":1,"fiber":2,"vitamins":1,"minerals":1,"water":60},
"upma": {"calories":210,"protein":6,"carbs":35,"fats":7,"sugar":1,"fiber":3,"vitamins":1,"minerals":1,"water":55},
"idli": {"calories":58,"protein":2,"carbs":12,"fats":0.4,"sugar":0,"fiber":0.5,"vitamins":1,"minerals":1,"water":65},
"dosa": {"calories":168,"protein":5,"carbs":25,"fats":6,"sugar":1,"fiber":1,"vitamins":1,"minerals":1,"water":50},
"paratha": {"calories":260,"protein":6,"carbs":40,"fats":10,"sugar":1,"fiber":3,"vitamins":1,"minerals":1,"water":45},

# Dairy
"milk": {"calories":60,"protein":3.2,"carbs":5,"fats":3.3,"sugar":5,"fiber":0,"vitamins":2,"minerals":2,"water":87},
"paneer": {"calories":265,"protein":18,"carbs":1.2,"fats":20,"sugar":1,"fiber":0,"vitamins":2,"minerals":2,"water":55},
"butter": {"calories":717,"protein":1,"carbs":0,"fats":81,"sugar":0,"fiber":0,"vitamins":2,"minerals":1,"water":16},
"cheese": {"calories":402,"protein":25,"carbs":1.3,"fats":33,"sugar":1,"fiber":0,"vitamins":2,"minerals":3,"water":37},
"yogurt": {"calories":59,"protein":10,"carbs":3.6,"fats":0.4,"sugar":3,"fiber":0,"vitamins":2,"minerals":2,"water":85},
"curd": {"calories":98,"protein":11,"carbs":4,"fats":4,"sugar":3,"fiber":0,"vitamins":2,"minerals":2,"water":80},
"ghee": {"calories":900,"protein":0,"carbs":0,"fats":100,"sugar":0,"fiber":0,"vitamins":2,"minerals":1,"water":0},

# Protein foods
"egg": {"calories":155,"protein":13,"carbs":1.1,"fats":11,"sugar":1,"fiber":0,"vitamins":2,"minerals":2,"water":75},
"chicken": {"calories":239,"protein":27,"carbs":0,"fats":14,"sugar":0,"fiber":0,"vitamins":2,"minerals":3,"water":65},
"fish": {"calories":206,"protein":22,"carbs":0,"fats":12,"sugar":0,"fiber":0,"vitamins":2,"minerals":3,"water":68},
"mutton": {"calories":294,"protein":25,"carbs":0,"fats":21,"sugar":0,"fiber":0,"vitamins":2,"minerals":3,"water":60},
"dal": {"calories":116,"protein":9,"carbs":20,"fats":0.4,"sugar":2,"fiber":8,"vitamins":2,"minerals":2,"water":70},
"chickpeas": {"calories":164,"protein":9,"carbs":27,"fats":2.6,"sugar":5,"fiber":7.6,"vitamins":2,"minerals":2,"water":60},
"rajma": {"calories":127,"protein":8.7,"carbs":22,"fats":0.5,"sugar":2,"fiber":6,"vitamins":2,"minerals":2,"water":68},
"soybeans": {"calories":446,"protein":36,"carbs":30,"fats":20,"sugar":7,"fiber":9,"vitamins":3,"minerals":3,"water":55},

# Vegetables
"potato": {"calories":77,"protein":2,"carbs":17,"fats":0.1,"sugar":2,"fiber":2.2,"vitamins":2,"minerals":1,"water":79},
"tomato": {"calories":18,"protein":0.9,"carbs":3.9,"fats":0.2,"sugar":3,"fiber":1.2,"vitamins":2,"minerals":1,"water":94},
"onion": {"calories":40,"protein":1.1,"carbs":9,"fats":0.1,"sugar":4,"fiber":1.7,"vitamins":1,"minerals":1,"water":89},
"carrot": {"calories":41,"protein":0.9,"carbs":10,"fats":0.2,"sugar":5,"fiber":2.8,"vitamins":3,"minerals":1,"water":88},
"broccoli": {"calories":34,"protein":2.8,"carbs":7,"fats":0.4,"sugar":2,"fiber":2.6,"vitamins":3,"minerals":2,"water":90},
"cabbage": {"calories":25,"protein":1.3,"carbs":6,"fats":0.1,"sugar":3,"fiber":2.5,"vitamins":2,"minerals":1,"water":92},
"spinach": {"calories":23,"protein":2.9,"carbs":3.6,"fats":0.4,"sugar":0,"fiber":2.2,"vitamins":4,"minerals":3,"water":91},
"peas": {"calories":81,"protein":5,"carbs":14,"fats":0.4,"sugar":6,"fiber":5,"vitamins":2,"minerals":2,"water":78},

# Fruits
"apple": {"calories":52,"protein":0.3,"carbs":14,"fats":0.2,"sugar":10,"fiber":2.4,"vitamins":2,"minerals":1,"water":86},
"banana": {"calories":96,"protein":1.3,"carbs":27,"fats":0.3,"sugar":12,"fiber":2.6,"vitamins":3,"minerals":2,"water":75},
"orange": {"calories":47,"protein":0.9,"carbs":12,"fats":0.1,"sugar":9,"fiber":2.4,"vitamins":3,"minerals":1,"water":86},
"mango": {"calories":60,"protein":0.8,"carbs":15,"fats":0.4,"sugar":14,"fiber":1.6,"vitamins":3,"minerals":1,"water":83},
"grapes": {"calories":69,"protein":0.7,"carbs":18,"fats":0.2,"sugar":16,"fiber":0.9,"vitamins":2,"minerals":1,"water":81},
"watermelon": {"calories":30,"protein":0.6,"carbs":8,"fats":0.2,"sugar":6,"fiber":0.4,"vitamins":2,"minerals":1,"water":91},
"pineapple": {"calories":50,"protein":0.5,"carbs":13,"fats":0.1,"sugar":10,"fiber":1.4,"vitamins":2,"minerals":1,"water":86},
"papaya": {"calories":43,"protein":0.5,"carbs":11,"fats":0.3,"sugar":8,"fiber":1.7,"vitamins":3,"minerals":1,"water":88},

# Snacks / Others
"samosa": {"calories":262,"protein":6,"carbs":30,"fats":17,"sugar":2,"fiber":2,"vitamins":1,"minerals":1,"water":40},
"burger": {"calories":295,"protein":17,"carbs":30,"fats":14,"sugar":6,"fiber":2,"vitamins":1,"minerals":1,"water":45},
"pizza": {"calories":266,"protein":11,"carbs":33,"fats":10,"sugar":4,"fiber":2,"vitamins":1,"minerals":1,"water":40},
"noodles": {"calories":138,"protein":5,"carbs":25,"fats":2,"sugar":2,"fiber":1,"vitamins":1,"minerals":1,"water":60},
"fried rice": {"calories":163,"protein":5,"carbs":28,"fats":6,"sugar":2,"fiber":1,"vitamins":1,"minerals":1,"water":55},
"biryani": {"calories":290,"protein":15,"carbs":35,"fats":12,"sugar":1,"fiber":2,"vitamins":1,"minerals":2,"water":50},
"ice cream": {"calories":207,"protein":3.5,"carbs":24,"fats":11,"sugar":21,"fiber":0,"vitamins":1,"minerals":1,"water":60}
}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if username == "admin" and password == "123":
        return RedirectResponse(url="/details", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password"}
    )




@app.get("/details")
def details(request: Request):
    return templates.TemplateResponse("details.html", {"request": request})



@app.post("/chatbot")
async def chatbot(request: Request):

    data = await request.json()
    message = data["message"].lower()

    if "protein" in message:
        reply = "Protein helps build muscles. Good sources are eggs, chicken, paneer and dal."

    elif "egg" in message:
        reply = "Eggs are rich in protein, vitamins and healthy fats."

    elif "rice" in message:
        reply = "Rice is a good source of carbohydrates and energy."

    elif "vitamin" in message:
        reply = "Vitamins support immunity. Fruits and vegetables are good sources."

    else:
        reply = "Eat a balanced diet with protein, carbohydrates, healthy fats and vegetables."

    return {"reply": reply}

import os

@app.post("/predict-food")
async def predict_food(file: UploadFile = File(...)):

    os.makedirs("static/uploads", exist_ok=True)

    file_path = f"static/uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    filename = file.filename.lower()
        
    if "pizza" in filename:
        detected_food = "pizza"
        confidence = 92
            
    elif "burger" in filename:
        detected_food = "burger"
        confidence = 90
                
    elif "apple" in filename:
        detected_food = "apple"
        confidence = 95

    elif "banana" in filename:
        detected_food = "banana"
        confidence = 70
                    
    elif "rice" in filename:
        detected_food = "rice"
        confidence = 80
        
    else:
        detected_food = "burger"
        confidence = 90

    return {
        "food": detected_food,
        "confidence": confidence,
        "image": file_path
    }

@app.get("/food")

def food(request: Request, weight: float, height: float, age: int, disease: str):
    height_m = height * 0.3048
    bmi = weight / (height_m * height_m)

    if bmi < 18.5:
        status = "Underweight"
        suggestion = "Eat calorie rich foods."

    elif bmi < 25:
        status = "Normal weight"
        suggestion = "Maintain balanced diet."

    elif bmi < 30:
        status = "Overweight"
        suggestion = "Reduce sugar and fried foods."

    else:
        status = "Obese"
        suggestion = "Focus on vegetables and exercise."

    daily_calories = weight * 30

    return templates.TemplateResponse(
        "food.html",
        {
            "request": request,
            "age": age,
            "disease": disease,
            "bmi": round(bmi, 2),
            "status": status,
            "suggestion": suggestion,
            "daily_calories": round(daily_calories),
            "weight": weight,
            "height": height
        }
    )


@app.post("/analyze")
def analyze_food(
    request: Request,
    image_path: str = Form(None),
    status: str = Form(""),
    
    food1: str = Form(""),
    qty1: float = Form(0),
    unit1: str = Form("grams"),

    food2: str = Form(""),
    qty2: float = Form(0),
    unit2: str = Form("grams"),

    food3: str = Form(""),
    qty3: float = Form(0),
    unit3: str = Form("grams")
):



    # Convert count → grams for some foods
    count_to_grams = {
        "egg": 50,
        "banana": 120,
        "apple": 180,
        "chapathi": 40,
        "roti": 40,
        "idli": 35
    }

    # Prepare food list
    foods = []

    items = [
        (food1, qty1, unit1),
        (food2, qty2, unit2),
        (food3, qty3, unit3)
    ]

    for food, qty, unit in items:

        food = food.lower()

        if unit == "count" and food in count_to_grams:
            qty = qty * count_to_grams[food]

        foods.append((food, qty))


    # Nutrition totals
    calories = 0
    protein = 0
    carbs = 0
    fats = 0
    sugar = 0
    fiber = 0
    vitamins = 0
    minerals = 0
    water = 0


    # Calculate nutrition
    for item, quantity in foods:

        if item in food_data and quantity > 0:

            factor = quantity / 100

            calories += food_data[item]["calories"] * factor
            protein += food_data[item]["protein"] * factor
            carbs += food_data[item]["carbs"] * factor
            fats += food_data[item]["fats"] * factor
            sugar += food_data[item]["sugar"] * factor
            fiber += food_data[item]["fiber"] * factor
            vitamins += food_data[item]["vitamins"] * factor
            minerals += food_data[item]["minerals"] * factor
            water += food_data[item]["water"] * factor


    # Health advice system

    advice_list = []
    
    # Nutrition advice
    
    if calories > 250:
        advice_list.append("This meal contains moderate calories.")
    
    if fats >= 10:
        advice_list.append("Fat content is high. Avoid frequent fast food.")
    
    if sugar >= 10:
        advice_list.append("Sugar intake is high.")
    
    if protein < 12:
        advice_list.append("Protein intake is slightly low. Consider adding protein foods.")
    
    
    # BMI advice
    
    status = status.strip().lower()
    
    if status == "overweight":
        advice_list.append("Your BMI indicates overweight. Reduce fried foods.")
    
    elif status == "underweight":
        advice_list.append("Your BMI is low. Increase protein intake.")
    
    elif status == "normal weight":
        advice_list.append("Your BMI is healthy.")
    
    
    if not advice_list:
        advice_list.append("Your meal looks balanced.")
    
    advice = " ".join(advice_list)
    
    # Health Score Calculation (0 - 100)
    
    health_score = 100
    
    if calories > 800:
        health_score -= 20

    if protein < 10:
        health_score -= 20

    if sugar > 25:
        health_score -= 20

    if fats > 15:
        health_score -= 20

    if fiber < 3:
        health_score -= 10

    if health_score < 0:
        health_score = 0
    
    # Return result page
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "image_path": image_path,
             
            "food1": food1,
            "qty1": qty1,
            "food2": food2,
            "qty2": qty2,
            "food3": food3,
            "qty3": qty3,

            "calories": round(calories,2),
            "protein": round(protein,2),
            "carbs": round(carbs,2),
            "fats": round(fats,2),
            "sugar": round(sugar,2),
            "fiber": round(fiber,2),
            "vitamins": round(vitamins,2),
            "minerals": round(minerals,2),
            "water": round(water,2),

            "advice": advice,
            "health_score": health_score
        }
)
