# -*- coding: utf-8 -*-
from elixir import *
from fa.jquery.utils import HTML
from datetime import datetime

class Article(Entity):

    title = Field(Unicode, required=True)
    text = Field(HTML)
    publication_date = Field(Date, default=datetime.now)


