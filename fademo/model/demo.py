# -*- coding: utf-8 -*-
from elixir import *
from fa.jquery.utils import HTML, Color, Slider
from datetime import datetime

class Article(Entity):

    title = Field(Unicode, required=True)
    text = Field(HTML)
    publication_date = Field(Date, default=datetime.now)


class Widgets(Entity):

    autocomplete = Field(Unicode)
    slider = Field(Slider, default=0)
    color = Field(Color)
    date = Field(Date)
    date_time = Field(DateTime, default=datetime.now)

