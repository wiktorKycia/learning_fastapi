from fastapi import FastAPI, HTTPException

app = FastAPI()

BANDS = [
	{'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
	{'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
	{'id': 3, 'name': 'Slowdive', 'genre': 'Shoegaze'},
	{'id': 4, 'name': 'Wu-Tang Clean', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands() -> list[dict]: # if there would be a list, fastapi will return an internal server error
	return BANDS

@app.get('/bands/{band_id}')
async def band(band_id: int) -> dict:
	band = next((b for b in BANDS if b['id'] == band_id), None)
	if band is None:
		raise HTTPException(status_code=404, detail='Band not found')

	return band

















