#!/usr/bin/env bash
set -euo pipefail

# Python version
PYTHON_BIN="python3.13-nogil"

# List of commands to benchmark.
# Each entry is a string that will be passed to `perf stat`.
# Replace these with your actual commands (the ones you ran with hyperfine before).
commands=(
    "./src/0_plain/plain.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/0_plain/improved.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/0_plain/itertools.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/0_plain/lib.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/1_multiprocessing/imap_unordered.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/1_multiprocessing/imap.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/1_multiprocessing/map_async.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/1_multiprocessing/map.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/2_multithreading/executor.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/2_multithreading/executor.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/2_multithreading/workers.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/2_multithreading/workers.py 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    # Compile and run ctypes:
    "./src/3_ctypes/invoke_hashcat.py ./src/3_ctypes/libhashcat.so 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    "./src/3_ctypes/invoke_hashcat.py ./src/3_ctypes/libhashcat_openmp.so 7e240de74fb1ed08fa08d38063f6a6a91462a815"
    # cpython:
    "./src/4_cpython/invoke_hashcat.py ./src/3_ctypes/libhashcat_openmp.so 7e240de74fb1ed08fa08d38063f6a6a91462a815"
)

gil=(
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    "PYTHON_GIL=0"
    "PYTHON_GIL=1"
    "PYTHON_GIL=0"
    # Compile and run ctypes:
    "PYTHON_GIL=1"
    "PYTHON_GIL=1"
    # cpython:
    "PYTHON_GIL=1"
)

# Output files
detail_results="runs_results.csv"

# Headers for the per-run detailed results:
echo "gil,command,run,cycles,instructions,task-clock,time_elapsed,user_time,sys_time" > "$detail_results"
runs=30

for idx in "${!commands[@]}"; do
    cmd="${commands[$idx]}"
    gil_var="${gil[$idx]}"

    echo "Running: $gil_var $cmd"
    for i in $(seq 1 $runs); do
        # Run perf stat with the GIL setting
        perf_output=$(eval "$gil_var perf stat -e cycles:u,instructions:u,task-clock:u --timeout 0 --log-fd 2 $PYTHON_BIN $cmd" 2>&1)


        # Extract values:
        # The lines look like:
        #         1078499331      cycles:u
        #         3537789566      instructions:u
        #               252.60 msec task-clock:u
        #       0.240214748 seconds time elapsed
        #       0.253503000 seconds user
        #       0.000000000 seconds sys
        #
        # We can use grep and awk to parse values.
        
        cycles=$(echo "$perf_output" | grep 'cycles:u' | awk '{print $1}')
        instructions=$(echo "$perf_output" | grep 'instructions:u' | awk '{print $1}')
        task_clock=$(echo "$perf_output" | grep 'task-clock:u' | awk '{print $1}')
        time_elapsed=$(echo "$perf_output" | grep 'seconds time elapsed' | awk '{print $1}')
        user_time=$(echo "$perf_output" | grep 'seconds user' | awk '{print $1}')
        sys_time=$(echo "$perf_output" | grep 'seconds sys' | awk '{print $1}')

        # Remove commas from numeric fields if any (perf sometimes uses them):
        cycles=$(echo $cycles | tr -d ',')
        instructions=$(echo $instructions | tr -d ',')
        task_clock=$(echo $task_clock | tr -d ',')
        time_elapsed=$(echo $time_elapsed | tr -d ',')
        user_time=$(echo $user_time | tr -d ',')
        sys_time=$(echo $sys_time | tr -d ',')

        # Append to detail CSV
        echo "$gil_var,$cmd,$i,$cycles,$instructions,$task_clock,$time_elapsed,$user_time,$sys_time" >> "$detail_results"
    done
done

echo "Benchmarking complete. Details in $detail_results."

