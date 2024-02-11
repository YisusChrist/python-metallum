from typing import Optional

from pyquery import PyQuery

from metallum.models.Metallum import Metallum


class MetallumEntity(Metallum):
    """Represents a metallum entity (artist, album...)"""

    def _dd_element_for_label(self, label: str) -> Optional[PyQuery]:
        """Data on entity pages are stored in <dt> / <dd> pairs"""
        labels = list(self._page("dt").contents())

        try:
            index = labels.index(label)
        except ValueError:
            return None

        return self._page("dd").eq(index)

    def _dd_text_for_label(self, label: str) -> str:
        element = self._dd_element_for_label(label)
        return element.text() if element else ""
