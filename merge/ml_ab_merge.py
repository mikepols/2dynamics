#!/usr/bin/env python3

import argparse
import math

def main():

    args = parse_command_line_arguments()
    trainsets = args.input
    filename = args.output

    combined_trainset_info, configurations = get_combined_trainset(trainsets)
    output_combined_trainset(filename, combined_trainset_info, configurations)

def parse_command_line_arguments():
    """
    Parse command line arguments for analyzing the chirality of metal halide perovskite structures or trajectories.
    """
    parser = argparse.ArgumentParser(description='Merge a number of VASP MLFF training sets into one training set')

    parser.add_argument('-i', '--input', help='Path to the MLFF training sets to be merged', required=True, type=str, nargs='+')
    parser.add_argument('-o', '--output', help='Path to the combined MLFF training set to be output', required=True, type=str)

    return parser.parse_args()

def get_combined_trainset(trainsets):
    """
    Combine a list of training sets into a single training set
    """
    combined_trainset_info = {
        'N_configs': 0,
        'N_species': 0,
        'N_max_atoms': 0,
        'N_max_atom_type': 0,
        'atom_types': [],
        'atom_masses': [],
    }

    configurations = []
    for trainset in trainsets:
        trainset_info = get_trainset_information(trainset)
        combined_trainset_info = update_combined_trainset_info(combined_trainset_info, trainset_info)
        configurations = get_trainset_configurations(configurations, trainset, trainset_info)

    return combined_trainset_info, configurations

def output_combined_trainset(filename, combined_trainset_info, configurations):
    """
    Output the combined training sets to a file
    """
    section_break = '*' * 50 + '\n'
    subsection_break = '-' * 50 + '\n'

    N_species_blocks = int(math.ceil(combined_trainset_info['N_species'] / 3))
    N_full = combined_trainset_info['N_species'] // 3
    N_partial = combined_trainset_info['N_species'] % 3

    N_lengths = [3 for x in range(N_full)]
    if N_partial != 0:
        N_lengths.append(N_partial)

    ts = ' 1.0 Version\n'
    ts += section_break

    # Configurations
    ts += '    The number of configurations\n'
    ts += subsection_break
    ts += '    {:>6.0f}\n'.format(combined_trainset_info['N_configs'])
    ts += section_break

    # Maximum number of atom types
    ts += '    The maximum number of atom type\n'
    ts += subsection_break
    ts += '    {:>6.0f}\n'.format(combined_trainset_info['N_species'])
    ts += section_break

    # Atom types
    ts += '    The atom types in the data file\n'
    ts += subsection_break
    for idx, length in enumerate(N_lengths):
        s_tmp = '    {:>3}' * length + '\n'
        ts += s_tmp.format(*combined_trainset_info['atom_types'][3 * idx:3 * idx + length])
    ts += section_break

    # Maximum number of atoms per system
    ts += '    The maximum number of atoms per system\n'
    ts += subsection_break
    ts += '    {:>6.0f}\n'.format(combined_trainset_info['N_max_atoms'])
    ts += section_break

    # Maximum number of atoms per atom type
    ts += '    The maximum number of atoms per atom type\n'
    ts += subsection_break
    ts += '    {:>6.0f}\n'.format(combined_trainset_info['N_max_atom_type'])
    ts += section_break

    # Reference atomic energies
    ts += '    Reference atomic energy (eV)\n'
    ts += subsection_break
    for idx, length in enumerate(N_lengths):
        s_tmp = '    {:<12.0E}  ' * length + '\n'
        ts += s_tmp.format(*[0] * length)
    ts += section_break

    # Atomic masses
    ts += '    Atomic mass\n'
    ts += subsection_break
    for idx, length in enumerate(N_lengths):
        s_tmp = '    {:<12.03f}' * length + '\n'
        ts += s_tmp.format(*combined_trainset_info['atom_masses'][3 * idx:3 * idx + length])
    ts += section_break

    # Number of basis sets
    ts += '    The numbers of basis sets per atom type\n'
    ts += subsection_break
    for idx, length in enumerate(N_lengths):
        s_tmp = '    {:<8.0f}  ' * length + '\n'
        ts += s_tmp.format(*[1] * length)
    ts += section_break

    for idx, atom_type in enumerate(combined_trainset_info['atom_types']):
        ts += '    Basis set for {:}\n'.format(atom_type)
        ts += subsection_break
        ts += '    {:<8.0f}{:<8.0f}\n'.format(1, 1)
        if idx != combined_trainset_info['N_species'] - 1:
            ts += section_break

    for configuration in configurations:
        for line in configuration:
            ts += line

    # Output training set to file
    with open(filename, 'w') as f:
        f.write(ts)

def update_combined_trainset_info(combined_trainset_info, trainset_info):
    """
    Update the training set information of the combined training set
    """
    if trainset_info['N_species'] > combined_trainset_info['N_species']:
        combined_trainset_info['atom_types'] = trainset_info['atom_types']
        combined_trainset_info['atom_masses'] = trainset_info['atom_masses']

    data2replace = ['N_species', 'N_max_atoms', 'N_max_atom_type']
    for data_name in data2replace:
        if trainset_info[data_name] > combined_trainset_info[data_name]:
            combined_trainset_info[data_name] = trainset_info[data_name]

    data2add = ['N_configs']
    for data_name in data2add:
        combined_trainset_info[data_name] += trainset_info[data_name]

    return combined_trainset_info

def get_trainset_information(file):
    """
    Obtain standard information from training set
    """
    # Find sections from training set
    section_break = '*' * 50
    section_idxs = []
    with open(file) as trainset:
        for num, line in enumerate(trainset):
            if section_break in line:
                section_idxs.append(num)

    # Read training set
    trainset = open(file, 'r')
    data = trainset.readlines()
    trainset.close()

    trainset_info = {}

    # Integers
    trainset_info['N_configs'] = int(data[section_idxs[0]:section_idxs[1]][-1].strip())
    trainset_info['N_species'] = int(data[section_idxs[1]:section_idxs[2]][-1].strip())
    trainset_info['N_max_atoms'] = int(data[section_idxs[3]:section_idxs[4]][-1].strip())
    trainset_info['N_max_atom_type'] = int(data[section_idxs[4]:section_idxs[5]][-1].strip())

    # Data from lists
    N_species_blocks = int(math.ceil(trainset_info['N_species'] / 3))

    # Atom types
    atom_types_raw = data[section_idxs[2]:section_idxs[3]][-N_species_blocks:]
    atom_types = []
    for row in atom_types_raw:
        atom_types.extend(row.strip().split())
    trainset_info['atom_types'] = atom_types

    # Atom masses
    atom_masses_raw = data[section_idxs[6]:section_idxs[7]][-N_species_blocks:]
    atom_masses = []
    for row in atom_masses_raw:
        atom_masses.extend([float(x) for x in row.strip().split()])
    trainset_info['atom_masses'] = atom_masses

    return trainset_info

def get_trainset_configurations(configurations, file, trainset_info):
    """
    Obtain configurations from training set
    """
    # Find sections from training set
    section_break = '*' * 50
    section_idxs = []
    with open(file) as trainset:
        for num, line in enumerate(trainset):
            if section_break in line:
                section_idxs.append(num)
    section_idxs.append(num + 1)

    # Read training set
    trainset = open(file, 'r')
    data = trainset.readlines()
    trainset.close()

    N_basis = 8
    N_species = trainset_info['N_species']
    N_configs = trainset_info['N_configs']
    N_offset = len(configurations)
    config_idxs = section_idxs[N_basis + N_species:]

    for idx in range(N_configs):
        configuration = data[config_idxs[2 * idx]:config_idxs[2 * idx + 2]]
        configuration[1] = '     Configuration num. {:>6.0f}\n'.format(idx + N_offset + 1)
        configurations.append(configuration)

    return configurations

if __name__ == '__main__':
    main()
