from homeassistant.core import HomeAssistant
from homeassistant.components.media_player import (
    MediaPlayerEntityFeature,
    MediaType,
    MediaPlayerEntity,
    DOMAIN,
)
from homeassistant.components.media_player.browse_media import BrowseMedia
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity_component import EntityComponent

from ..config import (
    CONF_BROWSE_MEDIA_ENTITY,
)
from ..core import TemplateMediaPlayerBase


class FeatureBrowseMedia(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        self._attr_browse_media_entity = None
        self._template_browse_media_entity = config.get(CONF_BROWSE_MEDIA_ENTITY)

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        flags = MediaPlayerEntityFeature(0)

        if self._template_browse_media_entity is not None:
            flags |= MediaPlayerEntityFeature.BROWSE_MEDIA

        return flags

    def _async_setup_templates(self):
        if self._template_browse_media_entity is not None:
            self.add_template_attribute(
                "_attr_browse_media_entity", self._template_browse_media_entity
            )

    async def async_browse_media(
        self,
        media_content_type: MediaType | str | None = None,
        media_content_id: str | None = None,
    ) -> BrowseMedia:
        """Return a BrowseMedia instance."""
        entity_id = self._attr_browse_media_entity
        component: EntityComponent[MediaPlayerEntity] = self.hass.data[DOMAIN]
        if entity_id and (entity := component.get_entity(entity_id)):
            return await entity.async_browse_media(media_content_type, media_content_id)
        raise NotImplementedError
