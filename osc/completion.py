import json
import os
import urllib.parse

from . import conf as osc_conf
from . import core as osc_core

def _get_apiurl(parsed_args):
    """
    Return apiurl based on config file content and already parsed args.
    """
    osc_conf.get_config(
        override_conffile=getattr(parsed_args, "config", None),
        override_apiurl=getattr(parsed_args, "apiurl", None),
    )
    return osc_conf.config["apiurl"]


def _get_hostname(url):
    return urllib.parse.urlparse(url).netloc


def cache(name, max_age=86400):
    def decorator(func):
        def new_func(prefix, parsed_args, **kwargs):
            apiurl = _get_apiurl(parsed_args)
            apiurl_hostname = _get_hostname(apiurl)

            cache_dir = os.path.expanduser(f"~/.cache/osc/argcomplete/{apiurl_hostname}")
            try:
                os.makedirs(cache_dir)
            except FileExistsError:
                pass
            cache_path = os.path.join(cache_dir, name)

            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "r") as f:
                        result = json.load(f)
                        return result
                except json.JSONDecodeError:
                    pass

            result = [str(i) for i in func(prefix, parsed_args, **kwargs)]
            with open(cache_path, "w") as f:
                json.dump(result, f)
            return result

        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        return new_func

    return decorator


def _get_common_prefix(iterable):
    """
    Return the longest prefix all items in the iterable have in common.
    """
    iterable = sorted(iterable)

    result = ""
    if not iterable:
        return result

    first = iterable[0]
    last = iterable[-1]
    for letter_first, letter_last in zip(first, last):
        if letter_first != letter_last:
            break
        result += letter_first
    return result


def _abbreviate_projects(entries, prefix):
    """
    Abbreviate names of some rpojects to their namespace prefixes in order to cut down
    the number of suggested entries and make the completion easier to use.

    NOTE:
    The function normally returns multiple values to trigger further completion.
    Returning a single value means that the completion is over.
    """

    # filter out entries that do not match the prefix
    entries = [i for i in entries if i.startswith(prefix)]

    if not entries:
        return []

    # abbreviated (incomplete) entries that contain right amount of information for the current completion
    abbreviated_entries = set()

    # find the longest common prefix
    common_prefix = _get_common_prefix(entries)

    # we're iterating through a copy because we're removing entries
    for entry in entries.copy():
        head = common_prefix
        tail = entry[len(common_prefix):]

        if ":" not in tail:
            # keep entries that do not have any more namespaces
            continue

        # remove the entry, it's going to be replaced with the abbreviated form
        entries.remove(entry)

        # keep the entry up to the next ':'
        abbreviated_entry = head + tail.split(":")[0] + ":"
        abbreviated_entries.add(abbreviated_entry)

    entries += sorted(abbreviated_entries)
    return entries


def abbreviate_projects(func):
    def new_func(prefix, parsed_args, **kwargs):
        result = func(prefix, parsed_args, **kwargs)
        result = _abbreviate_projects(result, prefix)
        return result

    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    return new_func


@abbreviate_projects
@cache("projects.json")
def project(prefix, parsed_args, **kwargs):
    apiurl = _get_apiurl(parsed_args)
    result = osc_core.meta_get_project_list(apiurl)
    return result
