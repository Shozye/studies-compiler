echo "TEST: Fibbonaci 26. Oczekiwano 121393"
python run.py tests/test_data/test_gebala/example3.imp compiled.out -o output -v
echo 1 | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out
