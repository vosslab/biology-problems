#!/usr/bin/env python

import os
import re
import sys
import yaml
import random
import multidisorderlib

#sample question:
#  A man (&male;) with both hemophilia and Huntington's disease marries
#    a normal phenotype woman (&female;) without either disease.
#  The man's (&male;) father also had Huntington's disease, but not his mother.
#  The woman's (&female;) father suffered from hemophilia, but her mother did not.
#  Huntington's disease is autosomal dominant, and hemophilia is X-linked recessive.

# step 1: pick a dominant disease
# step 2: pick a X-linked disease; mother is a carrier

#easy, ask the genotype of one of the individuals
#hard, ask a compounded question: What fraction of their sons (&male;) will suffer from Huntington's disease AND hemophilia?
#hard, ask a compounded question: What fraction of their daughters (&female;) will suffer from Huntington's disease AND hemophilia?

#A. None, 0%
#B. 1/4, 25%
#C. 1/2, 50%
#D. 3/4, 75%
#E. All, 100%

#=====================
#=====================
#=====================
if __name__ == '__main__':
	md = multi-disorder_problem.MultiDisorderClass()
	for XLR_disorder_name, XLR_disorder_dict in md.disorder_data['X-linked recessive'].items():
		XLR_description = md.getDisorderParagraph(XLR_disorder_dict)
		print("============")
		print(XLR_description)
		print("")
		for AD_disorder_name, AD_disorder_dict in md.disorder_data['autosomal dominant'].items():
			AR_description = md.getDisorderParagraph(AR_disorder_dict)
			print(AR_description)
			print("")
