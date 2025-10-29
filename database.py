import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
import weaviate.classes.query as wq

weaviate_url = "https://nkhzok3tri20h0azhycfa.c0.europe-west3.gcp.weaviate.cloud"
weaviate_api_key = "VjJEbHlYc0tvY2RFM2FtTV9VdXhxS0R1SHJPYklpOTl2Z1UyVFpDYTJ6RnFNSzd0Rlh3SkJaWU94UE04PV92MjAw"

def get_weaviate_client():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )
    return client

def create_notes_collection(client):
        if client.collections.exists("Note"):
            print("Collection 'Note' already exists")
            return
        
        client.collections.create(
            name="Note",
            vector_config=Configure.Vectors.text2vec_weaviate(),
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="note_id", data_type=DataType.INT),
            ]
        )

def add_note(client, note_id: int, text: str):
    notes_collection = client.collections.get("Note")
    notes_collection.data.insert(
        properties={
            "text": text,
            "note_id": note_id,
        }
    )
    return None

def get_note_by_id(client, note_id: int):
    notes_collection = client.collections.get("Note")
    response = notes_collection.query.fetch_objects(
        filters=wq.Filter.by_property("note_id").equal(note_id),
    )
    
    if response.objects:
        obj = response.objects[0]
        return {
            "id": obj.properties["note_id"],
            "text": obj.properties["text"],
        }
    return None

def search_notes(client, query: str):
    notes_collection = client.collections.get("Note")
    response = notes_collection.query.near_text(
        query=query,
    )

    results = []
    for obj in response.objects:
        results.append({"id": obj.properties["note_id"], "text": obj.properties["text"],})
    return results

def get_all_notes(client):
    notes_collection = client.collections.get("Note")
    response = notes_collection.query.fetch_objects()
    
    results = []
    for obj in response.objects:
        note_properties = obj.properties
        
        results.append({
            "id": note_properties["note_id"],
            "text": note_properties["text"],
        })
    return results

def delete_note_by_id(client, note_id: int):
    notes_collection = client.collections.get("Note")
    response = notes_collection.query.fetch_objects(
        filters=wq.Filter.by_property("note_id").equal(note_id),
    )
    if not response.objects:
        return False
    
    note_uuid = response.objects[0].uuid
    notes_collection.data.delete_by_id(uuid=note_uuid)
    return True
    
