from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
)
from homeassistant.const import (
    CONF_STATE,
    STATE_ON,
)
from homeassistant.helpers.script import Script
from homeassistant.helpers.typing import ConfigType
from typing import Optional

from ..config import (
    CONF_IS_MUTED,
    CONF_MUTE,
    CONF_SET,
    CONF_STEP_DOWN,
    CONF_STEP_UP,
    CONF_VOLUME,
)
from ..const import LOGGER
from ..core import TemplateMediaPlayerBase


class FeatureVolume(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        volume_conf = config.get(CONF_VOLUME, {})

        self._volume_level = None
        self._template_volume_level = volume_conf.get(CONF_STATE)

        self._is_muted = None
        self._template_is_muted = volume_conf.get(CONF_IS_MUTED)

        self._script_volume_step_up = None
        self._script_volume_step_down = None
        self._script_set_volume = None
        self._script_mute = None

        if hass is not None:
            if step_up := volume_conf.get(CONF_STEP_UP):
                self._script_volume_step_up = Script(
                    hass, step_up, self.friendly_name, self._domain
                )

            if step_down := volume_conf.get(CONF_STEP_DOWN):
                self._script_volume_step_down = Script(
                    hass, step_down, self.friendly_name, self._domain
                )

            if set_volume := volume_conf.get(CONF_SET):
                self._script_set_volume = Script(
                    hass, set_volume, self.friendly_name, self._domain
                )

            if mute := volume_conf.get(CONF_MUTE):
                self._script_mute = Script(hass, mute, self.friendly_name, self._domain)

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if (
            self._script_volume_step_up is not None
            or self._script_volume_step_down is not None
        ):
            flags |= MediaPlayerEntityFeature.VOLUME_STEP
        if self._script_set_volume is not None:
            flags |= MediaPlayerEntityFeature.VOLUME_SET
        if self._script_mute is not None:
            flags |= MediaPlayerEntityFeature.VOLUME_MUTE

        return flags

    def _async_setup_templates(self):
        if self._template_volume_level is not None:
            self.add_template_attribute("_volume_level", self._template_volume_level)
        if self._template_is_muted is not None:
            self.add_template_attribute("_is_muted", self._template_is_muted)

    @property
    def volume_level(self) -> Optional[float]:
        """Volume level of entity specified in attributes or active child."""
        if self._volume_level is None:
            return None
        try:
            return float(self._volume_level)
        except (TypeError, ValueError) as err:
            LOGGER.warning(
                "Error parsing volume level: %s, error: %s", self._volume_level, err
            )
            return None

    async def async_set_volume_level(self, volume: float) -> None:
        """Set the volume."""
        if self._template_volume_level is None:
            self._volume_level = volume
            self.async_write_ha_state()
        await self._script_set_volume.async_run(
            {"volume_level": volume},
            context=self._context,
        )

    async def async_volume_up(self) -> None:
        """Fire the volume up action."""
        await self._script_volume_step_up.async_run(context=self._context)

    async def async_volume_down(self) -> None:
        """Fire the volume down action."""
        await self._script_volume_step_down.async_run(context=self._context)

    @property
    def is_volume_muted(self):
        """Boolean if volume is muted."""
        return self._is_muted in [True, STATE_ON]

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        await self._script_mute.async_run({"mute": mute}, context=self._context)
