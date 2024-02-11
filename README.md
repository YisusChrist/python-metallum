<p align="center"><img width="750" src="https://www.metal-archives.com/css/default/images/smallerlogo.jpg" alt="python-metallum"></p>

<p align="center">
    <a href="https://github.com/YisusChrist/python-metallum/issues">
        <img src="https://img.shields.io/github/issues/YisusChrist/python-metallum?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/python-metallum/forks">
        <img src="https://img.shields.io/github/forks/YisusChrist/python-metallum?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/python-metallum/">
        <img src="https://img.shields.io/github/stars/YisusChrist/python-metallum?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/python-metallum/actions">
        <img alt="Tests Passing" src="https://github.com/YisusChrist/python-metallum/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/python-metallum/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/YisusChrist/python-metallum?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/gpl-2-0/">
        <img alt="License" src="https://img.shields.io/github/license/YisusChrist/python-metallum?color=0088ff">
    </a>
</p>

<br>

<p align="center">
    <a href="https://github.com/YisusChrist/python-metallum/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/YisusChrist/python-metallum/issues/new/choose">Request Feature</a>
    ·
    <a href="https://github.com/YisusChrist/python-metallum/discussions">Ask Question</a>
    ·
    <a href="https://github.com/YisusChrist/python-metallum/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

![Alt](https://repobeats.axiom.co/api/embed/e152e604c07d82a966e51ab803e3e442359d61d0.svg "Repobeats analytics image")

<br>

<details>
<summary>Table of Contents</summary>

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [Manual installation](#manual-installation)
  - [Uninstall](#uninstall)
- [Usage](#usage)
  - [Artist search](#artist-search)
  - [Album search](#album-search)
- [Contributors](#contributors)
  - [How do I contribute to python-metallum?](#how-do-i-contribute-to-python-metallum)
- [License](#license)

</details>

## Introduction

This is a versatile yet unofficial python API for the well known [Metal Archives](https://www.metal-archives.com/) website, also known as Encyclopaedia Metallum. It allows you to search for bands, albums and songs to get detailed information about them.

Here is a simple UML diagram of the main model classes used in the project:

![UML diagram](https://www.plantuml.com/plantuml/png/bLDTQnin47pNhr1_W7tGnz87kwMKGbjAOyYZMT-jBoBwEAHLuFBntwDO1C4Hxt9lrjxCUZIZsIM2IDbPzMcAC3hGEU4lJnWT3WO8_q5_3oCcVGQRKAdUGahQ8O6rsMrT6D2cxTwUiZlCKy4zgHSE97t_7gp5dapm4l8_fcofeBG-3WLWRFgY_mQFFEqsmZHXh3nucrHME_9Ble4V2fdxl5xPRtYSB-eg2IqwYJ57qtDk_y5whXiJfbGyRLVjWoVqr0OJZ5XFqaeXemNuXoT3CmEyGOZztKLcl1XNjELtPGAhEiqjDyvOYFj89b7YWC6FrtChWwgjl779fKCibLdcM4wBjpQOr1zzTYUCRHWUC9PbRIx-qI8B8OMlpvlDnxLGSjWCku4K5nIpeGAkggXChj0hhzxQkbfnfQqMt5ehaEGaX0My4ol9rGsU9DHETfYfuug7oTP3dKCWZFedUen0EEZJhBjkcZzFsTckKplqG_dr2W00)

Thanks to [py2puml](https://github.com/lucsorel/py2puml) and [PlantUML](https://github.com/plantuml/plantuml) for the easy generation of the diagram!

## Requirements

Here's a breakdown of the packages needed and their versions:

-   [poetry](https://pypi.org/project/poetry) = 1.7.1 (only for manual installation)
-   [requests](https://pypi.org/project/requests) = 2.31.0
-   [requests-cache](https://pypi.org/project/requests-cache) = 1.1.1
-   [pyquery](https://pypi.org/project/pyquery) = 2.0.0
-   [python-dateutil](https://pypi.org/project/python-dateutil) = 2.8.2
-   [lxml](https://pypi.org/project/lxml) = 5.1.0

> [!NOTE]\
> The software has been developed and tested using Python `3.12.1`. The minimum required version to run the software is Python 3.6. Although the software may work with previous versions, it is not guaranteed.

## Installation

### From PyPI

```bash
pip3 install python-metallum
```

> [!IMPORTANT]\
> For best practices and to avoid potential conflicts with your global Python environment, it is strongly recommended to install this program within a virtual environment. Avoid using the --user option for global installations. We highly recommend using [pipx](https://pypi.org/project/pipx) for a safe and isolated installation experience. Therefore, the appropriate command to install `python-metallum` would be:
>
> ```bash
> pipx install python-metallum
> ```

### Manual installation

If you prefer to install the program manually, follow these steps:

> [!WARNING]\
> This will install the version from the latest commit, not the latest release.

1. Download the latest version of [python-metallum](https://github.com/YisusChrist/python-metallum) from this repository:

    ```bash
    git clone https://github.com/YisusChrist/python-metallum
    cd python-metallum
    ```

2. Install the package:

    ```bash
    poetry install
    ```

### Uninstall

If you installed it from PyPI, you can use the following command:

```bash
pipx uninstall python-metallum
```

## Usage

### Artist search

```python
import metallum

# Search bands matching term
bands = metallum.band_search('metallica')
# -> [<SearchResult: Metallica | Thrash Metal (early), Hard Rock/Heavy/Thrash Metal (later) | United States>]

bands[0].name
# -> 'Metallica'

# Fetch band page
band = bands[0].get()

# Get all albums
band.albums
# -> [<Album: No Life 'til Leather (Demo)>, <Album: Kill 'Em All (Full-length)>, ...]

# Get only full-length albums
full_length = band.albums.search(type=metallum.AlbumTypes.FULL_LENGTH)
# -> [<Album: Kill 'Em All (Full-length)>, <Album: Ride the Lightning (Full-length)>, <Album: Master of Puppets (Full-length)>, <Album: ...and Justice for All (Full-length)>, <Album: Metallica (Full-length)>, <Album: Load (Full-length)>, <Album: ReLoad (Full-length)>, <Album: Garage Inc. (Full-length)>, <Album: St. Anger (Full-length)>, <Album: Death Magnetic (Full-length)>, <Album: Hardwired... to Self-Destruct (Full-length)>]

album = full_length[2]
album.title
# -> 'Master of Puppets'

album.date
# -> datetime.datetime(1986, 3, 3, 0, 0)

# Get all tracks
album.tracks
# -> [<Track: Battery (313)>, <Track: Master of Puppets (516)>, <Track: The Thing That Should Not Be (397)>, <Track: Welcome Home (Sanitarium) (388)>, <Track: Disposable Heroes (497)>, <Track: Leper Messiah (341)>, <Track: Orion (508)>, <Track: Damage, Inc. (330)>]
```

### Album search

```python
import metallum

# Search albums matching term
metallum.album_search('seventh')
# -> []

# Search albums containing term
metallum.album_search('seventh', strict=False)
# -> [<SearchResult: Beherit | Seventh Blasphemy | Demo>, <SearchResult: Black Sabbath | Seventh Star | Full-length>, ...]

# Search albums by band
metallum.album_search('seventh', band='iron maiden', strict=False)
# -> [<SearchResult: Iron Maiden | Seventh Son of a Seventh Son | Full-length>]
```

Refer to source and doctests for detailed usage

## Contributors

<a href="https://github.com/YisusChrist/python-metallum/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=YisusChrist/python-metallum" />
</a>

### How do I contribute to python-metallum?

Before you participate in our delightful community, please read the [code of conduct](.github/CODE_OF_CONDUCT.md).

I'm far from being an expert and suspect there are many ways to improve – if you have ideas on how to make the configuration easier to maintain (and faster), don't hesitate to fork and send pull requests!

We also need people to test out pull requests. So take a look through [the open issues](https://github.com/YisusChrist/python-metallum/issues) and help where you can.

See [Contributing](.github/CONTRIBUTING.md) for more details.

## License

`python-metallum` is released under the [MIT License](https://opensource.org/license/mit).
