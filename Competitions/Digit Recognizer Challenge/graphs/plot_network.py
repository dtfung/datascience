# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:25:35 2016

@author: donaldfung
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_arrow(x_from, x_to, y_origin):
    # add input connections
    ax = plt.gca()
    x_origin = x_from
    y_origin = y_origin
    head_width = 0.02
    head_length = 0.02
    arrow_length = x_to - head_length -.1
    angle = 0.0
    ax.arrow(x_origin, y_origin, arrow_length, angle, head_width = head_width, head_length = head_length, fc='k', ec='k', lw = .05)
    
def plot_line(x_to, x_from, y_to, y_from, line_width):
    line = plt.Line2D((x_to, x_from), (y_to, y_from), lw = y_from, c = 'black')
    plt.gca().add_line(line)
    
def plot_network(layers, input_layer_title, hidden_layer_title, output_layer_title,
                 neuron_radius, fill_neuron, line_width, layer_spacing, neuron_spacing):
    
    # initialize network mapping 
    network = [np.zeros(layer) for layer in layers]
    y_mid = 0.5
    
    for i, layer in enumerate(layers):
        mid_value = (layer / 2.0)/10.0
        count = 0.1
        for j in range(0, layer):
            if j == 0:
                network[i][j] = y_mid
            elif j/10.0 <= mid_value and j != 0:
                network[i][j] = y_mid - (j/10.0)
            elif j/10.0 > mid_value and j != 0:
                network[i][j] = y_mid + count
                count += .1
      
    x = layer_spacing         
    for i, layer in enumerate(network):
        if i == 0:
            # draw input arrows
            x_to = x - neuron_radius
            for y in network[0]:
                plot_arrow(x_from = 0.1, x_to = x_to, y_origin = y)

        for y in layer:
            # draw neurons
            circle = plt.Circle((x, y), neuron_radius, fill = fill_neuron)
            plt.gca().add_patch(circle)
            
            # draw connections for every layer except the output
            if i != len(network) - 1:
                for n in network[i + 1]:
                    # distance between layers 
                    dist = 0.2
                    x_to = x + dist - neuron_radius
                    x_from = x + neuron_radius
                    # account for case when y coordinate equals 0
                    if y == 0:
                        y = 0.01
                        plot_line(x_to, x_from, y_to = n, y_from = y, line_width = line_width)
                    plot_line(x_to, x_from, y_to = n, y_from = y, line_width = line_width)
                   
        # create some distance between each layer  
        x += 0.2
    
    for y in network[-1]:
        # draw output arrows
        x_from = len(network) * layer_spacing + neuron_radius
        x_to = .2
        plot_arrow(x_from = x_from, x_to = x_to, y_origin = y)
    plt.axis('off')

    # label layers
    # get y coordinate with highest value from network
    y_max = max([max(i) for i in network])
    plt.text(layer_spacing - .15, .5, 'input', rotation = 90)
    plt.text(x_from + .12, .5, 'output', rotation = 90)
    plt.text(.15, y_max + .06, input_layer_title)
    plt.text(.35, y_max + .06, hidden_layer_title)
    plt.text(.55, y_max + .06, output_layer_title)
    
    # add weight, bias labels
    #plt.text(.28, .43, r'$w_i^j$', rotation = 0, fontsize = 16)
    plt.text(.48, .7, r'$w^l_{jk}$', rotation = 340, fontsize = 16)
    #plt.text(.29, .46, r'$w$', rotation = 0, fontsize = 16)
    #plt.text(.12, .46, r'$w$', rotation = 0, fontsize = 16)
    
    # bias
    plt.text(.39, .69, r'$b^l_j$', rotation = 0, fontsize = 16)
    plt.text(.59, .59, r'$a^l_j$', rotation = 0, fontsize = 16)
    
    
layers = [8, 6, 4]  
plot_network(layers = layers,
             input_layer_title = 'Input Layer',
             hidden_layer_title = 'Hidden Layer',
             output_layer_title = 'Output Layer',
             neuron_radius = .04,
             fill_neuron = False,
             line_width = 1.0,
             layer_spacing = .2,
             neuron_spacing = .1)