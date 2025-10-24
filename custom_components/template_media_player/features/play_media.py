from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
    MediaType,
)
from homeassistant.helpers.script import Script
from homeassistant.helpers.typing import ConfigType

from ..config import (
    CONF_PLAY_MEDIA,
)
from ..core import TemplateMediaPlayerBase


class FeaturePlayMedia(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        self._script_play_media = None

        if hass is not None:
            if play_media := config.get(CONF_PLAY_MEDIA):
                self._script_play_media = Script(
                    hass, play_media, self.friendly_name, self._domain
                )

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if self._script_play_media is not None:
            flags |= MediaPlayerEntityFeature.PLAY_MEDIA

        return flags

    async def async_play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs: any
    ) -> None:
        """Play a piece of media."""
        data = {"media_type": media_type, "media_id": media_id}
        await self._script_play_media.async_run(data, context=self._context)
