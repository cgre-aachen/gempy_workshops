import matplotlib.pyplot as plt
import numpy as np
import gempy as gp


def plot_centered_grid(centered_grid, slice=None):

	a, b, c = centered_grid.kernel_centers, centered_grid.kernel_dxyz_left, \
	          centered_grid.kernel_dxyz_right
	tz = centered_grid.tz
	res = np.array(centered_grid.resolution) + 1
	if slice is None:
		slice = int(res[1]/2)

	fig = plt.figure(figsize=(13, 7))
	ax = fig.add_subplot(111)

	if tz.shape[0] != 0:
		plt.quiver(a[:, 0].reshape(res)[slice, :, :].ravel(),
		           a[:, 2].reshape(res)[:, slice, :].ravel(),
		           np.zeros(231),
		           tz.reshape(res)[slice, :, :].ravel(), label='$t_z$', alpha=.3
		           )

	plt.plot(a[:, 0].reshape(res)[slice, :, :].ravel(),
	         a[:, 2].reshape(res)[:, slice, :].ravel(), 'o', alpha=.3, label='Centers')

	# plt.plot(
	# 	a[:, 0].reshape(res)[slice, :, :].ravel() - b[:, 0].reshape(res)[slice, :, :].ravel(),
	# 	a[:, 2].reshape(res)[:, slice, :].ravel(), '.', alpha=.3, label='Lefts')
	#
	# plt.plot(a[:, 0].reshape(res)[slice, :, :].ravel(),
	#          a[:, 2].reshape(res)[:, slice, :].ravel() - b[:, 2].reshape(res)[:, slice,
	#                                                         :].ravel(), '.', alpha=.6,
	#          label='Ups')
	#
	# plt.plot(
	# 	a[:, 0].reshape(res)[slice, :, :].ravel() + c[:, 0].reshape(res)[slice, :, :].ravel(),
	# 	a[:, 2].reshape(res)[:, slice, :].ravel(), '.', alpha=.3, label='Rights')
	#
	# plt.plot(a[:, 0].reshape(res)[slice, :, :].ravel(),
	#          a[:, 2].reshape(res)[:, slice, :].ravel() + c[:, 2].reshape(res)[slice, :,
	#                                                         :].ravel(), '.', alpha=.3,
	#          label='Downs')


	ax.set_xticks(a[:, 0].reshape(res)[slice, :, :].ravel() -
	             b[:, 0].reshape(res)[slice, :, :].ravel())

	# ax.set_xticks(a[:, 0].reshape(res)[slice, :, :].ravel() +
	#               c[:, 0].reshape(res)[slice, :, :].ravel())

	ax.set_yticks(a[:, 2].reshape(res)[:, slice, :].ravel() -
	              b[:, 2].reshape(res)[:, slice, :].ravel())

	plt.grid()

	# plt.xlim(-200, 200)
	# plt.ylim(-200, 0)
	plt.legend()
	# plt.show()
	return fig


def plot_grav_inter(geo_model):
	# Creating new figure
	p_grav = gp.plot_2d(geo_model, direction=None, show=False, figsize=(6, 9))

	# Adding section for model
	ax2 = p_grav.add_section(cell_number=1, direction='y', ax_pos=211)

	# Adding section for gravity
	ax3 = p_grav.add_section(ax_pos=414)

	# Plotting model in section
	p_grav.plot_data(ax2, cell_number=5, legend=None)
	p_grav.plot_lith(ax2, cell_number=5)
	p_grav.plot_contacts(ax2, cell_number=5)
	ax2.plot(400, 0, '^', markersize=40, c='red')

	# Plotting initial values of the gravity axes
	target_grav = -81
	ax3.tick_params(bottom=False)
	ax3.spines['top'].set_visible(False)
	ax3.spines['bottom'].set_visible(False)
	ax3.spines['right'].set_visible(False)
	ax3.plot(0, target_grav, 'X', label='Target Gravity', markersize=4, c='red')
	ax3.plot(1, geo_model.solutions.fw_gravity, 'o', label='Current Gravity', markersize=4,
	         c='blue')
	ax3.set_ylabel('grav')

	# We store the original values of z for the surface 3
	Z_ori = geo_model.surface_points.df.loc[[5, 6, 7], 'Z'].copy()
	# init a list to store grav
	grav_ = []

	# Function that modify the model, compute it and plot
	def gravity_invert(dz):
		new_z = Z_ori + dz
		geo_model.modify_surface_points(indices=[5, 6, 7], Z=new_z)
		gp.compute_model(geo_model)
		grav_.append(geo_model.solutions.fw_gravity[0])

		p_grav.remove(ax2)
		p_grav.plot_data(ax2, cell_number=5)
		p_grav.plot_lith(ax2, cell_number=5)
		p_grav.plot_contacts(ax2, cell_number=5)
		ax3.plot(np.arange(len(grav_)) + 1, grav_, 'o', label='Current Gravity', markersize=4,
		         c='blue')
		ax3.set_xlim(-1, len(grav_) + 1)

	return gravity_invert