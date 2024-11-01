
# start of configuration
partition_count = 5  # edit this number wrt. your gpu capabilities
data_upload_name = "20240205"
# set the environment variables AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, S3_ENDPOINT_URL=https://s3.lexis.tech
#dont forget to configure runner-helper.py

#  end of configuration

import subprocess
import os
import time
import datetime

inputList = []
with open("list.txt") as file:
    for line in file:
        inputList.append(line)
    file.close()


total_count = len(inputList)
count_per_partition = total_count // partition_count
partition_list = []

for i in range(partition_count):
    if i == partition_count - 1:
        partition_list.append(inputList[count_per_partition * i:])
    else:
        partition_list.append(inputList[count_per_partition*i:count_per_partition*(i+1)])



result_directory = "./results"
if os.path.exists(result_directory):
    for root, dirs, files in os.walk(result_directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(result_directory)
os.mkdir(result_directory)


"""
internal_directory_deletable = "./internal-directory-deletable"
if os.path.exists(internal_directory_deletable):
    for root, dirs, files in os.walk(internal_directory_deletable, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(internal_directory_deletable)
os.mkdir(internal_directory_deletable)


for i in range(partition_count):
    os.mkdir(internal_directory_deletable+"/"+str(i))
    os.mkdir(internal_directory_deletable + "/" + str(i)+"/"+"download")
    with open(internal_directory_deletable+"/"+str(i)+"/"+"list-within-partition.txt", "w") as file:
        file.writelines(partition_list[i])
        file.close()
"""
for i in range(partition_count):
    p = subprocess.Popen(['conda', 'run', '-n', 's5cmdEnv', 'python', 'runner-helper.py', str(i), data_upload_name])



screen_clear_command = "clear"
if os.name == 'nt':
    screen_clear_command = "cls"

if partition_count > 0:
    start_time = datetime.datetime.now().replace(microsecond=0)
    while p.poll() is None:
        os.system(screen_clear_command)
        runtime = (datetime.datetime.now().replace(microsecond=0) - start_time)
        print(runtime)
        time.sleep(1)
else:
    print("ERR:no partitions exist")