import random as rnd
import numpy as np
from itertools import islice

"""
CSE-537
Network Security
IIT BHU
Practical Assignment #4 
Author: Mohd Zeeshan Khan (19134012)
Problem Statement: Implement any two PRNGs in a language of your choice. Run any two randomness tests over them and report the result.

Tests performed:
1. Chi-squared for Uniformity
2. Kolmogorov-Smirnov Test for Uniformity
"""
 test_selection = ""
    while (test_selection != "q" ):
        select_test()
        test_selection = raw_input("Selection > ").strip()
        if test_selection == "q":
            exit()

        select_number_of_observations()
        number_observations = raw_input("Selection > ").strip()
        number_observations = int(number_observations)

        # If use selects python rand function
        if int(test_selection) == 1:
            python_rand( number_observations )
            run_test_suite(test_selection, number_observations)

        # If use selects LCG function,
        elif int(test_selection) == 2:
            generate_lcg( number_observations )
            run_test_suite(test_selection, number_observations)



        # If user selects LCG with RANDU settings
        elif int(test_selection) == 3:
            generate_lcg_RANDU( number_observations )
            run_test_suite(test_selection, number_observations)
        else:
            print "Please select a number from 1 to 3."

            
    # THREE GENERAL FUNCTION SETTINGS
    
    # x 1.  Standard random number generator in Python
    # x 2.  LCG Implementation(seed=123456789)
    #         o Where:  a=101427; c=321, m=(2**16)
    #         o Obtain each number in U[0,1) by diving X_i by m
    # x 3.  LCG with RANDU
    #         o Where: a=65539; c=0; m=(2**31)
    #         o Again, obtain each number in U[0,1) by diving X_i by m

    def python_rand( num_iterations ):
     """
     Run the built-in python random number generator and output a number of data points
     specified by the user to a file
     :param num_iterations:  The number of data points to write to file
     :return: void
     """
     # Initialize seed value
     x_value = 123456789.0    # Our seed, or X_0 = 123456789
     rnd.seed(x_value)

     # counter for how many iterations we've run
     counter = 0

     # Open a file for output
     outFile = open("py_random_output.txt", "wb")

     # Perform number of iterations requested by user
     while counter < num_iterations:
        x_value = rnd.random()
        # Write to file
        writeValue = str(x_value)
        outFile.write(writeValue + "\n")
        counter = counter + 1

     outFile.close()
     print("Successfully stored %d random numbers in file named: 'py_random_output.txt'.", num_iterations)


     def generate_lcg( num_iterations ):
    """
    LCG - generates as many random numbers as requested by user, using a Linear Congruential Generator
    LCG uses the formula: X_(i+1) = (aX_i + c) mod m
    :param num_iterations: int - the number of random numbers requested
    :return: void
    """
    # Initialize variables
    x_value = 123456789.0    # Our seed, or X_0 = 123456789
    a = 101427               # Our "a" base value
    c = 321                  # Our "c" base value
    m = (2 ** 16)            # Our "m" base value

    # counter for how many iterations we've run
    counter = 0

    # Open a file for output
    outFile = open("lgc_output.txt", "wb")

    #Perfom number of iterations requested by user
    while counter < num_iterations:
        # Store value of each iteration
        x_value = (a * x_value + c) % m

        #Obtain each number in U[0,1) by diving X_i by m
        writeValue = str(x_value/m)

        # write to output file
        outFile.write(writeValue + "\n")
        # print "num: " + " " + str(counter) +":: " + str(x_value)

        counter = counter+1

    outFile.close()
    print("Successfully stored " + str(num_iterations) + " random numbers in file named: 'lgc_output.txt'.")


    def generate_lcg_RANDU( num_iterations ):
    """
    LCG RANDU- generates as many random numbers as requested by user, using a Linear Congruential Generator
    LCG uses the formula: X_(i+1) = (aX_i + c) mod m.
    This LCG uses the RANDU initial setting, a=65539; c=0; m=2^31.
    RANDU is known to have an issue: its values fall into 15 parallel 2D planes.
    So while its pseudo-randomness is enough for some applications. It's not great.
    Not crypto strength by any means.
    :param num_iterations: int - the number of random numbers requested
    :return: void
    """
    # Initialize variables
    x_value = 123456789.0    # Our seed, or X_0 = 123456789
    a = 65539                # Our "a" base value
    c = 0                    # Our "c" base value
    m = (2 ** 31)            # Our "m" base value

    # counter for how many iterations we've run
    counter = 0

    # Open a file for output
    outFile = open("lgc_RANDU_output.txt", "wb")

    #Perfom number of iterations requested by user
    while counter < num_iterations:
        # Store value of each iteration
        x_value = (a * x_value + c) % m

        #Obtain each number in U[0,1) by diving X_i by m
        writeValue = str(x_value/m)

        # write to output file
        outFile.write(writeValue + "\n")
        # print "num: " + " " + str(counter) +":: " + str(x_value)

        counter = counter+1

    outFile.close()
    print "Successfully stored " + str(num_iterations) + " random numbers in file named: 'lgc_RANDU_output.txt'."



######################
#### STATS TESTS #####
######################
    # STATISTICAL TESTS
    # Check for uniformity at 80%, 90%, and 95% level. Note that some tests are one-sided, others two sided
    # x 1. Chi-Square Frequency Test for Uniformity
    #      - Collect 10,000 numbers per generation method
    #      - Sub-divide[0.1) into 10 equal subdivisions
    # x 2. Kolmogorov-Smirnov Test for uniformity
    #      - Since K-S Test works better with a smaller set of numbers, you may use the first 100
    #        out fo the 10,000 that you generated for the Chi-Square Frequency Test

    def chi_square_uniformity_test( data_set, confidence_level, num_samples ):
    """
    Null hypothesis:  Our numbers distributed uniformly on the interval [0, 1).
    This function uses the chi-square test for uniformity to determine whether our numbers
    are uniformly distributed on the interval [0,1).
    Formula is: "sum[ (observed-val - expected-val)^2 / expected val ], from 0 to num_samples"
    This gives us a number which we can test against a chi-square value table.
    Also need to know, degrees of freedom:  df=num_samples-1
    :param data_set: the data_set, must be a dictionary with 10 intervals.
                     Use return value from  @divide_RNG_data_into_10_equal_subdivisions_and_count
    :param confidence_level: confidence level we are testing at
    :param num_samples: number of data points
    :return: A chi-squared value
    """
    # This is our test statistic, this will be an accumulated value, as we loop through the data set
    chi_sq_value = 0.0
    degrees_of_freedom = num_samples - 1

    # We're doing 10 equal subdivisions, so need to divide our number samples by 10,
    # Assuming uniform distribution, to get an expected value. All values should be same
    # If our distro is actually uniform.
    expected_val = num_samples/10.0


    # Loop through a dictionary and get every count
    # The observed value is going to be our count at each key, and then we can do chi-square
    for observed_val in data_set:
        # print "Observed value is: " + observed_val
        chi_sq_value += ( pow((expected_val - data_set[observed_val]), 2)/expected_val )

    # Coming out of this loop, we'll have a chi-squared test statistic
    # Now we just need to do a lookup to see if it's valid
    return chi_sq_value

    def kolmogorov_smirnov_test( data_set, confidence_level, num_samples ):
    """
    Kolmogorov-Smirnov test for uniform distribution of Random numbers
    :param data_set: The set of data to analyze. Should be floating point numbers [0,1) in a .txt file
    :param confidence_level: with how much confidence should we test?
    :param num_samples: number of samples to analyze
    :return: test statistic
    """
    # Step 1:  Rank data from smallest to largest, such that:
    # R(1) <= R(2) <= R(3) ... <= R(i)
    data_set.sort()

    # Step 2: Computer D+ and D-
    # D+ = max(i/N - R(i))
    d_plus = get_d_plus_value_for_KS_TEST(data_set, num_samples)
    print "D+ VALUE ="+str(d_plus)

    # D- = max(R(i) - (i -1)/n)
    d_minus = get_d_minus_value_for_KS_TEST(data_set, num_samples)
    print "D- VALUE="+str(d_minus)

    # Step 3:  Computer D = max(D+,D-)
    d_value = max(d_plus, d_minus)
    print "D VALUE (max): "+str(d_value)

    # Step 4: Determine critical value, using table
    # Step 5: Accept or reject Null hypothesis
    return d_value


##############################
##### Significance Tests #####
##############################

def chi_sq_significance_test( chi_sq, signif_level):
    """
    Performs a significance test for df=10000, based on values calculated at:
    https://www.swogstat.org/stat/public/chisq_calculator.htm
    :param chi_sq:  Chi-sq value to test
    :param signif_level: Level of significance we are testing: 0.80, 0.90, or 0.95
    :return: message stating whether we accept or reject null
    """
    result = "FAIL TO REJECT null hypothesis"
    crit_value = 0.0
    if signif_level == 0.8:
        crit_value = 10118.8246
    elif signif_level == 0.90:
        crit_value = 10181.6616
    elif signif_level == 0.95:
        crit_value = 10233.7489
    else:
        print "**Invalid Significance Level for Chi Sq***"

    if chi_sq > crit_value:
        result = "REJECT null hypothesis"

    print "Print Significance Level: " + str(signif_level)
    print "Chi Sq: " + str(chi_sq)
    print "Crit Value: " + str(crit_value)
    print "Result is: " + result
    print "...................................."

    return result

def ks_significance_test( d_statistic, num_observations, alpha_level ):
    """
    Perform Significance test for Kolmogorov-Smirnov
    Uses formulas from table A.7:  Discrete-Event System Simulation, by Banks and Carson, 1984
    :param d_statistic: The d-value we are testing
    :param num_observations: The number of observations in our data set
    :param alpha_level: The level of significance we are testing
    :return: result -- accept or reject
    """
    result = "FAIL TO REJECT null hypothesis"
    critical_value = 0


    if alpha_level == 0.1:
        critical_value = 1.22/np.sqrt(num_observations)
    elif alpha_level == 0.05:
        critical_value = 1.36/np.sqrt(num_observations)
    elif alpha_level == 0.01:
        critical_value = 1.63/np.sqrt(num_observations)
    else:
        print ("Invalid alpha level for KS test. Must be: 0.1, 0.05, or 0.01")

    if d_statistic > critical_value:
        result = ("REJECT null hypothesis")
    print ("Alpha Level is: " + str(alpha_level))
    print ("D_statistic is: " + str(d_statistic))
    print ("Critical value is: " + str(critical_value))
    print ("Result is: " + result)
    print ("............................")

    return result


#######################
### Helper Methods ####
#######################

def collect_first_100_samples_in_data_set( data_file ):
    """
    Takes a data file, with real number data points between [0,1) reads the first 100 values,
    then adds them to a dictionary as our return value
    :param data_file: A string - the name of the file to read in our current directory
    :return: A dictionary containing the first 100 values as floats
    """

    first_100_vals_as_FLOATS = []
    # grabs first 100 files, as strings with newline endpoints
    with open( data_file, "r" ) as f:
        first_100_vals_as_STRINGS = list(islice(f, 100))

    # transform all values to floats
    for val in first_100_vals_as_STRINGS:
        val = float(val)
        first_100_vals_as_FLOATS.append(val)

    return first_100_vals_as_FLOATS


def divide_RNG_data_into_10_equal_subdivisions_and_count( data_file ):
    """
    Takes a path to a data file in the current directory.
    Returns a dictionary with keys 1-10, values=num instances in each of
    10 equal intervals from range: [0, 1).
    The function counts how many data points are in each interval, and gives us
    a dictionary so we can manipulate this data more easily, based on count by index.
    :param data_file: Must be in current directory. Pass in the string name.
    :return: A dictionary with counts of how many occurrences our data had for each
    of 10 equal intervals between [0, 1). (Divided into 10ths)
    """
    # For each of our uniformity tests, need to divide our data points in 10 equal subdivisions
    subdivisions = {  "1":  0,
                      "2":  0,
                      "3":  0,
                      "4":  0,
                      "5":  0,
                      "6":  0,
                      "7":  0,
                      "8":  0,
                      "9":  0,
                      "10": 0   }
    with open(data_file, "r") as f:
        # data points is a list containing all numbers we've read in.
        data_points = f.readlines()

    # Loop through our data points and count number of data points in each subdivision
    # Divide by tenths, from 0.0 to 1.0.
    for num in data_points:
        num = float(num)
        if num < 0.1:
            subdivisions["1"] += 1
        elif num < 0.2:
            subdivisions["2"] += 1
        elif num < 0.3:
            subdivisions["3"] += 1
        elif num < 0.4:
            subdivisions["4"] += 1
        elif num < 0.5:
            subdivisions["5"] += 1
        elif num < 0.6:
            subdivisions["6"] += 1
        elif num < 0.7:
            subdivisions["7"] += 1
        elif num < 0.8:
            subdivisions["8"] += 1
        elif num < 0.9:
            subdivisions["9"] += 1
        elif num < 1.0:
            subdivisions["10"] += 1

    return subdivisions


def get_d_plus_value_for_KS_TEST( data_set, num_samples ):
    """
    Finds the D+ value for a KS test
    :param data_set: 100 values, must be a list of floats
    :return: the D-+Statistic for our data set
    """
    # D+ = max(i/N - R(i))
    d_plus_max = 0
    value_rank_i = 1

    # iterate through data set
    for value in data_set:
        # Do each D+ calculation, store it
        d_plus_i_value = ( (value_rank_i/num_samples) - value )

        # Check if it is highest D+ value yet
        if d_plus_i_value > d_plus_max:
            d_plus_max = d_plus_i_value

        # increment our "i" value
        value_rank_i = value_rank_i + 1

    # coming out of this loop, D+ = highest D+ value
    return d_plus_max


def get_d_minus_value_for_KS_TEST( data_set, num_samples ):
    """
    Finds the D- value for a KS test
    :param data_set: 100 values, must be a list of floats
    :return: the D- Statistic for our data set
    """
    # D- = max(R(i) - (i -1)/n)
    d_minus_max = 0
    value_rank_i = 1.0

    # iterate through data set
    for value in data_set:
        # Do each D+ calculation, store it
        substraction_value = ( (value_rank_i - 1.0)/num_samples )
        d_minus_i_value = value - substraction_value

        # Check if it is highest D+ value yet
        if d_minus_i_value > d_minus_max:
            d_minus_max = d_minus_i_value

        # increment our "i" value
        value_rank_i = value_rank_i + 1

    # coming out of this loop, D+ = highest D+ value
    return d_minus_max

def select_test():
    """
    Command line prompt for selecting a test
    :return: void - prints a prompt to command line
    """
    print ("Please select a method for generating random numbers: ")
    print (" 1. Python's Random Function")
    print (" 2. Linear Congruential Generator ") 
    print (" 3. Linear Feedback Shift Register ") 
    print ("      (or type 'q' to quit)")
    print ("")

def select_number_of_observations():
    """
    Command line prompt to select the number of observations for a given test
    :return: void - prints a prompt to command line
    """
    print ("How many observations should we perform?")


def run_test_suite( test_selection, number_observations ):
    """
    Runs all of our test suites and prints output to the screen
    :param test_selection:  an int - 1,2, or 3. Corresponds to test selected.
    :param number_observations: the number of data points to test
    :return: void - prints to command line
    """
    input_file = ""
    test_name = ""
    test_selection = int(test_selection)
    if test_selection == 1:
        input_file = "py_random_output.txt"
        test_name = "PYTHON BUILT-IN RAND"

    elif test_selection == 2:
        input_file = "lgc_output.txt"
        test_name = "LINEAR CONGRUENTIAL GENERATOR"

    elif test_selection ==3:
        input_file="lfsr_output.txt"
        test_name= "LINEAR FEEDBACK SHIFT REGISTER"

    else:
        print ("Invalid input. Please try again.")

    print ("")
    print ("TEST SUITE FOR:  %s " % (test_name))
    print ("======================================")

    # divide our output values in 10 equal subdivisions and run chi-square test
    print ("---------CHI-SQ_TEST-----------")
    data_points = divide_RNG_data_into_10_equal_subdivisions_and_count(input_file)
    chi_sq_result = chi_square_uniformity_test(data_points, 0, number_observations)
    chi_sq_significance_test( chi_sq_result, 0.8 )
    chi_sq_significance_test( chi_sq_result, 0.9 )
    chi_sq_significance_test( chi_sq_result, 0.95 )

    print ("")

    # get first 100 values from sample and run kolmogorov-smirnov test
    print ("---------KS_TEST-----------")
    first_100_values = collect_first_100_samples_in_data_set(input_file)
    first_100_values.sort()
    ks_result = kolmogorov_smirnov_test(first_100_values,1,100)
    ks_significance_test(ks_result,100, 0.1)
    ks_significance_test(ks_result,100, 0.05)
    ks_significance_test(ks_result,100, 0.01)
    print ("Kolmogorov-Smirnov Test Result for D-Value: " + str(ks_result))
    print ("")

if __name__ == "__main__":
    main()

