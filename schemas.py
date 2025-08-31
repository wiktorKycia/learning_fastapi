from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator, validator

class GenreURLChoices(Enum):
	ROCK = 'rock'
	ELECTRONIC = 'electronic'
	METAL = 'metal'
	HIP_HOP = 'hip-hop'

class GenreChoices(Enum):
	ROCK = 'Rock'
	ELECTRONIC = 'Electronic'
	METAL = 'Metal'
	HIP_HOP = 'Hip-Hop'

class Album(BaseModel):
	title: str
	release_date: date

class BandBase(BaseModel):
	name: str
	genre: GenreChoices
	albums: list[Album] = [] # default value

class BandCreate(BandBase):
	@validator('genre', pre=True)
	def title_case_genre(cls, value):
		return value.title()

class BandWithID(BandBase):
	id: int