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

        var wrapper = document.createElement("div");
        wrapper.className = "sn-wrapper";

        var pobudkaContainer = document.createElement("div");
        pobudkaContainer.className = "sn-pobudka-container";

        var pobudkaText = document.createElement("span");
        pobudkaText.className = "sn-pobudka-text";
        pobudkaText.innerHTML = "POBUDKA";

        var currentTime = document.createElement("span");
        currentTime.className = "sn-current-time";
        var date = new Date();
        currentTime.innerHTML = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        var bellIcon = document.createElement("i");
        bellIcon.className = "fas fa-bell sn-bell-icon";

        pobudkaContainer.appendChild(pobudkaText);
        pobudkaContainer.appendChild(currentTime);
        pobudkaContainer.appendChild(bellIcon);

        var notification = document.createElement("div");
        notification.className = "sn-notification";

        var imageContainer = document.createElement("div");
        imageContainer.className = "sn-image-container";

        var image = document.createElement("img");
        image.src = this.songData.image;
        imageContainer.appendChild(image);

        var infoContainer = document.createElement("div");
        infoContainer.className = "sn-info-container";

        var time = document.createElement("p");
        time.className = "sn-time";
        time.innerHTML = new Date().toLocaleTimeString();
        infoContainer.appendChild(time);

        var title = document.createElement("p");
        title.className = "sn-title";
        title.innerHTML = this.songData.title;
        infoContainer.appendChild(title);

        var author = document.createElement("p");
        author.className = "sn-author";
        author.innerHTML = this.songData.author;
        infoContainer.appendChild(author);

        notification.appendChild(imageContainer);
        notification.appendChild(infoContainer);

        wrapper.appendChild(pobudkaContainer);
        wrapper.appendChild(notification);
        document.body.appendChild(wrapper);

        this.currentNotification = wrapper;

        // Ensure notification is removed if no valid song data is available after a set time
        if (this.notificationTimeout) {
            clearTimeout(this.notificationTimeout);
        }
        this.notificationTimeout = setTimeout(() => {
            this.removeNotification();
        }, 100000000); // Adjusted to 10 seconds for a more reasonable display time
    },

    removeNotification: function () {
        if (this.currentNotification) {
            document.body.removeChild(this.currentNotification);
            this.currentNotification = null;
        }
        if (this.notificationTimeout) {
            clearTimeout(this.notificationTimeout);
            this.notificationTimeout = null;
        }
    },

    getStyles: function () {
        return [
            "MMM-SongNotification.css",
        ];
    },

    removeInjectedCSS: function () {
        const injectedStyles = document.querySelectorAll('style[data-module="MMM-SongNotification"]');
        injectedStyles.forEach(style => style.parentNode.removeChild(style));
    },

    getDom: function () {
        var wrapper = document.createElement("div");

        return wrapper;
    }
});
