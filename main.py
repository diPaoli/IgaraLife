from datetime import date

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import LeituraModel
from schemas import LeituraSchema
from database import engine


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', status_code=status.HTTP_200_OK)
async def get_all(request: Request):
    with Session(engine) as session:
        query = select(LeituraModel)
        lista = session.execute(query).scalars().all()
        return templates.TemplateResponse("consulta.html", {"request": request, "leituras": lista})


@app.get('/lista/ap/{ap_num}', status_code=status.HTTP_200_OK)
async def get_leituras_by_ap(request: Request, ap_num: int):
    with Session(engine) as session:
        query = select(LeituraModel).filter_by(apartamento=ap_num)
        lista = session.execute(query).scalars().all()
        return templates.TemplateResponse("consulta.html", {"request": request, "leituras": lista})


@app.get('/lista/{id_leitura}', status_code=status.HTTP_200_OK)
def get_leitura_by_id(id_leitura: int):
    with Session(engine) as session:
        query = select(LeituraModel).filter_by(id=id_leitura)
        result = session.execute(query).first()
        return result


# TODO: Filtro por data
@app.get('/lista/data/{data}', status_code=status.HTTP_200_OK)
def get_leituras_by_date(data: date):
    with Session(engine) as session:
        query = select(LeituraModel).filter_by(data=data)
        result = session.execute(query).all()
        return result


# TODO: Filtro por período
@app.get('/lista/data/{data_ini}/{data_fin}', status_code=status.HTTP_200_OK)
def get_leituras_within_period(data_ini, data_fin: date):
    with Session(engine) as session:
        query = select(LeituraModel).filter(LeituraModel.data >= data_ini, LeituraModel.data <= data_fin)
        result = session.execute(query).all()
        return result


@app.get('/leitura')
async def qrcode_scan(request: Request):
    return templates.TemplateResponse("leitura.html", {"request": request, "msg": "Teste"})


@app.post('/leitura')
async def post_leitura(request: Request):
    form = jsonable_encoder(await request.form())
    leitura_body = LeituraSchema(
        apartamento=form['ap'],
        gas = form['igas'],
        agua = form['iagua'],
        data = date.today()
        )
    msg = grava_leitura(leitura_body)
    return templates.TemplateResponse("leitura.html", {"request": request, "msg": msg})


def grava_leitura(leitura_body: LeituraSchema):
    with Session(engine) as session:
        try:
            leitura = LeituraModel.create_from_schema(leitura_body)
            session.add(leitura)
            session.commit()
            session.refresh(leitura)
            return "OK"
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception)) from exception


# TODO: Se precisar, fazer tela para editar/excluir registros
# @app.delete('/leitura/{leitura_id}', status_code=status.HTTP_200_OK)
# def delete_leitura(leitura_id: int):
#     with Session(engine) as session:
#         try:
#             leitura = session.get(LeituraModel, leitura_id)
#             if not leitura:
#                 return Response(status_code=status.HTTP_404_NOT_FOUND)
#             session.delete(leitura)
#             session.commit()
#             return Response(status_code=status.HTTP_200_OK)
#         except Exception as exception:
#             raise HTTPException(status_code=500, detail=str(exception)) from exception


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
