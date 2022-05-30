from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text
from sqlalchemy.orm.session import sessionmaker
import sqlalchemy


engine = sqlalchemy.create_engine('sqlite:///content2.db')
base = declarative_base()


class Post(base):

    __tablename__ = 'posts'

    post_id = Column(String, primary_key=True)
    datetime = Column(String(30))
    username = Column(String(30))
    caption = Column(Text)
    file = Column(Text)
    platform = Column(String(10))

    def __init__(self, post_id: str, datetime: str, username: str, caption: str, file: str, platform: str):
        super().__init__()
        self.post_id = post_id
        self.datetime = datetime
        self.username = username
        self.caption = caption
        self.file = file
        self.platform = platform

    def __iter__(self):
        yield 'post_id', self.post_id
        yield 'datetime', self.datetime
        yield 'username', self.username
        yield 'caption', self.caption
        yield 'file', self.file
        yield 'platform', self.platform


base.metadata.create_all(engine)


class OrmAbstraction:

    def __init__(self):
        self.engine = engine

    def _create_session(self) -> sessionmaker:
        session = sessionmaker(bind=self.engine)
        return session()

    def save_posts(self, posts: list[Post]) -> None:
        with self._create_session() as s:
            for post in posts:
                s.add(post)
            s.commit()

    def get_all_posts(self, condition=True) -> list:
        with self._create_session() as s:
            posts = s.query(Post).filter(condition).order_by(Post.datetime.asc()).all()
            return posts


    def get_all_posts_of_platform(self, platform: str) -> list:
        with self._create_session() as s:
            posts = s.query(Post).filter(Post.platform == platform).all()
            return posts

    def get_ids_by_platform(self, platform: str) -> list:
        with self._create_session() as s:
            posts = s.query(Post.post_id).filter(Post.platform == platform).all()
            return posts
