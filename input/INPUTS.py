from astropy import units as u
from poliastro.bodies import Earth
import numpy as np

FILE_TSV_num = 1

R = Earth.R.to(u.km).value
K = Earth.k.to(u.km**3 / u.s**2).value

FILE_TSV = "input/Debris_excel.tsv"
FILE_CSV = "input/Debris_excel.csv"
DECAYMENT_FILE = "output/decayments_data_file.txt"
MANOUVERS_FILE = "output/manouvers_log.txt"
RENDEZVOUS_DATA_PATH = 'output/rendezvous_' #proceeds in rendezvous_manouver
ITERATOR_OUTPUT_FILE = ("output/iterator_output_debris.txt","output/iterator_output_dv.txt")

DEBRIS_RENDEZVOUS_DATA = False
TOTAL_LOG = True
ITERATIONS_PROGRAM = False

if ITERATIONS_PROGRAM and TOTAL_LOG:
    ValueError("incoerence in logging")

COMPUTATIONAL_TIMER_PATH = "__main__" if not ITERATIONS_PROGRAM else "not_main"

PROGRAM_ITERATIONS = 100

ARBITRARY_THETA = 0.2