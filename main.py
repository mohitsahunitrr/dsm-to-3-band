import sys
from osgeo import gdal, gdalnumeric as gn
gdal.UseExceptions()

def main():
    """
    Entry function
    """
    if len(sys.argv) != 3:
        print("You should pass two arguments to this script. Abort.")
        sys.exit(1)

    coloring(sys.argv[1], sys.argv[2])

def coloring(input_path, result_path):
    input_tiff = gdal.Open(input_path)
    input_array = input_tiff.ReadAsArray()
    input_band = input_tiff.GetRasterBand(1)
    [input_min, input_max, _, _] = input_band.GetStatistics(True, True)

    output_tiff = create_output_tiff(result_path, input_tiff, input_array)
    fill_output_tiff(input_array, input_min, input_max, output_tiff)
    
def create_output_tiff(result_path, input_tiff, input_array):
    input_gt = input_tiff.GetGeoTransform()
    rows, cols = input_array.shape

    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_tiff = gtiff_driver.Create(result_path, cols, rows, 3, gdal.GDT_Byte)
    output_tiff.SetGeoTransform(input_gt)
    output_tiff.SetProjection(input_tiff.GetProjection())

    return output_tiff

def fill_output_tiff(input_array, input_min, input_max, output_tiff):
    input_percents = (input_array - input_min) * (256 * 256 * 256 / (input_max - input_min))
    input_percents[input_percents < 0] = 0

    red_channel = gn.floor(input_percents / 256 / 256)
    green_channel = gn.floor(gn.mod(input_percents / 256, 256))
    green_channel[red_channel==256] = 255
    blue_channel = gn.floor(gn.mod(input_percents, 256))
    blue_channel[red_channel==256] = 255
    red_channel[red_channel==256] = 255
    output_bands = [output_tiff.GetRasterBand(x + 1) for x in range(3)]
    output_bands[0].WriteArray(red_channel)
    output_bands[1].WriteArray(green_channel)
    output_bands[2].WriteArray(blue_channel)

    for output_band in output_bands:
        output_band.FlushCache()
    
if __name__ == "__main__":
    main()
