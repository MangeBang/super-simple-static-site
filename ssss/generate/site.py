def build(config):
    bake(config)


def watch(config):
    bake(config, reload_on_change=True)


def bake_context(config):
    for index, (context_ext, fn) in enumerate(config["contexts"]):
        (rules_ext, rules_fn) = config["rules"][index]
        baked_variables = fn(context_ext, config["searchpath"])
        rules_fn(rules_ext, baked_variables, config)


def bake(config=None, reload_on_change=False):
    if reload_on_change:
        print("Watching for changes...")

    else:
        print("Building...")

    bake_context(config)
