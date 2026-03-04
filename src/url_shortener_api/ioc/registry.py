from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from url_shortener_api.ioc.providers import AppProvider

container: AsyncContainer = make_async_container(
    AppProvider(),
    FastapiProvider(),
)
