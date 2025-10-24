from typing import Optional

from homeassistant.core import HomeAssistant, callback
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.script import (
    Script,
)
from homeassistant.util.dt import parse_datetime, now
from ..config import (
    CONF_POSITION,
    CONF_STATE,
    CONF_SET,
    CONF_UPDATED_AT,
)
from homeassistant.helpers.typing import ConfigType

from ..core import TemplateMediaPlayerBase
from ..const import LOGGER


class FeaturePosition(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        position_config = config.get(CONF_POSITION, {})

        self._template_position_state = position_config.get(CONF_STATE)
        self._template_position_updated_at = position_config.get(CONF_UPDATED_AT)

        self._script_position_set = None

        if hass is not None:
            if position_set := position_config.get(CONF_SET):
                self._script_position_set = Script(
                    hass, position_set, self.friendly_name, self._domain
                )

        self._position_last_update = None
        self._position_last_update_forced = None

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if self._script_position_set is not None:
            flags |= MediaPlayerEntityFeature.SEEK

        return flags

    def _async_setup_templates(self):
        if self._template_position_state is not None:
            self.add_template_attribute(
                "_attr_media_position",
                self._template_position_state,
                on_update=self._on_position_changed,
            )
        if self._template_position_updated_at is not None:
            self.add_template_attribute(
                "_attr_media_position_updated_at",
                self._template_position_updated_at,
                on_update=self._on_position_updated_at_changed,
            )

    @property
    def media_position_updated_at(self):
        return (
            self._position_last_update_forced
            or self._attr_media_position_updated_at
            or self._position_last_update
        )

    @callback
    def _on_position_changed(self, value: Optional[str | TemplateError]):
        if isinstance(value, TemplateError):
            LOGGER.warning("Error in position template: %s", value)
            return
        try:
            value = int(value)
        except Exception as e:
            LOGGER.error("Failed to parse position value: %s", e)
            value = None
        self._attr_media_position = value
        self._position_last_update = now()
        self._position_last_update_forced = None

    @callback
    def _on_position_updated_at_changed(self, value: Optional[str | TemplateError]):
        if isinstance(value, TemplateError):
            LOGGER.warning("Error in position_updated_at template: %s", value)
            return
        if value is None:
            self._attr_media_position_updated_at = None
            return
        try:
            self._attr_media_position_updated_at = parse_datetime(value)
        except Exception as e:
            LOGGER.error("Failed to parse updated_at value: %s", e)

    async def async_media_seek(self, position):
        """Send seek command."""
        self._position_last_update_forced = now()
        await self._script_position_set.async_run(
            {"position": position}, context=self._context
        )
