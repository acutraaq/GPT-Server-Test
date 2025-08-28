import base64
from pathlib import Path
from openai import OpenAI

speech_file_path = Path(__file__).parent / "speech.mp3"
audio_path = (
    Path(__file__).parent.parent / "assets/audio_data/roles/yu_chengdong/reference_audio.wav"
)

with open(audio_path, "rb") as f:
    audio_bytes = f.read()
audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
clone_voice = False  # Whether to use voice cloning
# Lei Jun's voice
url = "https://s1.aigei.com/src/aud/mp3/59/59b47e28dbc14589974a428180ef338d.mp3?download/%E9%9B%B7%E5%86%9B%E8%AF%AD%E9%9F%B3%E5%8C%85_%E7%88%B1%E7%BB%99%E7%BD%91_aigei_com.mp3&e=1745911680&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:RvcXPTseOqkvy2f_ppELez7d8jY="
if clone_voice:
    voice = audio_base64
    # voice = url
else:
    voice = "news_broadcast_female_voice"

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")
with client.audio.speech.with_streaming_response.create(
    model="tts",
    voice=voice,  # Built-in news_broadcast_female_voice, supports voice cloning, voice can be base64 or a url
    input="This episode's main content: 1. Xi Jinping emphasized when participating in the Beijing district NPC representative re-election voting to continuously develop whole-process people's democracy and strengthen supervision of the entire election process",
    speed="very_high",  # ["very_low", "low", "moderate", "high", "very_high"]
    extra_body={
        "pitch": "high"
    },  # ["very_low", "low", "moderate", "high", "very_high"]
) as response:
    with open(speech_file_path, mode="wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)  # This chunk can be streamed and played in real-time through a player
