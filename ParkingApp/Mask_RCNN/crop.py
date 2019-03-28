from PIL import Image

def cropImage(path, coords):
    if len(coords) != 4:
        raise Exception('coordinates should be in sets of 4.  The value was: {}'.format(len(coords)))

    coords = [int(i) for i in coords]
    pathToCropped = 'Videos/crop.jpg'
    imageObj = Image.open(path)
    #imageObj = Image.open('Videos/Parking1Copy.jpg')
    cropped = imageObj.crop(coords)
    cropped.save(pathToCropped)
    return pathToCropped
