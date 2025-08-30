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
async def get_random_number() -> RandomNumberType:
	"""Returns a random number between 1 and 10"""
	return RandomNumberType(**{"number": random.randint(1, 10)})