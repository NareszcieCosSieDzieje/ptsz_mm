from glob import glob
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(['science', 'ieee', 'high-vis'])

oo = 6666666

EXCEL = [
    132203,
    132325,
    136558,
    136674,
    136698,
    136704,
    136748,
    136751,
    136760,
    136800,
    136809,
    142192,
]

colormap = {
    136558: "#8936df",  # ok
    136674: "#fec32d",  # ok
    136698: "#e6091c",  # ok
    136704: "#26eb47",  # ok
    136760: "#25d7fd",  # ok
    136809: "#000000",  # ok
    142192: "#0d49fb",  # ok
}

RANGE = list(range(50, 500+50, 50))


def read_file(path):
    vec = open(path, 'r').read().split("\n")
    return list(map(float, filter(None, vec)))


def get_data(path):
    data = []
    vec = read_file(path)
    for i in range(len(EXCEL)*len(RANGE)):
        data.append(vec[i])
    return data


data_all = []
for i in range(len(EXCEL)*len(RANGE)):
    data_all.append([])

for path in glob("score_*.txt"):
    print(f"path --> {path}")
    idx = int(path.replace("score_", "").replace(".txt", ""))
    data = get_data(path)
    for i in range(len(data)):
        data_all[i].append(data[i])

val_min, val_max = +oo, -oo
for path in glob("score_*.txt"):
    print(f"path --> {path}")
    idx = int(path.replace("score_", "").replace(".txt", ""))
    data = get_data(path)
    for i in range(len(data)):
        data[i] = np.min(data_all[i]) / data[i]
    data = sorted(data)
    val_min = min(val_min, min(data))
    val_max = max(val_max, max(data))

    color = "#000000"  # FIXME: score color?
    if idx in colormap:
        color = colormap[idx]

    plt.plot(range(len(data)), data, label=idx, c=color)
    # plt.scatter(range(len(data)), data, label=idx, c=color, s=1)

plt.plot(range(len(data)), [1]*len(data), c="gray",
         linestyle="-", linewidth=10, alpha=0.2)

ax = plt.gca()
ax.autoscale(tight=True)
fig = plt.gcf()
fig.set_size_inches(8, 2.5)

plt.ylabel('score ratio (best/out)')
plt.legend(loc="lower center", bbox_to_anchor=(0.5, 1),  ncol=7)
plt.xlabel('cases (sorted by score)')

ax.set_ylim([0.95, val_max])
plt.savefig('score.jpg')
