from fastapi import APIRouter, HTTPException, Depends

from src.auth.auth import user_dependency
from src.services.snippet import *

from src.schemas.snippet import Snippets, SnippetCreate, SnippetUpdate
from src.api.v1.auth import has_role

snippets_router = APIRouter(prefix="/snippets", tags=["snippets"])

@snippets_router.get("/{snippet_id}", dependencies=[Depends(has_role(["user", "admin"]))])
async def read_snippet(snippet_id: int, db: db_dependency):
    snippet = await get_snippet_by_id(db, snippet_id)
    if snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

@snippets_router.get("/author/{author}", dependencies=[Depends(has_role(["user", "admin"]))])
async def read_snippets_by_author(author: str, db: db_dependency):
    snippets = await get_snippet_by_author(db, author)
    if not snippets:
        raise HTTPException(status_code=404, detail="No snippets found for this author")
    return snippets

@snippets_router.get("/", dependencies=[Depends(has_role(["user", "admin"]))])
async def read_snippets(db: db_dependency, skip: int = 0, limit: int = 10,):
    snippets = await get_snippets(db, skip, limit)
    return snippets

@snippets_router.post("/", dependencies=[Depends(has_role(["user", "admin"]))])
async def create_snippet_route(snippet: SnippetCreate, db: db_dependency, current_user: user_dependency):
    return await create_snippet(db, snippet.text, current_user)

@snippets_router.put("/{snippet_id}", dependencies=[Depends(has_role(["user", "admin"]))])
async def update_snippet_route(snippet_id: int, snippet: SnippetUpdate, db: db_dependency):
    updated_snippet = await update_snippet(db, snippet_id, snippet.text)
    if updated_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return updated_snippet

@snippets_router.delete("/{snippet_id}",
                        dependencies=[Depends(has_role(["admin"]))])
async def delete_snippet_route(snippet_id: int, db: db_dependency):
    deleted_snippet = await delete_snippet(db, snippet_id)
    if deleted_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return deleted_snippet

@snippets_router.post("/{snippet_id}/share", dependencies=[Depends(has_role(["user", "admin"]))])
async def share_snippet(snippet_id: int, db: db_dependency):
    snippet = await get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {"share_url": f"/share/{snippet.share_id}"}

@snippets_router.get("/share/{share_id}", response_model=Snippets)
async def get_shared_snippet(share_id: str, db: db_dependency):
    snippet = await get_snippet_by_share_id(db, share_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet