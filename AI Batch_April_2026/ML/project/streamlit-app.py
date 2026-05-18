import streamlit as st
import requests
import re

st.set_page_config(
    page_title="Titanic Survival Prediction",
    page_icon="🚢",
    layout="centered"
)

st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #0B5394;
    text-align: center;
}
.sub-title {
    text-align: center;
    color: #666666;
    font-size: 18px;
}
.result-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
.survived {
    background-color: #D9EAD3;
    color: #274E13;
}
.not-survived {
    background-color: #F4CCCC;
    color: #990000;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚢 Titanic Survival Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enter basic passenger details and predict survival result</div>', unsafe_allow_html=True)

#url = "http://localhost:8080/predict/"
url = "http://135.782.890:8080/predict/"

st.divider()

with st.form("prediction_form"):

    st.subheader("👤 Passenger Basic Details")

    col1, col2 = st.columns(2)

    with col1:
        Age = st.number_input("Age", min_value=0, max_value=100, value=25)
        Sex = st.selectbox("Sex", ["male", "female"])
        Pclass = st.selectbox(
            "Passenger Class",
            [1, 2, 3],
            format_func=lambda x: f"Class {x}"
        )

    with col2:
        Fare = st.number_input("Fare", min_value=0.0, value=34.6)
        Embarked = st.selectbox(
            "Embarked Port",
            ["S", "C", "Q"],
            format_func=lambda x: {
                "S": "S - Southampton",
                "C": "C - Cherbourg",
                "Q": "Q - Queenstown"
            }[x]
        )

    with st.expander("Optional details"):
        PassengerId = st.number_input("Passenger ID", min_value=1, value=100)
        Parch = st.number_input("Parents / Children Aboard", min_value=0, max_value=10, value=0)
        SibSp = st.number_input("Siblings / Spouse Aboard", min_value=0, max_value=10, value=0)
        Ticket = st.text_input("Ticket Number", value="XXX")
        Cabin = st.text_input("Cabin", value="X")

    submitted = st.form_submit_button("🔍 Predict Survival")

if submitted:

    data = [{
        "Age": Age,
        "PassengerId": PassengerId,
        "Sex": Sex,
        "Fare": Fare,
        "Pclass": Pclass,
        "Embarked": Embarked,
        "Parch": Parch,
        "SibSp": SibSp,
        "Ticket": Ticket,
        "Cabin": Cabin
    }]

    try:
        r = requests.post(url, json=data)

        if r.status_code == 200:
            result = r.json()
            raw_prediction = str(result.get("prediction", ""))

            numbers = re.findall(r"\d+", raw_prediction)
            prediction_value = int(numbers[0]) if numbers else None

            st.divider()
            st.subheader("🎯 Prediction Result")

            if prediction_value == 1:
                st.markdown(
                    '<div class="result-box survived">✅ Survived<br>Prediction Value: 1</div>',
                    unsafe_allow_html=True
                )
            elif prediction_value == 0:
                st.markdown(
                    '<div class="result-box not-survived">❌ Not Survived<br>Prediction Value: 0</div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("Prediction received, but value could not be understood.")
                st.write(result)

            with st.expander("View API Response"):
                st.json(result)

        else:
            st.error("Backend error. Please check Flask service.")
            st.write(r.text)

    except Exception as e:
        st.error("Could not connect to Flask backend.")
        st.info("Please make sure Flask backend is running on http://localhost:8080")
        st.write(e)