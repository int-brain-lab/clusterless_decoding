import argparse
from pathlib import Path

import h5py
import numpy as np


def load_h5(root_path):
    spike_index = []
    localization_results = []
    root_path = Path(root_path)
    sub_h5 = root_path / "subtraction.h5"
    assert sub_h5.exists()

    with h5py.File(sub_h5, "r") as h5:
        spike_times = h5["spike_index"][:,0] + (h5["start_time"][()] * 30_000)
        spike_channels = h5["spike_index"][:,1]
        spike_index.extend(np.c_[spike_times, spike_channels])
        x = h5["localizations"][:,0]
        z_reg = h5["z_reg"][:]
        maxptp = h5['maxptps'][:]
        localization_results.extend(np.c_[x, z_reg, maxptp]) 
                
    spike_index = np.array(spike_index)
    localization_results = np.array(localization_results)
    
    print("Spike index shape: ", spike_index.shape)
    print("Localization features shape: ", localization_results.shape)
    return spike_index, localization_results


def save_as_numpy(root_path, spike_index, localization_results):
    np.save(Path(root_path) / 'spike_index.npy', spike_index)
    np.save(Path(root_path) / 'localization_results.npy', localization_results)

    
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    
    g = ap.add_argument_group("h5_to_numpy")
    g.add_argument("--root_path")

    args = ap.parse_args()
    
    spike_index, localization_results = load_h5(args.root_path)
    save_as_numpy(args.root_path, spike_index, localization_results)
    
