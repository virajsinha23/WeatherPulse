from utils.logger import get_logger
logger = get_logger()

logger.info('weatherPulse pipeline started')
logger.warning('A sample warning message')
logger.error('a sample error message')

try:
    result = 10/0
except ZeroDivisionError:
    logger.exception('Sample Calculation Failed')
    