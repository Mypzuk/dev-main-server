import random
from random import choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from core.models import Competitions
from core.base import Base

engine = create_engine("sqlite:///OSport.sqlite3")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Competition types
types = ["pushUps", "squats", "climber", "bicycle", "pullUps"]

# Create 10 competitions
for i in range(1, 11):
    type = choice(types)

    # Randomly decide whether the competition is in the past, present, or future
    time_period = choice(["past", "current", "future"])

    if time_period == "past":
        # For past competitions, both start and end dates are in the past
        start_date = datetime.now() - timedelta(days=random.randint(60, 90))
        end_date = start_date + timedelta(days=random.randint(15, 30))

    elif time_period == "current":
        # For current competitions, start date is in the past, and end date is in the future
        start_date = datetime.now() - timedelta(days=random.randint(5, 15))
        end_date = datetime.now() + timedelta(days=random.randint(5, 15))

    else:  # 'future'
        # For future competitions, both start and end dates are in the future
        start_date = datetime.now() + timedelta(days=random.randint(5, 15))
        end_date = start_date + timedelta(days=random.randint(15, 30))

    competition = Competitions(
        title=f"Competition{i}",
        type=type,
        coef_m=round(random.uniform(0.5, 2.0), 2),
        coef_f=round(random.uniform(0.5, 2.0), 2),
        video_instruction=f"http://217.114.2.56/manuals/{type}.mp4",
        start_date=start_date,  # Adding start date
        end_date=end_date,
        status=choice(["free", "paid"]),
        priority=round(random.uniform(0.5, 2.0), 2),
        created=datetime.now(),
        updated=datetime.now(),
    )
    session.add(competition)

# Commit competitions to the database
session.commit()
