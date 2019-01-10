import argparse
import subprocess
import os



def main():
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    description = 'Run unit test in a docker environment'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--q', required=False, default='./app')

    args, extra_params = parser.parse_known_args()

    test_cmd = 'cd /src/tests; flask-philo test --q {}'.format(
        args.q)

    #test_cmd = 'ls /src'
    cmd = [
        'docker-compose',
        'run',
        '--rm',
        '--volume={}:/src'.format(os.path.join(os.getcwd(), '../')),
        'python',
        'sh',
        '-c',
        test_cmd
    ]
    subprocess.call(cmd)


if __name__ == '__main__':
    main()
