from typing import Optional

from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerState,
)
from homeassistant.const import (
    CONF_STATE,
)
from homeassistant.helpers.typing import ConfigType

from ..core import TemplateMediaPlayerBase


class FeatureState(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        self._state = None
        self._template_state = config[CONF_STATE]

    def _async_setup_templates(self):
        self.add_template_attribute(
            "_state", self._template_state, none_on_template_error=True
        )

    @property
    def state(self) -> Optional[str]:
        """Return the state of the player."""
        if self._state is None:
            return None
        elif self._state == "playing":
            return MediaPlayerState.PLAYING
        elif self._state == "paused":
            return MediaPlayerState.PAUSED
        elif self._state == "idle":
            return MediaPlayerState.IDLE
        elif self._state == "on":
            return MediaPlayerState.ON
        elif self._state == "off":
            return MediaPlayerState.OFF
        elif self._state == "standby":
            try:
                return MediaPlayerState.STANDBY
            except AttributeError:
                return MediaPlayerState.OFF
        elif self._state == "buffering":
            return MediaPlayerState.BUFFERING
        return MediaPlayerState.OFF
