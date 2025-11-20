from fastapi import APIRouter
import os, json

router = APIRouter()

# Path to stories.json
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "stories.json")

@router.get("/api/stories")
def get_stories():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data

@router.get("/api/stories/{story_id}")
def get_story(story_id: int):
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if item["id"] == story_id:
            return item
    return {"error": "Story not found"}
