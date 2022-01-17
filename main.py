from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


# Creating the root window
root = Tk()
root.title('BTNL - Boukler The New Loud - Alpha Version 0.0.1')
root.iconbitmap('C:/Users/chara/PycharmProjects/MusicPlayerNEW/images/app.ico')
root.geometry('500x400')

# initialize mixer
pygame.mixer.init()

#Grab song length time info
def play_time():
    #Check for double timing
    if stopped:
        return
    #Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000

    #Grab song title from playlist
    song = songs_list.get(ACTIVE)

    # add directory structure and mp3 to song title
    song = f'D:/IO/EOKH/Apallaktiki/Code/Tracks/{song}.mp3'

    # Load song with mutagen
    song_mut = MP3(song)
    global song_length
    #Get song length
    song_length = song_mut.info.length

    #Convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    #Increase current time by 1 sec
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}   of   {converted_song_length} ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):

        #slider hasn't moved
        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        #slider has been moved!
        # Update slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # Convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}   of   {converted_song_length} ')

        #Move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    #Update time
    status_bar.after(1000, play_time)

# add many songs to the playlist
def add_song():
    # a list of songs is returned
    song = filedialog.askopenfilename(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))

    # loop through everyitem in the list
    song = song.replace("D:/IO/EOKH/Apallaktiki/Code/Tracks/", "")
    song = song.replace(".mp3", "")

    #Add song to listbox
    songs_list.insert(END, song)

#Add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    #loop through song list and replace directory info and mp3
    for song in songs:
        song = song.replace("D:/IO/EOKH/Apallaktiki/Code/Tracks/", "")
        song = song.replace(".mp3", "")

        # Add song to listbox
        songs_list.insert(END, song)

#Play selected song
def play():

    #Set stopped variable to false so song can play
    global stopped
    stopped = False
    song = songs_list.get(ACTIVE)
    song = f'D:/IO/EOKH/Apallaktiki/Code/Tracks/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Call the play_time function to get song lenght
    play_time()

#Stop playing currrent song
global stopped
stopped = False
def stop():
    #Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #Stop song from playing
    pygame.mixer.music.stop()
    songs_list.selection_clear(ACTIVE)

    #Clear the status bar
    status_bar.config(text= '')

    #Set stop variable to true
    global stopped
    stopped = True

#Create global pause variable
global paused
paused = False

#Pause and Unpause current song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pause
        pygame.mixer.music.pause()
        paused = True

#Go to previous song
def prev():
    # Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # Get the current song tuple number
    next_song = songs_list.curselection()

    # Add one to the current song number
    next_song = next_song[0] - 1
    song = songs_list.get(next_song)

    # add directory structure and mp3 to song title
    song = f'D:/IO/EOKH/Apallaktiki/Code/Tracks/{song}.mp3'

    # load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist listbox
    songs_list.selection_clear(0, END)

    # Activate new song's bar
    songs_list.activate(next_song)

    # Set the active bar to next song
    songs_list.selection_set(next_song, last=None)

#Go to next song in the playlist
def next():
    # Reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    #Get the current song tuple number
    next_song = songs_list.curselection()

    #Add one to the current song number
    next_song = next_song[0]+1
    song = songs_list.get(next_song)

    #add directory structure and mp3 to song title
    song = f'D:/IO/EOKH/Apallaktiki/Code/Tracks/{song}.mp3'

    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Clear active bar in playlist listbox
    songs_list.selection_clear(0, END)

    #Activate new song's bar
    songs_list.activate(next_song)

    #Set the active bar to next song
    songs_list.selection_set(next_song, last=None)

#Delete a song from playlist
def delete_song():
    stop()
    #Delete selected song
    songs_list.delete(ANCHOR)
    # Stop music if it's playing
    pygame.mixer.music.stop()

#Delete All Songs from playlist
def delete_all_songs():
    stop()
    #Delete all songs
    songs_list.delete(0, END)
    #Stop music if it's playing
    pygame.mixer.music.stop()

#Create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())}  of {int(song_length)}')
    song = songs_list.get(ACTIVE)
    song = f'D:/IO/EOKH/Apallaktiki/Code/Tracks/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

#Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# create the listbox to contain songs
songs_list = Listbox(master_frame,  bg="black", fg="green", width=60, selectbackground="grey")
songs_list.grid(row=0, column=0)

#Define Player Control Button Images
back_button_img = PhotoImage(file='C:/Users/chara/PycharmProjects/MusicPlayerNEW/images/prev.png')
next_button_img = PhotoImage(file='C:/Users/chara/PycharmProjects/MusicPlayerNEW/images/forward.png')
play_button_img = PhotoImage(file='C:/Users/chara/PycharmProjects/MusicPlayerNEW/images/play.png')
pause_button_img = PhotoImage(file='C:/Users/chara/PycharmProjects/MusicPlayerNEW/images/pause.png')
stop_button_img = PhotoImage(file='C:/Users/chara/PycharmProjects/MusicPlayerNEW/images/stop.png')

#Create Player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

#Create volume label frame
volume_frame= LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#Create Player Control Buttons
back_button = Button(controls_frame, image=back_button_img, borderwidth=0, command=prev)
next_button = Button(controls_frame, image=next_button_img, borderwidth=0, command=next)
play_button = Button(controls_frame, image=play_button_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_button_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
next_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#Create a Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add One Song To Playlist', command=add_song)

#Add many songs to playlist
add_song_menu.add_command(label='Add Many Songs To Playlist', command=add_many_songs)

#Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_all_songs)

#Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Create Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row= 2, column=0, pady=10)

#Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

root.mainloop()
