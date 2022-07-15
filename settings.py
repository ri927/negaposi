# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'env/.env')
load_dotenv(dotenv_path)

BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
API_KEY = os.environ.get("API_KEY") 
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
