from fastapi import FastAPI

app = FastAPI()

bands = [
	{'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
	{'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
	{'id': 3, 'name': 'Slowdive', 'genre': 'Shoegaze'},
	{'id': 4, 'name': 'Wu-Tang Clean', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands() -> list[dict]: # if there would be a list, fastapi will return an internal server error
	return bands

@app.get('/about')
async def about() -> str:
	return "about page"