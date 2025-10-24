from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
    RepeatMode,
)
from homeassistant.const import (
    CONF_STATE,
)
from homeassistant.helpers.script import Script
from homeassistant.helpers.typing import ConfigType

from ..config import (
    CONF_SET,
    CONF_REPEAT,
)
from ..core import TemplateMediaPlayerBase


class FeatureRepeat(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        repeat_conf = config.get(CONF_REPEAT, {})

        self._template_repeat = repeat_conf.get(CONF_STATE)

        self._script_repeat_set = None
        if hass is not None:
            if repeat_set := repeat_conf.get(CONF_SET):
                self._script_repeat_set = Script(
                    hass, repeat_set, self.friendly_name, self._domain
                )

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if self._script_repeat_set is not None:
            flags |= MediaPlayerEntityFeature.REPEAT_SET

        return flags

    def _async_setup_templates(self):
        if self._template_repeat is not None:
            self.add_template_attribute("_attr_repeat", self._template_repeat)

    async def async_set_repeat(self, repeat: RepeatMode) -> None:
        await self._script_repeat_set.async_run(
            {"repeat": repeat}, context=self._context
        )
