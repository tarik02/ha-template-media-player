from homeassistant.components.media_player import (
    ENTITY_ID_FORMAT,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.template.template_entity import TemplateEntity
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_ENTITY_ID,
    CONF_UNIQUE_ID,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import async_generate_entity_id

from .features import (
    FeatureState,
    FeatureVolume,
    FeatureControls,
    FeatureMedia,
    FeaturePosition,
    FeatureRepeat,
    FeatureShuffle,
    FeatureBrowseMedia,
    FeaturePlayMedia,
)
from .const import LOGGER

from .config import PLATFORM_SCHEMA

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


class TemplateMediaPlayer(TemplateEntity, *FEATURES, MediaPlayerEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        super().__init__(
            hass,
            config=config,
            fallback_name=config.get(CONF_ENTITY_ID),
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
