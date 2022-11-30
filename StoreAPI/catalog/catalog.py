from fastapi import Request, HTTPException, APIRouter

from StoreAPI.catalog.get_catalog import get_catalog
from services.schemas.schemas import CatalogProductSchema

catalog_router = APIRouter()


@catalog_router.get('/catalog', response_model=list[CatalogProductSchema])
async def catalog(request: Request, page: int = 1) -> list[CatalogProductSchema]:
    completed_catalog = await get_catalog(request=request, page=page)
    if completed_catalog:
        return completed_catalog
    raise HTTPException(status_code=404, detail="The catalog hasn't that specified page number")
