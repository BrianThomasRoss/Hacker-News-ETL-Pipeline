from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .api import classify

app = FastAPI(
    title='Sentiment Analysis API',
    description='Simple sentiment analysis using vaderSentiment',
    version='0.1',
    docs_url='/',
)

app.include_router(classify.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
