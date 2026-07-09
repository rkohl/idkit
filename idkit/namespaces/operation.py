from enum import StrEnum, auto


class OperationNamespace(StrEnum):
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
    index = auto()
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


class Lifecycle(StrEnum):
    create = auto()
    delete = auto()
    initialize = auto()
    destroy = auto()


class CURD(StrEnum):
    read = auto()
    write = auto()
    update = auto()
    save = auto()
    patch = auto()
    delete = auto()


class Process(StrEnum):
    analyze = auto()
    process = auto()
    transform = auto()
    convert = auto()
    compile = auto()
    parse = auto()
    serialize = auto()
    deserialize = auto()


class Validation(StrEnum):
    validate = auto()
    verify = auto()
    authorize = auto()
    authenticate = auto()
    confirm = auto()


class Communication(StrEnum):
    send = auto()
    receive = auto()
    publish = auto()
    subscribe = auto()
    dispatch = auto()
    broadcast = auto()
    post = auto()


class Discovery(StrEnum):
    discover = auto()
    scan = auto()
    search = auto()
    index = auto()
    find = auto()


class Monitoring(StrEnum):
    monitor = auto()
    observe = auto()
    track = auto()
    watch = auto()


class Execution(StrEnum):
    execute = auto()
    run = auto()
    invoke = auto()
    trigger = auto()
    start = auto()
