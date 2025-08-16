from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def index() -> dict[str, str]: # if there would be a list, fastapi will return an internal server error
	return {'content': 'hello world!'}

@app.get('/about')
async def about() -> str:
	return "about page"