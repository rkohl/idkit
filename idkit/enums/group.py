from enum import StrEnum, auto


class IdentifierGroup(StrEnum):
    """
    The `Group` defines the primary classification or architectural domain of the `identifier` in the first segment. It represents the highest level of organization (e.g., `system`, `service`, `manage`).

    Default namespace values used as the first segment of an identifier.

    Group — Where does it belong?
    Source — What is it?
    Component — Which part of it?
    Action — What does it do?
    """

    system = auto()
    service = auto()
    core = auto()
    utility = auto()
    library = auto()
    package = auto()
    module = auto()
    framework = auto()
    application = auto()
    platform = auto()
    runtime = auto()
    database = auto()
    storage = auto()
    cache = auto()
    network = auto()
    transport = auto()
    filesystem = auto()
    cloud = auto()
    cluster = auto()
    node = auto()
    host = auto()
    container = auto()
    source = auto()
    stream = auto()
    pipeline = auto()
    warehouse = auto()
    analytics = auto()
    reporting = auto()
    api = auto()
    web = auto()
    cli = auto()
    shell = auto()
    desktop = auto()
    mobile = auto()
    ui = auto()
    domain = auto()
    business = auto()
    user = auto()
    account = auto()
    tenant = auto()
    organization = auto()
    project = auto()
    workspace = auto()
    workflow = auto()
    scheduler = auto()
    worker = auto()
    job = auto()
    queue = auto()
    event = auto()
    message = auto()
    bot = auto()
    agent = auto()
    ai = auto()
    testing = auto()
    development = auto()
    staging = auto()
    production = auto()
    build = auto()
    deploy = auto()
    migration = auto()
    script = auto()


class Architecture(StrEnum):
    system = auto()
    service = auto()
    core = auto()
    utility = auto()
    library = auto()
    package = auto()
    module = auto()
    framework = auto()
    application = auto()
    platform = auto()
    runtime = auto()


class Infrastructure(StrEnum):
    database = auto()
    storage = auto()
    cache = auto()
    network = auto()
    transport = auto()
    filesystem = auto()
    cloud = auto()
    cluster = auto()
    node = auto()
    host = auto()
    container = auto()


class Data(StrEnum):
    source = auto()
    stream = auto()
    pipeline = auto()
    warehouse = auto()
    analytics = auto()
    reporting = auto()


class Interface(StrEnum):
    api = auto()
    web = auto()
    cli = auto()
    shell = auto()
    desktop = auto()
    mobile = auto()
    ui = auto()


class Business(StrEnum):
    domain = auto()
    business = auto()
    user = auto()
    account = auto()
    tenant = auto()
    organization = auto()
    project = auto()
    workspace = auto()


class Automation(StrEnum):
    workflow = auto()
    scheduler = auto()
    worker = auto()
    job = auto()
    queue = auto()
    event = auto()
    message = auto()
    bot = auto()
    agent = auto()
    ai = auto()


class Development(StrEnum):
    testing = auto()
    development = auto()
    staging = auto()
    production = auto()
    build = auto()
    deploy = auto()
    migration = auto()
    script = auto()
