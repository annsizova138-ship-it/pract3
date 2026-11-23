cd /d "%~dp0.."
if not exist output mkdir output
python src\assembler.py --source examples\vector_max_1.asm --output output\vector_max_1.bin
python src\interpreter.py --binary output\vector_max_1.bin --dump output\vector_max_1.csv --range 400 405
python src\assembler.py --source examples\vector_max_2.asm --output output\vector_max_2.bin
python src\interpreter.py --binary output\vector_max_2.bin --dump output\vector_max_2.csv --range 400 405
python src\assembler.py --source examples\vector_max_3.asm --output output\vector_max_3.bin
python src\interpreter.py --binary output\vector_max_3.bin --dump output\vector_max_3.csv --range 400 405
pause
