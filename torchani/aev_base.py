import torch
from . import buildin_const_file


class AEVComputer:
    """Base class of various implementations of AEV computer

    Attributes
    ----------
    dtype : torch.dtype
        Data type of pytorch tensors for all the computations. This is also used
        to specify whether to use CPU or GPU.
    const_file : str
        The name of the original file that stores constant.
    constants : dict
        A dictionary that uses `str` as keys and `float` or `list` of `float`s as
        values to store constants.
    """

    def __init__(self, dtype=torch.cuda.float32, const_file=buildin_const_file):
        self.dtype = dtype
        self.const_file = const_file

        # load constants from const file
        self.constants = {}
        with open(const_file) as f:
            for i in f:
                try:
                    line = [x.strip() for x in i.split('=')]
                    name = line[0]
                    value = line[1]
                    if name == 'Rcr' or name == 'Rca':
                        self.constants[name] = float(value)
                    elif name in ['EtaR', 'ShfR', 'Zeta', 'ShfZ', 'EtaA', 'ShfA']:
                        value = [float(x.strip()) for x in value.replace(
                            '[', '').replace(']', '').split(',')]
                        self.constants[name] = value
                    elif name == 'Atyp':
                        value = [x.strip() for x in value.replace(
                            '[', '').replace(']', '').split(',')]
                        self.species = value
                except:
                    raise ValueError('unable to parse const file')

    def per_species_radial_length(self):
        """Returns the radial subaev length per species"""
        return len(self.constants['EtaR']) * len(self.constants['ShfR'])

    def radial_length(self):
        """Returns the full radial aev length"""
        return len(self.species) * self.per_species_radial_length()

    def per_species_angular_length(self):
        """Returns the angular subaev length per species"""
        return len(self.constants['EtaA']) * len(self.constants['Zeta']) * len(self.constants['ShfA']) * len(self.constants['ShfZ'])

    def angular_length(self):
        """Returns the full angular aev length"""
        species = len(self.species)
        return int((species * (species + 1)) / 2) * self.per_species_angular_length()

    def __call__(self, coordinates, species):
        """Compute AEV from coordinates and species

        Parameters
        ----------
        coordinates : pytorch tensor of `dtype`
            The tensor that specifies the xyz coordinates of atoms in the molecule.
            The tensor must have shape (conformations, atoms, 3)
        species : list of str
            The list that specifies the species of each atom. The length of the list
            must match with `coordinates.shape[1]`.

        Returns
        -------
        (pytorch tensor of `dtype`, pytorch tensor of `dtype`)
            Returns (radial AEV, angular AEV), both are pytorch tensor of `dtype`.
            The radial AEV must be of shape (conformations, atoms, radial_length())
            The angular AEV must be of shape (conformations, atoms, angular_length())
        """
        raise NotImplementedError('subclass must override this method')