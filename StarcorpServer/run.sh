source .venv/bin/activate

export SECRET_KEY=$(cat secrets/secret_key)
export DATA_STORE="/home/pi/Starcorp/Game-Design-Capstone/StarcorpServer/data"

python starcorp/app.py