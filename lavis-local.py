

from lavis.models import load_model_and_preprocess
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
model, vis_processors, _ = load_model_and_preprocess(name="blip_feature_extractor", model_type="base", is_eval=True, device=device)



for filepath in filepaths:
    raw_image = Image.open(filepath).convert("RGB")
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    sample = {"image": image}
    features_image = model.extract_features(sample, mode="image").image_embeds_proj[:,0,:]
    pathSaving = filepath[40:]
    name = pathSaving.split("\\")[-1]
    python_representation = {"name": name, "features": features_image.tolist()}
    textual_representation = json.dumps(python_representation)
    with open("results/"+name+".json", "w") as outfile:
        outfile.write(textual_representation)
        outfile.close()