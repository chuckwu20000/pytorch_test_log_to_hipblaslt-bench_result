# pytorch_test_log_to_hipblaslt-bench_result
Run test_torch.py on AMD GPU(MI300), if result fail, can through this python script to run hipblaslt-bench to see the atol, rtol 

## Require
`apt install hipblaslt-benchmarks`

## pytorch log
`export HIPBLASLT_LOG_MASK=0xFF`

`HIP_VISIBLE_DEVICES=0 PYTORCH_TESTING_DEVICE_ONLY_FOR="cuda" python -u test/test_torch.py -v -k test_cdi 2 > log.txt`

put this script with the log.txt
