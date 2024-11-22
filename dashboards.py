import os

import plotly.express as px
import base64
import io
global client
import anthropic
from gtts import gTTS
from io import BytesIO
from utils import cache_to_memory_and_disk

DASHBOARD_DEBRIEF_PROMPT = """
Summarize the overall trend or pattern observed in the plot, highlighting any notable peaks, troughs, or significant changes. If applicable, mention seasonal patterns or anomalies, and compare the current data to relevant benchmarks or targets. Make sure to provide specific observations to give stakeholders a clear picture of what the data shows.
Then Discuss the insights that can be drawn from the plot and their implications for business decisions. """


@cache_to_memory_and_disk
def get_dashboard_brief(image):
    api_key = os.environ.get("ANTROPIC_API_KEY")
    image = base64.b64encode(image.read()).decode("utf-8")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user",
                   "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image}},
                               {"type": "text", "text": DASHBOARD_DEBRIEF_PROMPT}],}],
    )
    print(message)
    text = message.content[0].text
    audio = speak_it(text)

    return text, audio


def get_dashboard(data, selected_dashboard, group_by):
    fig = px.line(
        data,
        x="Period",
        y="Close",
        title=f"{selected_dashboard} Close Price ({group_by.capitalize()})",
        template="plotly_dark",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Close Price",
        title_x=0.5,
    )

    image_data = io.BytesIO()
    fig.write_image(image_data, format="png")
    image_data.seek(0)
    return image_data, fig


def speak_it(text):
    sound_obj = BytesIO()
    tts = gTTS(text, lang='en')
    tts.write_to_fp(sound_obj)
    return sound_obj


if __name__ == "__main__":
    ...
