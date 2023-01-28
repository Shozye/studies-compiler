echo "TEST: Modulo. Oczekiwano 674106858"
python run.py tests/test_data/test_gebala/example5.imp compiled.out -o output -v
echo "1234567890 1234567890987654321 987654321" | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out
