
from necpp import *

def handle_nec(result):
    if (result != 0):
        print(nec_error_message())

def example3():

    nec = nec_create()

    # example at: http://tmolteno.github.io/necpp/test_nec_8c-example.html
    handle_nec(nec_wire(nec, 0, 9, 0., 0.0, 2.0, 0.0, 0.0, 7.0, 0.03, 1.0, 1.0));
    handle_nec(nec_geometry_complete(nec, 1, 0));
    handle_nec(nec_ek_card(nec, 0));
    handle_nec(nec_fr_card(nec, 0, 1, 30., 0 ));
    handle_nec(nec_ex_card(nec, 0, 0, 5, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0));
    handle_nec(nec_gn_card(nec, 1, 0, 0, 0, 0, 0, 0, 0));
    handle_nec(nec_rp_card(nec, 0,10,2,1,3,0,1,0.0,0.0,10.0,90.0, 0, 0));

    result_index = 0
    z = complex(nec_impedance_real(nec,result_index),
                nec_impedance_imag(nec,result_index))

    print(dir(nec))
    nec_delete(nec)
    return z

# Frequency is in MHz
z  = example3()
print("Impedance \t(%6.14f,%+6.1fI) Ohms" % (z.real, z.imag))


