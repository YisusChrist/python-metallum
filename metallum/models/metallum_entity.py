"""Base class for all entities on Metal Archives"""

from typing import Optional

from pyquery import PyQuery

from metallum.models.metallum import Metallum


class MetallumEntity(Metallum):
    """Represents a metallum entity (artist, album...)"""

    def _dd_element_for_label(self, label: str) -> Optional[PyQuery]:
        """
        Data on entity pages are stored in <dt> / <dd> pairs

        Args:
            label: The label to search for

        Returns:
            PyQuery: The <dd> element corresponding to the label
        """
        labels = list(self._page("dt").contents())

        try:
            index = labels.index(label)
        except ValueError:
            return None

        return self._page("dd").eq(index)

    def _dd_text_for_label(self, label: str) -> str:
        """
        Get the text of the <dd> element corresponding to the label

        Args:
            label: The label to search for

        Returns:
            str: The text of the <dd> element
        """
        element = self._dd_element_for_label(label)
        return element.text() if element else ""
