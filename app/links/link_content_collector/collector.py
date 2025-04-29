from common.exceptions import CantGetPageContent
from common.request_sender import RequestSender
from requests.exceptions import RequestException

from links.models import Link, normalize_link_type

from .converter import Converter
from .dto import PageContent


class LinkContentCollector:
    def __init__(self, request_sender: RequestSender, converter: Converter):
        self.request_sender = request_sender
        self.converter = converter

    def collect(self, link: Link, attempts: int = 2) -> None:
        try:
            page_content = self._page_link_content(url=link.url, attempts=attempts)
            Link.objects.filter(pk=link.pk).update(
                parsed_url=page_content.url,
                title=page_content.title,
                description=page_content.description,
                type=normalize_link_type(link_type=page_content.type),
                image_url=page_content.image,
                load_status=Link.LOAD_STATUS_LOADED,
            )
        except CantGetPageContent:
            Link.objects.filter(pk=link.pk).update(
                load_status=Link.LOAD_STATUS_ERROR,
            )

    def _page_link_content(self, url: str, attempts: int) -> PageContent:
        try:
            page_text = self.request_sender.request(url=url, attempts=attempts)
            with open('loaded.html', 'w') as file:
                file.write(page_text)
            return self.converter.convert(text=page_text)
        except RequestException:
            raise CantGetPageContent(f'Cant get content for url: {url}')
