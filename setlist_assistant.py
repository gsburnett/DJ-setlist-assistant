###########################
## DJ SETLIST GENERATOR  ##
## Author: Grace Burnett ##
###########################

'''
ABOUT:
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
'''


# import needed libraries
import pandas as pd
import tkinter as tk


# add column to djTracks that has more general genres
def fill_general_genres(genre):
    if 'house' in genre:
        return 'house'
    elif 'electronic' in genre:
        return 'electronic'
    elif 'dance' in genre:
        return 'dance'
    elif 'techno' in genre:
        return 'techno'
    elif 'hip hop' or 'r&b' in genre:
        return 'hiphop'
    elif 'disco' in genre:
        return 'disco'
    else:
        return 'other'


# add column to djTracks that has more general vibes
def fill_general_vibe(vibe):
    if 'chill' in vibe:
        return 'chill'
    elif 'ambient' in vibe:
        return 'ambient'
    elif 'rave' in vibe:
        return 'rave'
    elif 'bop' in vibe or 'dance' in vibe:
        return 'bop'
    else:
        return 'other'


# add seconds column to djTracks
def fill_seconds(djTracks):
    minutes = djTracks['duration'].str.split(':').str[0].astype(int) * 60
    seconds = djTracks['duration'].str.split(':').str[1].astype(int)
    djTracks['seconds'] = minutes + seconds


# create new dataframe with all possible track options based on genre and vibe
def create_track_options(djTracks, genGenre, genVibe):
    bestTrackOptions = djTracks[(djTracks['genGenre'] == genGenre) | (djTracks['genVibe'] == genVibe)].copy()
    bestTrackOptions['bpm'] = pd.to_numeric(bestTrackOptions['bpm'])  # convert values in bpm column to ints
    return bestTrackOptions


# generate setlist
def generate_setlist(djTracks, genGenre, genVibe, duration, bestTrackOptions, camelotMatches):
    setlist = []  # initialize list to setlist tracks
    currentTrack = bestTrackOptions.sample(n=1).iloc[0] # randomly select starting track from bestTrackOptions
    setlist.append(f"** {currentTrack['track']} - {currentTrack['artist']} **")  # append track title to setlist
    usedTracks = [currentTrack['track']]  # keep track of what songs are already in setlist

    currentCamelot = currentTrack['camelot'] # initialize currentCamelot with the camelot of currentTrack
    durationCount = int(currentTrack['seconds']) # initialize durationCount with the seconds of currentTrack as an int

    while durationCount < duration: # loop until setlist is long enough
        genreVibeTracks = bestTrackOptions[  # create dataframe with songs that match the genre and vibe
            (bestTrackOptions['genGenre'] == genGenre) &
            (bestTrackOptions['genVibe'] == genVibe)]

        nextTracks = genreVibeTracks[ # create dataframe with songs that have appropriate bpm and camelot
            (genreVibeTracks['bpm'] >= currentTrack['bpm'] - 8) &
            (genreVibeTracks['bpm'] <= currentTrack['bpm'] + 8) &
            (genreVibeTracks['camelot'].isin(camelotMatches[currentCamelot]))]

        if len(nextTracks) == 0: # if no songs meet the bpm and camelot criteria in genreVibeTracks, select song that only matches the genre
            nextTracks = bestTrackOptions[bestTrackOptions['genGenre'] == genGenre]

        if len(nextTracks) == 0: # as a last resort, select a track that only matches the vibe
            nextTracks = bestTrackOptions[bestTrackOptions['genVibe'] == genVibe]

        if len(nextTracks) > 0: #once nextTracks contains tracks to choose from:
            addTrack = nextTracks.sample(n=1).iloc[0] #randomly select song from nextTracks

            if addTrack['track'] not in usedTracks:  # ensure track not already in setlist
                setlist.append(f"** {addTrack['track']} - {addTrack['artist']} **")  # append track ** title - artist ** to setlist
                usedTracks.append(addTrack['track'])  # add track to usedTracks list
                durationCount += int(addTrack['seconds']) # add the seconds of the track to durationCount
                currentTrack = addTrack # change the currentTrack to be the most recently added one
                currentCamelot = addTrack['camelot']  # update camelot to most recently added track
            else: # if the track is in usedTracks start new iteration of while loop
                continue

        else: # if absolutely no tracks are appropriate, break the while loop
            break

    return setlist


def main():
    # read in DJ tracks csv
    # *** ALTER THIS TO YOUR PERSONAL CSV FILE PATH ***
    djTracks = pd.read_csv('/Users/gracestar/Downloads/DJmusic.csv')

    # appropriate camelot matches for each camelot:
    camelotMatches = {'1A': ['1A', '1B', '2A', '12A', '2B', '12B'],
                      '1B': ['1B', '1A', '2B', '12B', '2A', '12A'],
                      '2A': ['2A', '2B', '1A', '3A', '3B', '1B'],
                      '2B': ['2B', '2A', '1B', '3B', '3A', '1A'],
                      '3A': ['3A', '3B', '2A', '4A', '4B', '2B'],
                      '3B': ['3B', '3A', '2B', '4B', '4A', '2A'],
                      '4A': ['4A', '4B', '3A', '5A', '5B', '3B'],
                      '4B': ['4B', '4A', '3B', '5B', '5A', '3A'],
                      '5A': ['5A', '5B', '4A', '6A', '6B', '4B'],
                      '5B': ['5B', '5A', '4B', '6B', '6A', '4A'],
                      '6A': ['6A', '6B', '5A', '7A', '7B', '5B'],
                      '6B': ['6B', '6A', '5B', '7B', '7A', '5A'],
                      '7A': ['7A', '7B', '6A', '8A', '8B', '6B'],
                      '7B': ['7B', '7A', '6B', '8B', '8A', '6A'],
                      '8A': ['8A', '8B', '7A', '9A', '9B', '7B'],
                      '8B': ['8B', '8A', '7B', '9B', '7A', '9A'],
                      '9A': ['9A', '9B', '8A', '10A', '8B', '10B'],
                      '9B': ['9B', '9A', '8B', '10B', '10A', '8A'],
                      '10A': ['10A', '10B', '9A', '11A', '11B', '9B'],
                      '10B': ['10B', '10A', '9B', '11B', '11A', '9A'],
                      '11A': ['11A', '11B', '10A', '12A', '12B', '10B'],
                      '11B': ['11B', '11A', '10B', '12B', '12A', '10A'],
                      '12A': ['12A', '12B', '11A', '1A', '1B', '11B'],
                      '12B': ['12B', '12A', '11B', '1B', '1A', '11A']
                      }

    ##  ========================= MODIFY DATAFRAME ============================ ##

    djTracks['genGenre'] = djTracks['genre'].apply(fill_general_genres)  # add general genre col

    djTracks['genVibe'] = djTracks['vibe'].apply(fill_general_vibe)  # add general vibe col

    fill_seconds(djTracks)  # add seconds col

    # generate setlist based on user input, incorporating tkinter GUI
    def generate_setlist_gui():
        genGenre = selectedGenre.get() #store genre chosen by user
        genVibe = selectedVibe.get() #store vibe chosen by user
        duration = selectedDuration.get() #store duration chosen by user
        durationSeconds = (duration * 60) + (duration * 4.8) #add extra time to account for song transitions
        bestTrackOptions = create_track_options(djTracks, genGenre, genVibe) #save output of create_track_options into var
        setlist = generate_setlist(djTracks, genGenre, genVibe, durationSeconds, bestTrackOptions, camelotMatches) #save output of generate_setlist into var
        setlistOutput.config(text="\n".join(setlist)) #update to show the setlist

    # create tkinter window
    window = tk.Tk()
    window.title("Setlist Generator")
    window.configure(bg="black")

    # create genre selection dropdown
    genreLabel = tk.Label(window, text="Select Genre:", bg="black", fg="green")
    genreLabel.grid(row=0, column=0, padx=10, pady=5)
    selectedGenre = tk.StringVar()
    genreDropdown = tk.OptionMenu(window, selectedGenre, "house", "electronic", "dance", "techno")
    genreDropdown.grid(row=0, column=1, padx=10, pady=5)

    # creat vibe selection dropdown
    vibeLabel = tk.Label(window, text="Select Vibe:", bg="black", fg="green")
    vibeLabel.grid(row=1, column=0, padx=10, pady=5)
    selectedVibe = tk.StringVar()
    vibeDropdown = tk.OptionMenu(window, selectedVibe, "chill", "bop", "rave", "ambient")
    vibeDropdown.grid(row=1, column=1, padx=10, pady=5)

    # create duration selection dropdown
    durationLabel = tk.Label(window, text="Select Duration (minutes):", bg="black", fg="green")
    durationLabel.grid(row=2, column=0, padx=10, pady=5)
    selectedDuration = tk.IntVar()
    durationDropdown = tk.OptionMenu(window, selectedDuration, 30, 45, 60)
    durationDropdown.grid(row=2, column=1, padx=10, pady=5)

    # create button to generate setlist by running generate_setlist_gui when clicked
    generateButton = tk.Button(window, text="Generate Setlist", command=generate_setlist_gui)
    generateButton.grid(row=3, column=0, columnspan=2, pady=10)

    # display setlist in window
    setlistOutput = tk.Label(window, text="[setlist TBD]", wraplength=400, bg="black", fg="green")
    setlistOutput.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")

    window.mainloop()


if __name__ == '__main__':
    main()

