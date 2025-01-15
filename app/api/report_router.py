from fastapi import APIRouter, Depends
from app.schemas.sche_post import PostCreate, PostResponse
from app.service.report_service import ReportService
from app.until.authen_login import login_required
from app.model.models import User
from app.schemas.sche_page import PaginationParams
from app.until.page import Page
from app.schemas.sche_base import DataResponse
from fastapi.responses import StreamingResponse
router = APIRouter()

@router.post("/report-a-week")
def create(reportservice:ReportService=Depends(),user:User=Depends(login_required)):
    excel_file = reportservice.report(user=user)

    filename = f"report_for_{user.name}.xlsx"
    
    return StreamingResponse(
        excel_file, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )