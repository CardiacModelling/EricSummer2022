import nevis
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

nevis.download_os_terrain_50()

f = nevis.linear_interpolant()
ben_x, ben_y = nevis.ben().grid
def dist_to_ben(x, y):
    return np.linalg.norm(np.array([x, y]) - np.array([ben_x, ben_y]))
x_max, y_max = nevis.dimensions()
np.random.seed(1)

def plot_random_method(points_list=None, function_values=None, distance_values=None):
    """
    Plot random method results.

    Parameters
    ----------
    points_list : list of list of tuple of shape (m, n, 2)
        List of visited points to be plotted. m is the number of executions,
        and n is the nubmer of evaluations per execution. If None, ``function_values``
        and ``distance_values`` must be provided.
    function_values : list of list of float
        List of function values to be plotted. If None, they are obtained using
        ``points_list`` by evaluating the function at each point.
    distance_values : list of list of float
        List of distance values to be plotted. If None, they are obtained using
        ``points_list`` by calculating the distance to the Ben Nevis at each point.
    
    Returns
    -------
    fig, (ax1, ax2) : tuple of matplotlib.pyplot.Figure and (ax1, ax2)
    """

    if points_list is None:
        assert function_values is not None and distance_values is not None, \
            "Either points_list or (function_values and distance_values) must be provided."

    def calc(values_list, method):
        random_results = []
        for values in values_list:
            prefix = (np.maximum if method == 'max' else np.minimum).accumulate(values)
            random_results.append(prefix)
        
        temp = np.array(random_results).T

        re_mean = []
        re_0 = []
        re_25 = []
        re_75 = []
        re_100 = []
        for x in temp:
            re_mean.append(np.mean(x))
            sorted_x = np.sort(x)
            re_0.append(sorted_x[0])
            re_25.append(sorted_x[int(len(sorted_x) * 0.25)])
            re_75.append(sorted_x[int(len(sorted_x) * 0.75)])
            re_100.append(sorted_x[-1])

        return re_mean, re_0, re_25, re_75, re_100
    
    # Function values
    if function_values is None:
        print('Calculating function values...')
        function_values = []
        for points in points_list:
            function_values.append([f(x, y) for x, y in points])
    
    print(f'Length of function_values: {len(function_values)}')
    re_mean, re_0, re_25, re_75, re_100 = calc(function_values, 'max')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    fig.suptitle('Performance of grid search')

    ax1.set_xscale('log') # log scale for x axis
    ax1.plot(re_mean, label='mean')
    ax1.plot(re_0, label='0%')
    ax1.plot(re_25, label='25%')
    ax1.plot(re_75, label='75%')
    ax1.plot(re_100, label='100%')
    ax1.axhline(y=1344.9, color='r', linestyle='--', label='Ben Nevis')
    ax1.fill_between(range(len(re_mean)), re_25, re_75, color='#5CA4FA', alpha=0.5)
    ax1.fill_between(range(len(re_mean)), re_0, re_100, color='#5CF7FA', alpha=0.25)
    ax1.legend(loc='lower right')
    ax1.set_xlabel('Number of evaluations')
    ax1.set_ylabel('Height')
    

    # Distances to Ben Nevis
    if distance_values is None:
        print('Calculating distances to Ben Nevis...')
        distance_values = []
        for points in points_list:
            distance_values.append([dist_to_ben(x, y) for x, y in points])
    
    print(f'Length of distance_values: {len(distance_values)}')
    re_mean, re_0, re_25, re_75, re_100 = calc(distance_values, 'min')

    ax2.set_xscale('log') # log scale for x axis
    ax2.set_yscale('log') # log scale for y axis
    ax2.plot(re_mean, label='mean')
    ax2.plot(re_0, label='100%')
    ax2.plot(re_25, label='75%')
    ax2.plot(re_75, label='25%')
    ax2.plot(re_100, label='0%')
    ax2.fill_between(range(len(re_mean)), re_25, re_75, color='#5CA4FA', alpha=0.5)
    ax2.fill_between(range(len(re_mean)), re_0, re_100, color='#5CF7FA', alpha=0.25)
    ax2.legend(loc='upper right')
    ax2.set_xlabel('Number of evaluations')
    ax2.set_ylabel('Distance to Ben Nevis')
    ax2.set_ylim(10, 2e6)
    

    return fig, (ax1, ax2)


def read_results(prefix):
    """Read results from all pickle files with prefix ``prefix``."""   
    points_list = []
    function_values = []
    distance_values = []
    for file in os.listdir('result/'):
        if file.startswith(prefix) and file.endswith('.pickle'):
            print('Reading {}...'.format(file))

            data  = pickle.load(open('result/' + file, 'rb'))
            points_list.extend(data.get('points', []))
            function_values.extend(data.get('function_values', []))
            distance_values.extend(data.get('distance_values', []))
        
    return points_list, function_values, distance_values
    
if __name__ == '__main__':
    SIDE = 2000
    points_list, function_values, distance_values = read_results(f'grid_search_{SIDE}_')
    t = nevis.Timer()
    plot_random_method(points_list, function_values, distance_values)
    print(t.format())
    plt.show()