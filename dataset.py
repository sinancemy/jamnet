import jnntools as jnn
import os
import csv
import ast
from tqdm import tqdm

DATASET_DIR = "data"
RAW_MIDI_DIR = "data/raw_midi"
RAW_MIDI_TEST_DIR = "data/raw_midi_test"
CONVERTED_MIDI_DIR = "data/converted_midi"


def build(test=False):
    src_dir = RAW_MIDI_DIR if not test else RAW_MIDI_TEST_DIR
    with open("%s/data.csv" % DATASET_DIR, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=jnn.JNN_PIECE_PARTS)
        writer.writeheader()
        for jnn_piece in [jnn.midi_to_jnn("%s/%s" % (src_dir, midi_name)) for midi_name in
                          tqdm(os.listdir(src_dir))]:
            writer.writerow(jnn_piece)
    print("Built dataset with %d MIDI files." % len(os.listdir(src_dir)))


def load():
    jnn_pieces = list()
    with open("%s/data.csv" % DATASET_DIR, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        num_notes = 0
        for row in reader:
            row = {i: ast.literal_eval(row[i]) for i in row}
            jnn_pieces.append(row)
            num_notes += sum([len(row[i]) for i in row if isinstance(row[i], list)])
    print("Loaded dataset with %d JNN pieces with a total of %d JNN notes." % (len(jnn_pieces), num_notes))
    return jnn_pieces


def convert(test=False):
    src_dir = RAW_MIDI_DIR if not test else RAW_MIDI_TEST_DIR
    for midi_name in tqdm([midi_name[0:midi_name.index(".mid")] for midi_name in os.listdir(src_dir)]):
        jnn.jnnize_midi("%s/%s.mid" % (src_dir, midi_name),
                                "%s/%s_JNN.mid" % (CONVERTED_MIDI_DIR, midi_name))
    print("Converted %d MIDI files to JNN-ized MIDI files." % len(os.listdir(src_dir)))
