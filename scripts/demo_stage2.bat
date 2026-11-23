cd /d "%~dp0.."
if not exist output mkdir output
python src\assembler.py --source examples\spec_tests.asm --output output\spec_tests.bin --test
python src\assembler.py --source examples\copy_array.asm --output output\copy_array.bin
python src\assembler.py --source examples\error_command.asm --output output\x.bin
python src\assembler.py --source examples\spec_tests.asm --output no_such_dir\x.bin
pause
