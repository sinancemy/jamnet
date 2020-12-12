from src import model as model_, dataset as dataset_

REBUILD_DATASET, CONVERT_DATASET = True, True

if REBUILD_DATASET:
    dataset_.build()
if CONVERT_DATASET:
    dataset_.convert()
data = dataset_.load()

model = model_.JamNet()
