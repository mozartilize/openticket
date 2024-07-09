project(
    'openticket',
    version: '0.1',
    default_options: [
        'warning_level=3',
        'backend=none',
    ]
)

prefix = get_option('prefix')

buildtype = get_option('buildtype')
build_root = meson.global_build_root()
bindir = get_option('bindir')
message(bindir)

pymod = import('python')
python = pymod.find_installation('python3', required: true)
if python.language_version() != '3.8'
    error('Python version 3.8 required, found ', python.language_version())
endif

if buildtype == 'debug'
    watchman = find_program('watchman', native: true, required: true)

    cmd = run_command('bash', '-c', 'echo $VIRTUAL_ENV', check: true)
    virtualenv = cmd.stdout().strip()
    if virtualenv == ''
        message('Creating virtualenv at', build_root)
        cmd = run_command('python', '-m', 'venv', build_root, check: true)
    else
        message('virtualenv found')
    endif

else
    watchman = find_program('watchman', native: true, required: false)
endif
