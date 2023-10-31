import pandas as pd
import numpy as np
import json
import os
import re
import sys

# Accept filename and output directory as command-line arguments
if len(sys.argv) != 3:
    print("Usage: python create_dataframe.py <filename.json> <output_dir>")
    sys.exit(1)

filename = sys.argv[1]
output_dir = sys.argv[2]

# Read in the JSON file and store its 'transcription' item (list of dicts) in a list
transcripts = {}

with open(filename) as f:
    data = json.load(f)
    transcripts[os.path.basename(filename)] = data['transcription']

# Convert to df with multi-index:
# Filename -> Timestamp -> [from_sec, fo_sec, from_offset, to_offset, text]
data = []
for filename, transcript_list in transcripts.items():
    for transcript in transcript_list:
        timestamps = transcript['timestamps']
        offsets = transcript['offsets']
        text = transcript['text']
        data.append({
            'filename': filename,
            'from_time': timestamps['from'],
            'to_time': timestamps['to'],
            'from_offset': offsets['from'],
            'to_offset': offsets['to'],
            'text': text
        })

df = pd.DataFrame(data)
pattern = "^([0-9]{6})_([0-9]{4})(-.+)?\..+$"
df['date'] = df['filename'].apply(lambda x: re.match(pattern, x).group(1) if re.match(pattern, x) else None)
df['time'] = df['filename'].apply(lambda x: re.match(pattern, x).group(2) if re.match(pattern, x) else None)
df['title'] = df['filename'].apply(lambda x: re.match(pattern, x).group(3)[1:] if re.match(pattern, x) and re.match(pattern, x).group(3) else None)
df['datetime'] = pd.to_datetime(df['date'] + df['time'], format='%y%m%d%H%M')
df.drop(['date', 'time'], axis=1, inplace=True)

def time_str_to_seconds(time_str):
    h, m, s = map(float, time_str.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s

df['from_time'] = df['from_time'].apply(time_str_to_seconds)
df['to_time'] = df['to_time'].apply(time_str_to_seconds)
df['from_time'] = df['datetime'] + pd.to_timedelta(df['from_time'], unit='s')
df['to_time'] = df['datetime'] + pd.to_timedelta(df['to_time'], unit='s')

# Save the DataFrame to a CSV file in the provided directory
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.splitext(os.path.splitext(os.path.basename(filename))[0])[0] + ".csv"
df.to_csv(os.path.join(output_dir, output_filename), index=False)