from fastapi import APIRouter, Depends, Query, UploadFile, Form
from sqlalchemy import select, insert, update, func, delete
from ..auth.models import User, Role
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

        total_count_user = await session.scalar(
            select(func.count()).select_from(User)
        )

        users = users_result.mappings().all()
        roles = role_result.mappings().all()
        data = {
            'users': {
                'data_users': users,
                'total_count_users': total_count_user
            },
            'roles': roles
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
