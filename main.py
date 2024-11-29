from fastapi import FastAPI, Form
from datetime import date
from typing import Optional
from typing import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Orders(BaseModel):
    number: int
    startDate: Optional[date] = date.today()
    orgTechType: str
    orgTechModel: str
    problemDescryption: str
    FIO: str
    phoneNumber: str
    requestStatus: str
    completionDate: date
    master: Optional[str] = None
    comment: Optional[str] = None

app = FastAPI()

repo = [Orders(number = 1, startDate = "2024-11-28", orgTechType = "Компьютер", orgTechModel = "DEXP Aquilon O286", problemDescryption = "Перестал работать", FIO = "Ivanov Ivan Ivonovich", phoneNumber = "79512642831", requestStatus = "Завершена", completionDate = "2024-11-29"),
        Orders(number = 1, startDate = "2024-11-28", orgTechType = "Компьютер", orgTechModel = "DEXP Aquilon O286", problemDescryption = "Перестал работать", FIO = "Ivanov Ivan Ivonovich", phoneNumber = "79512642831", requestStatus = "Завершена", completionDate = "2024-11-29", )]

massage = ""
ifUpdateStatus = False


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get("/")
def get_orders():
    global massage
    global ifUpdateStatus
    if(ifUpdateStatus):
        buffer = message
        message = ""
        ifUpdateStatus = False
        return repo, buffer
    else:
        return repo
        

@app.get("/get/order")
def get_order(number: int = None, orgTechType: str = None, orgTechModel: str = None, FIO: str = None):
    for i in repo:
        if number == i.number or orgTechModel == i.orgTechModel or orgTechType == i.orgTechType or FIO == i.FIO:
            return i
    return "Заявка не найдена"

@app.get("/get/status")
def get_order(number: int):
    for i in repo:
        if number == i.number:
            result = f"Статус заявки №{i.number} - {i.requestStatus}"
        return result
    return "Заявка не найдена"

@app.get("/get/statistic")
def get_stat():
    return {"count_complete": count_complete(),
             "avg_date": avg_date(),
             "stat_problem": stat_problem()}

@app.post("/")
def add_order(orders: Annotated[Orders, Form()]):
    repo.append(orders)
    return "Данные успешно добавлены"

@app.put("/add/comment")
def add_comment(number: int, comment: str):
    for i in repo:
        if number == i.number:
            i.comment = comment
        return True

@app.put("/")
def update_order(number: int, status: str, description: str, master):
    global massage
    global ifUpdateStatus
    for i in repo:
        if number == i.number:
            if status != i.requestStatus:
                i.requestStatus = status
                massage = f"Статус заявки №{i.number} изменился"
                ifUpdateStatus = True
                if status == "Завершена":
                    i.completionDate = date.today()
                    massage = f"Заявка №{i.number} завершена"
                    ifUpdateStatus = True
            i.problemDescryption = description
            i.master = master
        return "Данные успешно обновлены"
    return "Заявка не найдена"



def complete_orders():
    return[ord for ord in repo if ord.requestStatus == "Завершена"]

def count_complete():
    return len(complete_orders())

def stat_problem():
    result = {}
    for o in repo:
        if o.orgTechType in result:
            result[o.orgTechType] += 1 
        else:
            result[o.orgTechType] = 1
    return result

def avg_date():
    times = []
    for ord in complete_orders():
        times.append(ord.completionDate - ord.startDate)
    timesum = sum([t.days for t in times])
    ordCount = count_complete()
    result = timesum/ordCount
    return result