source .venv/bin/activate


pushd starcorp
while getopts "id" arg; do
  case ${arg} in
    i)
        echo "Initializing database from config!"
        python db_init.py
      ;;
    d)
        echo "Dumping database config"
        python -c "from database.static import generate_config; generate_config()"
    ;;
  esac
done
popd