import matplotlib.pyplot as plt
import pickle
import glob

filenames = glob.glob("*.p")
for filename in filenames:
    results = pickle.load(open(filename, "rb"))

    plt.plot(results['magnitude'], results['efficiency'], label=filename.split('.')[0])
#    plt.savefig('efficiency plots.png')

plt.title('Efficiency vs. Magnitude')
plt.ylabel('Efficiency of Cut Collection')
plt.xlabel('Magnitude of Fake Signal')

plt.legend(loc='lower right')
plt.savefig('efficiency plots.png')
