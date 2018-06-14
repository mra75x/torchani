import torch
import torchani

device = torch.device('cpu')
const_file = '../torchani/resources/rHCNO-4.6R_16-3.1A_a4-8_3.params'
sae_file = '../torchani/resources/sae_linfit.dat'
network_dir = '../torchani/resources/networks/'

aev_computer = torchani.SortedAEV(const_file=const_file, device=device)
nn = torchani.ModelOnAEV(aev_computer, derivative=True, from_nc=network_dir)
shift_energy = torchani.EnergyShifter(sae_file)

coordinates = torch.tensor([[[0.03192167,  0.00638559,  0.01301679],
                             [-0.83140486,  0.39370209, -0.26395324],
                             [-0.66518241, -0.84461308,  0.20759389],
                             [0.45554739,   0.54289633,  0.81170881],
                             [0.66091919,  -0.16799635, -0.91037834]]],
                           dtype=aev_computer.dtype, device=aev_computer.device)
species = ['C', 'H', 'H', 'H', 'H']

energy, derivative = nn(coordinates, species)
energy = shift_energy.add_sae(energy, species)
force = -derivative

print('Energy:', energy.item())
print('Force:', force.squeeze().numpy())