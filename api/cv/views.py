from fastapi import APIRouter, UploadFile, File
import shutil
import os
from starlette.responses import JSONResponse

from .functions.bicycle import check_bicycle
from .functions.push_ups import check_pushUps
from .functions.pull_ups import check_pullUps
from .functions.squats import check_squats
from .functions.climber import check_climber



router = APIRouter(tags=["Video 📷"])

dispatch = {
    'bicycle': check_bicycle,
    'pushUps': check_pushUps,
    'pullUps': check_pullUps,
    'squats': check_squats,
    'climber': check_climber,
    }





@router.post('/upload_video')
async def upload_video(video: UploadFile = File(...), type = str):
    
    try:    
        
        video_name, video_extension = os.path.splitext(video.filename)
        print(video_extension)
        
        extensions = ['.mp4', '.mov']    
        if video_extension.lower() not in extensions:
            return JSONResponse(status_code=404, content={"code":"404","message": "Неверный формат видео"})  
        
        with open(f"api/cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
            
            result = await dispatch[type](video.filename)
            return {"result": result}
            
    except Exception as e:
       
        return JSONResponse(status_code=404, content={"code":"404","message": "При загрузке видео произошла ошибка"})  