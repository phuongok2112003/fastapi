from app.model.models import Post,Favorite
from fastapi_sqlalchemy import db
from app.until.exception_handler import CustomException
from app.model.models import User
from app.service.mapper.Mapper import favorite_mapper
class FavoriteService:
    def __init__(self):
        self.db=db.session

    def like(self,post_id:int,user:User):
        post=self.db.query(Post).filter(Post.id==post_id).first()
        if post is None:
            raise CustomException(http_code=400,code="400",message="post id khong ton tai")

        else :
            favorite = Favorite()
        
            favorite.author_id=user.id
            favorite.post_id=post_id
            self.db.add(favorite)
            self.db.commit()
            self.db.refresh(favorite)
            return favorite_mapper(favoirte=favorite)
    def un_like(self,post_id:int,user:User):
        favorite=self.db.query(Favorite).filter(Favorite.post_id==post_id and Favorite.author_id==user.id).first()
        if favorite is None:
            raise CustomException(http_code=400,code="400",message="favorite id khong ton tai")
        if favorite.author_id !=user.id:
                raise CustomException(http_code=403,code="403",message="Ban khong co quyen")   

        self.db.refresh(favorite)
        self.db.delete(favorite)
        self.db.commit()
      
        return {"message": "unlike đã được xóa thành công"}   