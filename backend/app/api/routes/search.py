from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.services.search_service import SearchService
from app.api.dependencies import get_search_service
from pydantic import BaseModel

router = APIRouter()

class SearchResponse(BaseModel):
    id: str
    title: str
    snippet: str
    score: float

@router.get("/", response_model=List[SearchResponse])
async def search_documents(
    q: str = Query(..., description="Search query string"),
    filters: Optional[str] = Query(None, description="Category or date filters"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Perform a search query. Supports keyword, boolean, and phrase searches.
    """
    results = await search_service.execute_search(q, filters, page, size)
    return results

@router.get("/autocomplete")
async def autocomplete(
    prefix: str = Query(..., min_length=1),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Get Trie-based autocomplete suggestions for the given prefix.
    """
    suggestions = await search_service.get_suggestions(prefix)
    return {"suggestions": suggestions}
