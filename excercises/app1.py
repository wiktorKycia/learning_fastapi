from fastapi import FastAPI
import random
from pydantic import BaseModel

class RandomNumberType(BaseModel):
	number: int
app = FastAPI()


@app.get('/')
async def home() -> str:
	return "hello world!"

@app.get('/random')
async def get_random_number(a: int = 1, b: int = 10) -> RandomNumberType:
	"""
	Returns a random number between a and b including both values

	:param a: int, from
	:param b: int, to
	"""
	return RandomNumberType(**{"number": random.randint(a, b)})