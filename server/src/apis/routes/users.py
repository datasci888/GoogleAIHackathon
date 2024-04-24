from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.post(path="", description="Create a resource")
async def create():
    pass


@router.get(path="", description="Read all resources")
async def read_all():
    pass


@router.get(path="/{id}", description="Read a resource")
async def read(id):
    pass


@router.patch(path="/{id}", description="Update a resource")
async def update(id):
    pass


@router.delete(path="/{id}", description="Delete a resource")
async def delete(id):
    pass
