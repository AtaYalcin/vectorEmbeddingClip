#configuration region
extractionSuffixes = [
    "_CAM_NFV_FW_CE_NO_ENC.npz.zip",
    "_CAM_SUR_FR_CE_NO_ENC.npz.zip",
    "_CAM_SUR_RE_CE_SO_ENC.npz.zip",
    "_CAM_SUR_WM_LE_WE_ENC.npz.zip",
    "_CAM_SUR_WM_RI_EA_ENC.npz.zip",
    "_CAM_WFV_FW_CE_NO_ENC.npz.zip",
    "_CAM_WFV_RW_CE_SO_ENC.npz.zip"
]

#dont forget to configure runner.py

#end of configuration

import os
import sys

arg_list = sys.argv
partition_id = arg_list[1]
data_upload_name = arg_list[2]

path_prefix = "internal-directory-deletable/"+partition_id+"/"

list = []
with open(path_prefix+"list-within-partition.txt") as file:
    for line in file.readlines():
        list.append(line.replace("\n",""))
    file.close()

download_command_template = "s5cmd cp s3://exa4mind/"+data_upload_name+"/"


data_path = path_prefix+"download"
for record in list:
    download_command = download_command_template+record+" "+data_path+"/."
    os.system(download_command)

    os.chdir(data_path)

    os.system("unzip {}".format(record))
    for suffix in extractionSuffixes:
        os.system(
            "unzip {} -d {} ".format(
                                        record.replace(".zip","")+suffix,
                                        record.replace(".zip","")+suffix.replace(".zip","")
                                    )
        )




    os.chdir("./../../../")

    os.system("conda run -n clip python clip-local.py "+partition_id+" "+data_upload_name)


    
    for root, dirs, files in os.walk(data_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    

exit()

