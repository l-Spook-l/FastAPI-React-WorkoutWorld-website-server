from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, insert, update, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi.exceptions import HTTPException

# router - объединяет несколько endpoints(url)
# и вызываем в main
from .models import Workout, Exercise, Set
from .schemas import WorkoutCreate, ExerciseCreate, SetCreate

router = APIRouter(
    # prefix - url путь
    prefix="/workouts",
    # tags - группа к которой он относиться
    tags=["Workout"]
)


@router.post("/create_workout")
async def add_workout(new_workout: WorkoutCreate, session: AsyncSession = Depends(get_async_session)):
    stat = insert(Workout).values(**new_workout.dict()).returning(Workout.id)
    result = await session.execute(stat)
    id = result.scalar()
    await session.commit()
    return {"status": "success", 'workout_ID': id}


@router.post("/create_exercise")
async def add_exercise(new_exercise: ExerciseCreate, session: AsyncSession = Depends(get_async_session)):
    stat = insert(Exercise).values(**new_exercise.dict())
    await session.execute(stat)
    await session.commit()
    return {"status": "success"}


@router.post("/create_set")
async def add_set(new_set: SetCreate, session: AsyncSession = Depends(get_async_session)):
    stat = insert(Set).values(**new_set.dict())
    await session.execute(stat)
    await session.commit()
    return {"status": "success"}


@router.get("/")
async def get_workouts(
        name: str = Query(None, description="Filter by name"),
        difficulty: str = Query(None, description="Filter by difficulty"),
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(12, description="Number of records to return"),
        session: AsyncSession = Depends(get_async_session)):
    try:
        # Создаем базовый запрос
        query = select(Workout)
        # Применяем фильтры, если они предоставлены в name или difficulty
        if name:  # Выбираем все записи из табл. Workout и по названию
            query = query.filter(Workout.name == name)
        if difficulty:  # Выбираем все записи из табл. Workout и по сложности
            query = query.filter(Workout.difficulty == difficulty)

        # добавляем лимиты
        query = query.limit(limit).offset(skip)
        # делаем запрос в БД
        result = await session.execute(query)
        # подсчет общего количества записей
        total_count = await session.scalar(select(func.count()).select_from(Workout))
        # получаем список из словарей
        workouts = result.mappings().all()

        return {
            'status': 'success',
            'data': workouts,
            'skip': skip,
            'limit': limit,
            'total_count': total_count,
            'details': None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })


@router.get("/workout/{workout_id}")  # изменить путь !!!!!!!!!!!!
async def get_workout(workout_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Workout).filter(Workout.id == workout_id).options(selectinload(Workout.exercise))
    result = await session.execute(query)
    workout = result.mappings().one()
    return {
        'status': 'success',
        'data': workout,
        'details': None,
    }


@router.get("/sets")
async def get_sets(exercise: int, user: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Set).filter(Set.exercise_id == exercise).filter(Set.user_id == user)
    # query = select(Set).filter(Set.id == exercise)
    print('query', query)
    result = await session.execute(query)
    sets = result.mappings().all()
    return {
        'status': 'success',
        'data': sets,
        'details': None,
    }


@router.patch("/update{set_id}")
async def update_set(set_id: int, count: int, session: AsyncSession = Depends(get_async_session)):
    query = update(Set).filter(Set.id == set_id).values(count=count)

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }
