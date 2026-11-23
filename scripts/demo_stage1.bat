cd /d "%~dp0.."
if not exist output mkdir output
python src\assembler.py --source examples\spec_tests.asm --output output\spec_tests.bin --test
python src\assembler.py --source examples\spec_tests.asm --output output\spec_tests.bin
python src\assembler.py --source examples\error_command.asm --output output\x.bin
python src\assembler.py --source examples\error_range.asm --output output\x.bin
python src\assembler.py --source examples\no_such.asm --output output\x.bin
python src\assembler.py --source examples\spec_tests.asm
python src\assembler.py --help
pause
