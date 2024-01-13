import re
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()


class YoutubeTranscriptData(BaseModel):
    url: str


@app.post("/youtube/transcript")
async def get_transcript(data: YoutubeTranscriptData):
    video_id = extract_video_id(data.url)

    if video_id is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    chunks = YouTubeTranscriptApi.get_transcript(video_id)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube Transcript Chunks"
        )

    return {
        "transcript": process_transcript_chunks(chunks)
    }


def process_transcript_chunks(chunks: List[str]):
    transcript = ""
    for chunk in chunks:
        transcript += chunk["text"] + " "
    return transcript.strip()


def extract_video_id(url: str) -> Optional[str]:
    patterns = [
        r"youtu\.be\/([^?]+)",
        r"youtube\.com\/(?:embed|v|watch)\?v=([^?]+)",
        r"youtube\.com\/(?:embed|v|watch)\?.*?&v=([^&]+)",
        r"youtube\.com\/(?:embed|v|watch)\?.*?\?(?:.*?&)?v=([^&]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match and match.group(1):
            return match.group(1)

    return None
