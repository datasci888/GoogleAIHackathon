from src.configs.index import OPENAI_API_KEY
from src.services.er_visit import read_er_visit
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import jsonpickle
import asyncio
import os
from nest_asyncio import apply
from PIL import Image
from openai import OpenAI
import uuid

client = OpenAI(api_key=OPENAI_API_KEY)
apply()


def transcribe(audio_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, response_format="text"
    )
    return transcription


def text_to_speech(text):
    response = client.audio.speech.create(model="tts-1", voice="nova", input=text)
    return response.content


if not "er_visit_id" in st.session_state:
    st.session_state.er_visit_id = f"triage{uuid.uuid4().hex}"

er_visit_id = st.session_state["er_visit_id"]
if "messages" not in st.session_state:
    # change the id later depending on session
    er_visit = asyncio.run(read_er_visit(id=er_visit_id))
    er_messages = er_visit.ChatMessages or []

    parsed_er_messages = []
    index = len(er_messages) - 1

    while index >= 0:
        parsed_message = jsonpickle.decode(er_messages[index].raw)
        parsed_er_messages.append(
            {"role": parsed_message.type, "content": parsed_message.content}
        )
    st.session_state.messages = parsed_er_messages


st.title("EVA - Emergency Virtual Assistant")
tts = st.checkbox("Enable Text-to-Speech")
uploaded_image = st.file_uploader(
    "Optionally, upload an image for analysis", type=["png", "jpg", "jpeg"]
)
chatbox = st.container(height=400)

with chatbox:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query_holder = st.empty()
    response_holder = st.empty()

cols = st.columns([0.9, 0.1])
error = st.empty()

with cols[0]:
    prompt = st.chat_input("What's your concern?")

with cols[1]:
    audio_bytes = audio_recorder(text="", icon_size="2x")
    if audio_bytes and not prompt:
        file_name = "speech.mp3"
        try:
            with open(file_name, "wb+") as audio_file:
                audio_file.write(audio_bytes)
                audio_file.seek(0)
                transcript = transcribe(audio_file)

            os.remove(file_name)
            if transcript:
                prompt = transcript
        except:
            error.warning(
                "The recorded file is too short. Please record your question again!",
                icon="🚨",
            )

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with query_holder.chat_message("user"):
        st.write(prompt)

    with response_holder.chat_message("assistant"):
        from src.services.agents.mts_agent.index import astream

        async def run_astream(
            er_visit_id: str, prompt: str | None = None, image: bytes | None = None
        ):
            async for message in astream(er_visit_id, prompt):
                st.markdown(body=message)
            return message

        final_response = ""
        if uploaded_image:
            with st.spinner("Analyzing image"):
                img_file = uploaded_image.read()
                final_response = asyncio.run(run_astream(er_visit_id, prompt, img_file))
                # process image here!

        with st.spinner("Thinking..."):
            try:
                final_response = asyncio.run(run_astream(er_visit_id, prompt))
            except:
                st.error(
                    body="We are experiencing some issues. Please try again later.",
                    icon="🚨",
                )
        if tts:
            with st.spinner("Generating audio response"):
                audio = text_to_speech(final_response)
                st.audio(audio)

    st.session_state.messages.append({"role": "assistant", "content": final_response})
