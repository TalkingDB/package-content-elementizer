from talkingdb.logger.console import logger, show_error


@show_error
def start_workers():
    logger.info("Workers started.")
