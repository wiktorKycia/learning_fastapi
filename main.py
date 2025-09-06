from fastapi import FastAPI, HTTPException, Path, Query, Depends
from schemas import GenreURLChoices, BandBase, BandCreate, Band, Album
from typing import Annotated
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from db import init_db, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
	init_db()
	yield

app = FastAPI(lifespan=lifespan) # lifespan triggers before or after the app is running




BANDS = [
	{'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
	{'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
	{'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
		{'title': 'Master of reality', 'release_date': '1971-07-21'}
	]},
	{'id': 4, 'name': 'Wu-Tang Clean', 'genre': 'Hip-Hop'},
]

# @app.get('/bands')
# async def bands(
# 		genre: GenreURLChoices | None = None,
# 		has_albums: bool = False,
# 		q: Annotated[str | None, Query(max_length=10)] = None # returns an error (422) if the string is longer than 10
# ) -> list[BandWithID]: # if there would be a list, fastapi will return an internal server error
# 	bands_list: list[BandWithID] = [BandWithID(**b) for b in BANDS]
# 	if has_albums:
# 		bands_list = list(filter(lambda band: len(band.albums), bands_list))
# 	if genre:
# 		bands_list = list(filter(lambda band: band.genre.value.lower() == genre.value, bands_list))
# 	if q:
# 		bands_list = [
# 			b for b in bands_list if q.lower() in b.name.lower()
# 		]
# 	return bands_list
#
# # @app.get('/bands/{band_id}', status_code=206) # if the response is successful, it will return this code
# @app.get('/bands/{band_id}')
# async def band(band_id: Annotated[int, Path(title="The band ID")]) -> BandWithID:
# 	band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)
# 	if band is None:
# 		raise HTTPException(status_code=404, detail='Band not found')
#
# 	return band
#
# @app.get('/bands/genre/{genre}')
# async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
# 	return [
# 		b for b in BANDS if b['genre'].lower() == genre.value
# 	]
#
#
# @app.post('/bands')
# async def create_band(band_data: BandCreate) -> BandWithID:
# 	id = BANDS[-1]['id'] + 1
# 	band = BandWithID(id=id, **band_data.model_dump())
# 	BANDS.append(band.model_dump())
# 	return band

@app.get('/bands')
async def bands(
		genre: GenreURLChoices | None = None,
		has_albums: bool = False,
		q: Annotated[str | None, Query(max_length=10)] = None, # returns an error (422) if the string is longer than 10
		session: Session = Depends(get_session)
) -> list[Band]: # if there would be a list, fastapi will return an internal server error

	bands_list = session.exec(select(Band)).all()

	if has_albums:
		bands_list = list(filter(lambda band: len(band.albums), bands_list))
	if genre:
		bands_list = list(filter(lambda band: band.genre.value.lower() == genre.value, bands_list))
	if q:
		bands_list = [
			b for b in bands_list if q.lower() in b.name.lower()
		]
	return bands_list


# @app.get('/bands/{band_id}', status_code=206) # if the response is successful, it will return this code
@app.get('/bands/{band_id}')
async def band(
		band_id: Annotated[int, Path(title="The band ID")],
		session: Session = Depends(get_session)
) -> Band:
	band = session.get(Band, band_id)
	if band is None:
		raise HTTPException(status_code=404, detail='Band not found')

	return band



@app.post('/bands')
async def create_band(
		band_data: BandCreate,
		session: Session = Depends(get_session)
) -> Band:
	band = Band(name=band_data.name, genre=band_data.genre)
	session.add(band)

	if band_data.albums:
		for album in band_data.albums:
			album_obj = Album(title=album.title, release_date=album.release_date, band=band)

			session.add(album_obj)

	session.commit() # primary key is added to the band after the commit method, but only in database
	session.refresh(band) # to add the id to the band object, we need to refresh it
	return band



