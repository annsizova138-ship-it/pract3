cd /d "%~dp0.."
if not exist output mkdir output
python src\assembler.py --source examples\max_demo.asm --output output\max_demo.bin
python src\interpreter.py --binary output\max_demo.bin --dump output\max_demo.csv --range 300 313
python src\assembler.py --source examples\copy_array.asm --output output\copy_array.bin
python src\interpreter.py --binary output\copy_array.bin --dump output\copy_array.csv --range 200 214
pause
