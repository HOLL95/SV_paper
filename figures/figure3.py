import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter
files=os.listdir('.')
titles=['$E^0$', '$k_0$', '$C_{dl}$','$Ru$']

pos=[0,1,3,2]
true_params=[-0.4, 1e1, 0.000134,20.0]
noise_vals=[0.01, 0.02, 0.005, 0]
fig=plt.figure()
counter=-1
file_1="0.005.cm"
file_2="0.005.lowkf"
experiment=["Sinusoidal","Ramped"]
plt.rcParams.update({'font.size': 15})
chain_select=0
files=[file_2, file_1]
def chain_appender(chains, param):
    new_chain=chains[0, 5000:, param]
    for i in range(1, len(chains)):
        new_chain=np.append(new_chain, chains[i, 5000:, param])
    return new_chain
path=os.getcwd()
paper_location=path[:path.index("figures")]
data_location=paper_location+("/").join(["Inferred_results", "MCMC", "Synthetic"])
for j in range(0, len(files)):
        chains=np.load(data_location+"/"+files[j])
        print(files[j])
        counter+=1
        for i in range(0, len(titles)):
            axes=plt.subplot(2,2,pos[i]+1)
            labels=experiment[j]
            if j==0:
                plot_chain=chain_appender(chains, i)
                if titles[pos[i]]=='$C_{dl}$':
                    axes.hist(plot_chain, alpha=0.4,bins=20,label=str(labels))#edgecolor='black'
                    axes.xaxis.set_major_formatter(FormatStrFormatter('%.4e'))
                else:
                    axes.hist(plot_chain, alpha=0.4,bins=20,label=str(labels))


            else:
                plot_chain=chain_appender(chains, pos[i])
                if titles[pos[i]]=='$C_{dl}$':
                    axes.hist(plot_chain, alpha=0.4,bins=20,label=str(labels))
                    axes.xaxis.set_major_formatter(FormatStrFormatter('%.4e'))
                else:
                    axes.hist(plot_chain, alpha=0.4,bins=20,label=str(labels))
            plt.xticks(rotation=15)
            axes.locator_params(nbins=3)
            axes.set_xlabel(titles[pos[i]])
            axes.set_ylabel('frequency')
            if titles[i]!='$\sigma$':
                axes.axvline(true_params[pos[i]],color="black", linestyle="--")
            axes.legend(loc="upper left")

fig.set_size_inches((6.5, 9))
fig=plt.gcf()
plt.subplots_adjust(left=0.14, bottom=0.12, right=0.97, top=0.98, hspace=0.2, wspace=0.415)
plt.show()
save_path="ramped_comparison.png"
#fig.savefig(save_path, dpi=500)
