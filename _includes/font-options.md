# Font Options for Your Website

You now have three font options in `assets/css/main.scss`. To switch between them:

## Current Active: Option 1 - Noto Sans Korean
- Best for: Korean language support, clean academic look
- Font size: 14px base (reduced from 16px default)
- Includes proper Korean character rendering

## Option 2 - Roboto (To Activate)
1. Comment out the Noto Sans section (lines 10-16)
2. Uncomment the Roboto section (lines 18-25)

## Option 3 - Mixed Fonts (To Activate)
1. Comment out Options 1 and 2
2. Uncomment the Mixed section (lines 27-34)
- Uses Roboto for English, Noto Sans KR for Korean

## How to Change Fonts

Edit `assets/css/main.scss` and:
1. Comment out current option by adding `/*` and `*/` around the section
2. Uncomment your preferred option by removing `/*` and `*/`
3. Save the file and restart Jekyll server

## Font Size Adjustments

Current settings (all reduced from defaults):
- Base font: 14px (was 16px)
- Small screens: 13px
- Extra small: 12px
- Page titles: 1.8em (was 2.2em)
- Body content: 0.95em

To make fonts even smaller, change the base font-size values in the CSS file.