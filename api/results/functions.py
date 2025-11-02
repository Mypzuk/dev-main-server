from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.results.schemas import ResultSchemas
from core.models import Users, Results, Competitions
from api.responses import ResponseTemplates

from fastapi import HTTPException



async def get_result(session: AsyncSession, **kwargs):
    query = select(Results)
    for key, value in kwargs.items():
        query = query.where(getattr(Results, key) == value)
    result = await session.execute(query)
    result = result.scalars().first()
    return result


async def get_results(session):
    stmt = select(Results).order_by(Results.competition_id)
    result = await session.execute(stmt)
    results = result.scalars().all()
    result_schemas = [ResultSchemas.model_validate(result) for result in results]
    return ResponseTemplates.success(data=result_schemas)



async def create_result(result_in, session):
    data = result_in.model_dump()
    user_id = data.get("user_id")
    competition_id = data.get("competition_id")
    count = int(data.get("count"))


    user = await session.scalar(select(Users).where(Users.id == user_id))
    

    competition = await session.scalar(
        select(Competitions).where(Competitions.competition_id == competition_id)
    )


    # Вычисляем points
    if user.sex == "М":
        points = count * (competition.coef_m or 1.0)
    elif user.sex == "Ж":
        points = count * (competition.coef_f or 1.0)
    else:
        points = count

    points = round(points)

    # Убираем points из data, если оно там уже есть
    data.pop("points", None)

    # Создаём запись
    result = Results(**data, points=points)
    session.add(result)
    await session.commit()
    await session.refresh(result)

    return ResponseTemplates.success(
        data={"result_id": result.result_id, "points": points},
        message="Result created successfully"
    )


async def update_result(result_in, result, session):
    for name, value in result_in:
        setattr(result, name, value)
    await session.commit()
    return ResponseTemplates.success(result_in)


async def delete_result(result_in, session):
    await session.delete(result_in)
    await session.commit()
    return ResponseTemplates.success(message=f"Result deleted")




async def user_results_info(user_id: int, session: AsyncSession):
    # Подзапрос: лучший результат каждого пользователя
    best_results_subq = (
        select(
            Results.competition_id,
            Results.user_id,
            func.max(Results.points).label("best_points")
        )
        .group_by(Results.competition_id, Results.user_id)
        .subquery()
    )

    # Ранжирование через оконную функцию
    ranked_subq = (
        select(
            best_results_subq.c.competition_id,
            best_results_subq.c.user_id,
            best_results_subq.c.best_points,
            func.rank().over(
                partition_by=best_results_subq.c.competition_id,
                order_by=best_results_subq.c.best_points.desc()
            ).label("place")
        ).subquery()
    )

    # Основной запрос: соединяем с соревнованиями и считаем участников
    q = (
        select(
            Competitions.competition_id,
            Competitions.title,
            Competitions.end_date,
            func.count(best_results_subq.c.user_id).label("participants"),
            ranked_subq.c.place
        )
        .join(ranked_subq, ranked_subq.c.competition_id == Competitions.competition_id)
        .join(best_results_subq, best_results_subq.c.competition_id == Competitions.competition_id)
        .filter(ranked_subq.c.user_id == user_id.id)
        .group_by(
            Competitions.competition_id,
            Competitions.title,
            Competitions.end_date,
            ranked_subq.c.place
        )
    )

    result = await session.execute(q)
    rows = result.all()



    return ResponseTemplates.success(data=[
        {
            "competition_id": r.competition_id,
            "title": r.title,
            "end_date": r.end_date.isoformat() if r.end_date else None,
            "participants": r.participants,
            "place": r.place
        }
        for r in rows
    ])



    
async def leaderboard(competition_id, session):
    # 1️⃣ Получаем соревнование
    competition = competition_id

    # 2️⃣ Подзапрос: лучший результат каждого пользователя в этом соревновании
    best_results_subq = (
        select(
            Results.user_id,
            func.max(Results.points).label("best_points")
        )
        .where(Results.competition_id == competition.competition_id)
        .group_by(Results.user_id)
        .subquery()
    )

    # 3️⃣ Основной запрос: достаём имена пользователей и их лучшие очки
    stmt = (
        select(
            Users.first_name,
            Users.last_name,
            best_results_subq.c.best_points
        )
        .join(best_results_subq, best_results_subq.c.user_id == Users.id)
        .order_by(best_results_subq.c.best_points.desc())
    )

    result = await session.execute(stmt)
    leaderboard_data = [
        {
            "name": f"{row.first_name or ''} {row.last_name or ''}".strip(),
            "points": row.best_points
        }
        for row in result.all()
    ]

    # 4️⃣ Формируем ответ
    return ResponseTemplates.success(
        data={
            "competition_title": competition.title,
            "end_date": competition.end_date.isoformat() if competition.end_date else None,
            "leaderboard": leaderboard_data
        }
    )



async def denied_result(result_in, session):

    print(result_in)