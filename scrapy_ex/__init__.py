from db_classes.saver import Saver
from proxy_manager import ProxyManager
import config as cfg
import my_log

main_logger = my_log.get_logger(__name__)
main_logger.info('program started')
saver = Saver()
proxy_manager = ProxyManager()
