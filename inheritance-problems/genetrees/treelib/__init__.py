import os
import sys

# Add the top-level directory (parent of `treelib`) to sys.path
top_level_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if top_level_dir not in sys.path:
	sys.path.append(top_level_dir)
