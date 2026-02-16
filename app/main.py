import random
from matplotlib.pylab import randint
from app.utils import load_data_json
from fastapi import HTTPException,FastAPI,Query,Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field ,UUID4
from typing import Annotated,Optional,Literal,List
import json
from app.model_utils import predict_email
import logging
from contextlib import asynccontextmanager
import os
# Add at top of file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Global cache
EMAIL_CACHE = []

# Helper: Generate unique numeric ID
def generate_unique_id(existing_ids, min_id=0, max_id=99999999):
    """Generate a numeric ID that does not exist in `existing_ids`."""
    while True:
        new_id = random.randint(min_id, max_id)
        if new_id not in existing_ids:
            return new_id
@asynccontextmanager
async def lifespan(app: FastAPI):
    global EMAIL_CACHE
    EMAIL_CACHE = load_data_json()
    logger.info(f"✅ Loaded {len(EMAIL_CACHE)} emails into cache")
    yield
    logger.info("🔻 Shutting down...")
app = FastAPI(lifespan=lifespan)

def save_data(data):
    json_path = os.path.join("data", "enron_spam_data.json")
    # Convert dict back to list for saving
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
    return data

# home page
@app.get("/")
def home():
    return {"message":"welcome to our email spam detector website"}

# about page 
@app.get("/about")
def about():
    return {"message": "this is an email spam detector website"}

# creating our pydantic object data:
class Emails_data(BaseModel):
    subject: Annotated[str,Field(...,description="copy your email subject for that")]
    Message: Annotated[str,Field(...,description="the content of your email")]
    date : Annotated[str,Field(...,description="the date of your message")]
    classification: Annotated[Optional[Literal["spam","ham"]],Field(default=None,description="Spam or ham classification")]
    MessageID:   Annotated[Optional[int], Field(default=None)]  # will auto-generate if missing
@app.post("/predict")    
def new_messages(email: Emails_data):
    global EMAIL_CACHE
    data = EMAIL_CACHE  # local reference

    # Extract all existing Message IDs
    existing_ids = {e["Message ID"] for e in data}

    # Auto-generate MessageID if not provided
    if email.MessageID is None:
        email.MessageID = generate_unique_id(existing_ids)

    # Double-check for duplicates (safe-guard)
    if email.MessageID in existing_ids:
        raise HTTPException(status_code=400, detail="Message ID already exists")
    
    # Predict classification
    prediction = predict_email(email.Message)
    email.classification = prediction

    # Map Pydantic keys → JSON keys
    new_email = {
        "Message ID": email.MessageID,
        "Subject": email.subject,
        "Message": email.Message,
        "classification": email.classification,
        "Date": email.date
    }

    # Append and save
    data.append(new_email)
    logger.info(f"After append, data has {len(data)} emails")
    save_data(data)
    logger.info("Save completed")

    # Verify
    verify_data = load_data_json()
    logger.info(f"VERIFICATION: File now contains {len(verify_data)} emails")
    if len(verify_data) != len(data):
        logger.error(f"DATA LOSS! Expected {len(data)}, but file has {len(verify_data)}")

    return JSONResponse(
        status_code=200,
        content={
            "message": f"Your email is a {email.classification}",
            "MessageID": email.MessageID
        }
    )

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}
