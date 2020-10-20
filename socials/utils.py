import re


def parse_to_tags(text):
    # https://stackoverflow.com/a/20614981/1029469
    tags = [re.sub(r"(\W+)$", "", j) for j in set([i for i in text.split() if i.startswith("#")])]
    for index, tag in enumerate(tags):
        tags[index] = tag.replace('#', '')
    return tags


def check_settings(prefix, conf, settings):
    for setting in dir(conf):
        # bad test if it is a setting!
        if setting == setting.upper():
            # old style
            global_setting_name = '{}_{}'.format(prefix, setting)
            value = getattr(settings, global_setting_name, None)
            if value:
                setattr(conf, setting, value)


def parse_to_tags_naive(text):
    # dont use!
    splitted = str(text).split(' #')
    if text.startswith('#'):
        splitted[0] = splitted[0][1:]
    else:
        del(splitted[0])
    tags = []
    for split in splitted:
        tag_split = split.split(' ')
        tags.append(tag_split[0])
    return tags
