import uvicorn

from weather_api.server import app

if __name__ == '__main__':
    uvicorn.run(app)
