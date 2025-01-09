from app.model.models import User, Friend
from fastapi_sqlalchemy import db
from app.schemas.sche_friend import FriendResponse
from app.until.exception_handler import CustomException
from app.schemas.sche_page import PaginationParams
from app.until.page import paginate, Page
from app.service.mapper.Mapper import friend_mapper,user_mapper
from app.until.enums import FriendshipStatus
from sqlalchemy import or_, and_
from app.schemas.sche_user import UserResponse
from app.model.models import User
class FriendService:
    def __init__(self):
        self.db = db.session
       

    def add_friend(self, receiver_id: int,sender:User) -> FriendResponse:
        receiver = self.db.query(User).filter(User.id == receiver_id).first()
        if not receiver:
            raise CustomException(
                http_code=404,
                code="404",
                message=f"Người nhận không tồn tại: {receiver_id}",
            )
        if (
            self.db.query(Friend)
            .filter(
                or_(
                    and_(Friend.sender == sender, Friend.receiver == receiver),
                    and_(Friend.sender == receiver, Friend.receiver == sender),
                )
            )
            .first()
        ):
            raise CustomException(
                http_code=400,
                code="400",
                message="Đã gửi kết bạn rồi",
            )
        if sender.id == receiver.id:
            raise CustomException(
                http_code=400,
                code="400",
                message="Không thể gửi kết bạn cho bản thân mình",
            )
        friend = Friend()
        friend.receiver = receiver
        friend.sender = sender
        friend.status = FriendshipStatus.PENDING

        self.db.add(friend)
        self.db.commit()
        self.db.refresh(friend)

        return friend_mapper(friend=friend)

    def response_friend(
        self, sender_id: int, request: FriendshipStatus,receiver:User
    ) -> FriendResponse:

        sender = self.db.query(User).filter(User.id == sender_id).first()
        if not sender:
            raise CustomException(
                http_code=404,
                code="404",
                message=f"Người nhận không tồn tại: {sender_id}",
            )
        friend = (
            self.db.query(Friend)
            .filter(and_(Friend.sender == sender, Friend.receiver == receiver))
            .first()
        )
        if not friend:
            raise CustomException(
                http_code=404,
                code="404",
                message=f"Người nhận không tồn tại: {sender_id}",
            )

        else:
            if (
                friend.status == FriendshipStatus.ACCEPTED
                and request == FriendshipStatus.PENDING
                or friend.status == FriendshipStatus.REJECTED
                and request == FriendshipStatus.ACCEPTED
            ):
                raise CustomException(
                    http_code=400,
                    code="400",
                    message="Nguoi dung sai thao tac",
                )
            else:
                friend.status = request
                self.db.commit()
                self.db.refresh(friend)
                return friend_mapper(friend=friend)

    def get_list_friend(
        self, param: PaginationParams,user:User
    ) -> "Page[UserResponse]":
       
        _query = (
            self.db.query(User)
            .join(
                Friend,
                or_(
                    and_(Friend.sender_id == user.id, Friend.receiver_id == User.id),
                    and_(Friend.receiver_id == user.id, Friend.sender_id == User.id),
                ),
            )
            .filter(Friend.status == FriendshipStatus.ACCEPTED)
        )
        return paginate(model=User,model_response=user_mapper,query=_query,params=param)
    
    def get_list_pending(self, param: PaginationParams,user:User
    ) -> "Page[FriendResponse]":
      
        _query=self.db.query(Friend).filter(and_(Friend.receiver_id==user.id,Friend.status==FriendshipStatus.PENDING))
        return paginate(model=Friend,model_response=friend_mapper,query=_query,params=param)