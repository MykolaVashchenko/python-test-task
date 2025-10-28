from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NoteCreate(BaseModel):
    text: str

id = 1
notes = {}

@app.post("/notes")
async def create_note(note: NoteCreate):
    global id
    note_id = id
    new_note = {
        "id": note_id,
        "text": note.text
    }
    notes[note_id] = new_note
    id += 1
    return new_note

@app.get("/notes/get_all_notes")
async def print_all_notes():
    return notes

@app.get("/notes/{note_id}")
async def read_note(note_id: int):
    if note_id not in notes:
        return "Error, note not found"
    else:
        return notes[note_id]
    
