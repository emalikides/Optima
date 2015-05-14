__author__ = 'purulentpig2'


import necpp

# test of Linden antenna.

def handle_nec(result):
    if (result != 0):
        print(necpp.nec_error_message())

def impedance(frequency, n, height):

    nec = necpp.nec_create()
    # \brief Generates segment geometry for a straight wire
    # \param in_context The nec_context created with nec_create()
    # \param tag_id
    # \param segment_count Number of Elements (should be around 12-20 per wavelength)
    # \param rad Wire radius of first segment (in Meters)
    # \param rdel Ratio of the length of a segment to the length of the previous segment.  (Set to 1.0 if segments have uniform length)
    # \param rrad The ratio of the radii of adjacent segments (Set to 1.0 if not tapered)
    # for nec_wire(in_context, tag_id, segment_count, x0, y0, z0, x1, y1, z1, rad, rdel, rrad)
    handle_nec(necpp.nec_wire(nec, 1, n, 0, 0, 0, 0, 0, height, 0.1, 1, 1))

    # # \brief Indicate that the geometry is complete (GE card)
	# \param in_context The nec_context created with nec_create()
	# \param gpflag Geometry ground plain flag.
	# 	0 - no ground plane is present.
	# 	1 - Indicates a ground plane is present. Structure symmetry is modified as required, and the current expansion is modified so that the currents an segments touching the ground (x, Y plane) are interpolated to their images below the ground (charge at base is zero)
	# 	-1 - indicates a ground is present. Structure symmetry is modified as required. Current expansion, however, is not modified, Thus, currents on segments touching the ground will go to zero at the ground.
	# \param card_int_2 Unused (set to zero)
    # void nec_geometry_complete(nec_context* in_context, int gpflag, int card_int_2);
    handle_nec(necpp.nec_geometry_complete(nec, 1, 0))


    handle_nec(necpp.nec_gn_card(nec, 1, 0, 0, 0, 0, 0, 0, 0))

#     /*!
#  * FR crd
#  *	@param in_context The nec_context created with nec_create()
#  *	@param in_ifrq 0 is a linear range of frequencies, 1 is a log range.
#  *	@param in_nfrq The number of frequencies
#  *	@param in_freq_mhz The starting frequency in MHz.
#  *	@param in_del_freq The frequency step (in MHz for ifrq = 0)
#  */
# void nec_fr_card(nec_context* in_context, int in_ifrq, int in_nfrq, double in_freq_mhz, double in_del_freq);
    handle_nec(necpp.nec_fr_card(nec, 0, 1, frequency, 0))

    # object
    # I1 - 0 means voltage source
    # I2 tag number of source segment - 0 means source identified using "absolute segment number"
    # I3 m specifies mth source segment, if I2 zero, then set to n?
    # I4 No action if zero.
    # last 6: Floating point options, F1-6,
    # for I1 = 0, (voltage source) F1 is real part of the voltage.
    # F2 - imaginary part of voltage
    # F3 F4, F5 and F6 should be blank.
    handle_nec(necpp.nec_ex_card(nec, 0,0,2, 0, 1.0, 0, 0, 0, 0, 0))

    # Specifies radiation pattern and causes program execution! - should be called last.
    # object Different to nec guide - see libnecpp.h document
    # calc_mode - 0 means space wave fields, with infinite ground plane.
    # number of theta angles
    nth = 90
    # number of phi angles
    nphi = 1
    # output format, 0 means major axis, minor axis and total gain will be printed, but will it be printed??
    output_format = 0
    # Controls the type of normalization of the output pattern, 5 means total gain is normalised.
    normalization = 5
    # Selects power gain (0) or directive gain (1)
    D = 0
    # Requests calculation of the average power gain. 0 means no averaging.
    A = 0
    # initial theta angle in degrees (angle to z axis - polar angle)
    theta0 = 0
    # initial phi angle in degrees (angle to north - azimuthal)
    phi0 = 90
    delta_theta = 1
    # increment for phi in degrees.
    delta_phi = 0
    # radial distance of field point from origin in metres. Should be in the far field if nonzero.
    radial_distance = 0
    # normalise the gain value - if zero, this normalises to the maximum value.
    gain_norm = 0
    handle_nec(necpp.nec_rp_card(nec, 0, nth, nphi, output_format,normalization,D,A, theta0, phi0, delta_theta,\
                                 delta_phi, radial_distance, gain_norm))
    handle_nec(necpp.nec_rp_card(nec, 0, nth, nphi, output_format,normalization,D,A, theta0, phi0, delta_theta,\
                                 delta_phi, radial_distance, gain_norm))
    result_index = 0

    z = complex(necpp.nec_impedance_real(nec,result_index),
                necpp.nec_impedance_imag(nec,result_index))

    necpp.nec_delete(nec)
    return z

# Frequency is in MHz
z  = impedance(frequency = 3e2, n = 4, height = 0.1)
z = z*z.conjugate()
print("Impedance \t(%6.1f,%+6.1fI) Ohms" % (z.real, z.imag))

