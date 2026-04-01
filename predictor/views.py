import joblib
import os
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')
# Load model
model_path = os.path.join(os.path.dirname(__file__), 'xgboost_model.pkl')
model = joblib.load(model_path)
# Load recipes dataset
recipes_path = os.path.join(os.path.dirname(__file__), 'recipes.csv')
recipes_df = pd.read_csv(recipes_path)

def predict(request):
    try:
        # Input values
        meat = float(request.GET.get('meat_count', 0))
        dairy = float(request.GET.get('dairy_count', 0))
        veg = float(request.GET.get('veg_count', 0))
        grain = float(request.GET.get('grain_count', 0))
        total = float(request.GET.get('total_ingredients', 1))

        # Feature engineering
        high_impact = meat + dairy

        veg_ratio = veg / total if total != 0 else 0
        meat_ratio = meat / total if total != 0 else 0
        dairy_ratio = dairy / total if total != 0 else 0

        # Final feature vector
        features = [[
            meat,
            dairy,
            veg,
            grain,
            total,
            high_impact,
            veg_ratio,
            meat_ratio,
            dairy_ratio
        ]]

        # Prediction
        prediction = float(model.predict(features)[0])


        return JsonResponse({
            "predicted_co2": round(prediction, 2)
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        })
def predict_dish(request):
    try:
        # Get dish name
        dish = request.GET.get('dish', '').lower().strip()

        # Find dish in dataset
        row = recipes_df[recipes_df['dish'] == dish]

        if row.empty:
            return JsonResponse({"error": "Dish not found"})

        # Extract ingredients
        ingredients = row.iloc[0]['ingredients'].split('|')

        # CATEGORY LISTS
        meat_items = ["chicken","beef","fish","lamb"]
        dairy_items = ["milk","cheese","butter","cream","yogurt","ghee"]
        veg_items = ["onion","tomato","carrot","beans","potato","spinach","okra","vegetables"]
        grain_items = ["rice","flour","bread","pasta","noodle","semolina"]

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

        # MODEL INPUT
        features = [[
            meat, dairy, veg, grain,
            total, high_impact,
            veg_ratio, meat_ratio, dairy_ratio
        ]]

        # Prediction
        prediction = float(model.predict(features)[0])

        return JsonResponse({
            "dish": dish,
            "ingredients": ingredients,
            "predicted_co2": round(prediction, 2)
        })

    except Exception as e:
        return JsonResponse({"error": str(e)})