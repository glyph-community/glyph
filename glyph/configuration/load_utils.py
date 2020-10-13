import os

_a_random_default = 'why_would_anyone_want_this_value'
_default_values = {
    bool: False,
    str: '',
    int: 0,
    list: [],
}


def calculate_base_dir(abspath, depth):
    """Easily calculate the project root from the depth of this file
    """
    next_dir = os.path.dirname(abspath)
    if depth == 0:
        return next_dir
    return calculate_base_dir(next_dir, depth - 1)


def getenv(env_var, load_as, default=_a_random_default):
    """
    Get the environment variable 'env_var', try to parse it to the type 'load_as'
    If the variable does not exist and is not required, return the default
    """
    if not isinstance(env_var, str):
        raise ValueError('env_var must be supplied as a str to getenv')
    if not isinstance(load_as, type):
        raise ValueError('load_as must be supplied as a type to getenv')

    if default == _a_random_default:
        default = _default_values[load_as]

    def __not_implemented_conv(env_var, default):
        raise NotImplementedError(f'getenv cannot handle type {load_as} for {env_var}')

    allowed_types = {
        str: os.getenv,
        bool: lambda env_var, default: os.getenv(env_var, str(default)).lower() in ['1', 'yes', 'true'],
        int: lambda env_var, default: int(os.getenv(env_var, str(default))),
        list: __get_list_env,
    }
    return allowed_types.get(load_as, __not_implemented_conv)(env_var, default)


def __get_list_env(env_var, default):
    """Load an environment variable 'env_var' and if it doesn't exist, return 'default'
    """
    raw_value = os.getenv(env_var, '')
    if not raw_value:
        return default
    return list(filter(lambda x: x, raw_value.split(',')))
