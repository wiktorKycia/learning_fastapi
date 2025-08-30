from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID
app = FastAPI()




BANDS = [
	{'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
	{'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
	{'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
		{'title': 'Master of reality', 'release_date': '1971-07-21'}
	]},
	{'id': 4, 'name': 'Wu-Tang Clean', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands(genre: GenreURLChoices | None = None, has_albums: bool = False) -> list[BandWithID]: # if there would be a list, fastapi will return an internal server error
	bands_list: list[BandWithID] = [BandWithID(**b) for b in BANDS]
	if has_albums:
		bands_list = list(filter(lambda band: len(band.albums), bands_list))
	if genre:
		bands_list = list(filter(lambda band: band.genre == genre.value, bands_list))
	return bands_list

# @app.get('/bands/{band_id}', status_code=206) # if the response is successful, it will return this code
@app.get('/bands/{band_id}')
async def band(band_id: int) -> BandWithID:
	band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)
	if band is None:
		raise HTTPException(status_code=404, detail='Band not found')

	return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
	return [
		b for b in BANDS if b['genre'].lower() == genre.value
	]















