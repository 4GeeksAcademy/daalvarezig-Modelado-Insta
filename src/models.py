from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    followers = relationship("Follower", foreign_keys="Follower.followed_id", back_populates="followed")
    following = relationship("Follower", foreign_keys="Follower.follower_id", back_populates="follower")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)   

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "image_url": self.image_url,
        }
    

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(300), nullable=False)    

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "image_url": self.text,
        }
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  

    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")


    def serialize(self):
        return {
            "id": self.id,
            "followed_id": self.followed_id,
            "follower_id": self.follower_id,
        }
    
class Message(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")


    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
        } 
    
