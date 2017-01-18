import os
from flask import Flask
from config import basedir
from .HostelryManage import HostelryManage


hostelryManage = HostelryManage
app = Flask(__name__)
app.config.from_object('config')


from app import views
