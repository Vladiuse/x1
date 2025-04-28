from requests.exceptions import RequestException

from common.exceptions import CantGetPageContent
from common.request_sender import RequestSender
from links.models import Link

from .converter import Converter
from .dto import PageContent


class LinkContentCollector:
    def __init__(self, request_sender: RequestSender, converter: Converter):
        self.request_sender = request_sender
        self.converter = converter

    def collect(self, link: Link, attempts: int = 2) -> Link:
        try:
            page_content = self._page_link_content(url=link.url, attempts=attempts)
            link.url = page_content.url
            link.title = page_content.title
            link.description = page_content.description
            link.type = page_content.type
            link.image_url = page_content.image
            link.load_status = Link.LOAD_STATUS_LOADED
        except CantGetPageContent:
            link.load_status = Link.LOAD_STATUS_ERROR
        link.save()
        return link

    def _page_link_content(self, url: str, attempts: int) -> PageContent:
        try:
            page_text = self.request_sender.get_content(url=url, attempts=attempts)
            with open('loaded.html', 'w') as file:
                file.write(page_text)
            return self.converter.convert(text=page_text)
        except RequestException:
            raise CantGetPageContent(f'Cant get content for url: {url}')
