source .venv/bin/activate

export SECRET_KEY=$(cat secrets/secret_key)
export DATA_STORE="$(pwd)/data"
export CONFIG="$(pwd)/config.yaml"

while getopts "c" arg; do
  case ${arg} in
    c)
      echo "Enabling console log handler!"
      export LOG_TO_CONSOLE='true'
      ;;
  esac
done

pushd starcorp
python app.py
popd