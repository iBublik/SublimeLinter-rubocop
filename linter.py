from SublimeLinter.lint import Linter


class RubyLinter(Linter):
    def context_sensitive_executable_path(self, cmd):
        # The default implementation will look for a user defined `executable`
        # setting.
        success, executable = super().context_sensitive_executable_path(cmd)
        if success:
            return True, executable

        settings = self.get_view_settings()
        gem_name = cmd[0]
        if settings.get('use_bundle_exec', False):
            return True, ['bundle', 'exec', gem_name]

        return True, gem_name  # Avoid testing if `gem_name` is on PATH


class Rubocop(RubyLinter):
    syntax = (
        'better rspec',
        'betterruby',
        'cucumber steps',
        'rspec',
        'ruby experimental',
        'ruby on rails',
        'ruby'
    )
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(:?(?P<warning>[RCW])|(?P<error>[EF])): '
        r'(?P<message>.+)'
    )

    cmd = ['rubocop', '--format', 'emacs', '--force-exclusion', '${args}']
    defaults = {
        '--stdin:': '${file_path:$folder}'
    }
