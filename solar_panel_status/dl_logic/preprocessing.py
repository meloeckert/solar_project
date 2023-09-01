from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.image import resize
from PIL import Image

def preprocess(image):

    img = img_to_array(Image.open(image))
    img = resize(img, (225, 225)).numpy()
    img = img.reshape((-1, 225, 225, 3))
    return img



def preprocess_tiles(images : dict, num_tiles=3):
    """
    Predict presence of damage and damage class based on image
    """
    filenames=list(images.keys())
    tile_arrays=[]
    tensors=[]
    invalid={}

    for f in filenames:

        img = images.get(f'{f}')
        img = Image.open(BytesIO(img))

        try:

            #image tiling, array conversion; append to 'image_tiles' list
            image_tiles = []
            img_675_array = np.array(img.resize((675,675)))

            #vertical slice; num_tiles = # of equal divisions
            for v in range(0,img_675_array.shape[0],img_675_array.shape[0]//num_tiles):
                #horizontal slice; num_tiles = # of equal divisions
                for h in range(0,img_675_array.shape[1],img_675_array.shape[1]//num_tiles):
                    tile_array = img_675_array[v:v+(img_675_array.shape[0]//num_tiles), h:h+(img_675_array.shape[1]//num_tiles),:]
                    image_tiles.append(tile_array)

            tile_arrays.append(image_tiles)

            #resize full image and convert to array; append to 'tensors' list
            img_255_array = np.array(img.resize((225,225)))
            tensor = img_255_array.reshape((-1, 225, 225, 3))
            tensors.append(tensor)

        except Exception as e:
            if f.lower().endswith("ds._store"):
                continue
            else:
                print("Error processing: ", f)
                print("Error: ", e)
                invalid[f]= e
                continue

    preprocessed_X = {"filenames":filenames,
                     "tensors":tensors,
                     "tile_arrays":tile_arrays,
                      "invalid":invalid
                     }

    return preprocessed_X
