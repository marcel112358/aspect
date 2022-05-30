# Python script to load the solution data into a
# numpy array, interpolate the data to a new
# uniform grid, and plot the results.
# From a terminal, execute the script with
#   python gerya_2019_analysis.py
# Within a python interpreter (e.g., a Jupyter notebook), 
# the script can be executed with the command:
#   exec(open("gerya_2019_analysis.py").read())
# This script was tested with the following 
# package versions:
#   python     - 3.7.7
#   numpy      - 1.19.1
#   scipy      - 1.5.2
#   vtk        - 8.2.0
#   matplotlib - 3.3.1

import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import vtk as vtk
from vtk.util import numpy_support



def main():
  parser = argparse.ArgumentParser(
    description='Create a strain rate field and profile from the output directory of the aspect',
    epilog='Author: Marcel Saaro, John Naliboff'
  )
  parser.add_argument(
    "-o", "--output-dir",
    type=str,
    required=True,
    help='Path of the output dir in the prm file',
  )
  parser.add_argument(
    "-p", "--plot-file",
    type=str,
    required=True,
    help='Path of the plot file. None existing folders in the path will be created.',
  )
  args = parser.parse_args()

  output_dir = Path(args.output_dir)
  plot_file = Path(args.plot_file)

  # -------------------------------------------------------------------------
  # Load the data
  # -------------------------------------------------------------------------
  solution_folder = Path(output_dir) / 'solution'
  # Find the last pvtu file in the solution folder
  pvtu_file = sorted(solution_folder.glob('solution-*.pvtu'))[-1]

  x, y, strain_rate = get_data(pvtu_file, 'strain_rate')

  strain_rate = np.log10(strain_rate)


  # -------------------------------------------------------------------------
  # Generate the Profile
  # -------------------------------------------------------------------------
  profile_indx = np.argwhere(abs(y  - 11./16.*np.max(y)) < 1e-3)

  df = pd.DataFrame({
    'x' : x[profile_indx].ravel(),
    'profile' : strain_rate[profile_indx].ravel()
  })
  df = df.groupby('x').mean()


  # -------------------------------------------------------------------------
  # Plot
  # -------------------------------------------------------------------------
  fig = plt.figure(
    figsize=(12, 6), # in inch
    # facecolor='white',
  )
  # fig.suptitle(
  #   'Title',
  #   x=0.5, y=0.98,
  #   fontsize=14
  # )

  gs = fig.add_gridspec(
    nrows=1, ncols=2,
    left=0.125, right=0.9,
    bottom=0.11, top=0.88,
    hspace=0.2, wspace=0.3,
  )

  # Strain Rate Field
  ax = fig.add_subplot(
    gs[0, 0],
    aspect='equal',
    # facecolor='white',
    title='$\log_{10}$ of Strain Rate Second Invariant (1/s)',
    xlabel='Horizontal Position (m)',
    xlim=(np.min(x), np.max(x)),
    # xticks=[], # Hide if empty
    # xticklabels=[], # Hide if empty
    ylabel='Vertical Position (m)',
    ylim=(np.min(y), np.max(y)),
    # yticks=[], # Hide if empty
    # yticklabels=[], # Hide if empty
  )
  sc = ax.scatter(
    x, y,
    s=5, marker='s',
    c=strain_rate, edgecolors='none',
    rasterized=True,
  )
  fig.colorbar(
    sc, ax=ax,
    # label='',
    # ticks=[], # Hide if empty
    location='right',
    orientation='vertical',
    fraction=0.1,
    aspect=30,
    shrink=0.75,
  )

  # Strain Rate Profile
  ax = fig.add_subplot(
    gs[0, 1],
    # aspect='equal',
    box_aspect=0.85,
    # facecolor='white',
    title='$\log_{10}$ of Strain Rate Profile at y = Model_Height * 5/16',
    xlabel='Horizontal Position (m)',
    # xlim=(np.min(x), np.max(x)),
    # xticks=[], # Hide if empty
    # xticklabels=[], # Hide if empty
    ylabel='Log10 of Strain Rate Second Invariant (1/s)',
    # ylim=(np.min(y), np.max(y)),
    # yticks=[], # Hide if empty
    # yticklabels=[], # Hide if empty
  )
  df['profile'].plot(ax=ax)

  # Save the figure
  plot_file.parent.mkdir(parents=True, exist_ok=True)
  plt.savefig(plot_file)



def get_data(pvtu_file, field_name):
  # Originally created by John Naliboff
  reader = vtk.vtkXMLPUnstructuredGridReader()
  reader.SetFileName(pvtu_file)
  reader.Update()

  # Get the coordinates of nodes in the mesh
  nodes_vtk_array = reader.GetOutput().GetPoints().GetData()

  # Convert nodal vtk data to a numpy array
  nodes_numpy_array = vtk.util.numpy_support.vtk_to_numpy(nodes_vtk_array)

  # Extract x, y and z coordinates from numpy array 
  x, y = nodes_numpy_array[:,0], nodes_numpy_array[:,1]

  # Determine the number of scalar fields contained in the .pvtu file
  number_of_fields = reader.GetOutput().GetPointData().GetNumberOfArrays()

  # Determine the name of each field and place it in an array.
  field_names = []
  for i in range(number_of_fields):
    field_names.append(reader.GetOutput().GetPointData().GetArrayName(i))

  # Determine the index of the field strain_rate
  idx = field_names.index(field_name)

  # Extract values of strain_rate
  field_vtk_array = reader.GetOutput().GetPointData().GetArray(idx)
  field_array     = numpy_support.vtk_to_numpy(field_vtk_array)

  return x, y, field_array



if __name__ == "__main__":
  main()
