# Device Profiles Registry

This registry defines device specifications for `/speckit.preview` device frame generation, safe area handling, and multi-device testing.

## Usage

```bash
# Preview with specific device
speckit preview --device iphone-14-pro

# Preview with multiple devices
speckit preview --device iphone-14-pro,pixel-8,ipad-pro

# Preview all devices in category
speckit preview --devices mobile
speckit preview --devices tablet
speckit preview --devices all
```

## Device Profiles

```yaml
device_profiles:
  # ═══════════════════════════════════════════════════════════════
  # APPLE iOS DEVICES
  # ═══════════════════════════════════════════════════════════════

  iphone_15_pro_max:
    name: "iPhone 15 Pro Max"
    category: mobile
    os: ios
    viewport:
      width: 430
      height: 932
    device_pixel_ratio: 3
    safe_areas:
      top: 59      # Dynamic Island
      bottom: 34   # Home Indicator
      left: 0
      right: 0
    has_notch: true
    notch_type: "dynamic_island"
    notch_dimensions:
      width: 126
      height: 37
    status_bar_height: 54
    home_indicator_height: 34
    corner_radius: 55
    bezel_width: 12
    touch_capable: true
    supports_haptics: true

  iphone_14_pro:
    name: "iPhone 14 Pro"
    category: mobile
    os: ios
    viewport:
      width: 393
      height: 852
    device_pixel_ratio: 3
    safe_areas:
      top: 59
      bottom: 34
      left: 0
      right: 0
    has_notch: true
    notch_type: "dynamic_island"
    notch_dimensions:
      width: 126
      height: 37
    status_bar_height: 54
    home_indicator_height: 34
    corner_radius: 47
    bezel_width: 12
    touch_capable: true
    supports_haptics: true

  iphone_14:
    name: "iPhone 14"
    category: mobile
    os: ios
    viewport:
      width: 390
      height: 844
    device_pixel_ratio: 3
    safe_areas:
      top: 47
      bottom: 34
      left: 0
      right: 0
    has_notch: true
    notch_type: "notch"
    notch_dimensions:
      width: 209
      height: 30
    status_bar_height: 44
    home_indicator_height: 34
    corner_radius: 47
    bezel_width: 12
    touch_capable: true
    supports_haptics: true

  iphone_se:
    name: "iPhone SE (3rd gen)"
    category: mobile
    os: ios
    viewport:
      width: 375
      height: 667
    device_pixel_ratio: 2
    safe_areas:
      top: 20
      bottom: 0
      left: 0
      right: 0
    has_notch: false
    has_home_button: true
    status_bar_height: 20
    corner_radius: 0
    bezel_width: 16
    touch_capable: true
    supports_haptics: true

  ipad_pro_12_9:
    name: "iPad Pro 12.9"
    category: tablet
    os: ipados
    viewport:
      width: 1024
      height: 1366
    device_pixel_ratio: 2
    safe_areas:
      top: 24
      bottom: 20
      left: 0
      right: 0
    has_notch: false
    status_bar_height: 24
    home_indicator_height: 20
    corner_radius: 18
    bezel_width: 24
    touch_capable: true
    supports_split_view: true
    supports_stage_manager: true
    supports_apple_pencil: true
    supports_keyboard: true

  ipad_pro_11:
    name: "iPad Pro 11"
    category: tablet
    os: ipados
    viewport:
      width: 834
      height: 1194
    device_pixel_ratio: 2
    safe_areas:
      top: 24
      bottom: 20
      left: 0
      right: 0
    has_notch: false
    status_bar_height: 24
    home_indicator_height: 20
    corner_radius: 18
    bezel_width: 18
    touch_capable: true
    supports_split_view: true
    supports_stage_manager: true
    supports_apple_pencil: true

  ipad_air:
    name: "iPad Air"
    category: tablet
    os: ipados
    viewport:
      width: 820
      height: 1180
    device_pixel_ratio: 2
    safe_areas:
      top: 24
      bottom: 20
      left: 0
      right: 0
    has_notch: false
    corner_radius: 18
    bezel_width: 18
    touch_capable: true
    supports_split_view: true

  # ═══════════════════════════════════════════════════════════════
  # ANDROID DEVICES
  # ═══════════════════════════════════════════════════════════════

  pixel_8_pro:
    name: "Google Pixel 8 Pro"
    category: mobile
    os: android
    viewport:
      width: 448
      height: 998
    device_pixel_ratio: 3
    safe_areas:
      top: 56
      bottom: 24
      left: 0
      right: 0
    has_notch: true
    notch_type: "punch_hole"
    notch_dimensions:
      width: 28
      height: 28
      position: "center"
    status_bar_height: 56
    navigation_bar_height: 24
    corner_radius: 48
    bezel_width: 10
    touch_capable: true
    supports_haptics: true

  pixel_8:
    name: "Google Pixel 8"
    category: mobile
    os: android
    viewport:
      width: 412
      height: 915
    device_pixel_ratio: 2.625
    safe_areas:
      top: 48
      bottom: 24
      left: 0
      right: 0
    has_notch: true
    notch_type: "punch_hole"
    notch_dimensions:
      width: 24
      height: 24
      position: "center"
    status_bar_height: 48
    navigation_bar_height: 24
    corner_radius: 40
    bezel_width: 10
    touch_capable: true
    supports_haptics: true

  samsung_s24_ultra:
    name: "Samsung Galaxy S24 Ultra"
    category: mobile
    os: android
    viewport:
      width: 480
      height: 1044
    device_pixel_ratio: 3.5
    safe_areas:
      top: 52
      bottom: 24
      left: 0
      right: 0
    has_notch: true
    notch_type: "punch_hole"
    notch_dimensions:
      width: 20
      height: 20
      position: "center"
    status_bar_height: 52
    navigation_bar_height: 24
    corner_radius: 38
    bezel_width: 8
    touch_capable: true
    supports_haptics: true
    supports_s_pen: true

  samsung_s24:
    name: "Samsung Galaxy S24"
    category: mobile
    os: android
    viewport:
      width: 360
      height: 780
    device_pixel_ratio: 3
    safe_areas:
      top: 44
      bottom: 24
      left: 0
      right: 0
    has_notch: true
    notch_type: "punch_hole"
    notch_dimensions:
      width: 18
      height: 18
      position: "center"
    status_bar_height: 44
    navigation_bar_height: 24
    corner_radius: 32
    bezel_width: 10
    touch_capable: true

  samsung_galaxy_tab_s9:
    name: "Samsung Galaxy Tab S9+"
    category: tablet
    os: android
    viewport:
      width: 960
      height: 1506
    device_pixel_ratio: 2.5
    safe_areas:
      top: 32
      bottom: 24
      left: 0
      right: 0
    has_notch: false
    status_bar_height: 32
    corner_radius: 20
    bezel_width: 16
    touch_capable: true
    supports_s_pen: true
    supports_dex: true

  # ═══════════════════════════════════════════════════════════════
  # DESKTOP / LAPTOP
  # ═══════════════════════════════════════════════════════════════

  macbook_pro_16:
    name: "MacBook Pro 16"
    category: desktop
    os: macos
    viewport:
      width: 1728
      height: 1117
    device_pixel_ratio: 2
    safe_areas:
      top: 0
      bottom: 0
      left: 0
      right: 0
    has_notch: true
    notch_type: "camera_notch"
    notch_dimensions:
      width: 160
      height: 32
    menu_bar_height: 32
    corner_radius: 10
    bezel_width: 16
    touch_capable: false
    has_touchbar: false
    has_keyboard: true
    has_trackpad: true

  macbook_pro_14:
    name: "MacBook Pro 14"
    category: desktop
    os: macos
    viewport:
      width: 1512
      height: 982
    device_pixel_ratio: 2
    safe_areas:
      top: 0
      bottom: 0
      left: 0
      right: 0
    has_notch: true
    notch_type: "camera_notch"
    notch_dimensions:
      width: 140
      height: 32
    menu_bar_height: 32
    corner_radius: 10
    bezel_width: 16
    touch_capable: false
    has_keyboard: true
    has_trackpad: true

  macbook_air_15:
    name: "MacBook Air 15"
    category: desktop
    os: macos
    viewport:
      width: 1710
      height: 1107
    device_pixel_ratio: 2
    safe_areas:
      top: 0
      bottom: 0
      left: 0
      right: 0
    has_notch: true
    notch_type: "camera_notch"
    corner_radius: 10
    bezel_width: 12
    touch_capable: false

  imac_24:
    name: "iMac 24"
    category: desktop
    os: macos
    viewport:
      width: 2240
      height: 1260
    device_pixel_ratio: 2
    safe_areas:
      top: 0
      bottom: 0
      left: 0
      right: 0
    has_notch: false
    menu_bar_height: 32
    corner_radius: 24
    bezel_width: 28
    chin_height: 60
    touch_capable: false

  # ═══════════════════════════════════════════════════════════════
  # WEARABLES
  # ═══════════════════════════════════════════════════════════════

  apple_watch_ultra_2:
    name: "Apple Watch Ultra 2"
    category: watch
    os: watchos
    viewport:
      width: 205
      height: 251
    device_pixel_ratio: 2
    safe_areas:
      top: 8
      bottom: 8
      left: 8
      right: 8
    has_notch: false
    corner_radius: 40
    bezel_width: 8
    touch_capable: true
    has_digital_crown: true
    has_action_button: true

  apple_watch_series_9:
    name: "Apple Watch Series 9 (45mm)"
    category: watch
    os: watchos
    viewport:
      width: 198
      height: 242
    device_pixel_ratio: 2
    safe_areas:
      top: 6
      bottom: 6
      left: 6
      right: 6
    has_notch: false
    corner_radius: 38
    bezel_width: 6
    touch_capable: true
    has_digital_crown: true

  galaxy_watch_6:
    name: "Samsung Galaxy Watch 6 (44mm)"
    category: watch
    os: wearos
    viewport:
      width: 192
      height: 192
    device_pixel_ratio: 2
    safe_areas:
      top: 4
      bottom: 4
      left: 4
      right: 4
    has_notch: false
    is_circular: true
    corner_radius: 96
    bezel_width: 6
    touch_capable: true
    has_rotating_bezel: false

# ═══════════════════════════════════════════════════════════════
# DEVICE CATEGORIES
# ═══════════════════════════════════════════════════════════════

device_categories:
  mobile:
    description: "Smartphones (iOS and Android)"
    devices:
      - iphone_15_pro_max
      - iphone_14_pro
      - iphone_14
      - iphone_se
      - pixel_8_pro
      - pixel_8
      - samsung_s24_ultra
      - samsung_s24

  tablet:
    description: "Tablets (iPadOS and Android)"
    devices:
      - ipad_pro_12_9
      - ipad_pro_11
      - ipad_air
      - samsung_galaxy_tab_s9

  desktop:
    description: "Desktop and laptop computers"
    devices:
      - macbook_pro_16
      - macbook_pro_14
      - macbook_air_15
      - imac_24

  watch:
    description: "Smartwatches"
    devices:
      - apple_watch_ultra_2
      - apple_watch_series_9
      - galaxy_watch_6

  all:
    description: "All available devices"
    devices: "*"  # Expands to all defined devices

# ═══════════════════════════════════════════════════════════════
# DEFAULT DEVICE SET
# ═══════════════════════════════════════════════════════════════

defaults:
  # Used when no --device flag is specified
  preview_devices:
    - iphone_14_pro    # Primary mobile
    - ipad_pro_11      # Primary tablet
    - macbook_pro_14   # Primary desktop

  # Responsive breakpoints for slider
  breakpoints:
    xs: 320
    sm: 640
    md: 768
    lg: 1024
    xl: 1280
    xxl: 1536

  # Screenshot viewports (legacy compatibility)
  viewports:
    mobile:
      width: 375
      height: 812
    tablet:
      width: 768
      height: 1024
    desktop:
      width: 1440
      height: 900

# ═══════════════════════════════════════════════════════════════
# FRAME ASSETS
# ═══════════════════════════════════════════════════════════════

frame_assets:
  base_path: ".preview/assets/device-frames/"

  generation_instructions: |
    Device frames are SVG templates with the following structure:

    ```svg
    <svg viewBox="0 0 {total_width} {total_height}" xmlns="http://www.w3.org/2000/svg">
      <!-- Device outer shell -->
      <rect class="device-shell"
            x="0" y="0"
            width="{total_width}" height="{total_height}"
            rx="{corner_radius + bezel_width}"
            fill="#1a1a1a"/>

      <!-- Screen bezel (slightly darker) -->
      <rect class="device-bezel"
            x="{bezel_width/2}" y="{bezel_width/2}"
            width="{total_width - bezel_width}"
            height="{total_height - bezel_width}"
            rx="{corner_radius}"
            fill="#0a0a0a"/>

      <!-- Screen area -->
      <foreignObject class="device-screen"
                     x="{bezel_width}" y="{bezel_width}"
                     width="{viewport.width}" height="{viewport.height}">
        <!-- Preview content injected here -->
      </foreignObject>

      <!-- Dynamic Island / Notch (if applicable) -->
      <g class="notch" transform="translate({center_x}, {bezel_width + 8})">
        <!-- Dynamic Island -->
        <rect x="-{notch.width/2}" y="0"
              width="{notch.width}" height="{notch.height}"
              rx="{notch.height/2}" fill="#000"/>
      </g>

      <!-- Status bar overlay -->
      <g class="status-bar">
        <text x="{bezel_width + 16}" y="{bezel_width + 20}"
              fill="#fff" font-size="14" font-family="-apple-system">
          9:41
        </text>
        <!-- Battery, signal, wifi icons -->
      </g>

      <!-- Home indicator (if applicable) -->
      <rect class="home-indicator"
            x="{center_x - 67}" y="{total_height - bezel_width - 15}"
            width="134" height="5"
            rx="2.5" fill="#fff" opacity="0.6"/>

      <!-- Side buttons (optional) -->
      <rect class="power-button"
            x="{total_width - 2}" y="100"
            width="3" height="60"
            rx="1" fill="#333"/>
      <rect class="volume-up"
            x="-1" y="100"
            width="3" height="40"
            rx="1" fill="#333"/>
      <rect class="volume-down"
            x="-1" y="150"
            width="3" height="40"
            rx="1" fill="#333"/>
    </svg>
    ```

  color_variants:
    - space_black: "#1a1a1a"
    - silver: "#e0e0e0"
    - gold: "#d4af37"
    - deep_purple: "#5e17eb"
    - blue: "#007aff"
```

## Status Bar Templates

```yaml
status_bar_templates:
  ios:
    time_format: "9:41"  # Apple's iconic time
    elements:
      - type: time
        position: left
        format: "h:mm"
      - type: signal
        position: right
        icon: signal_bars_4
      - type: wifi
        position: right
        icon: wifi_full
      - type: battery
        position: right
        icon: battery_100
        percentage: true

  android:
    time_format: "12:00"
    elements:
      - type: time
        position: left
        format: "HH:mm"
      - type: notifications
        position: left
        icons: []
      - type: signal
        position: right
        icon: signal_4g
      - type: wifi
        position: right
      - type: battery
        position: right
        percentage: true

  macos:
    menu_bar: true
    elements:
      - type: apple_menu
        position: left
        icon: apple_logo
      - type: app_menu
        position: left
        text: "App Name"
      - type: clock
        position: right
        format: "EEE MMM d h:mm a"
      - type: control_center
        position: right
      - type: wifi
        position: right
      - type: battery
        position: right
```

## Orientation Support

```yaml
orientation:
  portrait:
    description: "Default vertical orientation"
    swap_dimensions: false

  landscape:
    description: "Horizontal orientation (rotated 90°)"
    swap_dimensions: true
    safe_area_rotation:
      top: left
      right: top
      bottom: right
      left: bottom

  generation:
    both: true  # Generate both orientations by default
    primary: portrait
```

## Touch and Gesture Capabilities

```yaml
gesture_capabilities:
  mobile:
    tap: true
    double_tap: true
    long_press: true
    swipe: true
    pinch_zoom: true
    rotate: true
    pan: true
    force_touch: false  # Deprecated on most devices

  tablet:
    tap: true
    double_tap: true
    long_press: true
    swipe: true
    pinch_zoom: true
    rotate: true
    pan: true
    hover: true  # With Apple Pencil
    stylus: true

  desktop:
    click: true
    double_click: true
    right_click: true
    hover: true
    scroll: true
    drag: true
    keyboard: true

  watch:
    tap: true
    long_press: true
    swipe: true
    digital_crown: true  # Apple Watch
    force_touch: false   # Deprecated
```
