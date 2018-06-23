import os

dir_name = "training_data/faces/stressed"
test = os.listdir(dir_name)

for item in test:
    if not (item.endswith(".jpeg") or item.endswith(".jpg") or item.endswith(".png") or item.endswith(".gif")):
        os.remove(os.path.join(dir_name, item))