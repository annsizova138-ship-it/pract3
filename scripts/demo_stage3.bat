cd /d "%~dp0.."
if not exist output mkdir output
python src\assembler.py --source examples\copy_array.asm --output output\copy_array.bin
python src\interpreter.py --binary output\copy_array.bin --dump output\copy_array.csv --range 200 214
python src\interpreter.py --binary output\copy_array.bin --dump output\copy_array.csv --range 0xC8 0xD6
python src\interpreter.py --binary output\no_such.bin --dump output\x.csv --range 0 5
python src\interpreter.py --binary output\copy_array.bin --dump output\x.csv --range 10 5
python src\interpreter.py --help
pause
