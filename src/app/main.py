# import os
# import uvicorn
# from fastapi import FastAPI
# from db import database
# from api.v1.api import api_router
#
# app = FastAPI()
# app.include_router(api_router)
#
# if __name__ == '__main__':
#     database.create_db_if_missing()
#     database.create_tables_if_missing()
#     uvicorn.run('main:app', host='127.0.0.1', port=os.environ.get('LOCAL_PORT', 8000))
