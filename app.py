import gradio as gr
import requests
from google import genai

client = genai.Client(
    api_key="YOUR-API-KEY"
)

# ----------------------------------
# Crop Recommendation
# ----------------------------------

def crop_recommend(location, soil, season):

    prompt = f"""
    Recommend top 5 crops.

    Location: {location}
    Soil: {soil}
    Season: {season}

    Give short reasons.
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text


# ----------------------------------
# Agriculture Chatbot
# ----------------------------------

def agri_chat(crop, question):

    prompt = f"""
    You are an agriculture expert.

    Crop: {crop}

    Question:
    {question}

    Give practical advice.
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text


# ----------------------------------
# Weather Advice
# ----------------------------------

def weather_advice(location):

    try:

        weather = requests.get(
            f"https://wttr.in/{location}?format=j1"
        ).json()

        temp = weather["current_condition"][0]["temp_C"]
        humidity = weather["current_condition"][0]["humidity"]

        weather_info = f"""
Temperature: {temp}°C
Humidity: {humidity}%
"""

    except:
        weather_info = "Weather unavailable"

    prompt = f"""
    Location: {location}

    Weather:
    {weather_info}

    Give farming advice.

    Mention:
    - Irrigation
    - Fertilizer
    - Pest control
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text


# ----------------------------------
# Disease Information
# ----------------------------------

def disease_info(disease):

    prompt = f"""
    Disease:
    {disease}

    Explain:

    1. Symptoms
    2. Causes
    3. Remedies
    4. Prevention

    Keep it farmer friendly.
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text


# ==================================
# Gradio UI
# ==================================

with gr.Blocks(title="Smart Agriculture Advisor") as demo:

    gr.Markdown("# 🌾 Smart Agriculture Advisor")

    with gr.Tab("Crop Recommendation"):

        location = gr.Textbox(label="Location")
        soil = gr.Textbox(label="Soil Type")
        season = gr.Textbox(label="Season")

        output1 = gr.Textbox(lines=10)

        btn1 = gr.Button("Recommend Crops")

        btn1.click(
            crop_recommend,
            [location, soil, season],
            output1
        )

    with gr.Tab("Agriculture Chatbot"):

        crop = gr.Textbox(label="Crop Name")
        question = gr.Textbox(label="Question")

        output2 = gr.Textbox(lines=10)

        btn2 = gr.Button("Ask")

        btn2.click(
            agri_chat,
            [crop, question],
            output2
        )

    with gr.Tab("Weather-Based Advice"):

        weather_location = gr.Textbox(
            label="Location"
        )

        output3 = gr.Textbox(lines=10)

        btn3 = gr.Button(
            "Get Weather Advice"
        )

        btn3.click(
            weather_advice,
            weather_location,
            output3
        )

    with gr.Tab("Disease Information"):

        disease = gr.Textbox(
            label="Disease Name"
        )

        output4 = gr.Textbox(lines=10)

        btn4 = gr.Button(
            "Get Information"
        )

        btn4.click(
            disease_info,
            disease,
            output4
        )

demo.launch(share=True)
