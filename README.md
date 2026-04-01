Eco-Plate: Carbon Footprint Prediction System

Project Overview



Eco-Plate is a Machine Learning-based web application that predicts the carbon footprint (CO₂ emissions) of food dishes based on their ingredients. The system helps promote sustainable food choices.



Features

Predicts CO₂ emissions using ML model (XGBoost)

Ingredient-based analysis (meat, dairy, vegetables, grains)

Interactive web interface (Django)

Data-driven insights for sustainability

Machine Learning Model

Algorithm: XGBoost Regressor

Features:

meat\_count

dairy\_count

veg\_count

grain\_count

ratios (veg\_ratio, meat\_ratio, dairy\_ratio)

Target:

total\_co2



Dataset

Custom dataset with engineered features:

Ingredient counts

Ingredient ratios

Total CO₂ emissions



🖥️ Tech Stack

Python

Django

SQLite

Scikit-learn / XGBoost

Power BI (for visualization)

How to Run

git clone https://github.com/mj-lordy/Eco-Plate.git

cd Eco-Plate

python manage.py runserver



Objective

To raise awareness about environmental impact of food choices using Machine Learning.



📌 Future Enhancements

Real-time API integration

Mobile app version

Advanced ML models



👤 Author



Miraclin Jeyalordy

