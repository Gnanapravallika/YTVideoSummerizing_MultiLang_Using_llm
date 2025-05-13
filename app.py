import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt_template = {
    "en": """You are Youtube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    within 250 words. Please provide the summary of the text given here:  """,
    "es": """Eres un resumidor de videos de YouTube. Tomarás el texto de la transcripción
    y resumirás todo el video y proporcionarás el resumen importante en puntos
    en 250 palabras. Por favor, proporciona el resumen del texto dado aquí: """,
    "fr": """Vous êtes un résumeur de vidéos Youtube. Vous prendrez le texte de la transcription
    et résumerez l'ensemble de la vidéo et fournirez le résumé important en points
    en 250 mots. Veuillez fournir le résumé du texte donné ici: """,
    "de": """Du bist ein Youtube-Video-Zusammenfasser. Du wirst den Transkripttext nehmen
    und das gesamte Video zusammenfassen und die wichtige Zusammenfassung in Punkten
    innerhalb von 250 Wörtern bereitstellen. Bitte gib die Zusammenfassung des gegebenen Textes hier an: """,
    "ja": """あなたは、YouTubeビデオの要約者です。トランスクリプトのテキストを取得し、
    ビデオ全体を要約し、重要な要約を250ワード以内でポイントで提供します。ここに与えられたテキストの要約を提供してください: """,
    "ko": """당신은 유튜브 비디오 요약자입니다. 당신은 스크립트 텍스트를 가지고
    전체 비디오를 요약하고 중요한 요약을 250단어 이내의 요점으로 제공합니다. 여기에 주어진 텍스트의 요약을 제공하십시오: """,
    "zh-CN": """你是一位 YouTube 视频摘要生成器。你将获取转录文本，
    总结整个视频，并在 250 字内以要点形式提供重要的摘要。请提供此处给出的文本的摘要: """,
}

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

language = st.selectbox(
    "Select Language",
    options=list(prompt_template.keys()),
    index=0,
    key="language_select",
)

if st.button("Get Detailed Notes"):
    if video_id:
        transcript_text = extract_transcript_details(youtube_link)
    

        if transcript_text:
            prompt = prompt_template[language]
            summary=generate_gemini_content(transcript_text,prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
    else:
        st.warning("Please enter a valid YouTube link.")




