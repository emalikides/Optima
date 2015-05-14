import necpp

# Example script with documentation and explanation added by Emmanuel Malikides.

def handle_nec(result):
    if (result != 0):
        print(necpp.nec_error_message())

def impedance(frequency, z0, height):

# The central object in the NEC2++ simulation code is the nec context object, this
# object contains information about the state of the simulation as well as storing output
# information. A new nec context object is created for each simulation.
# After creation, a geometry is associated with the nec context through a c geometry
# object. This object contains details of the physical structure to be simulated. Analyses
# are then be triggered by calling methods on the nec context object. These methods
# correspond to the analysis cards of a traditional NEC-2 input file.


    # creates the object.
    nec = necpp.nec_create()
    n = 20
    # Why does the number of segments change the answer?

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

# Arguments: according to NEC guide
# ID
# I1 - type of excitation (0 is voltage source) determines the rest .
# I2 -
# I3
# I4
# F1
# F2
# F3
# F4
# F5
# F6

    handle_nec(necpp.nec_ex_card(nec, 0, 0, 1, 0, 1.0, 0, 0, 0, 0, 0))
    handle_nec(necpp.nec_rp_card(nec, 0, 90, 1, 0,5,0,0, 0, 90, 1, 0, 0, 0))
    result_index = 0

    z = complex(necpp.nec_impedance_real(nec,result_index),
                necpp.nec_impedance_imag(nec,result_index))

    necpp.nec_delete(nec)
    return z

# Frequency is in MHz
z = impedance(frequency = 34.5, z0 = 0.5, height = 4.0*20)
print("Impedance \t(%6.1f,%+6.1fI) Ohms" % (z.real, z.imag))
