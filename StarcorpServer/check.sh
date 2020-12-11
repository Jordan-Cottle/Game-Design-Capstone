pushd starcorp

black --check .
status=$?
if [[ $status -ne 0 ]]; then
    black --diff .
    exit $status
fi


status=0
for name in $(ls); do
    if [[ -d $name ]]; then
        pylint $name
        stat=$?
        if [[ $stat -ne 0 ]]; then
            status=$stat
        fi
    fi
done

popd

exit $status