import argparse
import glob
import time
import os

time = time.strftime("%Y%m%d", time.localtime())
outputdir = os.path.join("non-incremental", "QF_SLIA", f"{time}-denghang")
os.makedirs(outputdir, exist_ok=True)

def to_consistent_file(filename:str): 
    lines = []
    with open(filename, "r") as f:
      lines = f.readlines()
    outputfile = os.path.join(outputdir, os.path.basename(filename))
    with open(outputfile, "w") as f:
      header =  f"""
(set-info :smt-lib-version 2.6)
(set-logic QF_SLIA)
(set-info :source |
Generated by: Denghang Hu,
Generated on: {time},
Application: Evaluate string solvers
Description: The instance consists of:
(1) a regular membership predicate from the real world
(2) a regular membership predicate to sanitize danger letters in javascript such as <,>,&,",'
(3) a lower bound for string length
Target solver: Ostrich, Z3str3, CVC5
|)
(set-info :license "https://creativecommons.org/licenses/by/4.0/")
(set-info :category "industrial")
(set-info :status unknown)
        """
      f.write(header)
      for line in lines:
        if not ("set-info" in line and "set-logic" in line and "exit" in line):
            f.write(line)
      f.write("(exit)")
        
def to_consistent_dir(dirname:str):
    for filename in glob.glob(dirname + "/**/*.smt2", recursive=True):
        to_consistent_file(filename)

# parse arguments
parser = argparse.ArgumentParser(
    prog=__file__, description="Let the submitied smt2 files to be consistent with the instructions at https://github.com/SMT-LIB/benchmark-submission"
)
parser.add_argument("inputdir")


if __name__ == "__main__":
    args = parser.parse_args()
    to_consistent_dir(args.inputdir)