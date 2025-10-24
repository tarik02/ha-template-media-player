import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    CONF_NAME,
    CONF_ENTITY_ID,
    CONF_STATE,
    CONF_UNIQUE_ID,
    CONF_DEVICE_CLASS,
)
from homeassistant.components.template.const import (
    CONF_AVAILABILITY,
)
from homeassistant.components.media_player import (
    DEVICE_CLASSES_SCHEMA,
)

CONF_VOLUME = "volume"
CONF_IS_MUTED = "is_muted"
CONF_STEP_UP = "step_up"
CONF_STEP_DOWN = "step_down"
CONF_SET = "set"
CONF_MUTE = "mute"
CONF_CONTROLS = "controls"
CONF_PLAY = "play"
CONF_STOP = "stop"
CONF_PAUSE = "pause"
CONF_NEXT_TRACK = "next_track"
CONF_PREVIOUS_TRACK = "previous_track"
CONF_UPDATED_AT = "updated_at"
CONF_MEDIA = "media"
CONF_ALBUM_ARTIST = "album_artist"
CONF_ALBUM_NAME = "album_name"
CONF_ARTIST = "artist"
CONF_CHANNEL = "channel"
CONF_CONTENT_ID = "content_id"
CONF_CONTENT_TYPE = "content_type"
CONF_DURATION = "duration"
CONF_EPISODE = "episode"
CONF_IMAGE_HASH = "image_hash"
CONF_IMAGE_URL = "image_url"
CONF_PLAYLIST = "playlist"
CONF_POSITION = "position"
CONF_SEASON = "season"
CONF_SERIES_TITLE = "series_title"
CONF_TITLE = "title"
CONF_TRACK = "track"
CONF_REPEAT = "repeat"
CONF_SHUFFLE = "shuffle"
CONF_BROWSE_MEDIA_ENTITY = "browse_media_entity"
CONF_PLAY_MEDIA = "play_media"

PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME): cv.template,
        vol.Optional(CONF_ENTITY_ID): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
        vol.Optional(CONF_DEVICE_CLASS): DEVICE_CLASSES_SCHEMA,
        vol.Optional(CONF_AVAILABILITY): cv.template,
        vol.Required(CONF_STATE): cv.template,
        vol.Optional(CONF_VOLUME): vol.Schema(
            {
                vol.Optional(CONF_STATE): cv.template,
                vol.Optional(CONF_IS_MUTED): cv.template,
                vol.Optional(CONF_STEP_UP): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_STEP_DOWN): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_SET): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_MUTE): cv.SCRIPT_SCHEMA,
            }
        ),
        vol.Optional(CONF_CONTROLS): vol.Schema(
            {
                vol.Optional(CONF_PLAY): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_STOP): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_PAUSE): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_NEXT_TRACK): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_PREVIOUS_TRACK): cv.SCRIPT_SCHEMA,
            }
        ),
        vol.Optional(CONF_MEDIA): vol.Schema(
            {
                vol.Optional(CONF_ALBUM_ARTIST): cv.template,
                vol.Optional(CONF_ALBUM_NAME): cv.template,
                vol.Optional(CONF_ARTIST): cv.template,
                vol.Optional(CONF_CHANNEL): cv.template,
                vol.Optional(CONF_CONTENT_ID): cv.template,
                vol.Optional(CONF_CONTENT_TYPE): cv.template,
                vol.Optional(CONF_DURATION): cv.template,
                vol.Optional(CONF_EPISODE): cv.template,
                vol.Optional(CONF_IMAGE_HASH): cv.template,
                vol.Optional(CONF_IMAGE_URL): cv.template,
                vol.Optional(CONF_PLAYLIST): cv.template,
                vol.Optional(CONF_SEASON): cv.template,
                vol.Optional(CONF_SERIES_TITLE): cv.template,
                vol.Optional(CONF_TITLE): cv.template,
                vol.Optional(CONF_TRACK): cv.template,
            }
        ),
        vol.Optional(CONF_POSITION): vol.Schema(
            {
                vol.Optional(CONF_STATE): cv.template,
                vol.Optional(CONF_UPDATED_AT): cv.template,
                vol.Optional(CONF_SET): cv.SCRIPT_SCHEMA,
            }
        ),
        vol.Optional(CONF_REPEAT): vol.Schema(
            {
                vol.Optional(CONF_STATE): cv.template,
                vol.Optional(CONF_SET): cv.SCRIPT_SCHEMA,
            }
        ),
        vol.Optional(CONF_SHUFFLE): vol.Schema(
            {
                vol.Optional(CONF_STATE): cv.template,
                vol.Optional(CONF_SET): cv.SCRIPT_SCHEMA,
            }
        ),
        vol.Optional(CONF_BROWSE_MEDIA_ENTITY): cv.template,
        vol.Optional(CONF_PLAY_MEDIA): cv.SCRIPT_SCHEMA,
    }
)
