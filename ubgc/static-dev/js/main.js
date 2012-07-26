first_time = true;
function resizeFrame(container, url) {
    var transport = new easyXDM.Socket(/** The configuration */{
        remote: url,
        container: container,
        onMessage: function(message, origin){
            if(first_time == true){
                this.container.getElementsByTagName("iframe")[0].style.height = (message + 50) + "px";
                first_time = false;
            }
        }
    });
}
