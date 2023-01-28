echo "TEST: Krzywa Eliptyczna. Oczekiwano 43 21"
python run.py tests/test_data/test_slowik/test4b.imp compiled.out -o output -v
echo "71 70 5 7 32 17" | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out
