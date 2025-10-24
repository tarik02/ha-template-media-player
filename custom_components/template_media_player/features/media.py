from homeassistant.core import HomeAssistant
from ..config import (
    CONF_MEDIA,
    CONF_ALBUM_ARTIST,
    CONF_ALBUM_NAME,
    CONF_ARTIST,
    CONF_CHANNEL,
    CONF_CONTENT_ID,
    CONF_CONTENT_TYPE,
    CONF_DURATION,
    CONF_EPISODE,
    CONF_IMAGE_HASH,
    CONF_IMAGE_URL,
    CONF_PLAYLIST,
    CONF_SEASON,
    CONF_SERIES_TITLE,
    CONF_TITLE,
    CONF_TRACK,
)
from homeassistant.helpers.typing import ConfigType

from ..core import TemplateMediaPlayerBase


class FeatureMedia(TemplateMediaPlayerBase):
    def __init__(self, hass: HomeAssistant, config: ConfigType):
        self._attr_media_image_remotely_accessible = True

        media_config = config.get(CONF_MEDIA, {})

        self._template_album_artist = media_config.get(CONF_ALBUM_ARTIST)
        self._template_album_name = media_config.get(CONF_ALBUM_NAME)
        self._template_artist = media_config.get(CONF_ARTIST)
        self._template_channel = media_config.get(CONF_CHANNEL)
        self._template_content_id = media_config.get(CONF_CONTENT_ID)
        self._template_content_type = media_config.get(CONF_CONTENT_TYPE)
        self._template_duration = media_config.get(CONF_DURATION)
        self._template_episode = media_config.get(CONF_EPISODE)
        self._template_image_hash = media_config.get(CONF_IMAGE_HASH)
        self._template_image_url = media_config.get(CONF_IMAGE_URL)
        self._template_playlist = media_config.get(CONF_PLAYLIST)
        self._template_season = media_config.get(CONF_SEASON)
        self._template_series_title = media_config.get(CONF_SERIES_TITLE)
        self._template_title = media_config.get(CONF_TITLE)
        self._template_track = media_config.get(CONF_TRACK)

    def _async_setup_templates(self):
        if self._template_album_artist is not None:
            self.add_template_attribute(
                "_attr_media_album_artist", self._template_album_artist
            )
        if self._template_album_name is not None:
            self.add_template_attribute(
                "_attr_media_album_name", self._template_album_name
            )
        if self._template_artist is not None:
            self.add_template_attribute("_attr_media_artist", self._template_artist)
        if self._template_channel is not None:
            self.add_template_attribute("_attr_media_channel", self._template_channel)
        if self._template_content_id is not None:
            self.add_template_attribute(
                "_attr_media_content_id", self._template_content_id
            )
        if self._template_content_type is not None:
            self.add_template_attribute(
                "_attr_media_content_type", self._template_content_type
            )
        if self._template_duration is not None:
            self.add_template_attribute("_attr_media_duration", self._template_duration)
        if self._template_episode is not None:
            self.add_template_attribute("_attr_media_episode", self._template_episode)
        if self._template_image_hash is not None:
            self.add_template_attribute(
                "_attr_media_image_hash", self._template_image_hash
            )
        if self._template_image_url is not None:
            self.add_template_attribute(
                "_attr_media_image_url", self._template_image_url
            )
        if self._template_playlist is not None:
            self.add_template_attribute("_attr_media_playlist", self._template_playlist)
        if self._template_season is not None:
            self.add_template_attribute("_attr_media_season", self._template_season)
        if self._template_series_title is not None:
            self.add_template_attribute(
                "_attr_media_series_title", self._template_series_title
            )
        if self._template_title is not None:
            self.add_template_attribute("_attr_media_title", self._template_title)
        if self._template_track is not None:
            self.add_template_attribute("_attr_media_track", self._template_track)
