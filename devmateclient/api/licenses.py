import logging

PATH = '/v2/licenses'
RESET_ACTIVATION_PATH = '/reset_first_activation'

log = logging.getLogger(__name__)


class LicensesApiMixin(object):
    def reset_first_activation(self, activation_key):
        """
        Reset first license activation by given activation key. Raise error if license with given key doesn't exist
        :param activation_key: `str` or `int` license activation key
        :return: `void`
        """
        log.debug('Reset first activation by activation key %s', activation_key)

        self._dm_post(path='{}/{}{}'.format(PATH, activation_key, RESET_ACTIVATION_PATH), with_meta=False)
