from icons import extract_icon


source = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"

output = r"icons\chrome.png"


success = extract_icon(
    source,
    output
)


if success:
    print("Icon extracted successfully!")
else:
    print("Icon extraction failed.")