from bs4 import BeautifulSoup

from .dto import PageContent


class Converter:
    DEFAULT_TITLE = 'Нет заголовка'

    def convert(self, text: str) -> PageContent:
        soup = BeautifulSoup(text, 'lxml')
        title = self._get_meta_tag(soup=soup, name='og:title')
        description = self._get_meta_tag(soup=soup, name='og:description')
        url = self._get_meta_tag(soup=soup, name='og:url')
        image = self._get_meta_tag(soup=soup, name='og:image')
        page_type = self._get_meta_tag(soup=soup, name='og:type')
        return PageContent(
            title=title,
            description=description,
            url=url,
            image=image,
            type=page_type,
        )

    def _get_meta_tag(self, soup: BeautifulSoup, name: str) -> str | None:
        elem = soup.find('meta', attrs={'property': name})
        if elem is None:
            return None
        try:
            return elem['content']
        except KeyError:
            return None
