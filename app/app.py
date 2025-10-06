import streamlit as st
import pandas as pd
import sys

from src.db.upload_data import upload_user_data
from src.pipeline.prediction_pipeline import PredictPipeline, CustomData
from config.exception import CustomException


def main():
    st.set_page_config(page_title="Titanic Survival Prediction", layout="centered")
    st.title("🚢 Titanic Survival Prediction")
    st.markdown("Fill in the details below and check if the passenger would have survived.")

    # Collect user input
    sex = st.selectbox("Sex", ["male", "female"]).lower()
    age = st.number_input("Age", min_value=0, max_value=100, value=25)
    sibsp = st.number_input("Number of Siblings/Spouses Aboard (sibsp)", min_value=0, max_value=10, value=0)
    parch = st.number_input("Number of Parents/Children Aboard (parch)", min_value=0, max_value=10, value=0)
    fare = st.number_input("Fare Paid", min_value=0.0, value=32.5)
    embarked = st.selectbox("Port of Embarkation", ["C", "Q", "S"]).lower()
    classes = st.selectbox("Passenger Class", ["First", "Second", "Third"]).lower()
    identity = st.selectbox("Identity", ["man", "woman", "child"]).lower()
    alone = st.selectbox("Traveling Alone", [0, 1]) 

    if st.button("Predict Survival"):
        try:
            # Create custom data instance
            custom_data = CustomData(
                sex=sex,
                age=age,
                sibsp=sibsp,
                parch=parch,
                fare=fare,
                embarked=embarked,
                classes=classes,
                identity=identity,
                alone=alone
            )

            # Convert to DataFrame
            input_df = custom_data.get_data_as_frame()

            # Prediction
            pipeline = PredictPipeline()
            prediction = pipeline.predict(input_df)

            # Show result
            if prediction == 1:
                st.success("✅ The passenger would have SURVIVED.")
            else:
                st.error("❌ The passenger would NOT have survived.")

            # Save input + prediction to MongoDB
            user_record = input_df.to_dict(orient="records")[0]
            user_record["prediction"] = int(prediction)
            upload_user_data(user_record)
            st.info("📁 Passenger data has been saved to MongoDB.")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    main()
