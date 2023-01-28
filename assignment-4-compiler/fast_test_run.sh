
echo "TEST: Rozklad na czynniki pierwsze"
python run.py tests/test_data/test_gebala/program2.imp compiled.out -o output
echo 12345678903 | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out

echo "TEST: Kombinacje"
python run.py tests/test_data/test_gebala/example4.imp compiled.out -o output
echo "20 9" | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out

echo "TEST: Fibbonaci 26"
python run.py tests/test_data/test_gebala/example3.imp compiled.out -o output
echo 1 | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out

echo "TEST: GCD 4 liczb"
python run.py tests/test_data/test_gebala/program1.imp compiled.out -o output
echo "3814532926 1065023079 3875997978 1438730637" | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out

echo "TEST: Krzywa Eliptyczna"
python run.py tests/test_data/test_slowik/test4b.imp compiled.out -o output
echo "71 70 5 7 32 17" | ./vms/vm-original/maszyna-wirtualna-cln output/compiled.out

