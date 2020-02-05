import getopt
import sys

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    folder = "Q-Study"
    file_input = "BMS1-10-8-7-7-471-input.txt"
    file_output = "BMS1-10-8-7-7-471-divergence.txt"
    file_time = "BMS1-10-8-7-7-471-time.txt"
    file_exit = "BMS1-10-8-7-7-471-exit.txt"

    # controllo gli eventuali argomenti di command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:i:d:e:t:", ["file=", "input=", "divergence=", "exit=", "time="])
    except getopt.GetoptError:
        print('Main_Plot_Qvalues_Analysis.py \n' +
              ' -f <path della cartella>\n' +
              ' -i <nome file di input>\n' +
              ' -d <nome file con risultati di diverenza>\n' +
              " -e <nome file con risultati sull'esito>\n" +
              ' -t <nome file con risultati sul tempo>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Main_Plot_Qvalues_Analysis.py \n' +
                  ' -f <path della cartella>\n' +
                  ' -i <nome file di input>\n' +
                  ' -d <nome file con risultati di diverenza>\n' +
                  " -e <nome file con risultati sull'esito>\n" +
                  ' -t <nome file con risultati sul tempo>')
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder = arg
        elif opt in ("-i", "--input"):
            file_input = arg
        elif opt in ("-d", "--divergence"):
            file_output = arg
        elif opt in ("-e", "--exit"):
            file_exit = arg
        elif opt in ("-t", "--time"):
            file_time = arg

    file_read = open(folder +"/"+ file_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    file_read = open(folder +"/"+ file_output, "r")
    output_data = file_read.read().split(";")
    file_read.close()

    file_read = open(folder +"/"+ file_time, "r")
    output_time = file_read.read().split(";")
    file_read.close()

    file_read = open(folder +"/"+ file_exit, "r")
    output_exit = file_read.read().split(";")
    file_read.close()

    t = [0]*(len(output_time)-1)
    e = [0]*(len(output_exit)-1)
    d = [0]*(len(output_data)-1)
    x = [0]*(len(input_data)-1)
    y = [0]*(len(input_data)-1)

    for it in range(len(input_data)-1):
        itt = input_data[it].split(",")
        x[it] = float(itt[0])
        y[it] = float(itt[1])
    for it in range(len(output_data) - 1):
        d[it] = float(output_data[it])
    for it in range(len(output_time) - 1):
        t[it] = float(output_time[it])
    for it in range(len(output_exit) - 1):
        e[it] = int(output_exit[it])

    y_max = max(y)
    y_min = min(y)

    y_max += 0.02 * (y_max - y_min)
    y_min -= 0.02 * (y_max - y_min)

    x = np.array(x)
    y = np.array(y)
    t = np.array(t)
    d = np.array(d)
    e = np.array(e)

    cmap = plt.plasma()

    f, ax = plt.subplots()
    ax.set_title("KL-Divergence (%s)" % len(d))
    ax.set_ylabel('density')
    ax.set_xlabel('q_value')
    points = ax.scatter(x, y, c=d, s=10, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()

    x1 = x.copy()
    y1 = y.copy()
    d1 = d.copy()
    standard_deviation = np.std(d1)
    print("KL-Divergence: ")
    while 1:
        m_std = min(d1)
        M_std = max(d1)
        x1_t = list()
        y1_t = list()
        d_t = list()
        x1_m = None
        y1_m = None
        x1_M = None
        y1_M = None
        for index in range(len(d1)):
            if d1[index] == m_std and x1_m is None:
                x1_m = x1[index]
                y1_m = y1[index]
            elif d1[index] == M_std and x1_M is None:
                x1_M = x1[index]
                y1_M = y1[index]
            else:
                d_t.append(d1[index])
                x1_t.append(x1[index])
                y1_t.append(y1[index])
        standard_deviation_t = np.std(d_t)
        diff = standard_deviation - standard_deviation_t
        if diff > 0.0005:
            print("Removing %s and %s the standard deviation is decreased from %s to %s" % (
            M_std, m_std, standard_deviation, standard_deviation_t))
            x1 = x1_t
            y1 = y1_t
            d1 = d_t
            standard_deviation = standard_deviation_t
        else:
            break

    if len(x) > len(x1):
        f, ax = plt.subplots()
        ax.set_title("KL-Divergence (%s)" % len(d1))
        ax.set_ylabel('density')
        ax.set_xlabel('q_value')
        points = ax.scatter(x1, y1, c=d1, s=10, cmap=cmap)
        f.colorbar(points)
        plt.ylim((y_min, y_max))
        plt.show()

    print("")
    cmap = plt.winter()

    avg_0 = np.average(d)
    d_l = list()
    d_u = list()
    x_l = list()
    x_u = list()
    y_l = list()
    y_u = list()
    for index in range(len(d)):
        if d[index] < avg_0:
            x_l.append(x[index])
            y_l.append(y[index])
            d_l.append(d[index])
        elif d[index] > avg_0:
            x_u.append(x[index])
            y_u.append(y[index])
            d_u.append(d[index])

    avg_1 = np.average(d_l)
    d_l_l = list()
    x_l_l = list()
    y_l_l = list()
    for index in range(len(d_l)):
        if d_l[index] < avg_1:
            x_l_l.append(x_l[index])
            y_l_l.append(y_l[index])
            d_l_l.append(d_l[index])
    avg_2 = np.average(d_l_l)
    d_l = list()
    x_l = list()
    y_l = list()
    for index in range(len(d_l_l)):
        if d_l_l[index] < avg_2:
            x_l.append(x_l_l[index])
            y_l.append(y_l_l[index])
            d_l.append(d_l_l[index])
    avg_1 = np.average(d_l)
    d_l_l = list()
    x_l_l = list()
    y_l_l = list()
    for index in range(len(d_l)):
        if d_l[index] < avg_1:
            x_l_l.append(x_l[index])
            y_l_l.append(y_l[index])
            d_l_l.append(d_l[index])

    f, ax = plt.subplots()
    ax.set_title("min - KL-Divergence (%s)" % len(d_l_l))
    ax.set_ylabel('density')
    ax.set_xlabel('q_value')
    points = ax.scatter(x_l_l, y_l_l, c=d_l_l, s=50, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()

    cmap = plt.autumn()

    avg_1 = np.average(d_u)
    d_u_u = list()
    x_u_u = list()
    y_u_u = list()
    for index in range(len(d_u)):
        if d_u[index] > avg_1:
            x_u_u.append(x_u[index])
            y_u_u.append(y_u[index])
            d_u_u.append(d_u[index])
    avg_2 = np.average(d_u_u)
    d_u = list()
    x_u = list()
    y_u = list()
    for index in range(len(d_u_u)):
        if d_u_u[index] > avg_2:
            x_u.append(x_u_u[index])
            y_u.append(y_u_u[index])
            d_u.append(d_u_u[index])

    f, ax = plt.subplots()
    ax.set_title("Max - KL-Divergence (%s)" % len(d_u))
    ax.set_ylabel('density')
    ax.set_xlabel('q_value')
    points = ax.scatter(x_u, y_u, c=d_u, s=50, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()

    cmap = plt.plasma()

    f, ax = plt.subplots()
    ax.set_title("Time (%s)" % len(t))
    ax.set_ylabel('density')
    ax.set_xlabel('q_value')
    points = ax.scatter(x, y, c=t, s=10, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()

    x1 = x.copy()
    y1 = y.copy()
    standard_deviation = np.std(t)
    print("Time")
    while 1:
        m_std = min(t)
        M_std = max(t)
        x1_t = list()
        x1_removed_m = list()
        x1_removed_M = list()
        y1_t = list()
        y1_removed_m = list()
        y1_removed_M = list()
        d_t = list()
        for index in range(len(t)):
            if t[index] == m_std:
                x1_removed_m.append(x1[index])
                y1_removed_m.append(y1[index])
            elif t[index] == M_std:
                x1_removed_M.append(x1[index])
                y1_removed_M.append(y1[index])
            else:
                d_t.append(t[index])
                x1_t.append(x1[index])
                y1_t.append(y1[index])
        standard_deviation_t = np.std(d_t)
        diff = standard_deviation - standard_deviation_t
        if diff > 0.39:
            print("Removing %s and %s the standard deviation is decreased from %s to %s" % (
            M_std, m_std, standard_deviation, standard_deviation_t))
            x1 = x1_t
            y1 = y1_t
            t = d_t
            standard_deviation = standard_deviation_t
        else:
            break

    if len(x) > len(x1):
        f, ax = plt.subplots()
        ax.set_title("Time (%s)" % len(t))
        ax.set_ylabel('density')
        ax.set_xlabel('q_value')
        points = ax.scatter(x1, y1, c=t, s=10, cmap=cmap)
        f.colorbar(points)
        plt.ylim((y_min, y_max))
        plt.show()

    x1 = list()
    x2 = list()
    x3 = list()
    y1 = list()
    y2 = list()
    y3 = list()
    z3 = list()
    for tr in range(len(e)):
        if e[tr] == 1:
            x1.append(x[tr])
            y1.append(y[tr])
        elif e[tr] == -1:
            x2.append(x[tr])
            y2.append(y[tr])
        else:
            x3.append(x[tr])
            y3.append(y[tr])
            z3.append(e[tr])

    f, ax = plt.subplots()
    points = ax.scatter(x3, y3, c=z3, s=10, cmap=cmap)
    plt.xlabel("q_value")
    plt.ylabel("density")
    plt.title("Results (%s)" % len(z3))
    f.colorbar(points)
    plt.show()
