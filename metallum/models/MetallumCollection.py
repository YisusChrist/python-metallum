from metallum.models.Metallum import Metallum


class MetallumCollection(Metallum, list):
    """Base metallum class for collections (e.g. albums)"""

    def __init__(self, url):
        super().__init__(url)

    def search(self, **kwargs) -> "MetallumCollection":
        """Query the collection based on one or more key value pairs, where the
        keys are attributes of the contained objects:

        >>> len(band.albums.search(title='master of puppets'))
        2

        >>> len(band.albums.search(title='master of puppets', type=AlbumTypes.FULL_LENGTH))
        1
        """
        collection = self[:]
        for arg in kwargs:
            for item in collection[:]:
                if kwargs[arg].lower() != getattr(item, arg).lower():
                    try:
                        collection.remove(item)
                    except ValueError:
                        continue
        return collection