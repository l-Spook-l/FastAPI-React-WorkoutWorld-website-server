from fastapi import APIRouter, Depends, Query, UploadFile, Form
from sqlalchemy import select, insert, update, func, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from ..auth.models import User, Role
from ..workouts.models import Workout, Exercise
from ..auth.base_config import current_user
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

router = APIRouter(
    # prefix - url путь
    prefix="/admin",
    # tags - группа к которой он относиться
    tags=["Admin"]
)


@router.post("/")
async def admin(user: User = Depends(current_user),
                session: AsyncSession = Depends(get_async_session)):
    try:
        if not user.is_superuser:
            raise HTTPException(status_code=403)

        query_users = select(User)
        users_result = await session.execute(query_users)
        query_role = select(Role)
        role_result = await session.execute(query_role)
        query_workouts = select(Workout)
        workout_result = await session.execute(query_workouts)

        total_count_user = await session.scalar(
            select(func.count()).select_from(User)
        )
        total_count_workouts = await session.scalar(
            select(func.count()).select_from(Workout)
        )

        users = users_result.mappings().all()
        roles = role_result.mappings().all()
        workouts = workout_result.mappings().all()

        data = {
            'users': {
                'data_users': users,
                'total_count_users': total_count_user
            },
            'roles': roles,
            'workouts': {
                'data_workouts': workouts,
                'total_count_workouts': total_count_workouts
            }
        }

        return {"status": "success", 'data': data}
    except HTTPException as http_error:
        if http_error.status_code == 403:
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })


@router.get("/workout/{workout_id}")
async def get_one_workout(workout_id: int, user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):

    if not user.is_superuser:
        raise HTTPException(status_code=403)

    query = (select(Workout).filter(Workout.id == workout_id).
             options(selectinload(Workout.exercise).options(selectinload(Exercise.photo))))
    try:
        result = await session.execute(query)
        workout = result.mappings().one()

        return {
            'status': 'success',
            'data': workout,
            'details': None,
        }

    except NoResultFound:
        raise HTTPException(status_code=404, detail="This workout not found")
    except HTTPException as http_error:
        if http_error.status_code == 403:
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
