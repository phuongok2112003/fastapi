from app.model.models import Post, User, Friend, Favorite, Comment
from fastapi_sqlalchemy import db
from app.until.exception_handler import CustomException
from sqlalchemy import or_, and_
from app.until.enums import FriendshipStatus
from datetime import datetime, timedelta
import os
import openpyxl
from io import BytesIO
class ReportService:
    def __init__(self):
        self.db = db.session

    def report(self, user: User):
        now = datetime.utcnow()
        last_week = now - timedelta(days=7)
        post_counts = (
            self.db.query(Post)
            .filter(
                and_(
                    Post.author_id == user.id,
                    Post.created_at >= last_week,
                    Post.created_at <= now,
                )
            )
            .count()
        )

        frined_new_count = (
            self.db.query(Friend)
            .filter(
                and_(
                    Friend.status == FriendshipStatus.ACCEPTED,
                    or_(Friend.sender_id == user.id, Friend.receiver_id == user.id),
                    Friend.created_at >= last_week,
                    Friend.created_at <= now,
                )
            )
            .count()
        )

        like_count = (
            self.db.query(Favorite)
            .join(Post, Favorite.post_id == Post.id)
            .filter(
                and_(
                    Favorite.created_at >= last_week,
                    Favorite.created_at <= now,
                    Post.author_id == user.id,
                )
            )
            .count()
        )

        comment_count = (
            self.db.query(Comment)
            .join(Post, Comment.post_id == Post.id)
            .filter(
                and_(
                    Comment.created_at <= now,
                    Comment.created_at >= last_week,
                    Post.author_id == user.id,
                )
            )
            .count()
        )
        
        data={
            "So bai Post":post_counts,
            "So ban moi":frined_new_count,
            "So luot thich":like_count,
            "So comment moi":comment_count
      
        }


        template_path = os.path.join(os.getcwd(), 'app', 'template', 'report.xlsx')
        workbook = openpyxl.load_workbook(template_path)
        sheet = workbook.active

        sheet['A5'] = data['So bai Post']
        sheet['B5'] = data['So ban moi']
        sheet['C5'] = data['So luot thich']
        sheet['D5'] = data['So comment moi']

        # Lưu lại vào một buffer
        excel_file = BytesIO()
        workbook.save(excel_file)

        # Di chuyển con trỏ về đầu file trước khi trả về
        excel_file.seek(0)
        return excel_file
