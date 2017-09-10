all: install chromesetup

install:
	pip3 install -r requirements.txt -t lib

chromesetup:
	mkdir bin
	cd bin && wget https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip
	cd bin && unzip chromedriver_linux64.zip
	cd bin rm chromedriver_linux64.zip

clean:
	rm -rf lib bin

run:
	PATH=${PATH}:$(PWD)/bin python3 spider.py 2>&1 | tee terminal.output
