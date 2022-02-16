import mne
import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)


def generate_histogram(raw_before, raw_after, trigger_channels):
    events_before = np.empty((0, 3))
    events_after = np.empty((0, 3))
    for trig in trigger_channels:
        event_before = mne.find_events(raw_before, stim_channel=trig)
        event_after = mne.find_events(raw_after, stim_channel=trig)

        channel_id = int(''.join([s for s in trig if s.isdigit()]))

        event_before[:, 2] = channel_id
        events_before = np.append(event_before, events_before, axis=0)

        event_after[:, 2] = channel_id
        events_after = np.append(event_after, events_after, axis=0)

    events_after_sorted = events_after.copy()[events_after[:, 0].argsort()]
    events_before_sorted = events_before.copy()[events_before[:, 0].argsort()]

    reaction_time_before = []
    reaction_time_after = []
    for i, x in enumerate(events_after_sorted):
        if 100 < x[2] < 141:
            reaction_time_after.append(events_after_sorted[i + 1][0] - x[0])

    for i, x in enumerate(events_before_sorted):
        if 100 < x[2] < 141:
            reaction_time_before.append(events_before_sorted[i + 1][0] - x[0])

    plt.hist(reaction_time_before, 25, color='c', alpha=0.5, label='before')
    plt.axvline(sum(reaction_time_before) / len(reaction_time_before), color='c', linestyle='dashed', linewidth=1)
    plt.hist(reaction_time_after, 25, color='b', alpha=0.5, label='after')
    plt.axvline(sum(reaction_time_after) / len(reaction_time_after), color='b', linestyle='dashed', linewidth=1)
    plt.legend(loc='upper right')
    plt.title('GK6- before and after sleep')
    plt.savefig('GK6_sleep', bbox_inches='tight')

    print(1)


raw_before_file = '/Users/rotemfalach/Documents/University/lab/PAT/gk6/GK6_sleep_learning.mff'
raw_before = mne.io.read_raw_egi(raw_before_file)
raw_after_file = '/Users/rotemfalach/Documents/University/lab/PAT/gk6/GK6_sleep_test.mff'
raw_after = mne.io.read_raw_egi(raw_after_file)
D_chans_before = [x for x in raw_before.info.ch_names if x[0] == 'D']
D_chans_after = [x for x in raw_after.info.ch_names if x[0] == 'D']
trigger_channels = list(set(D_chans_before).intersection(D_chans_after))
generate_histogram(raw_before, raw_after, trigger_channels)

# to see the triggers
# raw = mne.io.read_raw_egi('/Users/rotemfalach/Downloads/IN9_MCI_sleep2_20190329_063556.mff')
# trigger_channels = [x for x in raw.info.ch_names if x[0] == 'D']
# channels = raw.pick_channels(trigger_channels)
# mne.viz.plot_raw(channels, duration=290)
# print('finish')
