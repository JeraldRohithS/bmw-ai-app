# ============================================
# BMW AI RECOMMENDATION SYSTEM
# ============================================

import pandas as pd
import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ============================================
# UI CONFIG + CSS
# ============================================
st.set_page_config(page_title="BMW AI Experience", layout="wide")

st.markdown("""
<style>

*{
    transition:none !important;
    animation:none !important;
}

html, body, .stApp{
    opacity:1 !important;
    scroll-behavior:auto !important;
}

[data-testid="stDecoration"]{
    display:none !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
section.main{
    animation:none !important;
    transition:none !important;
}

body{
    background-color:#0a0a0a;
    color:white;
    font-family:'Segoe UI';
}

.card{
    background:#111;
    padding:20px;
    border-radius:12px;
    box-shadow:0 4px 25px rgba(0,0,0,0.6);
}

.stButton>button{
    background:white;
    color:black;
    height:45px;
    border:none;
}
            
.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# LOGIN SYSTEM
# ============================================

users = pd.read_csv("users.csv")

def login(u, p):
    return ((users['username'] == u) & (users['password'] == p)).any()

# Always initialize first
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
    <style>
    .login-box {
    width: 280px;
    padding: 25px;
    border-radius: 16px;
    }
    text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.markdown("<h2>BMW AI System</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa'>Sheer Driving Intelligence</p>", unsafe_allow_html=True)

    u = st.text_input("Username", label_visibility="collapsed", placeholder="Username")
    p = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Password")

    if st.button("Sign In", use_container_width=True):
        if login(u, p):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

    st.markdown("""
<div style='padding:20px; margin-bottom:20px;
...
</div>
""", unsafe_allow_html=True)

# ============================================
# DATASET
# ============================================
data = []

for budget in range(40, 201, 5):
    for family in [2,4,5]:
        for usage in ["city","family","luxury"]:

            if budget < 60:
                car = "BMW 2 Series Gran Coupe"
            elif budget < 80:
               car = "BMW 3 Series Gran Limousine"
            elif budget < 100:
               car = "BMW X1"
            elif budget < 120:
               car = "BMW X3"
            elif budget < 140:
               car = "BMW 5 Series"
            elif budget < 160:
               car = "BMW X5"
            elif budget < 180:
               car = "BMW 7 Series"
            elif budget < 190:
               car = "BMW X7"
            elif budget < 200:
               car = "BMW M4 Competition"
            else:
               car = "BMW M5"

            data.append([budget, family, usage, car])

df = pd.DataFrame(data, columns=["budget","family_size","usage","car_model"])

usage_map = {"city":0,"family":1,"luxury":2}
df["usage"] = df["usage"].map(usage_map)

# Add extra features
df["luxury_score"] = df["budget"] * df["usage"]
df["family_weight"] = df["family_size"] * df["budget"]

# Updated features
X = df[["budget","family_size","usage","luxury_score","family_weight"]]
y = df["car_model"]

# ============================================
# MODEL
# ============================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=2,
    random_state=42
)
model.fit(X_train, y_train)

accuracy = accuracy_score(y, model.predict(X))


aaccuracy = accuracy_score(y, model.predict(X))

def recommend_car(b, f, u):
    usage_val = usage_map[u]

    luxury_score = b * usage_val
    family_weight = f * b

    return model.predict([[b, f, usage_val, luxury_score, family_weight]])[0]

# ============================================
# FULL BMW DATABASE
# ============================================
car_data = {
    "BMW 2 Series Gran Coupe": {
        "price": "₹43L - ₹46L",
        "type": "Compact Sedan",
        "engine": "2.0L Turbo Petrol/Diesel",
        "power": "189 bhp",
        "torque": "280 Nm",
        "acceleration": "7.1 sec",
        "top_speed": "240 km/h",
        "fuel_type": "Petrol/Diesel",
        "mileage": "14-18 km/l",
        "transmission": "7-Speed Automatic",
        "drive": "FWD",
        "seats": "5",
        "boot": "380L",
        "desc": "Entry-level luxury sedan with sporty styling and sharp handling.",
        "img": "https://www.usnews.com/object/image/00000199-0a5d-da09-abdb-7afd8bdf0000/usnpx-2026bmw2series-angularfront2-zd.jpg?update-time=1756815526721&size=responsiveGallery&format=webp"
    },

    "BMW 3 Series Gran Limousine": {
        "price": "₹60L - ₹65L",
        "type": "Luxury Sedan",
        "engine": "2.0L Turbo Petrol/Diesel",
        "power": "255 bhp",
        "torque": "400 Nm",
        "acceleration": "6.2 sec",
        "top_speed": "250 km/h",
        "fuel_type": "Petrol/Diesel",
        "mileage": "15-19 km/l",
        "transmission": "8-Speed Automatic",
        "drive": "RWD",
        "seats": "5",
        "boot": "480L",
        "desc": "Extended wheelbase sedan focused on comfort and driving dynamics.",
        "img": "https://www.carandbike.com/_next/image?url=https%3A%2F%2Fimages.carandbike.com%2Fcar-images%2Fgallery%2Fbmw%2F3-series%2Fexterior%2Fbmw-m340i_3.jpg%3Fv%3D1752928851&w=1920&q=90"
    },

    "BMW 5 Series": {
        "price": "₹72L - ₹85L",
        "type": "Executive Sedan",
        "engine": "2.0L Petrol / Electric (i5)",
        "power": "255 bhp / 335 bhp (EV)",
        "torque": "400 Nm / 430 Nm",
        "acceleration": "6.0 sec",
        "top_speed": "250 km/h",
        "fuel_type": "Petrol/Electric",
        "mileage": "15 km/l / 500 km range",
        "transmission": "8-Speed Automatic",
        "drive": "RWD",
        "seats": "5",
        "boot": "520L",
        "desc": "Premium executive sedan with modern tech and comfort.",
        "img": "https://di-uploads-pod20.dealerinspire.com/sewickleybmw/uploads/2025/02/25-BMW-5-Series-Exterior.jpg"
    },

    "BMW 7 Series": {
        "price": "₹1.80Cr - ₹2.0Cr",
        "type": "Luxury Sedan",
        "engine": "3.0L Turbo / Electric (i7)",
        "power": "375 bhp / 536 bhp (EV)",
        "torque": "520 Nm / 745 Nm",
        "acceleration": "4.7 sec",
        "top_speed": "250 km/h",
        "fuel_type": "Petrol/Electric",
        "mileage": "12 km/l / 600 km range",
        "transmission": "8-Speed Automatic",
        "drive": "RWD/AWD",
        "seats": "5",
        "boot": "540L",
        "desc": "Flagship luxury sedan with top-tier comfort and innovation.",
        "img": "https://www.motorbeam.com/wp-content/uploads/2026-BMW-7-Series-Facelift.jpg"
    },

    "BMW X1": {
        "price": "₹50L - ₹55L",
        "type": "Compact SUV",
        "engine": "1.5L Turbo Petrol / 2.0L Diesel",
        "power": "136 bhp / 150 bhp",
        "torque": "230 Nm / 360 Nm",
        "acceleration": "8.9 sec",
        "top_speed": "210 km/h",
        "fuel_type": "Petrol/Diesel",
        "mileage": "16-20 km/l",
        "transmission": "7-Speed Automatic",
        "drive": "FWD",
        "seats": "5",
        "boot": "500L",
        "desc": "Entry luxury SUV with practicality and premium feel.",
        "img": "https://www.carandbike.com/_next/image?url=https%3A%2F%2Fimages.carandbike.com%2Fcar-images%2Fgallery%2Fbmw%2Fx1%2Fexterior%2Fbmw_x1_headlight.jpg%3Fv%3D1752928333&w=1920&q=90"
    },

    "BMW X3": {
        "price": "₹68L - ₹75L",
        "type": "Mid-size SUV",
        "engine": "2.0L Petrol/Diesel",
        "power": "190-252 bhp",
        "torque": "350-400 Nm",
        "acceleration": "6.6 - 7.9 sec",
        "top_speed": "230 km/h",
        "fuel_type": "Petrol/Diesel",
        "mileage": "13-16 km/l",
        "transmission": "8-Speed Automatic",
        "drive": "AWD (xDrive)",
        "seats": "5",
        "boot": "550L",
        "desc": "Balanced SUV with performance and comfort.",
        "img": "https://hips.hearstapps.com/hmg-prod/images/2025-bmw-x3-xdrive30-228-687fec9f6b2e8.jpg?crop=0.721xw:0.541xh;0.228xw,0.356xh&resize=1200:*"
    },

    "BMW X5": {
        "price": "₹96L - ₹1.10Cr",
        "type": "Premium SUV",
        "engine": "3.0L Petrol/Diesel",
        "power": "335-375 bhp",
        "torque": "450-520 Nm",
        "acceleration": "5.5 sec",
        "top_speed": "250 km/h",
        "fuel_type": "Petrol/Diesel",
        "mileage": "11-14 km/l",
        "transmission": "8-Speed Automatic",
        "drive": "AWD",
        "seats": "5",
        "boot": "650L",
        "desc": "Luxury SUV combining power, space, and tech.",
        "img": "https://media.ed.edmunds-media.com/bmw/x5/2026/oem/2026_bmw_x5_4dr-suv_xdrive40i_fq_oem_1_1280.jpg"
    },

    "BMW X7": {
        "price": "₹1.25Cr - ₹1.35Cr",
        "type": "Flagship SUV",
        "engine": "3.0L Petrol/Diesel",
        "power": "375 bhp",
        "torque": "520 Nm",
        "acceleration": "5.8 sec",
        "top_speed": "245 km/h",
        "fuel_type": "Petrol/Diesel",
        "mileage": "10-12 km/l",
        "transmission": "8-Speed Automatic",
        "drive": "AWD",
        "seats": "6/7",
        "boot": "750L",
        "desc": "Full-size luxury SUV with 6/7-seat comfort.",
        "img": "https://hips.hearstapps.com/mtg-prod/683f7131cb545200086c04f6/1-2026-bmw-x7-m60i-front-view.jpg?w=768&width=768&q=75&format=webp"
    },

    "BMW M4 Competition": {
        "price": "₹1.50Cr - ₹1.60Cr",
        "type": "Performance Coupe",
        "engine": "3.0L Twin-Turbo Inline-6",
        "power": "503 bhp",
        "torque": "650 Nm",
        "acceleration": "3.5 sec",
        "top_speed": "290 km/h",
        "fuel_type": "Petrol",
        "mileage": "9-10 km/l",
        "transmission": "8-Speed Automatic",
        "drive": "RWD/AWD",
        "seats": "4",
        "boot": "440L",
        "desc": "High-performance coupe built for track and road.",
        "img": "https://imagecdn.zigwheels.ae/large/gallery/exterior/4/1334/bmw-m4-15639.jpg"
    },

    "BMW M5": {
        "price": "₹1.90Cr - ₹2.10Cr",
        "type": "Performance Sedan",
        "engine": "4.4L Twin-Turbo V8 Hybrid",
        "power": "717 bhp",
        "torque": "1000 Nm",
        "acceleration": "3.5 sec",
        "top_speed": "305 km/h",
        "fuel_type": "Hybrid",
        "mileage": "8-10 km/l",
        "transmission": "8-Speed Automatic",
        "drive": "AWD",
        "seats": "5",
        "boot": "530L",
        "desc": "Super sedan with extreme performance and luxury.",
        "img": "https://media.ed.edmunds-media.com/bmw/m5/2026/oem/2026_bmw_m5_sedan_base_fq_oem_1_600.jpg"
    }
}

# ============================================
# UI NAVIGATION
# ============================================
st.title("BMW AI Experience")

menu = st.sidebar.selectbox("Navigation", ["Recommendation", "Analytics"])

# ============================================
# RECOMMENDATION (HR APPROVED PRO UI)
# ============================================
if menu == "Recommendation":

    st.markdown("""
    <style>

    .title-main{
        font-size:42px;
        font-weight:700;
        margin-bottom:8px;
    }

    .subtitle{
        color:#8a8a8a;
        margin-bottom:30px;
        font-size:15px;
    }

    .glass{
        background:rgba(255,255,255,0.04);
        border:1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border-radius:18px;
        padding:28px;
        box-shadow:0 10px 30px rgba(0,0,0,0.35);
        transition:0.15s ease;
    }

    .glass:hover{
        transform:translateY(-4px);
        box-shadow:0 15px 35px rgba(255,255,255,0.05);
    }

    .metric-box{
        background:#111;
        padding:16px;
        border-radius:14px;
        margin-top:15px;
    }

    .car-img img{
        border-radius:16px;
        transition:0.4s;
    }

    .car-img img:hover{
        transform:scale(1.03);
    }
                
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title-main'>BMW Smart Recommendation</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Luxury • Intelligence • Performance</div>", unsafe_allow_html=True)

    left, right = st.columns([1.1,1])

    # LEFT SIDE
    with left:

        budget = st.slider("Select Budget (₹ Lakhs)", 40, 200, 80, step=5)

        family = st.selectbox("Family Members", [2,4,5])

        usage = st.selectbox(
            "Usage Purpose",
            ["city","family","luxury"]
        )

        recommend_clicked = st.button(
            "Find BMW",
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if recommend_clicked:

            result = recommend_car(budget, family, usage)
            car = car_data[result]

            confidence = np.max(
                model.predict_proba([[
                    budget,
                    family,
                    usage_map[usage],
                    budget * usage_map[usage],
                    family * budget
                ]])
            ) * 100

            st.metric("Model Accuracy", f"{round(accuracy*100,2)}%")

            st.progress(int(confidence))
            st.caption(f"AI Confidence: {round(confidence,2)}%")

            st.markdown("<div class='car-img'>", unsafe_allow_html=True)
            st.image(car["img"], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='metric-box'>
            <h2>{result}</h2>
            <p><b>Price:</b> {car['price']}</p>
            <p><b>Engine:</b> {car['engine']}</p>
            <p><b>Power:</b> {car['power']}</p>
            <p><b>Top Speed:</b> {car['top_speed']}</p>
            <p>{car['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # RIGHT SIDE
    with right:

        st.markdown("""
        <div class='glass'>

        <h1>Why BMW?</h1>

        <p>✔ German Engineering Precision</p>
        <p>✔ Premium Luxury Cabin</p>
        <p>✔ Strong Resale Value</p>
        <p>✔ Intelligent Driving Tech</p>
        <p>✔ Class-Leading Performance</p>

        <hr>

        <h2>Popular Picks</h2>

        <p>• X1 – Urban SUV</p>
        <p>• X5 – Luxury Powerhouse</p>
        <p>• 5 Series – Executive Sedan</p>
        <p>• M5 – Ultimate Beast</p>

        <hr>

        <h2>Brand Value</h2>
        <p>BMW ranked among world's top luxury car brands.</p>

        </div>
        """, unsafe_allow_html=True)
# ============================================
# ANALYTICS
# ============================================
if menu == "Analytics":

    st.subheader("Vehicle Intelligence Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Budget Distribution")
        st.bar_chart(df["budget"])

    with col2:
        st.write("Family Size Trends")
        st.area_chart(df["family_size"])

    st.markdown("---")

    st.metric("Model Accuracy", f"{round(accuracy*100,2)}%")
    st.caption("Model trained on structured automotive decision dataset")

    sales_data = pd.DataFrame({
        "Model": ["X1","X3","X5","X7","3 Series","5 Series","7 Series"],
        "Sales": [1200,1800,1500,900,2000,1700,800]
    })

    st.write("BMW Sales Performance")
    st.bar_chart(sales_data.set_index("Model"))

    st.write("Sales Trend")
    st.line_chart(sales_data.set_index("Model"))

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.caption("BMW AI System | Developed by Jerald")
st.markdown("""
<div style='text-align:center; color:#666; padding:20px'>
© 2026 BMW AI Experience | Developed for Intelligent Automotive Systems
</div>
""", unsafe_allow_html=True)