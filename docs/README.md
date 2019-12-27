# Documentation README
Check out the docs at http://hyperledger-indy.readthedocs.io/projects/node

Learn more about how our docs are built and maintained at http://hyperledger-indy.readthedocs.io/en/latest/docs.html

This `docs/` directory should contain all of the documents associated with the repository, with the exception of README files that describe technical details with the directories of code. 

The `docs/source/` directory contains all of the documentation that is built and hosted on readthedocs. Based on the maintainer's discretion, some docs may not be necessary to build on readthedocs, and can exist within the `docs/` directory but outside of the `source/` directory. 

블라블라


## Ubuntu 퀵셋업


1. 깃 클론
```
git clone https://github.com/hyperledger/indy-node.git
```


2. 퀙셋업 
```
cd ./dev-setup/ubuntu
./setup-dev-python.sh
```

3. 버추얼 영역 wrapping
```
source ~/.bashrc
```

4. 의존성 추가 (libindy, libindy-crypto, libsodium)
```
setup-dev-depend-ubuntu16.sh
```


5. indy-plenum 과 indy-node 포크하기

indy-node와 동일폴더 경로로 이동

6. 명령어 실행. indy-plenum and indy-node projects 클론

./init-dev-project.sh <github-name> <new-virtualenv-name>


8. Activate new virtualenv workon <new-virtualenv-namdfdfd



9. [Optionally] Install Pycharm
10. [Optionally] Open and configure projects in Pycharm:
◦ Open both indy-plenum and indy-node in one window
◦ Go to File -> Settings
◦ Configure Project Interpreter to use just created virtualenv
▪ Go to Project: <name> -> Project Interpreter
▪ You’ll see indy-plenum and indy-node projects on the right side tab. For each of them:
• Click on the project just beside “Project Interpreter” drop down, you’ll see one setting icon, click on it.
• Select “Add Local”
• Select existing virtualenv path as below: 
◦ Configure Project Dependency
▪ Go to Project: <name> -> Project Dependencies
▪ Mark each project to be dependent on another one
◦ Configure pytest
▪ Go to Configure Tools -> Python Integrated tools
▪ You’ll see indy-plenum and indy-node projects on the right side tab. For each of them:
• Select Py.test from the ‘Default test runner’
◦ Press Apply


To add a new file to a subfolder, simply update the subfolder's `index.rst` with the relative link to your file.

If you'd like to link to a file outside of the docs/ folder, you'll need to provide an external github link (this is by design, to keep our docs organized into a single folder)

## Building the docs on your machine

Here are the quick steps to achieve this on a local machine without depending on ReadTheDocs. Note: Instructions may differ depending on your OS.
Run these commands within the repository folder
```bash
cd docs/source # Be in this directory. Makefile sits there.
pip install -r requirements.txt
make html
```

This will generate all the html files in `docs/source/_build/html` which you can then browse locally in your browser. Every time you make a change to the documentation you will need to rerun `make html`.

## Additional Instructions
This section is to be used for repo maintainers to add additional documentation guidelines or instructions. 
**TODO: Build the respective code API's into the readthedocs website**

**TODO: Add table support for markdown files** 
* This link may help: https://github.com/ryanfox/sphinx-markdown-tables