document.getElementById("donwload_film").addEventListener("click", function () {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { message: "donwload_film" }, function(response) {
        })
    })
})

