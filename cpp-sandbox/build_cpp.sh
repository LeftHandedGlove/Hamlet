start_time="$(date -u +%s)"
SCRIPT_PATH="$( cd "$(dirname "#{BASH_SOURCE[0]}")" > /dev/null 2>&1 ; pwd -P )"
cd "${SCRIPT_PATH}"
mkdir -p build
cd build
cmake ..
make $1
end_time="$(date -u +%s)"
elapsed_time="$(($end_time-$start_time))"
echo "Total build time: ${elapsed_time}s."
