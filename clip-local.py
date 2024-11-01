import clip
import torch
from PIL import Image
import json
import os
import sys

arg_list = sys.argv
partition_id = arg_list[1]
data_upload_name = arg_list[2]

workingDirectory = "internal-directory-deletable/"+partition_id+"/download"
filepaths = []
for path, dirnames, filenames in os.walk(workingDirectory):
    if path != workingDirectory:
        for filename in filenames:
            filepath = os.path.join(path, filename)
            filepaths.append(filepath)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Load the CLIP model (ViT-L/14) and the preprocess function
model, preprocess = clip.load("ViT-L/14", device=device)  # Set to "cuda" if using a GPU



# Extract image features




for filepath in filepaths:
    raw_image = Image.open(filepath)
    image = preprocess(raw_image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        features_image = model.encode_image(image)

    pathSaving = filepath[40:]
    
    path_parts = pathSaving.split(os.path.sep)
    name = path_parts[-1]
    saving_directory = path_parts[-2]

    python_representation = {"name": name, "features": features_image.tolist()}
    textual_representation = json.dumps(python_representation)

    if(not os.path.exists(os.path.join("results",saving_directory))):
        os.mkdir(os.path.join("results",saving_directory))

    
    with open(os.path.join("results",saving_directory,"{}.json".format(name)), "w") as outfile:
        outfile.write(textual_representation)
        outfile.close()
    print("{}.json created".format(name))
    