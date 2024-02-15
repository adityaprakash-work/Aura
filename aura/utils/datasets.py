# ---INFO-----------------------------------------------------------------------
# Author        Aditya Prakash

# TODO  1. Dataloaders
#       2. Lightning intergration

# ---DEPENDENCIES---------------------------------------------------------------
import mne
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from lightning import LightningDataModule

import os, glob

# ---CONSTANTS------------------------------------------------------------------
STANDARD_EEG_CHANNELS = [
    "Fp1",
    "Fp2",
    "F3",
    "F4",
    "C3",
    "C4",
    "P3",
    "P4",
    "O1",
    "O2",
    "F7",
    "F8",
    "T3",
    "T4",
    "T5",
    "T6",
    "Fz",
    "Cz",
    "Pz",
]


# ---FUNCTIONS------------------------------------------------------------------
def mne_process_0(raw: mne.io.Raw):
    raw = raw.pick(picks=STANDARD_EEG_CHANNELS, exclude="bads")
    raw = raw.set_eeg_reference(
        ref_channels="average",
        projection=False,
        verbose=False,
    )
    return raw


# ---DATA COPY------------------------------------------------------------------
def chunk_data(source_path, dest_path, t=10, mne_process=mne_process_0):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    all_files_paths = glob.glob(source_path + "/*.fif")

    for file_path in all_files_paths:
        raw = mne.io.read_raw_fif(file_path, preload=True)
        raw_len = raw.n_times
        raw_sfr = raw.info["sfreq"]
        samples_per_chunk = int(raw_sfr * t)

        for i in range(raw_len // samples_per_chunk):
            try:
                tmin = int(i * samples_per_chunk / raw_sfr)
                tmax = tmin + t
                raw_temp = raw.copy().crop(tmin=tmin, tmax=tmax)
                if mne_process:
                    raw_temp = mne_process(raw_temp)
                name = os.path.basename(file_path).split(".")[0]
                name = name[:-3] + f"{i}_" + "raw.fif"
                raw_temp.save(os.path.join(dest_path, name))
            except:
                continue


# ---DATASET--------------------------------------------------------------------
class EEGDataset(Dataset):
    def __init__(self, class_paths, transform, start=0, end=5, file_ext="fif"):
        self.class_paths = class_paths
        self.class_paths.sort()
        self.binary = len(self.class_paths) == 2
        self.transform = lambda x: x if transform is None else transform
        self.start = start
        self.end = end
        self.file_ext = file_ext

        self.files = []
        self.labels = []
        for i, class_path in enumerate(self.class_paths):
            self.files += glob.glob(class_path + f"/*.{file_ext}")
            self.labels += [i] * len(self.files)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        if self.file_ext == "fif":
            raw = mne.io.read_raw_fif(self.files[idx], preload=False)
        elif self.file_ext == "edf":
            raw = mne.io.read_raw_edf(self.files[idx], preload=False)
        tmin = self.start
        tmax = self.end
        raw = raw.crop(tmin=tmin, tmax=tmax)
        raw = raw.get_data()
        raw = torch.from_numpy(raw).float()
        raw = self.transform(raw)
        label = self.labels[idx]
        if self.binary:
            label = torch.tensor(label).float()
        else:
            label = torch.nn.functional.one_hot(
                torch.tensor(label), len(self.class_paths)
            ).float()
        return raw, label


# ---LIGHTNING DATA MODULE------------------------------------------------------
class EEGLightningDataModule(LightningDataModule):
    def __init__(
        self,
        train_dataset_config,
        valid_dataset_config,
        batch_size=32,
        num_workers=0,
    ):
        super().__init__()
        self.train_dataset_config = train_dataset_config
        self.valid_dataset_config = valid_dataset_config
        self.batch_size = batch_size
        self.num_workers = num_workers

    def setup(self, stage=None):
        self.train_dataset = EEGDataset(**self.train_dataset_config)
        self.valid_dataset = EEGDataset(**self.valid_dataset_config)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.valid_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
        )


# ---SUBJECT SPECIFIC DATASET---------------------------------------------------
class SSLDataModule(LightningDataModule):
    """
    Subject Specific LightningDataModule
    """
    class _Dataset(torch.utils.data.Dataset):
        def __init__(self, X, Y, n_outputs=2):
            self.X = X
            self.Y = Y
            self.n_outputs = n_outputs

        def __len__(self):
            return len(self.X)

        def __getitem__(self, idx):
            x = torch.tensor(self.X[idx], dtype=torch.float32)
            y = torch.tensor(self.Y[idx], dtype=torch.long)
            y = torch.nn.functional.one_hot(y, num_classes=self.n_outputs)
            return x, y

    def __init__(
        self,
        X, 
        Y,
        S,
        select_classes=None,
        test_size=0.1,
        val_size=0.1,
        batch_size=32,
        num_workers=0,
        pin_memory=False,
        shuffle=True,
    ):
        super().__init__()
        if select_classes is not None:
            idx = np.isin(Y, select_classes)
            self.X = X[idx]
            self.Y = Y[idx]
            self.S = S[idx]
            unique_Y = sorted(np.unique(self.Y))
            for i, y in enumerate(unique_Y):
                self.Y[self.Y == y] = i
            self.n_outputs = len(unique_Y)
        else:
            self.X = X
            self.Y = Y
            self.S = S
            self.n_outputs = len(np.unique(Y))
        self.test_size = test_size
        self.val_size = val_size
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.shuffle = shuffle

    def setup(self, stage=None):
        unique_subjects = np.unique(self.S)
        ns = len(unique_subjects)
        nte = int(self.test_size * ns)
        nva = int(self.val_size * ns)
        np.random.shuffle(unique_subjects)
        tes = unique_subjects[:nte]
        vas = unique_subjects[nte:nte+nva]
        trs = unique_subjects[nte+nva:]
        self.trs = trs
        self.vas = vas
        self.tes = tes

    def train_dataloader(self):
        idx = np.isin(self.S, self.trs)
        X = self.X[idx]
        Y = self.Y[idx]
        return torch.utils.data.DataLoader(
            self._Dataset(X, Y, self.n_outputs),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=self.shuffle,
        )
    
    def val_dataloader(self):
        idx = np.isin(self.S, self.vas)
        X = self.X[idx]
        Y = self.Y[idx]
        return torch.utils.data.DataLoader(
            self._Dataset(X, Y, self.n_outputs),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=False,
        )
    
    def test_dataloader(self):
        idx = np.isin(self.S, self.tes)
        X = self.X[idx]
        Y = self.Y[idx]
        return torch.utils.data.DataLoader(
            self._Dataset(X, Y, self.n_outputs),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=False,
        )
        
        


