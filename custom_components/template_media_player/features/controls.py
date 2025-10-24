from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
)
from homeassistant.helpers.script import Script
from homeassistant.helpers.typing import ConfigType

from ..config import (
    CONF_CONTROLS,
    CONF_PLAY,
    CONF_STOP,
    CONF_PAUSE,
    CONF_NEXT_TRACK,
    CONF_PREVIOUS_TRACK,
)
from ..core import TemplateMediaPlayerBase


class FeatureControls(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        controls_conf = config.get(CONF_CONTROLS, {})

        self._script_play = None
        self._script_stop = None
        self._script_pause = None
        self._script_next_track = None
        self._script_previous_track = None

        if hass is not None:
            if play := controls_conf.get(CONF_PLAY):
                self._script_play = Script(hass, play, self.friendly_name, self._domain)

            if stop := controls_conf.get(CONF_STOP):
                self._script_stop = Script(hass, stop, self.friendly_name, self._domain)

            if pause := controls_conf.get(CONF_PAUSE):
                self._script_pause = Script(
                    hass, pause, self.friendly_name, self._domain
                )

            if next_track := controls_conf.get(CONF_NEXT_TRACK):
                self._script_next_track = Script(
                    hass, next_track, self.friendly_name, self._domain
                )

            if previous_track := controls_conf.get(CONF_PREVIOUS_TRACK):
                self._script_previous_track = Script(
                    hass, previous_track, self.friendly_name, self._domain
                )

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if self._script_play is not None:
            flags |= MediaPlayerEntityFeature.PLAY
        if self._script_stop is not None:
            flags |= MediaPlayerEntityFeature.STOP
        if self._script_pause is not None:
            flags |= MediaPlayerEntityFeature.PAUSE
        if self._script_next_track is not None:
            flags |= MediaPlayerEntityFeature.NEXT_TRACK
        if self._script_previous_track is not None:
            flags |= MediaPlayerEntityFeature.PREVIOUS_TRACK

        return flags

    async def async_media_play(self) -> None:
        await self._script_play.async_run(context=self._context)

    async def async_media_stop(self) -> None:
        await self._script_stop.async_run(context=self._context)

    async def async_media_pause(self) -> None:
        await self._script_pause.async_run(context=self._context)

    async def async_media_next_track(self) -> None:
        await self._script_next_track.async_run(context=self._context)

    async def async_media_previous_track(self) -> None:
        await self._script_previous_track.async_run(context=self._context)
