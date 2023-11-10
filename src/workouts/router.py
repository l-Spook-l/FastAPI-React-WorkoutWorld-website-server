from fastapi import APIRouter, Depends, Query, UploadFile, Form
from sqlalchemy import select, insert, update, func, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi.exceptions import HTTPException
import aiofiles
from uuid import uuid4
import os

# router - объединяет несколько endpoints(url)
# и вызываем в main
from .models import Workout, Exercise, Set, added_workouts_association, Exercise_photo, DifficultyWorkout
from ..auth.models import User
from .schemas import (
    WorkoutCreate, ExerciseCreate, SetCreate, WorkoutUpdate, ExerciseUpdate, SetUpdate, DifficultyWorkoutRead)

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


@router.post("/create_exercise")  # 19:00 номер видео 4
async def add_video_exercise(
        name: str = Form(...),
        workout_id: int = Form(...),
        description: str = Form(...),
        number_of_sets: int = Form(...),
        maximum_repetitions: int = Form(...),
        rest_time: int = Form(...),
        video: UploadFile = None,
        photos: list[UploadFile] = None,
        session: AsyncSession = Depends(get_async_session)):
    # print('video', f"src/static/Photos exercise/{video.filename}_{uuid4()}")
    # exercise_data = f"src/static/Photos exercise/{exercise_data.name}_{video.filename}"
    # print('weqwqe', video)

    exercise_data = ExerciseCreate(
        name=name,
        workout_id=workout_id,
        description=description,
        number_of_sets=number_of_sets,
        maximum_repetitions=maximum_repetitions,
        rest_time=rest_time,
    )

    if video:
        video.filename = video.filename.lower()
        path_video = f"src/media/Video_exercise/{name}_{uuid4()}.png"
        async with aiofiles.open(path_video, '+wb') as buffer:
            data = await video.read()
            await buffer.write(data)
        exercise_data.video = path_video[4:]

    stat = insert(Exercise).values(**exercise_data.model_dump(exclude_none=True)).returning(Exercise.id)
    result = await session.execute(stat)
    id = result.scalar()

    if photos:
        for photo in photos:
            photo.filename = photo.filename.lower()
            path_photos = f"src/media/Photos_exercise/{id}_{name}_{uuid4()}.png"
            async with aiofiles.open(path_photos, '+wb') as buffer:
                data = await photo.read()
                await buffer.write(data)
            add_photos = insert(Exercise_photo).values(photo=path_photos[4:], exercise_id=id)
            await session.execute(add_photos)

    await session.commit()
    return {"status": "success", 'exercise_ID': id}


@router.post("/create_set")
async def add_set(number_sets: int, new_set: SetCreate, session: AsyncSession = Depends(get_async_session)):
    for _ in range(number_sets):
        stat = insert(Set).values(**new_set.dict())
        await session.execute(stat)
    await session.commit()
    return {"status": "success"}


@router.post("/add-workout-to-user/{user_id}/{workout_id}")
async def add_workout_to_user(user_id: int, workout_id: int, session: AsyncSession = Depends(get_async_session)):
    # Проверяем, существует ли уже такая связь
    existing_association = select(added_workouts_association).where(
        (added_workouts_association.c.user_table == user_id) &
        (added_workouts_association.c.workout_table == workout_id)
    )
    result_existing = await session.execute(existing_association)
    if result_existing.scalar():
        raise HTTPException(status_code=400, detail="This workout is already added to the user")

    query_user = select(User).filter(User.id == user_id)
    result_user = await session.execute(query_user)
    user = result_user.first()
    query_workout = select(Workout).filter(Workout.id == workout_id)
    result_workout = await session.execute(query_workout)
    workout = result_workout.first()

    if not user or not workout:
        raise HTTPException(status_code=404, detail="User or Workout not found")

    # Создаем новую связь
    new_association = insert(added_workouts_association).values(user_table=user_id, workout_table=workout_id)
    await session.execute(new_association)
    await session.commit()

    return {"status": "success", "message": "Workout added to user"}


# response_model - для лучшей документации
@router.get("/")
async def get_workouts(
        name: str = Query(None, description="Filter by name"),
        difficulty: list[str] = Query(None, description="Filter by difficulty"),
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(12, description="Number of records to return"),
        page: int = Query(1, description="Page number"),
        session: AsyncSession = Depends(get_async_session)):

    # Нормализация запроса для безопасности (предотвращение SQL-инъекций)
    query_name = f"%{name}%"

    try:
        # Создаем базовый запрос
        query = select(Workout)
        # Применяем фильтры, если они предоставлены в name или difficulty
        if name:  # Выбираем все записи из табл. Workout и по названию
            query = query.filter(Workout.name.ilike(query_name))
        if difficulty:  # Выбираем все записи из табл. Workout и по сложности
            query = query.filter(Workout.difficulty.in_(difficulty))

        # добавляем лимиты и сортировку по полю is_public если оно True
        query = query.limit(limit).offset(skip).filter(Workout.is_public)
        # делаем запрос в БД
        result = await session.execute(query)
        # подсчет общего количества записей
        total_count = await session.scalar(
            select(func.count())
            .select_from(Workout)
            .filter(Workout.name.ilike(query_name) if name else True)
            .filter(Workout.difficulty.in_(difficulty) if difficulty else True)
        )
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
    query = (select(Workout).filter(Workout.id == workout_id).
             options(selectinload(Workout.exercise).options(selectinload(Exercise.photo))))
    result = await session.execute(query)
    workout = result.mappings().one()
    return {
        'status': 'success',
        'data': workout,
        'details': None,
    }


@router.get("/user-workouts")
async def get_my_workouts(user_id: int,
                          name: str = Query(None, description="Filter by name"),
                          difficulty: list[str] = Query(None, description="Filter by difficulty"),
                          skip: int = Query(0, description="Number of records to skip"),
                          limit: int = Query(12, description="Number of records to return"),
                          is_public: bool = Query(None, description="Filter by status"),
                          page: int = Query(1, description="Page number"),
                          session: AsyncSession = Depends(get_async_session)):
    query_name = f"%{name}%"

    try:
        query = select(Workout)
        # Применяем фильтры
        if name:  # Выбираем все записи из табл. Workout и по названию
            query = query.filter(Workout.name.ilike(query_name))
        if difficulty:  # Выбираем все записи из табл. Workout и по сложности
            query = query.filter(Workout.difficulty.in_(difficulty))
        if is_public is not None:
            query = query.filter(Workout.is_public == is_public)

        query = query.filter(Workout.user_id == user_id).limit(limit).offset(skip)
        result = await session.execute(query)
        my_workouts = result.mappings().all()
        # Запрос для общего количества отфильтрованных и отсортированных тренировок
        total_count = await session.scalar(
            select(func.count())
            .select_from(Workout)
            .filter(Workout.user_id == user_id)
            .filter(Workout.name.ilike(query_name) if name else True)
            .filter(Workout.difficulty.in_(difficulty) if difficulty else True)
            .filter(Workout.is_public == is_public if is_public is not None else True)
        )

        return {
            'status': 'success',
            'data': my_workouts,
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


@router.get("/get-user-added-workouts/{user_id}")
async def get_user_workouts(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query_user = select(User).filter(User.id == user_id)
    result_user = await session.execute(query_user)
    user = result_user.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Используем SQLAlchemy запрос для получения связанных тренировок пользователя
    # ПОМЕНЯТЬ ТАБЛИЦУ ОБЩУЮ
    stmt = select(Workout).join(added_workouts_association).filter(added_workouts_association.c.user_table == user_id)
    result = await session.execute(stmt)
    user_workouts = result.mappings().all()
    return {"user_id": user_id, "workouts": user_workouts}


@router.get("/workout-difficulties")
async def get_difficulty(session: AsyncSession = Depends(get_async_session)):
    query = select(DifficultyWorkout)
    result = await session.execute(query)
    difficulty = result.mappings().all()
    return {
        'status': 'success',
        'data': difficulty,
        'details': None,
    }


@router.get("/sets")
async def get_sets(user_id: int, exercise_ids: list[int] = Query(None),  session: AsyncSession = Depends(get_async_session)):
    # вывод в порядке id
    query = select(Set).filter(Set.exercise_id.in_(exercise_ids)).filter(Set.user_id == user_id).order_by(Set.id)
    result = await session.execute(query)
    sets = result.mappings().all()
    return {
        'status': 'success',
        'data': sets,
        'details': None,
    }


@router.patch("/workout/update/{workout_id}")
async def update_workout(workout_id: int, update_data: WorkoutUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Workout).filter(Workout.id == workout_id).values(**update_data.model_dump(exclude_none=True))

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.patch("/exercise/update/{exercise_id}")
async def update_exercise(exercise_id: int, update_data: ExerciseUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Exercise).filter(Exercise.id == exercise_id).values(**update_data.model_dump(exclude_none=True))

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.patch("/set/update/{set_id}")
async def update_set(set_id: int, update_data: SetUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Set).filter(Set.id == set_id).values(**update_data.model_dump(exclude_none=True))

    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.delete("/delete/created-workout")
async def delete_created_workout(workout_id: int, session: AsyncSession = Depends(get_async_session)):
    workout = await session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    exercises = await session.execute(select(Exercise).filter(Exercise.workout_id == workout_id))
    exercises_2 = exercises.mappings().all()
    for exercise in exercises_2:
        photos_exercise = await session.execute(select(Exercise_photo).filter(Exercise_photo.exercise_id == exercise.Exercise.id))
        result_photos_exercise = photos_exercise.mappings().all()
        for photo in result_photos_exercise:
            photo_path = os.path.join(photo.Exercise_photo.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)

    workout = delete(Workout).filter(Workout.id == workout_id)

    await session.execute(workout)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.delete("/delete/added-workout")
async def delete_added_workout(workout_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(added_workouts_association).where(
        (added_workouts_association.c.workout_table == workout_id) and
        (added_workouts_association.c.user_table == user_id)
    )
    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }


@router.delete("/delete/added-sets")
async def delete_added_sets(exercise_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Set).where(
        (Set.exercise_id == exercise_id) and
        (Set.user_id == user_id)
    )
    await session.execute(query)
    await session.commit()

    return {
        'status': 'success',
        'details': None,
    }
