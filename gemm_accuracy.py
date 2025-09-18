import subprocess

SPACE = "*************************"

# Store each test's gemm problem
hipblaslt_commands = []
problem_idx = 1

# May use argparse for flexibility
log_path = "./log.txt"
bench_result_path = "./fail_case_accuracy.txt"
with open(bench_result_path, 'w') as file:
    # Clean output file first
    file.write("")

# Fetch log
line_list = []
with open(log_path, 'r') as log:
    for log_line in log:
        line = log_line.strip()
        line_list.append(line)

# Split each line in log into word list
for line in line_list:
    word_list = line.split(" ")
    if (len(word_list) > 0):
        # Encount hipblaslt-bench command
        if (word_list[0] == "hipblaslt-bench"):
            line = f"{line} --verify"
            hipblaslt_commands.append(line)
        # Encount gemm problem finish with status "ok"
        if (word_list[0] == "ok" or word_list[len(word_list) - 1] == "ok"):
            # No need to run hipblaslt-bench
            print(SPACE)
            print(f"Problem #{problem_idx} status: ok")
            hipblaslt_commands = []
            problem_idx += 1
        # Encount gemm problem finish with status "FAIL"
        if (word_list[0] == "FAIL" and len(word_list) == 1):
            atol_rtol_list = []
            for hipblaslt_command in hipblaslt_commands:
                bench_result_output = subprocess.run(hipblaslt_command, shell = True, capture_output = True, text = True)
                bench_result = bench_result_output.stdout.strip()
                bench_result_split = bench_result.split("\n")
                problem_key = bench_result_split[-2]
                problem_key_list = problem_key.split(",")
                problem_val = bench_result_split[-1]
                problem_val_list = problem_val.split(",")
                if (len(problem_key_list) != len(problem_val_list)):
                    print(f"{len(problem_key_list)} != {len(problem_val_list)}")
                    raise Exception("hipblaslt-bench's problem #key and #val not match!")
                # Hardcode to fetch atol, rtol
                atol_rtol_list.append([problem_val_list[-2], problem_val_list[-1]])
            # Write into output file
            with open(bench_result_path, 'a') as file:
                file.write(f"{SPACE}\n")
                file.write(f"Problem #{problem_idx} status: FAIL\n")
                idx = 0
                for hipblaslt_command, atol_rtol in zip(hipblaslt_commands, atol_rtol_list):
                    file.write(f"GEMM #{idx}:\n")
                    file.write(f"    GEMM problem command: {hipblaslt_command}\n")
                    file.write(f"    atol: {atol_rtol[0]}, rtol: {atol_rtol[1]}\n")
                    idx = idx + 1
                file.write(f"{SPACE}\n\n")

            print(SPACE)
            print(f"Problem #{problem_idx} status: FAIL")
            print(f"Wrong accuracy can be seen in fail_case_accuracy.txt")
            hipblaslt_commands = []
            problem_idx += 1