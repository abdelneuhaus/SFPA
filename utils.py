import os
import pandas as pd


def read_locPALMTracer_file(file):
    return pd.read_csv(file, sep='\t', skiprows=2)

def read_poca_files(file):
    df = pd.read_csv(file)
    df.loc[df['# seq OFF'] > 300000, '# seq OFF'] = df['blinks']
    return df.iloc[:,:-1]

def get_poca_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('cleaned.txt')]
    return [x.replace("\\", "/") for x in a]

def get_csv_poca_intensity_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('intensity.csv')]
    return [x.replace("\\", "/") for x in a]

def get_csv_poca_sigma_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('sigmaXY.csv')]
    return [x.replace("\\", "/") for x in a]

def read_csv_poca(file):
    return pd.read_csv(file).values.tolist()

def get_csv_poca_frame_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('frame.csv')]
    return [x.replace("\\", "/") for x in a]

def get_PALMTracer_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('locPALMTracer.txt')]
    return [x.replace("\\", "/") for x in a]

def get_trcPALMTracer_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('trcPALMTracer.txt')]
    return [x.replace("\\", "/") for x in a]

def read_cluster_from_PoCA(file):
    df = pd.read_csv(file)
    return df[df.columns[:-1]]['frame'].tolist()