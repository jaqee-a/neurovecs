import matplotlib.pyplot as plt


users = [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
number = [4, 4, 5, 5, 5, 6, 7, 7, 7, 8, 8]
coverage = [99, 95, 97, 93, 83, 90, 95, 87, 80, 85, 80]
data = [14, 11, 12, 10, 9, 10, 11, 11, 10, 10, 10]

fig, axs = plt.subplots(3)

axs[0].plot(users, number)
axs[1].plot(users, coverage)
axs[2].plot(users, data)


axs[0].set(xlabel='Users number', ylabel='UAVs number')
axs[1].set(xlabel='Users number', ylabel='users coverage (%)')
axs[2].set(xlabel='Users number', ylabel='Date rate (Mbps)')


plt.show()