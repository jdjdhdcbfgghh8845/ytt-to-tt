from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from downloader import YouTubeDownloader
from uploader import TikTokUploader
from processor import VideoProcessor
import os
import uuid

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

downloader = YouTubeDownloader(download_path="downloads")
processor = VideoProcessor(output_path="processed")
uploader = TikTokUploader()

# In-memory status tracking
jobs = {}

class ProcessRequest(BaseModel):
    url: str

@app.post("/process")
def process_video(request: ProcessRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "progress": 0, "message": "Starting..."}
    
    background_tasks.add_task(run_workflow, job_id, request.url)
    
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

def run_workflow(job_id: str, url: str):
    try:
        # Step 1: Download
        jobs[job_id].update({"status": "downloading", "progress": 20, "message": "Downloading from YouTube..."})
        metadata = downloader.download_video(url)
        
        # Step 2: Anti-copyright processing
        jobs[job_id].update({"status": "processing", "progress": 40, "message": "Applying anti-copyright filters..."})
        processed_video = processor.process_video(metadata['video_path'])
        
        # Step 3: Metadata extraction (already done in download_video for simplicity)
        jobs[job_id].update({"status": "extracted", "progress": 60, "message": "Extracting description and hashtags..."})
        
        # Step 4: Upload to TikTok
        jobs[job_id].update({"status": "uploading", "progress": 80, "message": "Uploading to TikTok..."})
        
        # Combine title and description for best visibility
        video_desc = metadata.get('description', '') or metadata.get('title', '')
        
        uploader.upload_video(
            processed_video, 
            video_desc,
            metadata['hashtags'] + ["shorts", "fyp"] 
        )
        
        jobs[job_id].update({"status": "completed", "progress": 100, "message": "Finished successfully!"})
        
    except Exception as e:
        jobs[job_id].update({"status": "failed", "progress": 0, "message": f"Error: {str(e)}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
