Module.register("MMM-SongNotification", {
    defaults: {
        updateInterval: 1000,
        apiUrl: "http://asus:5001/json",
    },

    start: function () {
        this.songData = null;
        this.currentNotification = null;
        this.notificationTimeout = null;
        this.getSongData();
        this.scheduleUpdate();
        this.removeInjectedCSS();
    },

    scheduleUpdate: function () {
        setInterval(() => {
            this.getSongData();
        }, this.config.updateInterval);
    },

    getSongData: function () {
        this.sendSocketNotification("GET_SONG_DATA", this.config.apiUrl);
    },

    socketNotificationReceived: function (notification, payload) {
        if (notification === "SONG_DATA") {
            this.processSongData(payload);
        }
    },

    processSongData: function (data) {
        let songFound = false;
        let validSongData = null;

        if (data && data.length > 0) {
            data.forEach(song => {
                var songTime = new Date(song.time);
                var currentTime = new Date();
                validSongData = song;
                songFound = true;

            });
        }

        if (songFound) {
            if (!this.songData || this.songData.id !== validSongData.id) {

                this.songData = validSongData;
                this.showNotification();
            }
        } else {
            this.removeNotification();
            this.songData = null;
        }
    },

    showNotification: function () {
        if (this.currentNotification) {
            this.removeNotification();
        }

        if (!this.songData) {
            return;
        }
    },
}); //end for now