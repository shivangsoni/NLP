import matplotlib.pyplot as plt

x = [5000,10000,15000,20000,25000,30000,35000,40000]
y = [0.356680091052355,0.330590089301348,0.307126597793731,0.308177201891087,0.308177201891087,0.308177201891087,0.308177201891087,0.308177201891087]
plt.plot(x,y)

plt.xlabel('x - axis')

plt.ylabel('y - axis')

plt.title('Error rates by word')

plt.show()
