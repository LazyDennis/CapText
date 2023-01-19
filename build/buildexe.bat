@cd ..
@cd Source
@pyinstaller -i Resource\icon256.ico -F -w --clean -n CapText --distpath ..\bin --workpath ..\temp main.py
@pause