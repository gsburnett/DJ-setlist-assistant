This code generates a DJ set tracklist based on input given by the user
Note that specific, unlikely, combinations such as "chill techno" will likely result in issues
I recommend trying combos such as "chill house" or "bop electronic" or "rave techno"

HOW TO USE:
1. Create a csv file organizing your tracks with the following column headers:
                            track, artist, bpm, camelot, duration, genre, vibe
    1b. If you are unfamiliar with the camelot system, see https://mixedinkey.com/camelot-wheel/
    1c. If you'd like a template, download "track_csv_template.csv"
        I added rows for 100 tracks, but I recommend adding AT LEAST 500 for the code to run smoothly
        I also recommend editing this in google sheets or excel
2. Save this csv to your desired location
3. Insert the file path to your csv on line 114 and save ***
4. Run virtual_dj.py and follow the prompts in the tkinter window
