from utils import read_locPALMTracer_file, get_PALMTracer_files
import matplotlib.pyplot as plt
import numpy as np 

exp = '230126_stablefp'
file_paths = get_PALMTracer_files(exp)

mean = []
for i in file_paths:
        print(i)
        file = read_locPALMTracer_file(i)
        mean.append(file['Integrated_Intensity'])

fig, ax1 = plt.subplots()
h = list(range(0,len(mean)))
ax1.boxplot(mean, widths=0.5, positions=h, showmeans=False, manage_ticks=False, showfliers=False)
plt.show()
#     file = read_locPALMTracer_file(i)
#     int_int = file['Integrated_Intensity']
#     mean.append(int_int.mean())
# mean.sort()

# ax = data[['Box1', 'Box2']].plot(kind='box', title='boxplot')
