from datetime import timedelta

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, \
    NoTranscriptAvailable

app = FastAPI()


class YoutubeTranscriptData(BaseModel):
    url: str


@app.post("/youtube/transcript")
async def get_transcript(data: YoutubeTranscriptData):
    try:
        yt = YouTube(data.url)

        try:
            chunks = YouTubeTranscriptApi.get_transcript(yt.video_id)
        except (TranscriptsDisabled, NoTranscriptAvailable) as e:
            raise HTTPException(
                status_code=404,
                detail=f"Transcript not available: {str(e)}"
            )

        return {
            "title": getattr(yt, "title", "Undefined"),
            "views": getattr(yt, "views", 0),
            "author": getattr(yt, "author", "Unknown"),
            "length": str(timedelta(seconds=yt.length)),
            "published": (yt.publish_date.strftime("%Y-%m-%d")
                          if yt.publish_date else None),
            "thumbnail": yt.thumbnail_url,
            "transcript": (
                ' '.join(chunk.get('text', '') for chunk in chunks)
                .strip()
            ),
        }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Error processing video: {str(e)}"
        )
