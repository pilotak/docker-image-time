# Docker image time
[![docker build](https://github.com/pilotak/docker-image-time/actions/workflows/build.yaml/badge.svg)](https://github.com/pilotak/docker-image-time/actions/workflows/build.yaml)

Overlay image with it's last modified time

```yaml
version: "3"
services:
  camera_time:
    container_name: camera_time
    restart: unless-stopped
    build: .
    environment:
      WATCH_PATH: '/watch_dir/test.jpg'
      SAVE_DIR: '/output'
    volumes:
      - my_local_dir:/watch_dir
      - my_local_dir/output:/output
      - /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:/font.ttf
      - /etc/localtime:/etc/localtime:ro
```

> You must provide watched path, output path and font volumes, and also timezone for proper time

### Environmental variables
Bellow are all available variables

| Variable | Description | Default value | |
| --- | --- | :---:| :---: |
| `WATCH_PATH` | Dir or exact file to watch | | ***required*** |
| `SAVE_DIR` | Output dir path, filename will be the same as source | | ***required*** |
| `FONT_SIZE` | Size of the font| 25 | *optional* |
| `FONT_COLOR` | Color of the font in HEX format | #FFFFFF | *optional* |
| `TEXT_OFFSET` | Text offset from the edge | 50 | *optional* |
| `TEXT_POSITION` | [top,bottom,center]-[left,right,center] | bottom-right | *optional* |

