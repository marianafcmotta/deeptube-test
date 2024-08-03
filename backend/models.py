from typing import Optional, List
from pydantic import BaseModel

class Announcement(BaseModel):
    title: Optional[str] = None
    channel_title: Optional[str] = None
    duration: Optional[int] = None
    number_of_views: Optional[int] = None
    number_of_likes: Optional[int] = None
    thumbnail_url: Optional[str] = None
    is_short: Optional[bool] = False
    transcription: Optional[str] = None
    published_date: Optional[str] = None
    video_url: Optional[str] = None
    advertiser_name: Optional[str] = None

class requestData(BaseModel):
    keys: List[str]