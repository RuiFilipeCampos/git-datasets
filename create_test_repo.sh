


cd src
export PYTHONPATH=$PYTHONPATH:'"$(pwd)"'
cd ..

mkdir test-rep
cp src/development.py test-rep/development.py
cd test-rep
git init
git add development.py
ABS_PATH="$(pwd)/development.py"


setup_hook() {
    hook_type="$1"
    echo '
#!/bin/sh
python '"$ABS_PATH"' --'"$hook_type"'
' > $hook_type

    chmod +x $hook_type
}

cd .git/hooks
setup_hook pre-commit
setup_hook post-commit
setup_hook post-checkout
