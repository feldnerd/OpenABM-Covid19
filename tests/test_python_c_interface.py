#!/usr/bin/env python3
"""
Very basic example to show how testing may work using pytest

Usage:
With pytest installed (https://docs.pytest.org/en/latest/getting-started.html) tests can be 
run by calling 'pytest' from project folder.

pytest ./tests/test_step_calc.py

Created: March 2020
Author: Daniel Montero
"""

import sys
import subprocess, shutil, os
from os.path import join
import numpy as np, pandas as pd
from random import randrange
import pytest

sys.path.append("src/COVID19")
from model import Model, Parameters, ModelParamaterException


# STEPS > 0
STEPS = randrange(1, 10)
PARAM_LINE_NUMBER = 1

# Directories
IBM_DIR = "src"
IBM_DIR_TEST = "src_test"
DATA_DIR_TEST = "data_test"

TEST_DATA_TEMPLATE = "./tests/data/baseline_parameters.csv"
TEST_DATA_HOUSEHOLD_DEMOGRAPHICS = "./tests/data/baseline_household_demographics.csv"
TEST_DATA_FILE = join(DATA_DIR_TEST, "test_params.csv")


class TestClass(object):
    """
    Test class for checking
    """

    @classmethod
    def setup_class(self):
        """
        When the class is instatiated: compile the IBM in a temporary directory
        """

        # Make a temporary copy of the code (remove this temporary directory if
        # it already exists)
        shutil.rmtree(IBM_DIR_TEST, ignore_errors=True)
        shutil.copytree(IBM_DIR, IBM_DIR_TEST)

        # Construct the compilation command and compile
        compile_command = "make clean; make swig-all"
        completed_compilation = subprocess.run(
            [compile_command], shell=True, cwd=IBM_DIR_TEST, capture_output=True
        )

    @classmethod
    def teardown_class(self):
        """
        Remove the temporary code directory (when this class is removed)
        """
        shutil.rmtree(IBM_DIR_TEST, ignore_errors=True)

    def setup_method(self):
        """

        """
        os.mkdir(DATA_DIR_TEST)
        shutil.copy(TEST_DATA_TEMPLATE, TEST_DATA_FILE)

    def teardown_method(self):
        """

        """
        shutil.rmtree(DATA_DIR_TEST, ignore_errors=True)

    """
    def test_lockdown_on_off(self):
    """
        #Test that a lock down can be turned on and off
    """
        # Create model object
        params = Parameters(
            TEST_DATA_TEMPLATE,
            PARAM_LINE_NUMBER,
            DATA_DIR_TEST,
            TEST_DATA_HOUSEHOLD_DEMOGRAPHICS,
        )
        params.set_param( "app_users_fraction", 0.25)
        model = Model(params)

        STEPS = 100
        last  = 0
        # Run steps
        for step in range(0, STEPS):
            model.one_time_step()
            res = model.one_time_step_results()
            
            print( "Time =  " + str( res["time"]) + 
                   "; lockdown = "  +  str( res["lockdown"]) +  
                   "; app_turned_on = "  +  str( model.get_param( "app_turned_on") ) +  
                   "; new_infected = " + str( res[ "total_infected" ] - last )
            )
            
            last = res[ "total_infected" ] 
            
            if res["time"] == 20:
                model.update_running_params( "lockdown_on", 1 )
                np.testing.assert_equal(model.get_param("lockdown_on"), 1)


            if res["time"] == 30:
                model.update_running_params( "lockdown_on", 0 )
                model.update_running_params( "app_turned_on", 1 )
                np.testing.assert_equal(model.get_param("lockdown_on"), 0)
                np.testing.assert_equal(model.get_param("lockdown_on"), 1)

            if res["time"] == 60:
                model.update_running_params( "app_users_fraction", 0.85 )
    """
    

    def test_set_get_parameters(self):
        """
        Test the a parameter can be changed in between step runs
        """
        # Create model object
        params = Parameters(
            TEST_DATA_TEMPLATE,
            PARAM_LINE_NUMBER,
            DATA_DIR_TEST,
            TEST_DATA_HOUSEHOLD_DEMOGRAPHICS,
        )
        params.set_param( "app_users_fraction", 0.25)
        model = Model(params)

        STEPS = 2
        # Run steps
        for step in range(0, STEPS):
            model.one_time_step()
            res = model.one_time_step_results()
           
            # Try to set valid parameters
            model.update_running_params("test_on_symptoms", 1)
            np.testing.assert_equal(model.get_param("test_on_symptoms"), 1)

            model.update_running_params("test_on_traced", 1)
            np.testing.assert_equal(model.get_param("test_on_traced"), 1)

            model.update_running_params("quarantine_on_traced", 1)
            np.testing.assert_equal(model.get_param("quarantine_on_traced"), 1)

            model.update_running_params("traceable_interaction_fraction", 0.30)
            np.testing.assert_equal(
                model.get_param("traceable_interaction_fraction"), 0.30
            )

            model.update_running_params("tracing_network_depth", 1)
            np.testing.assert_equal(model.get_param("tracing_network_depth"), 1)

            model.update_running_params("allow_clinical_diagnosis", 1)
            np.testing.assert_equal(model.get_param("allow_clinical_diagnosis"), 1)

            model.update_running_params("quarantine_household_on_positive", 1)
            np.testing.assert_equal(
                model.get_param("quarantine_household_on_positive"), 1
            )

            model.update_running_params("quarantine_household_on_symptoms", 1)
            np.testing.assert_equal(
                model.get_param("quarantine_household_on_symptoms"), 1
            )

            model.update_running_params("quarantine_household_on_traced", 1)
            np.testing.assert_equal(
                model.get_param("quarantine_household_on_traced"), 1
            )

            model.update_running_params("quarantine_household_contacts_on_positive", 1)
            np.testing.assert_equal(
                model.get_param("quarantine_household_contacts_on_positive"), 1,
            )

            model.update_running_params("quarantine_days", 1)
            np.testing.assert_equal(model.get_param("quarantine_days"), 1)

            model.update_running_params("test_order_wait", 1)
            np.testing.assert_equal(model.get_param("test_order_wait"), 1)

            model.update_running_params("test_result_wait", 1)
            np.testing.assert_equal(model.get_param("test_result_wait"), 1)

            model.update_running_params("self_quarantine_fraction", 1)
            np.testing.assert_equal(model.get_param("self_quarantine_fraction"), 1)

            # Try to set/get invalid parameters
            with pytest.raises(ModelParamaterException):
                model.update_running_params("wrong_parameter", 1)

            with pytest.raises(ModelParamaterException):
                model.get_param("wrong_parameter")
        