from datetime import datetime
from DB_interface import Get_data, get_att_sal, get_data_Txn, get_due, get_payroll, insert_data, get_att_data, insert_data_Txn, insert_data_payroll, update_data
from Utilities.Response_manager import Att_encoder, Txn_decoder, Txn_decoder_sal
from fastapi import FastAPI, HTTPException, Query, Request # type: ignore
from fastapi.responses import JSONResponse, ORJSONResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can use ["*"] for simplicity but it's less secure
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-data")
def show_info():
    fetched_data = Get_data()
    return {fetched_data}

@app.get("/get-att-data")
def show_info(date: str):
    attendance_data = get_att_data(date)
    return attendance_data

@app.get("/check-att-data")
def show_info(date: str):
    exists = bool(get_att_data(date))
    return {"exists": exists}

@app.post("/submit")
async def receive_data(request: Request):
    data = await request.json()
    Att_encoder(data)
    insert_data(data)
    return {"message": "Data updated successfully", "data": data}

@app.put("/update")
async def receive_data(request: Request):
    data = await request.json()
    Att_encoder(data)
    update_data(data)
    return {"message": "Data updated successfully", "data": data}

@app.post("/Txn")
async def receive_data(request: Request):
    data = await request.json()
    Txn_decoder(data)
    insert_data_Txn(data)
    return {"data": data}

@app.post("/Txn-sal")
async def receive_data(request: Request):
    data = await request.json()
    Txn_decoder_sal(data)
    insert_data_Txn(data)
    return {"data": data}

@app.post("/Payroll")
async def receive_data(request: Request):
    data = await request.json()
    insert_data_payroll(data)
    return {"data": data}

@app.get("/get-due")
def show_info(data: int):
    fetched_data = get_due(data)
    return{fetched_data}

@app.get("/get-Txn")
def show_info(data: int):
    fetched_data = get_data_Txn(data)
    return fetched_data

@app.get("/get-att-sal")
def show_info(data: int = Query(..., alias='data'), date: str = Query(..., alias='data2')):
    fetched_data = get_att_sal(data, date)
    return JSONResponse(content=fetched_data)

@app.get("/get-payroll")
def show_info(data: int = Query(..., alias='data'), date: str = Query(..., alias='data2')):
    fetched_data = get_payroll(data, date)
    return JSONResponse(content=fetched_data)
