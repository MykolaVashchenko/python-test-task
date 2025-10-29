from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database as db

app = FastAPI()

class NoteCreate(BaseModel):
    text: str

weaviate_client = db.get_weaviate_client()
db.create_notes_collection(weaviate_client)

note_counter = 1

@app.post("/notes")
async def create_note(note: NoteCreate):
    global note_counter
    note_id = note_counter
    try:
        db.add_note(weaviate_client, note_id, note.text)
        note_counter += 1
        return {
            "id": note_id,
            "text": note.text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating note: {str(e)}")

@app.get("/notes/all")
async def get_notes():
    notes = db.get_all_notes(weaviate_client)
    return notes

@app.get("/notes/{note_id}")
async def read_note_by_id(note_id: int):
    note = db.get_note_by_id(weaviate_client, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.get("/search")
async def search_notes(q: str):
    try:
        results = db.search_notes(weaviate_client, q)
        return {
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching notes: {str(e)}")
    
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    result = db.delete_note_by_id(weaviate_client, note_id)
    if result is True:
        return "Note deleted successfully"
    else:
        raise HTTPException(status_code=404, detail="Note not found")