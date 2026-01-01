# Template Media Player

Home Assistant integration that provides fully-featured media player based on YAML templates.

## Installation

### HACS (recommended)

The quickest way to install this integration is via [HACS][hacs-url] by clicking the button below:

[![Add to HACS via My Home Assistant][hacs-install-image]][hacs-install-url]

If it doesn't work, add the repository to HACS manually:

1. Visit HACS → Integrations → ... (in the top right) → Custom repositories
2. Click Add.
3. Paste `https://github.com/tarik02/ha-template-media-player` into the URL field
4. Chose Integration as a Category
5. Template Media Player will appear in the list of available integrations. Install it normally.

### Manual

1. Copy `custom_components/template_media_player` from this repository into your HA config directory, ending up with: `config/custom_components/template_media_player/…`
2. Restart Home Assistant.

## Configuration

Minimal example:

```yaml
media_player:
  - platform: template_media_player
    entity_id: my_custom_player
    state: >
      {{ states('sensor.my_player_state') }}
```

Extended example (MQTT-backed librespot): see [examples/librespot-mqtt.yaml](https://github.com/tarik02/ha-template-media-player/blob/master/examples/librespot-mqtt.yaml).

## License

The project is released under the MIT license. Read the [license](https://github.com/tarik02/ha-template-media-player/blob/master/LICENSE) for more information.

[hacs-url]: https://github.com/hacs/integration
[hacs-install-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=tarik02&repository=ha-template-media-player&category=integration
[hacs-install-image]: https://my.home-assistant.io/badges/hacs_repository.svg
