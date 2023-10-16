from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import json

def item_lookup(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_lookup(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_lookup(item, lookup_key)

app = FastAPI()

@app.post("/uploadfile/{search_field}")
async def create_upload_file(search_field: str,file: UploadFile = File(...)):
    fcc_data = json.load(file.file)
    output = []
    for i in item_lookup(fcc_data, search_field ):
        ans = {search_field: i}
        output.append(ans)
    return {"Results": output}
