"""Base metallum class for collections (e.g. albums)"""

from metallum.models.metallum import Metallum


class MetallumCollection(Metallum, list):
    """Base metallum class for collections (e.g. albums)"""

    def search(self, **kwargs) -> "MetallumCollection":
        """
        Query the collection based on one or more key value pairs, where the
        keys are attributes of the contained objects:

        Args:
            **kwargs: Key value pairs to filter the collection

        Returns:
            MetallumCollection: A new collection containing only the items
            that match the search criteria

        Examples:
            >>> len(band.albums.search(title='master of puppets'))
            2

            >>> len(band.albums.search(title='master of puppets', type=AlbumTypes.FULL_LENGTH))
            1
        """
        collection = self[:]
        for key, value in kwargs.items():
            for item in collection[:]:
                if value.lower() != getattr(item, key).lower():
                    try:
                        collection.remove(item)
                    except ValueError:
                        continue
        return collection
