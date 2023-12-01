from utils import read_poca_files
from preprocessing import pre_process_off_frame_csv, pre_process_on_frame_csv, pre_process_sigma, pre_process_single_intensity, get_num_fov_idx_results_dir
def calculate_duty_cycle(total_ON, lifetime):
    return total_ON/lifetime

def calculate_lifetime(num_blink, lifetime):
    return num_blink/lifetime

