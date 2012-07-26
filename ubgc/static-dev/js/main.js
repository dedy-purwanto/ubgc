function resizeFrame(container, url) {
    var transport = new easyXDM.Socket(/** The configuration */{
        remote: url,
        container: container,
        onMessage: function(message, origin){
            this.container.getElementsByTagName("iframe")[0].style.height = message + "px";
        }
    });
}
