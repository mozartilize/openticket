project(
    'openticket',
    version: '0.1',
    default_options: [
        'warning_level=3',
    ]
)

prefix = get_option('prefix')

buildtype = get_option('buildtype')
build_root = meson.global_build_root()

pymod = import('python')
python = pymod.find_installation('python3', required: true)

if buildtype == 'release'
    cmd = run_command('python', '-c', 'import importlib.metadata as im; print(im.version("build"))', check: true)
    python_build = cmd.stdout().strip()
    message('Found python-build version', python_build)
    build = custom_target(
        'build',
        command: [python, '-m', 'build', '..'],
        output: 'openticket-0.1.0-py3-none-any.whl',
    )
else
    if python.language_version() != '3.8'
        error('Python version 3.8 required, found ', python.language_version())
    endif
    watchman = find_program('watchman', native: true, required: true)

    cmd = run_command('bash', '-c', 'echo $VIRTUAL_ENV', check: true)
    virtualenv = cmd.stdout().strip()
    if virtualenv == ''
        message('Creating virtualenv at', build_root)
        cmd = run_command('python', '-m', 'venv', build_root, check: true)
    else
        message('virtualenv found')
    endif

    pip = find_program(build_root / 'bin/pip')
    build = custom_target(
        'build',
        command: [pip, 'install', '-e', '..[dev]'],
        output: 'openticket',
    )
endif
