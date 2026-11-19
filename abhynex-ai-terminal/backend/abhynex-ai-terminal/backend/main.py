from fastapi import FastAPI
from api.routes import router
import uvicorn
import os

app = FastAPI(title='ABHYNEX AI TERMINAL - Backend')

app.include_router(router, prefix='/api')

@app.get('/')
def health_check():
    return {'status': 'online', 'project': 'ABHYNEX AI TERMINAL'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)