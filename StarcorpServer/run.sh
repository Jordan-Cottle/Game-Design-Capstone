source .venv/bin/activate

export SECRET_KEY=$(cat secrets/secret_key)
export DATA_STORE="/home/pi/Starcorp/Game-Design-Capstone/StarcorpServer/data"

while getopts "c" arg; do
  case ${arg} in
    c)
      echo "Enabling console log handler!"
      export LOG_TO_CONSOLE='true'
      ;;
  esac
done

python starcorp/app.py