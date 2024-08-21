const NodeHelper = require("node_helper");
const request = require("request");

module.exports = NodeHelper.create({
    start: function () {
        console.log("Starting node helper for: " + this.name);
    },

    socketNotificationReceived: function (notification, payload) {
        if (notification === "GET_SONG_DATA") {
            this.getSongData(payload);
        }
    },

    getSongData: function (apiUrl) {
        var self = this;
        request(apiUrl, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                var data = JSON.parse(body);
                self.sendSocketNotification("SONG_DATA", data);
            } else {
                //console.error("Error fetching data: " + error);
                self.sendSocketNotification("SONG_DATA", {});
            }
        });
    }
});
