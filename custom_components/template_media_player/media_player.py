from homeassistant.components.media_player import (
    ENTITY_ID_FORMAT,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.components.template.template_entity import TemplateEntity
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_ENTITY_ID,
    CONF_UNIQUE_ID,
)
from homeassistant.const import (
    Platform,
)
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
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import async_generate_entity_id
from .const import LOGGER

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


class TemplateMediaPlayer(TemplateEntity, *FEATURES, MediaPlayerEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        super().__init__(
            hass,
            config=config,
            unique_id=config.get(CONF_UNIQUE_ID),
        )

        if hass is not None:
            self.entity_id = async_generate_entity_id(
                ENTITY_ID_FORMAT, config.get(CONF_ENTITY_ID), hass=hass
            )

        self.hass = hass
        self._domain = DOMAIN

        self._attr_device_class = config.get(CONF_DEVICE_CLASS)
        self._available = True

        for feature in FEATURES:
            feature.__init__(self, hass, config)

    @property
    def friendly_name(self) -> str:
        return self._attr_name

    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return self._available

    @property
    def supported_features(self):
        support = MediaPlayerEntityFeature(0)
        for feature in FEATURES:
            if hasattr(feature, "supported_features"):
                support |= feature.supported_features.__get__(self)
        return support

    async def async_added_to_hass(self):
        for feature in FEATURES:
            if hasattr(feature, "_async_setup_templates"):
                try:
                    feature._async_setup_templates(self)
                except Exception as e:
                    LOGGER.error(
                        f"Error setting up templates for feature {feature.__name__}: {e}"
                    )

        await super().async_added_to_hass()

    async def async_update(self) -> None:
        if self._template_result_info is not None:
            await super().async_update()
