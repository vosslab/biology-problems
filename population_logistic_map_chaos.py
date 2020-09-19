#!/usr/bin/env python

import numpy
from matplotlib import pyplot

#https://en.wikipedia.org/wiki/Logistic_map
#r: 0 to 1 -> die
#r: 1 to 2 -> quick to (r-1)/r
#r: 2 to 3 -> oscillate to (r-1)/r
#r: 3 to 3.449 -> oscillate between 2 values
#r: 3.450 to 3.544 -> oscillate between 4 values
#r: 3.545 to 3.564 -> oscillate between 8 values
#r: 3.570 to 3.999 -> chaos
#r: 4 and up -> diverge

growth_rates = [0.9, 1.3, 2.9, 3.1, 3.8]
labels = ["r = 0.9 (die)", "r = 1.3 (quick)", "r = 2.9 (slow)",
			 "r = 3.1 (bimodal)", "r = 3.8 (chaos)",]
original_population = 0.3
num_generations = 60
population_multiplier = 20000
population_list_list = []

for growth_rate in growth_rates:
	population_list = [original_population, ]
	old_population = original_population
	for generation_number in range(num_generations):
		new_population = growth_rate * old_population * (1.0 - old_population)
		population_list.append(new_population)
		old_population = new_population
	population_list_list.append(population_list)

#make the graph
for i in range(len(population_list_list)):
	population_list = population_list_list[i]
	label = "r = %.3f"%(growth_rates[i])
	nums = numpy.around(population_list, 5)*population_multiplier
	pyplot.plot(list(range(num_generations+1)), nums, label=labels[i])
pyplot.xlabel("Generation Number")
pyplot.ylabel("Population")
pyplot.legend(bbox_to_anchor=(0.65, 0.3), loc=2, borderaxespad=0.)
pyplot.ylim(ymin=0, ymax=20000)
pyplot.xlim(xmin=0, xmax=54)
#pyplot.savefig("outchaos.png", dpi=300)
pyplot.show()
