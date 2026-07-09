from enum import auto

from .namespace import Namespace


class OperationNamespace(Namespace):
    """
    An operation describes what is being performed.

    Operations are better for events, logs, tasks, states, and commands,
    rather than stable object identity.
    """

    save = auto()
    seed = auto()
    sync = auto()
    update = auto()
    analyze = auto()
    process = auto()
    forward = auto()
    ingest = auto()
    extract = auto()
    transform = auto()
    execute = auto()
    validate = auto()
    control = auto()
    run = auto()
    use = auto()
    filter = auto()
    require = auto()
    create = auto()
    read = auto()
    write = auto()
    delete = auto()
    load = auto()
    parse = auto()
    serialize = auto()
    deserialize = auto()
    compile = auto()
    convert = auto()
    publish = auto()
    subscribe = auto()
    dispatch = auto()
    broadcast = auto()
    send = auto()
    receive = auto()
    handle = auto()
    listen = auto()
    monitor = auto()
    observe = auto()
    watch = auto()
    track = auto()
    scan = auto()
    search = auto()
    discover = auto()
    authenticate = auto()
    authorize = auto()
    verify = auto()
    encrypt = auto()
    decrypt = auto()
    schedule = auto()
    coordinate = auto()
    orchestrate = auto()
    adapt = auto()
    connect = auto()
    provide = auto()
    resolve = auto()
    route = auto()


class Lifecycle(Namespace):
    create = auto()
    delete = auto()
    initialize = auto()
    destroy = auto()


class CURD(Namespace):
    read = auto()
    write = auto()
    update = auto()
    save = auto()
    patch = auto()
    delete = auto()


class Process(Namespace):
    analyze = auto()
    process = auto()
    transform = auto()
    convert = auto()
    compile = auto()
    parse = auto()
    serialize = auto()
    deserialize = auto()


class Validation(Namespace):
    validate = auto()
    verify = auto()
    authorize = auto()
    authenticate = auto()
    confirm = auto()


class Communication(Namespace):
    send = auto()
    receive = auto()
    publish = auto()
    subscribe = auto()
    dispatch = auto()
    broadcast = auto()
    post = auto()


class Discovery(Namespace):
    discover = auto()
    scan = auto()
    search = auto()


class Monitoring(Namespace):
    monitor = auto()
    observe = auto()
    track = auto()
    watch = auto()


class Execution(Namespace):
    execute = auto()
    run = auto()
    invoke = auto()
    trigger = auto()
    start = auto()
