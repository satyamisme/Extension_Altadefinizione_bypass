async function main_donwload_film(){

    var arr_url = window.location.href.split("/")
    var type = arr_url[3]
    var id = arr_url[4]
    var response = await fetch("http://localhost:8080/video/type="+type+"&id="+id)
    var json = await response.json()
    var url_video = json.result_video.url
    
    window.open(url_video, "_blank");
}

chrome.runtime.onMessage.addListener( 
    function(request, sender, sendResponse) {
        if(request.message === "donwload_film"){
            main_donwload_film()
        }
    }
)