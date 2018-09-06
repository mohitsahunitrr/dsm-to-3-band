import sys
from osgeo import gdal, gdalnumeric as gn
gdal.UseExceptions()

def main():
    """
    Entry function
    """
    if len(sys.argv) != 3:
        print_help()
        print("You should pass two arguments to this script. Abort.")
        sys.exit(1)

    dsm_path = sys.argv[1]
    result_path = sys.argv[2]

    dsm = gdal.Open(dsm_path)
    heights = dsm.ReadAsArray()
    height_band = dsm.GetRasterBand(1)
    [min_height, max_height, _, _] = height_band.GetStatistics(True, True)

    result_tiff = make_empty_tiff(result_path, heights.shape, 3, gdal.GDT_Byte)
    set_tiff_info(result_tiff, dsm)
    fill_colors_to_tiff(result_tiff, heights, [min_height, max_height])

def make_empty_tiff(path, original_shape, number_of_band, band_size):
    """
    Make empty tiff with same size
    """
    rows, cols = original_shape
    gtiff_driver = gdal.GetDriverByName('GTiff')
    return gtiff_driver.Create(path, cols, rows, number_of_band, band_size)

def set_tiff_info(tgt_tiff, src_tiff):
    """
    Set geo transform and projection for `tgt_tiff`
    by copying those of `src_tiff`.
    """
    tgt_tiff.SetGeoTransform(src_tiff.GetGeoTransform())
    tgt_tiff.SetProjection(src_tiff.GetProjection())

def fill_colors_to_tiff(tiff, heights, height_range):
    """
    Fill colors into `tiff`.
    Colors comes from `heights` which is converted to ratios.
    For detail of conversion from ratios to colors,
    see `get_rgb_from_24_bits_values`
    """
    max_of_24bit = 256 * 256 * 256 - 1
    bits_range = [0, max_of_24bit]

    # interp automatically removes NODATA values (convert it to 0).
    ratios_in_24bits = gn.floor(gn.interp(heights, height_range, bits_range)).astype(gn.int32)
    red, green, blue = get_rgb_from_24bits_values(ratios_in_24bits)

    data_bands = [tiff.GetRasterBand(x + 1) for x in range(3)]
    data_bands[0].WriteArray(red)
    data_bands[1].WriteArray(green)
    data_bands[2].WriteArray(blue)

    for data_band in data_bands:
        data_band.FlushCache()

def get_rgb_from_24bits_values(values):
    """
    Convert 24bits values into RGBs.
    When you have an array with following value (in binary representation),

    |             value             |
    ---------------------------------
    | 0100_0001_1011_1101_0001_0111 |

    corresponding RGB value will be

    |    red    |   green   |    blue   |
    | 0100_0001 | 1011_1101 | 0001_0111 |

    i.e., red bits are first 8bits,
    green bits are second 8bits,
    and blue bits are final 8bits.

    Using `view` would be faster but that is hard to port.
    """
    blue = gn.bitwise_and(values, 0b11111111)
    values = values >> 8
    green = gn.bitwise_and(values, 0b11111111)
    red = values >> 8

    return red, green, blue

def print_help():
    print("usage: python main.py <input_dsm_path> <output_tiff_path>")
    print("")
    print("  input_dsm_path   : Path of input DSM file. It should have only 1 band.")
    print("                     You can check it by running")
    print("                     'gdalinfo dsm.tif | grep \"^Band \"'")
    print("  output_tiff_path : Path to write result tiff file.")
    print("")

if __name__ == "__main__":
    main()
