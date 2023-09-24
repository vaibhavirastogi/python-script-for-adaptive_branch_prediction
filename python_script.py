from __future__ import division
import os
import sys
import re


ZSIM_DIR_PATTERN = "simsmall"

def find_simsmall_dirs(source):
    zsim_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if ZSIM_DIR_PATTERN in directory:
                path = os.path.join(root, directory)
                zsim_paths.append(path)
    return zsim_paths

def get_zsim_out_files(zsim_paths):
    zsim_files = []
    for path in zsim_paths:
        file_path = os.path.join(path, "zsim.out")
        if os.path.isfile(file_path):
            zsim_files.append(file_path)
    return zsim_files

def read_zsim_out(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    return content

def read_all_zsim_out_files(zsim_out_files):
    all_contents = {}
    for file_paths in zsim_out_files:
        all_contents[file_paths] = read_zsim_out(file_paths)
    return all_contents

def parse_data_from_zsim_out(all_contents):
    parsed_data = {}
    pattern = re.compile(r"westmere-(\d+):.*?cycles: (\d+).*?cCycles: (\d+).*?instrs: (\d+).*?mispredBranches: (\d+).*?condBranches: (\d+)", re.DOTALL)
    for file_path, content in all_contents.items():
        content_as_string = ''.join(content)
        matches = pattern.findall(content_as_string)
        if matches:
            parsed_data[file_path] = []
            for match in matches:
                westmere = int(match[0])
                cycles = int(match[1])
                cCycles = int(match[2])
                instrs = int(match[3])
                mispredBranches = int(match[4])
                condBranches = int(match[5])
                parsed_data[file_path].append({
                    "westmere": westmere,
                    "cycles": cycles,
                    "cCycles": cCycles,
                    "instrs": instrs,
                    "mispredBranches": mispredBranches,
                    "condBranches": condBranches
                })
    return parsed_data

def calc_performance(parsed_data):
    for file_path, data_list in parsed_data.items():
        for data in data_list:
            Name = file_path
            Westmere = data['westmere']
            CPI = float(data['cycles'] + data['cCycles']) / data['instrs']
            mispredictionRate = float(data['mispredBranches']) / data['condBranches']
	
	    #print("CPI: {}, MispredRate: {}\n".format(CPI, mispredictionRate))
		#Formatting output string
            output_string = (
                "Name: {}\n"
                "Westmere: {}\n"
                "CPI: {:.6f}\n"
                "MispredRate: {:.6f}\n\n"
            ).format(Name, Westmere, CPI, mispredictionRate)
            
            #Print to console
            print(output_string)
		

            with open("parsed_results", 'a') as file:
                file.write("{}\n".format(Name))
                file.write("Westmere: {}\n".format(Westmere))
                file.write("CPI: {}\n".format(CPI))
                file.write("MispredRate: {}\n".format(mispredictionRate))
                file.write("\n")


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    paths = find_simsmall_dirs(source_path)
    zsim_out_files = get_zsim_out_files(paths)
    all_contents = read_all_zsim_out_files(zsim_out_files)
    parsed_data = parse_data_from_zsim_out(all_contents)
#    print("printing parsed data")
#    print(parsed_data)
    calc_performance(parsed_data)

if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only")

    source, target = args[1:]
    #print(source)
    #print(target)
    main(source, target)

