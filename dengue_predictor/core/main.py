# ==========================================
# DENGUE RISK PREDICTION - LOCAL INFERENCE
# ==========================================

# 1️⃣ Import necessary libraries
import joblib
import pandas as pd

# 2️⃣ Load the trained Logistic Regression model
model_path = "models\logistic_regression_model.joblib"  # <-- change path if needed
loaded_model = joblib.load(model_path)
print(f"✅ Model loaded successfully from '{model_path}'")

# 3️⃣ Get the feature columns used during training
# (The model stores them automatically if trained with sklearn >= 1.0)
feature_columns = loaded_model.feature_names_in_
print(f"📊 Feature columns loaded ({len(feature_columns)} total).")

# 4️⃣ Create a new data point (example)
#    This should reflect the same structure as your training data.
#    Example: A 35-year-old Male, NS1 positive, IgG positive, IgM negative,
#    from Mirpur (Undeveloped Area, Building HouseType, District Dhaka)

new_data_raw = {
    'Gender': [1],   # Male = 1, Female = 0
    'Age': [35],
    'NS1': [1],      # NS1 positive
    'IgG': [1],      # IgG positive
    'IgM': [0]       # IgM negative
}

# Convert to DataFrame
new_df = pd.DataFrame(new_data_raw)

# 5️⃣ Initialize all one-hot encoded columns (from training set) to 0
for col in feature_columns:
    if col not in new_df.columns:
        new_df[col] = 0

# 6️⃣ Set the one-hot encoded columns for the selected attributes
new_df.loc[0, 'Area_Mirpur'] = 1
new_df.loc[0, 'AreaType_Undeveloped'] = 1
new_df.loc[0, 'District_Dhaka'] = 1
new_df.loc[0, 'HouseType_Building'] = 1

# 7️⃣ Ensure the correct column order
new_data_for_prediction = new_df[feature_columns]

print("\n🧾 Prepared Input Data for Prediction:")
print(new_data_for_prediction.head())

# 8️⃣ Make the prediction
prediction = loaded_model.predict(new_data_for_prediction)
probability = loaded_model.predict_proba(new_data_for_prediction)[0][1]

# 9️⃣ Output the result
print("\n🎯 Predicted Outcome:")
print(f"Class: {prediction[0]}  (0 = Not Affected, 1 = Dengue Affected)")
print(f"Predicted Probability of Dengue: {probability:.2%}")

if prediction[0] == 1:
    print("⚠️ The model predicts this individual is likely to be DENGUE AFFECTED.")
else:
    print("✅ The model predicts this individual is NOT LIKELY to be affected by Dengue.")
