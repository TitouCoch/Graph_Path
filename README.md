
---
"Graph Path"
---


## Apply multiple algorithms on graphs


### Grap  :
The graph is composed of the 465 bus stop GPS coordinates of the BAB (Biaritz, Anglet, Bayonne) region in France

#### Development

I have developed a graph traversal application using Python and the libraries Tkinter and Graphics. The application applies various well-known algorithms such as A*, Dijkstra, Floyd-Warshall, and Bellman-Ford on a bus stop map. The application features a menu and a graphical map where the results can be observed.

### Algorithms :

| Algorithme        | Temps d'exécution (second) |
| ---------------- | --------------------- |
| Floyd Warshall    | 9.99                  |
| Bellman           | 1.036                 |
| Dijkstra          | 1.374                 |
| Dijkstra(priority queue)| 0.956                 |
| A*                | 0.013                 |


```python
  import time
  start_time = time.time()
  #algorithms code
  print("--- %s seconds ---" % (time.time() - start_time))
```


This time test was done with the time library for a distance of 11,500 meters that we recover thanks to the GPS coordinate.

Note that the A* algorithm outperforms, it is particularly with the priority list and a heuristic function that checks that we do not deviate from the coordinates of the arrival point.

### Final Application :

I realized a small menu to facilitate the choice of the user, he can choose the bus stops with a drop-down list or directly on the map, he can also choose the algorithm and acceleration 

<img width="248" alt="Screenshot 2022-09-20 at 12 24 58 PM" src="https://user-images.githubusercontent.com/91782454/191234777-aaecb279-0312-474a-8460-0fee9fb37cba.png">

<br/>

<p style="font-size: 24px;
  font-weight: bold;
  text-align: center;
  color:
  margin-bottom: 20px;">Here is the Result</p>


<img width="896" alt="Screenshot 2022-09-20 at 12 26 31 PM" src="https://user-images.githubusercontent.com/91782454/191234832-457eac7c-1c30-4277-801f-5e286db421b7.png">

