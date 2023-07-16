from fastapi import APIRouter

router = APIRouter(prefix='/api/user', tags=['User'])


@router.get('/')
async def get_users():
    return 'Buenas desde router'


@router.get('/{id}')
async def get_user(id: str):
    return 'Buenas desde router'


@router.post('/')
async def create_user():
    return 'Buenas desde router'


@router.put('/{id}')
async def update_user(id: str):
    return 'Buenas desde router'


@router.delete('/{id}')
async def delete_user(id: str):
    return 'Buenas desde router'
