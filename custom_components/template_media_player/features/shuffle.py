from homeassistant.core import HomeAssistant, callback
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
)
from homeassistant.const import (
    CONF_STATE,
    STATE_ON,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.script import Script
from homeassistant.helpers.typing import ConfigType
from typing import Optional

from ..config import (
    CONF_SET,
    CONF_SHUFFLE,
)
from ..const import LOGGER
from ..core import TemplateMediaPlayerBase


class FeatureShuffle(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        shuffle_conf = config.get(CONF_SHUFFLE, {})

        self._template_shuffle = shuffle_conf.get(CONF_STATE)

        self._script_shuffle_set = None
        if hass is not None:
            if shuffle_set := shuffle_conf.get(CONF_SET):
                self._script_shuffle_set = Script(
                    hass, shuffle_set, self.friendly_name, self._domain
                )

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if self._script_shuffle_set is not None:
            flags |= MediaPlayerEntityFeature.SHUFFLE_SET

        return flags

    def _async_setup_templates(self):
        if self._template_shuffle is not None:
            self.add_template_attribute(
                "_attr_shuffle",
                self._template_shuffle,
                on_update=self._on_shuffle_changed,
            )

    @callback
    def _on_shuffle_changed(self, value: Optional[str | TemplateError]):
        if isinstance(value, TemplateError):
            LOGGER.warning("Error in shuffle template: %s", value)
            return
        self._attr_shuffle = value in [True, "true", STATE_ON]

    async def async_set_shuffle(self, shuffle: bool) -> None:
        await self._script_shuffle_set.async_run(
            {"shuffle": shuffle}, context=self._context
        )
