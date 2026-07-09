from enum import StrEnum, auto


class RoleNamespace(StrEnum):
    """
    A role describes what an identifier represents as a stable responsibility.

    Examples:
        analyzer
        runner
        ingester
        validator
        publisher

    Best used in identifiers:
        system::runtime-agent+analyzer
        service::data-resource+ingester
    """

    saver = auto()
    seeder = auto()
    synchronizer = auto()
    updater = auto()
    analyzer = auto()
    processor = auto()
    forwarder = auto()
    ingester = auto()
    extractor = auto()
    transformer = auto()
    executor = auto()
    validator = auto()
    controller = auto()
    runner = auto()
    user = auto()
    filterer = auto()
    requirer = auto()

    creator = auto()
    reader = auto()
    writer = auto()
    deleter = auto()
    loader = auto()
    parser = auto()
    serializer = auto()
    deserializer = auto()
    compiler = auto()
    converter = auto()

    publisher = auto()
    subscriber = auto()
    dispatcher = auto()
    broadcaster = auto()
    sender = auto()
    receiver = auto()
    handler = auto()
    listener = auto()

    monitor = auto()
    observer = auto()
    watcher = auto()
    tracker = auto()
    scanner = auto()
    searcher = auto()
    indexer = auto()
    discoverer = auto()

    authenticator = auto()
    authorizer = auto()
    verifier = auto()
    encryptor = auto()
    decryptor = auto()

    scheduler = auto()
    worker = auto()
    coordinator = auto()
    orchestrator = auto()
    adapter = auto()
    connector = auto()
    provider = auto()
    resolver = auto()
    router = auto()
    gateway = auto()
    proxy = auto()
    bridge = auto()
    session = auto()
