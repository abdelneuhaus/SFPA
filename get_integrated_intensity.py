from utils import read_locPALMTracer_file, get_PALMTracer_files

exp = 'stack.PT'
file_paths = get_PALMTracer_files(exp)

mean = []
for i in file_paths:
    file = read_locPALMTracer_file(i)
    int_int = file['Integrated_Intensity']
    mean.append(int_int.mean())
mean.sort()
