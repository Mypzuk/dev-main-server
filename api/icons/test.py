from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent  # подстрой под структуру
ICONS_DIR = PROJECT_ROOT / "static" / "icons"


@router.get("/icons/{icon_name}")
def get_icon(icon_name: str):
    icon_path = ICONS_DIR / icon_name
    if not icon_path.exists():
        raise HTTPException(status_code=404, detail="Icon not found")

    return FileResponse(icon_path)