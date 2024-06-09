import atexit
import os
import subprocess

from django.core.management.commands.runserver import Command as RunServerCmd


def watchman_static_handler():
    build_proc = subprocess.Popen(
        ["yarn", "build"],
    )
    build_proc.wait()
    return subprocess.Popen(
        [
            'watchman-make',
            '-p',
            'frontend/**/*',
            'esbuild.config.mjs',
            '-r',
            'yarn build',
        ],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

class Command(RunServerCmd):
    def handle(self, *args, **options):
        if not os.environ.get('RUN_MAIN'):
            build_static_proc = watchman_static_handler()

            atexit.register(build_static_proc.terminate)

        super().handle(*args, **options)
