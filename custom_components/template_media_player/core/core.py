from homeassistant.core import HomeAssistant
from abc import ABC, abstractmethod
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import (
    CONF_STATE_TEMPLATE,
)


class TemplateMediaPlayerBase(ABC):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        self._state = None
        self._template_state = config[CONF_STATE_TEMPLATE]

    @abstractmethod
    def _async_setup_templates(self):
        pass
