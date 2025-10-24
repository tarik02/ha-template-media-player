from homeassistant.const import (
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.reload import async_setup_reload_service
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .config import PLATFORM_SCHEMA
from .features import (
    FeatureBrowseMedia,
    FeatureControls,
    FeatureMedia,
    FeaturePlayMedia,
    FeaturePosition,
    FeatureRepeat,
    FeatureShuffle,
    FeatureState,
    FeatureVolume,
)
from .media_player import TemplateMediaPlayer

FEATURES = [
    FeatureState,
    FeatureVolume,
    FeatureControls,
    FeatureMedia,
    FeaturePosition,
    FeatureShuffle,
    FeatureRepeat,
    FeatureBrowseMedia,
    FeaturePlayMedia,
]

PLATFORM_SCHEMA = PLATFORM_SCHEMA
DOMAIN = "template_media_player"


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the custom universal media players."""
    await async_setup_reload_service(hass, DOMAIN, [Platform.MEDIA_PLAYER])

    player = TemplateMediaPlayer(hass, config)
    async_add_entities([player])
