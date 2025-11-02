from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, CheckConstraint

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, nullable=False)
    telegram_id = Column(String(20), nullable=True)
    telegram_link = Column(String(100), nullable=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(Date)
    sex = Column(String(1), CheckConstraint("sex IN ('М', 'Ж')"))
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    total_experience = Column(Float, default=0.0)
    current_experience = Column(Float, default=0.0)


class Competitions(Base):
    __tablename__ = "competitions"

    competition_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    type = Column(String, nullable=False)
    password = Column(String)
    video_instruction = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    priority = Column(Integer, server_default="0")
    coef_m = Column(Float)
    coef_f = Column(Float)


class Results(Base):
    __tablename__ = "results"

    result_id = Column(Integer, primary_key=True)
    competition_id = Column(
        Integer,
        ForeignKey("competitions.competition_id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video = Column(String)
    count = Column(Integer)
    points = Column(Float)
    status = Column(String(1))


class Whitelist(Base):
    __tablename__ = "whitelist"

    id = Column(Integer, primary_key=True)
    competition_id = Column(
        Integer,
        ForeignKey("competitions.competition_id", ondelete="CASCADE"),
        nullable=False,
    )
    email = Column(String(100), nullable=False)


class PwdAuthorized(Base):
    __tablename__ = "pwd_authorized"

    authorize_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    competition_id = Column(
        Integer,
        ForeignKey("competitions.competition_id", ondelete="CASCADE"),
        nullable=False,
    )


class Trainings(Base):
    __tablename__ = "trainings"

    training_id = Column(Integer, primary_key=True)
    title = Column(String(100))
    video_instruction = Column(String)
    coef_m = Column(Float)
    coef_f = Column(Float)
