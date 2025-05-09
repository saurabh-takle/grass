"""
Created on Tue Apr  2 19:00:15 2013

@author: pietro
"""

from grass.pygrass.gis.region import Region
from grass.pygrass.vector.basic import Bbox


def get_bbox(reg, row, col, width, height, overlap):
    """Return a Bbox

    :param reg: a Region object to split
    :type reg: Region object
    :param row: the number of row
    :type row: int
    :param col: the number of row
    :type col: int
    :param width: the width of tiles
    :type width: int
    :param height: the width of tiles
    :type height: int
    :param overlap: the value of overlap between tiles
    :type overlap: int
    """
    north = reg.north - (row * height - overlap) * reg.nsres
    south = reg.north - ((row + 1) * height + overlap) * reg.nsres
    east = reg.west + ((col + 1) * width + overlap) * reg.ewres
    west = reg.west + (col * width - overlap) * reg.ewres
    return Bbox(
        north=min(north, reg.north),
        south=max(south, reg.south),
        east=min(east, reg.east),
        west=max(west, reg.west),
    )


def get_tile_start_end_row_col(reg, row, col, width, height):
    """Return a tile's starting and ending row and col

    :param reg: a Region object to split
    :type reg: Region object
    :param row: the number of tiles in a row
    :type row: int
    :param col: the number of tiles in a col
    :type col: int
    :param width: the width of tiles
    :type width: int
    :param height: the width of tiles
    :type height: int
    """
    start_row = row * height
    end_row = (row + 1) * height - 1
    start_col = col * width
    end_col = (col + 1) * width - 1
    end_row = reg.rows - 1 if end_row >= reg.rows else end_row
    end_col = reg.cols - 1 if end_col >= reg.cols else end_col
    return (start_row, end_row, start_col, end_col)


def split_region_in_overlapping_tiles(region=None, width=100, height=100, overlap=0):
    """Split a region into a list of overlapping tiles defined as (N, S, E, W).

    :param region: a Region object to split
    :type region: Region object
    :param width: the width of tiles
    :type width: int
    :param height: the width of tiles
    :type height: int
    :param overlap: the value of overlap between tiles
    :type overlap: int

    >>> reg = Region()
    >>> reg.north = 1350
    >>> reg.south = 0
    >>> reg.nsres = 1
    >>> reg.east = 1500
    >>> reg.west = 0
    >>> reg.ewres = 1
    >>> reg.cols
    1500
    >>> reg.rows
    1350
    >>> split_region_in_overlapping_tiles(
    ...     region=reg, width=1000, height=700, overlap=0
    ... )  # doctest: +NORMALIZE_WHITESPACE
    [[Bbox(1350.0, 650.0, 1000.0, 0.0), Bbox(1350.0, 650.0, 1500.0, 1000.0)],
     [Bbox(650.0, 0.0, 1000.0, 0.0), Bbox(650.0, 0.0, 1500.0, 1000.0)]]
    >>> split_region_in_overlapping_tiles(
    ...     region=reg, width=1000, height=700, overlap=10
    ... )  # doctest: +NORMALIZE_WHITESPACE
    [[Bbox(1350.0, 640.0, 1010.0, 0.0), Bbox(1350.0, 640.0, 1500.0, 990.0)],
     [Bbox(660.0, 0.0, 1010.0, 0.0), Bbox(660.0, 0.0, 1500.0, 990.0)]]
    """
    reg = region or Region()
    ncols = (reg.cols + width - 1) // width
    nrows = (reg.rows + height - 1) // height
    box_list = []
    # print reg
    for row in range(nrows):
        row_list = [
            get_bbox(reg, row, col, width, height, overlap) for col in range(ncols)
        ]
        box_list.append(row_list)
    return box_list


def split_region_tiles(region=None, width=100, height=100):
    """Split a region into a list of tiles defined as (start_row, end_row, start_col,
    end_col).

    :param region: a Region object to split
    :type region: Region object
    :param width: the width of tiles
    :type width: int
    :param height: the width of tiles
    :type height: int
    """
    reg = region or Region()
    ncols = (reg.cols + width - 1) // width
    nrows = (reg.rows + height - 1) // height
    box_list = []
    for row in range(nrows):
        row_list = [
            get_tile_start_end_row_col(reg, row, col, width, height)
            for col in range(ncols)
        ]
        box_list.append(row_list)
    return box_list


def get_overlap_region_tiles(region=None, width=100, height=100, overlap=0):
    """Get the Bbox of the overlapped region.

    :param region: a Region object to split
    :type region: Region object
    :param width: the width of tiles
    :type width: int
    :param height: the width of tiles
    :type height: int
    :param overlap: the value of overlap between tiles
    :type overlap: int
    """
    reg = region or Region()
    ncols = (reg.cols + width - 1) // width
    nrows = (reg.rows + height - 1) // height
    box_list = []
    for row in range(nrows):
        row_list = [
            get_bbox(reg, row, col, width, height, -overlap) for col in range(ncols)
        ]
        box_list.append(row_list)
    return box_list
