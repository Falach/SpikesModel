import mne
import neo
from neo import AnalogSignal
import numpy as np
from mnelab.io.writers import write_edf
from mff_to_edf import write_edf as rotem_write_edf

for i in range(6):
    number = str(i + 2)
    nsx_filepath = f'C:\\Firas\\D038\\20210722-200746\\20210722-200746-00{number}.ns3'
    nsx_reader = neo.io.BlackrockIO(filename=nsx_filepath)
    bl = nsx_reader.read(lazy=False)[0]
    signal = bl.segments[1].analogsignals[1]
    if i == 0:
        data = signal.transpose().magnitude
    else:
        data = np.concatenate((data, signal.transpose().magnitude), axis=1)

ch_names = signal.name
sfreq = int(signal.sampling_rate.magnitude)
info = mne.create_info(ch_names=ch_names.replace('Channel bundle(', '').split(','), sfreq=sfreq)
mne_raw = mne.io.RawArray(data, info)

rotem_write_edf(mne_raw, 'blackrock_38_1.edf')
# pickle = neo.io.PickleIO(filename)
# pickle.write_block(bl)


# reader = neo.io.BlackrockIO(nsx_filepath)
# block = reader.read(lazy=False)[0]  # get the first block
# segment = block.segments[0]         # get data from first (and only) segment
# signals = segment.analogsignals[0]  # get first (multichannel) signal
#
# data = signals.rescale('V').magnitude.T
# sfreq = signals.sampling_rate.magnitude
# ch_names = [f'Neo {(idx + 1):02}' for idx in range(signals.shape[1])]
# ch_types = ['eeg'] * len(ch_names)  # if not specified, type 'misc' is assumed
#
# info = mne.create_info(ch_names=ch_names, ch_types=ch_types, sfreq=sfreq)
# raw = mne.io.RawArray(data, info)
# # raw.plot(show_scrollbars=False)
# write_edf('D38.edf', raw)

print()