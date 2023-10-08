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
        page: int = Query(1, description="Page number"),
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
async def get_one_workout(workout_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Workout).filter(Workout.id == workout_id).options(selectinload(Workout.exercise))
    result = await session.execute(query)
    workout = result.mappings().one()
    return {
        'status': 'success',
        'data': workout,
        'details': None,
    }


@router.get("/user-workouts")
async def get_my_workouts(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Workout).filter(Workout.user_id == user_id)
    result = await session.execute(query)
    my_workouts = result.mappings().all()
    return {
        'status': 'success',
        'data': my_workouts,
        'details': None,
    }


@router.get("/sets")
async def get_sets(exercise: int, user: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Set).filter(Set.exercise_id == exercise).filter(Set.user_id == user)
    print('query', query)
    result = await session.execute(query)
    sets = result.mappings().all()
    return {
        'status': 'success',
        'data': sets,
        'details': None,
    }


@router.patch("/workout/update/{workout_id}")
async def update_workout(workout_id: int, name: str, description: str, difficulty: str, total_time: str,
                         session: AsyncSession = Depends(get_async_session)):
    query = (update(Workout).filter(Workout.id == workout_id).values(name=name, description=description,
                                                                     difficulty=difficulty, total_time=total_time))

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.patch("/exercise/update/{exercise_id}")
async def update_exercise(exercise_id: int, name: str, description: str, number_of_sets: int,
                          maximum_repetitions: int, rest_time: int, video: str, photo: str,
                          session: AsyncSession = Depends(get_async_session)):
    query = update(Exercise).filter(Exercise.id == exercise_id).values(name=name, description=description,
                                                                       number_of_sets=number_of_sets,
                                                                       maximum_repetitions=maximum_repetitions,
                                                                       rest_time=rest_time, video=video, photo=photo)

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.patch("/set/update/{set_id}")
async def update_set(set_id: int, count: int, weight: int, session: AsyncSession = Depends(get_async_session)):
    query = update(Set).filter(Set.id == set_id).values(count=count, weight=weight)

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }
