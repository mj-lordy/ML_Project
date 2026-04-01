import joblib
import os
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render

# Home Page
def home(request):
    return render(request, 'index.html')

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'xgboost_model.pkl')
model = joblib.load(model_path)

# Load recipes dataset
recipes_path = os.path.join(os.path.dirname(__file__), 'recipes.csv')
recipes_df = pd.read_csv(recipes_path)

# =========================
# 🔹 MANUAL INPUT PREDICTION
# =========================
def predict(request):
    try:
        meat = float(request.GET.get('meat_count', 0))
        dairy = float(request.GET.get('dairy_count', 0))
        veg = float(request.GET.get('veg_count', 0))
        grain = float(request.GET.get('grain_count', 0))
        total = float(request.GET.get('total_ingredients', 1))

        # FEATURE ENGINEERING
        high_impact = meat + dairy

        veg_ratio = veg / total if total != 0 else 0
        meat_ratio = meat / total if total != 0 else 0
        dairy_ratio = dairy / total if total != 0 else 0

        # 🔥 CO2 ESTIMATION FEATURES (IMPORTANT)
        meat_co2_est = meat * 5
        dairy_co2_est = dairy * 3
        veg_co2_est = veg * 1
        grain_co2_est = grain * 1.5

        # FINAL FEATURE VECTOR (13 FEATURES)
        features = [[
            meat,
            dairy,
            veg,
            grain,
            total,
            high_impact,
            veg_ratio,
            meat_ratio,
            dairy_ratio,
            meat_co2_est,
            dairy_co2_est,
            veg_co2_est,
            grain_co2_est
        ]]

        prediction = float(model.predict(features)[0])

        return JsonResponse({
            "predicted_co2": round(prediction, 2)
        })

    except Exception as e:
        return JsonResponse({"error": str(e)})


# =========================
# 🔹 DISH-BASED PREDICTION
# =========================
def predict_dish(request):
    try:
        dish = request.GET.get('dish', '').lower().strip()

        row = recipes_df[recipes_df['dish'] == dish]

        if row.empty:
            return JsonResponse({"error": "Dish not found"})

        ingredients = row.iloc[0]['ingredients'].split('|')

        # CATEGORY LISTS
        meat_items = ["chicken", "beef", "fish", "lamb"]
        dairy_items = ["milk", "cheese", "butter", "cream", "yogurt", "ghee"]
        veg_items = ["onion", "tomato", "carrot", "beans", "potato", "spinach", "okra", "vegetables"]
        grain_items = ["rice", "flour", "bread", "pasta", "noodle", "semolina"]

        # COUNTING
        meat = sum(1 for i in ingredients if i in meat_items)
        dairy = sum(1 for i in ingredients if i in dairy_items)
        veg = sum(1 for i in ingredients if i in veg_items)
        grain = sum(1 for i in ingredients if i in grain_items)

        total = len(ingredients)

        # FEATURE ENGINEERING
        high_impact = meat + dairy
        veg_ratio = veg / total if total != 0 else 0
        meat_ratio = meat / total if total != 0 else 0
        dairy_ratio = dairy / total if total != 0 else 0

        # 🔥 CO2 ESTIMATION FEATURES
        meat_co2_est = meat * 5
        dairy_co2_est = dairy * 3
        veg_co2_est = veg * 1
        grain_co2_est = grain * 1.5

        # FINAL FEATURE VECTOR (13 FEATURES)
        features = [[
            meat,
            dairy,
            veg,
            grain,
            total,
            high_impact,
            veg_ratio,
            meat_ratio,
            dairy_ratio,
            meat_co2_est,
            dairy_co2_est,
            veg_co2_est,
            grain_co2_est
        ]]

        prediction = float(model.predict(features)[0])

        return JsonResponse({
            "dish": dish,
            "ingredients": ingredients,
            "predicted_co2": round(prediction, 2)
        })

    except Exception as e:
        return JsonResponse({"error": str(e)})
