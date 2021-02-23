from src import midi2roll as jnn
import os
import numpy as np
from tqdm import tqdm

DATASET_DIR = "data"
RAW_MIDI_DIR = "data/raw_midi"
RAW_MIDI_TEST_DIR = "data/raw_midi_test"
CONVERTED_MIDI_DIR = "data/converted_midi"
DOWNSCALE_FACTOR = 64.0
SILENCE_INTERVAL = 6


def build(test=False):
    src_dir = RAW_MIDI_DIR if not test else RAW_MIDI_TEST_DIR
    data = np.hstack([np.hstack((jnn.midi_to_rollt(os.path.join(src_dir, midi_name), DOWNSCALE_FACTOR)[0],
                                 np.zeros((88, SILENCE_INTERVAL, 3), dtype=bool))) for midi_name in
                      tqdm(os.listdir(src_dir))])
    np.savez_compressed(os.path.join(DATASET_DIR, "data.npz"), data)
    print("Built dataset with %d MIDI files." % len(os.listdir(src_dir)))


def load():
    return np.load(os.path.join(DATASET_DIR, "data.npz"))["arr_0"]


def convert(test=False):
    src_dir = RAW_MIDI_DIR if not test else RAW_MIDI_TEST_DIR
    for midi_name in tqdm([midi_name[0:midi_name.index(".mid")] for midi_name in os.listdir(src_dir)]):
        jnn.make_jamnet_midi("%s/%s.mid" % (src_dir, midi_name),
                             "%s/%s_JN.mid" % (CONVERTED_MIDI_DIR, midi_name), downscale_f=DOWNSCALE_FACTOR)
    print("Converted %d MIDI files to JNN'ized MIDI files." % len(os.listdir(src_dir)))
